import asyncio
from typing import List, Optional
from tornado.httputil import HTTPServerRequest
from tornado.web import RequestHandler, HTTPError
import os
import zlib
import subprocess
import tornado.ioloop
from tornado.iostream import IOStream
from grader.service.handlers.git.git_base_handler import GitBaseHandler


class FileWrapper:
    """Wraps a file and communicates with HTTP client"""

    def __init__(
        self, handler: RequestHandler, filename: str, headers: Optional[dict] = None
    ) -> None:
        if headers is None:
            headers = {}

        self.headers: dict = headers.copy()
        self.handler: RequestHandler = handler
        self.request: HTTPServerRequest = handler.request

        try:
            self.file = open(filename, "rb")
            filesize = os.path.getsize(filename)
        except:
            raise HTTPError(500, "Unable to open file")

        self.headers.update(
            {
                "Date": GitBaseHandler.get_date_header(),
            }
        )
        for k, v in self.headers.items():
            self.handler.set_header(k, v)
        self.write_chunk()

    def write_chunk(self):
        data: bytes = self.file.read(8192)
        if data == "":
            # EOF
            self.file.close()
            # TODO: what to do here???
            # self.request.finish()
            return
        # write data to client and continue when data has been written
        self.handler.write(data)
        self.handler.flush()
        self.write_chunk()


class ProcessWrapper:
    """Wraps a subprocess and communicates with HTTP client

    Supports gzip compression and chunked transfer encoding
    """

    reading_chunks = False
    got_chunk = False
    headers_sent = False
    got_request = False
    sent_chunks = False

    number_of_8k_chunks_sent = 0

    gzip_decompressor = None
    gzip_header_seen = False

    process_input_buffer = ""

    output_prelude = ""

    def __init__(
        self,
        handler: RequestHandler,
        command: List[str],
        headers: dict,
        output_prelude: str = "",
    ):
        self.handler = handler
        self.request = handler.request
        self.headers = headers
        self.output_prelude = output_prelude

        # invoke process
        self.process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            env=os.environ,
        )

        # check return status
        if self.process.poll() is not None:
            raise HTTPError(500, "subprocess returned prematurely")

        # get fds
        self.fd_stdout = self.process.stdout.fileno()
        self.fd_stderr = self.process.stderr.fileno()
        self.fd_stdin = self.process.stdin.fileno()

        self.ioloop = tornado.ioloop.IOLoop.current()
        self.ioloop.add_handler(
            self.fd_stdout,
            self._handle_stdout_event,
            self.ioloop.READ | self.ioloop.ERROR,
        )
        self.ioloop.add_handler(
            self.fd_stderr,
            self._handle_stderr_event,
            self.ioloop.READ | self.ioloop.ERROR,
        )
        self.ioloop.add_handler(
            self.fd_stdin,
            self._handle_stdin_event,
            self.ioloop.WRITE | self.ioloop.ERROR,
        )

        self.finish_state = asyncio.get_event_loop().create_future()

        # is it gzipped? If yes, we initialize a zlib decompressobj
        if (
            "gzip" in self.request.headers.get("Content-Encoding", "").lower()
        ):  # HTTP/1.1 RFC says value is case-insensitive
            self.gzip_decompressor = zlib.decompressobj(
                16 + zlib.MAX_WBITS
            )  # skip the gzip header

        if self.request.method == "POST":
            # Handle chunked encoding
            if (
                self.request.headers.get("Expect", None) == "100-continue"
                and self.request.headers.get("Transfer-Encoding", None) == "chunked"
            ):
                self.httpstream: IOStream = self.request.connection.stream
                self.handler.set_status(100)
                self.read_chunks()
            else:
                if self.gzip_decompressor:
                    assert self.request.body[:2] == "\x1f\x8b", "gzip header"
                    self.process_input_buffer = self.gzip_decompressor.decompress(
                        self.request.body
                    )
                else:
                    self.process_input_buffer = self.request.body
                self.got_request = True
        else:
            self.got_request = True

    async def read_chunks(self):
        """Read chunks from the HTTP client"""

        if self.reading_chunks and self.got_chunk:
            # we got on the fast-path and directly read from the buffer.
            # if we continue to recurse, this is going to blow up the stack.
            # so instead return
            #
            # NOTE: This actually is unnecessary as long as tornado guarantees that
            #       ioloop.add_callback always gets dispatched via the main io loop
            #       and they don't introduce a fast-path similar to read_XY
            return

        while not self.got_request:
            self.reading_chunks = True
            self.got_chunk = False
            # chunk starts with length, so read it
            data: bytes = await self.httpstream.read_until("\r\n")
            self._chunk_length(data)
            self.reading_chunks = False

            if self.got_chunk:
                # the previous read hit the fast path and read from the buffer
                # instead of going through the main polling loop. This means we
                # should iteratively issue the next request
                continue
            else:
                break

        # if we arrive here, we read the complete request or
        # the ioloop has scheduled another call to read_chunks
        return

    async def _chunk_length(self, data):
        """Received the chunk length"""

        assert data[-2:] == "\r\n", "CRLF"

        length = data[:-2].split(";")[0]  # cut off optional length paramters
        length = int(length.strip(), 16)  # length is in hex

        if length:
            read_data: bytes = await self.httpstream.read_bytes(length + 2)
            self._chunk_data(read_data)
        else:
            self.got_request = True
            # enable input write event so the handler can finish things up
            # when it has written all pending data
            self.ioloop.update_handler(
                self.fd_stdin, self.ioloop.WRITE | self.ioloop.ERROR
            )

    def _chunk_data(self, data: bytes):
        """Received chunk data"""

        assert data[-2:] == "\r\n", "CRLF"

        if self.gzip_decompressor:
            if not self.gzip_header_seen:
                assert data[:2] == "\x1f\x8b", "gzip header"
                self.gzip_header_seen = True

            self.process_input_buffer += self.gzip_decompressor.decompress(data[:-2])
        else:
            self.process_input_buffer += data[:-2]

        self.got_chunk = True

        if self.process_input_buffer:
            # since we now have data in the buffer, enable write events again
            self.ioloop.update_handler(
                self.fd_stdin, self.ioloop.WRITE | self.ioloop.ERROR
            )

        # do NOT call read_chunks directly. This is to give git a chance to consume input.
        # we don't want to grow the buffer unnecessarily.
        # Additionally, this should mitigate the stack explosion mentioned in read_chunks
        self.ioloop.add_callback(self.read_chunks)

        # maybe better alternative:
        # self.ioloop.add_future(somehow_previous_read_chunks_future, self.read_chunks)

    def _handle_stdin_event(self, fd, events):
        """Eventhandler for stdin"""

        assert fd == self.fd_stdin

        if events & self.ioloop.ERROR:
            # An error at the end is expected since tornado maps HUP to ERROR
            # ensure pipe is closed
            if not self.process.stdin.closed:
                self.process.stdin.close()
            # remove handler
            self.ioloop.remove_handler(self.fd_stdin)
            # if all fds are closed, we can finish
            return self._graceful_finish()

        # got data ready
        if self.process_input_buffer:
            count = os.write(fd, self.process_input_buffer)
            self.process_input_buffer = self.process_input_buffer[count:]

        if not self.process_input_buffer:
            # consumed everything in the buffer
            if self.got_request:
                # we got the request and wrote everything to the process
                # this means we can close stdin and stop handling events
                # for it
                self.process.stdin.close()
                self.ioloop.remove_handler(fd)
            else:
                # There is more data bound to come from the client
                # so just disable write events for the moment until
                # we got more to write
                self.ioloop.update_handler(fd, self.ioloop.ERROR)

    def _handle_stdout_event(self, fd, events):
        """Eventhandler for stdout"""

        assert fd == self.fd_stdout

        if events & self.ioloop.READ:
            # got data ready to read
            data = ""

            # Now basically we have two cases: either the client supports
            # HTTP/1.1 in which case we can stream the answer in chunked mode
            # in HTTP/1.0 we need to send a content-length and thus buffer the complete output
            if self.request.version == "HTTP/1.1":
                if not self.headers_sent:
                    self.sent_chunks = True
                    self.headers.update(
                        {
                            "Date": GitBaseHandler.get_date_header(),
                        }
                    )
                    for k, v in self.headers.items():
                        self.handler.set_header(k, v)

                    if self.output_prelude and len(self.output_prelude) > 0:
                        data += self.output_prelude + "\r\n"

                    self.headers_sent = True

                payload: bytes = os.read(fd, 8192)
                if (
                    events & self.ioloop.ERROR
                ):  # there might be data remaining in the buffer if we got HUP, get it all
                    remainder = True
                    while remainder != "":  # until EOF
                        remainder = os.read(fd, 8192)
                        payload += remainder

                if len(payload) > 0:
                    data += payload.decode("ascii") + "\r\n"

            else:
                if not self.headers_sent:
                    # Use the over-eager blocking read that will get everything until we hit EOF
                    # this might actually be somewhat dangerous as noted in the subprocess documentation
                    # and lead to a deadlock. This is only a legacy mode for HTTP/1.0 clients anyway,
                    # so we might want to remove it entirely anyways
                    payload = self.process.stdout.read()
                    self.headers.update(
                        {
                            "Date": GitBaseHandler.get_date_header(),
                        }
                    )
                    for k, v in self.headers.items():
                        self.handler.set_header(k, v)
                    # self.handler.set_header("Content-Length", None)

                    self.headers_sent = True
                    data += self.output_prelude + payload
                else:
                    # this is actually somewhat illegal as it messes with content-length but
                    # it shouldn't happen anyways, as the read above should have read anything
                    # python docs say this can happen on ttys...
                    data = self.process.stdout.read()

            if len(data) == 8200:
                self.number_of_8k_chunks_sent += 1
            else:
                if self.number_of_8k_chunks_sent > 0:
                    self.number_of_8k_chunks_sent = 0

            self.handler.write(data)
            self.handler.flush()

        # now we can also have an error. This is because tornado maps HUP onto error
        # therefore, no elif here!
        if events & self.ioloop.ERROR or self.process.poll() is not None:
            # ensure file is closed
            if not self.process.stdout.closed:
                self.process.stdout.close()
            # remove handler
            self.ioloop.remove_handler(self.fd_stdout)
            # if all fds are closed, we can finish
            return self._graceful_finish()

    def _handle_stderr_event(self, fd, events):
        """Eventhandler for stderr"""

        assert fd == self.fd_stderr

        if events & self.ioloop.READ:
            # got data ready
            if not self.headers_sent:
                payload = self.process.stderr.read()

                self.handler.set_status(500)
                self.headers_sent = True
                data = payload.decode("ascii")
            else:
                # see stdout
                data = self.process.stderr.read()

            self.handler.write(data)
            self.handler.flush()

        # TODO: what if there is still data on the outputs but we are closing because of process.poll()?
        if events & self.ioloop.ERROR or self.process.poll() is not None:
            # ensure file is closed
            if not self.process.stderr.closed:
                self.process.stderr.close()
            # remove handler
            self.ioloop.remove_handler(self.fd_stderr)
            # if all fds are closed, we can finish
            return self._graceful_finish()

    def _graceful_finish(self):
        """Detect if process has closed pipes and we can finish"""

        if not self.process.stdout.closed or not self.process.stderr.closed:
            return  # stdout/stderr still open

        if not self.process.stdin.closed:
            self.process.stdin.close()

        if not self.headers_sent:
            retval = self.process.poll()
            if retval != 0:
                payload = "Did not produce any data. Errorcode: " + str(retval)
                self.handler.set_status(500)
                self.headers_sent = True
                data = payload
                self.handler.write(data)
                self.handler.flush()
            else:
                self.handler.set_status(200)
                self.headers_sent = True

        # if we are in chunked mode, send end chunk with length 0
        # elif self.sent_chunks:
        # self.handler.write("0\r\n") # TODO: uncomment?
        # we could now send some more headers resp. trailers
        # self.handler.write("\r\n")

        # self.request.finish()
        self.finish_state.set_result(True)

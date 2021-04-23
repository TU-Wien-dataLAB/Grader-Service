import base64

#for strings
def encode_strings(content: str) -> str:
    asciicontent = content.encode('ascii')
    encodedContent = base64.b64encode(asciicontent)
    #make it human readable
    encodedContent = encodedContent.decode('ascii')
    return encodedContent

#for binaries
def encode_binary(binary: bytes) -> str:
    encodedContent = base64.b64encode(binary)
    #make it human readable
    encodedContent = encodedContent.decode('utf-8')
    return encodedContent

def decode_strings(encoded: str) -> str:
    base64bytes = encoded.encode('ascii')
    decoded = base64.b64decode(base64bytes)
    content = decoded.decode('ascii')
    return content

def decode_binary(encoded: str) -> bytes:
    filebytes = encoded.encode('utf-8')
    binary = base64.decodebytes(filebytes)
    return binary

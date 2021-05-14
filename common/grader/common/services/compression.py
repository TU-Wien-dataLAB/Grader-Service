# this module will use gzip compression with a low compression level because gzip is significantly faster for compression with acceptable size and also for decompression.
# see: https://tukaani.org/lzma/benchmarks.html

import tarfile
import os
import os.path as osp
import io
from grader.common.models.assignment import Assignment
from grader.common.models.lecture import Lecture
from grader.common.models.user import User
from grader.common.models.submission import Submission

from traitlets.config.configurable import LoggingConfigurable
from traitlets.traitlets import Int, TraitError, Unicode, validate

class CompressionEngine(LoggingConfigurable):

  compression_dir = Unicode('', help="The absolute path to the directory where the archives should be written.").tag(config=True)
  compression_algo = Unicode('gz', help="The compression algorithm to use. Either: '', 'gz', 'bz' or 'xz'").tag(config=True)
  compression_level = Int(2).tag(config=True)

  def __init__(self, compression_dir: str, **kwargs):
      super().__init__(**kwargs)
      self.compression_dir = compression_dir

  async def create_archive(self, name: str, path: str) -> str:
    file_name = osp.join(self.compression_dir, name + self.extension)

    directory = osp.dirname(file_name)
    if not osp.exists(directory):
        os.makedirs(directory)

    path = osp.abspath(path)
    with tarfile.open(file_name, 'w:'+self.compression_algo) as tar:
      tar.add(path, arcname=osp.basename(path))
    return file_name
  
  async def read_archive(self, src: str) -> bytes:
    if not tarfile.is_tarfile(src):
      raise ValueError(f"The path {src} is not a tar file.")
    with open(src, "rb") as f:
      data = f.read()
    return data
  
  async def unpack_archive(self, archive: bytes, dst: str, archive_name: str):
    if not osp.isdir(dst):
      raise ValueError(f"The path {dst} is not a direcotry.")
    file_obj = io.BytesIO(archive)
    with tarfile.open(fileobj=file_obj) as tar:
      archive_dir = dst + "/" + archive_name
      os.mkdir(archive_dir)
      tar.extractall(path=archive_dir)

  async def archive_assignment(self, lecture: Lecture, assignment: Assignment, dir: str) -> str:
    return self.create_archive("assignments/" + lecture.name + "/" + assignment.name, dir)

  async def archive_submission(self, user: User, assignment: Assignment, submission: Submission, dir: str) -> str:
    return self.create_archive("submissions/" + user.id + "/" + assignment.name + "/" + submission.id, dir)

  @property
  def extension(self):
    ext = ".tar"
    if self.compression_algo != "":
      ext += ("." + self.compression_algo)
    return ext

  
  @validate('compression_dir')
  def _validate_dir(self, proposal):
    path: str = proposal['value']
    if not osp.isabs(path):
      raise TraitError("The path is not absolute")
    if not osp.isdir(path):
      raise TraitError("The path has to be an existing directory")
    return proposal["value"]
  
  @validate('compression_algo')
  def _validate_algo(self, proposal):
    algo: str = proposal['value']
    if algo not in {'', 'gz', 'bz', 'xz'}:
      raise TraitError("Incorrect compression algorithm")
    return proposal["value"]
  
  @validate("compression_level")
  def _validate_level(self, proposal):
    level = proposal["value"]
    if not 0 <= level <= 9:
      raise TraitError("Compression level has to be between 0 and 9.")
    return level


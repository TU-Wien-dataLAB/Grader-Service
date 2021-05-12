import pytest
from grader.common.services.compression import CompressionEngine
import os
from pathlib import Path
import asyncio

from traitlets.traitlets import TraitError

@pytest.mark.asyncio 
async def test_create_archive(tmp_path):
  path: Path = tmp_path / "base"
  path.mkdir()
  engine = CompressionEngine(os.path.abspath(path))
  
  test_dir: Path = tmp_path / "test"
  test_dir.mkdir()

  test_file = test_dir / "file.txt"
  test_file.write_text("File")


  archive_path = await engine.create_archive("test/archive", str(test_dir.resolve()))
  assert archive_path is not None
  file_path = Path(archive_path)
  assert file_path.exists()
  assert file_path.is_file()
  assert file_path.name == "archive" + engine.extension

def test_engine_compression_path_error():
  with pytest.raises(TraitError):
    CompressionEngine(compression_dir="~/hello")

  with pytest.raises(TraitError):
    CompressionEngine(compression_dir="./hello")
  
  with pytest.raises(TraitError):
    CompressionEngine(compression_dir="/does/not/exist")

@pytest.mark.asyncio 
async def test_read_archive(tmp_path):
  # create archive
  path: Path = tmp_path / "base"
  path.mkdir()
  engine = CompressionEngine(os.path.abspath(path))
  
  test_dir: Path = tmp_path / "test"
  test_dir.mkdir()

  test_file = test_dir / "file.txt"
  test_file.write_text("File")


  archive_path = await engine.create_archive("test/archive", str(test_dir.resolve()))
  data: bytes = await engine.read_archive(archive_path)
  assert data is not None
  assert type(data) == bytes
  assert data != b""

@pytest.mark.asyncio 
async def test_unpack_archive(tmp_path):
  # create archive
  path: Path = tmp_path / "base"
  path.mkdir()
  engine = CompressionEngine(os.path.abspath(path))
  
  test_dir: Path = tmp_path / "test"
  test_dir.mkdir()

  test_file = test_dir / "file.txt"
  test_file.write_text("File")

  archive_path = await engine.create_archive("test/archive", str(test_dir.resolve()))
  data: bytes = await engine.read_archive(archive_path)
  
  unpack_dir: Path = tmp_path / "unpack"
  unpack_dir.mkdir()

  await engine.unpack_archive(data, str(unpack_dir), "archive")

  assert (unpack_dir / "archive").is_dir()
  assert (unpack_dir / "archive" / "test").is_dir()
  assert (unpack_dir / "archive" / "test" / "file.txt").is_file()



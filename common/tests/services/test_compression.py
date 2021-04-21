import pytest
from grader.common.services.compression import CompressionEngine
import os
from pathlib import Path

def test_create_archive(tmp_path):
  path: Path = tmp_path / "base"
  path.mkdir()
  engine = CompressionEngine(os.path.abspath(path))
  
  test_dir: Path = tmp_path / "test"
  test_dir.mkdir()

  test_file = test_dir / "file.txt"
  test_file.write_text("File")


  archive_path = engine.create_archive("test/archive", str(test_dir.resolve()))
  assert archive_path is not None
  file_path = Path(archive_path)
  assert file_path.exists()
  assert file_path.is_file()
  assert file_path.name == "archive" + engine.extension
  
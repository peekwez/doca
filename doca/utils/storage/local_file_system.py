import os
from glob import glob
from enum import StrEnum
from pathlib import Path

from typing import Iterable, List, Any

from ..helpers import get_bucket_name, getenv
from ..providers import StorageProvider
from .base import BaseStorageLayer


class FileMode(StrEnum):
    RB = "rb"
    WB = "wb"


class FileObject:
    def __init__(self, home: str, bucket_name: str, key: str):
        self.bucket = bucket_name
        self.key = key
        self.__home = home
        self.__file_path = os.path.join(self.__home, self.bucket, self.key)
        self.__file_head, _ = os.path.split(self.__file_path)

    def get(self) -> bytes:
        with open(self.__file_path, FileMode.RB.value) as f:
            content = f.read()
        return content

    def put(self, content: bytes) -> None:
        if self.__file_head not in ["", None]:
            Path(self.__file_head).mkdir(parents=True, exist_ok=True)
        with open(self.__file_path, FileMode.WB.value) as f:
            f.write(content)


class LocalFileSystem(BaseStorageLayer):
    name: StorageProvider = StorageProvider.local_file_system

    def setup(self):
        self.__home = getenv("LOCAL_STORAGE_PATH")
        bucket_name = get_bucket_name()
        bucket_path = f"{self.__home}/{bucket_name}"
        try:
            Path(bucket_path).mkdir(parents=True)
            self._log.info(f"Bucket `{bucket_name}` created...")
        except:
            self._log.warning(f"Bucket `{bucket_name}` already exists...")
        finally:
            self._log.info("File system store initialized...")

    def list(self, storage_bucket: str, prefix: str, delimiter: str | None = None) -> Iterable:
        if prefix == "":
            prefix = "*"
        path_ = f"{self.__home}/{storage_bucket}/{prefix}/*"
        keys = [
            f"{file.split(f'{storage_bucket}{os.sep}')[-1]}" for file in glob(path_)]
        for key in keys:
            yield FileObject(self.__home, bucket_name=storage_bucket, key=key)

    def download(self, obj: FileObject) -> bytes:
        return obj.get()

    def get_object(self, storage_bucket: str, document_path: str) -> FileObject:
        return FileObject(self.__home, bucket_name=storage_bucket, key=document_path)

    def read(self, storage_bucket: str, document_path: str) -> bytes:
        obj = self.get_object(storage_bucket, document_path)
        return self.download(obj)

    def write(self, content: bytes, mime_type: str | None, storage_bucket: str, document_path: str) -> None:
        obj = self.get_object(storage_bucket, document_path)
        obj.put(content)

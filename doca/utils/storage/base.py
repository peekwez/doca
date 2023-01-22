import abc
from enum import StrEnum, auto
from typing import Any

from ..logging import get_class_logger
from ..document import Document


class StorageProvider(StrEnum):
    aws_s3 = auto()
    gcp_cloud_storage = auto()
    azure_blob_storage = auto()
    local_file_system = auto()


class BaseStorageLayer(abc.ABC):
    name: None

    def __init__(self, debug: bool = False):
        self._log = get_class_logger(self)
        if not debug:
            self.setup()

    @abc.abstractmethod
    def setup(self):
        pass

    @abc.abstractmethod
    def list(self, bucket_name: str, prefix: str, delimiter: str = None) -> list:
        pass

    @abc.abstractmethod
    def download(self, obj: Any) -> bytes:
        pass

    @abc.abstractmethod
    def get_object(self, doc: Document) -> Any:
        pass

    @abc.abstractmethod
    def read(self, doc: Document) -> Document:
        pass

    @abc.abstractmethod
    def write(self, doc: Document) -> bool:
        pass

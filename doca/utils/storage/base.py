import abc
from typing import Any

from ..logging import get_class_logger


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
    def list(self, storage_bucket: str, prefix: str, delimiter: str = None) -> list:
        pass

    @abc.abstractmethod
    def download(self, obj: Any) -> bytes:
        pass

    @abc.abstractmethod
    def get_object(self, storage_bucket: str, document_path: str) -> Any:
        pass

    @abc.abstractmethod
    def read(self, storage_bucket: str, document_path: str) -> bytes:
        pass

    @abc.abstractmethod
    def write(self, content: bytes, mime_type: str, storage_bucket: str, document_path: str) -> None:
        pass

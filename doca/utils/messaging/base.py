import abc
from typing import Callable

from ..logging import get_logger


class BaseMessageLayer(abc.ABC):
    name: None

    def __init__(self, consume_queue: str | None = None, publish_queue: str | None = None, debug: bool = False):
        self._log = get_logger(self.__class__.__name__)
        self._consume_queue = consume_queue
        self._publish_queue = publish_queue
        if not debug:
            self.setup()

    @abc.abstractmethod
    def setup(self):
        pass

    @abc.abstractmethod
    def consume(self, callback: Callable[[str | bytes], None]) -> None:
        pass

    @abc.abstractmethod
    def publish(self, body: str) -> None:
        pass

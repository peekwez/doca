import abc
from typing import Callable

from ..logging import get_class_logger
from ..event import EventRecord


class BaseMessageLayer(abc.ABC):
    name: None

    def __init__(self, consume_queue: str, publish_queue: str, debug: bool = False):
        self._log = get_class_logger(self)
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
    def publish(self, record: EventRecord) -> None:
        pass

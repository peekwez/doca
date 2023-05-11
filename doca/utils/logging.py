import logging
from typing import Callable

LOG_FORMAT = "[%(asctime)s] [%(process)s] [%(levelname)s] [%(name)s]: %(message)s"


def get_logger(name: str = "Document Analysis", log_level: int = logging.INFO) -> logging.Logger:

    log = logging.getLogger(name)
    fmt = logging.Formatter(LOG_FORMAT)
    log.setLevel(log_level)

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)

    log.addHandler(ch)

    return log


def get_class_logger(cls: Callable) -> logging.Logger:
    return get_logger(cls.__class__.__name__)

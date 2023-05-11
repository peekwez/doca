import os
import sys
import uuid
import time

from typing import Any

from . import exceptions as exc


def getenv(env_name: str, default_value: str = None) -> str:
    try:
        return os.environ[env_name]
    except KeyError:
        if default_value is not None:
            return default_value
        raise exc.MissingEnvironmentVariable(
            f"Environment variable `{env_name}` is not available")


def new_guid() -> str:
    return uuid.uuid4().hex


def time_ns() -> int:
    return time.time_ns()


def get_size(data: bytes) -> int:
    return sys.getsizeof(data)


def chunk_list(lst: list[Any], n: int) -> list[list[Any]]:
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_bucket_name() -> str:
    return getenv("PROJECT_NAME", "")


def get_processor_name() -> str:
    return getenv("PROCESSOR_NAME", "")


def get_consumer_name() -> str:
    return f'{getenv("PROJECT_NAME")}-{getenv("CONSUME_FROM")}'


def get_producer_name() -> str:
    return f'{getenv("PROJECT_NAME")}-{getenv("PRODUCE_TO")}'

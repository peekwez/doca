from azure.storage.queue import (
    QueueClient, BinaryBase64DecodePolicy,
    BinaryBase64EncodePolicy,
)
from azure.core import exceptions
from typing import Callable, Any

from ..helpers import getenv
from ..providers import MessageProvider
from .base import BaseMessageLayer


class AzureStorageQueue(BaseMessageLayer):
    name: MessageProvider = MessageProvider.azure_storage_queue

    def setup(self) -> None:
        if self._consume_queue:
            self.consumer = self.__get_client(
                self._consume_queue.replace("_", "-"))

        if self._publish_queue:
            self.publisher = self.__get_client(
                self._publish_queue.replace("_", "-"))

    def __get_client(self, queue_name) -> Any:
        client = QueueClient.from_connection_string(
            getenv("AZURE_STORAGE_CONNECTION_STRING"),
            queue_name=queue_name,
            message_encode_policy=BinaryBase64EncodePolicy(),
            message_decode_policy=BinaryBase64DecodePolicy()
        )
        try:
            client.create_queue()
            self._log.info(f"Queue `{queue_name}` created ...")
        except exceptions.ResourceExistsError:
            self._log.warning(f"Queue `{queue_name}` already exists ...")
        finally:
            self._log.info("Storage queue client initialized...")
        return client

    def consume(self, callback: Callable[[str | bytes], None]) -> None:
        while True:
            messages = self.consumer.receive_messages()
            for message in messages:
                callback(message.content.decode("utf-8"))
                self.consumer.delete_message(message.id, message.pop_receipt)

    def publish(self, body: str) -> None:
        self.publisher.send_message(body.encode("utf-8"))

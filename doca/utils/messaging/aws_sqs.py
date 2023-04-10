import boto3
from typing import Callable, Any

from ..providers import MessageProvider
from .base import BaseMessageLayer


class AWSSimpleQueueService(BaseMessageLayer):
    name: MessageProvider = MessageProvider.aws_sqs

    def setup(self) -> None:
        self.__sqs = boto3.resource("sqs")

        if self._consume_queue:
            self.consumer = self.__get_client(self._consume_queue)

        if self._publish_queue:
            self.publisher = self.__get_client(self._publish_queue)

    def __get_client(self, queue_name) -> Any:
        try:
            _ = self.__sqs.get_queue_by_name(QueueName=queue_name)
            self._log.warning(f"Queue `{queue_name}` already exists ...")
        except self.__sqs.meta.client.exceptions.QueueDoesNotExist:
            self.__sqs.create_queue(QueueName=f"{queue_name}")
            self._log.info(f"Created queue `{queue_name}` ...")
        finally:
            client = self.__sqs.get_queue_by_name(QueueName=queue_name)
            self._log.info("SQS queue client initialized...")
        return client

    def consume(self, callback: Callable[[str | bytes], None]) -> None:
        while True:
            messages = self.consumer.receive_messages(
                MaxNumberOfMessages=10, WaitTimeSeconds=1)
            for message in messages:
                callback(message.data)
                message.delete()

    def publish(self, body: str) -> None:
        self.publisher.send_message(MessageBody=body, MessageAttributes={})

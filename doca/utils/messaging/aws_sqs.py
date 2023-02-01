
import boto3
from typing import Callable, Any

from ..providers import MessageProvider
from .base import BaseMessageLayer


class AWSSimpleQueueService(BaseMessageLayer):
    name = MessageProvider.aws_sqs

    def setup(self) -> None:
        self._sqs = boto3.resource("sqs")
        self.con = self.__get_queue(self._consume_queue)
        self.pub = self.__get_queue(self._publish_queue)

    def __get_queue(self, queue_name) -> Any:
        try:
            _ = self._sqs.get_queue_by_name(QueueName=queue_name)
            self._log.warning(f"Queue `{queue_name}` already exists ...")
        except self._sqs.meta.client.exceptions.QueueDoesNotExist:
            self._sqs.create_queue(QueueName=f"{queue_name}")
            self._log.info(f"Created queue `{queue_name}` ...")
        finally:
            self._queue = self._sqs.get_queue_by_name(QueueName=queue_name)
            self._log.info("SQS queue client initialized...")

    def consume(self, callback: Callable[[str, bytes], None]) -> None:
        while True:
            messages = self.con.receive_messages(
                MaxNumberOfMessages=10, WaitTimeSeconds=1)
            for message in messages:
                callback(message.data)
                message.delete()

    def publish(self, body: bytes) -> None:
        self.pub.send_message(MessageBody=body, MessageAttributes={})

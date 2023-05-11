import json

from google.cloud import pubsub_v1
from google.api_core import exceptions, retry

from typing import Callable, Any

from ..helpers import getenv
from ..providers import MessageProvider
from .base import BaseMessageLayer


class GoogleCloudPubSub(BaseMessageLayer):
    name = MessageProvider.google_cloud_pubsub

    def setup(self) -> None:
        with open(getenv("GOOGLE_APPLICATION_CREDENTIALS"), "r") as f:
            self.__project_id = json.load(f)["project_id"]

        if self._consume_queue:
            self.consumer = self.__get_client(
                self._consume_queue, is_subscriber=True)

        if self._publish_queue:
            self.publisher = self.__get_client(self._publish_queue)

    def __get_client(self, queue_name, is_subscriber=False) -> Any:
        client = pubsub_v1.PublisherClient()
        topic_path = client.topic_path(self.__project_id, queue_name)

        try:
            _ = client.create_topic(request={"name": topic_path})
            self._log.info(f"Topic `{queue_name}` created ...")
        except exceptions.AlreadyExists:
            self._log.warning(f"Topic `{queue_name}` already exists ...")
        finally:
            self._log.info("Cloud PubSub client initialized...")

        if not is_subscriber:
            return client

        try:
            client = pubsub_v1.SubscriberClient()
            subscriber_path = client.subscription_path(
                self.__project_id, queue_name)
            client.create_subscription(
                request={
                    "name": subscriber_path,
                    "topic": topic_path,
                    "enable_exactly_once_delivery": True,
                    "ack_deadline_seconds": 180,
                }
            )
            self._log.info(f"Subscription `{queue_name}` created ...")
        except exceptions.AlreadyExists:
            self._log.info(f"Subscription `{queue_name}` created ...")
        finally:
            self._log.info("Cloud PubSub client initialized...")
        return client

    def consume(self, callback: Callable[[str, bytes], None]) -> None:
        NUM_MESSAGES = 10
        subscriber_path = self.consumer.subscription_path(
            self.__project_id, self._consume_queue)
        with self.consumer:
            while True:
                response = self.con.pull(
                    request=dict(subscription=subscriber_path,
                                 max_messages=NUM_MESSAGES),
                    retry=retry.Retry(deadline=300)
                )
                ack_ids = []
                for message in response.received_messages:
                    callback(message.message.data)
                    ack_ids.append(message.ack_id)

                if ack_ids:
                    request = dict(subscription=subscriber_path,
                                   ack_ids=ack_ids)
                    self.consumer.acknowledge(request=request)

    def publish(self, body: bytes) -> None:
        topic_path = self.publisher.topic_path(
            self.__project_id, self._publish_queue)
        future = self.pub.publish(topic_path, body)
        future.result(timeout=30)

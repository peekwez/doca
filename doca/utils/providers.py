from enum import StrEnum, auto


class StorageProvider(StrEnum):
    aws_s3 = auto()
    gcp_cloud_storage = auto()
    azure_blob_storage = auto()
    local_file_system = auto()


class MessageProvider(StrEnum):
    aws_sqs = auto()
    gcp_pubsub = auto()
    azure_queue_storage = auto()
    rabbitmq = auto()

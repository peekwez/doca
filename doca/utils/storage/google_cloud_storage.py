from typing import Iterable
from google.cloud import storage  # type: ignore
from google.cloud.storage.constants import PUBLIC_ACCESS_PREVENTION_ENFORCED
from google.api_core import exceptions

from ..helpers import get_bucket_name
from ..providers import StorageProvider
from .base import BaseStorageLayer


class GoogleCloudStorage(BaseStorageLayer):
    name: StorageProvider = StorageProvider.google_cloud_storage

    def setup(self):
        bucket_name = get_bucket_name()
        self._client = storage.Client()
        bucket = self._client.bucket(bucket_name)
        bucket.storage_class = "STANDARD"
        bucket.iam_configuration.uniform_bucket_level_access_enabled = True
        bucket.iam_configuration.public_access_prevention = PUBLIC_ACCESS_PREVENTION_ENFORCED
        try:
            self._client.create_bucket(
                bucket, location="northamerica-northeast2")
            self._log.info(f"Bucket `{bucket_name}` created...")
        except exceptions.Conflict:
            self._log.warning(f"Bucket `{bucket_name}` already exists...")
        finally:
            self._log.info("Cloud Storage initialized...")

    def list(self, storage_bucket: str, prefix: str, delimiter: str | None = None) -> Iterable:
        return self._client.list_blobs(storage_bucket, prefix=prefix, delimiter=delimiter)

    def download(self, obj) -> bytes:
        return obj.download_as_string()

    def get_object(self, storage_bucket: str, document_path: str):
        bucket = self._client.bucket(storage_bucket)
        return bucket.blob(document_path)

    def read(self, storage_bucket: str, document_path: str) -> bytes:
        obj = self.get_object(storage_bucket, document_path)
        return self.download(obj)

    def write(self, content: bytes, mime_type: str | None, storage_bucket: str, document_path: str) -> None:
        obj = self.get_object(storage_bucket, document_path)
        obj.upload_from_string(content, mime_type)

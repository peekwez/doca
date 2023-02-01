from azure.storage.blob import BlobServiceClient, ContentSettings, BlobClient
from azure.core import exceptions

from ..helpers import get_bucket_name, getenv
from ..providers import StorageProvider
from .base import BaseStorageLayer


class AzureStorageBlob(BaseStorageLayer):
    name = StorageProvider.azure_storage_blob

    def setup(self):
        bucket_name = get_bucket_name()
        self._client = BlobServiceClient.from_connection_string(
            getenv("AZURE_STORAGE_CONNECTION_STRING"),
        )
        try:
            self._client.create_container(bucket_name)
            self._log.info(f"Bucket `{bucket_name}` created...")
        except exceptions.ResourceExistsError:
            self._log.warning(f"Bucket `{bucket_name}` already exists...")
        finally:
            self._log.info("Storage Blob initialized...")

    def list(self, storage_bucket: str, prefix: str, delimiter: str = None) -> list:
        container = self._client.get_container_client(storage_bucket)
        props = container.list_blobs(name_starts_with=prefix)
        for prop in props:
            yield self._client.get_blob_client(container=storage_bucket, blob=prop.name)

    def download(self, obj) -> bytes:
        return obj.download_blob().readall()

    def get_object(self, storage_bucket: str, document_path: str):
        return self._client.get_blob_client(container=storage_bucket, blob=document_path)

    def read(self, storage_bucket: str, document_path: str) -> bytes:
        obj = self.get_object(storage_bucket, document_path)
        return self.download(obj)

    def write(self, content: bytes, mime_type: str, storage_bucket: str, document_path: str) -> None:
        obj = self.get_object(storage_bucket, document_path)
        obj.upload_blob(
            content, content_settings=ContentSettings(mime_type), overwrite=True)

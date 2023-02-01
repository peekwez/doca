import boto3

from ..helpers import get_bucket_name
from ..providers import StorageProvider
from .base import BaseStorageLayer


class S3StorageLayer(BaseStorageLayer):
    name = StorageProvider.aws_s3

    def setup(self):
        self._s3 = boto3.resource("s3")
        bucket_name = get_bucket_name()
        try:
            config = dict(LocationConstraint="ca-central-1")
            self._s3.create_bucket(Bucket=bucket_name,
                                   CreateBucketConfiguration=config)
            self._log.info(f"Bucket `{bucket_name}` created...")
        except self._s3.meta.client.exceptions.BucketAlreadyOwnedByYou:
            self._log.warning(f"Bucket `{bucket_name}` exists...")
        finally:
            self._log.info(f"AWS S3 storage layer initialized...")

    def list(self, storage_bucket: str, prefix: str, delimiter: str = None) -> list:
        bucket = self._s3.Bucket(storage_bucket)
        objects = list(bucket.objects.filter(Prefix=prefix))
        return filter(lambda x: x.key != f"{prefix}/", objects)

    def download(self, obj) -> bytes:
        return obj.get()["Body"].read()

    def get_object(self, storage_bucket: str, document_path: str):
        return self._s3.Object(bucket_name=storage_bucket, key=document_path)

    def read(self, storage_bucket: str, document_path: str) -> bytes:
        obj = self.get_object(storage_bucket, document_path)
        return self.download(obj)

    def write(self, content: bytes, mime_type: str, storage_bucket: str, document_path: str) -> None:
        obj = self.get_object(storage_bucket, document_path)
        obj.put(Body=content, ContentType=mime_type)

import boto3

from ..helpers import get_bucket_name
from ..document import Document
from ..providers import StorageProvider
from .base import BaseStorageLayer


class S3StorageLayer(BaseStorageLayer):
    name = StorageProvider.aws_s3

    def setup(self):
        self.s3 = boto3.resource("s3")
        bucket_name = get_bucket_name()
        try:
            config = dict(LocationConstraint="ca-central-1")
            self.s3.create_bucket(Bucket=bucket_name,
                                  CreateBucketConfiguration=config)
            self._log.info(f"Bucket `{bucket_name}` created...")
        except self.s3.meta.client.exceptions.BucketAlreadyOwnedByYou:
            self._log.warning(f"Bucket `{bucket_name}` exists...")
        finally:
            self._log.info(f"AWS S3 storage layer initialized...")

    def list(self, bucket_name: str, prefix: str, delimiter: str = None) -> list:
        bucket = self.s3.Bucket(bucket_name)
        objects = list(bucket.objects.filter(Prefix=prefix))
        return filter(lambda x: x.key != f"{prefix}/", objects)

    def download(self, obj) -> bytes:
        return obj.get()["Body"].read()

    def get_object(self, doc: Document):
        return self.s3.Object(bucket_name=doc.storage_bucket, key=doc.document_path)

    def read(self, doc: Document) -> None:
        obj = self.get_object(doc)
        doc.add_content(self.download(obj))

    def write(self, doc: Document) -> None:
        obj = self.get_object(doc)
        obj.put(Body=doc.content, ContentType=doc.document_format.mime_type)

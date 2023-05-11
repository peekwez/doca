import io
import os

from enum import StrEnum, auto
from pydantic import BaseModel, Field

from .providers import StorageProvider
from .storage import BaseStorageLayer
from .helpers import get_bucket_name, get_processor_name


class DocumentFormat(StrEnum):
    none = ""
    png = auto()
    jpeg = auto()
    jpg = auto()
    bmp = auto()
    tiff = auto()
    gif = auto()
    pdf = auto()
    txt = auto()
    csv = auto()
    zip = auto()
    xls = auto()
    xlsx = auto()
    json = auto()
    pickle = auto()
    parquet = auto()

    @property
    def mime_type(self) -> str:
        match self:
            case "csv":
                return f"text/csv"
            case "txt" | "none":
                return f"text/plain"
            case "png" | "jpeg" | "jpg" | "tiff" | "gif":
                return f"image/{self}"
            case "xls":
                return "application/vnd.ms-excel"
            case "xlsx":
                return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            case _:
                return f"application/{self}"


class Document(BaseModel):
    storage_provider: StorageProvider
    storage_bucket: str = Field(default_factory=get_bucket_name)
    processor_name: str = Field(default_factory=get_processor_name)
    document_owner: str
    document_name: str
    document_format: DocumentFormat
    document_buffer: io.BytesIO | None

    class Config:
        arbitrary_types_allowed = True
        fields = {'document_buffer': {'exclude': True}}

    @property
    def mime_type(self) -> str:
        return self.document_format.mime_type

    @property
    def document_path(self) -> str:
        suffix = "_{0.processor_name}".format(
            self) if self.processor_name else ""
        return f"{self.document_owner}/{self.document_name}{suffix}.{self.document_format}"

    @property
    def content(self) -> bytes:
        if not self.document_buffer:
            return None
        return self.document_buffer.getvalue()

    def save(self, store: BaseStorageLayer):
        store.write(
            self.content, self.mime_type,
            self.storage_bucket, self.document_path
        )

    def read(self, store: BaseStorageLayer):
        content = store.read(
            self.storage_bucket, self.document_path
        )
        self.document_buffer = io.BytesIO(content)


def new_document(
    storage_provider: StorageProvider,
    document_owner: str,
    document_name: str,
    document_format: DocumentFormat = None,
    document_content: bytes = None
) -> Document:

    if not document_format:
        name, ext = os.path.splitext(document_name)
        document_name = name
        document_format = ext if ext == "" else ext[1:]

    document_buffer = None
    if document_content:
        document_buffer = io.BytesIO(document_content)

    return Document(
        storage_provider=storage_provider,
        document_owner=document_owner,
        document_name=document_name,
        document_format=document_format,
        document_buffer=document_buffer
    )

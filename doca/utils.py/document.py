import io
import os
from enum import StrEnum, auto
from pydantic import BaseModel, Field


from . import storage as st
from . import helpers as hp


class DocumentFormat(StrEnum):
    none = auto()
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
    storage_provider: st.StorageProvider
    storage_bucket: str = Field(default_factory=hp.get_bucket_name)
    processor_name: str = Field(default_factory=hp.get_processor_name)
    document_owner: str
    document_name: str
    document_format: DocumentFormat
    document_content: io.BytesIO | None

    class Config:
        arbitrary_types_allowed = True
        fields = {'document_content': {'exclude': True}}

    @property
    def file_path(self) -> str:
        suffix = "_{0.processor_name}".format(
            self) if self.processor_name else ""
        return f"{self.document_owner}/{self.document_name}{suffix}.{self.document_format}"

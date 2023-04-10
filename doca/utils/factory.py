import io
import os
from .providers import StorageProvider
from .document import Document, DocumentFormat
from .event import EventRecord, EventType


def new_document(
    storage_provider: StorageProvider,
    document_owner: str,
    document_name: str,
    document_format: DocumentFormat | None = None,
    document_content: bytes | None = None
) -> Document:

    if not document_format:
        name, ext = os.path.splitext(document_name)
        document_name = name
        document_format = DocumentFormat(ext if ext == "" else ext[1:])

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


def new_event(event: EventType, payload: list[Document]) -> EventRecord:
    return EventRecord(event=event, payload=payload)

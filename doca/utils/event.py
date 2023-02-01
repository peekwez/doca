from uuid import UUID
from enum import StrEnum
from pydantic import BaseModel, Field

from .document import Document
from .messaging import BaseMessageLayer
from .helpers import new_guid, time_ns


class EventType(StrEnum):
    DOCUMENT_CREATED = "document-created"
    DOCUMENT_INGESTED = "document-ingested"
    DOCUMENT_ANALYZED = "document-analyzed"
    DOCUMENT_PROCESSED = "document-processed"


class EventRecord(BaseModel):
    id: UUID = Field(default_factory=new_guid)
    event: EventType
    payload: list[Document]
    timestamp_ns: int = Field(default_factory=time_ns)

    def publish(self, messenger: BaseMessageLayer) -> None:
        messenger.publish(self.json().encode("uft-8"))


def new_event(event: EventType, payload: list[Document]) -> EventRecord:
    return EventRecord(event=event, payload=payload)

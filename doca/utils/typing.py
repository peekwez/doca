from typing import Type

from .document import Document
from .messaging.base import BaseMessageLayer
from .storage.base import BaseStorageLayer

PayloadType = list[Document]
ResourceType = Type[BaseMessageLayer | BaseStorageLayer]

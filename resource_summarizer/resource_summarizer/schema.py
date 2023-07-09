"""Schematic types for the resource summarizer."""

from typing import Any, Callable, Hashable, Sequence, Tuple

from llama_index import Document
from llama_index.schema import TextNode
from llama_index.indices.base import BaseIndex

Block = Sequence[TextNode]
Partition = Sequence[Block]
Layer = Tuple[Sequence[Document], BaseIndex[Any]]
PartitionStrategy = Callable[[Layer], Partition]
SummarizationStrategy = Callable[[Block], Document]
IndexStrategy = Callable[[Sequence[Document]], BaseIndex[Any]]
IngestionStrategy = Callable[[Hashable], Sequence[Document]]
PersistenceStrategy = Callable[[BaseIndex[Any]], None]

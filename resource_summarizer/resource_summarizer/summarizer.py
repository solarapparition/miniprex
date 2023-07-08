"""Creation of resource summarization."""

from dataclasses import dataclass
from typing import Any, Callable, Hashable, Sequence, Tuple, Union

from llama_index import Document
from llama_index.schema import TextNode
from llama_index.indices.base import BaseIndex
from llama_index.response.schema import RESPONSE_TYPE as LLAMA_INDEX_RESPONSE_TYPE

Block = Sequence[TextNode]
Partition = Sequence[Block]
Layer = Tuple[Sequence[Document], BaseIndex[Any]]
PartitionStrategy = Callable[[Layer], Partition]
SummarizationStrategy = Callable[[Block], Document]
IndexStrategy = Callable[[Sequence[Document]], BaseIndex[Any]]
IngestionStrategy = Callable[[Hashable], Sequence[Document]]
PersistenceStrategy = Callable[[BaseIndex[Any]], None]


def create_next_layer(
    current_layer: Layer,
    partition: PartitionStrategy,
    summarize: SummarizationStrategy,
    create_index: IndexStrategy,
) -> Layer:
    """Creates the next summarization layer."""

    blocks = partition(current_layer)
    next_layer_docs = [summarize(block) for block in blocks]
    next_layer_index = create_index(next_layer_docs)
    return next_layer_docs, next_layer_index


def create_layers(
    initial_docs: Sequence[Document],
    partition: PartitionStrategy,
    summarize: SummarizationStrategy,
    create_index: IndexStrategy,
    n_layers: Union[int, None] = None,
) -> Sequence[Layer]:
    """Creates a sequence of summarization layers."""

    layer_0 = initial_docs, create_index(initial_docs)
    layers = [layer_0]
    while not n_layers or len(layers) < n_layers:
        current_layer = layers[-1]
        current_layer_docs, _ = current_layer
        if len(current_layer_docs) == 1:
            break
        layers.append(
            create_next_layer(current_layer, partition, summarize, create_index)
        )
    return layers


@dataclass
class ResourceSummarizer:
    """Summarizes a resource."""

    layers: Sequence[Layer]
    """The layers of the resource."""

    @property
    def levels_of_detail(self) -> int:
        """The number of levels of detail that the resource has."""
        return len(self.layers)

    def query(
        self, query: str, level: int, **query_kwargs: Any
    ) -> LLAMA_INDEX_RESPONSE_TYPE:
        """Queries the resource at a given level of detail. The higher the level, the more detailed the answer is."""
        if level < 0:
            raise ValueError("Level must be non-negative.")
        if level > self.levels_of_detail:
            raise ValueError(
                f"Resource only has {self.levels_of_detail} levels of detail available."
            )
        _, index = self.layers[level]
        query_engine = index.as_query_engine(**query_kwargs)
        return query_engine.query(query)


def create_summarizer(
    resource_location: Hashable,
    ingest: IngestionStrategy,
    partition: PartitionStrategy,
    summarize: SummarizationStrategy,
    create_index: IndexStrategy,
    n_layers: Union[int, None] = None,
) -> ResourceSummarizer:
    """Create a resource summarizer."""

    docs = ingest(resource_location)
    layers = create_layers(docs, partition, summarize, create_index, n_layers)
    summarizer = ResourceSummarizer(layers)
    return summarizer

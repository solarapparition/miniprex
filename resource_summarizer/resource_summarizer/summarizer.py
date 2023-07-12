"""Creation of resource summarization."""

from dataclasses import dataclass
import logging
from typing import Any, Hashable, Sequence, Union

from llama_index import Document
from llama_index.response.schema import RESPONSE_TYPE as LLAMA_INDEX_RESPONSE_TYPE

from .schema import (
    IndexStrategy,
    IngestionStrategy,
    Layer,
    PartitionStrategy,
    SummarizationStrategy,
)

logging.basicConfig(level=logging.INFO)


def create_next_layer(
    current_layer: Layer,
    partition_strategy: PartitionStrategy,
    summarization_strategy: SummarizationStrategy,
    index_strategy: IndexStrategy,
) -> Layer:
    """Creates the next summarization layer."""

    blocks = partition_strategy(current_layer)
    next_layer_docs: Sequence[Document] = []

    for block in blocks:
        logging.info("Summarizing block %s/%s.", len(next_layer_docs) + 1, len(blocks))
        next_layer_docs.append(summarization_strategy(block))
    next_layer_index = index_strategy(next_layer_docs)
    return next_layer_docs, next_layer_index


def create_layers(
    initial_docs: Sequence[Document],
    partition_strategy: PartitionStrategy,
    summarization_strategy: SummarizationStrategy,
    index_strategy: IndexStrategy,
    n_layers: Union[int, None] = None,
) -> Sequence[Layer]:
    """Creates a sequence of summarization layers."""

    layer_0 = initial_docs, index_strategy(initial_docs)
    layers = [layer_0]
    while not n_layers or len(layers) < n_layers:
        current_layer = layers[-1]
        current_layer_docs, _ = current_layer
        if len(current_layer_docs) == 1:
            break
        logging.info("Creating layer %s.", len(layers) + 1)
        layers.append(
            create_next_layer(
                current_layer,
                partition_strategy,
                summarization_strategy,
                index_strategy,
            )
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
    *,
    ingestion_strategy: IngestionStrategy,
    partition_strategy: PartitionStrategy,
    summarization_strategy: SummarizationStrategy,
    indexing_strategy: IndexStrategy,
    n_layers: Union[int, None] = None,
) -> ResourceSummarizer:
    """Create a resource summarizer."""

    docs = ingestion_strategy(resource_location)
    layers = create_layers(
        docs, partition_strategy, summarization_strategy, indexing_strategy, n_layers
    )
    summarizer = ResourceSummarizer(layers)
    return summarizer

from typing import Sequence
from typing import Callable
from typing import Any


from llama_index.schema import TextNode
from llama_index.indices.base import BaseIndex

Block = Sequence[TextNode]
Partition = Sequence[Block]


from llama_index import Document

from typing import Tuple

Layer = Tuple[Sequence[Document], BaseIndex[Any]]
PartitionStrategy = Callable[[Layer], Partition]
SummarizationStrategy = Callable[[Block], Document]
IndexStrategy = Callable[[Sequence[Document]], BaseIndex[Any]]


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
    # layers = [initial_layer]
    # for _ in range(n_layers):
    #     current_layer = layers[-1]
    #     last_layer_docs, _ = current_layer
    #     if len(last_layer_docs) == 1:
    #         break
    #     layers.append(create_next_layer(current_layer, partition, summarize, create_index))

    # return layers


# from llama_index.node_parser import NodeParser
from typing import Hashable

IngestionStrategy = Callable[[Hashable], Sequence[Document]]
PersistenceStrategy = Callable[[BaseIndex[Any]], None]

from llama_index.response.schema import RESPONSE_TYPE as LLAMA_INDEX_RESPONSE_TYPE
from dataclasses import dataclass


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


from typing import Union


def create_resource_summarizer(
    resource_location: Hashable,
    ingest: IngestionStrategy,
    partition: PartitionStrategy,
    summarize: SummarizationStrategy,
    create_index: IndexStrategy,
    n_layers: Union[int, None] = None,
) -> ResourceSummarizer:
    """Creates a resource summarizer."""

    docs = ingest(resource_location)
    layers = create_layers(docs, partition, summarize, create_index, n_layers)
    summarizer = ResourceSummarizer(layers)
    return summarizer

breakpoint()


from argparse import ArgumentParser, Namespace


def get_args() -> Namespace:
    """Get the command line arguments."""

    parser = ArgumentParser()
    parser.add_argument(
        "--config",
        dest="config_file",
        help="The location of the configuration file.",
        metavar="CONFIG_LOCATION",
    )
breakpoint()

from pathlib import Path

chunks = Path("data/paul_graham_essay.txt").read_text().split("\n\n")
chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
from llama_index import Document

documents = [Document(text=chunk) for chunk in chunks]

from llama_index import TreeIndex, DocumentSummaryIndex

# tree_index = TreeIndex.from_documents(documents)
# tree_index

summary_index = DocumentSummaryIndex.from_documents(documents[:10])
retriever = summary_index.as_retriever()

breakpoint()


@dataclass
class KnowledgeLayer:
    """A layer of knowledge."""

    chunks: Sequence[str]
    """Text chunks for the layer."""


layers: Sequence[KnowledgeLayer]


def extract_test_chunks() -> Sequence[str]:
    """Extracts chunks from test file."""


layers[0] = extract_test_chunks()
breakpoint()
layers[1] = abstract_layer(layers[0])


# take in list of chunks as input
# ....
# >
# set up layered indexing system
# readme: different spin on tree index

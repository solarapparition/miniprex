"""Create a resource summarizer for a text file."""

from argparse import ArgumentParser, Namespace

from resource_summarizer.summarizer import create_summarizer








from pathlib import Path
from llama_index import Document
from typing import Hashable, Sequence

def main() -> None:
    """Demos the creating of a resource summarizer for a text file."""

    resource_location = "data/paul_graham_essay.txt"

    def ingest(resource_location: str) -> Sequence[Document]:
        """Ingest a text file."""
        chunks = Path(resource_location).read_text(encoding="utf-8").split("\n\n")
        chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
        documents = [Document(text=chunk) for chunk in chunks]
        return documents


    from schema import Layer, Partition
    breakpoint()
    def partition(layer: Layer) -> Partition:
        breakpoint()

    summarizer = create_summarizer(resource_location, ingest, partition, None, None)
    breakpoint()

if __name__ == "__main__":
    main()
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

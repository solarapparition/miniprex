"""Create a resource summarizer for a text file."""

from more_itertools import batched
from pathlib import Path
from typing import Sequence

from llama_index import Document
from llama_index import VectorStoreIndex
from llama_index.schema import TextNode
from resource_summarizer.summarizer import create_summarizer
from resource_summarizer.schema import Layer, Partition


def main() -> None:
    """Demos the creating of a resource summarizer for a text file."""

    resource_location = "data/paul_graham_essay.txt"

    def ingest(resource_location: str) -> Sequence[Document]:
        """Ingest a text file."""
        chunks = Path(resource_location).read_text(encoding="utf-8").split("\n\n")
        chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
        documents = [Document(text=chunk) for chunk in chunks]
        return documents


    def demo_create_index(documents: Sequence[Document]) -> VectorStoreIndex:
        """Create basic vector index."""
        index = VectorStoreIndex.from_documents(documents)
        return index

    def demo_partition(layer: Layer) -> Partition:
        """Example partition that takes groups of 5 sequential documents (paragraphs in the demo) to create a block."""
        docs, _ = layer
        nodes = [TextNode(text=doc.text) for doc in docs]
        node_batches = [list(node_batch) for node_batch in batched(nodes, 5)]
        return node_batches

    from resource_summarizer.schema import Block
    def demo_summarize(block: Block) -> Document:
        """Example summarization via simple LLM prompting."""
        from langchain.schema import SystemMessage, HumanMessage, AIMessage
        from langchain.chat_models import ChatOpenAI

        system_message = SystemMessage(content=REWRITE_CONCISE)


    summarizer = create_summarizer(resource_location, ingest, partition, None, None)
    breakpoint()

if __name__ == "__main__":
    main()
breakpoint()


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
# > add retriever and chat engine to summarizer object
# set up layered indexing system
# readme: different spin on tree index

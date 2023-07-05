"""Convert an example webpage to Markdown format using the LangChain integration."""

from pathlib import Path
from langchain.document_loaders import ToMarkdownLoader

TOMARKDOWN_API_KEY = "YOUR-API-KEY"
OUTPUT_FILE = "output.md"
URL = "https://2markdown.com"


loader = ToMarkdownLoader(
    url=URL, api_key=TOMARKDOWN_API_KEY
)
docs = loader.load()

Path(OUTPUT_FILE).write_text(docs[0].page_content, encoding="utf-8")
print(f"Markdown data saved to {OUTPUT_FILE}")

"""Convert an example webpage to Markdown format using `requests`."""

from pathlib import Path
import requests

TOMARKDOWN_API_KEY = "YOUR-API-KEY"
OUTPUT_FILE = "output.md"
URL = "https://2markdown.com"

res = requests.post(
    "https://2markdown.com/api/2md",
    json={"url": URL},
    headers={"X-Api-Key": TOMARKDOWN_API_KEY},
    timeout=10,
)

Path(OUTPUT_FILE).write_text(res.json()["article"], encoding="utf-8")
print(f"Markdown data saved to {OUTPUT_FILE}")

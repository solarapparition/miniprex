#!/bin/sh

# Convert an example webpage to Markdown format using `curl`

TOMARKDOWN_API_KEY="YOUR-API-KEY"
OUTPUT_FILE="output.json"

# use curl to fetch data
DATA=$(curl --request POST \
  --url https://2markdown.com/api/2md \
  --header 'Content-Type: application/json' \
  --header "X-Api-Key: $TOMARKDOWN_API_KEY" \
  --data "{'url': $URL}")

# save data to the file
printf '%s' "$DATA" > "$OUTPUT_FILE"
echo "Markdown data saved to $OUTPUT_FILE"

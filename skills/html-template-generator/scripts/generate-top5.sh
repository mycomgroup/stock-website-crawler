#!/bin/bash

# Generate templates for top 5 URL patterns

TEMPLATES=(
  "analytics-chart-maker"
  "detail-sz"
  "detail-sh"
  "user-companies"
  "detail-nasdaq"
)

INPUT="../../stock-crawler/output/lixinger-crawler/url-patterns.json"
OUTPUT_DIR="../../stock-crawler/output/lixinger-crawler/templates"
PREVIEW_DIR="../../stock-crawler/output/lixinger-crawler/previews"

echo "🚀 Generating templates for top 5 URL patterns"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

for i in "${!TEMPLATES[@]}"; do
  template="${TEMPLATES[$i]}"
  num=$((i + 1))
  
  echo ""
  echo "[$num/5] Processing: $template"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  node scripts/generate-and-test.js "$template" \
    --input "$INPUT" \
    --output-dir "$OUTPUT_DIR" \
    --preview-dir "$PREVIEW_DIR"
  
  if [ $? -eq 0 ]; then
    echo "✅ Success: $template"
  else
    echo "❌ Failed: $template"
  fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Done! Check previews in: $PREVIEW_DIR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

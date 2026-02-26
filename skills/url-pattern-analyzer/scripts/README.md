# URL Pattern Analyzer Scripts

This directory contains command-line scripts for analyzing URL patterns from crawled data.

## Scripts

### analyze-url-patterns.js

Analyzes URL patterns from a `links.txt` file and generates pattern reports.

**Usage:**
```bash
node scripts/analyze-url-patterns.js [options]
```

**Options:**
- `--input, -i <path>` - Input links.txt file path (default: stock-crawler/output/lixinger-crawler/links.txt)
- `--output, -o <path>` - Output directory (default: stock-crawler/output/lixinger-crawler)
- `--min-group <number>` - Minimum group size (default: 5)
- `--samples <number>` - Number of sample URLs per pattern (default: 5)
- `--help, -h` - Show help information

**Examples:**
```bash
# Use default settings
node scripts/analyze-url-patterns.js

# Specify input and output
node scripts/analyze-url-patterns.js -i data/links.txt -o output

# Custom parameters
node scripts/analyze-url-patterns.js --min-group 10 --samples 3
```

**Output Files:**
- `url-patterns.json` - JSON format report with all URL patterns
- `url-patterns.md` - Markdown format report for human reading

**Features:**
- ✅ Command-line argument parsing
- ✅ Progress display with progress bars
- ✅ Error handling and validation
- ✅ Detailed statistics and summaries
- ✅ Configurable thresholds and parameters

## Workflow

1. **Read links.txt** - Parse JSON format URL records
2. **Extract URLs** - Filter valid URLs (fetched, no errors)
3. **Cluster URLs** - Group similar URLs by pattern
4. **Generate patterns** - Create regex patterns for each group
5. **Generate reports** - Output JSON and Markdown reports

## Requirements

- Node.js 12+
- Dependencies from parent skill (url-pattern-analyzer)

## Related

- See `../lib/` for the core analysis libraries
- See `../test/` for test scripts and examples

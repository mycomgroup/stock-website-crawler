#!/bin/bash

# Quick Start Script for HTML Template Generator
# 快速开始脚本 - 生成和测试模板

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
INPUT_FILE=""
OUTPUT_DIR=""
PREVIEW_DIR=""
CONFIG_FILE="config/quick-test.json"
TEMPLATE_NAME=""

# Function to print colored messages
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to show help
show_help() {
    cat << EOF
Quick Start Script for HTML Template Generator

Usage: ./quick-start.sh [options]

Options:
    -t, --template <name>     Template name (required)
    -i, --input <path>        Path to url-patterns.json (required)
    -o, --output <path>       Output directory for templates (required)
    -p, --preview <path>      Preview directory for markdown (required)
    -c, --config <path>       Config file (default: config/quick-test.json)
    -h, --help                Show this help message

Examples:
    # Test single template with quick-test config
    ./quick-start.sh \\
        -t api-doc \\
        -i ../../stock-crawler/output/lixinger-crawler/url-patterns.json \\
        -o ../../stock-crawler/output/lixinger-crawler/templates \\
        -p ../../stock-crawler/output/lixinger-crawler/previews

    # Use production config
    ./quick-start.sh \\
        -t api-doc \\
        -i url-patterns.json \\
        -o output/templates \\
        -p output/previews \\
        -c config/production.json

Available Configs:
    config/quick-test.json    - Fast testing (2 samples, visible browser)
    config/production.json    - Production quality (5 samples)
    config/detail-pages.json  - Optimized for detail pages
    config/list-pages.json    - Optimized for list pages
    config/table-pages.json   - Optimized for table pages

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--template)
            TEMPLATE_NAME="$2"
            shift 2
            ;;
        -i|--input)
            INPUT_FILE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -p|--preview)
            PREVIEW_DIR="$2"
            shift 2
            ;;
        -c|--config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Validate required arguments
if [ -z "$TEMPLATE_NAME" ] || [ -z "$INPUT_FILE" ] || [ -z "$OUTPUT_DIR" ] || [ -z "$PREVIEW_DIR" ]; then
    print_error "Missing required arguments"
    show_help
    exit 1
fi

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    print_error "Input file not found: $INPUT_FILE"
    exit 1
fi

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    print_error "Config file not found: $CONFIG_FILE"
    exit 1
fi

# Create output directories if they don't exist
mkdir -p "$OUTPUT_DIR"
mkdir -p "$PREVIEW_DIR"

# Print configuration
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
print_info "HTML Template Generator - Quick Start"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
print_info "Configuration:"
echo "  Template:    $TEMPLATE_NAME"
echo "  Input:       $INPUT_FILE"
echo "  Output:      $OUTPUT_DIR"
echo "  Preview:     $PREVIEW_DIR"
echo "  Config:      $CONFIG_FILE"
echo ""

# Run the generator
print_info "Step 1: Generating template..."
echo ""

if node scripts/generate-and-test.js "$TEMPLATE_NAME" \
    --input "$INPUT_FILE" \
    --output-dir "$OUTPUT_DIR" \
    --preview-dir "$PREVIEW_DIR" \
    --config "$CONFIG_FILE"; then
    
    echo ""
    print_success "Template generation completed!"
    echo ""
    
    # Show output files
    TEMPLATE_FILE="$OUTPUT_DIR/${TEMPLATE_NAME}.json"
    PREVIEW_FILE="$PREVIEW_DIR/${TEMPLATE_NAME}.md"
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_success "Output Files:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    if [ -f "$TEMPLATE_FILE" ]; then
        TEMPLATE_SIZE=$(wc -c < "$TEMPLATE_FILE")
        print_success "Template: $TEMPLATE_FILE ($TEMPLATE_SIZE bytes)"
    fi
    
    if [ -f "$PREVIEW_FILE" ]; then
        PREVIEW_SIZE=$(wc -c < "$PREVIEW_FILE")
        PREVIEW_LINES=$(wc -l < "$PREVIEW_FILE")
        print_success "Preview:  $PREVIEW_FILE ($PREVIEW_LINES lines, $PREVIEW_SIZE bytes)"
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_info "Next Steps:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "1. Review the preview file:"
    echo "   cat $PREVIEW_FILE"
    echo ""
    echo "2. Check if extraction is correct:"
    echo "   - Are titles extracted correctly?"
    echo "   - Are tables formatted properly?"
    echo "   - Is there any unwanted content (ads, navigation)?"
    echo ""
    echo "3. If good, proceed with batch generation:"
    echo "   node scripts/batch-generate-with-config.js \\"
    echo "     --input $INPUT_FILE \\"
    echo "     --output-dir $OUTPUT_DIR \\"
    echo "     --config $CONFIG_FILE"
    echo ""
    echo "4. If not good, adjust parameters:"
    echo "   - Lower frequency threshold: --frequency-threshold 0.6"
    echo "   - Increase samples: --max-samples 10"
    echo "   - Try different config: --config config/detail-pages.json"
    echo ""
    
else
    echo ""
    print_error "Template generation failed!"
    echo ""
    print_info "Troubleshooting:"
    echo "  - Check if the template name exists in url-patterns.json"
    echo "  - Verify Chrome/Chromium is installed"
    echo "  - Check network connectivity"
    echo "  - Try with visible browser: edit config file, set headless: false"
    echo ""
    exit 1
fi

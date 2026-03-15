# Stock Website Crawler

A flexible and powerful web crawler specifically designed for stock and financial websites, with advanced features for handling complex web content.

## 🌟 Features

### Core Capabilities
- **Multi-Parser Architecture**: Specialized parsers for different page types (API docs, generic pages)
- **Advanced Tab Extraction**: 3-layer detection strategy for standard and custom tab implementations
- **Pagination Support**: Automatic detection and navigation through paginated content
- **Infinite Scroll Handling**: Smart detection and loading of dynamically loaded content
- **Dropdown Content Extraction**: Automatic detection and extraction of dropdown menu content
- **Date Filter Processing**: Intelligent handling of date range filters

### Content Extraction
- **Rich Content Support**: Tables, images, charts (Canvas/SVG), code blocks, lists, videos, audio
- **Mixed Content Preservation**: Maintains original layout order of paragraphs, images, and other elements
- **Markdown Generation**: Clean, readable markdown output with proper formatting
- **Image & Chart Saving**: Automatic download and organization of images and charts

### Authentication & Session
- **Persistent Login**: Uses Chrome user data directory to maintain login sessions
- **Cookie Management**: Automatic cookie handling for authenticated sessions

### Link Management
- **Smart Link Discovery**: Automatic extraction of relevant links from pages
- **Priority System**: URL prioritization based on depth, structure, and content
- **Status Tracking**: Track link processing status (unfetched, fetched, failed)
- **Deduplication**: Automatic handling of duplicate URLs

### Quality & Reliability
- **Invalid URL Detection**: Multi-layer validation to prevent undefined/null parameters
- **Smart Filename Generation**: Readable, collision-resistant filenames
- **Comprehensive Logging**: Detailed logging with statistics tracking
- **Error Handling**: Robust error handling and recovery mechanisms

## 📁 Project Structure

```
stock-website-crawler/
├── stock-crawler/          # Main crawler implementation
│   ├── src/               # Source code
│   │   ├── parsers/       # Page parsers
│   │   ├── browser-manager.js
│   │   ├── crawler-main.js
│   │   ├── link-manager.js
│   │   └── ...
│   ├── config/            # Configuration files
│   ├── scripts/           # Utility scripts
│   ├── test/              # Test files
│   └── doc/               # Documentation
├── .kiro/                 # Kiro AI specs
└── README.md
```

## 🚀 Quick Start

See [stock-crawler/QUICK_START.md](stock-crawler/QUICK_START.md) for detailed setup instructions.

### Basic Usage

```bash
cd stock-crawler
npm install
npm start
```

## 📚 Documentation

- [Quick Start Guide](stock-crawler/QUICK_START.md)
- [Implementation Summary](stock-crawler/doc/IMPLEMENTATION_SUMMARY.md)
- [Parser Architecture](stock-crawler/doc/PARSER_ARCHITECTURE.md)
- [Tab & Dropdown Feature](stock-crawler/doc/TAB_DROPDOWN_FEATURE.md)
- [Tab Extraction Improvement](stock-crawler/doc/TAB_EXTRACTION_IMPROVEMENT.md)
- [Pagination Feature](stock-crawler/doc/PAGINATION_FEATURE.md)
- [Persistent Login](stock-crawler/doc/PERSISTENT_LOGIN.md)
- [URL Prioritization](stock-crawler/doc/URL_PRIORITIZATION.md)
- [Logging System](stock-crawler/doc/LOGGING.md)
- [API Doc Crawl Optimization Guide](stock-crawler/doc/API_DOC_CRAWL_OPTIMIZATION_GUIDE.md)

## 🔧 Recent Improvements

### Tab Extraction Enhancement
Implemented a 3-layer tab detection strategy to handle custom tab implementations:
1. **Standard Tab Selectors**: `[role="tab"]`, `.tab`, etc.
2. **Clickable Element Grouping**: Detects groups of clickable elements
3. **Keyword-Based Detection**: Finds tabs by company/organization names

This improvement enables extraction of content from pages like QFII (Qualified Foreign Institutional Investor) listings where tabs are implemented as custom clickable elements.

### Filename Strategy
- Reduced average filename length by 49%
- More readable and intuitive filenames
- Automatic collision handling with hash suffixes

### Invalid URL Cleanup
- Multi-layer URL validation
- Cleaned 230 invalid links with undefined/null parameters
- Enhanced link extraction with parameter validation

## 🧪 Testing

```bash
cd stock-crawler
npm test
```

Test specific features:
```bash
# Test tab extraction on QFII page
node scripts/test-qfii-tab-extraction.js

# Test filename generation
node scripts/test-filename-generation.js

# Test login functionality
node scripts/test-login.js
```

## 📊 Use Cases

This crawler is particularly well-suited for:
- Financial data aggregation
- Stock market research
- Company information collection
- Regulatory filing extraction
- Market analysis data gathering

## 🛠️ Technology Stack

- **Node.js**: Runtime environment
- **Playwright**: Browser automation
- **ES Modules**: Modern JavaScript module system
- **Jest**: Testing framework

## 📝 Configuration

Create a configuration file in `stock-crawler/config/`:

```json
{
  "name": "your-project",
  "baseUrl": "https://example.com",
  "loginUrl": "https://example.com/login",
  "credentials": {
    "username": "your-username",
    "password": "your-password"
  },
  "linkFinder": {
    "enabled": true,
    "patterns": ["api-key="]
  }
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📄 License

MIT

## 🙏 Acknowledgments

Built with assistance from Kiro AI for rapid development and iteration.

---

**Note**: This crawler is designed for legitimate data collection purposes. Please respect website terms of service and robots.txt files.

# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- **Timestamp Pages Directory**: Pages directory now includes a timestamp suffix (e.g., `pages-20260226-153523`) that matches the corresponding log file name. This makes it easy to correlate crawled pages with their execution logs for debugging and tracking purposes.
  - Format: `pages-YYYYMMDD-HHmmss/`
  - Timezone: Beijing Time (UTC+8)
  - See [TIMESTAMP_PAGES_FEATURE.md](doc/TIMESTAMP_PAGES_FEATURE.md) for details

### Changed
- Modified `Logger` class to expose timestamp via `getTimestamp()` method
- Modified `CrawlerMain` initialization to create timestamped pages directory

### Technical Details
- Each crawl execution now creates a unique pages directory with timestamp
- Log file: `logs/crawler-{timestamp}.log`
- Pages directory: `pages-{timestamp}/`
- Both use the same timestamp for easy correlation
- Old `pages/` directories (if exist) are not affected

## [1.0.0] - Previous Release

### Features
- Configurable web crawling for stock data websites
- Automatic login handling
- Link discovery and management
- Page parsing with table, code block, and tab extraction
- API data extraction from intercepted responses
- Pagination support
- Date filter handling
- Markdown output generation
- Error handling and retry logic
- Progress tracking and statistics
- Resumable crawling with links.txt

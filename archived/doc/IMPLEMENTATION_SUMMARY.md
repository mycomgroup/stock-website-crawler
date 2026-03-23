# Implementation Summary

This document describes the **current** implementation as it exists in the codebase (not a historical task checklist).

## Project Entry Points

- `src/index.js` - CLI entry point for crawling via config file.
- `src/template-pipeline-cli.js` - CLI for the template crawl pipeline.
- `src/crawler-main.js` - Main orchestration class used by the CLI.

## Core Modules (Top-Level `src/`)

- `src/config-manager.js` - Loads and validates crawl configuration.
- `src/link-manager.js` - Manages URL state and crawl progress.
- `src/browser-manager.js` - Playwright browser/session lifecycle.
- `src/login-handler.js` - Login page detection and session handling.
- `src/link-finder.js` - In-page link discovery and filtering.
- `src/page-parser.js` - Coordinates parser selection and extraction.
- `src/markdown-generator.js` - Markdown output assembly.
- `src/logger.js` - Logging and structured summaries.
- `src/stats-tracker.js` - Crawl statistics tracking.
- `src/url-utils.js` - URL normalization and utilities.
- `src/template-crawl-pipeline.js` - Template-driven crawling pipeline.

## Application Layer (`src/application/`)

- `crawler-bootstrap-service.js` - Bootstraps crawl runtime and dependencies.
- `crawl-job-service.js` - Runs crawl jobs and manages lifecycle.
- `url-processing-service.js` - URL processing workflow (fetch, parse, store).
- `browser-crawl-processor.js` - Browser-based crawl execution.
- `login-orchestration-service.js` - Orchestrates login flow when required.

## Domain Layer (`src/domain/`)

- `retry-policy.js` - Retry strategy and backoff behavior.
- `url-state-machine.js` - URL state transitions and status control.

## Storage Layer (`src/storage/`)

- `page-storage.js` + `index.js` - Storage interface and registry.
- `file-page-storage.js` - File-based page output.
- `sqlite-link-storage-json.js` / `sqlite-link-storage-row.js` - SQLite link storage.
- `lancedb-page-storage.js` - LanceDB page storage option.

## Parsers and Formatters

- `src/parsers/` - Parser implementations and routing via `parser-manager.js`.
  - Base + generic parsers (`base-parser.js`, `generic-parser.js`, `core-content-parser.js`).
  - Domain-specific parsers (e.g., `finnhub-api-parser.js`, `yfinance-api-parser.js`, etc.).
  - Support parsers such as `mintlify-parser.js`, `list-parser.js`, `directory-parser.js`.
- `src/formatters/` - Output formatters (e.g., `api-doc-formatter.js`).

## Configuration

- Configs live under `config/` (e.g., `example.json`, `lixinger.json`, and many site-specific configs).
- The crawler is configuration-driven; URLs, filters, parsers, and outputs are defined per config.

## Tests

- Jest configuration: `jest.config.js`.
- Unit and integration tests live under `test/` and cover core modules, parsers, and pipelines.

## Scripts and Utilities

- `scripts/` contains helper tasks for crawling/validation and site-specific runs.
- Root-level `.mjs` utilities are used for inspection, debugging, and regeneration.

## Notes

- This summary intentionally avoids hard-coded test counts or "all tests passing" claims; refer to `npm test` for current results.
- If new modules are added, update this summary to keep it aligned with code structure.

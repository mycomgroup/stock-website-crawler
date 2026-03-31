#!/usr/bin/env node

import fs from 'fs/promises';
import path from 'path';
import { TemplateExtractor } from '../lib/template-extractor.js';
import { TemplateRenderer } from '../lib/template-renderer.js';
import { BrowserManager } from '../lib/browser-manager.js';
import { HTMLFetcher } from '../lib/html-fetcher.js';

function parseArgs() {
  const args = process.argv.slice(2);
  const config = {
    template: null,
    urlsFile: null,
    output: null,
    markdownDir: null,
    headless: true,
    timeout: 30000,
    userDataDir: null,
    maxPages: null
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--template') config.template = args[++i];
    else if (arg === '--urls-file') config.urlsFile = args[++i];
    else if (arg === '--output') config.output = args[++i];
    else if (arg === '--markdown-dir') config.markdownDir = args[++i];
    else if (arg === '--headless') config.headless = args[++i] !== 'false';
    else if (arg === '--timeout') config.timeout = parseInt(args[++i], 10);
    else if (arg === '--user-data-dir') config.userDataDir = args[++i];
    else if (arg === '--max-pages') config.maxPages = parseInt(args[++i], 10);
  }

  if (!config.template || !config.urlsFile || !config.output) {
    console.error('Usage: node scripts/extract-useful-content.js --template <template.json> --urls-file <urls.txt|json> --output <result.jsonl> [--markdown-dir <dir>] [--headless false] [--timeout 30000] [--user-data-dir <dir>] [--max-pages 20]');
    process.exit(1);
  }

  return config;
}

async function loadUrls(urlsFile) {
  const content = await fs.readFile(urlsFile, 'utf-8');
  const trimmed = content.trim();
  if (trimmed.startsWith('[')) {
    return JSON.parse(trimmed).filter(Boolean);
  }

  return trimmed.split(/\r?\n/).map(line => line.trim()).filter(Boolean);
}

async function main() {
  const args = parseArgs();

  const templatePath = path.resolve(args.template);
  const urlsPath = path.resolve(args.urlsFile);
  const outputPath = path.resolve(args.output);
  const markdownDir = args.markdownDir ? path.resolve(args.markdownDir) : null;

  const template = JSON.parse(await fs.readFile(templatePath, 'utf-8'));
  let urls = await loadUrls(urlsPath);
  if (args.maxPages && urls.length > args.maxPages) {
    urls = urls.slice(0, args.maxPages);
  }

  const browserManager = new BrowserManager({
    headless: args.headless,
    timeout: args.timeout,
    ...(args.userDataDir ? { userDataDir: path.resolve(args.userDataDir) } : {})
  });
  const fetcher = new HTMLFetcher(browserManager, args.timeout);
  const extractor = new TemplateExtractor();
  const renderer = new TemplateRenderer();

  const reviewItems = [];
  const results = [];
  const failedUrls = [];

  await browserManager.launch();
  try {
    for (const url of urls) {
      try {
        const { html } = await fetcher.fetchOne(url);
        const record = extractor.extract(html, template, { url });
        results.push(record);

        if (markdownDir) {
          const markdown = renderer.render(html, template);
          const safeName = encodeURIComponent(url).replace(/%/g, '_');
          await fs.mkdir(markdownDir, { recursive: true });
          await fs.writeFile(path.join(markdownDir, `${safeName}.md`), markdown, 'utf-8');
        }

        if (record.needsHumanReview) {
          reviewItems.push({
            url,
            score: record.confidence.score,
            missing: record.confidence.missingCritical
          });
        }
      } catch (error) {
        console.error(`Failed to fetch ${url}: ${error.message}`);
        failedUrls.push({ url, error: error.message });
      }
    }
  } finally {
    await browserManager.close();
  }

  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.writeFile(outputPath, results.map(item => JSON.stringify(item)).join('\n') + '\n', 'utf-8');

  const reportPath = outputPath.replace(/\.jsonl?$/, '.review.json');
  await fs.writeFile(reportPath, JSON.stringify({ total: results.length, needReview: reviewItems.length, items: reviewItems }, null, 2));

  console.log(`✅ Extracted ${results.length} pages`);
  console.log(`📄 JSONL: ${outputPath}`);
  console.log(`🧑‍💻 Review report: ${reportPath}`);
  if (markdownDir) {
    console.log(`📝 Markdown previews: ${markdownDir}`);
  }
  if (failedUrls.length > 0) {
    console.log(`\n❌ Failed URLs (${failedUrls.length}):`);
    failedUrls.forEach(({ url, error }) => {
      console.log(`  - ${url}: ${error}`);
    });
  }
}

main().catch((err) => {
  console.error(`❌ ${err.message}`);
  process.exit(1);
});

#!/usr/bin/env node

/**
 * Run review workflow in one command.
 *
 * Job file example:
 * [
 *   {
 *     "template": "./templates/api-doc.json",
 *     "urlsFile": "./input/api-doc-urls.txt",
 *     "name": "api-doc"
 *   }
 * ]
 */

import fs from 'fs/promises';
import path from 'path';
import { TemplateExtractor } from '../lib/template-extractor.js';
import { TemplateRenderer } from '../lib/template-renderer.js';
import { BrowserManager } from '../lib/browser-manager.js';
import { HTMLFetcher } from '../lib/html-fetcher.js';
import { StructureComparator } from '../lib/structure-comparator.js';

function parseArgs() {
  const args = process.argv.slice(2);
  const config = {
    jobs: null,
    workspaceDir: null,
    headless: true,
    timeout: 30000,
    userDataDir: null,
    maxPagesPerJob: null,
    withMarkdown: true
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--jobs') config.jobs = args[++i];
    else if (arg === '--workspace-dir') config.workspaceDir = args[++i];
    else if (arg === '--headless') config.headless = args[++i] !== 'false';
    else if (arg === '--timeout') config.timeout = parseInt(args[++i], 10);
    else if (arg === '--user-data-dir') config.userDataDir = args[++i];
    else if (arg === '--max-pages-per-job') config.maxPagesPerJob = parseInt(args[++i], 10);
    else if (arg === '--with-markdown') config.withMarkdown = args[++i] !== 'false';
  }

  if (!config.jobs || !config.workspaceDir) {
    console.error('Usage: node scripts/run-review-workflow.js --jobs <jobs.json> --workspace-dir <dir> [--headless false] [--timeout 30000] [--user-data-dir <dir>] [--max-pages-per-job 20] [--with-markdown true]');
    process.exit(1);
  }

  return config;
}

async function loadUrls(urlsFile) {
  const content = await fs.readFile(urlsFile, 'utf-8');
  const trimmed = content.trim();
  if (trimmed.startsWith('[')) return JSON.parse(trimmed).filter(Boolean);
  return trimmed.split(/\r?\n/).map(s => s.trim()).filter(Boolean);
}

async function writeJson(filePath, data) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, JSON.stringify(data, null, 2));
}

function buildFeedbackTemplate(records, reviewItems) {
  return {
    instructions: [
      '请补充 wrongXpaths: 哪个字段抽错了',
      '请补充 suggestedXPath: 你建议的 XPath',
      '可选：note 填写页面差异说明'
    ],
    items: reviewItems.map(item => ({
      url: item.url,
      score: item.score,
      missing: item.missing,
      wrongXpaths: [],
      suggestedXPath: {},
      note: ''
    })),
    examples: records.slice(0, 3).map(r => ({
      url: r.url,
      title: r.title,
      sectionCount: r.stats?.sectionCount,
      tableCount: r.stats?.tableCount
    }))
  };
}

async function main() {
  const args = parseArgs();
  const jobs = JSON.parse(await fs.readFile(path.resolve(args.jobs), 'utf-8'));

  const browserManager = new BrowserManager({
    headless: args.headless,
    timeout: args.timeout,
    ...(args.userDataDir ? { userDataDir: path.resolve(args.userDataDir) } : {})
  });

  const fetcher = new HTMLFetcher(browserManager, args.timeout);
  const extractor = new TemplateExtractor();
  const renderer = new TemplateRenderer();
  const comparator = new StructureComparator();

  const workflowSummary = [];

  await browserManager.launch();
  try {
    for (const job of jobs) {
      const name = job.name || path.basename(job.template, '.json');
      const template = JSON.parse(await fs.readFile(path.resolve(job.template), 'utf-8'));
      let urls = await loadUrls(path.resolve(job.urlsFile));
      if (args.maxPagesPerJob && urls.length > args.maxPagesPerJob) {
        urls = urls.slice(0, args.maxPagesPerJob);
      }

      const outDir = path.resolve(args.workspaceDir, name);
      await fs.mkdir(outDir, { recursive: true });

      const records = [];
      const reviewItems = [];

      for (const url of urls) {
        const { html } = await fetcher.fetchOne(url);
        const record = extractor.extract(html, template, { url });
        records.push(record);

        if (args.withMarkdown) {
          const markdown = renderer.render(html, template);
          const safeName = encodeURIComponent(url).replace(/%/g, '_');
          await fs.writeFile(path.join(outDir, `${safeName}.md`), markdown, 'utf-8');
        }

        if (record.needsHumanReview) {
          reviewItems.push({
            url,
            score: record.confidence.score,
            missing: record.confidence.missingCritical
          });
        }
      }

      await fs.writeFile(path.join(outDir, 'extracted.jsonl'), records.map(r => JSON.stringify(r)).join('\n') + '\n');
      await writeJson(path.join(outDir, 'review.json'), {
        total: records.length,
        needReview: reviewItems.length,
        items: reviewItems
      });

      const comparison = comparator.compare(records);
      await writeJson(path.join(outDir, 'structure-comparison.json'), comparison);

      const feedbackTemplate = buildFeedbackTemplate(records, reviewItems);
      await writeJson(path.join(outDir, 'feedback.template.json'), feedbackTemplate);

      workflowSummary.push({
        name,
        total: records.length,
        needReview: reviewItems.length,
        commonSectionHeadings: comparison.commonSectionHeadings,
        commonTableHeaders: comparison.commonTableHeaders
      });
    }
  } finally {
    await browserManager.close();
  }

  await writeJson(path.resolve(args.workspaceDir, 'summary.json'), workflowSummary);

  console.log(`✅ Review workflow finished: ${args.workspaceDir}`);
  console.log('输出内容: extracted.jsonl / review.json / structure-comparison.json / feedback.template.json / summary.json');
}

main().catch((err) => {
  console.error(`❌ ${err.message}`);
  process.exit(1);
});

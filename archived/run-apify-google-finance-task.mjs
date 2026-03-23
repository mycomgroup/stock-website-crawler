#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { spawnSync } from 'child_process';

const projectRoot = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const configRelPath = 'config/apify-google-finance-scraper.json';
const configPath = path.join(projectRoot, configRelPath);

const requiredDocs = [
  'Google_Finance_Scraper.md',
  'ScrapAPI.md',
  'Apify_API.md'
];

const maxRuns = Number(process.env.APIFY_TASK_MAX_RUNS || 3);

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function getLatestPagesDir(outputProjectDir) {
  if (!fs.existsSync(outputProjectDir)) return null;

  const dirs = fs.readdirSync(outputProjectDir, { withFileTypes: true })
    .filter((d) => d.isDirectory() && d.name.startsWith('pages-'))
    .map((d) => d.name)
    .sort();

  if (dirs.length === 0) return null;
  return path.join(outputProjectDir, dirs[dirs.length - 1]);
}

function getMissingDocs(pagesDir) {
  if (!pagesDir || !fs.existsSync(pagesDir)) return [...requiredDocs];
  return requiredDocs.filter((name) => !fs.existsSync(path.join(pagesDir, name)));
}

function runCrawl() {
  const result = spawnSync('npm', ['run', 'crawl', configRelPath], {
    cwd: projectRoot,
    stdio: 'inherit',
    env: process.env
  });
  return result.status === 0;
}

function readUnfetchedCount(outputProjectDir) {
  const linksPath = path.join(outputProjectDir, 'links.txt');
  if (!fs.existsSync(linksPath)) return 0;

  let count = 0;
  const lines = fs.readFileSync(linksPath, 'utf8').split(/\r?\n/).filter(Boolean);
  for (const line of lines) {
    try {
      const item = JSON.parse(line);
      if (item?.status === 'unfetched') count += 1;
    } catch {
      // ignore non-JSON lines
    }
  }
  return count;
}

function main() {
  const config = readJson(configPath);
  const outputDir = config.output?.directory || './output';
  const outputProjectDir = path.resolve(projectRoot, outputDir, config.name);

  let latestPagesDir = getLatestPagesDir(outputProjectDir);
  let missing = getMissingDocs(latestPagesDir);

  for (let i = 1; i <= maxRuns && missing.length > 0; i += 1) {
    console.log(`\n[run-apify-google-finance-task] Run ${i}/${maxRuns}: missing docs -> ${missing.join(', ')}`);
    const ok = runCrawl();
    if (!ok) {
      console.error('[run-apify-google-finance-task] crawl command failed.');
      process.exit(1);
    }

    latestPagesDir = getLatestPagesDir(outputProjectDir);
    missing = getMissingDocs(latestPagesDir);
  }

  const unfetchedCount = readUnfetchedCount(outputProjectDir);
  const latestDirDisplay = latestPagesDir ? path.relative(projectRoot, latestPagesDir) : '(none)';

  if (missing.length > 0) {
    console.error(`\n[run-apify-google-finance-task] required docs still missing: ${missing.join(', ')}`);
    console.error(`[run-apify-google-finance-task] latest pages dir: ${latestDirDisplay}`);
    process.exit(2);
  }

  console.log('\n[run-apify-google-finance-task] success: required docs are available.');
  console.log(`[run-apify-google-finance-task] latest pages dir: ${latestDirDisplay}`);
  console.log(`[run-apify-google-finance-task] unfetched urls remaining in links.txt: ${unfetchedCount}`);
}

main();

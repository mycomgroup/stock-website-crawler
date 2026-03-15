#!/usr/bin/env node
/**
 * Regenerate all markdown files for Tushare Pro documentation
 * This script re-parses all fetched URLs and regenerates the markdown files
 */

import { chromium } from 'playwright';
import TushareProApiParser from './src/parsers/tushare-pro-api-parser.js';
import MarkdownGenerator from './src/markdown-generator.js';
import fs from 'fs';
import path from 'path';

const LINKS_FILE = './output/tushare-pro/tushare-pro-crawler/links.txt';
const OUTPUT_DIR = './output/tushare-pro/tushare-pro-crawler/pages-regenerated';

async function main() {
  // Create output directory
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  // Read all links
  const linksContent = fs.readFileSync(LINKS_FILE, 'utf-8');
  const links = linksContent.trim().split('\n').map(line => {
    try {
      return JSON.parse(line);
    } catch {
      return null;
    }
  }).filter(link => link && link.status === 'fetched');

  console.log(`Found ${links.length} fetched URLs to process`);

  const browser = await chromium.launch({ headless: true });
  const parser = new TushareProApiParser();
  const mdGen = new MarkdownGenerator();

  let processed = 0;
  let errors = 0;

  for (const link of links) {
    try {
      process.stdout.write(`\rProcessing ${processed + 1}/${links.length}: ${link.url.substring(0, 50)}...`);

      const page = await browser.newPage();
      await page.goto(link.url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForSelector('.content h2', { timeout: 15000 });
      await page.waitForTimeout(500);

      const result = await parser.parse(page, link.url);
      const markdown = mdGen.generate(result);

      // Generate filename
      const filename = result.suggestedFilename || mdGen.safeFilename(result.title || 'untitled', link.url);
      const filepath = path.join(OUTPUT_DIR, `${filename}.md`);

      // Handle duplicate filenames
      let finalPath = filepath;
      let counter = 1;
      while (fs.existsSync(finalPath) && finalPath === filepath) {
        finalPath = path.join(OUTPUT_DIR, `${filename}_${counter}.md`);
        counter++;
      }

      fs.writeFileSync(finalPath, markdown, 'utf-8');
      processed++;

      await page.close();

      // Small delay to avoid overwhelming the server
      await new Promise(resolve => setTimeout(resolve, 200));
    } catch (error) {
      console.error(`\nError processing ${link.url}: ${error.message}`);
      errors++;
    }
  }

  await browser.close();

  console.log(`\n\n=== Summary ===`);
  console.log(`Processed: ${processed}`);
  console.log(`Errors: ${errors}`);
  console.log(`Output directory: ${OUTPUT_DIR}`);
}

main().catch(console.error);
import { chromium } from 'playwright';
import MassiveApiParser from './src/parsers/massive-api-parser.js';
import MarkdownGenerator from './src/markdown-generator.js';
import fs from 'fs';
import path from 'path';

const linksFile = './output/massive-api-docs/links.txt';
const outputDir = './output/massive-api-docs/pages-regenerated';

async function regenerateAll() {
  console.log('Loading links...');
  const links = fs.readFileSync(linksFile, 'utf-8')
    .split('\n')
    .filter(line => line.trim())
    .map(line => JSON.parse(line))
    .filter(link => link.status === 'fetched');

  console.log(`Found ${links.length} fetched URLs`);

  // 创建输出目录
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const browser = await chromium.launch({ headless: true });
  const parser = new MassiveApiParser();
  const mdGenerator = new MarkdownGenerator();

  let processed = 0;
  let errors = 0;

  for (const link of links) {
    processed++;
    const url = link.url;

    if (processed % 50 === 0) {
      console.log(`Progress: ${processed}/${links.length} (${((processed/links.length)*100).toFixed(1)}%)`);
    }

    const page = await browser.newPage();
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await parser.waitForContent(page);

      const data = await parser.parse(page, url);
      const md = mdGenerator.generateMassiveApi(data);

      const filename = parser.generateFilename(url) + '.md';
      const outputPath = path.join(outputDir, filename);
      fs.writeFileSync(outputPath, md);

    } catch (e) {
      errors++;
      if (errors <= 10) {
        console.error(`Error processing ${url}: ${e.message}`);
      }
    }
    await page.close();
  }

  await browser.close();
  console.log(`\nCompleted! Processed: ${processed}, Errors: ${errors}`);
}

regenerateAll();
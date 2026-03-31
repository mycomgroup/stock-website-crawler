#!/usr/bin/env node

/**
 * Render All Templates to Markdown Previews
 */

import { TemplateRenderer } from '../lib/template-renderer.js';
import { HTMLFetcher } from '../lib/html-fetcher.js';
import { BrowserManager } from '../lib/browser-manager.js';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function main() {
  const templatesDir = process.argv[2] || '../../stock-crawler/output/lixinger-crawler/templates';
  const previewsDir = process.argv[3] || '../../stock-crawler/output/lixinger-crawler/previews';
  
  console.log('🎨 Rendering Templates to Markdown');
  console.log('━'.repeat(60));
  console.log(`📁 Templates: ${templatesDir}`);
  console.log(`📁 Previews: ${previewsDir}`);
  console.log('━'.repeat(60));
  
  // Create previews directory
  await fs.mkdir(path.resolve(previewsDir), { recursive: true });
  
  // Get all template files
  const templateFiles = (await fs.readdir(path.resolve(templatesDir)))
    .filter(f => f.endsWith('.json'));
  
  console.log(`\n📝 Found ${templateFiles.length} templates\n`);
  
  // Setup browser
  const userDataDir = path.resolve(__dirname, '../../../stock-crawler/chrome_user_data');
  const browserManager = new BrowserManager({
    userDataDir,
    headless: true,
    channel: 'chrome',
    timeout: 30000
  });
  
  await browserManager.launch();
  const fetcher = new HTMLFetcher(browserManager);
  const renderer = new TemplateRenderer();
  
  // Process each template
  for (const templateFile of templateFiles) {
    const templatePath = path.resolve(templatesDir, templateFile);
    const previewPath = path.resolve(previewsDir, templateFile.replace('.json', '.md'));
    
    console.log(`\n[${templateFiles.indexOf(templateFile) + 1}/${templateFiles.length}] ${templateFile}`);
    
    try {
      // Load template
      const template = JSON.parse(await fs.readFile(templatePath, 'utf-8'));
      console.log(`  Template: ${template.templateName}`);
      console.log(`  Samples: ${template.samples.length}`);
      
      // Fetch first sample URL
      if (!template.samples || template.samples.length === 0) {
        console.log(`  ⚠ No sample URLs found, skipping`);
        continue;
      }
      const url = template.samples[0];
      console.log(`  Fetching: ${url}`);
      const result = await fetcher.fetchOne(url);
      
      // Render to markdown
      const markdown = renderer.render(result.html, template);
      console.log(`  Rendered: ${markdown.length} characters`);
      
      // Save preview
      await fs.writeFile(previewPath, markdown, 'utf-8');
      console.log(`  ✅ Saved: ${previewPath}`);
      
    } catch (error) {
      console.error(`  ❌ Error: ${error.message}`);
    }
  }
  
  await browserManager.close();
  
  console.log('\n' + '━'.repeat(60));
  console.log('✨ Done!');
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});

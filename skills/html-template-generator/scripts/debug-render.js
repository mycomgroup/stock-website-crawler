#!/usr/bin/env node

/**
 * Debug Template Rendering
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
  const templatePath = process.argv[2] || '../../stock-crawler/output/lixinger-crawler/templates/detail-sz.json';
  
  console.log('🔍 Debug Template Rendering');
  console.log('━'.repeat(60));
  
  try {
    // Load template
    console.log('\n1. Loading template...');
    const template = JSON.parse(await fs.readFile(path.resolve(templatePath), 'utf-8'));
    console.log('✓ Template loaded:', template.templateName);
    console.log('  Samples:', template.samples.length);
    console.log('  XPaths:', JSON.stringify(template.xpaths, null, 2));
    
    // Fetch HTML
    console.log('\n2. Fetching HTML...');
    const url = template.samples[0];
    console.log('  URL:', url);
    
    const userDataDir = path.resolve(__dirname, '../../../stock-crawler/chrome_user_data');
    const browserManager = new BrowserManager({
      userDataDir,
      headless: true,
      channel: 'chrome',
      timeout: 30000
    });
    
    await browserManager.launch();
    const fetcher = new HTMLFetcher(browserManager);
    const result = await fetcher.fetchOne(url);
    await browserManager.close();
    
    console.log('✓ HTML fetched:', result.html.length, 'bytes');
    
    // Save HTML for inspection
    const htmlPath = '/tmp/debug-page.html';
    await fs.writeFile(htmlPath, result.html, 'utf-8');
    console.log('  Saved to:', htmlPath);
    
    // Try rendering
    console.log('\n3. Rendering to Markdown...');
    const renderer = new TemplateRenderer();
    const markdown = renderer.render(result.html, template);
    
    console.log('✓ Markdown generated:', markdown.length, 'characters');
    console.log('\n━'.repeat(60));
    console.log('Rendered Markdown:');
    console.log('━'.repeat(60));
    console.log(markdown);
    console.log('━'.repeat(60));
    
    // Test XPath directly
    console.log('\n4. Testing XPath directly...');
    const xpath = (await import('xpath')).default;
    
    const dom = new JSDOM(result.html);
    const doc = dom.window.document;
    
    // Test sections xpath
    if (template.xpaths.sections?.xpath) {
      console.log('\n  Testing sections xpath:', template.xpaths.sections.xpath);
      const sections = xpath.select(template.xpaths.sections.xpath, doc);
      console.log('  Found sections:', sections.length);
      
      if (sections.length > 0) {
        console.log('  First section HTML (first 200 chars):');
        console.log('  ', sections[0].outerHTML?.substring(0, 200) || sections[0].textContent?.substring(0, 200));
      }
    }
    
    // Test title xpath
    if (template.xpaths.title) {
      console.log('\n  Testing title xpath:', template.xpaths.title);
      const title = xpath.select(template.xpaths.title, doc);
      console.log('  Found title:', title);
    }
    
  } catch (error) {
    console.error('\n❌ Error:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

main();

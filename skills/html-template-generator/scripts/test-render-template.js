#!/usr/bin/env node

/**
 * Test Template Renderer
 * 
 * Test rendering a template by fetching a sample URL and generating Markdown
 */

import { TemplateRenderer } from '../lib/template-renderer.js';
import { HTMLFetcher } from '../lib/html-fetcher.js';
import { BrowserManager } from '../lib/browser-manager.js';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Parse command-line arguments
 */
function parseArgs() {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log(`
Usage: node test-render-template.js <template-file> <url> [output-file]

Arguments:
  template-file  Path to template JSON file
  url           URL to fetch and render
  output-file   Optional output Markdown file (default: stdout)

Example:
  node test-render-template.js \\
    ../../stock-crawler/output/lixinger-crawler/templates/api-doc.json \\
    https://www.lixinger.com/open/api/doc \\
    ./output/api-doc-sample.md
    `);
    process.exit(1);
  }
  
  return {
    templateFile: args[0],
    url: args[1],
    outputFile: args[2] || null
  };
}

/**
 * Main function
 */
async function main() {
  const config = parseArgs();
  
  console.log('🎨 Template Renderer Test');
  console.log('━'.repeat(60));
  console.log(`📄 Template: ${config.templateFile}`);
  console.log(`🔗 URL: ${config.url}`);
  if (config.outputFile) {
    console.log(`💾 Output: ${config.outputFile}`);
  }
  console.log('━'.repeat(60));
  
  try {
    // Load template
    console.log('\n📖 Loading template...');
    const renderer = new TemplateRenderer();
    const template = await renderer.loadTemplate(path.resolve(config.templateFile));
    console.log(`✓ Template loaded: ${template.templateName}`);
    
    // Launch browser and fetch HTML
    console.log('\n🌐 Fetching HTML...');
    const userDataDir = path.resolve(__dirname, '../../../stock-crawler/chrome_user_data');
    const browserManager = new BrowserManager({
      userDataDir,
      headless: true,
      channel: 'chrome',
      timeout: 30000
    });
    
    await browserManager.launch();
    const fetcher = new HTMLFetcher(browserManager);
    const result = await fetcher.fetchOne(config.url);
    await browserManager.close();
    console.log(`✓ Fetched ${result.html.length} bytes`);
    const html = result.html;
    
    // Render to Markdown
    console.log('\n✍️  Rendering to Markdown...');
    const markdown = renderer.render(html, template);
    console.log(`✓ Generated ${markdown.length} characters`);
    
    // Output
    if (config.outputFile) {
      const outputPath = path.resolve(config.outputFile);
      await fs.mkdir(path.dirname(outputPath), { recursive: true });
      await fs.writeFile(outputPath, markdown, 'utf-8');
      console.log(`\n✅ Saved to: ${outputPath}`);
    } else {
      console.log('\n' + '━'.repeat(60));
      console.log('📝 Rendered Markdown:');
      console.log('━'.repeat(60));
      console.log(markdown);
    }
    
    console.log('\n✨ Done!');
    
  } catch (error) {
    console.error('\n❌ Error:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

main();

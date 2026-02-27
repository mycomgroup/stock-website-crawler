#!/usr/bin/env node

/**
 * Generate Template and Test Rendering
 * 
 * Generate a template and immediately test it by rendering a sample page
 */

import { TemplateGenerator } from '../main.js';
import { TemplateRenderer } from '../lib/template-renderer.js';
import { HTMLFetcher } from '../lib/html-fetcher.js';
import { BrowserManager } from '../lib/browser-manager.js';
import { ConfigLoader } from '../lib/config-loader.js';
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
  
  if (args.length < 1 || args.includes('--help') || args.includes('-h')) {
    showHelp();
    process.exit(args.includes('--help') || args.includes('-h') ? 0 : 1);
  }
  
  const config = {
    templateName: args[0],
    input: null,
    outputDir: null,
    previewDir: null,
    configFile: null,
    cliArgs: {}
  };
  
  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--input' && i + 1 < args.length) {
      config.input = args[++i];
    } else if (arg === '--output-dir' && i + 1 < args.length) {
      config.outputDir = args[++i];
    } else if (arg === '--preview-dir' && i + 1 < args.length) {
      config.previewDir = args[++i];
    } else if (arg === '--config' && i + 1 < args.length) {
      config.configFile = args[++i];
    } else if (arg === '--headless' && i + 1 < args.length) {
      config.cliArgs.headless = args[++i] !== 'false';
    } else if (arg === '--timeout' && i + 1 < args.length) {
      config.cliArgs.timeout = parseInt(args[++i], 10);
    } else if (arg === '--max-samples' && i + 1 < args.length) {
      config.cliArgs.maxSamples = parseInt(args[++i], 10);
    } else if (arg === '--frequency-threshold' && i + 1 < args.length) {
      config.cliArgs.frequencyThreshold = parseFloat(args[++i]);
    } else if (arg === '--wait-time' && i + 1 < args.length) {
      config.cliArgs.waitTime = parseInt(args[++i], 10);
    }
  }
  
  if (!config.input || !config.outputDir || !config.previewDir) {
    console.error('Error: --input, --output-dir, and --preview-dir are required');
    process.exit(1);
  }
  
  return config;
}

/**
 * Show help information
 */
function showHelp() {
  console.log(`
Usage: node generate-and-test.js <template-name> [options]

Arguments:
  template-name         Name of template from url-patterns.json

Required Options:
  --input <path>        Path to url-patterns.json
  --output-dir <path>   Directory for template JSON files
  --preview-dir <path>  Directory for preview Markdown files

Optional:
  --config <path>       Path to config file (default: config/default.json)
  --headless <bool>     Run browser in headless mode (default: true)
  --timeout <ms>        Page load timeout in milliseconds
  --max-samples <n>     Maximum number of sample pages to fetch
  --frequency-threshold <n>  Element frequency threshold (0-1)
  --wait-time <ms>      Wait time after page load

Examples:
  # Basic usage
  node generate-and-test.js api-doc \\
    --input url-patterns.json \\
    --output-dir output/templates \\
    --preview-dir output/previews

  # With custom config
  node generate-and-test.js api-doc \\
    --input url-patterns.json \\
    --output-dir output/templates \\
    --preview-dir output/previews \\
    --config config/quick-test.json

  # Override specific parameters
  node generate-and-test.js api-doc \\
    --input url-patterns.json \\
    --output-dir output/templates \\
    --preview-dir output/previews \\
    --config config/detail-pages.json \\
    --max-samples 3 \\
    --frequency-threshold 0.6
  `);
}

/**
 * Main function
 */
async function main() {
  const config = parseArgs();
  
  console.log('🚀 Generate Template and Test Rendering');
  console.log('━'.repeat(60));
  console.log(`📝 Template: ${config.templateName}`);
  console.log(`📁 Output: ${config.outputDir}`);
  console.log(`👁️  Preview: ${config.previewDir}`);
  if (config.configFile) {
    console.log(`⚙️  Config: ${config.configFile}`);
  }
  console.log('━'.repeat(60));
  
  // Load configuration
  const configLoader = new ConfigLoader();
  const fullConfig = await configLoader.load(config.configFile, config.cliArgs);
  configLoader.validate(fullConfig);
  
  console.log('\n⚙️  Configuration:');
  console.log(`   Frequency threshold: ${fullConfig.analysis.frequencyThreshold}`);
  console.log(`   Max samples: ${fullConfig.fetching.maxSamples}`);
  console.log(`   Headless: ${fullConfig.browser.headless}`);
  console.log(`   Detect page type: ${fullConfig.analysis.detectPageType}`);
  
  const userDataDir = path.resolve(__dirname, fullConfig.browser.userDataDir);
  const inputPath = path.resolve(config.input);
  const outputDir = path.resolve(config.outputDir);
  const previewDir = path.resolve(config.previewDir);
  const templatePath = path.join(outputDir, `${config.templateName}.json`);
  const previewPath = path.join(previewDir, `${config.templateName}.md`);
  
  try {
    // Step 1: Generate template
    console.log('\n📊 Step 1: Generating template...');
    const generator = new TemplateGenerator({
      browser: fullConfig.browser,
      fetching: fullConfig.fetching,
      analysis: fullConfig.analysis,
      xpath: fullConfig.xpath,
      filters: fullConfig.filters
    });
    
    await generator.generate(config.templateName, inputPath, templatePath);
    console.log(`✓ Template saved: ${templatePath}`);
    
    // Step 2: Load template and get first sample URL
    console.log('\n📖 Step 2: Loading template...');
    const templateContent = await fs.readFile(templatePath, 'utf-8');
    const template = JSON.parse(templateContent);
    const sampleUrl = template.samples?.[0];
    
    if (!sampleUrl) {
      throw new Error('No sample URL found in template');
    }
    console.log(`✓ Sample URL: ${sampleUrl}`);
    
    // Step 3: Fetch HTML
    console.log('\n🌐 Step 3: Fetching HTML...');
    const browserManager = new BrowserManager(fullConfig.browser);
    
    await browserManager.launch();
    const fetcher = new HTMLFetcher(browserManager);
    const result = await fetcher.fetchOne(sampleUrl);
    await browserManager.close();
    console.log(`✓ Fetched ${result.html.length} bytes`);
    const html = result.html;
    
    // Step 4: Render to Markdown
    console.log('\n✍️  Step 4: Rendering to Markdown...');
    const renderer = new TemplateRenderer();
    const markdown = renderer.render(html, template);
    console.log(`✓ Generated ${markdown.length} characters`);
    
    // Step 5: Save preview
    console.log('\n💾 Step 5: Saving preview...');
    await fs.mkdir(previewDir, { recursive: true });
    await fs.writeFile(previewPath, markdown, 'utf-8');
    console.log(`✓ Preview saved: ${previewPath}`);
    
    // Summary
    console.log('\n' + '━'.repeat(60));
    console.log('✅ Success!');
    console.log('━'.repeat(60));
    console.log(`📄 Template: ${templatePath}`);
    console.log(`👁️  Preview: ${previewPath}`);
    console.log('\n💡 Next steps:');
    console.log('   1. Review the preview Markdown file');
    console.log('   2. Check if the extraction is correct');
    console.log('   3. If good, proceed with batch generation');
    console.log('━'.repeat(60));
    
  } catch (error) {
    console.error('\n❌ Error:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

main();

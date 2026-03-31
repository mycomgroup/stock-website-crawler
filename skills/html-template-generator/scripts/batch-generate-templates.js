#!/usr/bin/env node

/**
 * Batch Template Generator
 * 
 * Generate templates for all patterns in url-patterns.json
 */

import { TemplateGenerator } from '../main.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Parse command-line arguments
 */
function parseArgs() {
  const args = process.argv.slice(2);
  
  const config = {
    input: null,
    outputDir: null,
    headless: true,
    userDataDir: '../../../stock-crawler/chrome_user_data',
    startFrom: 0,
    limit: null
  };
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--input' && i + 1 < args.length) {
      config.input = args[++i];
    } else if (arg === '--output-dir' && i + 1 < args.length) {
      config.outputDir = args[++i];
    } else if (arg === '--headless') {
      config.headless = args[++i] !== 'false';
    } else if (arg === '--user-data-dir' && i + 1 < args.length) {
      config.userDataDir = args[++i];
    } else if (arg === '--start-from' && i + 1 < args.length) {
      config.startFrom = parseInt(args[++i], 10);
    } else if (arg === '--limit' && i + 1 < args.length) {
      config.limit = parseInt(args[++i], 10);
    }
  }
  
  if (!config.input || !config.outputDir) {
    console.error('Usage: node batch-generate-templates.js --input <patterns-file> --output-dir <output-directory>');
    process.exit(1);
  }
  
  return config;
}

/**
 * Main function
 */
async function main() {
  const config = parseArgs();
  
  console.log('🚀 Batch Template Generator');
  console.log('━'.repeat(60));
  
  // Read patterns file
  const inputPath = path.resolve(config.input);
  let patternsData;
  try {
    patternsData = JSON.parse(fs.readFileSync(inputPath, 'utf-8'));
  } catch (error) {
    console.error(`Error: Failed to parse JSON file ${inputPath}: ${error.message}`);
    process.exit(1);
  }
  const patterns = patternsData.patterns || [];
  
  console.log(`📊 Total patterns: ${patterns.length}`);
  console.log(`📁 Output directory: ${config.outputDir}`);
  console.log(`🎯 Start from: ${config.startFrom}`);
  if (config.limit) {
    console.log(`🔢 Limit: ${config.limit}`);
  }
  console.log('━'.repeat(60));
  
  // Create output directory
  const outputDir = path.resolve(config.outputDir);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
    console.log(`✅ Created output directory: ${outputDir}`);
  }
  
  // Filter patterns
  let patternsToProcess = patterns.slice(config.startFrom);
  if (config.limit) {
    patternsToProcess = patternsToProcess.slice(0, config.limit);
  }
  
  console.log(`\n📝 Processing ${patternsToProcess.length} patterns...\n`);
  
  // Create generator instance
  const userDataDir = path.resolve(__dirname, config.userDataDir);
  const generator = new TemplateGenerator({
    browser: {
      userDataDir,
      headless: config.headless,
      channel: 'chrome',
      timeout: 30000
    }
  });
  
  // Process each pattern
  const results = {
    success: [],
    failed: [],
    skipped: []
  };
  
  for (let i = 0; i < patternsToProcess.length; i++) {
    const pattern = patternsToProcess[i];
    const index = config.startFrom + i;
    const templateName = pattern.name;
    const outputPath = path.join(outputDir, `${templateName}.json`);
    
    console.log(`\n[${index + 1}/${patterns.length}] Processing: ${templateName}`);
    console.log(`  Description: ${pattern.description}`);
    console.log(`  URLs: ${pattern.urlCount}`);
    
    // Skip if already exists
    if (fs.existsSync(outputPath)) {
      console.log(`  ⏭️  Skipped (already exists)`);
      results.skipped.push(templateName);
      continue;
    }
    
    try {
      await generator.generate(templateName, inputPath, outputPath);
      console.log(`  ✅ Success: ${outputPath}`);
      results.success.push(templateName);
    } catch (error) {
      console.error(`  ❌ Failed: ${error.message}`);
      results.failed.push({ name: templateName, error: error.message });
    }
  }
  
  // Summary
  console.log('\n' + '━'.repeat(60));
  console.log('📊 Summary');
  console.log('━'.repeat(60));
  console.log(`✅ Success: ${results.success.length}`);
  console.log(`❌ Failed: ${results.failed.length}`);
  console.log(`⏭️  Skipped: ${results.skipped.length}`);
  
  if (results.failed.length > 0) {
    console.log('\n❌ Failed patterns:');
    results.failed.forEach(({ name, error }) => {
      console.log(`  - ${name}: ${error}`);
    });
  }
  
  console.log('\n✨ Done!');
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});

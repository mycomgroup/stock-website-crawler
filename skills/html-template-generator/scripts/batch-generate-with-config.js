#!/usr/bin/env node

/**
 * Batch Template Generator with Configuration Support
 * 
 * Generate templates for patterns with full configuration control
 */

import { TemplateGenerator } from '../main.js';
import { ConfigLoader } from '../lib/config-loader.js';
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
  
  if (args.includes('--help') || args.includes('-h')) {
    showHelp();
    process.exit(0);
  }
  
  const config = {
    input: null,
    outputDir: null,
    configFile: null,
    startFrom: 0,
    limit: null,
    skipExisting: true,
    cliArgs: {}
  };
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--input' && i + 1 < args.length) {
      config.input = args[++i];
    } else if (arg === '--output-dir' && i + 1 < args.length) {
      config.outputDir = args[++i];
    } else if (arg === '--config' && i + 1 < args.length) {
      config.configFile = args[++i];
    } else if (arg === '--start-from' && i + 1 < args.length) {
      config.startFrom = parseInt(args[++i], 10);
    } else if (arg === '--limit' && i + 1 < args.length) {
      config.limit = parseInt(args[++i], 10);
    } else if (arg === '--skip-existing' && i + 1 < args.length) {
      config.skipExisting = args[++i] !== 'false';
    } else if (arg === '--include-patterns' && i + 1 < args.length) {
      config.cliArgs.includePatterns = args[++i];
    } else if (arg === '--exclude-patterns' && i + 1 < args.length) {
      config.cliArgs.excludePatterns = args[++i];
    } else if (arg === '--priority-patterns' && i + 1 < args.length) {
      config.cliArgs.priorityPatterns = args[++i];
    } else if (arg === '--headless' && i + 1 < args.length) {
      config.cliArgs.headless = args[++i] !== 'false';
    } else if (arg === '--max-samples' && i + 1 < args.length) {
      config.cliArgs.maxSamples = parseInt(args[++i], 10);
    } else if (arg === '--frequency-threshold' && i + 1 < args.length) {
      config.cliArgs.frequencyThreshold = parseFloat(args[++i]);
    }
  }
  
  if (!config.input || !config.outputDir) {
    console.error('Error: --input and --output-dir are required');
    showHelp();
    process.exit(1);
  }
  
  return config;
}

/**
 * Show help information
 */
function showHelp() {
  console.log(`
Batch Template Generator with Configuration Support

Usage: node batch-generate-with-config.js [options]

Required Options:
  --input <path>              Path to url-patterns.json
  --output-dir <path>         Directory for output template files

Optional:
  --config <path>             Path to config file (default: config/default.json)
  --start-from <n>            Start from pattern index (default: 0)
  --limit <n>                 Limit number of patterns to process
  --skip-existing <bool>      Skip existing template files (default: true)
  
  --include-patterns <list>   Comma-separated patterns to include (supports *)
  --exclude-patterns <list>   Comma-separated patterns to exclude (supports *)
  --priority-patterns <list>  Comma-separated patterns to process first
  
  --headless <bool>           Run browser in headless mode
  --max-samples <n>           Maximum number of sample pages
  --frequency-threshold <n>   Element frequency threshold (0-1)

Examples:
  # Basic usage with default config
  node batch-generate-with-config.js \\
    --input url-patterns.json \\
    --output-dir output/templates

  # Use quick-test config for first 5 patterns
  node batch-generate-with-config.js \\
    --input url-patterns.json \\
    --output-dir output/templates \\
    --config config/quick-test.json \\
    --limit 5

  # Generate only API and detail patterns
  node batch-generate-with-config.js \\
    --input url-patterns.json \\
    --output-dir output/templates \\
    --include-patterns "api-*,detail-*"

  # Generate with priority order
  node batch-generate-with-config.js \\
    --input url-patterns.json \\
    --output-dir output/templates \\
    --priority-patterns "api-doc,detail-sh,detail-sz"

  # Production batch with detail-pages config
  node batch-generate-with-config.js \\
    --input url-patterns.json \\
    --output-dir output/templates \\
    --config config/detail-pages.json \\
    --max-samples 5

  # Resume from pattern 50
  node batch-generate-with-config.js \\
    --input url-patterns.json \\
    --output-dir output/templates \\
    --start-from 50

Config Files:
  config/default.json       - Default configuration
  config/quick-test.json    - Fast testing (2 samples, visible browser)
  config/production.json    - Production quality (5 samples, strict)
  config/detail-pages.json  - Optimized for detail/content pages
  config/list-pages.json    - Optimized for list/index pages
  config/table-pages.json   - Optimized for table/data pages
  `);
}

/**
 * Match pattern with wildcard support
 */
function matchPattern(name, pattern) {
  const regex = new RegExp('^' + pattern.replace(/\*/g, '.*') + '$');
  return regex.test(name);
}

/**
 * Filter patterns based on include/exclude rules
 */
function filterPatterns(patterns, config) {
  let filtered = [...patterns];
  
  // Apply include filter
  if (config.patterns.include && config.patterns.include.length > 0) {
    filtered = filtered.filter(p => 
      config.patterns.include.some(pattern => matchPattern(p.name, pattern))
    );
  }
  
  // Apply exclude filter
  if (config.patterns.exclude && config.patterns.exclude.length > 0) {
    filtered = filtered.filter(p => 
      !config.patterns.exclude.some(pattern => matchPattern(p.name, pattern))
    );
  }
  
  return filtered;
}

/**
 * Sort patterns by priority
 */
function sortByPriority(patterns, priorityList) {
  if (!priorityList || priorityList.length === 0) {
    return patterns;
  }
  
  const priorityMap = new Map();
  priorityList.forEach((name, index) => {
    priorityMap.set(name, index);
  });
  
  return patterns.sort((a, b) => {
    const aPriority = priorityMap.has(a.name) ? priorityMap.get(a.name) : 9999;
    const bPriority = priorityMap.has(b.name) ? priorityMap.get(b.name) : 9999;
    return aPriority - bPriority;
  });
}

/**
 * Main function
 */
async function main() {
  const config = parseArgs();
  
  console.log('🚀 Batch Template Generator');
  console.log('━'.repeat(60));
  
  // Load configuration
  const configLoader = new ConfigLoader();
  const fullConfig = await configLoader.load(config.configFile, config.cliArgs);
  configLoader.validate(fullConfig);
  
  console.log('⚙️  Configuration:');
  if (config.configFile) {
    console.log(`   Config file: ${config.configFile}`);
  }
  console.log(`   Frequency threshold: ${fullConfig.analysis.frequencyThreshold}`);
  console.log(`   Max samples: ${fullConfig.fetching.maxSamples}`);
  console.log(`   Headless: ${fullConfig.browser.headless}`);
  console.log(`   Detect page type: ${fullConfig.analysis.detectPageType}`);
  
  // Read patterns file
  const inputPath = path.resolve(config.input);
  const patternsData = JSON.parse(fs.readFileSync(inputPath, 'utf-8'));
  let patterns = patternsData.patterns || [];
  
  console.log(`\n📊 Total patterns in file: ${patterns.length}`);
  
  // Filter patterns
  patterns = filterPatterns(patterns, fullConfig);
  console.log(`📊 After filtering: ${patterns.length}`);
  
  if (fullConfig.patterns.include && fullConfig.patterns.include.length > 0) {
    console.log(`   Include: ${fullConfig.patterns.include.join(', ')}`);
  }
  if (fullConfig.patterns.exclude && fullConfig.patterns.exclude.length > 0) {
    console.log(`   Exclude: ${fullConfig.patterns.exclude.join(', ')}`);
  }
  
  // Sort by priority
  if (fullConfig.patterns.priority && fullConfig.patterns.priority.length > 0) {
    patterns = sortByPriority(patterns, fullConfig.patterns.priority);
    console.log(`📊 Priority order: ${fullConfig.patterns.priority.join(', ')}`);
  }
  
  // Apply start-from and limit
  const totalPatterns = patterns.length;
  patterns = patterns.slice(config.startFrom);
  if (config.limit) {
    patterns = patterns.slice(0, config.limit);
  }
  
  console.log(`\n📝 Processing ${patterns.length} patterns (from ${config.startFrom} to ${config.startFrom + patterns.length})`);
  console.log(`📁 Output directory: ${config.outputDir}`);
  console.log('━'.repeat(60));
  
  // Create output directory
  const outputDir = path.resolve(config.outputDir);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
    console.log(`✅ Created output directory: ${outputDir}`);
  }
  
  // Create generator instance
  const userDataDir = path.resolve(__dirname, fullConfig.browser.userDataDir);
  const generator = new TemplateGenerator({
    browser: {
      ...fullConfig.browser,
      userDataDir
    },
    fetching: fullConfig.fetching,
    analysis: fullConfig.analysis,
    xpath: fullConfig.xpath,
    filters: fullConfig.filters
  });
  
  // Process each pattern
  const results = {
    success: [],
    failed: [],
    skipped: []
  };
  
  const startTime = Date.now();
  
  for (let i = 0; i < patterns.length; i++) {
    const pattern = patterns[i];
    const index = config.startFrom + i;
    const templateName = pattern.name;
    const outputPath = path.join(outputDir, `${templateName}.json`);
    
    console.log(`\n[${i + 1}/${patterns.length}] Processing: ${templateName}`);
    console.log(`  Description: ${pattern.description || 'N/A'}`);
    console.log(`  URLs: ${pattern.urlCount || pattern.urls?.length || 0}`);
    
    // Skip if already exists
    if (config.skipExisting && fs.existsSync(outputPath)) {
      console.log(`  ⏭️  Skipped (already exists)`);
      results.skipped.push(templateName);
      continue;
    }
    
    try {
      const patternStartTime = Date.now();
      await generator.generate(templateName, inputPath, outputPath);
      const duration = ((Date.now() - patternStartTime) / 1000).toFixed(1);
      console.log(`  ✅ Success (${duration}s): ${outputPath}`);
      results.success.push(templateName);
    } catch (error) {
      console.error(`  ❌ Failed: ${error.message}`);
      results.failed.push({ name: templateName, error: error.message });
    }
  }
  
  const totalDuration = ((Date.now() - startTime) / 1000).toFixed(1);
  
  // Summary
  console.log('\n' + '━'.repeat(60));
  console.log('📊 Summary');
  console.log('━'.repeat(60));
  console.log(`✅ Success: ${results.success.length}`);
  console.log(`❌ Failed: ${results.failed.length}`);
  console.log(`⏭️  Skipped: ${results.skipped.length}`);
  console.log(`⏱️  Total time: ${totalDuration}s`);
  
  if (results.success.length > 0) {
    const avgTime = (totalDuration / results.success.length).toFixed(1);
    console.log(`⏱️  Average time per template: ${avgTime}s`);
  }
  
  if (results.failed.length > 0) {
    console.log('\n❌ Failed patterns:');
    results.failed.forEach(({ name, error }) => {
      console.log(`  - ${name}: ${error}`);
    });
  }
  
  console.log('\n✨ Done!');
  
  // Exit with error code if any failures
  process.exit(results.failed.length > 0 ? 1 : 0);
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});

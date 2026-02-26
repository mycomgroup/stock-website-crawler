#!/usr/bin/env node

/**
 * HTML Template Generator - CLI Runner
 * 
 * Generate XPath extraction templates from sample URLs
 * 
 * Usage:
 *   node run-skill.js <templateName> [options]
 * 
 * Example:
 *   node run-skill.js api-doc \
 *     --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
 *     --output ./output/api-doc.json
 */

import { TemplateGenerator } from './main.js';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Parse command-line arguments
 */
function parseArgs() {
  const args = process.argv.slice(2);
  
  // Show help if no arguments or help flag
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    showHelp();
    process.exit(0);
  }
  
  const config = {
    templateName: args[0],
    input: null,
    output: null,
    headless: true,
    userDataDir: '../../stock-crawler/chrome_user_data'
  };
  
  // Parse options
  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--input' && i + 1 < args.length) {
      config.input = args[++i];
    } else if (arg === '--output' && i + 1 < args.length) {
      config.output = args[++i];
    } else if (arg === '--headless') {
      config.headless = args[++i] !== 'false';
    } else if (arg === '--user-data-dir' && i + 1 < args.length) {
      config.userDataDir = args[++i];
    }
  }
  
  // Validate required arguments
  if (!config.templateName) {
    console.error('Error: Template name is required');
    showHelp();
    process.exit(1);
  }
  
  if (!config.input) {
    console.error('Error: --input parameter is required');
    showHelp();
    process.exit(1);
  }
  
  if (!config.output) {
    console.error('Error: --output parameter is required');
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
HTML Template Generator - CLI Runner

Generate XPath extraction templates from sample URLs

Usage:
  node run-skill.js <templateName> [options]

Arguments:
  templateName           Template name from url-patterns.json (e.g., api-doc)

Options:
  --input <path>         Path to url-patterns.json file (required)
  --output <path>        Path to output template JSON file (required)
  --headless <bool>      Run browser in headless mode (default: true)
  --user-data-dir <path> Path to Chrome user data directory
                         (default: ../../stock-crawler/chrome_user_data)
  --help, -h             Show this help message

Examples:
  # Generate template for api-doc pattern
  node run-skill.js api-doc \\
    --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \\
    --output ./output/api-doc.json

  # Generate with custom user data directory
  node run-skill.js detail-sh \\
    --input ./url-patterns.json \\
    --output ./output/detail-sh.json \\
    --user-data-dir /path/to/chrome_user_data

  # Run with visible browser (non-headless)
  node run-skill.js api-doc \\
    --input ./url-patterns.json \\
    --output ./output/api-doc.json \\
    --headless false

Output:
  The generated template will be saved as a JSON file containing:
  - XPath extraction rules for page elements
  - Filter rules to remove noise
  - Metadata about the analysis

  The template can be used to extract structured data from HTML pages
  matching the pattern.

Notes:
  - The input file must be a valid url-patterns.json file
  - The template name must exist in the url-patterns.json file
  - The browser will use the specified user data directory for login state
  - Output directory will be created automatically if it doesn't exist
  `);
}

/**
 * Display progress information
 */
function displayProgress(message, type = 'info') {
  const timestamp = new Date().toLocaleTimeString();
  const prefix = {
    info: 'ℹ',
    success: '✓',
    error: '✗',
    warning: '⚠'
  }[type] || 'ℹ';
  
  console.log(`[${timestamp}] ${prefix} ${message}`);
}

/**
 * Main function
 */
async function main() {
  try {
    // Parse command-line arguments
    const config = parseArgs();
    
    displayProgress('Starting HTML Template Generator', 'info');
    displayProgress(`Template: ${config.templateName}`, 'info');
    displayProgress(`Input: ${config.input}`, 'info');
    displayProgress(`Output: ${config.output}`, 'info');
    
    // Resolve paths
    const inputPath = path.resolve(config.input);
    const outputPath = path.resolve(config.output);
    const userDataDir = path.resolve(__dirname, config.userDataDir);
    
    displayProgress(`Resolved input path: ${inputPath}`, 'info');
    displayProgress(`Resolved output path: ${outputPath}`, 'info');
    displayProgress(`User data directory: ${userDataDir}`, 'info');
    
    // Create generator instance
    const generator = new TemplateGenerator({
      browser: {
        userDataDir,
        headless: config.headless,
        channel: 'chrome',
        timeout: 30000
      }
    });
    
    // Generate template
    displayProgress('Generating template...', 'info');
    await generator.generate(config.templateName, inputPath, outputPath);
    
    displayProgress('Template generation completed successfully!', 'success');
    displayProgress(`Output saved to: ${outputPath}`, 'success');
    
    process.exit(0);
    
  } catch (error) {
    displayProgress(`Error: ${error.message}`, 'error');
    
    // Show helpful error messages
    if (error.message.includes('not found')) {
      console.error('\nTroubleshooting:');
      console.error('  - Check that the input file path is correct');
      console.error('  - Check that the template name exists in url-patterns.json');
      console.error('  - Ensure the file is readable');
    } else if (error.message.includes('browser')) {
      console.error('\nTroubleshooting:');
      console.error('  - Check that Chrome/Chromium is installed');
      console.error('  - Check that the user data directory exists');
      console.error('  - Try running with --headless false to see browser errors');
    } else if (error.message.includes('fetch')) {
      console.error('\nTroubleshooting:');
      console.error('  - Check your internet connection');
      console.error('  - Check that the URLs are accessible');
      console.error('  - Verify login state in user data directory');
    }
    
    console.error('\nFor more help, run: node run-skill.js --help');
    
    process.exit(1);
  }
}

// Run main function
main();

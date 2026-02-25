#!/usr/bin/env node

/**
 * Migration script to move old output files to new directory structure
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function migrateOutput(oldDir, newDir) {
  console.log('Output Migration Script');
  console.log('======================\n');

  // Check if old directory exists
  if (!fs.existsSync(oldDir)) {
    console.error(`Error: Old output directory not found: ${oldDir}`);
    process.exit(1);
  }

  // Create new directory if it doesn't exist
  if (!fs.existsSync(newDir)) {
    fs.mkdirSync(newDir, { recursive: true });
    console.log(`Created new output directory: ${newDir}`);
  }

  // Get all markdown files from old directory
  const files = fs.readdirSync(oldDir).filter(file => file.endsWith('.md'));
  console.log(`Found ${files.length} Markdown files to migrate`);

  if (files.length === 0) {
    console.log('No files to migrate.');
    return;
  }

  // Copy files to new directory
  let copiedCount = 0;
  let skippedCount = 0;

  for (const file of files) {
    const oldPath = path.join(oldDir, file);
    const newPath = path.join(newDir, file);

    // Check if file already exists in new location
    if (fs.existsSync(newPath)) {
      console.log(`Skipping (already exists): ${file}`);
      skippedCount++;
      continue;
    }

    // Copy file
    fs.copyFileSync(oldPath, newPath);
    console.log(`Copied: ${file}`);
    copiedCount++;
  }

  console.log(`\nMigration Summary:`);
  console.log(`  Copied: ${copiedCount} files`);
  console.log(`  Skipped: ${skippedCount} files`);
  console.log(`\nMigration completed successfully!`);
  console.log(`\nNote: Original files are preserved in ${oldDir}`);
}

// Main execution
const args = process.argv.slice(2);

if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
  console.log(`
Usage:
  node scripts/migrate-output.js <old-output-dir> <new-output-dir>

Arguments:
  <old-output-dir>    Path to the old output directory
  <new-output-dir>    Path to the new output directory

Examples:
  node scripts/migrate-output.js ../api-docs ./output
  node scripts/migrate-output.js ../old-output ./output
  `);
  process.exit(0);
}

if (args.length < 2) {
  console.error('Error: Both old and new directory paths are required');
  console.log('Run with --help for usage information');
  process.exit(1);
}

const oldDir = path.resolve(args[0]);
const newDir = path.resolve(args[1]);

try {
  migrateOutput(oldDir, newDir);
} catch (error) {
  console.error('\nError during migration:', error.message);
  process.exit(1);
}

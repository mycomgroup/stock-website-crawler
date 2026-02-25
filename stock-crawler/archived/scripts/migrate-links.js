#!/usr/bin/env node

/**
 * Migration script to convert old links.txt format to new format
 * Old format: Simple URLs, one per line
 * New format: JSON objects with status tracking, one per line
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function migrateLinks(oldFilePath, newFilePath) {
  console.log('Link Migration Script');
  console.log('====================\n');

  // Check if old file exists
  if (!fs.existsSync(oldFilePath)) {
    console.error(`Error: Old links file not found: ${oldFilePath}`);
    process.exit(1);
  }

  // Read old file
  console.log(`Reading old links from: ${oldFilePath}`);
  const oldContent = fs.readFileSync(oldFilePath, 'utf-8');
  const oldLines = oldContent.split('\n').filter(line => line.trim() !== '');
  console.log(`Found ${oldLines.length} URLs in old format`);

  // Convert to new format
  const newLinks = oldLines.map(url => {
    const trimmedUrl = url.trim();
    
    // Check if it's already in JSON format
    if (trimmedUrl.startsWith('{')) {
      try {
        return JSON.parse(trimmedUrl);
      } catch (e) {
        // If parsing fails, treat as simple URL
      }
    }

    // Convert simple URL to new format
    return {
      url: trimmedUrl,
      status: 'pending',
      addedAt: Date.now(),
      crawledAt: null,
      retryCount: 0,
      error: null
    };
  });

  // Write new file
  console.log(`Writing new links to: ${newFilePath}`);
  const newContent = newLinks.map(link => JSON.stringify(link)).join('\n');
  fs.writeFileSync(newFilePath, newContent, 'utf-8');
  console.log(`Successfully migrated ${newLinks.length} links`);

  // Create backup of old file
  const backupPath = oldFilePath + '.backup';
  fs.copyFileSync(oldFilePath, backupPath);
  console.log(`\nBackup created: ${backupPath}`);
  console.log('\nMigration completed successfully!');
}

// Main execution
const args = process.argv.slice(2);

if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
  console.log(`
Usage:
  node scripts/migrate-links.js <old-links-file> [new-links-file]

Arguments:
  <old-links-file>    Path to the old links.txt file
  [new-links-file]    Path for the new links.txt file (optional, defaults to same as old)

Examples:
  node scripts/migrate-links.js ../links.txt
  node scripts/migrate-links.js ../links.txt ./links.txt
  `);
  process.exit(0);
}

const oldFilePath = path.resolve(args[0]);
const newFilePath = args[1] ? path.resolve(args[1]) : oldFilePath;

try {
  migrateLinks(oldFilePath, newFilePath);
} catch (error) {
  console.error('\nError during migration:', error.message);
  process.exit(1);
}

#!/usr/bin/env node

import fs from 'fs/promises';
import path from 'path';
import { StructureComparator } from '../lib/structure-comparator.js';

function parseArgs() {
  const args = process.argv.slice(2);
  const config = { input: null, output: null };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--input') config.input = args[++i];
    else if (arg === '--output') config.output = args[++i];
  }

  if (!config.input || !config.output) {
    console.error('Usage: node scripts/compare-extracted-structures.js --input <extracted.jsonl> --output <comparison.json>');
    process.exit(1);
  }

  return config;
}

async function main() {
  const args = parseArgs();
  const content = await fs.readFile(path.resolve(args.input), 'utf-8');
  const records = content.split(/\r?\n/).map(line => line.trim()).filter(Boolean).map(line => JSON.parse(line));

  const comparator = new StructureComparator();
  const result = comparator.compare(records);

  await fs.mkdir(path.dirname(path.resolve(args.output)), { recursive: true });
  await fs.writeFile(path.resolve(args.output), JSON.stringify(result, null, 2));

  console.log(`✅ Comparison saved: ${args.output}`);
  console.log(`commonSectionHeadings: ${result.commonSectionHeadings.join(', ') || '(none)'}`);
  console.log(`commonTableHeaders: ${result.commonTableHeaders.join(', ') || '(none)'}`);
}

main().catch((err) => {
  console.error(`❌ ${err.message}`);
  process.exit(1);
});

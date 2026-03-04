#!/usr/bin/env node

/**
 * Apply human feedback as manualOverrides into template files.
 *
 * feedback json format:
 * {
 *   "template": "api-doc",
 *   "overrides": {
 *     "title": "//h1/text()",
 *     "sections": { "xpath": "//main/section" }
 *   }
 * }
 */

import fs from 'fs/promises';
import path from 'path';

function parseArgs() {
  const args = process.argv.slice(2);
  const config = {
    templateFile: null,
    feedbackFile: null,
    outputFile: null
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--template-file') config.templateFile = args[++i];
    else if (arg === '--feedback-file') config.feedbackFile = args[++i];
    else if (arg === '--output-file') config.outputFile = args[++i];
  }

  if (!config.templateFile || !config.feedbackFile || !config.outputFile) {
    console.error('Usage: node scripts/apply-feedback-overrides.js --template-file <template.json> --feedback-file <feedback.json> --output-file <optimized-template.json>');
    process.exit(1);
  }

  return config;
}

function deepMerge(target, source) {
  if (!source || typeof source !== 'object' || Array.isArray(source)) {
    return source;
  }

  const out = { ...(target || {}) };
  for (const [key, value] of Object.entries(source)) {
    if (value && typeof value === 'object' && !Array.isArray(value)) {
      out[key] = deepMerge(out[key], value);
    } else {
      out[key] = value;
    }
  }
  return out;
}

async function main() {
  const args = parseArgs();
  const templatePath = path.resolve(args.templateFile);
  const feedbackPath = path.resolve(args.feedbackFile);
  const outputPath = path.resolve(args.outputFile);

  const template = JSON.parse(await fs.readFile(templatePath, 'utf-8'));
  const feedback = JSON.parse(await fs.readFile(feedbackPath, 'utf-8'));

  if (!feedback.overrides || typeof feedback.overrides !== 'object') {
    throw new Error('feedback.overrides is required and must be an object');
  }

  const mergedOverrides = deepMerge(template.manualOverrides || {}, feedback.overrides);

  const output = {
    ...template,
    manualOverrides: mergedOverrides,
    optimizedAt: new Date().toISOString(),
    optimizationNotes: feedback.notes || ''
  };

  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.writeFile(outputPath, JSON.stringify(output, null, 2));

  console.log(`✅ Optimized template saved: ${outputPath}`);
}

main().catch((err) => {
  console.error(`❌ ${err.message}`);
  process.exit(1);
});

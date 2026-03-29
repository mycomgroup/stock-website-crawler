#!/usr/bin/env node
import fs from 'fs';
import path from 'path';
import { runNotebookTest } from '../skills/joinquant_nookbook/request/test-joinquant-notebook.js';

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const current = argv[i];
    if (!current.startsWith('--')) continue;
    const key = current.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args['cell-source-file']) {
    throw new Error('缺少 --cell-source-file');
  }

  const cellSourcePath = path.resolve(args['cell-source-file']);
  const cellSource = fs.readFileSync(cellSourcePath, 'utf8');

  const result = await runNotebookTest({
    sessionFile: args['session-file'],
    notebookUrl: args['notebook-url'],
    mode: args.mode,
    cellSource,
    cellIndex: args['cell-index'],
    timeoutMs: args['timeout-ms'],
    kernelName: args['kernel-name'],
    appendCell: args['append-cell'] === 'false' ? false : true,
  });

  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error.message}\n`);
  process.exitCode = 1;
});

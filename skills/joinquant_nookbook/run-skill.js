#!/usr/bin/env node
import { runNotebookTest } from './request/test-joinquant-notebook.js';

function parseArgs(argv) {
  const args = {};
  for (let index = 0; index < argv.length; index += 1) {
    const current = argv[index];
    if (!current.startsWith('--')) continue;
    const key = current.slice(2);
    const next = argv[index + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    index += 1;
  }
  return args;
}

const args = parseArgs(process.argv.slice(2));

const result = await runNotebookTest({
  sessionFile: args['session-file'],
  notebookUrl: args['notebook-url'],
  mode: args.mode,
  cellSource: args['cell-source'],
  cellIndex: args['cell-index'],
  timeoutMs: args['timeout-ms'],
  kernelName: args['kernel-name'],
  appendCell: args['append-cell'] === 'false' ? false : true
});

process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);

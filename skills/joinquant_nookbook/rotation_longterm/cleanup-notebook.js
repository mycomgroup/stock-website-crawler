#!/usr/bin/env node
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { JoinQuantClient } from '../request/joinquant-client.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SESSION_FILE = resolve(__dirname, '..', 'data', 'session.json');
const OUTPUT_ROOT = resolve(__dirname, 'output');
const NOTEBOOK_URL = 'https://www.joinquant.com/research?target=research&url=/user/21333940833/notebooks/rotation_longterm_analysis.ipynb';
const CELL_MARKER = '# AUTO_ROTATION_ANALYSIS_30D';
const BASE_CELL_COUNT = 3;

export async function main() {
  const client = new JoinQuantClient({
    sessionFile: SESSION_FILE,
    notebookUrl: NOTEBOOK_URL,
    outputRoot: OUTPUT_ROOT
  });

  const model = await client.getNotebookModel();
  const cells = model.content?.cells || [];
  const keptCells = cells.filter((cell, index) => {
    const source = Array.isArray(cell.source) ? cell.source.join('') : String(cell.source || '');
    return index < BASE_CELL_COUNT || source.includes(CELL_MARKER);
  });

  model.content.cells = keptCells;
  await client.saveNotebook(model.content);
  const snapshotPath = client.writeArtifact('joinquant-notebook-cleaned', model.content, 'ipynb');

  console.log(`清理完成，保留 ${keptCells.length} 个 cell`);
  console.log(`Notebook: ${client.directNotebookUrl}`);
  console.log(`快照: ${snapshotPath}`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main().catch(error => {
    console.error('清理失败:', error.stack || error.message);
    process.exit(1);
  });
}

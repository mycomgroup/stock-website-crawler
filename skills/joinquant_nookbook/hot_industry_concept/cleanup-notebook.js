#!/usr/bin/env node
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { JoinQuantClient } from '../request/joinquant-client.js';
import { ensureJoinQuantSession } from '../request/ensure-joinquant-session.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SESSION_FILE = resolve(__dirname, '..', 'data', 'session.json');
const OUTPUT_ROOT = resolve(__dirname, 'output');
const NOTEBOOK_URL = 'https://www.joinquant.com/research?target=research&url=/user/21333940833/notebooks/hot_industry_concept_analysis.ipynb';

export async function main() {
  await ensureJoinQuantSession({
    sessionFile: SESSION_FILE,
    notebookUrl: NOTEBOOK_URL,
    outputRoot: OUTPUT_ROOT
  });

  const client = new JoinQuantClient({
    sessionFile: SESSION_FILE,
    notebookUrl: NOTEBOOK_URL,
    outputRoot: OUTPUT_ROOT
  });

  const model = await client.getNotebookModel();
  await client.saveNotebook(model.content);
  const snapshotPath = client.writeArtifact('joinquant-notebook-cleaned', model.content, 'ipynb');

  console.log('清理完成（保留原 notebook 结构，仅生成快照）');
  console.log(`Notebook: ${client.directNotebookUrl}`);
  console.log(`快照: ${snapshotPath}`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main().catch(error => {
    console.error('清理失败:', error.stack || error.message);
    process.exit(1);
  });
}

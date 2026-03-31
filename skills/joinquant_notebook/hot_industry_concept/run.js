#!/usr/bin/env node
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { JoinQuantClient } from '../request/joinquant-client.js';
import { ensureJoinQuantSession } from '../request/ensure-joinquant-session.js';
import { runNotebookTest } from '../request/test-joinquant-notebook.js';
import { formatHotIndustryConceptSummary, summarizeHotIndustryConceptResult } from './summarize-result.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SESSION_FILE = resolve(__dirname, '..', 'data', 'session.json');
const OUTPUT_ROOT = resolve(__dirname, 'output');
const SOURCE_NOTEBOOK_URL = 'https://www.joinquant.com/research?target=research&url=/user/21333940833/notebooks/98%20%E7%83%AD%E7%82%B9%E8%A1%8C%E4%B8%9A%E5%92%8C%E7%83%AD%E7%82%B9%E6%A6%82%E5%BF%B5-%E6%88%90%E5%88%86%E8%82%A1-%E5%8F%8A%E9%BE%99%E4%B8%80%E9%BE%99%E4%BA%8C%E9%BE%99%E4%B8%89-for%20agent.ipynb';
const NOTEBOOK_URL = 'https://www.joinquant.com/research?target=research&url=/user/21333940833/notebooks/hot_industry_concept_analysis.ipynb';

async function ensureNotebookExists() {
  const targetClient = new JoinQuantClient({
    sessionFile: SESSION_FILE,
    notebookUrl: NOTEBOOK_URL,
    outputRoot: OUTPUT_ROOT
  });

  try {
    await targetClient.getNotebookMetadata();
    return { created: false };
  } catch (error) {
    if (!String(error.message || '').includes('404')) {
      throw error;
    }
  }

  const sourceClient = new JoinQuantClient({
    sessionFile: SESSION_FILE,
    notebookUrl: SOURCE_NOTEBOOK_URL,
    outputRoot: OUTPUT_ROOT
  });
  const sourceModel = await sourceClient.getNotebookModel();
  await targetClient.saveNotebook(sourceModel.content);
  return { created: true };
}

export async function main() {
  await ensureJoinQuantSession({
    sessionFile: SESSION_FILE,
    notebookUrl: SOURCE_NOTEBOOK_URL,
    outputRoot: OUTPUT_ROOT
  });

  const { created } = await ensureNotebookExists();
  console.log(created ? '已创建热点行业/概念分析 notebook，开始执行全部代码单元...' : '将复用热点行业/概念分析 notebook，并重新执行全部代码单元...');

  const result = await runNotebookTest({
    sessionFile: SESSION_FILE,
    outputRoot: OUTPUT_ROOT,
    notebookUrl: NOTEBOOK_URL,
    mode: 'all',
    timeoutMs: 900000,
    kernelName: 'python3',
    appendCell: false
  });

  const executions = result.executions || [];
  const lastExecution = executions[executions.length - 1];

  const summary = summarizeHotIndustryConceptResult(result.resultFile, { writeSummary: true });

  console.log(`Notebook: ${result.notebookUrl}`);
  console.log(`结果文件: ${result.resultFile}`);
  console.log(`Notebook 快照: ${result.notebookSnapshotPath}`);
  console.log(`摘要文件: ${summary.summaryFile}`);
  console.log(`执行 cell 数: ${executions.length}`);

  if (lastExecution?.textOutput) {
    console.log('\n最后一个 cell 输出前 6000 字：\n');
    console.log(lastExecution.textOutput.slice(0, 6000));
  }

  console.log('\n本地摘要：\n');
  console.log(formatHotIndustryConceptSummary(summary));

  return {
    ...result,
    summary
  };
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main().catch(error => {
    console.error('主程序错误:', error.stack || error.message);
    process.exit(1);
  });
}

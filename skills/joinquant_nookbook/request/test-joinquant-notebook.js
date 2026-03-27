#!/usr/bin/env node
import { JoinQuantClient, createCodeCell } from './joinquant-client.js';

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

function normalizeCellSource(cellSource) {
  return String(cellSource || 'print("hello")');
}

function parseCellIndices(input, notebookContent) {
  if (!input || input === 'last') {
    return [notebookContent.cells.length - 1];
  }
  return String(input)
    .split(',')
    .map(item => Number(item.trim()))
    .filter(Number.isInteger)
    .filter(index => index >= 0 && index < notebookContent.cells.length);
}

function resolveRunCellIndices(mode, notebookContent, explicitCellIndex) {
  if (mode === 'all') {
    return notebookContent.cells
      .map((cell, index) => ({ cell, index }))
      .filter(item => item.cell?.cell_type === 'code')
      .map(item => item.index);
  }
  return parseCellIndices(explicitCellIndex, notebookContent);
}

function summarizeExecution(result) {
  return {
    msgId: result.msgId,
    websocketSessionId: result.websocketSessionId,
    executionCount: result.executionCount,
    status: result.reply?.status || 'unknown',
    textOutput: result.textOutput,
    outputs: result.outputs
  };
}

export async function runNotebookTest(options = {}) {
  const client = new JoinQuantClient(options);
  const mode = options.mode === 'all' ? 'all' : 'partial';
  const appendCell = options.appendCell !== false;
  const cellSource = normalizeCellSource(options.cellSource);
  const timeoutMs = Number(options.timeoutMs || 30000);

  const notebookModel = await client.getNotebookModel();
  const notebookContent = notebookModel.content;
  if (!notebookContent?.cells) {
    throw new Error('未获取到 notebook content.cells');
  }

  let appendedCellIndex = null;
  if (appendCell) {
    notebookContent.cells.push(createCodeCell(cellSource));
    appendedCellIndex = notebookContent.cells.length - 1;
    await client.saveNotebook(notebookContent);
  }

  const session = await client.ensureSession({ kernelName: options.kernelName || 'python3' });
  const kernelId = session?.kernel?.id;
  if (!kernelId) {
    throw new Error('未能创建 kernel session');
  }

  const targetCellIndices = resolveRunCellIndices(
    mode,
    notebookContent,
    options.cellIndex || (appendCell ? 'last' : null)
  );
  if (!targetCellIndices.length) {
    throw new Error('未解析到可执行的 cell 索引');
  }

  const executions = [];
  for (const cellIndex of targetCellIndices) {
    const cell = notebookContent.cells[cellIndex];
    if (!cell || cell.cell_type !== 'code') {
      continue;
    }

    const execution = await client.executeCode({
      kernelId,
      code: Array.isArray(cell.source) ? cell.source.join('') : String(cell.source || ''),
      timeoutMs
    });

    cell.execution_count = execution.executionCount;
    cell.outputs = execution.outputs;
    executions.push({
      cellIndex,
      source: cell.source,
      ...summarizeExecution(execution)
    });
  }

  await client.saveNotebook(notebookContent);
  const notebookMetadata = await client.getNotebookMetadata();

  const notebookSnapshotPath = client.writeArtifact('joinquant-notebook', notebookContent, 'ipynb');
  const resultPayload = {
    capturedAt: new Date().toISOString(),
    notebookUrl: client.directNotebookUrl,
    notebookPath: client.notebookPath,
    kernelId,
    sessionId: session.id,
    appendedCellIndex,
    mode,
    targetCellIndices,
    notebookMetadata,
    executions
  };
  const resultFile = client.writeArtifact('joinquant-notebook-result', resultPayload, 'json');

  return {
    resultFile,
    notebookSnapshotPath,
    notebookUrl: client.directNotebookUrl,
    notebookPath: client.notebookPath,
    mode,
    appendedCellIndex,
    targetCellIndices,
    executions,
    session
  };
}

async function main() {
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
}

main().catch(error => {
  console.error(error.stack || error.message);
  process.exit(1);
});

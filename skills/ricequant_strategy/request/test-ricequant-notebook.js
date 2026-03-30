#!/usr/bin/env node
import { fileURLToPath } from 'node:url';
import { RiceQuantNotebookClient, createCodeCell } from './ricequant-notebook-client.js';
import { ensureRiceQuantNotebookSession } from './ensure-ricequant-notebook-session.js';

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

function getCellSourceText(cell) {
  if (!cell) return '';
  return Array.isArray(cell.source) ? cell.source.join('') : String(cell.source || '');
}

function findMarkerCellIndices(notebookContent, marker) {
  if (!marker) return [];
  return notebookContent.cells
    .map((cell, index) => ({ cell, index }))
    .filter(item => item.cell?.cell_type === 'code')
    .filter(item => getCellSourceText(item.cell).includes(marker))
    .map(item => item.index);
}

function upsertMarkedCell(notebookContent, marker, cellSource, appendCell) {
  if (!marker) {
    if (!appendCell) {
      return { targetCellIndex: null, appendedCellIndex: null };
    }
    notebookContent.cells.push(createCodeCell(cellSource));
    return {
      targetCellIndex: notebookContent.cells.length - 1,
      appendedCellIndex: notebookContent.cells.length - 1
    };
  }

  const matchedIndices = findMarkerCellIndices(notebookContent, marker);
  matchedIndices.slice(1).reverse().forEach(index => {
    notebookContent.cells.splice(index, 1);
  });

  const primaryIndex = matchedIndices[0];
  if (Number.isInteger(primaryIndex)) {
    notebookContent.cells[primaryIndex] = createCodeCell(cellSource);
    return { targetCellIndex: primaryIndex, appendedCellIndex: null };
  }

  if (!appendCell) {
    return { targetCellIndex: null, appendedCellIndex: null };
  }

  notebookContent.cells.push(createCodeCell(cellSource));
  return {
    targetCellIndex: notebookContent.cells.length - 1,
    appendedCellIndex: notebookContent.cells.length - 1
  };
}

function parseCellIndices(input, notebookContent) {
  if (!input || input === 'last') {
    return [notebookContent.cells.length - 1];
  }
  return String(input)
    .split(',')
    .map(item => item.trim())
    .map(item => (item === 'last' ? notebookContent.cells.length - 1 : Number(item)))
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
  await ensureRiceQuantNotebookSession({
    sessionFile: options.sessionFile,
    notebookUrl: options.notebookUrl,
    outputRoot: options.outputRoot
  });

  const client = new RiceQuantNotebookClient(options);
  const mode = options.mode === 'all' ? 'all' : 'partial';
  const appendCell = options.appendCell !== false;
  const cellSource = normalizeCellSource(options.cellSource);
  const timeoutMs = Number(options.timeoutMs || 30000);
  const createNew = options.createNew === true || options['create-new'] === true;
  const cleanup = options.cleanup === true;

  let newNotebookPath = null;
  let newNotebookCreated = false;

  if (createNew) {
    newNotebookPath = client.generateUniqueNotebookName(options.notebookBaseName || 'strategy_run');
    console.log(`Creating new notebook: ${newNotebookPath}`);
    
    try {
      const createResult = await client.createNotebook({
        notebookPath: newNotebookPath,
        kernelName: options.kernelName || 'python3'
      });
      newNotebookCreated = true;
      console.log(`New notebook created: ${createResult.notebookUrl}`);
      
      client.notebookPath = newNotebookPath;
      client.directNotebookUrl = createResult.notebookUrl;
    } catch (error) {
      console.error(`Failed to create new notebook: ${error.message}`);
      console.log('Falling back to existing notebook...');
    }
  }

  const notebookModel = await client.getNotebookModel();
  const notebookContent = notebookModel.content;
  if (!notebookContent?.cells) {
    throw new Error('未获取到 notebook content.cells');
  }

  const upsertResult = upsertMarkedCell(
    notebookContent,
    options.cellMarker,
    cellSource,
    appendCell
  );
  const appendedCellIndex = upsertResult.appendedCellIndex;
  const managedCellIndex = upsertResult.targetCellIndex;
  if (Number.isInteger(managedCellIndex)) {
    await client.saveNotebook(notebookContent);
  }

  const session = await client.ensureSession({ kernelName: options.kernelName || 'python3' });
  const kernelId = session?.kernel?.id;
  if (!kernelId) {
    throw new Error('未能创建 kernel session');
  }

  const defaultCellIndex = options.cellIndex
    || (Number.isInteger(managedCellIndex) ? String(managedCellIndex) : null)
    || (appendCell ? 'last' : null);
  const targetCellIndices = resolveRunCellIndices(
    mode,
    notebookContent,
    defaultCellIndex
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

  const notebookSnapshotPath = client.writeArtifact('ricequant-notebook', notebookContent, 'ipynb');
  const resultPayload = {
    capturedAt: new Date().toISOString(),
    notebookUrl: client.directNotebookUrl,
    notebookPath: client.notebookPath,
    kernelId,
    sessionId: session.id,
    appendedCellIndex,
    managedCellIndex,
    mode,
    targetCellIndices,
    notebookMetadata,
    executions,
    newNotebookCreated,
    cleanup
  };
  const resultFile = client.writeArtifact('ricequant-notebook-result', resultPayload, 'json');

  let cleanupResult = null;
  if (cleanup && newNotebookCreated) {
    console.log(`Cleaning up notebook: ${newNotebookPath}`);
    cleanupResult = await client.deleteNotebook({ notebookPath: newNotebookPath });
    if (cleanupResult.success) {
      console.log('Notebook cleaned up successfully');
    } else {
      console.error(`Failed to cleanup notebook: ${cleanupResult.error}`);
    }
  }

  return {
    resultFile,
    notebookSnapshotPath,
    notebookUrl: client.directNotebookUrl,
    notebookPath: client.notebookPath,
    mode,
    appendedCellIndex,
    managedCellIndex,
    targetCellIndices,
    executions,
    session,
    newNotebookCreated,
    cleanupResult
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
    cellMarker: args['cell-marker'],
    timeoutMs: args['timeout-ms'],
    kernelName: args['kernel-name'],
    appendCell: args['append-cell'] === 'false' ? false : true
  });

  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main().catch(error => {
    console.error(error.stack || error.message);
    process.exit(1);
  });
}
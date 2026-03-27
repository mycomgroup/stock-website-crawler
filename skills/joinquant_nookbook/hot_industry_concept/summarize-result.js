#!/usr/bin/env node
import fs from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUTPUT_ROOT = resolve(__dirname, 'output');
const RESULT_FILE_PATTERN = /^joinquant-notebook-result-(\d+)\.json$/;
const GENERIC_CONCEPTS = new Set([
  '龙头股',
  '双百企业',
  '福建',
  '股权转让',
  '昨日涨停',
  '昨日涨停_含一字'
]);

function stripAnsi(text = '') {
  return String(text).replace(/\u001b\[[0-9;]*m/g, '');
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function writeJson(filePath, data) {
  fs.writeFileSync(filePath, `${JSON.stringify(data, null, 2)}\n`, 'utf8');
}

function getSourceText(execution = {}) {
  return Array.isArray(execution.source) ? execution.source.join('') : String(execution.source || '');
}

function collectTextOutput(execution = {}) {
  if (execution.textOutput) {
    return stripAnsi(execution.textOutput);
  }

  const outputs = Array.isArray(execution.outputs) ? execution.outputs : [];
  return stripAnsi(outputs.map(output => {
    if (!output) return '';
    if (output.output_type === 'stream') {
      return typeof output.text === 'string' ? output.text : String(output.text || '');
    }
    if (output.output_type === 'error') {
      return `${output.ename || 'Error'}: ${output.evalue || ''}`.trim();
    }
    if (output.data?.['text/plain']) {
      return Array.isArray(output.data['text/plain'])
        ? output.data['text/plain'].join('')
        : String(output.data['text/plain']);
    }
    return '';
  }).join(''));
}

function listResultFiles(outputRoot = OUTPUT_ROOT) {
  return fs.readdirSync(outputRoot)
    .filter(name => RESULT_FILE_PATTERN.test(name))
    .map(name => ({
      name,
      timestamp: Number(name.match(RESULT_FILE_PATTERN)?.[1] || 0),
      filePath: resolve(outputRoot, name)
    }))
    .sort((left, right) => right.timestamp - left.timestamp);
}

function resolveResultFile(inputPath) {
  if (inputPath) {
    return resolve(process.cwd(), inputPath);
  }

  const latest = listResultFiles()[0];
  if (!latest) {
    throw new Error(`未在 ${OUTPUT_ROOT} 找到 notebook 结果文件`);
  }
  return latest.filePath;
}

function findExecution(executions, predicate) {
  for (const execution of executions) {
    const source = getSourceText(execution);
    const text = collectTextOutput(execution);
    if (predicate({ execution, source, text })) {
      return { execution, source, text };
    }
  }
  return null;
}

function extractSingleMatch(text, regex) {
  const match = String(text || '').match(regex);
  return match || null;
}

function parseDateInfo(executions) {
  const combinedText = executions.map(collectTextOutput).join('\n');
  const match = extractSingleMatch(
    combinedText,
    /1、竞价日期\s+(\d{4}-\d{2}-\d{2})\s+2、K线最后一个交易日\s+(\d{4}-\d{2}-\d{2})\s+3、观察(\d+)天的数据/s
  );

  return {
    auctionDate: match?.[1] || null,
    endDate: match?.[2] || null,
    watchDays: match ? Number(match[3]) : null
  };
}

function parseCombinedInfo(label) {
  const match = String(label || '').match(/^(.*?)\s*\((\d+)只,\s*([\d.]+)%攻击\)$/);
  if (!match) {
    return {
      category: String(label || '').trim(),
      stockCount: null,
      pctOfAttack: null,
      combinedInfo: String(label || '').trim()
    };
  }

  return {
    category: match[1].trim(),
    stockCount: Number(match[2]),
    pctOfAttack: Number(match[3]),
    combinedInfo: String(label || '').trim()
  };
}

function parseTrailingRankTable(text, topN = 5) {
  const lines = stripAnsi(text)
    .split(/\r?\n/)
    .map(line => line.replace(/\s+$/g, ''))
    .filter(Boolean);

  const headerLine = lines.find(line => /\d{4}-\d{2}-\d{2}/.test(line));
  const lastTradeDate = headerLine?.match(/(\d{4}-\d{2}-\d{2})\s*$/)?.[1] || null;
  const entries = [];

  for (const line of lines) {
    if (!/^\s*\d+\s+/.test(line)) {
      continue;
    }

    const parts = line.trim().split(/\s{2,}/).filter(Boolean);
    if (parts.length < 2) {
      continue;
    }

    const parsed = parseCombinedInfo(parts[parts.length - 1]);
    entries.push({
      rank: entries.length + 1,
      date: lastTradeDate,
      ...parsed
    });

    if (entries.length >= topN) {
      break;
    }
  }

  return {
    date: lastTradeDate,
    entries
  };
}

function parseConceptTable(text, topN = 10) {
  const rows = [];
  const lines = stripAnsi(text)
    .split(/\r?\n/)
    .map(line => line.trimEnd())
    .filter(Boolean);

  for (const line of lines) {
    const match = line.match(/^\s*\d+\s+(\S+)\s+(\d{4}-\d{2}-\d{2})\s+([\d.]+)\s+(\d+)\s+([\d.]+)\s+(.+)$/);
    if (!match) {
      continue;
    }

    rows.push({
      rank: rows.length + 1,
      category: match[1],
      date: match[2],
      score: Number(match[3]),
      stockCount: Number(match[4]),
      pctOfAttack: Number(match[5]),
      combinedInfo: match[6].trim()
    });

    if (rows.length >= topN) {
      break;
    }
  }

  return rows;
}

function parseHotSelection(executions) {
  const combinedText = executions.map(collectTextOutput).join('\n');
  const hottestIndustry = extractSingleMatch(combinedText, /最后一天最热行业是:\s*([^,\n]+),\s*成分股为:\s*(\d+)只/);
  const hottestConceptByScore = extractSingleMatch(combinedText, /最后一天按涨停攻击家数最热概念是:\s*([^,\n]+),\s*成分股为:\s*(\d+)只/);
  const hottestConceptByPct = extractSingleMatch(combinedText, /最后一天按涨停攻击比例最热概念是:\s*([^,\n]+),\s*成分股为:\s*(\d+)只/);
  const unionOfConcepts = extractSingleMatch(combinedText, /两个维度的最热概念成分股合并起来:\s*成分股为:\s*(\d+)只/);
  const unionOfAllHotStocks = extractSingleMatch(combinedText, /最后一天 热点行业 和 热点概念 成分股的并集为:\s*(\d+)只/);

  return {
    industry: hottestIndustry
      ? { category: hottestIndustry[1].trim(), stockCount: Number(hottestIndustry[2]) }
      : null,
    conceptByScore: hottestConceptByScore
      ? { category: hottestConceptByScore[1].trim(), stockCount: Number(hottestConceptByScore[2]) }
      : null,
    conceptByPct: hottestConceptByPct
      ? { category: hottestConceptByPct[1].trim(), stockCount: Number(hottestConceptByPct[2]) }
      : null,
    conceptUnionStockCount: unionOfConcepts ? Number(unionOfConcepts[1]) : null,
    totalUnionStockCount: unionOfAllHotStocks ? Number(unionOfAllHotStocks[1]) : null
  };
}

function parseRotationHighlights(text, maxDays = 5) {
  const normalizedText = stripAnsi(text)
    .replace(/<Figure size[^>]+>/g, '\n')
    .replace(/(日期:\s*\d{4}-\d{2}-\d{2})/g, '\n$1');

  const lines = normalizedText
    .split(/\r?\n/)
    .map(line => line.trim())
    .filter(Boolean);

  const dayMap = new Map();
  let currentDate = null;

  for (const line of lines) {
    const dateMatch = line.match(/^日期:\s*(\d{4}-\d{2}-\d{2})$/);
    if (dateMatch) {
      currentDate = dateMatch[1];
      if (!dayMap.has(currentDate)) {
        dayMap.set(currentDate, { date: currentDate, items: [] });
      }
      continue;
    }

    const itemMatch = line.match(/^(攻击家数最多的概念|攻击比例最高的概念|攻击比例大于5%的概念):\s*(.+?)，(攻击家数|攻击比例):\s*([\d.-]+)/);
    if (!itemMatch || !currentDate) {
      continue;
    }

    dayMap.get(currentDate).items.push({
      type: itemMatch[1],
      category: itemMatch[2],
      metricLabel: itemMatch[3],
      value: Number(itemMatch[4])
    });
  }

  return Array.from(dayMap.values())
    .sort((left, right) => right.date.localeCompare(left.date))
    .slice(0, maxDays)
    .map(day => ({
      ...day,
      items: day.items.slice(0, 6)
    }));
}

function extractSection(text, startMarker, endMarker) {
  const startIndex = text.indexOf(startMarker);
  if (startIndex === -1) {
    return '';
  }

  const contentStart = startIndex + startMarker.length;
  const tail = text.slice(contentStart);
  if (!endMarker) {
    return tail;
  }

  const endIndex = tail.indexOf(endMarker);
  return endIndex === -1 ? tail : tail.slice(0, endIndex);
}

function parseMoneyFlowRows(sectionText, topN = 5) {
  const rows = [];
  const lines = stripAnsi(sectionText)
    .split(/\r?\n/)
    .map(line => line.trimEnd())
    .filter(Boolean);

  for (const line of lines) {
    if (!line.includes('成分股)')) {
      continue;
    }

    const parts = line.trim().split(/\s{2,}/).filter(Boolean);
    if (parts.length < 2) {
      continue;
    }

    const label = parts[0];
    const value = Number(parts[parts.length - 1]);
    if (Number.isNaN(value)) {
      continue;
    }

    const match = label.match(/^(.*?)\s*\((\d+)\s*成分股\)$/);
    rows.push({
      rank: rows.length + 1,
      category: match?.[1]?.trim() || label,
      stockCount: match ? Number(match[2]) : null,
      value
    });

    if (rows.length >= topN) {
      break;
    }
  }

  return rows;
}

function parseMoneyFlow(text) {
  const cleanedText = stripAnsi(text);
  const inflowMarker = '最后一天 【大单资金】流入最多的 二级行业 时间序列数据表格：';
  const outflowMarker = '最后一天 【大单资金】流出最多的 二级行业 时间序列数据表格：';

  const inflowSection = extractSection(cleanedText, inflowMarker, outflowMarker);
  const outflowSection = extractSection(cleanedText, outflowMarker);

  return {
    inflow: parseMoneyFlowRows(inflowSection, 5),
    outflow: parseMoneyFlowRows(outflowSection, 5)
  };
}

function buildWarnings(summary) {
  const warnings = [];
  const genericConcepts = summary.latestConcepts
    .filter(item => GENERIC_CONCEPTS.has(item.category))
    .map(item => item.category);

  if (genericConcepts.length) {
    warnings.push(`概念榜包含泛概念：${Array.from(new Set(genericConcepts)).join('、')}，更适合做观察，不宜直接当交易主线。`);
  }

  const hotIndustry = summary.hotSelection.industry?.category || '';
  const powerOutflow = summary.moneyFlow.outflow.find(item => /电力/.test(item.category));
  if (/火电|电力/.test(hotIndustry) && powerOutflow) {
    warnings.push(`热度最强的是 ${hotIndustry}，但资金流里 ${powerOutflow.category} 为净流出，说明板块可能处于分歧阶段。`);
  }

  return warnings;
}

function formatPercent(value) {
  if (value == null || Number.isNaN(value)) return '-';
  return `${Number(value).toFixed(2).replace(/\.00$/, '').replace(/(\.\d)0$/, '$1')}%`;
}

function formatNumber(value) {
  if (value == null || Number.isNaN(value)) return '-';
  return new Intl.NumberFormat('zh-CN', { maximumFractionDigits: 2 }).format(value);
}

export function summarizeHotIndustryConceptResult(resultFile, options = {}) {
  const resolvedResultFile = resolveResultFile(resultFile);
  const payload = readJson(resolvedResultFile);
  const executions = Array.isArray(payload.executions) ? payload.executions : [];

  if (!executions.length) {
    throw new Error(`结果文件不包含 executions：${resolvedResultFile}`);
  }

  const industryExecution = findExecution(
    executions,
    ({ source }) => source.includes('一级行业打分。更确切地说')
  );
  const conceptExecution = findExecution(
    executions,
    ({ source }) => source.includes('最后一天的热点概念，单独看看')
  );
  const rotationExecution = findExecution(
    executions,
    ({ source, text }) => source.includes('find_lead_stocks_in_recent_hot_concepts') || text.includes('攻击家数最多的概念:')
  );
  const moneyFlowExecution = findExecution(
    executions,
    ({ source, text }) => source.includes('最后一天 【大单资金】流入最多的 二级行业') || text.includes('最后一天 【大单资金】流入最多的 二级行业')
  );

  const dateInfo = parseDateInfo(executions);
  const latestIndustry = industryExecution ? parseTrailingRankTable(industryExecution.text, 5) : { date: dateInfo.endDate, entries: [] };
  const latestConcepts = conceptExecution ? parseConceptTable(conceptExecution.text, 10) : [];
  const actionableConcepts = latestConcepts.filter(item => !GENERIC_CONCEPTS.has(item.category)).slice(0, 5);
  const hotSelection = parseHotSelection(executions);
  const rotationHighlights = rotationExecution ? parseRotationHighlights(rotationExecution.text, 5) : [];
  const moneyFlow = moneyFlowExecution ? parseMoneyFlow(moneyFlowExecution.text) : { inflow: [], outflow: [] };

  const summary = {
    resultFile: resolvedResultFile,
    sourceNotebookUrl: payload.notebookUrl || null,
    capturedAt: payload.capturedAt || null,
    summaryGeneratedAt: new Date().toISOString(),
    analysisWindow: dateInfo,
    latestIndustry,
    latestConcepts,
    actionableConcepts,
    hotSelection,
    rotationHighlights,
    moneyFlow,
    warnings: []
  };

  summary.warnings = buildWarnings(summary);

  if (options.writeSummary !== false) {
    const summaryFile = resolve(dirname(resolvedResultFile), 'hot-industry-concept-summary-latest.json');
    writeJson(summaryFile, summary);
    summary.summaryFile = summaryFile;
  }

  return summary;
}

export function formatHotIndustryConceptSummary(summary) {
  const lines = [];
  const window = summary.analysisWindow || {};

  lines.push('hot_industry_concept 本地摘要');
  lines.push(`结果文件: ${summary.resultFile}`);
  if (summary.summaryFile) {
    lines.push(`摘要文件: ${summary.summaryFile}`);
  }
  lines.push(`竞价日期: ${window.auctionDate || '-'}`);
  lines.push(`K线截止: ${window.endDate || '-'}`);
  lines.push(`观察窗口: ${window.watchDays || '-'} 天`);
  lines.push('');

  lines.push('最新行业 Top5:');
  for (const item of summary.latestIndustry.entries || []) {
    lines.push(`- ${item.rank}. ${item.category} (${item.stockCount || '-'}只, ${formatPercent(item.pctOfAttack)}攻击)`);
  }
  if (!summary.latestIndustry.entries?.length) {
    lines.push('- 无');
  }
  lines.push('');

  lines.push('最新概念 Top5:');
  for (const item of (summary.latestConcepts || []).slice(0, 5)) {
    lines.push(`- ${item.rank}. ${item.category} (${item.stockCount}只, ${formatPercent(item.pctOfAttack)}攻击, score=${formatNumber(item.score)})`);
  }
  if (!summary.latestConcepts?.length) {
    lines.push('- 无');
  }
  lines.push('');

  lines.push('更可交易的概念 Top5（已过滤泛概念）:');
  for (const [index, item] of (summary.actionableConcepts || []).entries()) {
    lines.push(`- ${index + 1}. ${item.category} (${item.stockCount}只, ${formatPercent(item.pctOfAttack)}攻击)`);
  }
  if (!summary.actionableConcepts?.length) {
    lines.push('- 无');
  }
  lines.push('');

  lines.push('热点归纳:');
  lines.push(`- 最热行业: ${summary.hotSelection.industry?.category || '-'} (${summary.hotSelection.industry?.stockCount || '-'}只)`);
  lines.push(`- 攻击家数最热概念: ${summary.hotSelection.conceptByScore?.category || '-'} (${summary.hotSelection.conceptByScore?.stockCount || '-'}只)`);
  lines.push(`- 攻击比例最热概念: ${summary.hotSelection.conceptByPct?.category || '-'} (${summary.hotSelection.conceptByPct?.stockCount || '-'}只)`);
  lines.push(`- 热点概念并集: ${summary.hotSelection.conceptUnionStockCount || '-'}只`);
  lines.push(`- 行业+概念并集: ${summary.hotSelection.totalUnionStockCount || '-'}只`);
  lines.push('');

  lines.push('近 5 日轮动:');
  for (const day of summary.rotationHighlights || []) {
    const tags = day.items.map(item => `${item.type}=${item.category}(${formatNumber(item.value)})`);
    lines.push(`- ${day.date}: ${tags.join('；')}`);
  }
  if (!summary.rotationHighlights?.length) {
    lines.push('- 无');
  }
  lines.push('');

  lines.push('资金流（最后一天二级行业）:');
  lines.push(`- 流入: ${(summary.moneyFlow.inflow || []).map(item => `${item.category}(${formatNumber(item.value)})`).join('，') || '无'}`);
  lines.push(`- 流出: ${(summary.moneyFlow.outflow || []).map(item => `${item.category}(${formatNumber(item.value)})`).join('，') || '无'}`);

  if (summary.warnings?.length) {
    lines.push('');
    lines.push('提示:');
    for (const warning of summary.warnings) {
      lines.push(`- ${warning}`);
    }
  }

  return lines.join('\n');
}

export function main(argv = process.argv.slice(2)) {
  const summary = summarizeHotIndustryConceptResult(argv[0], { writeSummary: true });
  console.log(formatHotIndustryConceptSummary(summary));
  return summary;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  try {
    main();
  } catch (error) {
    console.error('摘要失败:', error.stack || error.message);
    process.exit(1);
  }
}

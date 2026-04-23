#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const STRATEGIES = [
  {
    name: 'A_原版_Release_V1',
    file: path.join(__dirname, '../../strategies/rfscore_offensive/rfscore7_pb10_release_v1.py'),
    description: '原版：RFScore7 + PB筛选 + 市场状态风控 + 行业分散',
  },
  {
    name: 'B_纯PB低估值',
    file: path.join(__dirname, 'attribution_b_pure_pb.py'),
    description: '剥离RFScore7，仅保留PB最低10%选股',
  },
  {
    name: 'C_纯RFScore7',
    file: path.join(__dirname, 'attribution_c_pure_rfscore.py'),
    description: '剥离PB筛选，仅按RFScore7打分排序',
  },
  {
    name: 'D_无市场状态风控',
    file: path.join(__dirname, 'attribution_d_no_market_state.py'),
    description: '移除市场状态判断，始终满仓',
  },
];

function analyzeCode(filePath) {
  const code = fs.readFileSync(filePath, 'utf8');
  const lines = code.split('\n');

  return {
    totalLines: lines.length,
    hasRFScore: code.includes('class RFScore'),
    hasPBFilter: code.includes('pb_group'),
    hasMarketState: code.includes('calc_market_state') && code.includes('get_target_hold_num'),
    hasIndustryCap: code.includes('industry_cap'),
    holdNumNormal: extractParam(code, 'hold_num_normal') || extractParam(code, 'hold_num_fixed'),
    breadthStop: extractParam(code, 'breadth_stop'),
    primaryPBGroup: extractParam(code, 'primary_pb_group'),
  };
}

function extractParam(code, paramName) {
  const regex = new RegExp(`g\\.${paramName}\\s*=\\s*(.+?)(?:\\s|$)`);
  const match = code.match(regex);
  return match ? match[1].trim() : null;
}

function main() {
  console.log('RFScore7 因子剥离验证 - 代码结构对比\n');
  console.log('='.repeat(80));

  const analysis = {};

  for (const strategy of STRATEGIES) {
    if (!fs.existsSync(strategy.file)) {
      console.log(`⚠ 文件不存在: ${strategy.file}`);
      continue;
    }

    analysis[strategy.name] = analyzeCode(strategy.file);
  }

  // 打印对比表格
  console.log('\n代码结构对比:\n');
  console.log('| 特征 | A_原版 | B_纯PB | C_纯RFScore | D_无风控 |');
  console.log('|------|--------|--------|-------------|---------|');

  const features = [
    ['RFScore因子', 'hasRFScore'],
    ['PB分组筛选', 'hasPBFilter'],
    ['市场状态风控', 'hasMarketState'],
    ['行业分散控制', 'hasIndustryCap'],
    ['正常持仓数', 'holdNumNormal'],
    ['清仓阈值', 'breadthStop'],
    ['PB主分组', 'primaryPBGroup'],
  ];

  for (const [label, key] of features) {
    const row = [label];
    for (const name of ['A_原版_Release_V1', 'B_纯PB低估值', 'C_纯RFScore7', 'D_无市场状态风控']) {
      const val = analysis[name]?.[key];
      if (val === true) row.push('✓');
      else if (val === false) row.push('✗');
      else if (val !== null && val !== undefined) row.push(val);
      else row.push('-');
    }
    console.log(`| ${row.join(' | ')} |`);
  }

  console.log('\n' + '='.repeat(80));
  console.log('\n验证逻辑说明:\n');
  console.log('1. A vs B: 如果B收益接近A → PB是核心因子，RFScore7贡献有限');
  console.log('2. A vs C: 如果C收益远低于A → PB筛选是必要的风控/增强层');
  console.log('3. A vs D: 如果D回撤显著大于A → 市场状态风控有效');
  console.log('\n预期结果:');
  console.log('  - 如果 "PB低估值" 是核心收益来源: B ≈ A, C << A');
  console.log('  - 如果 "RFScore7" 有真实贡献: A >> B, C 也有一定收益');
  console.log('  - 如果 "市场风控" 有效: A夏普 > D夏普, A回撤 < D回撤');
}

main();

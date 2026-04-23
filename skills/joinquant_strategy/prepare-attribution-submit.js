#!/usr/bin/env node
/**
 * RFScore7 收益归因验证 - 提交脚本
 * 只提交用户创建的归因测试文件，不改动他人文件
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 只提交用户创建的归因测试文件
const STRATEGIES_TO_SUBMIT = [
  {
    name: 'Attribution_C_Pure_RFScore',
    file: path.join(__dirname, 'attribution_c_pure_rfscore.py'),
    desc: '纯RFScore7质量因子（剥离PB过滤）',
    purpose: '验证RFScore7单独贡献'
  },
  {
    name: 'Attribution_D_No_Risk_Control',
    file: path.join(__dirname, 'attribution_d_no_risk_control.py'),
    desc: '无动态风控（始终满仓20只）',
    purpose: '验证动态风控贡献'
  },
  {
    name: 'Attribution_E_PB20_Loose',
    file: path.join(__dirname, 'attribution_e_pb20_loose.py'),
    desc: 'PB20%宽松版（vs PB10%严格版）',
    purpose: '验证PB严格度是否过拟合'
  }
];

const BACKTEST_CONFIG = {
  startTime: '2020-01-01',
  endTime: '2025-12-31',
  baseCapital: '1000000',
  frequency: 'day'
};

function printHeader() {
  console.log('='.repeat(70));
  console.log('RFScore7 收益归因验证 - 批量提交');
  console.log('='.repeat(70));
  console.log('\n提交策略:');
  STRATEGIES_TO_SUBMIT.forEach((s, i) => {
    console.log(`\n  ${i + 1}. ${s.name}`);
    console.log(`     文件: ${path.basename(s.file)}`);
    console.log(`     描述: ${s.desc}`);
    console.log(`     目的: ${s.purpose}`);
  });
  console.log('\n' + '='.repeat(70));
}

function validateFiles() {
  console.log('\n验证文件...');
  let allValid = true;
  
  for (const strategy of STRATEGIES_TO_SUBMIT) {
    if (!fs.existsSync(strategy.file)) {
      console.error(`  ✗ 缺失: ${strategy.file}`);
      allValid = false;
    } else {
      const stats = fs.statSync(strategy.file);
      console.log(`  ✓ ${path.basename(strategy.file)} (${(stats.size / 1024).toFixed(1)} KB)`);
    }
  }
  
  return allValid;
}

function generateManualInstructions() {
  console.log('\n' + '='.repeat(70));
  console.log('手动提交指南');
  console.log('='.repeat(70));
  
  console.log('\n请在聚宽平台手动创建以下策略:\n');
  
  STRATEGIES_TO_SUBMIT.forEach((s, i) => {
    console.log(`${i + 1}. 策略名称: RFScore_Attr_${s.name}`);
    console.log(`   文件路径: ${s.file}`);
    console.log(`   复制代码后粘贴到聚宽策略编辑器`);
    console.log(`   回测设置:`);
    console.log(`     - 开始时间: ${BACKTEST_CONFIG.startTime}`);
    console.log(`     - 结束时间: ${BACKTEST_CONFIG.endTime}`);
    console.log(`     - 初始资金: ${BACKTEST_CONFIG.baseCapital}`);
    console.log(`     - 回测频率: 每天`);
    console.log('');
  });
  
  console.log('对比基准策略:');
  console.log('  - v1_rfscore7_offensive.py (原始基准)');
  console.log('  - rfscore7_pb10_final_v2.py (PB10%严格版)');
  console.log('');
}

function main() {
  printHeader();
  
  // 验证文件存在
  if (!validateFiles()) {
    console.error('\n错误: 部分文件缺失，请检查文件路径');
    process.exit(1);
  }
  
  // 输出手动提交指南
  generateManualInstructions();
  
  console.log('='.repeat(70));
  console.log('文件准备完成！');
  console.log('='.repeat(70));
  console.log('\n归因验证对比表:');
  console.log('-'.repeat(70));
  console.log('对比组                | 验证问题');
  console.log('-'.repeat(70));
  console.log('基准 vs 纯RFScore     | RFScore7单独贡献多少？');
  console.log('基准 vs 无风控        | 动态风控贡献多少？');
  console.log('PB10% vs PB20%        | PB严格度是否过拟合？');
  console.log('-'.repeat(70));
}

main();

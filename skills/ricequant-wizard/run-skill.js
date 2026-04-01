#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { WizardClient } from './request/wizard-client.js';
import { validateWizardConfig, normalizeConfig } from './lib/config-validator.js';
import { EXAMPLES_DIR, DATA_DIR } from './paths.js';
import { getAllFactorsFlat, OPERATORS, TEMPLATES, ST_OPTIONS, DEFAULT_UNIVERSES } from './lib/factor-definitions.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function showHelp() {
  console.log(`
RiceQuant 向导式策略工具

用法：
  node run-skill.js <command> [options]

命令：
  --create --config <file>     创建向导式策略
  --update --id <id> --config <file>   更新策略配置
  --run --id <id> [options]    运行回测
  --report --id <backtestId>   获取回测报告
  --list [--type wizard|code]  列出策略
  --delete --id <id>           删除策略
  --validate --config <file>   验证配置文件
  --factors                    列出所有可用因子
  --help                       显示帮助

回测选项：
  --start <date>               开始日期 (默认: 2020-01-01)
  --end <date>                 结束日期 (默认: 2025-03-28)
  --capital <number>           初始资金 (默认: 100000)
  --benchmark <code>           基准 (默认: 000300.XSHG)
  --wait                       等待回测完成
  --full                       获取完整报告

示例：
  # 创建策略
  node run-skill.js --create --config examples/value-investing.json

  # 运行回测并等待结果
  node run-skill.js --run --id 123456 --wait --full

  # 列出所有向导式策略
  node run-skill.js --list --type wizard

  # 验证配置
  node run-skill.js --validate --config examples/value-investing.json
`);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (!arg.startsWith('--')) continue;
    const key = arg.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i++;
  }
  return args;
}

function loadConfig(configPath) {
  if (!fs.existsSync(configPath)) {
    throw new Error(`配置文件不存在: ${configPath}`);
  }
  return JSON.parse(fs.readFileSync(configPath, 'utf8'));
}

async function createStrategy(args) {
  const client = new WizardClient();
  const config = loadConfig(args.config);
  
  const validation = validateWizardConfig(config);
  if (!validation.valid) {
    console.error('配置验证失败:');
    validation.errors.forEach(e => console.error(`  - ${e}`));
    process.exit(1);
  }
  
  if (validation.warnings.length > 0) {
    console.log('配置警告:');
    validation.warnings.forEach(w => console.log(`  - ${w}`));
  }
  
  const normalized = normalizeConfig(config);
  
  console.log(`创建向导式策略: ${normalized.name}`);
  const result = await client.createWizardStrategy(normalized);
  
  console.log(`\n策略创建成功!`);
  console.log(`  ID: ${result.strategyId}`);
  console.log(`  名称: ${result.title}`);
  
  if (args.run) {
    console.log(`\n启动回测...`);
    const backtest = await client.runBacktest(result.strategyId, normalized.backtest);
    console.log(`  回测ID: ${backtest.backtestId}`);
    
    if (args.wait) {
      console.log('\n等待回测完成...');
      const waitResult = await client.waitForBacktest(backtest.backtestId);
      
      if (waitResult.status === 'finished') {
        console.log('回测完成!');
        
        if (args.full) {
          const report = await client.getFullReport(backtest.backtestId);
          const reportPath = client.saveReport(backtest.backtestId, report);
          console.log(`\n完整报告已保存: ${reportPath}`);
          
          if (report.risk) {
            console.log('\n风险指标:');
            console.log(`  Alpha: ${(report.risk.alpha * 100).toFixed(2)}%`);
            console.log(`  Beta: ${report.risk.beta?.toFixed(2) || 'N/A'}`);
            console.log(`  Sharpe: ${report.risk.sharpe?.toFixed(2) || 'N/A'}`);
            console.log(`  Max Drawdown: ${(report.risk.max_drawdown * 100).toFixed(2)}%`);
          }
        }
      } else if (waitResult.status === 'error') {
        console.error('回测出错:', waitResult.exception);
      } else {
        console.log('回测超时，请稍后查询结果');
      }
    }
  }
  
  return result;
}

async function updateStrategy(args) {
  const client = new WizardClient();
  const config = loadConfig(args.config);
  
  const validation = validateWizardConfig(config);
  if (!validation.valid) {
    console.error('配置验证失败:');
    validation.errors.forEach(e => console.error(`  - ${e}`));
    process.exit(1);
  }
  
  const normalized = normalizeConfig(config);
  
  console.log(`更新策略 ${args.id}...`);
  await client.updateWizardStrategy(args.id, normalized);
  console.log('更新成功');
}

async function runBacktest(args) {
  const client = new WizardClient();
  
  const backtestConfig = {
    start: args.start || '2020-01-01',
    end: args.end || '2025-03-28',
    capital: args.capital || '100000',
    benchmark: args.benchmark || '000300.XSHG',
    frequency: 'day'
  };
  
  console.log(`运行回测: 策略 ${args.id}`);
  console.log(`  时间: ${backtestConfig.start} ~ ${backtestConfig.end}`);
  console.log(`  资金: ${backtestConfig.capital}`);
  
  const result = await client.runBacktest(args.id, backtestConfig);
  console.log(`\n回测已启动: ${result.backtestId}`);
  
  if (args.wait) {
    console.log('等待回测完成...');
    const waitResult = await client.waitForBacktest(result.backtestId);
    
    if (waitResult.status === 'finished') {
      console.log('回测完成!');
      
      if (args.full) {
        const report = await client.getFullReport(result.backtestId);
        const reportPath = client.saveReport(result.backtestId, report);
        console.log(`\n完整报告: ${reportPath}`);
        
        if (report.risk) {
          console.log('\n风险指标:');
          console.log(`  Alpha: ${(report.risk.alpha * 100).toFixed(2)}%`);
          console.log(`  Beta: ${report.risk.beta?.toFixed(2) || 'N/A'}`);
          console.log(`  Sharpe: ${report.risk.sharpe?.toFixed(2) || 'N/A'}`);
          console.log(`  Max Drawdown: ${(report.risk.max_drawdown * 100).toFixed(2)}%`);
        }
      }
    } else if (waitResult.status === 'error') {
      console.error('回测出错:', waitResult.exception);
    } else {
      console.log('回测超时');
    }
  }
  
  return result;
}

async function getReport(args) {
  const client = new WizardClient();
  
  const report = await client.getFullReport(args.id);
  const reportPath = path.join(DATA_DIR, `report-${args.id}-${Date.now()}.json`);
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
  
  console.log(`回测报告: ${args.id}`);
  console.log(`  状态: ${report.result?.status || 'unknown'}`);
  
  if (report.risk) {
    console.log('\n风险指标:');
    console.log(`  Alpha: ${(report.risk.alpha * 100).toFixed(2)}%`);
    console.log(`  Beta: ${report.risk.beta?.toFixed(2) || 'N/A'}`);
    console.log(`  Sharpe: ${report.risk.sharpe?.toFixed(2) || 'N/A'}`);
    console.log(`  Max Drawdown: ${(report.risk.max_drawdown * 100).toFixed(2)}%`);
    console.log(`  Annual Volatility: ${(report.risk.annual_volatility * 100).toFixed(2)}%`);
  }
  
  if (report.exception) {
    console.log(`\n异常: ${report.exception}`);
  }
  
  console.log(`\n详细报告: ${reportPath}`);
}

async function listStrategies(args) {
  const client = new WizardClient();
  
  const strategies = await client.listStrategies({ type: args.type });
  
  console.log(`策略列表 (${strategies.length} 个):\n`);
  
  for (const s of strategies) {
    console.log(`  [${s.type === 'wizard' ? 'W' : 'C'}] ${s.id} - ${s.title}`);
  }
}

async function deleteStrategy(args) {
  const client = new WizardClient();
  
  console.log(`删除策略 ${args.id}...`);
  const success = await client.deleteStrategy(args.id);
  
  if (success) {
    console.log('删除成功');
  } else {
    console.log('删除失败');
  }
}

function validateConfig(args) {
  const config = loadConfig(args.config);
  const validation = validateWizardConfig(config);
  
  console.log(`配置文件: ${args.config}`);
  console.log(`验证结果: ${validation.valid ? '通过' : '失败'}`);
  
  if (validation.errors.length > 0) {
    console.log('\n错误:');
    validation.errors.forEach(e => console.log(`  - ${e}`));
  }
  
  if (validation.warnings.length > 0) {
    console.log('\n警告:');
    validation.warnings.forEach(w => console.log(`  - ${w}`));
  }
  
  if (validation.valid) {
    const normalized = normalizeConfig(config);
    console.log('\n规范化配置:');
    console.log(JSON.stringify(normalized, null, 2));
  }
}

function listFactors() {
  
  const factors = getAllFactorsFlat();
  
  console.log('可用因子:\n');
  
  const byType = {};
  for (const f of factors) {
    if (!byType[f.type]) byType[f.type] = [];
    byType[f.type].push(f);
  }
  
  for (const [type, typeFactors] of Object.entries(byType)) {
    console.log(`\n[${type}]`);
    for (const f of typeFactors.slice(0, 10)) {
      console.log(`  ${f.name} - ${f.label}`);
    }
    if (typeFactors.length > 10) {
      console.log(`  ... 共 ${typeFactors.length} 个因子`);
    }
  }
  
  console.log('\n\n操作符:');
  for (const op of OPERATORS) {
    console.log(`  ${op.name} - ${op.label}`);
  }
  
  console.log('\n\n模板:');
  for (const t of TEMPLATES) {
    console.log(`  ${t.name} - ${t.label}`);
  }
  
  console.log('\n\nST选项:');
  for (const s of ST_OPTIONS) {
    console.log(`  ${s.value} - ${s.label}`);
  }
  
  console.log('\n\n默认股票池:');
  for (const u of DEFAULT_UNIVERSES) {
    console.log(`  ${u.code} - ${u.name}`);
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  
  if (args.help || Object.keys(args).length === 0) {
    showHelp();
    process.exit(0);
  }
  
  try {
    if (args.create) {
      await createStrategy(args);
    } else if (args.update) {
      await updateStrategy(args);
    } else if (args.run) {
      await runBacktest(args);
    } else if (args.report) {
      await getReport(args);
    } else if (args.list) {
      await listStrategies(args);
    } else if (args.delete) {
      await deleteStrategy(args);
    } else if (args.validate) {
      validateConfig(args);
    } else if (args.factors) {
      listFactors();
    } else {
      console.error('未知命令，使用 --help 查看帮助');
      process.exit(1);
    }
  } catch (error) {
    console.error('执行失败:', error.message);
    process.exit(1);
  }
}

main();
#!/usr/bin/env node
/**
 * JoinQuant Data CLI
 *
 * 通过 CLI 调用 JoinQuant Notebook 执行数据获取操作。
 *
 * 使用方式:
 *   node joinquant_data_cli.js --function get_stock_daily --params '{"symbol":"000001.XSHE","count":5}'
 *   node joinquant_data_cli.js --list                          # 列出所有可用方法
 *   node joinquant_data_cli.js --test                          # 测试连接
 */

import { execSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const EXECUTOR_FILE = path.join(__dirname, 'joinquant_data_executor.py');

// ============================================================
// 可用方法列表
// ============================================================

const METHODS = {
  // 第一类：行情数据
  get_stock_daily: {
    desc: '获取单只股票的日线行情数据',
    params: {
      symbol: '股票代码',
      start_date: '开始日期 (可选)',
      end_date: '结束日期 (可选)',
      count: '获取数量 (可选)',
      adjust: '复权类型: qfq/hfq/none (可选)'
    }
  },
  get_stock_daily_batch: {
    desc: '批量获取多只股票的日线行情数据',
    params: {
      symbols: '股票代码列表',
      start_date: '开始日期 (可选)',
      end_date: '结束日期 (可选)',
      count: '获取数量 (可选)',
      adjust: '复权类型 (可选)'
    }
  },
  get_stock_minute: {
    desc: '获取单只股票的分时行情数据',
    params: {
      symbol: '股票代码',
      date: '交易日期',
      freq: '频率: 1min/5min/15min/30min/60min (可选，默认5min)'
    }
  },
  get_call_auction: {
    desc: '获取单只股票的集合竞价数据',
    params: {
      symbol: '股票代码',
      date: '交易日期'
    }
  },

  // 第二类：估值数据
  get_valuation: {
    desc: '获取单只股票的估值数据',
    params: {
      symbol: '股票代码',
      start_date: '开始日期 (可选)',
      end_date: '结束日期 (可选)'
    }
  },
  get_index_valuation: {
    desc: '获取指数的估值数据',
    params: {
      index_symbol: '指数代码',
      start_date: '开始日期 (可选)',
      end_date: '结束日期 (可选)'
    }
  },

  // 第三类：财务数据
  get_financial: {
    desc: '获取单只股票的财务报表数据',
    params: {
      symbol: '股票代码',
      table: '报表类型: income/balance/cashflow (可选)',
      period: '报告周期: quarterly/annual/ttm (可选)'
    }
  },
  get_finance_indicators: {
    desc: '获取单只股票的财务指标数据',
    params: {
      symbol: '股票代码',
      start_date: '开始日期 (可选)',
      end_date: '结束日期 (可选)'
    }
  },
  get_dividend: {
    desc: '获取单只股票的分红送转数据',
    params: {
      symbol: '股票代码'
    }
  },

  // 第四类：指数与行业
  get_index_daily: {
    desc: '获取指数的日线行情数据',
    params: {
      symbol: '指数代码',
      start_date: '开始日期 (可选)',
      end_date: '结束日期 (可选)',
      count: '获取数量 (可选)'
    }
  },
  get_index_components: {
    desc: '获取指数在指定日期的成分股列表',
    params: {
      index_symbol: '指数代码',
      date: '查询日期'
    }
  },
  get_industry_list: {
    desc: '获取行业分类列表',
    params: {
      level: '行业级别: sw_l1/sw_l2/sw_l3 (可选)'
    }
  },
  get_industry_classification: {
    desc: '获取股票的行业分类信息',
    params: {
      symbols: '股票代码列表',
      level: '行业级别 (可选)'
    }
  },

  // 第五类：宏观与情绪
  get_market_spot: {
    desc: '获取指定日期的全市场行情快照',
    params: {
      date: '交易日期'
    }
  },
  get_money_flow: {
    desc: '获取单只股票的资金流向数据',
    params: {
      symbol: '股票代码',
      start_date: '开始日期 (可选)',
      end_date: '结束日期 (可选)'
    }
  },
  get_analyst_forecast: {
    desc: '获取分析师盈利预测数据',
    params: {
      symbol: '股票代码',
      start_date: '开始日期 (可选)',
      end_date: '结束日期 (可选)'
    }
  },
  get_shareholder_data: {
    desc: '获取股东人数及户均持股数据',
    params: {
      symbol: '股票代码',
      start_date: '开始日期 (可选)',
      end_date: '结束日期 (可选)'
    }
  },

  // 第六类：辅助数据
  get_trading_calendar: {
    desc: '获取交易日日历',
    params: {
      start_date: '开始日期 (可选)',
      end_date: '结束日期 (可选)'
    }
  },
  get_stock_info: {
    desc: '获取单只股票的基本信息',
    params: {
      symbol: '股票代码'
    }
  },

  // 第七类：交易事件
  get_dragon_tiger_list: {
    desc: '获取指定日期的龙虎榜明细数据',
    params: {
      date: '交易日期'
    }
  },
  get_limit_up_pool: {
    desc: '获取指定日期的涨停股池',
    params: {
      date: '交易日期'
    }
  },
  get_restricted_release: {
    desc: '获取限售解禁数据',
    params: {
      start_date: '开始日期 (可选)',
      end_date: '结束日期 (可选)'
    }
  },

  // 第九类：板块与概念
  get_concept_list: {
    desc: '获取概念板块列表',
    params: {}
  },
  get_concept_constituents: {
    desc: '获取概念板块成分股',
    params: {
      concept_code: '概念板块代码'
    }
  },
  get_stock_industry: {
    desc: '获取个股行业信息',
    params: {
      symbol: '股票代码'
    }
  },
  get_st_stocks: {
    desc: '获取ST股票列表',
    params: {}
  },

  // 第十类：基金与可转债
  get_etf_list: {
    desc: '获取ETF列表',
    params: {}
  },
  get_etf_hist: {
    desc: '获取ETF历史行情',
    params: {
      symbol: 'ETF代码',
      start_date: '开始日期 (可选)',
      end_date: '结束日期 (可选)'
    }
  },
  get_convert_bond_list: {
    desc: '获取可转债列表',
    params: {}
  },
  get_convert_bond_hist: {
    desc: '获取可转债历史行情',
    params: {
      symbol: '可转债代码',
      start_date: '开始日期 (可选)',
      end_date: '结束日期 (可选)'
    }
  },

  // 第十一类：因子数据
  get_all_factors: {
    desc: '获取聚宽因子库所有因子',
    params: {}
  },
  get_factor_kanban_values: {
    desc: '获取因子看板数据',
    params: {
      universe: '股票池: hs300/zz500/zz800/zz1000/zzqz (可选)',
      bt_cycle: '测试周期: month_3/year_1/year_3/year_10 (可选)',
      model: '模型: long_only/long_short (可选)',
      category: '因子分类列表 (可选)',
      skip_paused: '过滤涨停及停牌股 (可选)',
      commision_slippage: '手续费及滑点 (可选)'
    }
  },

  // 其他常用API
  get_all_securities: {
    desc: '获取股票列表',
    params: {
      types: '类型列表 (可选，默认["stock"])',
      date: '日期 (可选)'
    }
  },
  get_trade_days: {
    desc: '获取交易日列表',
    params: {
      start_date: '开始日期 (可选)',
      end_date: '结束日期 (可选)',
      count: '获取数量 (可选)'
    }
  }
};

// ============================================================
// 参数解析
// ============================================================

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const current = argv[i];
    if (!current.startsWith('--')) continue;
    const key = current.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
      continue;
    }
    // 尝试解析 JSON
    if (next.startsWith('{') || next.startsWith('[')) {
      try {
        args[key] = JSON.parse(next);
      } catch {
        args[key] = next;
      }
    } else {
      args[key] = next;
    }
    i++;
  }
  return args;
}

// ============================================================
// 执行数据调用
// ============================================================

async function runDataCall(functionName, params, options = {}) {
  // 构建执行代码
  const executorCode = fs.readFileSync(EXECUTOR_FILE, 'utf8');

  // 构建参数
  const paramsStr = JSON.stringify(params);

  // 创建临时脚本
  const fullCode = `
import json
import os

# 设置环境变量
os.environ['JQ_FUNCTION'] = '${functionName}'
os.environ['JQ_PARAMS'] = '''${paramsStr.replace(/'/g, "\\'")}'''

# 执行
${executorCode}
`;

  // 通过 run-strategy.js 执行
  const { runNotebookTest } = await import('../request/test-joinquant-notebook.js');

  const result = await runNotebookTest({
    sessionFile: options.sessionFile,
    notebookUrl: options.notebookUrl || process.env.JOINQUANT_NOTEBOOK_URL,
    cellSource: fullCode,
    timeoutMs: options.timeoutMs || 60000,
    autoShutdown: true
  });

  return result;
}

// ============================================================
// 主程序
// ============================================================

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    console.log(`
JoinQuant Data CLI

使用方式:
  node joinquant_data_cli.js --function <方法名> --params '<JSON参数>'
  node joinquant_data_cli.js --list                          # 列出所有可用方法
  node joinquant_data_cli.js --test                          # 测试连接

示例:
  # 获取股票日线行情
  node joinquant_data_cli.js --function get_stock_daily --params '{"symbol":"000001.XSHE","count":5}'

  # 获取股票列表
  node joinquant_data_cli.js --function get_all_securities --params '{"types":["stock"],"date":"2024-01-02"}'

  # 获取因子数据
  node joinquant_data_cli.js --function get_factor_kanban_values --params '{"universe":"hs300","bt_cycle":"month_3"}'

  # 获取交易日
  node joinquant_data_cli.js --function get_trade_days --params '{"start_date":"2024-01-01","end_date":"2024-01-10"}'
`);
    return;
  }

  if (args.list) {
    console.log('可用方法列表:\n');
    for (const [name, info] of Object.entries(METHODS)) {
      console.log(`  ${name}`);
      console.log(`    ${info.desc}`);
      const paramCount = Object.keys(info.params).length;
      if (paramCount > 0) {
        console.log(`    参数:`);
        for (const [pname, pdesc] of Object.entries(info.params)) {
          console.log(`      ${pname}: ${pdesc}`);
        }
      }
      console.log();
    }
    return;
  }

  if (args.test) {
    console.log('测试连接...');
    // 简单测试
    try {
      const result = await runDataCall('get_all_securities', { types: ['stock'], date: '2024-01-02' }, {
        timeoutMs: 30000
      });
      console.log('连接成功!');
      return;
    } catch (e) {
      console.error('连接失败:', e.message);
      process.exit(1);
    }
  }

  const functionName = args.function;
  const params = args.params || {};

  if (!functionName) {
    console.error('请指定 --function 参数');
    console.error('使用 --list 查看所有可用方法');
    process.exit(1);
  }

  if (!METHODS[functionName]) {
    console.error(`未知方法: ${functionName}`);
    console.error('使用 --list 查看所有可用方法');
    process.exit(1);
  }

  console.log(`\n调用方法: ${functionName}`);
  console.log(`参数: ${JSON.stringify(params, null, 2)}\n`);

  try {
    const result = await runDataCall(functionName, params, {
      sessionFile: args['session-file'],
      notebookUrl: args['notebook-url'],
      timeoutMs: Number(args['timeout-ms'] || 60000)
    });

    console.log('\n========== 执行结果 ==========\n');
    if (result.executions) {
      for (const exec of result.executions) {
        if (exec.textOutput) {
          console.log(exec.textOutput);
        }
      }
    }
    console.log('\n==============================\n');

  } catch (error) {
    console.error('调用失败:', error.message);
    process.exit(1);
  }
}

main().catch(error => {
  console.error('程序异常:', error.message);
  process.exit(1);
});
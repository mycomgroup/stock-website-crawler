/**
 * JoinQuant API 调用脚本
 *
 * 通过此脚本可以调用聚宽 API 函数并获取返回结果。
 * 支持不同的函数和参数组合，方便在其他地方包装。
 *
 * 使用方式:
 *   node run-api-call.js --function get_price --params '{"security":"000001.XSHE","count":5}'
 *   node run-api-call.js --function get_all_securities --params '{"types":["stock"]}'
 *   node run-api-call.js --function get_factor_kanban_values --params '{"universe":"hs300"}'
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { runNotebookTest } from './request/test-joinquant-notebook.js';
import { OUTPUT_ROOT } from './paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ============================================================
// API 函数定义 - 对应 AbstractDataSource 接口
// ============================================================

const API_DEFINITIONS = {
  // 第一类：行情数据
  get_stock_daily: {
    doc: '获取单只股票的日线行情数据',
    params: {
      symbol: { type: 'string', required: true, desc: '股票代码，如 "000001.XSHE"' },
      start_date: { type: 'string', required: false, desc: '开始日期 "YYYY-MM-DD"' },
      end_date: { type: 'string', required: false, desc: '结束日期 "YYYY-MM-DD"' },
      count: { type: 'number', required: false, desc: '获取最近 count 个交易日' },
      adjust: { type: 'string', required: false, default: 'qfq', desc: '复权类型: qfq/hfq/none' }
    },
    jq_code: `get_price(security, start_date=None, end_date=None, count=None, frequency='daily', fields=['open','close','high','low','volume','money'], skip_paused=False, fq='pre')`
  },

  get_stock_daily_batch: {
    doc: '批量获取多只股票的日线行情数据',
    params: {
      symbols: { type: 'array', required: true, desc: '股票代码列表' },
      start_date: { type: 'string', required: false, desc: '开始日期' },
      end_date: { type: 'string', required: false, desc: '结束日期' },
      count: { type: 'number', required: false, desc: '获取最近 count 个交易日' },
      adjust: { type: 'string', required: false, default: 'qfq', desc: '复权类型' }
    }
  },

  get_stock_minute: {
    doc: '获取单只股票的分时行情数据',
    params: {
      symbol: { type: 'string', required: true, desc: '股票代码' },
      date: { type: 'string', required: true, desc: '交易日期 "YYYY-MM-DD"' },
      freq: { type: 'string', required: false, default: '5min', desc: '频率: 1min/5min/15min/30min/60min' }
    }
  },

  get_call_auction: {
    doc: '获取单只股票的集合竞价数据',
    params: {
      symbol: { type: 'string', required: true, desc: '股票代码' },
      date: { type: 'string', required: true, desc: '交易日期 "YYYY-MM-DD"' }
    }
  },

  // 第二类：估值数据
  get_valuation: {
    doc: '获取单只股票的估值数据',
    params: {
      symbol: { type: 'string', required: true, desc: '股票代码' },
      start_date: { type: 'string', required: false, desc: '开始日期' },
      end_date: { type: 'string', required: false, desc: '结束日期' }
    }
  },

  get_index_valuation: {
    doc: '获取指数的估值数据',
    params: {
      index_symbol: { type: 'string', required: true, desc: '指数代码，如 "000300.XSHG"' },
      start_date: { type: 'string', required: false, desc: '开始日期' },
      end_date: { type: 'string', required: false, desc: '结束日期' }
    }
  },

  // 第三类：财务数据
  get_financial: {
    doc: '获取单只股票的财务报表数据',
    params: {
      symbol: { type: 'string', required: true, desc: '股票代码' },
      table: { type: 'string', required: false, default: 'income', desc: '报表类型: income/balance/cashflow' },
      period: { type: 'string', required: false, default: 'quarterly', desc: '报告周期: quarterly/annual/ttm' }
    }
  },

  get_finance_indicators: {
    doc: '获取单只股票的财务指标数据',
    params: {
      symbol: { type: 'string', required: true, desc: '股票代码' },
      start_date: { type: 'string', required: false, desc: '开始日期' },
      end_date: { type: 'string', required: false, desc: '结束日期' }
    }
  },

  get_dividend: {
    doc: '获取单只股票的分红送转数据',
    params: {
      symbol: { type: 'string', required: true, desc: '股票代码' }
    }
  },

  // 第四类：指数与行业
  get_index_daily: {
    doc: '获取指数的日线行情数据',
    params: {
      symbol: { type: 'string', required: true, desc: '指数代码' },
      start_date: { type: 'string', required: false, desc: '开始日期' },
      end_date: { type: 'string', required: false, desc: '结束日期' },
      count: { type: 'number', required: false, desc: '获取最近 count 个交易日' }
    }
  },

  get_index_components: {
    doc: '获取指数在指定日期的成分股列表',
    params: {
      index_symbol: { type: 'string', required: true, desc: '指数代码' },
      date: { type: 'string', required: true, desc: '查询日期' }
    }
  },

  get_industry_daily: {
    doc: '获取行业指数的日线行情数据',
    params: {
      industry_name: { type: 'string', required: true, desc: '行业名称' },
      start_date: { type: 'string', required: false, desc: '开始日期' },
      end_date: { type: 'string', required: false, desc: '结束日期' }
    }
  },

  get_industry_list: {
    doc: '获取行业分类列表',
    params: {
      level: { type: 'string', required: false, default: 'sw_l1', desc: '行业分类级别: sw_l1/sw_l2/sw_l3' }
    }
  },

  get_industry_classification: {
    doc: '获取股票的行业分类信息',
    params: {
      symbols: { type: 'array', required: true, desc: '股票代码列表' },
      level: { type: 'string', required: false, default: 'sw_l1', desc: '行业分类级别' }
    }
  },

  // 第五类：宏观与情绪
  get_market_spot: {
    doc: '获取指定日期的全市场行情快照',
    params: {
      date: { type: 'string', required: true, desc: '交易日期 "YYYY-MM-DD"' }
    }
  },

  get_money_flow: {
    doc: '获取单只股票的资金流向数据',
    params: {
      symbol: { type: 'string', required: true, desc: '股票代码' },
      start_date: { type: 'string', required: false, desc: '开始日期' },
      end_date: { type: 'string', required: false, desc: '结束日期' }
    }
  },

  get_analyst_forecast: {
    doc: '获取分析师盈利预测数据',
    params: {
      symbol: { type: 'string', required: true, desc: '股票代码' },
      start_date: { type: 'string', required: false, desc: '开始日期' },
      end_date: { type: 'string', required: false, desc: '结束日期' }
    }
  },

  get_shareholder_data: {
    doc: '获取股东人数及户均持股数据',
    params: {
      symbol: { type: 'string', required: true, desc: '股票代码' },
      start_date: { type: 'string', required: false, desc: '开始日期' },
      end_date: { type: 'string', required: false, desc: '结束日期' }
    }
  },

  // 第六类：辅助数据
  get_trading_calendar: {
    doc: '获取交易日日历',
    params: {
      start_date: { type: 'string', required: false, desc: '开始日期' },
      end_date: { type: 'string', required: false, desc: '结束日期' }
    }
  },

  get_stock_info: {
    doc: '获取单只股票的基本信息',
    params: {
      symbol: { type: 'string', required: true, desc: '股票代码' }
    }
  },

  // 第七类：交易事件
  get_dragon_tiger_list: {
    doc: '获取指定日期的龙虎榜明细数据',
    params: {
      date: { type: 'string', required: true, desc: '交易日期 "YYYY-MM-DD"' }
    }
  },

  get_limit_up_pool: {
    doc: '获取指定日期的涨停股池',
    params: {
      date: { type: 'string', required: true, desc: '交易日期 "YYYY-MM-DD"' }
    }
  },

  // 第八类：公司事件
  get_restricted_release: {
    doc: '获取限售解禁数据',
    params: {
      start_date: { type: 'string', required: false, desc: '开始日期' },
      end_date: { type: 'string', required: false, desc: '结束日期' }
    }
  },

  // 第九类：板块与概念
  get_concept_list: {
    doc: '获取概念板块列表',
    params: {}
  },

  get_concept_constituents: {
    doc: '获取概念板块成分股',
    params: {
      concept_code: { type: 'string', required: true, desc: '概念板块代码' }
    }
  },

  get_stock_industry: {
    doc: '获取个股行业信息',
    params: {
      symbol: { type: 'string', required: true, desc: '股票代码' }
    }
  },

  get_st_stocks: {
    doc: '获取ST股票列表',
    params: {}
  },

  // 第十类：基金与可转债
  get_etf_list: {
    doc: '获取ETF列表',
    params: {}
  },

  get_etf_hist: {
    doc: '获取ETF历史行情',
    params: {
      symbol: { type: 'string', required: true, desc: 'ETF代码' },
      start_date: { type: 'string', required: false, desc: '开始日期' },
      end_date: { type: 'string', required: false, desc: '结束日期' }
    }
  },

  get_convert_bond_list: {
    doc: '获取可转债列表',
    params: {}
  },

  get_convert_bond_hist: {
    doc: '获取可转债历史行情',
    params: {
      symbol: { type: 'string', required: true, desc: '可转债代码' },
      start_date: { type: 'string', required: false, desc: '开始日期' },
      end_date: { type: 'string', required: false, desc: '结束日期' }
    }
  },

  // 第十一类：因子数据
  get_all_factors: {
    doc: '获取聚宽因子库所有因子',
    params: {}
  },

  get_factor_kanban_values: {
    doc: '获取因子看板数据',
    params: {
      universe: { type: 'string', required: false, default: 'hs300', desc: '股票池: hs300/zz500/zz800/zz1000/zzqz' },
      bt_cycle: { type: 'string', required: false, default: 'month_3', desc: '测试周期: month_3/year_1/year_3/year_10' },
      model: { type: 'string', required: false, default: 'long_only', desc: '组合构建模型: long_only/long_short' },
      category: { type: 'array', required: false, default: ['quality', 'basics'], desc: '因子分类列表' },
      skip_paused: { type: 'boolean', required: false, default: false, desc: '过滤涨停及停牌股' },
      commision_slippage: { type: 'number', required: false, default: 0, desc: '手续费及滑点' }
    }
  },

  // 其他常用 API
  get_all_securities: {
    doc: '获取股票列表',
    params: {
      types: { type: 'array', required: false, default: ['stock'], desc: '类型列表' },
      date: { type: 'string', required: false, desc: '日期' }
    }
  },

  get_trade_days: {
    doc: '获取交易日列表',
    params: {
      start_date: { type: 'string', required: false, desc: '开始日期' },
      end_date: { type: 'string', required: false, desc: '结束日期' }
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
// 代码生成
// ============================================================

function generateCode(functionName, params) {
  const apiDef = API_DEFINITIONS[functionName];
  if (!apiDef) {
    throw new Error(`未知的 API 函数: ${functionName}`);
  }

  // 构建参数
  const paramEntries = Object.entries(params || {});
  if (paramEntries.length === 0) {
    return `${functionName}()`;
  }

  const args = paramEntries.map(([key, value]) => {
    if (value === null || value === undefined) {
      return `${key}=None`;
    }
    if (typeof value === 'string') {
      return `${key}='${value}'`;
    }
    if (Array.isArray(value)) {
      return `${key}=${JSON.stringify(value)}`;
    }
    if (typeof value === 'boolean') {
      return `${key}=${value}`;
    }
    if (typeof value === 'number') {
      return `${key}=${value}`;
    }
    return `${key}=${JSON.stringify(value)}`;
  });

  return `${functionName}(${args.join(', ')})`;
}

// ============================================================
// 执行 API 调用
// ============================================================

async function runApiCall(functionName, params, options = {}) {
  const apiDef = API_DEFINITIONS[functionName];
  if (!apiDef) {
    throw new Error(`未知的 API 函数: ${functionName}`);
  }

  console.log(`\n调用 API: ${functionName}`);
  console.log(`参数: ${JSON.stringify(params, null, 2)}`);

  const code = generateCode(functionName, params);

  // 构建完整的执行代码
  const fullCode = `
# 调用 ${functionName}
result = ${code}
print("__RESULT_START__")
print(type(result).__name__)
print("__RESULT_DATA__")
if isinstance(result, (pd.DataFrame, pd.Series)):
    print(result.shape if hasattr(result, 'shape') else len(result))
    # 不对结果做 trim，由客户端统一处理
    # 直接打印 DataFrame
    with pd.option_context('display.max_rows', 10, 'display.max_columns', 10, 'display.width', 200):
        print(result.to_string())
elif isinstance(result, dict):
    print(result)
elif isinstance(result, list):
    print(f"list length: {len(result)}")
    print(result[:5] if len(result) > 5 else result)
else:
    print(result)
print("__RESULT_END__")
`;

  console.log(`\n执行代码:\n${fullCode}`);

  const timeoutMs = options.timeoutMs || 60000;

  try {
    const result = await runNotebookTest({
      sessionFile: options.sessionFile,
      notebookUrl: options.notebookUrl || process.env.JOINQUANT_NOTEBOOK_URL,
      cellSource: fullCode,
      timeoutMs,
      autoShutdown: true
    });

    return result;
  } catch (error) {
    console.error(`API 调用失败: ${error.message}`);
    throw error;
  }
}

// ============================================================
// 主程序
// ============================================================

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help || !args.function) {
    console.log(`
JoinQuant API 调用工具

使用方式:
  node run-api-call.js --function <函数名> --params '<JSON参数>'
  node run-api-call.js --function get_price --params '{"security":"000001.XSHE","count":5}'
  node run-api-call.js --list                          # 列出所有可用 API
  node run-api-call.js --help                         # 显示帮助

示例:
  # 获取股票日线行情
  node run-api-call.js --function get_price --params '{"security":"000001.XSHE","count":5,"frequency":"daily"}'

  # 获取股票列表
  node run-api-call.js --function get_all_securities --params '{"types":["stock"],"date":"2024-01-02"}'

  # 获取因子数据
  node run-api-call.js --function get_factor_kanban_values --params '{"universe":"hs300","bt_cycle":"month_3"}'

  # 获取交易日历
  node run-api-call.js --function get_trade_days --params '{"start_date":"2024-01-01","end_date":"2024-01-10"}'

可用 API 函数:
${Object.entries(API_DEFINITIONS).map(([name, def]) => `  ${name}: ${def.doc}`).join('\n')}
`);
    return;
  }

  if (args.list) {
    console.log('可用 API 函数:');
    for (const [name, def] of Object.entries(API_DEFINITIONS)) {
      console.log(`\n${name}:`);
      console.log(`  描述: ${def.doc}`);
      console.log(`  参数:`);
      for (const [paramName, paramDef] of Object.entries(def.params || {})) {
        const required = paramDef.required ? '(必填)' : '(可选)';
        const defaultVal = paramDef.default !== undefined ? ` 默认: ${paramDef.default}` : '';
        console.log(`    ${paramName} ${required}: ${paramDef.desc}${defaultVal}`);
      }
    }
    return;
  }

  const functionName = args.function;
  const params = args.params || {};

  try {
    const result = await runApiCall(functionName, params, {
      sessionFile: args['session-file'],
      notebookUrl: args['notebook-url'],
      timeoutMs: Number(args['timeout-ms'] || 60000)
    });

    console.log('\n========== 执行结果 ==========');
    if (result.executions) {
      for (const exec of result.executions) {
        if (exec.textOutput) {
          console.log(exec.textOutput);
        }
      }
    }
    console.log('==============================\n');

    console.log(`结果文件: ${result.resultFile}`);
  } catch (error) {
    console.error('调用失败:', error.message);
    process.exit(1);
  }
}

main().catch(error => {
  console.error('程序异常:', error.message);
  process.exit(1);
});
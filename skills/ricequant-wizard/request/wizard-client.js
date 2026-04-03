import fs from 'node:fs';
import path from 'node:path';
import '../load-env.js';
import { DATA_DIR, FACTOR_CATALOG_FILE, RICEQUANT_STRATEGY_SESSION } from '../paths.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';

export function loadJson(filePath) {
  if (!fs.existsSync(filePath)) return null;
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch {
    return null;
  }
}

export function saveJson(filePath, data) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

export class WizardClient {
  constructor(options = {}) {
    this.sessionFile = options.sessionFile || RICEQUANT_STRATEGY_SESSION;
    this.sessionPayload = options.sessionPayload || loadJson(this.sessionFile) || {};
    
    if (!this.sessionPayload.cookies?.length && process.env._RQ_SESSION_MISSING === '1') {
      console.warn('警告: 未找到 session 文件，请先运行 ricequant_strategy skill 登录，或在本 skill 的 data/session.json 中配置 cookies');
    }
    
    this.origin = 'https://www.ricequant.com';
    this.cookieJar = options.cookies || this.sessionPayload.cookies || [];
    this.workspaceId = null;
  }

  buildHeaders(url, overrides = {}) {
    return {
      'User-Agent': USER_AGENT,
      'Accept': 'application/json, text/plain, */*',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      'X-Requested-With': 'XMLHttpRequest',
      'Referer': url,
      'Origin': this.origin,
      'Cookie': this.cookieJar.map(c => `${c.name}=${c.value}`).join('; '),
      ...overrides
    };
  }

  async request(url, options = {}) {
    const fullUrl = url.startsWith('http') ? url : `${this.origin}${url}`;
    
    const response = await fetch(fullUrl, {
      method: options.method || 'GET',
      headers: this.buildHeaders(fullUrl, options.headers),
      body: options.body
    });

    const text = await response.text();
    
    if (!response.ok) {
      throw new Error(`Request failed ${response.status} ${fullUrl}: ${text.slice(0, 500)}`);
    }

    try {
      const parsed = JSON.parse(text);
      return parsed;
    } catch {
      return text;
    }
  }

  async getWorkspaceId() {
    if (this.workspaceId) return this.workspaceId;
    
    const result = await this.request('/api/user/v1/workspaces');
    
    if (result.data && result.data.length > 0) {
      this.workspaceId = result.data[0].id;
      return this.workspaceId;
    }
    
    throw new Error('No workspace found');
  }

  async checkLogin() {
    return this.request('/api/user/isLogin.do', { method: 'POST' });
  }

  async listStrategies(options = {}) {
    const workspaceId = await this.getWorkspaceId();
    const url = `/api/strategy/v1/workspaces/${workspaceId}/strategies?code=false&metadata=true`;
    const result = await this.request(url);
    
    let strategies = Array.isArray(result) ? result : [];
    
    if (options.type === 'wizard') {
      strategies = strategies.filter(s => s.metadata?.strategy_type === 'wizard');
    } else if (options.type === 'code') {
      strategies = strategies.filter(s => s.metadata?.strategy_type !== 'wizard');
    }
    
    return strategies.map(s => ({
      id: s._id || s.strategy_id,
      title: s.title,
      type: s.metadata?.strategy_type || 'code',
      lastModified: s.last_modified,
      config: s.config,
      wizardOption: s.metadata?.wizard_option || null
    }));
  }

  async getStrategy(strategyId) {
    const workspaceId = await this.getWorkspaceId();
    const url = `/api/strategy/v1/workspaces/${workspaceId}/strategies/${strategyId}?code=true`;
    return this.request(url);
  }

  async createWizardStrategy(config) {
    const workspaceId = await this.getWorkspaceId();
    const url = `/api/strategy/v1/workspaces/${workspaceId}/strategies`;
    
    const wizardOption = this.buildWizardOption(config);
    const code = this.generateWizardCode(config);
    
    const body = JSON.stringify({
      title: config.name,
      code,
      metadata: {
        strategy_type: 'wizard',
        wizard_option: wizardOption
      },
      config: this.buildBacktestConfig(config.backtest),
      account_type: 'stock',
      permission: 'write'
    });
    
    const result = await this.request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body
    });
    
    return {
      strategyId: result._id || result.strategy_id,
      title: config.name,
      wizardOption
    };
  }

  async updateWizardStrategy(strategyId, config) {
    const workspaceId = await this.getWorkspaceId();
    const url = `/api/strategy/v1/workspaces/${workspaceId}/strategies/${strategyId}`;
    
    const wizardOption = this.buildWizardOption(config);
    const code = this.generateWizardCode(config);
    
    const body = JSON.stringify({
      title: config.name,
      code,
      metadata: {
        strategy_type: 'wizard',
        wizard_option: wizardOption
      }
    });
    
    try {
      return await this.request(url, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body
      });
    } catch {
      return { success: true };
    }
  }

  async deleteStrategy(strategyId) {
    const workspaceId = await this.getWorkspaceId();
    const url = `/api/strategy/v1/workspaces/${workspaceId}/strategies/${strategyId}`;
    
    try {
      await this.request(url, { method: 'DELETE' });
      return true;
    } catch (e) {
      console.log(`Warning: Failed to delete strategy ${strategyId}: ${e.message}`);
      return false;
    }
  }

  async runBacktest(strategyId, backtestConfig) {
    const workspaceId = await this.getWorkspaceId();
    const url = `/api/backtest/v1/workspaces/${workspaceId}/backtests`;
    
    const body = JSON.stringify({
      strategy_id: strategyId,
      code: null,
      config: {
        start_date: backtestConfig.start || '2020-01-01',
        end_date: backtestConfig.end || '2025-03-28',
        stock_init_cash: parseInt(backtestConfig.capital || '100000', 10),
        futures_init_cash: 0,
        bond_init_cash: 0,
        frequency: backtestConfig.frequency || 'day',
        benchmark: backtestConfig.benchmark || '000300.XSHG'
      }
    });
    
    const result = await this.request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body
    });
    
    let backtestId;
    if (typeof result === 'string') {
      backtestId = result.replace(/"/g, '');
    } else {
      backtestId = result.backtestId || result._id || result.id;
      if (typeof backtestId === 'string') {
        backtestId = backtestId.replace(/"/g, '');
      }
    }
    
    return { backtestId };
  }

  async getBacktestResult(backtestId) {
    const workspaceId = await this.getWorkspaceId();
    const url = `/api/backtest/v1/workspaces/${workspaceId}/backtests/${backtestId}`;
    return this.request(url);
  }

  async getBacktestRisk(backtestId) {
    const workspaceId = await this.getWorkspaceId();
    const url = `/api/backtest/v1/workspaces/${workspaceId}/backtests/${backtestId}/risk`;
    try {
      return this.request(url);
    } catch {
      return null;
    }
  }

  async getBacktestLogs(backtestId) {
    const workspaceId = await this.getWorkspaceId();
    const url = `/api/backtest/v1/workspaces/${workspaceId}/backtests/${backtestId}/logs`;
    try {
      return this.request(url);
    } catch {
      return { logs: [] };
    }
  }

  async waitForBacktest(backtestId, options = {}) {
    const maxAttempts = options.maxAttempts || 60;
    const interval = options.interval || 3000;
    const terminalStatuses = new Set(['error_exit', 'cancelled', 'failed', 'stopped']);
    
    for (let i = 0; i < maxAttempts; i++) {
      const result = await this.getBacktestResult(backtestId);
      
      if (result.status === 'finished' || result.progress === 100) {
        return { status: 'finished', result };
      }
      
      if (terminalStatuses.has(result.status)) {
        return { status: 'error', result, exception: result.exception || result.status };
      }
      
      await new Promise(r => setTimeout(r, interval));
    }
    
    return { status: 'timeout' };
  }

  async getFullReport(backtestId) {
    const [result, risk, logs] = await Promise.all([
      this.getBacktestResult(backtestId),
      this.getBacktestRisk(backtestId),
      this.getBacktestLogs(backtestId)
    ]);
    
    return {
      backtestId,
      result,
      risk: risk || result.risk,
      summary: result?.summary || risk || {},
      logs: logs.logs || [],
      exception: result.exception || null
    };
  }

  buildWizardOption(config) {
    const option = {
      template_name: config.template || 'single_period',
      universe: config.universe || ['000300.XSHG'],
      industries: config.industries || ['*'],
      board: config.board || ['*'],
      st_option: config.stOption || 'exclude',
      max_holding_num: config.maxHoldingNum || 10,
      rebalance_interval: config.rebalanceInterval || 5,
      filters: this.buildFilters(config.filters || []),
      sorting: this.buildSorting(config.sorting || []),
      risk: this.buildRisk(config.risk || {}),
      customStockPoolList: [],
      buy: {
        filters: this.buildFilters(config.buy?.filters || []),
        rebalance_interval: config.buy?.rebalanceInterval || 1
      },
      sell: {
        filters: this.buildFilters(config.sell?.filters || []),
        rebalance_interval: config.sell?.rebalanceInterval || 1
      },
      three_periods: {
        max_holding_num: config.maxHoldingNum || 10,
        max_holding_percent: config.maxHoldingPercent || 0.2,
        rebalance_interval: config.rebalanceInterval || 5
      }
    };

    if (config.template === 'three_periods' || config.buy || config.sell) {
      option.template_name = 'three_periods';
    }

    return option;
  }

  buildFilters(filters) {
    return filters.map(f => ({
      operator: f.operator,
      lhs: {
        type: f.factor?.type || 'fundamental',
        name: f.factor?.name || f.name,
        parameters: f.factor?.parameters || f.parameters
      },
      rhs: f.rhs || f.value
    }));
  }

  buildSorting(sorting) {
    return sorting.map(s => ({
      factor: {
        type: s.factor?.type || 'fundamental',
        name: s.factor?.name || s.name,
        parameters: s.factor?.parameters
      },
      ascending: s.ascending !== false,
      weight: s.weight || 1
    }));
  }

  buildRisk(risk) {
    return {
      market_enter_signals: risk.marketEnterSignals || [],
      market_panic_signals: risk.marketPanicSignals || [],
      pnl: risk.pnl || []
    };
  }

  buildBacktestConfig(backtest = {}) {
    return {
      stock_init_cash: parseInt(backtest.capital || '100000', 10),
      futures_init_cash: 0,
      bond_init_cash: 0,
      start_date: backtest.start || '2020-01-01',
      end_date: backtest.end || '2025-03-28',
      frequency: backtest.frequency || 'day',
      benchmark: backtest.benchmark || '000300.XSHG',
      commission_multiplier: 1,
      dividend_reinvestment: false,
      enable_profiler: false,
      enable_short_sell: false,
      margin_multiplier: 1,
      matching_type: 'current_bar',
      slippage: 0,
      slippage_model: 'PriceRatioSlippage',
      volume_limit: false,
      volume_percent: 0.25
    };
  }

generateWizardCode(config) {
    const isThreePeriods = config.template === 'three_periods' || config.buy || config.sell;
    
    if (isThreePeriods) {
      return this._generateThreePeriodsCode(config);
    }
    return this._generateSinglePeriodCode(config);
  }

  _buildFilterCodeLines(filters) {
    return (filters || []).map(f => {
      const factorName = f.factor?.name || f.name;
      const factorType = f.factor?.type || 'fundamental';
      const rhsValue = JSON.stringify(f.rhs || f.value);
      return `    {'operator': '${f.operator}', 'lhs': {'type': '${factorType}', 'name': '${factorName}'}, 'rhs': ${rhsValue}},`;
    }).join('\n');
  }

  _buildSortingCodeLines(sorting) {
    return (sorting || []).map(s => {
      const factorName = s.factor?.name || s.name;
      const factorType = s.factor?.type || 'fundamental';
      const ascending = s.ascending === false ? 'False' : 'True';
      return `    {'weight': ${s.weight || 1}, 'ascending': ${ascending}, 'factor': {'type': '${factorType}', 'name': '${factorName}'}},`;
    }).join('\n');
  }

  _commonCodeHeader(config) {
    const risk = config.risk || {};
    const universeStr = JSON.stringify(config.universe || ['000300.XSHG']);
    const industriesStr = JSON.stringify(config.industries || ['*']);
    const boardStr = JSON.stringify(config.board || ['*']);
    const stOption = config.stOption || 'exclude';
    const profitTaken = risk.profitTaking ?? 'None';
    const stopLoss = risk.stopLoss ?? 'None';

    return `import numpy as np
import pandas as pd
import talib.abstract

UNIVERSE = ${universeStr}
BOARDS = ${boardStr}
INDUSTRIES = ${industriesStr}
ST_OPTION = '${stOption}'

SINGLE_PROFIT_TAKEN = ${profitTaken}
SINGLE_STOP_LOSS = ${stopLoss}

MARKET_ENTER_SIGNALS = []
MARKET_PANIC_SIGNALS = []`;
  }

  _commonFilterFunctions() {
    return `
SIMPLE_OPERATOR = {"greater_than", "less_than", "in_range", "rank_in_range"}

def apply_simple_operator(operator, data, rhs):
    if data is None or data.empty:
        return []
    if operator == "greater_than":
        return data.index[data > rhs].tolist()
    elif operator == "less_than":
        return data.index[data < rhs].tolist()
    elif operator == "in_range":
        vmin, vmax = rhs
        return data.index[(data > vmin) & (data < vmax)].tolist()
    else:
        assert operator == "rank_in_range"
        vmin, vmax = rhs[0] / 100.0, rhs[1] / 100.0
        rank = data.rank(pct=True)
        c = (rank > vmin) & (rank < vmax)
        return c[c].index.tolist()

def filter_for(rule):
    lhs = rule['lhs']
    return filter_for_type(lhs['type'], lhs['name'])

def filter_for_type(type, name):
    if type == 'fundamental':
        return fundamental_filter
    elif type == 'pricing':
        return pricing_filter
    elif type == 'extra':
        if name == 'listed_days':
            return listed_days_filter
    return fundamental_filter

def fundamental_filter(stocks, rule, bar_dict):
    if rule["operator"] not in SIMPLE_OPERATOR:
        return stocks
    data = get_factor(stocks, rule["lhs"]["name"])
    return apply_simple_operator(rule["operator"], data, rule["rhs"])

def listed_days_filter(stocks, rule, bar_dict):
    data = pd.Series({s: instruments(s).days_from_listed() for s in stocks})
    return apply_simple_operator(rule["operator"], data, rule["rhs"])

def pricing_filter(stocks, rule, bar_dict):
    stocks = [s for s in stocks if instruments(s).days_from_listed() > 0]
    lhs, operator, rhs = rule['lhs'], rule['operator'], rule['rhs']
    if operator == 'rank_in_range':
        data = pd.Series({s: getattr(bar_dict[s], lhs['name']) for s in stocks})
        return apply_simple_operator(operator, data, rhs)
    filtered = []
    for s in stocks:
        lv = getattr(bar_dict[s], lhs['name'])
        if operator == "greater_than" and lv > rhs:
            filtered.append(s)
        elif operator == "less_than" and lv < rhs:
            filtered.append(s)
        elif operator == "in_range" and rhs[0] < lv < rhs[1]:
            filtered.append(s)
    return filtered

def apply_filters(stocks, rules, bar_dict):
    for rule in rules:
        f = filter_for(rule)
        stocks = f(stocks, rule, bar_dict)
    return stocks

def sort_stocks(stocks, rules, bar_dict):
    if len(stocks) <= 1:
        return stocks
    if not rules:
        return sorted(stocks)
    result = pd.Series(data=0.0, index=stocks)
    for rule in rules:
        factor = rule["factor"]
        if factor["type"] == "fundamental":
            data = get_factor(stocks, factor["name"])
        elif factor["type"] == "pricing":
            data = pd.Series({s: getattr(bar_dict[s], factor["name"]) for s in stocks})
        elif factor["type"] == "extra":
            if factor["name"] == "listed_days":
                data = pd.Series({s: instruments(s).days_from_listed() for s in stocks})
        na_option = "bottom" if rule["ascending"] else "top"
        result += data.rank(method="average", ascending=rule['ascending'], na_option=na_option, pct=True)
    return result.sort_values().index.tolist()

def get_universe(universe, industries, boards, st_option):
    stocks = set()
    if universe != ["*"]:
        for index in universe:
            i = instruments(index)
            if not i:
                continue
            if i.type == 'INDX':
                stocks.update(index_components(i.order_book_id))
            else:
                stocks.add(i.order_book_id)
    else:
        stocks.update(all_instruments("CS").order_book_id)
    if industries != ["*"]:
        stocks_of_industries = set()
        for ind in industries:
            stocks_of_industries.update(get_industry(ind, source='citics'))
        stocks.intersection_update(stocks_of_industries)
    if boards != ["*"]:
        stocks = {s for s in stocks if instruments(s).board_type in boards}
    if st_option == "only":
        stocks = {s for s in stocks if is_st_stock(s)}
    elif st_option == "exclude":
        stocks = {s for s in stocks if not is_st_stock(s)}
    return list(stocks)

def sell_out_all(portfolio):
    for order_book_id, position in portfolio.positions.items():
        if position.quantity > 0:
            order_target_value(order_book_id, 0)`;
  }

  _generateSinglePeriodCode(config) {
    const filters = config.filters || [];
    const sorting = config.sorting || [];
    const risk = config.risk || {};
    const maxHoldingNum = config.maxHoldingNum || 10;
    const rebalanceInterval = config.rebalanceInterval || 5;

    const filterCode = this._buildFilterCodeLines(filters);
    const sortingCode = this._buildSortingCodeLines(sorting);

    return `${this._commonCodeHeader(config)}

REBALANCE_INTERVAL = ${rebalanceInterval}
MAX_HOLDING_NUM = ${maxHoldingNum}

FILTERS = [
${filterCode}
]

SORTING_RULES = [
${sortingCode}
]
${this._commonFilterFunctions()}

import random

def init(context):
    context.count = -1
    context.strategy_stop = False
    minute = random.randint(1, 15)
    scheduler.run_daily(rebalance_first_part, time_rule=market_open(minute=minute))
    scheduler.run_daily(rebalance_second_part, time_rule=market_open(minute=minute+1))

def before_trading(context):
    context.count += 1

def handle_bar(context, bar_dict):
    if context.strategy_stop:
        sell_out_all(context.portfolio)
        return
    if SINGLE_STOP_LOSS is None and SINGLE_PROFIT_TAKEN is None:
        return
    for order_book_id, position in context.portfolio.positions.items():
        if position.quantity == 0:
            continue
        profit = bar_dict[order_book_id].last / position.avg_price - 1
        if SINGLE_PROFIT_TAKEN is not None and SINGLE_PROFIT_TAKEN < profit:
            order_target_value(order_book_id, 0)
        elif SINGLE_STOP_LOSS is not None and SINGLE_STOP_LOSS > profit:
            order_target_value(order_book_id, 0)

def rebalance_first_part(context, bar_dict):
    if context.count % REBALANCE_INTERVAL != 0 or context.strategy_stop:
        return
    stocks = get_universe(UNIVERSE, INDUSTRIES, BOARDS, ST_OPTION)
    stocks = [s for s in stocks if not is_suspended(s)]
    stocks = apply_filters(stocks, FILTERS, bar_dict)
    stocks = [s for s in stocks if bar_dict[s].last < bar_dict[s].limit_up]
    sorted_pool = sort_stocks(stocks, SORTING_RULES, bar_dict)
    context.buy_list = sorted_pool[:MAX_HOLDING_NUM]
    if context.buy_list:
        context.target_position_value = context.portfolio.total_value * 0.99 / len(context.buy_list)
    else:
        context.target_position_value = 0
    for order_book_id, position in context.stock_account.positions.items():
        if position.quantity > 0:
            if order_book_id not in context.buy_list:
                order_target_value(order_book_id, 0)
            elif position.market_value > context.target_position_value:
                order_target_value(order_book_id, context.target_position_value)

def rebalance_second_part(context, bar_dict):
    if context.count % REBALANCE_INTERVAL != 0 or context.strategy_stop:
        return
    for s in context.buy_list:
        order_target_value(s, context.target_position_value)
`;
  }

  _generateThreePeriodsCode(config) {
    const filters = config.filters || [];
    const sorting = config.sorting || [];
    const buyFilters = config.buy?.filters || [];
    const sellFilters = config.sell?.filters || [];
    const maxHoldingNum = config.maxHoldingNum || 10;
    const maxHoldingPercent = config.maxHoldingPercent || 0.2;
    const rebalanceInterval = config.rebalanceInterval || 5;
    const buyInterval = config.buy?.rebalanceInterval || 1;
    const sellInterval = config.sell?.rebalanceInterval || 1;

    const filterCode = this._buildFilterCodeLines(filters);
    const sortingCode = this._buildSortingCodeLines(sorting);
    const buyFilterCode = this._buildFilterCodeLines(buyFilters);
    const sellFilterCode = this._buildFilterCodeLines(sellFilters);

    return `${this._commonCodeHeader(config)}

REBALANCE_INTERVAL = ${rebalanceInterval}
MAX_HOLDING_NUM = ${maxHoldingNum}
MAX_HOLDING_PERCENT = ${maxHoldingPercent}

BUY_REBALANCE_INTERVAL = ${buyInterval}
SELL_REBALANCE_INTERVAL = ${sellInterval}

# 基础筛选（持仓期）
FILTERS = [
${filterCode}
]

# 买入额外条件
BUY_FILTERS = [
${buyFilterCode}
]

# 卖出触发条件
SELL_FILTERS = [
${sellFilterCode}
]

SORTING_RULES = [
${sortingCode}
]
${this._commonFilterFunctions()}

import random

def init(context):
    context.count = -1
    context.buy_count = -1
    context.sell_count = -1
    context.strategy_stop = False
    minute = random.randint(1, 15)
    scheduler.run_daily(sell_rebalance, time_rule=market_open(minute=minute))
    scheduler.run_daily(buy_rebalance, time_rule=market_open(minute=minute+1))

def before_trading(context):
    context.count += 1
    context.buy_count += 1
    context.sell_count += 1

def handle_bar(context, bar_dict):
    if context.strategy_stop:
        sell_out_all(context.portfolio)
        return
    if SINGLE_STOP_LOSS is None and SINGLE_PROFIT_TAKEN is None:
        return
    for order_book_id, position in context.portfolio.positions.items():
        if position.quantity == 0:
            continue
        profit = bar_dict[order_book_id].last / position.avg_price - 1
        if SINGLE_PROFIT_TAKEN is not None and SINGLE_PROFIT_TAKEN < profit:
            order_target_value(order_book_id, 0)
        elif SINGLE_STOP_LOSS is not None and SINGLE_STOP_LOSS > profit:
            order_target_value(order_book_id, 0)

def sell_rebalance(context, bar_dict):
    """卖出期：检查持仓是否触发卖出条件"""
    if context.sell_count % SELL_REBALANCE_INTERVAL != 0 or context.strategy_stop:
        return
    held = list(context.stock_account.positions.keys())
    if not held:
        return
    # 触发卖出条件的股票直接清仓
    if SELL_FILTERS:
        to_sell = apply_filters(held, SELL_FILTERS, bar_dict)
        for s in to_sell:
            if context.stock_account.positions[s].quantity > 0:
                order_target_value(s, 0)
    # 不再满足基础筛选条件的也卖出
    valid = apply_filters(held, FILTERS, bar_dict)
    valid_set = set(valid)
    for s in held:
        if s not in valid_set and context.stock_account.positions[s].quantity > 0:
            order_target_value(s, 0)

def buy_rebalance(context, bar_dict):
    """买入期：从候选池中选股买入"""
    if context.buy_count % BUY_REBALANCE_INTERVAL != 0 or context.strategy_stop:
        return
    stocks = get_universe(UNIVERSE, INDUSTRIES, BOARDS, ST_OPTION)
    stocks = [s for s in stocks if not is_suspended(s)]
    stocks = apply_filters(stocks, FILTERS, bar_dict)
    if BUY_FILTERS:
        stocks = apply_filters(stocks, BUY_FILTERS, bar_dict)
    stocks = [s for s in stocks if bar_dict[s].last < bar_dict[s].limit_up]
    sorted_pool = sort_stocks(stocks, SORTING_RULES, bar_dict)
    
    current_holdings = {s for s, p in context.stock_account.positions.items() if p.quantity > 0}
    slots_available = MAX_HOLDING_NUM - len(current_holdings)
    
    if slots_available <= 0:
        return
    
    candidates = [s for s in sorted_pool if s not in current_holdings][:slots_available]
    
    target_value = context.portfolio.total_value * MAX_HOLDING_PERCENT
    for s in candidates:
        order_target_value(s, target_value)
`;
  }

  saveReport(backtestId, report) {
    const filePath = path.join(DATA_DIR, `report-${backtestId}-${Date.now()}.json`);
    saveJson(filePath, report);
    return filePath;
  }
}
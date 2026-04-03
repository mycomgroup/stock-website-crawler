import { validateFilter } from './filter-builder.js';
import { validateSortingRule } from './sorting-builder.js';
import { TEMPLATES, ST_OPTIONS, DEFAULT_UNIVERSES } from './factor-definitions.js';

export function validateWizardConfig(config) {
  const errors = [];
  const warnings = [];

  if (!config.name) {
    errors.push('缺少策略名称');
  }

  if (!config.universe || config.universe.length === 0) {
    errors.push('缺少股票池配置');
  }

  if (config.filters && Array.isArray(config.filters)) {
    for (let i = 0; i < config.filters.length; i++) {
      const result = validateFilter(config.filters[i]);
      if (!result.valid) {
        errors.push(`筛选条件 ${i + 1}: ${result.errors.join(', ')}`);
      }
    }
  }

  if (config.sorting && Array.isArray(config.sorting)) {
    for (let i = 0; i < config.sorting.length; i++) {
      const result = validateSortingRule(config.sorting[i]);
      if (!result.valid) {
        errors.push(`排序规则 ${i + 1}: ${result.errors.join(', ')}`);
      }
    }
  }

  if (config.maxHoldingNum !== undefined) {
    if (config.maxHoldingNum < 1 || config.maxHoldingNum > 50) {
      errors.push('maxHoldingNum 应在 1-50 之间');
    }
  }

  if (config.rebalanceInterval !== undefined) {
    if (config.rebalanceInterval < 1) {
      errors.push('rebalanceInterval 应 >= 1');
    }
  }

  if (config.template && !TEMPLATES.find(t => t.name === config.template)) {
    warnings.push(`未知的 template: ${config.template}, 将使用 single_period`);
  }

  if (config.stOption && !ST_OPTIONS.find(o => o.value === config.stOption)) {
    errors.push(`不支持的 stOption: ${config.stOption}`);
  }

  if (config.risk) {
    if (config.risk.profitTaking !== undefined && config.risk.profitTaking <= 0) {
      warnings.push('profitTaking 应 > 0');
    }
    if (config.risk.stopLoss !== undefined && config.risk.stopLoss >= 0) {
      warnings.push('stopLoss 应 < 0');
    }
  }

  if (config.backtest) {
    if (config.backtest.start && config.backtest.end) {
      const start = new Date(config.backtest.start);
      const end = new Date(config.backtest.end);
      if (start >= end) {
        errors.push('回测开始日期应早于结束日期');
      }
    }
    if (config.backtest.capital && config.backtest.capital < 10000) {
      warnings.push('回测资金建议 >= 10000');
    }
  }

  if (config.buy?.filters) {
    for (let i = 0; i < config.buy.filters.length; i++) {
      const result = validateFilter(config.buy.filters[i]);
      if (!result.valid) {
        errors.push(`买入条件 ${i + 1}: ${result.errors.join(', ')}`);
      }
    }
  }

  if (config.sell?.filters) {
    for (let i = 0; i < config.sell.filters.length; i++) {
      const result = validateFilter(config.sell.filters[i]);
      if (!result.valid) {
        errors.push(`卖出条件 ${i + 1}: ${result.errors.join(', ')}`);
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings
  };
}

export function normalizeConfig(config) {
  const normalized = { ...config };

  if (!normalized.template) {
    normalized.template = 'single_period';
  }

  if (!normalized.universe) {
    normalized.universe = ['000300.XSHG'];
  }

  if (!normalized.industries) {
    normalized.industries = ['*'];
  }

  if (!normalized.board) {
    normalized.board = ['*'];
  }

  if (!normalized.stOption) {
    normalized.stOption = 'exclude';
  }

  if (!normalized.maxHoldingNum) {
    normalized.maxHoldingNum = 10;
  }

  if (!normalized.rebalanceInterval) {
    normalized.rebalanceInterval = 5;
  }

  if (!normalized.filters) {
    normalized.filters = [];
  }

  if (!normalized.sorting) {
    normalized.sorting = [];
  }

  if (!normalized.risk) {
    normalized.risk = {};
  }

  if (!normalized.backtest) {
    normalized.backtest = {
      start: '2020-01-01',
      end: '2025-03-28',
      capital: 100000,
      benchmark: '000300.XSHG',
      frequency: 'day'
    };
  }

  normalized.filters = normalized.filters.map(f => ({
    operator: f.operator,
    factor: f.factor || { type: f.type || 'fundamental', name: f.name },
    rhs: f.rhs || f.value
  }));

  normalized.sorting = normalized.sorting.map(s => ({
    factor: s.factor || { type: s.type || 'fundamental', name: s.name },
    ascending: s.ascending !== false,
    weight: s.weight || 1
  }));

  // 归一化 sorting 权重，确保总和为 1
  const totalWeight = normalized.sorting.reduce((sum, s) => sum + s.weight, 0);
  if (totalWeight > 0 && Math.abs(totalWeight - 1) > 0.001) {
    normalized.sorting = normalized.sorting.map(s => ({
      ...s,
      weight: s.weight / totalWeight
    }));
  }

  return normalized;
}
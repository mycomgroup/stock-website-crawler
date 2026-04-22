import { describe, it } from 'node:test';
import assert from 'node:assert';
import { validateWizardConfig, normalizeConfig } from '../lib/config-validator.js';

describe('validateWizardConfig', () => {
  describe('name validation', () => {
    it('should error when name is missing', () => {
      const result = validateWizardConfig({ universe: ['000300.XSHG'] });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['缺少策略名称']);
    });

    it('should error when name is empty string', () => {
      const result = validateWizardConfig({ name: '', universe: ['000300.XSHG'] });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['缺少策略名称']);
    });

    it('should pass when name is provided', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'] });
      assert.strictEqual(result.valid, true);
    });
  });

  describe('universe validation', () => {
    it('should error when universe is missing', () => {
      const result = validateWizardConfig({ name: 'test' });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['缺少股票池配置']);
    });

    it('should error when universe is empty array', () => {
      const result = validateWizardConfig({ name: 'test', universe: [] });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['缺少股票池配置']);
    });

    it('should pass when universe has values', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'] });
      assert.strictEqual(result.valid, true);
    });
  });

  describe('filters validation', () => {
    it('should validate valid filters', () => {
      const config = {
        name: 'test',
        universe: ['000300.XSHG'],
        filters: [
          { operator: 'greater_than', factor: { type: 'fundamental', name: 'pe_ratio' }, rhs: 10 }
        ]
      };
      const result = validateWizardConfig(config);
      assert.strictEqual(result.valid, true);
    });

    it('should error on invalid filter (missing operator)', () => {
      const config = {
        name: 'test',
        universe: ['000300.XSHG'],
        filters: [
          { factor: { type: 'fundamental', name: 'pe_ratio' }, rhs: 10 }
        ]
      };
      const result = validateWizardConfig(config);
      assert.strictEqual(result.valid, false);
      assert.match(result.errors[0], /筛选条件 1/);
      assert.match(result.errors[0], /缺少 operator/);
    });

    it('should error on invalid filter (missing factor)', () => {
      const config = {
        name: 'test',
        universe: ['000300.XSHG'],
        filters: [
          { operator: 'greater_than', rhs: 10 }
        ]
      };
      const result = validateWizardConfig(config);
      assert.strictEqual(result.valid, false);
      assert.match(result.errors[0], /缺少 factor/);
    });

    it('should error on invalid filter (unsupported operator)', () => {
      const config = {
        name: 'test',
        universe: ['000300.XSHG'],
        filters: [
          { operator: 'invalid_op', factor: { type: 'fundamental', name: 'pe_ratio' }, rhs: 10 }
        ]
      };
      const result = validateWizardConfig(config);
      assert.strictEqual(result.valid, false);
      assert.match(result.errors[0], /不支持的 operator/);
    });
  });

  describe('sorting validation', () => {
    it('should validate valid sorting rules', () => {
      const config = {
        name: 'test',
        universe: ['000300.XSHG'],
        sorting: [
          { factor: { type: 'fundamental', name: 'pe_ratio' }, ascending: true, weight: 0.5 }
        ]
      };
      const result = validateWizardConfig(config);
      assert.strictEqual(result.valid, true);
    });

    it('should error on invalid sorting (missing factor)', () => {
      const config = {
        name: 'test',
        universe: ['000300.XSHG'],
        sorting: [
          { ascending: true, weight: 0.5 }
        ]
      };
      const result = validateWizardConfig(config);
      assert.strictEqual(result.valid, false);
      assert.match(result.errors[0], /排序规则 1/);
      assert.match(result.errors[0], /缺少 factor/);
    });

    it('should error on invalid sorting (factor missing type)', () => {
      const config = {
        name: 'test',
        universe: ['000300.XSHG'],
        sorting: [
          { factor: { name: 'pe_ratio' }, ascending: true }
        ]
      };
      const result = validateWizardConfig(config);
      assert.strictEqual(result.valid, false);
      assert.match(result.errors[0], /factor 缺少 type/);
    });

    it('should error on invalid sorting (weight out of range)', () => {
      const config = {
        name: 'test',
        universe: ['000300.XSHG'],
        sorting: [
          { factor: { type: 'fundamental', name: 'pe_ratio' }, weight: 2 }
        ]
      };
      const result = validateWizardConfig(config);
      assert.strictEqual(result.valid, false);
      assert.match(result.errors[0], /weight 应在 0-1 之间/);
    });
  });

  describe('maxHoldingNum validation', () => {
    it('should error when maxHoldingNum < 1', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], maxHoldingNum: 0 });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['maxHoldingNum 应在 1-50 之间']);
    });

    it('should error when maxHoldingNum > 50', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], maxHoldingNum: 51 });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['maxHoldingNum 应在 1-50 之间']);
    });

    it('should pass when maxHoldingNum is 1', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], maxHoldingNum: 1 });
      assert.strictEqual(result.valid, true);
    });

    it('should pass when maxHoldingNum is 50', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], maxHoldingNum: 50 });
      assert.strictEqual(result.valid, true);
    });

    it('should pass for normal values', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], maxHoldingNum: 10 });
      assert.strictEqual(result.valid, true);
    });
  });

  describe('rebalanceInterval validation', () => {
    it('should error when rebalanceInterval < 1', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], rebalanceInterval: 0 });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['rebalanceInterval 应 >= 1']);
    });

    it('should error when rebalanceInterval is negative', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], rebalanceInterval: -1 });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['rebalanceInterval 应 >= 1']);
    });

    it('should pass when rebalanceInterval is 1', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], rebalanceInterval: 1 });
      assert.strictEqual(result.valid, true);
    });

    it('should pass for normal values', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], rebalanceInterval: 5 });
      assert.strictEqual(result.valid, true);
    });
  });

  describe('template validation', () => {
    it('should pass for known template single_period', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], template: 'single_period' });
      assert.strictEqual(result.valid, true);
      assert.strictEqual(result.warnings.length, 0);
    });

    it('should pass for known template three_periods', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], template: 'three_periods' });
      assert.strictEqual(result.valid, true);
      assert.strictEqual(result.warnings.length, 0);
    });

    it('should warn for unknown template', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], template: 'unknown_template' });
      assert.strictEqual(result.valid, true);
      assert.strictEqual(result.warnings.length, 1);
      assert.match(result.warnings[0], /未知的 template/);
    });
  });

  describe('stOption validation', () => {
    it('should pass for valid stOption include', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], stOption: 'include' });
      assert.strictEqual(result.valid, true);
    });

    it('should pass for valid stOption exclude', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], stOption: 'exclude' });
      assert.strictEqual(result.valid, true);
    });

    it('should pass for valid stOption only', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], stOption: 'only' });
      assert.strictEqual(result.valid, true);
    });

    it('should error for invalid stOption', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], stOption: 'invalid' });
      assert.strictEqual(result.valid, false);
      assert.match(result.errors[0], /不支持的 stOption/);
    });
  });

  describe('risk.profitTaking validation', () => {
    it('should warn when profitTaking <= 0', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], risk: { profitTaking: 0 } });
      assert.strictEqual(result.valid, true);
      assert.deepStrictEqual(result.warnings, ['profitTaking 应 > 0']);
    });

    it('should warn when profitTaking is negative', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], risk: { profitTaking: -0.1 } });
      assert.strictEqual(result.valid, true);
      assert.deepStrictEqual(result.warnings, ['profitTaking 应 > 0']);
    });

    it('should pass when profitTaking > 0', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], risk: { profitTaking: 0.2 } });
      assert.strictEqual(result.valid, true);
      assert.strictEqual(result.warnings.length, 0);
    });
  });

  describe('risk.stopLoss validation', () => {
    it('should warn when stopLoss >= 0', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], risk: { stopLoss: 0 } });
      assert.strictEqual(result.valid, true);
      assert.deepStrictEqual(result.warnings, ['stopLoss 应 < 0']);
    });

    it('should warn when stopLoss is positive', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], risk: { stopLoss: 0.1 } });
      assert.strictEqual(result.valid, true);
      assert.deepStrictEqual(result.warnings, ['stopLoss 应 < 0']);
    });

    it('should pass when stopLoss < 0', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'], risk: { stopLoss: -0.1 } });
      assert.strictEqual(result.valid, true);
      assert.strictEqual(result.warnings.length, 0);
    });
  });

  describe('backtest.start/end validation', () => {
    it('should error when start date >= end date', () => {
      const result = validateWizardConfig({
        name: 'test',
        universe: ['000300.XSHG'],
        backtest: { start: '2024-01-01', end: '2024-01-01' }
      });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['回测开始日期应早于结束日期']);
    });

    it('should error when start date > end date', () => {
      const result = validateWizardConfig({
        name: 'test',
        universe: ['000300.XSHG'],
        backtest: { start: '2024-06-01', end: '2024-01-01' }
      });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['回测开始日期应早于结束日期']);
    });

    it('should pass when start date < end date', () => {
      const result = validateWizardConfig({
        name: 'test',
        universe: ['000300.XSHG'],
        backtest: { start: '2020-01-01', end: '2024-01-01' }
      });
      assert.strictEqual(result.valid, true);
    });
  });

  describe('backtest.capital validation', () => {
    it('should warn when capital < 10000', () => {
      const result = validateWizardConfig({
        name: 'test',
        universe: ['000300.XSHG'],
        backtest: { capital: 5000 }
      });
      assert.strictEqual(result.valid, true);
      assert.deepStrictEqual(result.warnings, ['回测资金建议 >= 10000']);
    });

    it('should pass when capital >= 10000', () => {
      const result = validateWizardConfig({
        name: 'test',
        universe: ['000300.XSHG'],
        backtest: { capital: 10000 }
      });
      assert.strictEqual(result.valid, true);
      assert.strictEqual(result.warnings.length, 0);
    });
  });

  describe('buy.filters validation', () => {
    it('should validate buy.filters', () => {
      const config = {
        name: 'test',
        universe: ['000300.XSHG'],
        buy: {
          filters: [
            { operator: 'greater_than', factor: { type: 'fundamental', name: 'roe' }, rhs: 0.1 }
          ]
        }
      };
      const result = validateWizardConfig(config);
      assert.strictEqual(result.valid, true);
    });

    it('should error on invalid buy.filters', () => {
      const config = {
        name: 'test',
        universe: ['000300.XSHG'],
        buy: {
          filters: [
            { factor: { type: 'fundamental', name: 'roe' }, rhs: 0.1 }
          ]
        }
      };
      const result = validateWizardConfig(config);
      assert.strictEqual(result.valid, false);
      assert.match(result.errors[0], /买入条件 1/);
    });
  });

  describe('sell.filters validation', () => {
    it('should validate sell.filters', () => {
      const config = {
        name: 'test',
        universe: ['000300.XSHG'],
        sell: {
          filters: [
            { operator: 'less_than', factor: { type: 'fundamental', name: 'pe_ratio' }, rhs: 5 }
          ]
        }
      };
      const result = validateWizardConfig(config);
      assert.strictEqual(result.valid, true);
    });

    it('should error on invalid sell.filters', () => {
      const config = {
        name: 'test',
        universe: ['000300.XSHG'],
        sell: {
          filters: [
            { factor: { type: 'fundamental', name: 'pe_ratio' }, rhs: 5 }
          ]
        }
      };
      const result = validateWizardConfig(config);
      assert.strictEqual(result.valid, false);
      assert.match(result.errors[0], /卖出条件 1/);
    });
  });

  describe('return value', () => {
    it('should return valid, errors, warnings', () => {
      const result = validateWizardConfig({ name: 'test', universe: ['000300.XSHG'] });
      assert.ok('valid' in result);
      assert.ok('errors' in result);
      assert.ok('warnings' in result);
      assert.ok(Array.isArray(result.errors));
      assert.ok(Array.isArray(result.warnings));
    });
  });
});

describe('normalizeConfig', () => {
  describe('default values', () => {
    it('should set default template', () => {
      const result = normalizeConfig({ name: 'test' });
      assert.strictEqual(result.template, 'single_period');
    });

    it('should set default universe', () => {
      const result = normalizeConfig({ name: 'test' });
      assert.deepStrictEqual(result.universe, ['000300.XSHG']);
    });

    it('should set default industries', () => {
      const result = normalizeConfig({ name: 'test' });
      assert.deepStrictEqual(result.industries, ['*']);
    });

    it('should set default board', () => {
      const result = normalizeConfig({ name: 'test' });
      assert.deepStrictEqual(result.board, ['*']);
    });

    it('should set default stOption', () => {
      const result = normalizeConfig({ name: 'test' });
      assert.strictEqual(result.stOption, 'exclude');
    });

    it('should set default maxHoldingNum', () => {
      const result = normalizeConfig({ name: 'test' });
      assert.strictEqual(result.maxHoldingNum, 10);
    });

    it('should set default rebalanceInterval', () => {
      const result = normalizeConfig({ name: 'test' });
      assert.strictEqual(result.rebalanceInterval, 5);
    });

    it('should set default filters', () => {
      const result = normalizeConfig({ name: 'test' });
      assert.deepStrictEqual(result.filters, []);
    });

    it('should set default sorting', () => {
      const result = normalizeConfig({ name: 'test' });
      assert.deepStrictEqual(result.sorting, []);
    });

    it('should set default risk', () => {
      const result = normalizeConfig({ name: 'test' });
      assert.deepStrictEqual(result.risk, {});
    });

    it('should set default backtest', () => {
      const result = normalizeConfig({ name: 'test' });
      assert.strictEqual(result.backtest.start, '2020-01-01');
      assert.strictEqual(result.backtest.end, '2025-03-28');
      assert.strictEqual(result.backtest.capital, 100000);
      assert.strictEqual(result.backtest.benchmark, '000300.XSHG');
      assert.strictEqual(result.backtest.frequency, 'day');
    });
  });

  describe('filters format conversion', () => {
    it('should convert simple filter format to standard format', () => {
      const config = {
        name: 'test',
        filters: [
          { operator: 'greater_than', type: 'fundamental', name: 'pe_ratio', value: 10 }
        ]
      };
      const result = normalizeConfig(config);
      assert.strictEqual(result.filters[0].operator, 'greater_than');
      assert.deepStrictEqual(result.filters[0].factor, { type: 'fundamental', name: 'pe_ratio' });
      assert.strictEqual(result.filters[0].rhs, 10);
    });

    it('should preserve standard filter format', () => {
      const config = {
        name: 'test',
        filters: [
          { operator: 'greater_than', factor: { type: 'pricing', name: 'close' }, rhs: 100 }
        ]
      };
      const result = normalizeConfig(config);
      assert.strictEqual(result.filters[0].operator, 'greater_than');
      assert.deepStrictEqual(result.filters[0].factor, { type: 'pricing', name: 'close' });
      assert.strictEqual(result.filters[0].rhs, 100);
    });

    it('should handle multiple filters', () => {
      const config = {
        name: 'test',
        filters: [
          { operator: 'greater_than', name: 'pe_ratio', value: 10 },
          { operator: 'less_than', type: 'fundamental', name: 'pb_ratio', rhs: 2 }
        ]
      };
      const result = normalizeConfig(config);
      assert.strictEqual(result.filters.length, 2);
    });
  });

  describe('sorting format conversion', () => {
    it('should convert simple sorting format to standard format', () => {
      const config = {
        name: 'test',
        sorting: [
          { type: 'fundamental', name: 'pe_ratio', ascending: true }
        ]
      };
      const result = normalizeConfig(config);
      assert.deepStrictEqual(result.sorting[0].factor, { type: 'fundamental', name: 'pe_ratio' });
      assert.strictEqual(result.sorting[0].ascending, true);
      assert.strictEqual(result.sorting[0].weight, 1);
    });

    it('should convert ascending: false correctly', () => {
      const config = {
        name: 'test',
        sorting: [
          { name: 'market_cap', ascending: false }
        ]
      };
      const result = normalizeConfig(config);
      assert.strictEqual(result.sorting[0].ascending, false);
    });

    it('should default ascending to true when not specified', () => {
      const config = {
        name: 'test',
        sorting: [
          { name: 'pe_ratio' }
        ]
      };
      const result = normalizeConfig(config);
      assert.strictEqual(result.sorting[0].ascending, true);
    });
  });

  describe('sorting weight normalization', () => {
    it('should normalize weights to sum to 1', () => {
      const config = {
        name: 'test',
        sorting: [
          { factor: { type: 'fundamental', name: 'pe_ratio' }, weight: 2 },
          { factor: { type: 'fundamental', name: 'pb_ratio' }, weight: 2 }
        ]
      };
      const result = normalizeConfig(config);
      assert.strictEqual(result.sorting[0].weight, 0.5);
      assert.strictEqual(result.sorting[1].weight, 0.5);
    });

    it('should not normalize weights that already sum to 1', () => {
      const config = {
        name: 'test',
        sorting: [
          { factor: { type: 'fundamental', name: 'pe_ratio' }, weight: 0.3 },
          { factor: { type: 'fundamental', name: 'pb_ratio' }, weight: 0.7 }
        ]
      };
      const result = normalizeConfig(config);
      assert.strictEqual(result.sorting[0].weight, 0.3);
      assert.strictEqual(result.sorting[1].weight, 0.7);
    });

    it('should handle single sorting rule with weight', () => {
      const config = {
        name: 'test',
        sorting: [
          { factor: { type: 'fundamental', name: 'pe_ratio' }, weight: 1 }
        ]
      };
      const result = normalizeConfig(config);
      assert.strictEqual(result.sorting[0].weight, 1);
    });

    it('should handle three sorting rules with unequal weights', () => {
      const config = {
        name: 'test',
        sorting: [
          { factor: { type: 'fundamental', name: 'pe_ratio' }, weight: 3 },
          { factor: { type: 'fundamental', name: 'pb_ratio' }, weight: 2 },
          { factor: { type: 'fundamental', name: 'roe' }, weight: 1 }
        ]
      };
      const result = normalizeConfig(config);
      const sum = result.sorting.reduce((acc, s) => acc + s.weight, 0);
      assert.ok(Math.abs(sum - 1) < 0.001);
      assert.strictEqual(result.sorting[0].weight, 0.5);
      assert.strictEqual(result.sorting[1].weight, 1/3);
      assert.strictEqual(result.sorting[2].weight, 1/6);
    });
  });

  describe('preserve existing values', () => {
    it('should not modify existing template', () => {
      const result = normalizeConfig({ name: 'test', template: 'three_periods' });
      assert.strictEqual(result.template, 'three_periods');
    });

    it('should not modify existing universe', () => {
      const result = normalizeConfig({ name: 'test', universe: ['000905.XSHG'] });
      assert.deepStrictEqual(result.universe, ['000905.XSHG']);
    });

    it('should not modify existing maxHoldingNum', () => {
      const result = normalizeConfig({ name: 'test', maxHoldingNum: 20 });
      assert.strictEqual(result.maxHoldingNum, 20);
    });

    it('should not modify existing rebalanceInterval', () => {
      const result = normalizeConfig({ name: 'test', rebalanceInterval: 10 });
      assert.strictEqual(result.rebalanceInterval, 10);
    });

    it('should not modify existing risk config', () => {
      const result = normalizeConfig({ name: 'test', risk: { profitTaking: 0.2, stopLoss: -0.1 } });
      assert.strictEqual(result.risk.profitTaking, 0.2);
      assert.strictEqual(result.risk.stopLoss, -0.1);
    });

    it('should not modify existing backtest config', () => {
      const result = normalizeConfig({
        name: 'test',
        backtest: { start: '2021-01-01', end: '2023-12-31', capital: 500000 }
      });
      assert.strictEqual(result.backtest.start, '2021-01-01');
      assert.strictEqual(result.backtest.end, '2023-12-31');
      assert.strictEqual(result.backtest.capital, 500000);
    });

    it('should preserve maxHoldingNum = 0 as existing value (falsy check)', () => {
      const result = normalizeConfig({ name: 'test', maxHoldingNum: 0 });
      assert.strictEqual(result.maxHoldingNum, 0);
    });

    it('should preserve rebalanceInterval = 0 as existing value (falsy check)', () => {
      const result = normalizeConfig({ name: 'test', rebalanceInterval: 0 });
      assert.strictEqual(result.rebalanceInterval, 0);
    });
  });

  describe('edge cases', () => {
    it('should handle empty config', () => {
      const result = normalizeConfig({});
      assert.strictEqual(result.template, 'single_period');
      assert.deepStrictEqual(result.universe, ['000300.XSHG']);
    });

    it('should not mutate original config', () => {
      const original = { name: 'test', maxHoldingNum: 15 };
      const result = normalizeConfig(original);
      assert.strictEqual(original.template, undefined);
      assert.strictEqual(result.maxHoldingNum, 15);
    });
  });
});
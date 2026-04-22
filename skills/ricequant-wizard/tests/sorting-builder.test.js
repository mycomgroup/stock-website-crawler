import { describe, it } from 'node:test';
import assert from 'node:assert';
import { SortingBuilder, validateSortingRule } from '../lib/sorting-builder.js';

describe('SortingBuilder', () => {
  describe('constructor', () => {
    it('should initialize with empty rules array', () => {
      const builder = new SortingBuilder();
      assert.deepStrictEqual(builder.rules, []);
    });
  });

  describe('add', () => {
    it('should add a sorting rule and return this for chaining', () => {
      const builder = new SortingBuilder();
      const result = builder.add({ type: 'fundamental', name: 'pe_ratio' });
      assert.strictEqual(result, builder);
      assert.strictEqual(builder.rules.length, 1);
    });

    it('should add rule with default ascending and weight', () => {
      const builder = new SortingBuilder();
      builder.add({ type: 'fundamental', name: 'pe_ratio' });
      assert.deepStrictEqual(builder.rules[0], {
        factor: { type: 'fundamental', name: 'pe_ratio' },
        ascending: true,
        weight: 1
      });
    });

    it('should add rule with custom ascending', () => {
      const builder = new SortingBuilder();
      builder.add({ type: 'fundamental', name: 'pe_ratio' }, false);
      assert.strictEqual(builder.rules[0].ascending, false);
    });

    it('should add rule with custom weight', () => {
      const builder = new SortingBuilder();
      builder.add({ type: 'fundamental', name: 'pe_ratio' }, true, 0.5);
      assert.strictEqual(builder.rules[0].weight, 0.5);
    });

    it('should add rule with all custom parameters', () => {
      const builder = new SortingBuilder();
      builder.add({ type: 'fundamental', name: 'pe_ratio' }, false, 0.3);
      assert.deepStrictEqual(builder.rules[0], {
        factor: { type: 'fundamental', name: 'pe_ratio' },
        ascending: false,
        weight: 0.3
      });
    });
  });

  describe('sortByMarketCap', () => {
    it('should add market cap sorting rule with descending by default', () => {
      const builder = new SortingBuilder();
      builder.sortByMarketCap();
      assert.strictEqual(builder.rules[0].factor.name, 'market_cap');
      assert.strictEqual(builder.rules[0].ascending, false);
      assert.strictEqual(builder.rules[0].weight, 1);
    });

    it('should add market cap sorting rule with ascending when desc=false', () => {
      const builder = new SortingBuilder();
      builder.sortByMarketCap(false);
      assert.strictEqual(builder.rules[0].ascending, true);
    });

    it('should support chaining', () => {
      const builder = new SortingBuilder();
      const result = builder.sortByMarketCap();
      assert.strictEqual(result, builder);
    });
  });

  describe('sortByPE', () => {
    it('should add PE sorting rule with ascending by default', () => {
      const builder = new SortingBuilder();
      builder.sortByPE();
      assert.strictEqual(builder.rules[0].factor.name, 'pe_ratio');
      assert.strictEqual(builder.rules[0].ascending, true);
      assert.strictEqual(builder.rules[0].weight, 1);
    });

    it('should add PE sorting rule with descending when ascending=false', () => {
      const builder = new SortingBuilder();
      builder.sortByPE(false);
      assert.strictEqual(builder.rules[0].ascending, false);
    });
  });

  describe('sortByPB', () => {
    it('should add PB sorting rule with ascending by default', () => {
      const builder = new SortingBuilder();
      builder.sortByPB();
      assert.strictEqual(builder.rules[0].factor.name, 'pb_ratio');
      assert.strictEqual(builder.rules[0].ascending, true);
      assert.strictEqual(builder.rules[0].weight, 1);
    });

    it('should add PB sorting rule with descending when ascending=false', () => {
      const builder = new SortingBuilder();
      builder.sortByPB(false);
      assert.strictEqual(builder.rules[0].ascending, false);
    });
  });

  describe('sortByROE', () => {
    it('should add ROE sorting rule with descending by default', () => {
      const builder = new SortingBuilder();
      builder.sortByROE();
      assert.strictEqual(builder.rules[0].factor.name, 'roe');
      assert.strictEqual(builder.rules[0].ascending, false);
      assert.strictEqual(builder.rules[0].weight, 1);
    });

    it('should add ROE sorting rule with ascending when desc=false', () => {
      const builder = new SortingBuilder();
      builder.sortByROE(false);
      assert.strictEqual(builder.rules[0].ascending, true);
    });
  });

  describe('sortByDividendYield', () => {
    it('should add dividend yield sorting rule with descending by default', () => {
      const builder = new SortingBuilder();
      builder.sortByDividendYield();
      assert.strictEqual(builder.rules[0].factor.name, 'dividend_yield');
      assert.strictEqual(builder.rules[0].ascending, false);
      assert.strictEqual(builder.rules[0].weight, 1);
    });

    it('should add dividend yield sorting rule with ascending when desc=false', () => {
      const builder = new SortingBuilder();
      builder.sortByDividendYield(false);
      assert.strictEqual(builder.rules[0].ascending, true);
    });
  });

  describe('sortByTurnoverRate', () => {
    it('should add turnover rate sorting rule with descending by default', () => {
      const builder = new SortingBuilder();
      builder.sortByTurnoverRate();
      assert.strictEqual(builder.rules[0].factor.name, 'turnover_rate');
      assert.strictEqual(builder.rules[0].factor.type, 'pricing');
      assert.strictEqual(builder.rules[0].ascending, false);
      assert.strictEqual(builder.rules[0].weight, 1);
    });

    it('should add turnover rate sorting rule with ascending when desc=false', () => {
      const builder = new SortingBuilder();
      builder.sortByTurnoverRate(false);
      assert.strictEqual(builder.rules[0].ascending, true);
    });
  });

  describe('build', () => {
    it('should return rules array', () => {
      const builder = new SortingBuilder();
      builder.sortByPE().sortByPB();
      const result = builder.build();
      assert.strictEqual(result.length, 2);
    });

    it('should return empty array when no rules added', () => {
      const builder = new SortingBuilder();
      const result = builder.build();
      assert.deepStrictEqual(result, []);
    });

    it('should normalize weights when total is not 1', () => {
      const builder = new SortingBuilder();
      builder.add({ type: 'fundamental', name: 'pe_ratio' }, true, 2);
      builder.add({ type: 'fundamental', name: 'pb_ratio' }, true, 2);
      const result = builder.build();
      assert.strictEqual(result[0].weight, 0.5);
      assert.strictEqual(result[1].weight, 0.5);
    });

    it('should not normalize when total is 1', () => {
      const builder = new SortingBuilder();
      builder.add({ type: 'fundamental', name: 'pe_ratio' }, true, 0.6);
      builder.add({ type: 'fundamental', name: 'pb_ratio' }, true, 0.4);
      const result = builder.build();
      assert.strictEqual(result[0].weight, 0.6);
      assert.strictEqual(result[1].weight, 0.4);
    });

    it('should handle single rule with weight 1', () => {
      const builder = new SortingBuilder();
      builder.sortByPE();
      const result = builder.build();
      assert.strictEqual(result[0].weight, 1);
    });

    it('should handle three rules with unequal weights', () => {
      const builder = new SortingBuilder();
      builder.add({ type: 'fundamental', name: 'pe_ratio' }, true, 3);
      builder.add({ type: 'fundamental', name: 'pb_ratio' }, true, 2);
      builder.add({ type: 'fundamental', name: 'roe' }, true, 1);
      const result = builder.build();
      assert.strictEqual(result[0].weight, 0.5);
      assert.strictEqual(result[1].weight, 1/3);
      assert.strictEqual(result[2].weight, 1/6);
    });

    it('should not normalize when total weight is 0', () => {
      const builder = new SortingBuilder();
      builder.add({ type: 'fundamental', name: 'pe_ratio' }, true, 0);
      builder.add({ type: 'fundamental', name: 'pb_ratio' }, true, 0);
      const result = builder.build();
      assert.strictEqual(result[0].weight, 0);
      assert.strictEqual(result[1].weight, 0);
    });

    it('should mutate rules array on normalization', () => {
      const builder = new SortingBuilder();
      builder.add({ type: 'fundamental', name: 'pe_ratio' }, true, 2);
      builder.add({ type: 'fundamental', name: 'pb_ratio' }, true, 2);
      const result = builder.build();
      assert.strictEqual(builder.rules[0].weight, 0.5);
      assert.strictEqual(builder.rules[1].weight, 0.5);
    });
  });

  describe('fromConfig', () => {
    it('should create rules from standard format with factor', () => {
      const config = [
        { factor: { type: 'fundamental', name: 'pe_ratio' }, ascending: true, weight: 1 }
      ];
      const result = SortingBuilder.fromConfig(config);
      assert.strictEqual(result.length, 1);
      assert.deepStrictEqual(result[0].factor, { type: 'fundamental', name: 'pe_ratio' });
      assert.strictEqual(result[0].ascending, true);
      assert.strictEqual(result[0].weight, 1);
    });

    it('should create rules from simplified format with type and name', () => {
      const config = [
        { type: 'fundamental', name: 'pe_ratio', ascending: false }
      ];
      const result = SortingBuilder.fromConfig(config);
      assert.deepStrictEqual(result[0].factor, { type: 'fundamental', name: 'pe_ratio' });
      assert.strictEqual(result[0].ascending, false);
    });

    it('should default type to fundamental when not specified', () => {
      const config = [
        { name: 'pe_ratio' }
      ];
      const result = SortingBuilder.fromConfig(config);
      assert.strictEqual(result[0].factor.type, 'fundamental');
    });

    it('should default ascending to true when not specified', () => {
      const config = [
        { factor: { type: 'fundamental', name: 'pe_ratio' } }
      ];
      const result = SortingBuilder.fromConfig(config);
      assert.strictEqual(result[0].ascending, true);
    });

    it('should set ascending to false when ascending is explicitly false', () => {
      const config = [
        { factor: { type: 'fundamental', name: 'pe_ratio' }, ascending: false }
      ];
      const result = SortingBuilder.fromConfig(config);
      assert.strictEqual(result[0].ascending, false);
    });

    it('should default weight to 1 when not specified', () => {
      const config = [
        { factor: { type: 'fundamental', name: 'pe_ratio' } }
      ];
      const result = SortingBuilder.fromConfig(config);
      assert.strictEqual(result[0].weight, 1);
    });

    it('should handle multiple rules', () => {
      const config = [
        { factor: { type: 'fundamental', name: 'pe_ratio' }, ascending: true, weight: 0.6 },
        { factor: { type: 'fundamental', name: 'pb_ratio' }, ascending: true, weight: 0.4 }
      ];
      const result = SortingBuilder.fromConfig(config);
      assert.strictEqual(result.length, 2);
    });

    it('should normalize weights from config', () => {
      const config = [
        { factor: { type: 'fundamental', name: 'pe_ratio' }, weight: 2 },
        { factor: { type: 'fundamental', name: 'pb_ratio' }, weight: 2 }
      ];
      const result = SortingBuilder.fromConfig(config);
      assert.strictEqual(result[0].weight, 0.5);
      assert.strictEqual(result[1].weight, 0.5);
    });

    it('should handle pricing type factors', () => {
      const config = [
        { type: 'pricing', name: 'turnover_rate', ascending: false }
      ];
      const result = SortingBuilder.fromConfig(config);
      assert.strictEqual(result[0].factor.type, 'pricing');
      assert.strictEqual(result[0].factor.name, 'turnover_rate');
    });
  });
});

describe('validateSortingRule', () => {
  describe('missing factor', () => {
    it('should return error when factor is missing', () => {
      const result = validateSortingRule({ ascending: true, weight: 0.5 });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['缺少 factor']);
    });
  });

  describe('factor missing type', () => {
    it('should return error when factor.type is missing', () => {
      const result = validateSortingRule({
        factor: { name: 'pe_ratio' },
        ascending: true
      });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['factor 缺少 type']);
    });
  });

  describe('factor missing name', () => {
    it('should return error when factor.name is missing', () => {
      const result = validateSortingRule({
        factor: { type: 'fundamental' },
        ascending: true
      });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['factor 缺少 name']);
    });
  });

  describe('weight boundary values', () => {
    it('should return error when weight < 0', () => {
      const result = validateSortingRule({
        factor: { type: 'fundamental', name: 'pe_ratio' },
        weight: -0.1
      });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['weight 应在 0-1 之间']);
    });

    it('should return error when weight > 1', () => {
      const result = validateSortingRule({
        factor: { type: 'fundamental', name: 'pe_ratio' },
        weight: 1.5
      });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['weight 应在 0-1 之间']);
    });

    it('should pass when weight is 0', () => {
      const result = validateSortingRule({
        factor: { type: 'fundamental', name: 'pe_ratio' },
        weight: 0
      });
      assert.strictEqual(result.valid, true);
    });

    it('should pass when weight is 1', () => {
      const result = validateSortingRule({
        factor: { type: 'fundamental', name: 'pe_ratio' },
        weight: 1
      });
      assert.strictEqual(result.valid, true);
    });

    it('should pass when weight is between 0 and 1', () => {
      const result = validateSortingRule({
        factor: { type: 'fundamental', name: 'pe_ratio' },
        weight: 0.5
      });
      assert.strictEqual(result.valid, true);
    });

    it('should pass when weight is undefined', () => {
      const result = validateSortingRule({
        factor: { type: 'fundamental', name: 'pe_ratio' }
      });
      assert.strictEqual(result.valid, true);
    });
  });

  describe('return value', () => {
    it('should return valid and errors array', () => {
      const result = validateSortingRule({
        factor: { type: 'fundamental', name: 'pe_ratio' }
      });
      assert.ok('valid' in result);
      assert.ok('errors' in result);
      assert.ok(Array.isArray(result.errors));
    });

    it('should return valid true for correct rule', () => {
      const result = validateSortingRule({
        factor: { type: 'fundamental', name: 'pe_ratio' },
        ascending: true,
        weight: 0.5
      });
      assert.strictEqual(result.valid, true);
      assert.deepStrictEqual(result.errors, []);
    });
  });

  describe('multiple errors', () => {
    it('should return multiple errors', () => {
      const result = validateSortingRule({
        factor: {},
        weight: 2
      });
      assert.strictEqual(result.valid, false);
      assert.strictEqual(result.errors.length, 3);
      assert.ok(result.errors.includes('factor 缺少 type'));
      assert.ok(result.errors.includes('factor 缺少 name'));
      assert.ok(result.errors.includes('weight 应在 0-1 之间'));
    });
  });

  describe('valid rules', () => {
    it('should pass for valid rule without weight', () => {
      const result = validateSortingRule({
        factor: { type: 'fundamental', name: 'pe_ratio' },
        ascending: true
      });
      assert.strictEqual(result.valid, true);
    });

    it('should pass for valid rule with all fields', () => {
      const result = validateSortingRule({
        factor: { type: 'fundamental', name: 'pe_ratio' },
        ascending: false,
        weight: 0.7
      });
      assert.strictEqual(result.valid, true);
    });

    it('should pass for pricing type factor', () => {
      const result = validateSortingRule({
        factor: { type: 'pricing', name: 'turnover_rate' },
        weight: 0.3
      });
      assert.strictEqual(result.valid, true);
    });

    it('should pass for extra type factor', () => {
      const result = validateSortingRule({
        factor: { type: 'extra', name: 'listed_days' }
      });
      assert.strictEqual(result.valid, true);
    });
  });
});
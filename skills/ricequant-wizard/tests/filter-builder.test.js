import { describe, it } from 'node:test';
import assert from 'node:assert';
import { FilterBuilder, validateFilter } from '../lib/filter-builder.js';

describe('FilterBuilder', () => {
  describe('constructor', () => {
    it('should initialize with empty filters array', () => {
      const builder = new FilterBuilder();
      assert.deepStrictEqual(builder.filters, []);
    });
  });

  describe('add', () => {
    it('should add a filter and return this for chaining', () => {
      const builder = new FilterBuilder();
      const result = builder.add({ type: 'fundamental', name: 'pe_ratio' }, 'less_than', 20);
      assert.strictEqual(result, builder);
      assert.strictEqual(builder.filters.length, 1);
    });

    it('should add filter with correct structure', () => {
      const builder = new FilterBuilder();
      builder.add({ type: 'fundamental', name: 'pe_ratio' }, 'less_than', 20);
      assert.deepStrictEqual(builder.filters[0], {
        operator: 'less_than',
        lhs: { type: 'fundamental', name: 'pe_ratio' },
        rhs: 20
      });
    });
  });

  describe('peLessThan', () => {
    it('should add PE filter with less_than operator', () => {
      const builder = new FilterBuilder();
      builder.peLessThan(15);
      assert.deepStrictEqual(builder.filters[0], {
        operator: 'less_than',
        lhs: { type: 'fundamental', name: 'pe_ratio' },
        rhs: 15
      });
    });

    it('should support chaining', () => {
      const builder = new FilterBuilder();
      const result = builder.peLessThan(15);
      assert.strictEqual(result, builder);
    });
  });

  describe('pbLessThan', () => {
    it('should add PB filter with less_than operator', () => {
      const builder = new FilterBuilder();
      builder.pbLessThan(2);
      assert.deepStrictEqual(builder.filters[0], {
        operator: 'less_than',
        lhs: { type: 'fundamental', name: 'pb_ratio' },
        rhs: 2
      });
    });
  });

  describe('peBetween', () => {
    it('should add PE filter with in_range operator', () => {
      const builder = new FilterBuilder();
      builder.peBetween(5, 20);
      assert.deepStrictEqual(builder.filters[0], {
        operator: 'in_range',
        lhs: { type: 'fundamental', name: 'pe_ratio' },
        rhs: [5, 20]
      });
    });
  });

  describe('pbBetween', () => {
    it('should add PB filter with in_range operator', () => {
      const builder = new FilterBuilder();
      builder.pbBetween(0.5, 3);
      assert.deepStrictEqual(builder.filters[0], {
        operator: 'in_range',
        lhs: { type: 'fundamental', name: 'pb_ratio' },
        rhs: [0.5, 3]
      });
    });
  });

  describe('roeGreaterThan', () => {
    it('should add ROE filter with greater_than operator', () => {
      const builder = new FilterBuilder();
      builder.roeGreaterThan(0.15);
      assert.deepStrictEqual(builder.filters[0], {
        operator: 'greater_than',
        lhs: { type: 'fundamental', name: 'roe' },
        rhs: 0.15
      });
    });
  });

  describe('debtRatioLessThan', () => {
    it('should add debt ratio filter with less_than operator', () => {
      const builder = new FilterBuilder();
      builder.debtRatioLessThan(0.6);
      assert.deepStrictEqual(builder.filters[0], {
        operator: 'less_than',
        lhs: { type: 'fundamental', name: 'debt_ratio' },
        rhs: 0.6
      });
    });
  });

  describe('dividendYieldGreaterThan', () => {
    it('should add dividend yield filter with greater_than operator', () => {
      const builder = new FilterBuilder();
      builder.dividendYieldGreaterThan(0.03);
      assert.deepStrictEqual(builder.filters[0], {
        operator: 'greater_than',
        lhs: { type: 'fundamental', name: 'dividend_yield' },
        rhs: 0.03
      });
    });
  });

  describe('marketCapBetween', () => {
    it('should add market cap filter with in_range operator', () => {
      const builder = new FilterBuilder();
      builder.marketCapBetween(1e9, 1e11);
      assert.deepStrictEqual(builder.filters[0], {
        operator: 'in_range',
        lhs: { type: 'fundamental', name: 'market_cap' },
        rhs: [1e9, 1e11]
      });
    });
  });

  describe('listedDaysGreaterThan', () => {
    it('should add listed days filter with greater_than operator', () => {
      const builder = new FilterBuilder();
      builder.listedDaysGreaterThan(365);
      assert.deepStrictEqual(builder.filters[0], {
        operator: 'greater_than',
        lhs: { type: 'extra', name: 'listed_days' },
        rhs: 365
      });
    });
  });

  describe('rankInRange', () => {
    it('should add filter with rank_in_range operator', () => {
      const builder = new FilterBuilder();
      builder.rankInRange({ type: 'fundamental', name: 'pe_ratio' }, 0.1, 0.3);
      assert.deepStrictEqual(builder.filters[0], {
        operator: 'rank_in_range',
        lhs: { type: 'fundamental', name: 'pe_ratio' },
        rhs: [0.1, 0.3]
      });
    });
  });

  describe('build', () => {
    it('should return filters array', () => {
      const builder = new FilterBuilder();
      builder.peLessThan(20).pbLessThan(2);
      const result = builder.build();
      assert.strictEqual(result.length, 2);
    });

    it('should return empty array when no filters added', () => {
      const builder = new FilterBuilder();
      const result = builder.build();
      assert.deepStrictEqual(result, []);
    });

    it('should return correct filter structure', () => {
      const builder = new FilterBuilder();
      builder.peLessThan(20);
      const result = builder.build();
      assert.deepStrictEqual(result, [{
        operator: 'less_than',
        lhs: { type: 'fundamental', name: 'pe_ratio' },
        rhs: 20
      }]);
    });
  });

  describe('fromConfig', () => {
    it('should create filters from standard format with factor', () => {
      const config = [
        { factor: { type: 'fundamental', name: 'pe_ratio' }, operator: 'less_than', rhs: 20 }
      ];
      const result = FilterBuilder.fromConfig(config);
      assert.strictEqual(result.length, 1);
      assert.deepStrictEqual(result[0].lhs, { type: 'fundamental', name: 'pe_ratio' });
    });

    it('should create filters from simplified format with type and name', () => {
      const config = [
        { type: 'fundamental', name: 'pe_ratio', operator: 'less_than', value: 20 }
      ];
      const result = FilterBuilder.fromConfig(config);
      assert.strictEqual(result.length, 1);
      assert.deepStrictEqual(result[0].lhs, { type: 'fundamental', name: 'pe_ratio' });
      assert.strictEqual(result[0].rhs, 20);
    });

    it('should default type to fundamental when not specified', () => {
      const config = [
        { name: 'pe_ratio', operator: 'less_than', value: 20 }
      ];
      const result = FilterBuilder.fromConfig(config);
      assert.strictEqual(result[0].lhs.type, 'fundamental');
    });

    it('should use rhs over value when both present', () => {
      const config = [
        { factor: { type: 'fundamental', name: 'pe_ratio' }, operator: 'less_than', rhs: 15, value: 20 }
      ];
      const result = FilterBuilder.fromConfig(config);
      assert.strictEqual(result[0].rhs, 15);
    });

    it('should handle multiple filters', () => {
      const config = [
        { factor: { type: 'fundamental', name: 'pe_ratio' }, operator: 'less_than', rhs: 20 },
        { factor: { type: 'fundamental', name: 'pb_ratio' }, operator: 'less_than', rhs: 2 },
        { factor: { type: 'fundamental', name: 'roe' }, operator: 'greater_than', rhs: 0.1 }
      ];
      const result = FilterBuilder.fromConfig(config);
      assert.strictEqual(result.length, 3);
    });

    it('should handle in_range operator with array value', () => {
      const config = [
        { factor: { type: 'fundamental', name: 'pe_ratio' }, operator: 'in_range', rhs: [5, 20] }
      ];
      const result = FilterBuilder.fromConfig(config);
      assert.deepStrictEqual(result[0].rhs, [5, 20]);
    });

    it('should handle pricing type factors', () => {
      const config = [
        { type: 'pricing', name: 'turnover_rate', operator: 'greater_than', value: 0.05 }
      ];
      const result = FilterBuilder.fromConfig(config);
      assert.strictEqual(result[0].lhs.type, 'pricing');
      assert.strictEqual(result[0].lhs.name, 'turnover_rate');
    });

    it('should handle extra type factors', () => {
      const config = [
        { type: 'extra', name: 'listed_days', operator: 'greater_than', value: 365 }
      ];
      const result = FilterBuilder.fromConfig(config);
      assert.strictEqual(result[0].lhs.type, 'extra');
    });
  });
});

describe('validateFilter', () => {
  describe('missing operator', () => {
    it('should return error when operator is missing', () => {
      const result = validateFilter({ factor: { type: 'fundamental', name: 'pe_ratio' }, rhs: 20 });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['缺少 operator']);
    });
  });

  describe('unsupported operator', () => {
    it('should return error for unsupported operator', () => {
      const result = validateFilter({
        operator: 'invalid_operator',
        factor: { type: 'fundamental', name: 'pe_ratio' },
        rhs: 20
      });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['不支持的 operator: invalid_operator']);
    });
  });

  describe('missing factor/lhs', () => {
    it('should return error when factor is missing', () => {
      const result = validateFilter({ operator: 'less_than', rhs: 20 });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['缺少 factor (因子引用)']);
    });

    it('should return error when lhs is missing', () => {
      const result = validateFilter({ operator: 'less_than', rhs: 20 });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['缺少 factor (因子引用)']);
    });
  });

  describe('factor missing type', () => {
    it('should return error when factor.type is missing', () => {
      const result = validateFilter({
        operator: 'less_than',
        factor: { name: 'pe_ratio' },
        rhs: 20
      });
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors.includes('factor 缺少 type'));
    });
  });

  describe('factor missing name', () => {
    it('should return error when factor.name is missing', () => {
      const result = validateFilter({
        operator: 'less_than',
        factor: { type: 'fundamental' },
        rhs: 20
      });
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors.includes('factor 缺少 name'));
    });
  });

  describe('missing rhs/value', () => {
    it('should return error when rhs is missing', () => {
      const result = validateFilter({
        operator: 'less_than',
        factor: { type: 'fundamental', name: 'pe_ratio' }
      });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['缺少 rhs 或 value']);
    });

    it('should accept value as alternative to rhs', () => {
      const result = validateFilter({
        operator: 'less_than',
        factor: { type: 'fundamental', name: 'pe_ratio' },
        value: 20
      });
      assert.strictEqual(result.valid, true);
    });
  });

  describe('requiresArray operators', () => {
    it('should validate in_range requires array', () => {
      const result = validateFilter({
        operator: 'in_range',
        factor: { type: 'fundamental', name: 'pe_ratio' },
        rhs: 20
      });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['in_range 需要 rhs 为数组 [min, max]']);
    });

    it('should pass when in_range has array', () => {
      const result = validateFilter({
        operator: 'in_range',
        factor: { type: 'fundamental', name: 'pe_ratio' },
        rhs: [5, 20]
      });
      assert.strictEqual(result.valid, true);
    });

    it('should validate rank_in_range requires array', () => {
      const result = validateFilter({
        operator: 'rank_in_range',
        factor: { type: 'fundamental', name: 'pe_ratio' },
        rhs: 0.1
      });
      assert.strictEqual(result.valid, false);
      assert.deepStrictEqual(result.errors, ['rank_in_range 需要 rhs 为数组 [min, max]']);
    });

    it('should pass when rank_in_range has array', () => {
      const result = validateFilter({
        operator: 'rank_in_range',
        factor: { type: 'fundamental', name: 'pe_ratio' },
        rhs: [0.1, 0.3]
      });
      assert.strictEqual(result.valid, true);
    });
  });

  describe('return value', () => {
    it('should return valid and errors array', () => {
      const result = validateFilter({
        operator: 'less_than',
        factor: { type: 'fundamental', name: 'pe_ratio' },
        rhs: 20
      });
      assert.ok('valid' in result);
      assert.ok('errors' in result);
      assert.ok(Array.isArray(result.errors));
    });

    it('should return valid true for correct filter', () => {
      const result = validateFilter({
        operator: 'less_than',
        factor: { type: 'fundamental', name: 'pe_ratio' },
        rhs: 20
      });
      assert.strictEqual(result.valid, true);
      assert.deepStrictEqual(result.errors, []);
    });
  });

  describe('multiple errors', () => {
    it('should return multiple errors', () => {
      const result = validateFilter({
        operator: 'invalid',
        factor: { },
        rhs: 20
      });
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors.length > 1);
      assert.ok(result.errors.some(e => e.includes('不支持的 operator')));
      assert.ok(result.errors.some(e => e.includes('factor 缺少 type')));
      assert.ok(result.errors.some(e => e.includes('factor 缺少 name')));
    });
  });

  describe('using lhs instead of factor', () => {
    it('should accept lhs as factor reference', () => {
      const result = validateFilter({
        operator: 'less_than',
        lhs: { type: 'fundamental', name: 'pe_ratio' },
        rhs: 20
      });
      assert.strictEqual(result.valid, true);
    });

    it('should validate lhs missing type', () => {
      const result = validateFilter({
        operator: 'less_than',
        lhs: { name: 'pe_ratio' },
        rhs: 20
      });
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors.includes('factor 缺少 type'));
    });
  });

  describe('all supported operators', () => {
    it('should validate greater_than operator', () => {
      const result = validateFilter({
        operator: 'greater_than',
        factor: { type: 'fundamental', name: 'roe' },
        rhs: 0.1
      });
      assert.strictEqual(result.valid, true);
    });

    it('should validate less_than operator', () => {
      const result = validateFilter({
        operator: 'less_than',
        factor: { type: 'fundamental', name: 'pe_ratio' },
        rhs: 20
      });
      assert.strictEqual(result.valid, true);
    });
  });
});
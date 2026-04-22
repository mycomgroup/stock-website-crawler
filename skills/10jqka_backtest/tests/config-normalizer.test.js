import { jest, describe, test, expect } from '@jest/globals';
import { normalizeConfig } from '../request/config-normalizer.js';

describe('config-normalizer', () => {
  describe('normalizeConfig', () => {
    test('should map query field correctly', () => {
      const input = { query: 'test query' };
      const result = normalizeConfig(input);
      expect(result.query).toBe('test query');
    });

    test('should map formula to query', () => {
      const input = { formula: 'close > ma5' };
      const result = normalizeConfig(input);
      expect(result.query).toBe('close > ma5');
      expect(result.formula).toBeUndefined();
    });

    test('should map conditions to query', () => {
      const input = { conditions: '涨停板' };
      const result = normalizeConfig(input);
      expect(result.query).toBe('涨停板');
    });

    test('should map startDate to start_date', () => {
      const input = { startDate: '2024-01-01' };
      const result = normalizeConfig(input);
      expect(result.start_date).toBe('2024-01-01');
      expect(result.startDate).toBeUndefined();
    });

    test('should keep start_date as is', () => {
      const input = { start_date: '2024-01-01' };
      const result = normalizeConfig(input);
      expect(result.start_date).toBe('2024-01-01');
    });

    test('should map endDate to end_date', () => {
      const input = { endDate: '2024-12-31' };
      const result = normalizeConfig(input);
      expect(result.end_date).toBe('2024-12-31');
      expect(result.endDate).toBeUndefined();
    });

    test('should keep end_date as is', () => {
      const input = { end_date: '2024-12-31' };
      const result = normalizeConfig(input);
      expect(result.end_date).toBe('2024-12-31');
    });

    test('should map daysForSaleStrategy to period', () => {
      const input = { daysForSaleStrategy: '5,10' };
      const result = normalizeConfig(input);
      expect(result.period).toBe('5,10');
    });

    test('should map stockHoldCount to stock_hold', () => {
      const input = { stockHoldCount: '3' };
      const result = normalizeConfig(input);
      expect(result.stock_hold).toBe('3');
    });

    test('should map maxPositions to stock_hold', () => {
      const input = { maxPositions: '5' };
      const result = normalizeConfig(input);
      expect(result.stock_hold).toBe('5');
    });

    test('should map dayBuyStockNum to day_buy_stock_num', () => {
      const input = { dayBuyStockNum: '2' };
      const result = normalizeConfig(input);
      expect(result.day_buy_stock_num).toBe('2');
    });

    test('should map dailyBuyCount to day_buy_stock_num', () => {
      const input = { dailyBuyCount: '3' };
      const result = normalizeConfig(input);
      expect(result.day_buy_stock_num).toBe('3');
    });

    test('should map upperIncome to upper_income', () => {
      const input = { upperIncome: '20' };
      const result = normalizeConfig(input);
      expect(result.upper_income).toBe('20');
    });

    test('should map takeProfit to upper_income', () => {
      const input = { takeProfit: '30' };
      const result = normalizeConfig(input);
      expect(result.upper_income).toBe('30');
    });

    test('should map lowerIncome to lower_income', () => {
      const input = { lowerIncome: '10' };
      const result = normalizeConfig(input);
      expect(result.lower_income).toBe('10');
    });

    test('should map stopLoss to lower_income', () => {
      const input = { stopLoss: '15' };
      const result = normalizeConfig(input);
      expect(result.lower_income).toBe('15');
    });

    test('should map fallIncome to fall_income', () => {
      const input = { fallIncome: '5' };
      const result = normalizeConfig(input);
      expect(result.fall_income).toBe('5');
    });

    test('should map trailingStopLoss to fall_income', () => {
      const input = { trailingStopLoss: '8' };
      const result = normalizeConfig(input);
      expect(result.fall_income).toBe('8');
    });

    test('should map capital to capital', () => {
      const input = { capital: '1000000' };
      const result = normalizeConfig(input);
      expect(result.capital).toBe('1000000');
    });

    test('should map initialCapital to capital', () => {
      const input = { initialCapital: '5000000' };
      const result = normalizeConfig(input);
      expect(result.capital).toBe('5000000');
    });

    test('should map engine to engine', () => {
      const input = { engine: 'v2' };
      const result = normalizeConfig(input);
      expect(result.engine).toBe('v2');
    });

    test('should convert array query to comma-separated string', () => {
      const input = { query: ['涨停板', '创业板', '非ST'] };
      const result = normalizeConfig(input);
      expect(result.query).toBe('涨停板，创业板，非ST');
    });

    test('should apply default capital when not provided', () => {
      const input = { query: 'test' };
      const result = normalizeConfig(input);
      expect(result.capital).toBe('10000000');
    });

    test('should apply default engine when not provided', () => {
      const input = { query: 'test' };
      const result = normalizeConfig(input);
      expect(result.engine).toBe('undefined');
    });

    test('should preserve provided capital', () => {
      const input = { query: 'test', capital: '5000000' };
      const result = normalizeConfig(input);
      expect(result.capital).toBe('5000000');
    });

    test('should preserve provided engine', () => {
      const input = { query: 'test', engine: 'v3' };
      const result = normalizeConfig(input);
      expect(result.engine).toBe('v3');
    });

    test('should handle unknown fields by passing them through', () => {
      const input = { query: 'test', customField: 'customValue' };
      const result = normalizeConfig(input);
      expect(result.customField).toBe('customValue');
    });

    test('should handle complex config with multiple fields', () => {
      const input = {
        formula: 'close > ma5',
        startDate: '2024-01-01',
        endDate: '2024-12-31',
        stockHoldCount: '3',
        dayBuyStockNum: '2',
        upperIncome: '20',
        lowerIncome: '10',
        fallIncome: '5',
        capital: '2000000'
      };
      const result = normalizeConfig(input);
      
      expect(result.query).toBe('close > ma5');
      expect(result.start_date).toBe('2024-01-01');
      expect(result.end_date).toBe('2024-12-31');
      expect(result.stock_hold).toBe('3');
      expect(result.day_buy_stock_num).toBe('2');
      expect(result.upper_income).toBe('20');
      expect(result.lower_income).toBe('10');
      expect(result.fall_income).toBe('5');
      expect(result.capital).toBe('2000000');
    });

    test('should handle empty config', () => {
      const input = {};
      const result = normalizeConfig(input);
      expect(result.capital).toBe('10000000');
      expect(result.engine).toBe('undefined');
    });

    test('should not modify original config object', () => {
      const input = { query: 'test', customField: 'value' };
      const result = normalizeConfig(input);
      expect(input.customField).toBe('value');
      expect(result.customField).toBe('value');
    });

    test('should handle Chinese field names', () => {
      const input = {
        query: '涨停板',
        start_date: '2024-01-01',
        end_date: '2024-12-31'
      };
      const result = normalizeConfig(input);
      
      expect(result.query).toBe('涨停板');
      expect(result.start_date).toBe('2024-01-01');
      expect(result.end_date).toBe('2024-12-31');
    });
  });
});
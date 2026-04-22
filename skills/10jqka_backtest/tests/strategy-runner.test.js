import { jest, describe, test, expect, beforeEach, afterEach } from '@jest/globals';
import fs from 'node:fs';
import path from 'node:path';
import { StrategyRunner } from '../request/strategy-runner.js';

describe('StrategyRunner', () => {
  let runner;
  let mockClient;
  const testOutputDir = './test-output';

  beforeEach(() => {
    mockClient = {
      runBacktest: jest.fn()
    };
    
    runner = new StrategyRunner({
      verbose: false,
      outputRoot: testOutputDir
    });
    runner.client = mockClient;
  });

  afterEach(() => {
    if (fs.existsSync(testOutputDir)) {
      fs.rmSync(testOutputDir, { recursive: true, force: true });
    }
  });

  describe('constructor', () => {
    test('should create instance with default options', () => {
      const runner = new StrategyRunner();
      expect(runner.verbose).toBe(true);
    });

    test('should create instance with verbose false', () => {
      const runner = new StrategyRunner({ verbose: false });
      expect(runner.verbose).toBe(false);
    });

    test('should accept custom outputRoot', () => {
      const runner = new StrategyRunner({ outputRoot: '/custom/path' });
      expect(runner.outputRoot).toBe('/custom/path');
    });
  });

  describe('_safeFloat', () => {
    test('should return number for valid string', () => {
      expect(runner._safeFloat('123.45')).toBe(123.45);
    });

    test('should return number for valid number', () => {
      expect(runner._safeFloat(123.45)).toBe(123.45);
    });

    test('should return default for null', () => {
      expect(runner._safeFloat(null)).toBe(0);
    });

    test('should return default for undefined', () => {
      expect(runner._safeFloat(undefined)).toBe(0);
    });

    test('should return default for empty string', () => {
      expect(runner._safeFloat('')).toBe(0);
    });

    test('should return default for dash string', () => {
      expect(runner._safeFloat('-')).toBe(0);
    });

    test('should return default for NaN', () => {
      expect(runner._safeFloat('abc')).toBe(0);
    });

    test('should return custom default value', () => {
      expect(runner._safeFloat(null, 100)).toBe(100);
    });

    test('should handle percentage strings', () => {
      expect(runner._safeFloat('45.5%')).toBe(45.5);
    });

    test('should handle negative numbers', () => {
      expect(runner._safeFloat('-50.3')).toBe(-50.3);
    });
  });

  describe('_safeInt', () => {
    test('should return integer for valid string', () => {
      expect(runner._safeInt('123')).toBe(123);
    });

    test('should return integer for valid number', () => {
      expect(runner._safeInt(123)).toBe(123);
    });

    test('should truncate decimal numbers', () => {
      expect(runner._safeInt(123.45)).toBe(123);
    });

    test('should return default for null', () => {
      expect(runner._safeInt(null)).toBe(0);
    });

    test('should return default for undefined', () => {
      expect(runner._safeInt(undefined)).toBe(0);
    });

    test('should return default for empty string', () => {
      expect(runner._safeInt('')).toBe(0);
    });

    test('should return default for dash string', () => {
      expect(runner._safeInt('-')).toBe(0);
    });

    test('should return default for NaN', () => {
      expect(runner._safeInt('abc')).toBe(0);
    });

    test('should return custom default value', () => {
      expect(runner._safeInt(null, 50)).toBe(50);
    });
  });

  describe('_extractMetrics', () => {
    test('should extract annual_return', () => {
      const data = { annual_return: '25.5' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.annualReturn).toBe(25.5);
    });

    test('should extract annualReturn', () => {
      const data = { annualReturn: '30.2' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.annualReturn).toBe(30.2);
    });

    test('should extract year_return', () => {
      const data = { year_return: '15.8' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.annualReturn).toBe(15.8);
    });

    test('should extract 年化收益', () => {
      const data = { 年化收益: '20.5' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.annualReturn).toBe(20.5);
    });

    test('should extract total_return', () => {
      const data = { total_return: '100.5' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.totalReturn).toBe(100.5);
    });

    test('should extract 总收益', () => {
      const data = { 总收益: '150.3' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.totalReturn).toBe(150.3);
    });

    test('should extract max_drawdown', () => {
      const data = { max_drawdown: '-15.5' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.maxDrawdown).toBe(-15.5);
    });

    test('should extract maxDrawdown', () => {
      const data = { maxDrawdown: '20.3' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.maxDrawdown).toBe(20.3);
    });

    test('should extract 最大回撤', () => {
      const data = { 最大回撤: '18.5' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.maxDrawdown).toBe(18.5);
    });

    test('should extract win_rate', () => {
      const data = { win_rate: '65.5' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.winRate).toBe(65.5);
    });

    test('should extract winRate', () => {
      const data = { winRate: '70.2' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.winRate).toBe(70.2);
    });

    test('should extract 胜率', () => {
      const data = { 胜率: '55.8' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.winRate).toBe(55.8);
    });

    test('should extract sharpe', () => {
      const data = { sharpe: '1.85' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.sharpe).toBe(1.85);
    });

    test('should extract 夏普', () => {
      const data = { 夏普: '2.1' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.sharpe).toBe(2.1);
    });

    test('should calculate sortino from sharpe', () => {
      const data = { sharpe: '1.5' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.sortino).toBeCloseTo(1.8, 1);
    });

    test('should extract information_ratio', () => {
      const data = { information_ratio: '0.85' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.informationRatio).toBe(0.85);
    });

    test('should extract avg_holding_days', () => {
      const data = { avg_holding_days: '15.5' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.avgHoldingDays).toBe(15.5);
    });

    test('should extract 平均持仓天数', () => {
      const data = { 平均持仓天数: '20' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.avgHoldingDays).toBe(20);
    });

    test('should extract trade_count', () => {
      const data = { trade_count: '50' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.tradeCount).toBe(50);
    });

    test('should extract 交易次数', () => {
      const data = { 交易次数: '35' };
      const metrics = runner._extractMetrics(data);
      expect(metrics.tradeCount).toBe(35);
    });

    test('should extract metrics from nested data.data', () => {
      const data = {
        data: {
          annual_return: '25.5',
          total_return: '100.3'
        }
      };
      const metrics = runner._extractMetrics(data);
      expect(metrics.annualReturn).toBe(25.5);
      expect(metrics.totalReturn).toBe(100.3);
    });

    test('should extract metrics from scoreData', () => {
      const data = {
        data: {
          scoreData: {
            annualYield: '18.5',
            maxDrawDown: 15
          }
        }
      };
      const metrics = runner._extractMetrics(data);
      expect(metrics.annualReturn).toBe(18.5);
      expect(metrics.maxDrawdown).toBe(0.15);
    });

    test('should handle missing metrics with defaults', () => {
      const data = {};
      const metrics = runner._extractMetrics(data);
      expect(metrics.annualReturn).toBe(0);
      expect(metrics.totalReturn).toBe(0);
      expect(metrics.maxDrawdown).toBe(0);
      expect(metrics.winRate).toBe(0);
      expect(metrics.sharpe).toBe(0);
      expect(metrics.tradeCount).toBe(0);
    });
  });

  describe('_extractBacktestId', () => {
    test('should extract task_id', () => {
      const data = { task_id: 'task_123' };
      expect(runner._extractBacktestId(data)).toBe('task_123');
    });

    test('should extract backtest_id', () => {
      const data = { backtest_id: 'bt_456' };
      expect(runner._extractBacktestId(data)).toBe('bt_456');
    });

    test('should extract id', () => {
      const data = { id: 'id_789' };
      expect(runner._extractBacktestId(data)).toBe('id_789');
    });

    test('should extract calc_id', () => {
      const data = { calc_id: 'calc_111' };
      expect(runner._extractBacktestId(data)).toBe('calc_111');
    });

    test('should generate default id when none provided', () => {
      const data = {};
      const id = runner._extractBacktestId(data);
      expect(id).toMatch(/^jqka_\d+$/);
    });

    test('should prioritize task_id over other fields', () => {
      const data = { task_id: 'task_1', backtest_id: 'bt_2', id: 'id_3' };
      expect(runner._extractBacktestId(data)).toBe('task_1');
    });
  });

  describe('_standardizeResult', () => {
    test('should return error for errorcode -401', () => {
      const data = { errorcode: -401 };
      const config = {};
      const result = runner._standardizeResult(data, config);
      
      expect(result.status).toBe('error');
      expect(result.error).toBe('noauth');
      expect(result.message).toBe('未授权，请重新登录');
    });

    test('should return error for errorcode 401', () => {
      const data = { errorcode: 401 };
      const config = {};
      const result = runner._standardizeResult(data, config);
      
      expect(result.status).toBe('error');
      expect(result.error).toBe('noauth');
    });

    test('should return error for error_code -401', () => {
      const data = { error_code: -401 };
      const config = {};
      const result = runner._standardizeResult(data, config);
      
      expect(result.status).toBe('error');
      expect(result.error).toBe('noauth');
    });

    test('should return error for non-zero errorcode', () => {
      const data = { errorcode: -500, message: 'Server error' };
      const config = {};
      const result = runner._standardizeResult(data, config);
      
      expect(result.status).toBe('error');
      expect(result.error).toBe('errorcode_-500');
      expect(result.message).toBe('Server error');
    });

    test('should return ok status for success', () => {
      const data = {
        errorcode: 0,
        task_id: 'task_123',
        annual_return: '25.5'
      };
      const config = {
        query: 'test query',
        period: '2,3',
        start_date: '2024-01-01',
        end_date: '2024-12-31',
        stock_hold: '3',
        upper_income: '20',
        lower_income: '10',
        fall_income: '5',
        day_buy_stock_num: '2',
        capital: '1000000'
      };
      const result = runner._standardizeResult(data, config);
      
      expect(result.status).toBe('ok');
      expect(result.backtest_id).toBe('task_123');
      expect(result.config.query).toBe('test query');
      expect(result.metrics.annualReturn).toBe(25.5);
    });

    test('should include raw data in result', () => {
      const data = { errorcode: 0, custom: 'data' };
      const config = { query: 'test' };
      const result = runner._standardizeResult(data, config);
      
      expect(result.raw).toEqual(data);
    });

    test('should handle undefined errorcode as success', () => {
      const data = { annual_return: '20' };
      const config = { query: 'test' };
      const result = runner._standardizeResult(data, config);
      
      expect(result.status).toBe('ok');
    });

    test('should preserve all config fields', () => {
      const data = { errorcode: 0 };
      const config = {
        query: '涨停板',
        period: '5',
        start_date: '2024-01-01',
        end_date: '2024-06-30',
        stock_hold: '5',
        upper_income: '30',
        lower_income: '12',
        fall_income: '8',
        day_buy_stock_num: '3',
        capital: '5000000'
      };
      const result = runner._standardizeResult(data, config);
      
      expect(result.config).toEqual(config);
    });
  });

  describe('_saveResult', () => {
    test('should save result to file', () => {
      const result = { status: 'ok', test: 'data' };
      const filePath = runner._saveResult(result);
      
      expect(filePath).toMatch(/backtest-\d+\.json$/);
      expect(fs.existsSync(filePath)).toBe(true);
      
      const savedData = JSON.parse(fs.readFileSync(filePath, 'utf8'));
      expect(savedData).toEqual(result);
    });

    test('should create output directory if not exists', () => {
      const newDir = './new-test-output';
      runner.outputRoot = newDir;
      
      if (fs.existsSync(newDir)) {
        fs.rmSync(newDir, { recursive: true, force: true });
      }
      
      const result = { test: 'data' };
      const filePath = runner._saveResult(result);
      
      expect(fs.existsSync(newDir)).toBe(true);
      expect(fs.existsSync(filePath)).toBe(true);
      
      fs.rmSync(newDir, { recursive: true, force: true });
    });

    test('should return file path', () => {
      const result = { test: 'data' };
      const filePath = runner._saveResult(result);
      
      expect(filePath).toContain('backtest-');
      expect(filePath).toContain('test-output');
    });
  });

  describe('run', () => {
    test('should throw error when backtest fails', async () => {
      mockClient.runBacktest.mockRejectedValue(new Error('Network error'));
      
      await expect(runner.run({ query: 'test' }))
        .rejects.toThrow('Network error');
    });

    test('should call client.runBacktest with normalized config', async () => {
      mockClient.runBacktest.mockResolvedValue({
        success: true,
        data: { errorcode: 0, task_id: 'test_id' }
      });
      
      await runner.run({ formula: 'test', startDate: '2024-01-01' });
      
      expect(mockClient.runBacktest).toHaveBeenCalled();
      const calledConfig = mockClient.runBacktest.mock.calls[0][0];
      expect(calledConfig.query).toBe('test');
      expect(calledConfig.start_date).toBe('2024-01-01');
    });
  });

  describe('log', () => {
    test('should log when verbose is true', () => {
      const consoleSpy = jest.spyOn(console, 'log');
      runner.verbose = true;
      runner.log('test message');
      expect(consoleSpy).toHaveBeenCalledWith('test message');
      consoleSpy.mockRestore();
    });

    test('should not log when verbose is false', () => {
      const consoleSpy = jest.spyOn(console, 'log');
      runner.verbose = false;
      runner.log('test message');
      expect(consoleSpy).not.toHaveBeenCalled();
      consoleSpy.mockRestore();
    });
  });
});
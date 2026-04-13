import { JqkaBacktestClient } from './10jqka-client.js';
import { normalizeConfig } from './config-normalizer.js';
import fs from 'node:fs';
import path from 'node:path';
import '../load-env.js';
import { OUTPUT_ROOT } from '../paths.js';

export class StrategyRunner {
  constructor(options = {}) {
    this.client = new JqkaBacktestClient(options);
    this.verbose = options.verbose !== false;
    this.outputRoot = options.outputRoot || OUTPUT_ROOT;
  }

  log(...args) {
    if (this.verbose) console.log(...args);
  }

  async run(rawConfig) {
    try {
      this.log('🧮 格式化策略参数...');
      const config = normalizeConfig(rawConfig);
      this.log('📝 提交给问财引擎的参数:', JSON.stringify(config, null, 2));

      this.log('\n🚀 正在提交10jqka问财回测...');
      const runResult = await this.client.runBacktest(config);
      
      this.log('✅ 回测发起成功!');
      
      const data = runResult.data;
      
      const standardized = this._standardizeResult(data, config);
      
      const resultFile = this._saveResult(standardized);
      this.log(`📊 结果已保存: ${resultFile}`);
      
      return standardized;
      
    } catch (error) {
      this.log(`\n❌ 回测执行失败: ${error.message}`);
      throw error;
    }
  }

  _standardizeResult(data, config) {
    const errorcode = data?.errorcode ?? data?.error_code ?? 0;
    
    if (errorcode === -401 || errorcode === 401) {
      return {
        status: 'error',
        error: 'noauth',
        message: '未授权，请重新登录',
        backtest_id: '',
        metrics: null,
        raw: data
      };
    }
    
    if (errorcode !== 0 && errorcode !== undefined) {
      return {
        status: 'error',
        error: `errorcode_${errorcode}`,
        message: data?.message || data?.msg || '回测失败',
        backtest_id: '',
        metrics: null,
        raw: data
      };
    }
    
    const summary = this._extractMetrics(data);
    
    return {
      status: 'ok',
      backtest_id: this._extractBacktestId(data),
      config: {
        query: config.query,
        period: config.period,
        start_date: config.start_date,
        end_date: config.end_date,
        stock_hold: config.stock_hold,
        upper_income: config.upper_income,
        lower_income: config.lower_income,
        fall_income: config.fall_income,
        day_buy_stock_num: config.day_buy_stock_num,
        capital: config.capital
      },
      metrics: summary,
      raw: data
    };
  }

  _extractMetrics(data) {
    const result = data?.data || data?.result || data;
    const scoreData = result?.scoreData || {};
    const reportData = result?.reportData || {};
    
    const annualReturn = this._safeFloat(
      result?.annual_return ?? 
      result?.annualReturn ?? 
      result?.year_return ?? 
      result?.年化收益 ?? 
      scoreData?.annualYield ?? 
      (reportData?.maxAnnualYield ? reportData.maxAnnualYield[0] : undefined)
    );
    
    const totalReturn = this._safeFloat(
      result?.total_return ?? 
      result?.totalReturn ?? 
      result?.总收益
    );
    
    const maxDrawdown = this._safeFloat(
      result?.max_drawdown ?? 
      result?.maxDrawdown ?? 
      result?.最大回撤 ?? 
      (result?.maxdrop !== undefined ? Math.abs(result?.maxdrop) : undefined) ?? 
      (scoreData?.maxDrawDown !== undefined ? scoreData.maxDrawDown / 100 : undefined)
    );
    
    const winRate = this._safeFloat(
      result?.win_rate ?? 
      result?.winRate ?? 
      result?.胜率 ?? 
      result?.win_ratio ?? 
      (reportData?.maxWinRate ? reportData.maxWinRate[0] : undefined)
    );
    
    const sharpe = this._safeFloat(
      result?.sharpe ?? 
      result?.sharpe_ratio ?? 
      result?.夏普
    );
    
    const sortino = this._safeFloat(
      result?.sortino ?? 
      result?.sortino_ratio ?? 
      sharpe * 1.2
    );
    
    const informationRatio = this._safeFloat(
      result?.information_ratio ?? 
      result?.信息比率 ?? 
      result?.info_ratio
    );
    
    const avgHoldingDays = this._safeFloat(
      result?.avg_holding_days ?? 
      result?.平均持仓天数
    );
    
    const tradeCount = this._safeInt(
      result?.trade_count ?? 
      result?.交易次数 ?? 
      result?.sell_count ?? 
      reportData?.averageStockNum
    );

    return {
      annualReturn: annualReturn,
      totalReturn: totalReturn,
      maxDrawdown: maxDrawdown,
      winRate: winRate,
      sharpe: sharpe,
      sortino: sortino,
      informationRatio: informationRatio,
      avgHoldingDays: avgHoldingDays,
      tradeCount: tradeCount
    };
  }

  _extractBacktestId(data) {
    return data?.task_id ?? 
           data?.backtest_id ?? 
           data?.id ?? 
           data?.calc_id ?? 
           `jqka_${Date.now()}`;
  }

  _safeFloat(val, defaultVal = 0) {
    if (val === null || val === undefined || val === '' || val === '-') {
      return defaultVal;
    }
    const num = parseFloat(val);
    return isNaN(num) ? defaultVal : num;
  }

  _safeInt(val, defaultVal = 0) {
    if (val === null || val === undefined || val === '' || val === '-') {
      return defaultVal;
    }
    const num = parseInt(val);
    return isNaN(num) ? defaultVal : num;
  }

  _saveResult(result) {
    const fileName = `backtest-${Date.now()}.json`;
    const filePath = path.join(this.outputRoot, fileName);
    
    if (!fs.existsSync(this.outputRoot)) {
      fs.mkdirSync(this.outputRoot, { recursive: true });
    }
    
    fs.writeFileSync(filePath, JSON.stringify(result, null, 2), 'utf8');
    return filePath;
  }
}

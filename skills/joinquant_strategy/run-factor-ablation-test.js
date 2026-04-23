#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

const BASE_STRATEGY_FILE = '/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore_offensive/rfscore7_pb10_final.py';

const BACKTEST_CONFIG = {
  startTime: '2022-12-01',
  endTime: '2026-03-30',
  baseCapital: '1000000',
  frequency: 'day'
};

const FACTORS = [
  { name: 'ROA', key: 'roa' },
  { name: 'DELTA_ROA', key: 'delta_roa' },
  { name: 'OCFOA', key: 'ocfoa' },
  { name: 'ACCRUAL', key: 'accrual' },
  { name: 'DELTA_LEVELER', key: 'delta_leveler' },
  { name: 'DELTA_MARGIN', key: 'delta_margin' },
  { name: 'DELTA_TURN', key: 'delta_turn' }
];

function generateAblationCode(baseCode, excludeFactor) {
  const lines = baseCode.split('\n');
  let result = [];
  let inCalcFunction = false;
  let inIndicatorTuple = false;
  let indicatorTupleLines = [];
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    if (line.includes('def calc(self, data):')) {
      inCalcFunction = true;
    }
    
    if (inCalcFunction && line.includes('indicator_tuple = (')) {
      inIndicatorTuple = true;
      indicatorTupleLines = [];
      continue;
    }
    
    if (inIndicatorTuple) {
      if (line.includes(')')) {
        inIndicatorTuple = false;
        const filteredIndicators = indicatorTupleLines.filter(l => {
          if (!excludeFactor) return true;
          return !l.includes(excludeFactor.name);
        });
        result.push('        indicator_tuple = (');
        for (const l of filteredIndicators) {
          result.push(l);
        }
        result.push('        )');
        continue;
      }
      indicatorTupleLines.push(line);
      continue;
    }
    
    if (inCalcFunction && line.includes('self.basic.columns = [')) {
      if (!excludeFactor) {
        result.push(line);
      } else {
        const nextLine = lines[i + 1];
        const columns = nextLine.split(',').map(c => c.trim().replace(/"/g, '').replace(/'/g, '').replace('[', '').replace(']', '').replace(',', '').trim()).filter(c => c);
        const filteredColumns = columns.filter(c => c !== excludeFactor.name);
        result.push('        self.basic.columns = [');
        result.push('            "' + filteredColumns.join('", "') + '",');
        result.push('        ]');
        i++;
        continue;
      }
    }
    
    result.push(line);
  }
  
  return result.join('\n');
}

function generateSingleFactorCode(baseCode, factorKey) {
  let code = baseCode;
  
  code = code.replace(
    /class RFScore\(Factor\):.*?def calc\(self, data\):.*?self\.fscore = self\.basic\.apply\(sign\)\.sum\(axis=1\)/s,
    `class RFScore(Factor):
    name = "RFScore"
    max_window = 1
    dependencies = [
        "${factorKey === 'delta_roa' ? 'roa' : factorKey}",
        "${factorKey === 'delta_roa' ? 'roa_4' : ''}",
    ]

    def calc(self, data):
        ${factorKey === 'roa' ? 'score = data["roa"]' : 
          factorKey === 'delta_roa' ? 'score = data["roa"] / data["roa_4"] - 1' :
          factorKey === 'ocfoa' ? `cfo_sum = data["net_operate_cash_flow"] + data["net_operate_cash_flow_1"] + data["net_operate_cash_flow_2"] + data["net_operate_cash_flow_3"]
        ta_ttm = (data["total_assets"] + data["total_assets_1"] + data["total_assets_2"] + data["total_assets_3"]) / 4
        score = cfo_sum / ta_ttm` :
          factorKey === 'accrual' ? `cfo_sum = data["net_operate_cash_flow"] + data["net_operate_cash_flow_1"] + data["net_operate_cash_flow_2"] + data["net_operate_cash_flow_3"]
        ta_ttm = (data["total_assets"] + data["total_assets_1"] + data["total_assets_2"] + data["total_assets_3"]) / 4
        ocfoa = cfo_sum / ta_ttm
        score = ocfoa - data["roa"] * 0.01` :
          factorKey === 'delta_leveler' ? `leveler = data["total_non_current_liability"] / data["total_assets"]
        leveler1 = data["total_non_current_liability_1"] / data["total_assets_1"]
        score = -(leveler / leveler1 - 1)` :
          factorKey === 'delta_margin' ? 'score = data["gross_profit_margin"] / data["gross_profit_margin_4"] - 1' :
          factorKey === 'delta_turn' ? `turnover = data["operating_revenue"] / (data["total_assets"] + data["total_assets_1"]).mean()
        turnover_1 = data["operating_revenue_4"] / (data["total_assets_4"] + data["total_assets_5"]).mean()
        score = turnover / turnover_1 - 1` : 'score = data["roa"]'}
        
        self.basic = pd.DataFrame({"${factorKey.toUpperCase()}": score})
        self.fscore = (score > 0).astype(int)`
  );
  
  return code;
}

function generatePBOnlyCode(baseCode) {
  let code = baseCode;
  
  code = code.replace(
    /def choose_stocks\(watch_date, hold_num\):/,
    `def choose_stocks_pb_only(watch_date, hold_num):
    stocks = get_universe(watch_date)
    
    val = get_valuation(stocks, end_date=watch_date, fields=["pb_ratio", "pe_ratio"], count=1)
    val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
    
    df = val.copy()
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["pb_ratio"])
    df["pb_group"] = pd.qcut(df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop") + 1
    
    primary = df[df["pb_group"] <= g.primary_pb_group].copy()
    primary = primary.sort_values("pb_ratio", ascending=True)
    picks = primary.index.tolist()
    
    if len(picks) < hold_num:
        secondary = df[df["pb_group"] <= g.reduced_pb_group].copy()
        secondary = secondary.sort_values("pb_ratio", ascending=True)
        for code in secondary.index.tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break
    
    return picks[:hold_num], df

def choose_stocks(watch_date, hold_num):`
  );
  
  return code;
}

const STRATEGY_VARIANTS = [
  { name: 'Baseline_Full7Factors', excludeFactor: null, type: 'baseline' },
  { name: 'No_ROA', excludeFactor: FACTORS[0], type: 'ablation' },
  { name: 'No_DELTA_ROA', excludeFactor: FACTORS[1], type: 'ablation' },
  { name: 'No_OCFOA', excludeFactor: FACTORS[2], type: 'ablation' },
  { name: 'No_ACCRUAL', excludeFactor: FACTORS[3], type: 'ablation' },
  { name: 'No_DELTA_LEVELER', excludeFactor: FACTORS[4], type: 'ablation' },
  { name: 'No_DELTA_MARGIN', excludeFactor: FACTORS[5], type: 'ablation' },
  { name: 'No_DELTA_TURN', excludeFactor: FACTORS[6], type: 'ablation' },
  { name: 'PB_Only_NoRFScore', excludeFactor: 'pb_only', type: 'pb_only' },
];

async function runSingleBacktest(client, context, variant, index, total) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`[${index + 1}/${total}] Running: ${variant.name}`);
  console.log('='.repeat(60));
  
  const baseCode = fs.readFileSync(BASE_STRATEGY_FILE, 'utf8');
  let variantCode;
  
  if (variant.type === 'baseline') {
    variantCode = baseCode;
  } else if (variant.type === 'ablation') {
    variantCode = generateAblationCode(baseCode, variant.excludeFactor);
  } else if (variant.type === 'pb_only') {
    variantCode = generatePBOnlyCode(baseCode);
  }
  
  const strategyName = `RFScore7_Ablation_${variant.name}`;
  console.log(`Strategy name: ${strategyName}`);
  
  console.log('Uploading strategy code...');
  await client.saveStrategy(ALGORITHM_ID, strategyName, variantCode, context);
  
  console.log(`Running backtest: ${BACKTEST_CONFIG.startTime} ~ ${BACKTEST_CONFIG.endTime}`);
  const buildResult = await client.runBacktest(ALGORITHM_ID, variantCode, BACKTEST_CONFIG, context);
  const backtestId = buildResult.backtestId;
  console.log(`Backtest ID: ${backtestId}`);
  
  console.log('Waiting for completion...');
  let attempts = 0;
  const maxAttempts = 90;
  
  while (attempts < maxAttempts) {
    await new Promise(resolve => setTimeout(resolve, 2000));
    attempts++;
    
    try {
      const result = await client.getBacktestResult(backtestId, context);
      
      if (result && result.results) {
        console.log('✓ Backtest completed!');
        
        const r = result.results;
        return {
          success: true,
          backtestId,
          variant: variant.name,
          type: variant.type,
          excludeFactor: variant.excludeFactor?.name || null,
          metrics: {
            totalReturn: (r.total_returns * 100).toFixed(2),
            annualReturn: (r.annualized_returns * 100).toFixed(2),
            sharpe: r.sharpe.toFixed(3),
            maxDrawdown: (r.max_drawdown * 100).toFixed(2),
            alpha: (r.alpha * 100).toFixed(2),
            beta: r.beta.toFixed(3),
            winRate: (r.win_rate * 100).toFixed(1)
          }
        };
      }
      
      if (attempts % 15 === 0) {
        console.log(`  Waiting... ${Math.floor(attempts * 2 / 60)} minutes`);
      }
    } catch (err) {
      console.log(`Error: ${err.message}`);
    }
  }
  
  console.log('⚠ Timeout');
  return {
    success: false,
    backtestId,
    variant: variant.name,
    error: 'Timeout'
  };
}

function analyzeResults(results) {
  console.log('\n' + '='.repeat(80));
  console.log('FACTOR ABLATION ANALYSIS');
  console.log('='.repeat(80));
  
  const successful = results.filter(r => r.success);
  const baseline = successful.find(r => r.type === 'baseline');
  
  if (!baseline) {
    console.log('No baseline result available');
    return;
  }
  
  console.log('\nBaseline (Full 7 Factors):');
  console.log(`  Total Return: ${baseline.metrics.totalReturn}%`);
  console.log(`  Annual Return: ${baseline.metrics.annualReturn}%`);
  console.log(`  Sharpe: ${baseline.metrics.sharpe}`);
  console.log(`  Max Drawdown: ${baseline.metrics.maxDrawdown}%`);
  
  console.log('\n' + '-'.repeat(80));
  console.log('Ablation Results (Factor Contribution Analysis):');
  console.log('-'.repeat(80));
  console.log('Variant          | TotalRet | AnnRet | Sharpe | MaxDD  | Delta_vs_Baseline');
  console.log('-'.repeat(80));
  
  const ablations = successful.filter(r => r.type === 'ablation');
  
  for (const r of ablations) {
    const deltaTR = (parseFloat(r.metrics.totalReturn) - parseFloat(baseline.metrics.totalReturn)).toFixed(2);
    const deltaSR = (parseFloat(r.metrics.sharpe) - parseFloat(baseline.metrics.sharpe)).toFixed(3);
    console.log(
      `${r.variant.padEnd(16)} | ${r.metrics.totalReturn.padStart(7)}% | ${r.metrics.annualReturn.padStart(6)}% | ${r.metrics.sharpe.padStart(6)} | ${r.metrics.maxDrawdown.padStart(5)}% | TR:${deltaTR.padStart(5)} SR:${deltaSR}`
    );
  }
  
  const pbOnly = successful.find(r => r.type === 'pb_only');
  if (pbOnly) {
    const deltaTR = (parseFloat(pbOnly.metrics.totalReturn) - parseFloat(baseline.metrics.totalReturn)).toFixed(2);
    console.log('-'.repeat(80));
    console.log('PB Only (No RFScore):');
    console.log(`  ${pbOnly.variant.padEnd(16)} | ${pbOnly.metrics.totalReturn.padStart(7)}% | ${pbOnly.metrics.annualReturn.padStart(6)}% | ${pbOnly.metrics.sharpe.padStart(6)} | ${pbOnly.metrics.maxDrawdown.padStart(5)}% | TR:${deltaTR.padStart(5)}`);
  }
  
  console.log('\n' + '='.repeat(80));
  console.log('KEY FINDINGS:');
  console.log('='.repeat(80));
  
  const factorImpacts = ablations.map(r => ({
    factor: r.excludeFactor,
    deltaTR: parseFloat(r.metrics.totalReturn) - parseFloat(baseline.metrics.totalReturn),
    deltaSR: parseFloat(r.metrics.sharpe) - parseFloat(baseline.metrics.sharpe)
  })).sort((a, b) => b.deltaTR - a.deltaTR);
  
  const negativeImpacts = factorImpacts.filter(f => f.deltaTR < 0);
  const positiveImpacts = factorImpacts.filter(f => f.deltaTR >= 0);
  
  if (negativeImpacts.length > 0) {
    console.log('\nFactors with POSITIVE contribution (removing them hurts performance):');
    for (const f of negativeImpacts.sort((a, b) => a.deltaTR - b.deltaTR)) {
      console.log(`  - ${f.factor}: removing causes ${f.deltaTR.toFixed(2)}% lower return, ${f.deltaSR.toFixed(3)} lower sharpe`);
    }
  }
  
  if (positiveImpacts.length > 0) {
    console.log('\nFactors with NEGATIVE/NEUTRAL contribution (removing them improves/neutral):');
    for (const f of positiveImpacts) {
      console.log(`  - ${f.factor}: removing causes ${f.deltaTR.toFixed(2)}% higher return, ${f.deltaSR.toFixed(3)} higher sharpe`);
    }
  }
  
  if (pbOnly) {
    const pbDelta = parseFloat(pbOnly.metrics.totalReturn) - parseFloat(baseline.metrics.totalReturn);
    console.log(`\nPB-only vs Full RFScore7: ${pbDelta.toFixed(2)}% delta`);
    if (pbDelta < -5) {
      console.log('  → RFScore factors contribute SIGNIFICANTLY beyond PB selection');
    } else if (pbDelta < 0) {
      console.log('  → RFScore factors contribute SOME value beyond PB selection');
    } else {
      console.log('  → PB selection alone may be sufficient (RFScore adds little)');
    }
  }
}

async function main() {
  console.log('='.repeat(80));
  console.log('RFScore7 Factor Ablation Test');
  console.log('='.repeat(80));
  console.log(`Base Strategy: ${BASE_STRATEGY_FILE}`);
  console.log(`Variants: ${STRATEGY_VARIANTS.length}`);
  console.log(`Backtest Period: ${BACKTEST_CONFIG.startTime} ~ ${BACKTEST_CONFIG.endTime}`);
  
  console.log('\n[1] Ensuring session...');
  await ensureJoinQuantSession({ headed: false, headless: true });
  
  const client = new JoinQuantStrategyClient();
  console.log('\n[2] Getting strategy context...');
  const context = await client.getStrategyContext(ALGORITHM_ID);
  console.log(`Target: ${context.name}`);
  
  const results = [];
  
  console.log('\n[3] Running ablation tests...');
  for (let i = 0; i < STRATEGY_VARIANTS.length; i++) {
    const result = await runSingleBacktest(
      client, 
      context, 
      STRATEGY_VARIANTS[i], 
      i, 
      STRATEGY_VARIANTS.length
    );
    results.push(result);
    
    if (i < STRATEGY_VARIANTS.length - 1) {
      console.log('\nWaiting 5 seconds before next test...');
      await new Promise(resolve => setTimeout(resolve, 5000));
    }
  }
  
  analyzeResults(results);
  
  const outputDir = path.join(__dirname, 'data');
  const outputFile = path.join(outputDir, `factor_ablation_${Date.now()}.json`);
  fs.writeFileSync(outputFile, JSON.stringify({
    config: BACKTEST_CONFIG,
    variants: STRATEGY_VARIANTS,
    results: results
  }, null, 2));
  console.log(`\nResults saved to: ${outputFile}`);
  
  console.log('\n' + '='.repeat(80));
  console.log('DONE');
  console.log('='.repeat(80));
}

main().catch(err => {
  console.error('Failed:', err);
  process.exit(1);
});
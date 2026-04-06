#!/usr/bin/env node
/**
 * 重新提交所有修复了 market_cap 单位的策略
 * 从 rq_strategy_mapping.json 读取 strategyId，重新提交
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { RiceQuantClient } from '../../skills/ricequant_strategy/request/ricequant-client.js';
import { ensureRiceQuantSession } from '../../skills/ricequant_strategy/browser/session-manager.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STRATEGIES_DIR = path.join(__dirname, 'strategies');
const MAPPING_FILE = path.join(__dirname, 'rq_strategy_mapping.json');

const START_DATE = '2023-01-01';
const END_DATE = '2026-04-01';
const MAX_CONCURRENT = 3;
const POLL_INTERVAL_MS = 15000;

async function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// Files fixed in this round (market_cap units + circulating_market_cap)
const FIXED_FILES = process.argv[2] === '--all' ? null : [
  "rq_01_01_wywy1995大侠的小市值AI因子选股_5组参数50.py",
  "rq_01_01_一颗耀眼的星回顾2小市值成长股策略更新改.py",
  "rq_01_7年40倍高回撤低.py",
  "rq_02_02_龙头底分型战法-两年23倍.py",
  "rq_02_7年40倍绩优低价小盘.py",
  "rq_05_ARBR-SGAI-NPTTOR-RPPS.py",
  "rq_05_FL-VOL240-AEttm.py",
  "rq_05_ITR-StPR-STM-NLoMC.py",
  "rq_05_Liquidity-VCPttm-ROAttm.py",
  "rq_05_NCAR-AER-ATR6-VOL20.py",
  "rq_05_ORGR-SRFps-VSTD20-NOCFtOI.py",
  "rq_05_ORGR-TPGR-NPGR-EGR-EPS.py",
  "rq_05_PNF-TPtCR-ITR.py",
  "rq_05_SQR-CoS-CtE.py",
  "rq_05_VSTD20-ARTR-LTDtAR-OC.py",
  "rq_08_14个月200_超短线实盘交易策略_无未来函数.py",
  "rq_08_国九条后中小板微盘小改_年化135.py",
  "rq_08_科技与狠活_纯粹的数据挖掘策略.py",
  "rq_09_FROEC-PB-CAP-HL.py",
  "rq_09_SG-MS-PEG-HL.py",
  "rq_09_持续跑赢大盘_真蓝筹v2_资金容量千万以上.py",
  "rq_10_10倍_二板排板战法优化.py",
  "rq_10_10年52倍_年化59_全新因子方法超稳定.py",
  "rq_10_龙头首阴战法改版二.py",
  "rq_13_涨停研究三_连板股票收益统计与回测.py",
  "rq_13_首板高开_低开_弱转强混合策略.py",
  "rq_14_为实盘做的更新_分钟级别和盘中止损.py",
  "rq_14_胜率65_缩量分歧反包战法.py",
  "rq_15_10年52倍_年化59_全新因子方法超稳定.py",
  "rq_15_2020年_267_年化_13_回撤_上涨趋势策略修改版.py",
  "rq_15_高股息低杠杆小市值轮动策略.py",
  "rq_16_大市值价值投资_从2005年至今超额稳定.py",
  "rq_16_集合竞价三合一_今年收益1067_年化198.py",
  "rq_17_5年多因子超额收益1055_K线风险过滤_无未来函数.py",
  "rq_17_科技与狠活.py",
  "rq_19_高股息低PE价投.py",
  "rq_28_PEG-EBIT-CAP加入换手率因子.py",
  "rq_28_中小综指数增强.py",
  "rq_28_多个成长因子评分.py",
  "rq_28_正黄旗大妈选股.py",
  "rq_29_高增长小市值成长.py",
  "rq_31_蛇皮走位小市值.py",
  "rq_32_追高概率涨停.py",
  "rq_35_精选价值策略.py",
  "rq_39_39_随机森林策略低换手率年化近50pct.py",
];

async function main() {
  console.log('=== Resubmitting market_cap-fixed strategies ===');
  const cookies = await ensureRiceQuantSession({
    username: process.env.RICEQUANT_USERNAME,
    password: process.env.RICEQUANT_PASSWORD
  });
  const client = new RiceQuantClient({ cookies });
  const mapping = JSON.parse(fs.readFileSync(MAPPING_FILE, 'utf8'));

  const filesToSubmit = FIXED_FILES || Object.keys(mapping);
  console.log(`Submitting ${filesToSubmit.length} files\n`);

  let submitted = 0, skipped = 0;

  for (const filename of filesToSubmit) {
    const filepath = path.join(STRATEGIES_DIR, filename);
    if (!fs.existsSync(filepath)) { skipped++; continue; }
    const mapEntry = mapping[filename];
    if (!mapEntry?.strategyId) { skipped++; continue; }

    while (true) {
      const running = await client.getRunningBacktestCount();
      if (running < MAX_CONCURRENT) break;
      process.stdout.write(`  [waiting] ${running}/${MAX_CONCURRENT}\r`);
      await sleep(POLL_INTERVAL_MS);
    }

    try {
      const code = fs.readFileSync(filepath, 'utf8');
      const context = await client.getStrategyContext(mapEntry.strategyId);
      const stratName = context?.name || filename.replace('.py', '');
      await client.saveStrategy(mapEntry.strategyId, stratName, code, context);
      const btResult = await client.runBacktest(mapEntry.strategyId, code, {
        startTime: START_DATE, endTime: END_DATE,
        baseCapital: '100000', frequency: 'day', benchmark: '000300.XSHG'
      }, context);
      let backtestId = btResult.backtestId || btResult._id;
      if (typeof backtestId === 'string') backtestId = backtestId.replace(/"/g, '');
      if (backtestId) {
        console.log(`  ✓ ${filename} -> ${backtestId}`);
        mapping[filename].backtestId = String(backtestId);
        submitted++;
      }
    } catch (e) {
      console.log(`  ✗ ${filename}: ${e.message?.slice(0, 60)}`);
    }
    fs.writeFileSync(MAPPING_FILE, JSON.stringify(mapping, null, 2));
    await sleep(1000);
  }
  console.log(`\n=== Done: submitted=${submitted}, skipped=${skipped} ===`);
}

main().catch(e => { console.error(e); process.exit(1); });

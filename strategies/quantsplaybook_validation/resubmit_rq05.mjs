#!/usr/bin/env node
/**
 * 重新提交修复后的 rq_05_* 策略（更新已有策略代码并重跑回测）
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

const TARGET_FILES = [
  'rq_05_ARBR-SGAI-NPTTOR-RPPS.py',
  'rq_05_FL-VOL240-AEttm.py',
  'rq_05_ITR-StPR-STM-NLoMC.py',
  'rq_05_Liquidity-VCPttm-ROAttm.py',
  'rq_05_NCAR-AER-ATR6-VOL20.py',
  'rq_05_ORGR-SRFps-VSTD20-NOCFtOI.py',
  'rq_05_ORGR-TPGR-NPGR-EGR-EPS.py',
  'rq_05_PNF-TPtCR-ITR.py',
  'rq_05_SQR-CoS-CtE.py',
  'rq_05_VSTD20-ARTR-LTDtAR-OC.py',
];

function loadMapping() {
  try { return JSON.parse(fs.readFileSync(MAPPING_FILE, 'utf8')); } catch { return {}; }
}

function saveMapping(m) {
  fs.writeFileSync(MAPPING_FILE, JSON.stringify(m, null, 2));
}

async function main() {
  console.log('=== 重提交修复后的 rq_05_* 策略 ===\n');

  const credentials = {
    username: process.env.RICEQUANT_USERNAME,
    password: process.env.RICEQUANT_PASSWORD,
  };
  const cookies = await ensureRiceQuantSession(credentials);
  const client = new RiceQuantClient({ cookies });
  const mapping = loadMapping();

  for (const filename of TARGET_FILES) {
    const filepath = path.join(STRATEGIES_DIR, filename);
    const code = fs.readFileSync(filepath, 'utf8');
    const existing = mapping[filename];

    console.log(`\n处理: ${filename}`);
    console.log(`  已有 strategyId: ${existing?.strategyId}`);

    let strategyId = existing?.strategyId;

    // 1. 更新策略代码（用已有 strategyId）
    if (strategyId) {
      try {
        const ctx = await client.getStrategyContext(strategyId);
        const name = ctx?.name || filename.replace(/\.py$/, '');
        await client.saveStrategy(strategyId, name, code, ctx);
        console.log(`  ✓ 代码已更新`);
      } catch (e) {
        console.log(`  ✗ 更新失败: ${e.message}, 尝试新建...`);
        strategyId = null;
      }
    }

    // 2. 若无 strategyId 或更新失败，新建策略
    if (!strategyId) {
      try {
        const name = `rq_${filename.replace(/\.py$/, '')}_${Date.now()}`;
        const res = await client.createStrategy(name, code);
        strategyId = res.strategy_id || res._id || res.id;
        console.log(`  ✓ 新建策略: ${strategyId}`);
      } catch (e) {
        console.log(`  ✗ 新建失败: ${e.message}`);
        continue;
      }
    }

    // 3. 获取上下文并提交回测
    let context;
    try {
      context = await client.getStrategyContext(strategyId);
    } catch (e) {
      console.log(`  ✗ 获取上下文失败: ${e.message}`);
      continue;
    }

    let backtestId;
    // 等待有空位再提交（最多等5分钟）
    for (let attempt = 0; attempt < 20; attempt++) {
      try {
        const btResult = await client.runBacktest(strategyId, code, {
          startTime: START_DATE,
          endTime: END_DATE,
          baseCapital: '100000',
          frequency: 'day',
          benchmark: '000300.XSHG',
        }, context);
        backtestId = btResult.backtestId || btResult._id || btResult.id;
        if (typeof backtestId === 'string') backtestId = backtestId.replace(/"/g, '');
        console.log(`  ✓ 回测已提交: ${backtestId}`);
        break;
      } catch (e) {
        if (e.message.includes('最大数量') || e.message.includes('403')) {
          process.stdout.write(`  ⏳ 等待回测槽位... (${attempt + 1}/20)\r`);
          await new Promise(r => setTimeout(r, 15000));
        } else {
          console.log(`  ✗ 回测提交失败: ${e.message}`);
          break;
        }
      }
    }
    if (!backtestId) { console.log(`  ✗ 超时，跳过`); continue; }

    // 4. 更新 mapping
    mapping[filename] = {
      strategyId,
      backtestId: String(backtestId),
      submittedAt: new Date().toISOString(),
    };
    saveMapping(mapping);
    console.log(`  ✓ mapping 已更新`);
  }

  console.log('\n=== 全部完成 ===');
  console.log('运行 fetch_new_results.mjs 获取回测结果');
}

main().catch(e => { console.error('Fatal:', e); process.exit(1); });

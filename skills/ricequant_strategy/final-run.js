import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const AUTH_STATE_FILE = path.join(__dirname, 'data', 'auth-state.json');
const OUTPUT_DIR = path.join(__dirname, 'data');

async function runBacktest(strategyId, codeFile, startDate, endDate) {
  const code = fs.readFileSync(codeFile, 'utf8');
  const strategyName = path.basename(codeFile, '.py');
  
  console.log('\n' + '='.repeat(60));
  console.log('RiceQuant Backtest Runner');
  console.log('='.repeat(60));
  console.log('Strategy:', strategyName);
  console.log('ID:', strategyId);
  console.log('Period:', startDate, '-', endDate);
  console.log('='.repeat(60) + '\n');
  
  if (!fs.existsSync(AUTH_STATE_FILE)) {
    console.error('Error: Auth state file not found:', AUTH_STATE_FILE);
    console.error('Please run auto-login.js first to authenticate.');
    process.exit(1);
  }
  const state = JSON.parse(fs.readFileSync(AUTH_STATE_FILE, 'utf8'));
  
  const browser = await chromium.launch({ 
    headless: true,
    slowMo: 50
  });
  
  const context = await browser.newContext({
    storageState: state,
    viewport: { width: 1400, height: 900 }
  });
  
  const page = await context.newPage();
  let resultData = {
    strategyId,
    strategyName,
    startDate,
    endDate,
    timestamp: new Date().toISOString()
  };
  
  try {
    // Step 1
    console.log('1. Loading page...');
    await page.goto(`https://www.ricequant.com/quant/create_edit/${strategyId}`, {
      waitUntil: 'domcontentloaded',
      timeout: 30000
    });
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.waitForTimeout(3000);
    
    // Step 2
    console.log('2. Pasting code...');
    const cm = await page.$('.CodeMirror');
    if (cm) {
      await cm.click();
      await page.keyboard.down('Control');
      await page.keyboard.press('a');
      await page.keyboard.up('Control');
      await page.keyboard.press('Backspace');
      await page.waitForTimeout(300);
      await page.evaluate(c => navigator.clipboard.writeText(c), code);
      await page.keyboard.down('Control');
      await page.keyboard.press('v');
      await page.keyboard.up('Control');
      console.log('   Code pasted');
    }
    await page.waitForTimeout(500);
    
    // Step 3
    console.log('3. Setting dates...');
    const startInput = await page.$('input[start]');
    const endInput = await page.$('input[end]');
    if (startInput) await startInput.fill(startDate);
    if (endInput) await endInput.fill(endDate);
    console.log('   Dates:', startDate, '-', endDate);
    await page.waitForTimeout(300);
    
    // Step 4
    console.log('4. Clicking run...');
    const btn = await page.$('button:has-text("运行")') || await page.$('button:has-text("回测")');
    if (btn) {
      await btn.click();
      console.log('   Run clicked');
    }
    
    // Step 5
    console.log('\n5. Waiting for results (max 5 min)...\n');
    const start = Date.now();
    let done = false;
    
    while (!done && (Date.now() - start) < 300000) {
      await page.waitForTimeout(3000);
      try {
        const txt = await page.evaluate(() => document.body?.innerText || '');
        if (txt.includes('年化收益') || txt.includes('总收益')) {
          done = true;
          console.log('   ✓ Results found!\n');
        }
        const s = Math.floor((Date.now() - start) / 1000);
        if (s % 30 === 0) console.log(`   [${s}s]`);
      } catch (e) {
        done = true;
      }
    }
    
    // Step 6
    console.log('6. Saving...');
    await page.waitForTimeout(2000);
    
    const ts = Date.now();
    const shot = path.join(OUTPUT_DIR, `result-${ts}.png`);
    await page.screenshot({ path: shot, fullPage: true });
    console.log('   Screenshot:', shot);
    
    const txt = await page.evaluate(() => document.body?.innerText || '');
    const txtFile = path.join(OUTPUT_DIR, `result-${ts}.txt`);
    fs.writeFileSync(txtFile, txt);
    console.log('   Text:', txtFile);
    
    // Extract metrics
    const ext = (p) => { const m = txt.match(p); return m ? m[1] : null; };
    resultData.metrics = {
      annualReturn: ext(/年化收益[率]*[：:\s]*([-\d.]+%?)/),
      totalReturn: ext(/总收益[率]*[：:\s]*([-\d.]+%?)/),
      maxDrawdown: ext(/最大回撤[：:\s]*([-\d.]+%?)/),
      sharpe: ext(/夏普[比率]*[：:\s]*([-\d.]+)/),
      winRate: ext(/胜率[：:\s]*([-\d.]+%?)/)
    };
    resultData.screenshot = shot;
    
    const jsonFile = path.join(OUTPUT_DIR, `result-${ts}.json`);
    fs.writeFileSync(jsonFile, JSON.stringify(resultData, null, 2));
    console.log('   JSON:', jsonFile);
    
    // Print results
    console.log('\n' + '='.repeat(60));
    console.log('RESULTS');
    console.log('='.repeat(60));
    if (resultData.metrics.annualReturn) console.log('Annual Return:', resultData.metrics.annualReturn);
    if (resultData.metrics.totalReturn) console.log('Total Return:', resultData.metrics.totalReturn);
    if (resultData.metrics.maxDrawdown) console.log('Max Drawdown:', resultData.metrics.maxDrawdown);
    if (resultData.metrics.sharpe) console.log('Sharpe:', resultData.metrics.sharpe);
    if (resultData.metrics.winRate) console.log('Win Rate:', resultData.metrics.winRate);
    console.log('='.repeat(60));
    
    return resultData;
    
  } catch (e) {
    console.error('Error:', e.message);
    resultData.error = e.message;
    return resultData;
  } finally {
    console.log('\nClosing browser...');
    await page.waitForTimeout(process.env.BROWSER_CLOSE_DELAY ? parseInt(process.env.BROWSER_CLOSE_DELAY) : 2000);
    try { await browser.close(); } catch (e) { console.error('Browser close error:', e.message); }
  }
}

const args = process.argv.slice(2);
if (args.length < 2) {
  console.log('Usage: node final-run.js <strategyId> <codeFile> [startDate] [endDate]');
  process.exit(0);
}

runBacktest(args[0], args[1], args[2] || '2021-01-01', args[3] || '2025-03-28')
  .then(r => console.log(r.error ? '\n❌ Failed' : '\n✓ Done'));
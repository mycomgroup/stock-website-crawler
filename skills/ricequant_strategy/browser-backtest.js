import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const AUTH_STATE_FILE = path.join(__dirname, 'data', 'auth-state.json');
const OUTPUT_DIR = path.join(__dirname, 'data');

async function runBacktest(strategyId, codeFile, options = {}) {
  const { startDate = '2021-01-01', endDate = '2025-03-28', capital = 100000 } = options;
  
  const code = fs.readFileSync(codeFile, 'utf8');
  const strategyName = path.basename(codeFile, '.py');
  
  console.log('\n' + '='.repeat(60));
  console.log('RiceQuant Backtest Runner (Browser Mode)');
  console.log('='.repeat(60));
  console.log('Strategy:', strategyName);
  console.log('ID:', strategyId);
  console.log('Period:', startDate, '-', endDate);
  console.log('='.repeat(60) + '\n');
  
  const state = JSON.parse(fs.readFileSync(AUTH_STATE_FILE, 'utf8'));
  
  const browser = await chromium.launch({ 
    headless: false,
    slowMo: 30
  });
  
  const context = await browser.newContext({
    storageState: state,
    viewport: { width: 1400, height: 900 }
  });
  
  const page = await context.newPage();
  
  let result = null;
  
  try {
    // 1. 导航到策略页面
    console.log('1. Opening strategy editor...');
    await page.goto(`https://www.ricequant.com/quant/create_edit/${strategyId}`, { 
      waitUntil: 'networkidle',
      timeout: 30000
    });
    await page.waitForTimeout(2000);
    
    // 2. 替换代码
    console.log('2. Replacing code...');
    
    await page.keyboard.press('Control+a');
    await page.waitForTimeout(200);
    
    await page.evaluate(c => navigator.clipboard.writeText(c), code);
    await page.waitForTimeout(200);
    await page.keyboard.press('Control+v');
    await page.waitForTimeout(500);
    
    // 3. 设置回测参数
    console.log('3. Setting parameters...');
    
    try {
      await page.click('input[start]');
      await page.waitForTimeout(200);
      await page.keyboard.press('Control+a');
      await page.keyboard.type(startDate);
      await page.keyboard.press('Enter');
      console.log('   Start date set:', startDate);
    } catch (e) {}
    
    await page.waitForTimeout(300);
    
    try {
      await page.click('input[end]');
      await page.waitForTimeout(200);
      await page.keyboard.press('Control+a');
      await page.keyboard.type(endDate);
      await page.keyboard.press('Enter');
      console.log('   End date set:', endDate);
    } catch (e) {}
    
    // 4. 点击运行回测
    console.log('4. Running backtest...');
    await page.waitForTimeout(500);
    
    const runBtn = await page.$('button:has-text("运行")') || 
                   await page.$('button:has-text("回测")');
    
    if (runBtn) {
      await runBtn.click();
      console.log('   Clicked run button');
    }
    
    // 5. 等待回测完成
    console.log('\n5. Waiting for backtest...');
    console.log('   (This may take 1-3 minutes)\n');
    
    let completed = false;
    let attempts = 0;
    const maxAttempts = 120;
    
    while (!completed && attempts < maxAttempts) {
      await page.waitForTimeout(3000);
      attempts++;
      
      const pageContent = await page.content();
      
      if (pageContent.includes('年化收益') || 
          pageContent.includes('最大回撤') ||
          pageContent.includes('回测结果')) {
        completed = true;
        console.log('\n   ✓ Backtest completed!');
      }
      
      if (attempts % 10 === 0) {
        process.stdout.write(`   [${attempts}/${maxAttempts}] Waiting...\r`);
      }
    }
    
    // 6. 提取结果
    if (completed) {
      console.log('\n6. Extracting results...');
      
      await page.waitForTimeout(2000);
      
      const screenshotPath = path.join(OUTPUT_DIR, `backtest-${strategyId}-${Date.now()}.png`);
      await page.screenshot({ path: screenshotPath, fullPage: true });
      console.log('   Screenshot:', screenshotPath);
      
      result = await page.evaluate(() => {
        const findValue = (keywords) => {
          const elements = document.querySelectorAll('td, span, div, p');
          for (const el of elements) {
            const text = el.textContent || '';
            for (const keyword of keywords) {
              if (text.includes(keyword)) {
                const next = el.nextElementSibling || el.parentElement?.nextElementSibling;
                if (next) {
                  const value = next.textContent?.trim();
                  if (value && !isNaN(parseFloat(value))) {
                    return value;
                  }
                }
              }
            }
          }
          return null;
        };
        
        return {
          annualReturn: findValue(['年化收益', '年化']),
          totalReturn: findValue(['总收益', '总收益率']),
          maxDrawdown: findValue(['最大回撤']),
          sharpe: findValue(['夏普']),
          winRate: findValue(['胜率']),
          trades: findValue(['交易次数', '交易'])
        };
      });
      
      console.log('\n' + '='.repeat(60));
      console.log('Backtest Results');
      console.log('='.repeat(60));
      
      if (result.annualReturn) console.log('Annual Return:', result.annualReturn);
      if (result.totalReturn) console.log('Total Return:', result.totalReturn);
      if (result.maxDrawdown) console.log('Max Drawdown:', result.maxDrawdown);
      if (result.sharpe) console.log('Sharpe Ratio:', result.sharpe);
      if (result.winRate) console.log('Win Rate:', result.winRate);
      
      console.log('='.repeat(60));
      
      const resultPath = path.join(OUTPUT_DIR, `result-${strategyId}-${Date.now()}.json`);
      fs.writeFileSync(resultPath, JSON.stringify({
        strategyId,
        strategyName,
        startDate,
        endDate,
        capital,
        result,
        screenshot: screenshotPath,
        timestamp: new Date().toISOString()
      }, null, 2));
      console.log('\nResult saved:', resultPath);
      
    } else {
      console.log('\n   ✗ Backtest did not complete in time');
    }
    
  } catch (e) {
    console.error('\nError:', e.message);
  }
  
  console.log('\nClosing browser in 5 seconds...');
  await page.waitForTimeout(5000);
  await browser.close();
  
  return result;
}

const args = process.argv.slice(2);

if (args.length < 2) {
  console.log(`
Usage: node browser-backtest.js <strategyId> <codeFile> [startDate] [endDate]

Examples:
  node browser-backtest.js 2415370 ./strategy.py
  node browser-backtest.js 2415370 ./strategy.py 2023-01-01 2024-12-31
`);
  process.exit(0);
}

runBacktest(args[0], args[1], {
  startDate: args[2] || '2021-01-01',
  endDate: args[3] || '2025-03-28'
});
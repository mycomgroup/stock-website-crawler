import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const AUTH_STATE_FILE = path.join(__dirname, 'data', 'auth-state.json');
const OUTPUT_DIR = path.join(__dirname, 'data');

async function main() {
  const args = process.argv.slice(2);
  const strategyId = args[0] || '2415370';
  const codeFile = args[1];
  const startDate = args[2] || '2021-01-01';
  const endDate = args[3] || '2025-03-28';
  
  console.log('\n' + '='.repeat(60));
  console.log('RiceQuant Backtest - Simple Mode');
  console.log('='.repeat(60));
  console.log('Strategy ID:', strategyId);
  console.log('Period:', startDate, '-', endDate);
  if (codeFile) {
    console.log('Code file:', codeFile);
  }
  console.log('='.repeat(60) + '\n');
  
  const state = JSON.parse(fs.readFileSync(AUTH_STATE_FILE, 'utf8'));
  
  console.log('Launching browser...');
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({ storageState: state });
  const page = await context.newPage();
  
  try {
    // 1. 打开策略页面
    console.log('\n1. Opening strategy page...');
    await page.goto(`https://www.ricequant.com/quant/create_edit/${strategyId}`);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    
    // 2. 如果提供了代码文件，替换代码
    if (codeFile && fs.existsSync(codeFile)) {
      console.log('2. Replacing code...');
      const code = fs.readFileSync(codeFile, 'utf8');
      
      // 点击编辑器
      await page.click('.CodeMirror, .monaco-editor').catch(() => {});
      await page.waitForTimeout(300);
      
      // 全选并粘贴
      await page.keyboard.press('Control+a');
      await page.keyboard.press('Backspace');
      await page.waitForTimeout(300);
      
      await page.evaluate(c => navigator.clipboard.writeText(c), code);
      await page.keyboard.press('Control+v');
      await page.waitForTimeout(500);
      
      console.log('   Code replaced');
    }
    
    // 3. 设置日期
    console.log('3. Setting dates...');
    
    // 点击开始日期输入框
    const startInput = await page.$('input[start]');
    if (startInput) {
      await startInput.fill(startDate);
      console.log('   Start:', startDate);
    }
    
    const endInput = await page.$('input[end]');
    if (endInput) {
      await endInput.fill(endDate);
      console.log('   End:', endDate);
    }
    
    await page.waitForTimeout(500);
    
    // 4. 运行回测
    console.log('\n4. Running backtest...');
    console.log('   Please click "运行回测" button in the browser window.');
    console.log('   Then wait for the backtest to complete.');
    console.log('\n   The script will automatically detect when results appear.');
    console.log('   Or press Ctrl+C when done.\n');
    
    // 等待回测结果页面出现
    // 检测页面变化或新元素
    let resultDetected = false;
    let checkCount = 0;
    const maxChecks = 180; // 最多等待6分钟
    
    while (!resultDetected && checkCount < maxChecks) {
      await page.waitForTimeout(2000);
      checkCount++;
      
      const url = page.url();
      const text = await page.evaluate(() => document.body.innerText).catch(() => '');
      
      // 检查是否有结果
      if (text.includes('年化收益') || 
          text.includes('总收益') ||
          text.includes('夏普') ||
          url.includes('backtest')) {
        resultDetected = true;
        console.log('\n✓ Results detected!');
        break;
      }
      
      if (checkCount % 15 === 0) {
        console.log(`   [${checkCount * 2}s] Still waiting...`);
      }
    }
    
    // 5. 保存结果
    console.log('\n5. Saving results...');
    await page.waitForTimeout(2000);
    
    const timestamp = Date.now();
    const screenshot = path.join(OUTPUT_DIR, `result-${timestamp}.png`);
    await page.screenshot({ path: screenshot, fullPage: true });
    console.log('   Screenshot:', screenshot);
    
    // 提取文本
    const pageText = await page.evaluate(() => document.body.innerText);
    
    // 保存
    const resultFile = path.join(OUTPUT_DIR, `result-${timestamp}.txt`);
    fs.writeFileSync(resultFile, pageText);
    console.log('   Text:', resultFile);
    
    // 提取关键指标
    const extract = (pattern) => {
      const match = pageText.match(pattern);
      return match ? match[1] : null;
    };
    
    console.log('\n' + '='.repeat(60));
    console.log('Results');
    console.log('='.repeat(60));
    
    const annual = extract(/年化收益[率]*[：:\s]*([-\d.]+%?)/);
    const total = extract(/总收益[率]*[：:\s]*([-\d.]+%?)/);
    const maxDD = extract(/最大回撤[：:\s]*([-\d.]+%?)/);
    const sharpe = extract(/夏普[比率]*[：:\s]*([-\d.]+)/);
    
    if (annual) console.log('Annual Return:', annual);
    if (total) console.log('Total Return:', total);
    if (maxDD) console.log('Max Drawdown:', maxDD);
    if (sharpe) console.log('Sharpe:', sharpe);
    
    console.log('='.repeat(60));
    
  } catch (e) {
    console.error('\nError:', e.message);
  }
  
  console.log('\nBrowser will close in 5 seconds...');
  await page.waitForTimeout(5000);
  await browser.close();
  console.log('Done!');
}

main().catch(console.error);
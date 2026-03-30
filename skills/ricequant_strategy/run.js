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
  console.log('Code length:', code.length);
  console.log('='.repeat(60) + '\n');
  
  const state = JSON.parse(fs.readFileSync(AUTH_STATE_FILE, 'utf8'));
  
  const browser = await chromium.launch({ 
    headless: false,
    slowMo: 100,
    args: ['--start-maximized']
  });
  
  const context = await browser.newContext({
    storageState: state,
    viewport: null  // 最大化窗口
  });
  
  const page = await context.newPage();
  
  try {
    // 1. 打开策略编辑页面
    console.log('1. Opening strategy page...');
    await page.goto(`https://www.ricequant.com/quant/create_edit/${strategyId}`, { 
      waitUntil: 'networkidle',
      timeout: 30000
    });
    await page.waitForTimeout(2000);
    
    // 截图初始状态
    await page.screenshot({ path: path.join(OUTPUT_DIR, 'step1-page-loaded.png') });
    
    // 2. 清空编辑器并粘贴代码
    console.log('2. Replacing code in editor...');
    
    // 点击代码编辑区域
    const editorArea = await page.$('.CodeMirror, .monaco-editor, .ace_editor, [class*="editor"]');
    if (editorArea) {
      await editorArea.click();
    }
    
    // 全选
    await page.keyboard.press('Control+a');
    await page.waitForTimeout(300);
    
    // 复制代码到剪贴板
    await page.evaluate(code => navigator.clipboard.writeText(code), code);
    await page.waitForTimeout(200);
    
    // 粘贴
    await page.keyboard.press('Control+v');
    await page.waitForTimeout(1000);
    
    console.log('   Code pasted');
    
    // 3. 设置回测日期
    console.log('3. Setting backtest dates...');
    
    // 点击日期输入区域
    const dateInputs = await page.$$('input[type="text"]');
    for (const input of dateInputs) {
      const placeholder = await input.getAttribute('placeholder');
      const value = await input.inputValue();
      console.log('   Found input:', placeholder, value);
    }
    
    // 尝试设置日期
    const startInput = await page.$('input[start]');
    if (startInput) {
      await startInput.scrollIntoViewIfNeeded();
      await startInput.click();
      await page.waitForTimeout(200);
      await startInput.fill(startDate);
      console.log('   Start date:', startDate);
    }
    
    await page.waitForTimeout(300);
    
    const endInput = await page.$('input[end]');
    if (endInput) {
      await endInput.scrollIntoViewIfNeeded();
      await endInput.click();
      await page.waitForTimeout(200);
      await endInput.fill(endDate);
      console.log('   End date:', endDate);
    }
    
    await page.waitForTimeout(500);
    await page.screenshot({ path: path.join(OUTPUT_DIR, 'step2-before-run.png') });
    
    // 4. 运行回测
    console.log('4. Running backtest...');
    
    // 查找运行按钮
    const runButton = await page.$('button:has-text("运行回测")') ||
                      await page.$('button:has-text("运行")') ||
                      await page.$('[class*="run-btn"]') ||
                      await page.$('[class*="button"][class*="primary"]');
    
    if (runButton) {
      await runButton.scrollIntoViewIfNeeded();
      await runButton.click();
      console.log('   Clicked run button');
    } else {
      // 使用快捷键
      await page.keyboard.press('Control+Enter');
      console.log('   Pressed Ctrl+Enter');
    }
    
    await page.waitForTimeout(2000);
    await page.screenshot({ path: path.join(OUTPUT_DIR, 'step3-after-click.png') });
    
    // 5. 等待回测完成
    console.log('\n5. Waiting for backtest to complete...');
    console.log('   (Please wait, this may take several minutes)\n');
    
    const startTime = Date.now();
    const maxWait = 300000; // 5分钟
    let completed = false;
    let lastStatus = '';
    
    while (!completed && (Date.now() - startTime) < maxWait) {
      await page.waitForTimeout(2000);
      
      // 获取页面内容
      const content = await page.content();
      const text = await page.evaluate(() => document.body.innerText);
      const url = page.url();
      
      // 检查状态
      let status = 'running';
      
      if (text.includes('回测完成') || 
          text.includes('运行完成') ||
          url.includes('backtest')) {
        status = 'completed';
        completed = true;
      } else if (text.includes('运行中') || text.includes('backtest')) {
        status = 'running';
      } else if (text.includes('错误') || text.includes('失败')) {
        status = 'error';
        completed = true;
      }
      
      // 打印状态变化
      if (status !== lastStatus) {
        console.log(`   Status: ${status}`);
        lastStatus = status;
      }
      
      // 每30秒截图
      const elapsed = Math.floor((Date.now() - startTime) / 1000);
      if (elapsed > 0 && elapsed % 30 === 0) {
        await page.screenshot({ path: path.join(OUTPUT_DIR, `progress-${elapsed}s.png`) });
      }
      
      process.stdout.write(`   [${elapsed}s] Waiting...\r`);
    }
    
    // 6. 获取结果
    console.log('\n\n6. Extracting results...');
    
    await page.waitForTimeout(3000);
    
    // 截取最终结果
    const timestamp = Date.now();
    const finalScreenshot = path.join(OUTPUT_DIR, `final-result-${strategyName}-${timestamp}.png`);
    await page.screenshot({ path: finalScreenshot, fullPage: true });
    console.log('   Screenshot saved:', finalScreenshot);
    
    // 提取关键指标
    const pageText = await page.evaluate(() => document.body.innerText);
    
    // 用正则提取
    const extract = (pattern) => {
      const match = pageText.match(pattern);
      return match ? match[1] : null;
    };
    
    const results = {
      annualReturn: extract(/年化收益[率]*[：:\s]*([-\d.]+%?)/),
      totalReturn: extract(/总收益[率]*[：:\s]*([-\d.]+%?)/),
      maxDrawdown: extract(/最大回撤[：:\s]*([-\d.]+%?)/),
      sharpe: extract(/夏普[比率]*[：:\s]*([-\d.]+)/),
      winRate: extract(/胜率[：:\s]*([-\d.]+%?)/),
      alpha: extract(/Alpha[：:\s]*([-\d.]+)/),
      beta: extract(/Beta[：:\s]*([-\d.]+)/)
    };
    
    // 打印结果
    console.log('\n' + '='.repeat(60));
    console.log('BACKTEST RESULTS');
    console.log('='.repeat(60));
    
    let hasResults = false;
    for (const [key, value] of Object.entries(results)) {
      if (value) {
        const label = key.replace(/([A-Z])/g, ' $1').trim();
        console.log(`   ${label}: ${value}`);
        hasResults = true;
      }
    }
    
    if (!hasResults) {
      console.log('   (No metrics extracted - check screenshot)');
    }
    
    console.log('='.repeat(60));
    
    // 保存结果JSON
    const resultData = {
      strategyId,
      strategyName,
      startDate,
      endDate,
      results,
      screenshot: finalScreenshot,
      timestamp: new Date().toISOString()
    };
    
    const jsonPath = path.join(OUTPUT_DIR, `result-${strategyName}-${timestamp}.json`);
    fs.writeFileSync(jsonPath, JSON.stringify(resultData, null, 2));
    console.log('\n   Result JSON:', jsonPath);
    
    // 检查是否有错误
    if (pageText.includes('错误') || pageText.includes('Error') || pageText.includes('失败')) {
      console.log('\n   ⚠ Errors detected in backtest');
      
      // 保存错误信息
      const errorMatch = pageText.match(/错误[：:\s]*([^\n]+)/);
      if (errorMatch) {
        console.log('   Error:', errorMatch[1]);
        resultData.error = errorMatch[1];
        fs.writeFileSync(jsonPath, JSON.stringify(resultData, null, 2));
      }
    }
    
    return resultData;
    
  } catch (e) {
    console.error('\n❌ Error:', e.message);
    
    // 保存错误截图
    try {
      const errorPath = path.join(OUTPUT_DIR, `error-${Date.now()}.png`);
      await page.screenshot({ path: errorPath, fullPage: true });
      console.log('   Error screenshot:', errorPath);
    } catch (e2) {}
    
    return null;
  } finally {
    // 关闭浏览器
    console.log('\nClosing browser in 10 seconds...');
    await page.waitForTimeout(10000);
    
    try {
      await browser.close();
    } catch (e) {}
  }
}

// 主程序
const args = process.argv.slice(2);

if (args.length < 2) {
  console.log('\nUsage: node run.js <strategyId> <codeFile> [startDate] [endDate]');
  console.log('\nExample:');
  console.log('  node run.js 2415370 strategy.py 2021-01-01 2025-03-28\n');
  process.exit(0);
}

runBacktest(
  args[0], 
  args[1], 
  args[2] || '2021-01-01', 
  args[3] || '2025-03-28'
).then(result => {
  if (result) {
    console.log('\n✓ Backtest completed!');
    console.log('Check the screenshot for visual results.');
  } else {
    console.log('\n✗ Backtest failed');
  }
});
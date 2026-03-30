#!/usr/bin/env node
import { chromium } from 'playwright';
import '../load-env.js';
import { SESSION_FILE } from '../paths.js';
import fs from 'node:fs';

const PYTHON_CODE = `
print("测试JQData连接...")
import jqdata
print("JQData可用")

print("\\n测试基础API...")
from jqdata import *
print("API导入成功")

print("\\n获取交易日...")
days = get_trade_days(start_date="2021-01-01", end_date="2021-01-10")
print(f"交易日数: {len(days)}")

print("\\n测试涨停股票...")
zt = []
all_stocks = get_all_securities("stock", "2021-01-05").index.tolist()
all_stocks = [s for s in all_stocks if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))]
df = get_price(all_stocks[:50], end_date="2021-01-05", count=1, fields=["close", "high_limit"], panel=False)
df = df.dropna()
zt_df = df[df["close"] == df["high_limit"]]
zt = list(zt_df["code"])
print(f"涨停股票数: {len(zt)}")

print("\\n基础API测试完成!")
`;

async function runCode() {
  const sessionData = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const notebookUrl = sessionData.notebookUrl;
  
  console.log('打开notebook:', notebookUrl);
  
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  });
  
  const cookies = sessionData.cookies.map(c => ({
    name: c.name,
    value: c.value,
    domain: c.domain,
    path: c.path
  }));
  
  await context.addCookies(cookies);
  const page = await context.newPage();
  
  await page.goto(notebookUrl);
  await page.waitForTimeout(5000);
  
  console.log('等待notebook加载...');
  await page.waitForSelector('.jp-NotebookPanel', { timeout: 30000 });
  
  console.log('创建新cell...');
  await page.keyboard.press('b');
  await page.waitForTimeout(1000);
  
  const codeCell = page.locator('.jp-CodeCell').last();
  await codeCell.click();
  
  console.log('输入代码...');
  await page.keyboard.insertText(PYTHON_CODE);
  await page.waitForTimeout(500);
  
  console.log('执行代码...');
  await page.keyboard.press('Control+Enter');
  await page.waitForTimeout(15000);
  
  const outputArea = codeCell.locator('.jp-OutputArea-output');
  const outputText = await outputArea.textContent().catch(() => '');
  console.log('\\n输出结果:\\n', outputText);
  
  await browser.close();
}

runCode().catch(console.error);
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  
  try {
    const sessionStr = fs.readFileSync(path.join(__dirname, 'data/session.json'), 'utf8');
    const session = JSON.parse(sessionStr);
    if (session.cookies) {
      await context.addCookies(session.cookies);
      console.log('Loaded cookies from thsquant_strategy');
    }
  } catch (e) {
    console.error('No cookies found or failed to load:', e.message);
  }

  const page = await context.newPage();
  
  page.on('response', async (response) => {
    const url = response.url();
    if (url.includes('api') || url.includes('10jqka')) {
      const contentType = response.headers()['content-type'] || '';
      if (contentType.includes('application/json') || contentType.includes('text/html') || url.includes('.json')) {
        console.log(`[Response] ${url}`);
        // Log common API requests for analysis
        if (url.includes('query') || url.includes('filter') || url.includes('backtest') || url.includes('run')) {
            try {
                const req = response.request();
                const method = req.method();
                const postData = req.postData();
                console.log(`-> ${method} ${url}`);
                if (postData) console.log(`-> PostData: ${postData}`);
            } catch(e) {}
        }
      }
    }
  });

  const url = "https://backtest.10jqka.com.cn/backtest/app.html#/strategybacktest?query=%E5%88%9B%E4%B8%9A%E6%9D%BF%EF%BC%8C%E9%9D%9EST%EF%BC%8C%E7%83%AD%E7%82%B9%E6%A6%82%E5%BF%B5%EF%BC%8C%E5%91%A8%E6%88%90%E4%BA%A4%E9%87%8F%E7%8E%AF%E6%AF%94%E5%A2%9E%E9%95%BF%E7%8E%87%E5%A4%A7%E4%BA%8E8%25%EF%BC%8C%E8%BF%913%E5%A4%A9%E7%9A%84%E6%B6%A8%E5%B9%85%E5%A4%A7%E4%BA%8E0%25%E5%B0%8F%E4%BA%8E20%25%EF%BC%8C%E4%B8%8A%E5%B8%82%E6%97%B6%E9%97%B4%E5%A4%A7%E4%BA%8E300%E5%A4%A9%EF%BC%8C%E6%9C%AA%E6%9D%A55%E5%A4%A9%E6%B6%A8%E8%B7%8C%E5%B9%85%E4%BB%8E%E5%A4%A7%E5%88%B0%E5%B0%8F%EF%BC%8C%E9%BE%99%E8%84%8A%E7%BA%BF%E7%99%BE%E5%88%86%E6%AF%94%E7%94%B1%E8%BF%91%E5%88%B0%E8%BF%9C%E3%80%82&daysForSaleStrategy=2,3&startDate=2025-01-01&endDate=2026-04-10&stockHoldCount=2&dayBuyStockNum=2&upperIncome=25&lowerIncome=9&fallIncome=5&engine=undefined&capital=10000000";
  console.log('Navigating to ' + url);
  await page.goto(url, { waitUntil: 'networkidle' });
  
  console.log('Wait 10 seconds...');
  await page.waitForTimeout(10000);
  
  const html = await page.content();
  fs.writeFileSync(path.join(__dirname, 'data/10jqka_backtest_page.html'), html);
  console.log('Saved page html.');
  
  await browser.close();
})();

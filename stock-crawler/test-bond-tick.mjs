import { chromium } from 'playwright';

async function test() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  await page.goto('https://finnhub.io/docs/api/bond-tick', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForSelector('.docs-text', { timeout: 15000 });
  await page.waitForTimeout(3000);
  
  // 找到 Bond Tick Data 的 .docs-text
  const result = await page.evaluate(() => {
    const allDocTexts = document.querySelectorAll('.docs-text');
    for (const docText of allDocTexts) {
      const text = docText.innerText;
      const firstLine = text.split('\n')[0].trim().toLowerCase();
      if (firstLine === 'bond tick data' || firstLine.includes('bond') && firstLine.includes('tick')) {
        return {
          title: text.split('\n')[0].trim(),
          content: text
        };
      }
    }
    return null;
  });
  
  console.log('Found content:');
  console.log('='.repeat(60));
  console.log(result?.content || 'Not found');
  
  await browser.close();
}

test().catch(console.error);

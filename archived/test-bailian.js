import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  page.on('response', async (res) => {
    const url = res.url();
    if (url.includes('mcp-server') || url.includes('aliyun')) {
      if (res.request().resourceType() === 'xhr' || res.request().resourceType() === 'fetch') {
        console.log('API:', url);
      }
    }
  });

  await page.goto('https://bailian.console.aliyun.com/cn-beijing/?tab=mcp#/mcp-market/detail/code_interpreter_mcp');
  await page.waitForTimeout(5000);
  
  const content = await page.evaluate(() => {
    return {
      provider: document.querySelector('.provider')?.textContent || document.body.innerText.match(/由\s*(.*?)\s*提供/)?.[1],
      innerText: document.body.innerText.substring(0, 1000)
    };
  });
  console.log(content);
  
  await browser.close();
})();

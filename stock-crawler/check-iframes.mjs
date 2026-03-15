import { chromium } from 'playwright';

async function inspectPage() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto('https://site.financialmodelingprep.com/developer/docs', { waitUntil: 'networkidle' });
  await page.waitForTimeout(5000);
  
  // Check for iframes
  const frames = page.frames();
  console.log('Number of frames:', frames.length);
  
  for (let i = 0; i < frames.length; i++) {
    const frame = frames[i];
    const url = frame.url();
    console.log(`\nFrame ${i}: ${url}`);
    
    try {
      const content = await frame.evaluate(() => {
        return {
          title: document.title,
          hasTable: !!document.querySelector('table'),
          hasPre: !!document.querySelector('pre'),
          bodyText: document.body?.textContent?.substring(0, 200)
        };
      });
      console.log('Content:', content);
    } catch (e) {
      console.log('Error accessing frame:', e.message);
    }
  }
  
  // Also check shadow roots
  const shadowInfo = await page.evaluate(() => {
    const elementsWithShadow = Array.from(document.querySelectorAll('*')).filter(el => el.shadowRoot);
    return elementsWithShadow.map(el => ({
      tag: el.tagName,
      className: el.className,
      shadowChildren: el.shadowRoot?.children?.length
    }));
  });
  
  console.log('\n=== Shadow DOM Elements ===');
  console.log(shadowInfo);
  
  await browser.close();
}

inspectPage();

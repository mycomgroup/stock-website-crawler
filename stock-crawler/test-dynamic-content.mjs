import { chromium } from 'playwright';

async function testPage() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto('https://site.financialmodelingprep.com/developer/docs', { waitUntil: 'domcontentloaded' });
  
  // Scroll to trigger content
  await page.evaluate(() => window.scrollTo(0, 1000));
  await page.waitForTimeout(3000);
  
  // Check for dynamic content every second for 10 seconds
  for (let i = 0; i < 10; i++) {
    const content = await page.evaluate(() => {
      const blocks = document.querySelectorAll('[class*="responsePlaceBlock"]');
      let hasContent = false;
      let contentSample = '';
      
      blocks.forEach(block => {
        const text = block.textContent?.trim();
        if (text && text.length > 10) {
          hasContent = true;
          contentSample = text.substring(0, 200);
        }
      });
      
      // Also check for any table elements
      const tables = document.querySelectorAll('table');
      
      return {
        hasContent,
        contentSample,
        tableCount: tables.length,
        blockCount: blocks.length
      };
    });
    
    console.log(`Check ${i + 1}: hasContent=${content.hasContent}, tables=${content.tableCount}, blocks=${content.blockCount}`);
    if (content.hasContent) {
      console.log('Content sample:', content.contentSample);
    }
    
    await page.waitForTimeout(1000);
  }
  
  await browser.close();
}

testPage();

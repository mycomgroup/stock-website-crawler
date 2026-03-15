import { chromium } from 'playwright';

async function inspectPage() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto('https://site.financialmodelingprep.com/developer/docs', { waitUntil: 'networkidle' });
  await page.waitForTimeout(10000);
  
  // Scroll down to trigger lazy loading
  await page.evaluate(() => window.scrollTo(0, 1000));
  await page.waitForTimeout(3000);
  
  // Check what's inside the responsePlaceBlock
  const content = await page.evaluate(() => {
    const blocks = document.querySelectorAll('[class*="responsePlaceBlock"]');
    const results = [];
    
    blocks.forEach((block, i) => {
      if (i < 3) {
        results.push({
          index: i,
          outerHTML: block.outerHTML.substring(0, 1000),
          innerHTML: block.innerHTML.substring(0, 1000),
          childText: Array.from(block.querySelectorAll('*')).map(el => el.textContent?.substring(0, 50)).filter(t => t && t.length > 5).slice(0, 10)
        });
      }
    });
    
    // Also check for any table-like structures
    const allText = document.body.textContent;
    const hasParamTable = allText.includes('Query Parameter') || allText.includes('query*');
    const hasResponse = allText.includes('"symbol"') && allText.includes('Apple');
    
    return { blocks: results, hasParamTable, hasResponse };
  });
  
  console.log('=== Response Blocks ===');
  content.blocks.forEach(b => {
    console.log(`\nBlock ${b.index}:`);
    console.log('Outer HTML:', b.outerHTML.substring(0, 200));
    console.log('Child text:', b.childText);
  });
  
  console.log('\n=== Has Content ===');
  console.log('Has param table:', content.hasParamTable);
  console.log('Has response:', content.hasResponse);
  
  await browser.close();
}

inspectPage();

import { chromium } from 'playwright';

async function inspectPage() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto('https://site.financialmodelingprep.com/developer/docs', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(8000);
  
  // Get the full HTML of a small section
  const html = await page.evaluate(() => {
    const wrapper = document.querySelector('[class*="documentationWrapper"]');
    if (!wrapper) return 'wrapper not found';
    
    // Find first API section
    const apiSection = Array.from(wrapper.children).find(child => 
      child.tagName === 'DIV' && 
      !child.className && 
      child.children.length > 40
    );
    
    if (!apiSection) return 'API section not found';
    
    // Get the first few API items (Symbol Search)
    const children = Array.from(apiSection.children).slice(0, 12);
    return children.map(child => child.outerHTML).join('\n---CHILD---\n');
  });
  
  console.log(html.substring(0, 5000));
  
  await browser.close();
}

inspectPage();

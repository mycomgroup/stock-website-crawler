import { chromium } from 'playwright';

async function inspectPage() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto('https://site.financialmodelingprep.com/developer/docs', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(5000);
  
  // Get the page structure
  const structure = await page.evaluate(() => {
    // Find all headings
    const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4')).map(h => ({
      tag: h.tagName,
      text: h.textContent.trim().substring(0, 50),
      className: h.className,
      parent: h.parentElement?.className || ''
    }));
    
    // Find main content containers
    const mainContainers = Array.from(document.querySelectorAll('main, [class*="main"], [class*="content"], [class*="doc"]')).map(el => ({
      tag: el.tagName,
      className: el.className,
      id: el.id,
      childCount: el.children.length
    }));
    
    return { headings, mainContainers };
  });
  
  console.log('=== Headings ===');
  structure.headings.slice(0, 20).forEach(h => console.log(`${h.tag}: "${h.text}" (parent: ${h.parent})`));
  
  console.log('\n=== Main Containers ===');
  structure.mainContainers.forEach(c => console.log(`${c.tag}.${c.className} (children: ${c.childCount})`));
  
  await browser.close();
}

inspectPage();

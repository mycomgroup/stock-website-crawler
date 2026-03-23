import { chromium } from 'playwright';

async function inspectPage() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto('https://site.financialmodelingprep.com/developer/docs', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(5000);
  
  // Get the structure of a single API section
  const structure = await page.evaluate(() => {
    const wrapper = document.querySelector('[class*="documentationWrapper"]');
    if (!wrapper) return { error: 'wrapper not found' };
    
    // Find the first API section div (the one with 44 children - Company Search)
    const apiSection = Array.from(wrapper.children).find(child => 
      child.tagName === 'DIV' && 
      !child.className && 
      child.children.length > 40
    );
    
    if (!apiSection) return { error: 'API section not found' };
    
    // Get the structure of this section
    const children = Array.from(apiSection.children).slice(0, 25).map(child => ({
      tag: child.tagName,
      className: child.className?.split(' ')[0] || '',
      text: child.textContent?.substring(0, 80).trim(),
      childCount: child.children.length
    }));
    
    // Find pre/code or similar elements
    const codeElements = Array.from(apiSection.querySelectorAll('pre, code, [class*="code"], [class*="Code"]')).map(el => ({
      tag: el.tagName,
      className: el.className,
      text: el.textContent?.substring(0, 100)
    }));
    
    return { children, codeElements };
  });
  
  console.log('=== API Section Children ===');
  structure.children?.forEach((c, i) => {
    console.log(`${i}. ${c.tag}.${c.className} (${c.childCount} children): "${c.text?.substring(0, 60)}..."`);
  });
  
  console.log('\n=== Code Elements ===');
  structure.codeElements?.forEach((c, i) => {
    console.log(`${i}. ${c.tag}.${c.className}: "${c.text?.substring(0, 60)}"`);
  });
  
  await browser.close();
}

inspectPage();

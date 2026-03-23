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
    
    // Find the first API section (after Authorization)
    const sections = [];
    let current = wrapper.firstElementChild;
    let depth = 0;
    
    // Walk through direct children
    const children = Array.from(wrapper.children);
    for (const child of children.slice(0, 30)) {
      sections.push({
        tag: child.tagName,
        className: child.className,
        text: child.textContent.substring(0, 100).trim(),
        childCount: child.children.length
      });
    }
    
    // Find elements that might contain parameters
    const paramLike = Array.from(wrapper.querySelectorAll('[class*="param"], [class*="Param"], [class*="query"]')).map(el => ({
      tag: el.tagName,
      className: el.className,
      text: el.textContent.substring(0, 100)
    }));
    
    // Find response-like elements
    const responseLike = Array.from(wrapper.querySelectorAll('[class*="response"], [class*="Response"], [class*="code"]')).map(el => ({
      tag: el.tagName,
      className: el.className,
      text: el.textContent.substring(0, 100)
    }));
    
    return { sections, paramLike, responseLike };
  });
  
  console.log('=== First 30 sections ===');
  structure.sections?.forEach((s, i) => {
    console.log(`${i}. ${s.tag}.${s.className?.split(' ')[0] || ''} (${s.childCount} children): "${s.text?.substring(0, 50)}..."`);
  });
  
  console.log('\n=== Parameter-like elements ===');
  structure.paramLike?.slice(0, 5).forEach(p => console.log(`${p.tag}.${p.className}: "${p.text?.substring(0, 50)}"`));
  
  console.log('\n=== Response-like elements ===');
  structure.responseLike?.slice(0, 5).forEach(r => console.log(`${r.tag}.${r.className}: "${r.text?.substring(0, 50)}"`));
  
  await browser.close();
}

inspectPage();

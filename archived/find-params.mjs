import { chromium } from 'playwright';

async function inspectPage() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto('https://site.financialmodelingprep.com/developer/docs', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(5000);
  
  // Find elements containing parameter data
  const structure = await page.evaluate(() => {
    const wrapper = document.querySelector('[class*="documentationWrapper"]');
    if (!wrapper) return { error: 'wrapper not found' };
    
    // Find elements containing "query*stringAAPL"
    const allElements = Array.from(wrapper.querySelectorAll('*'));
    
    const paramElements = allElements.filter(el => {
      const text = el.textContent || '';
      return text.includes('query*') && text.includes('AAPL') && el.children.length === 0;
    }).map(el => ({
      tag: el.tagName,
      className: el.className,
      text: el.textContent
    }));
    
    // Find parent of these elements
    const parentElements = allElements.filter(el => {
      const text = el.textContent || '';
      return text.includes('query*') && text.includes('AAPL') && el.children.length > 0 && el.children.length < 20;
    }).map(el => ({
      tag: el.tagName,
      className: el.className,
      childCount: el.children.length,
      firstChild: el.firstElementChild ? {
        tag: el.firstElementChild.tagName,
        className: el.firstElementChild.className,
        text: el.firstElementChild.textContent?.substring(0, 30)
      } : null,
      children: Array.from(el.children).slice(0, 10).map(c => ({
        tag: c.tagName,
        className: c.className?.split(' ')[0],
        text: c.textContent?.substring(0, 20)
      }))
    }));
    
    // Find the response JSON
    const jsonElements = allElements.filter(el => {
      const text = el.textContent || '';
      return text.includes('"symbol"') && text.includes('"Apple"') && el.children.length === 0;
    }).map(el => ({
      tag: el.tagName,
      className: el.className,
      text: el.textContent?.substring(0, 200)
    }));
    
    return { paramElements, parentElements, jsonElements };
  });
  
  console.log('=== Parameter Elements (leaf) ===');
  structure.paramElements?.slice(0, 3).forEach(p => console.log(`${p.tag}.${p.className}: "${p.text}"`));
  
  console.log('\n=== Parameter Parent Elements ===');
  structure.parentElements?.slice(0, 3).forEach(p => {
    console.log(`${p.tag}.${p.className} (${p.childCount} children):`);
    p.children?.forEach(c => console.log(`  - ${c.tag}.${c.className}: "${c.text}"`));
  });
  
  console.log('\n=== JSON Elements ===');
  structure.jsonElements?.slice(0, 2).forEach(j => console.log(`${j.tag}.${j.className}: "${j.text?.substring(0, 100)}"`));
  
  await browser.close();
}

inspectPage();

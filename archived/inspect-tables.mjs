import { chromium } from 'playwright';

async function inspectPage() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto('https://site.financialmodelingprep.com/developer/docs', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(5000);
  
  // Get table and code structure
  const structure = await page.evaluate(() => {
    const wrapper = document.querySelector('[class*="documentationWrapper"]');
    if (!wrapper) return { error: 'wrapper not found' };
    
    // Find tables
    const tables = Array.from(wrapper.querySelectorAll('table')).map(t => ({
      rows: t.querySelectorAll('tr').length,
      html: t.outerHTML.substring(0, 500)
    }));
    
    // Find code/pre elements
    const codeBlocks = Array.from(wrapper.querySelectorAll('pre, code')).map(c => ({
      tag: c.tagName,
      text: c.textContent.substring(0, 100),
      className: c.className
    }));
    
    // Find elements that look like response examples
    const jsonLike = Array.from(wrapper.querySelectorAll('*')).filter(el => {
      const text = el.textContent || '';
      return text.includes('[') && text.includes('"symbol"') && text.length < 500;
    }).map(el => ({
      tag: el.tagName,
      className: el.className,
      text: el.textContent.substring(0, 200)
    }));
    
    return { tables, codeBlocks, jsonLike };
  });
  
  console.log('=== Tables ===');
  structure.tables?.forEach((t, i) => {
    console.log(`\nTable ${i + 1} (${t.rows} rows):`);
    console.log(t.html);
  });
  
  console.log('\n=== Code Blocks ===');
  structure.codeBlocks?.forEach((c, i) => {
    console.log(`${i + 1}. ${c.tag}: "${c.text}..." (class: ${c.className})`);
  });
  
  console.log('\n=== JSON-like elements ===');
  structure.jsonLike?.slice(0, 3).forEach((j, i) => {
    console.log(`${i + 1}. ${j.tag}.${j.className}: "${j.text}..."`);
  });
  
  await browser.close();
}

inspectPage();

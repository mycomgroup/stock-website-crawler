import { chromium } from 'playwright';

async function debug() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto('https://site.financialmodelingprep.com/developer/docs', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(5000);
  
  const info = await page.evaluate(() => {
    const wrapper = document.querySelector('[class*="documentationWrapper"]');
    if (!wrapper) return 'no wrapper';
    
    const children = Array.from(wrapper.children);
    
    // Count elements
    const counts = {
      total: children.length,
      h1: children.filter(c => c.tagName === 'H1').length,
      h2: children.filter(c => c.tagName === 'H2').length,
      h3: children.filter(c => c.tagName === 'H3').length,
      h4: children.filter(c => c.tagName === 'H4').length,
      p: children.filter(c => c.tagName === 'P').length,
      div: children.filter(c => c.tagName === 'DIV').length
    };
    
    // Get H2 texts
    const h2Texts = children.filter(c => c.tagName === 'H2').map(c => c.textContent.trim().substring(0, 50));
    
    // Get first 20 children
    const first20 = children.slice(0, 20).map(c => ({
      tag: c.tagName,
      class: (c.className || '').split(' ')[0],
      text: c.textContent?.substring(0, 40).trim()
    }));
    
    return { counts, h2Texts, first20 };
  });
  
  console.log('Counts:', info.counts);
  console.log('H2 texts:', info.h2Texts);
  console.log('First 20 children:');
  info.first20?.forEach((c, i) => console.log(`  ${i}. ${c.tag}.${c.class}: "${c.text}"`));
  
  await browser.close();
}

debug();

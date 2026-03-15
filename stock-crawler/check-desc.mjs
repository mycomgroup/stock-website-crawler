import { chromium } from 'playwright';

async function check() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto('https://site.financialmodelingprep.com/developer/docs', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(5000);
  
  const info = await page.evaluate(() => {
    const wrapper = document.querySelector('[class*="documentationWrapper"]');
    const children = Array.from(wrapper.children);
    
    // Find Company Search section (first div without class)
    const companySearchDiv = children.find(c => 
      c.tagName === 'DIV' && 
      !c.className && 
      c.textContent.includes('Company Search')
    );
    
    if (!companySearchDiv) return 'Company Search div not found';
    
    // Get structure of first few children
    const apiChildren = Array.from(companySearchDiv.children).slice(0, 15);
    
    return apiChildren.map(c => ({
      tag: c.tagName,
      class: (c.className || '').split(' ').slice(0, 2).join(' '),
      text: c.textContent?.substring(0, 60).trim()
    }));
  });
  
  console.log('Company Search children:');
  info.forEach((c, i) => console.log(`  ${i}. ${c.tag}.${c.class}: "${c.text}"`));
  
  await browser.close();
}

check();

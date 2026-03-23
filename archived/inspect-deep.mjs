import { chromium } from 'playwright';

async function inspectPage() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto('https://site.financialmodelingprep.com/developer/docs', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(5000);
  
  // Deep inspection of endpoint and parameters
  const structure = await page.evaluate(() => {
    const wrapper = document.querySelector('[class*="documentationWrapper"]');
    if (!wrapper) return { error: 'wrapper not found' };
    
    // Find the first API section div
    const apiSection = Array.from(wrapper.children).find(child => 
      child.tagName === 'DIV' && 
      !child.className && 
      child.children.length > 40
    );
    
    if (!apiSection) return { error: 'API section not found' };
    
    // Find the endpoint div (has 2 children, starts with "Endpoint:")
    const endpointDiv = Array.from(apiSection.children).find(child => 
      child.textContent?.startsWith('Endpoint:') && child.children.length === 2
    );
    
    // Find parameter container
    const paramsIndex = Array.from(apiSection.children).findIndex(child => 
      child.tagName === 'P' && child.textContent === 'Parameters'
    );
    
    let paramContainer = null;
    let responseContainer = null;
    
    if (paramsIndex >= 0) {
      // The next div after "Parameters" should contain the parameter table
      paramContainer = apiSection.children[paramsIndex + 1];
      
      // Look for response section
      for (let i = paramsIndex + 1; i < Math.min(paramsIndex + 10, apiSection.children.length); i++) {
        const el = apiSection.children[i];
        if (el.textContent?.includes('Response') || el.querySelector('[class*="response"]')) {
          responseContainer = el;
          break;
        }
      }
    }
    
    const inspectElement = (el, depth = 0) => {
      if (!el) return null;
      const indent = '  '.repeat(depth);
      const result = {
        tag: el.tagName,
        className: el.className?.split(' ')[0] || '',
        text: el.textContent?.substring(0, 50).trim(),
        children: []
      };
      
      if (depth < 3) {
        Array.from(el.children).forEach(child => {
          result.children.push(inspectElement(child, depth + 1));
        });
      }
      
      return result;
    };
    
    return {
      endpoint: inspectElement(endpointDiv),
      params: inspectElement(paramContainer),
      response: inspectElement(responseContainer)
    };
  });
  
  console.log('=== Endpoint Structure ===');
  console.log(JSON.stringify(structure.endpoint, null, 2));
  
  console.log('\n=== Parameters Structure ===');
  console.log(JSON.stringify(structure.params, null, 2));
  
  console.log('\n=== Response Structure ===');
  console.log(JSON.stringify(structure.response, null, 2));
  
  await browser.close();
}

inspectPage();

import { chromium } from 'playwright';

async function testPage() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto('https://site.financialmodelingprep.com/developer/docs', { waitUntil: 'networkidle' });
  await page.waitForTimeout(5000);
  
  // Check for canvas elements
  const canvasInfo = await page.evaluate(() => {
    const canvases = document.querySelectorAll('canvas');
    return {
      canvasCount: canvases.length,
      canvasSizes: Array.from(canvases).map(c => ({ width: c.width, height: c.height }))
    };
  });
  console.log('Canvas info:', canvasInfo);
  
  // Check for any data attributes
  const dataAttrs = await page.evaluate(() => {
    const elementsWithData = document.querySelectorAll('[data-params], [data-endpoint], [data-response]');
    return Array.from(elementsWithData).map(el => ({
      tag: el.tagName,
      data: Object.keys(el.dataset)
    }));
  });
  console.log('Elements with data attrs:', dataAttrs);
  
  // Check React fiber
  const reactInfo = await page.evaluate(() => {
    const root = document.getElementById('__next');
    if (!root) return 'No __next root';
    
    const fiberKey = Object.keys(root).find(k => k.startsWith('__reactFiber'));
    if (!fiberKey) return 'No React fiber found';
    
    return 'React fiber found: ' + fiberKey;
  });
  console.log('React info:', reactInfo);
  
  // Check if there's any global state
  const globalState = await page.evaluate(() => {
    const windowKeys = Object.keys(window).filter(k => 
      k.includes('state') || 
      k.includes('data') || 
      k.includes('store') ||
      k.includes('redux') ||
      k.includes('__')
    );
    return windowKeys.slice(0, 10);
  });
  console.log('Global state keys:', globalState);
  
  await browser.close();
}

testPage();

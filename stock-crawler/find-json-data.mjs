import { chromium } from 'playwright';

async function inspectPage() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto('https://site.financialmodelingprep.com/developer/docs', { waitUntil: 'networkidle' });
  await page.waitForTimeout(5000);
  
  // Check for embedded JSON data (Next.js uses __NEXT_DATA__)
  const jsonData = await page.evaluate(() => {
    const nextData = document.getElementById('__NEXT_DATA__');
    if (nextData) {
      const data = JSON.parse(nextData.textContent);
      return {
        type: 'NEXT_DATA',
        keys: Object.keys(data.props?.pageProps || {}),
        preview: JSON.stringify(data.props?.pageProps || {}).substring(0, 1000)
      };
    }
    
    // Check for other script tags with JSON
    const scripts = Array.from(document.querySelectorAll('script')).filter(s => 
      s.textContent.includes('query') || 
      s.textContent.includes('endpoint') ||
      s.textContent.includes('parameter')
    ).map(s => ({
      content: s.textContent.substring(0, 500)
    }));
    
    return { type: 'scripts', scripts };
  });
  
  console.log('=== JSON Data ===');
  console.log(JSON.stringify(jsonData, null, 2));
  
  await browser.close();
}

inspectPage();

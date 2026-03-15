// Script to inspect Mintlify DOM structure for parameter extraction
import { chromium } from 'playwright';

async function inspectPage(url) {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  console.log(`Loading ${url}...`);
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);

  // Find parameter-like elements
  const paramInfo = await page.evaluate(() => {
    const results = [];

    // Look for code elements that might be parameter names
    const codeElements = document.querySelectorAll('code');
    codeElements.forEach(code => {
      const parent = code.parentElement;
      const grandParent = parent?.parentElement;
      const classList = (parent?.className || '').toString();
      const gpClassList = (grandParent?.className || '').toString();

      // Check if this looks like a parameter name
      const text = code.textContent.trim();
      if (text.length > 0 && text.length < 50 && !text.includes(' ')) {
        // Get surrounding text
        const parentText = parent?.textContent?.trim() || '';
        const gpText = grandParent?.textContent?.trim() || '';

        // Check for common parameter name patterns
        const isParamLike =
          classList.includes('param') ||
          gpClassList.includes('param') ||
          classList.includes('property') ||
          gpClassList.includes('property') ||
          classList.includes('field') ||
          (parentText.includes(text) && parentText.length < 500);

        if (isParamLike) {
          results.push({
            name: text,
            parentClass: classList.substring(0, 100),
            gpClass: gpClassList.substring(0, 100),
            description: parentText.substring(0, 200)
          });
        }
      }
    });

    // Look for elements with param-related classes
    const paramElements = document.querySelectorAll('[class*="param"], [class*="property"], [class*="field"]');
    paramElements.forEach(el => {
      const code = el.querySelector('code');
      if (code) {
        results.push({
          name: code.textContent.trim(),
          parentClass: (el.className || '').toString().substring(0, 100),
          description: el.textContent.trim().substring(0, 300)
        });
      }
    });

    // Look for specific Mintlify structures
    // Mintlify uses divs with specific patterns
    const divs = document.querySelectorAll('div');
    divs.forEach(div => {
      const classList = (div.className || '').toString();
      const firstCode = div.querySelector(':scope > code, :scope > span > code, :scope > strong > code');
      if (firstCode && classList.length > 0) {
        const codeText = firstCode.textContent.trim();
        const divText = div.textContent.trim();
        // Check if this looks like a parameter block
        if (codeText.length < 50 && !codeText.includes(' ') && divText.length > 20 && divText.length < 500) {
          results.push({
            type: 'div-with-code',
            name: codeText,
            class: classList.substring(0, 100),
            description: divText.substring(0, 300)
          });
        }
      }
    });

    return results;
  });

  console.log('\n=== Parameter Elements Found ===');
  paramInfo.forEach((p, i) => {
    console.log(`\n${i + 1}. Name: "${p.name}"`);
    if (p.parentClass) console.log(`   Parent Class: ${p.parentClass}`);
    if (p.class) console.log(`   Class: ${p.class}`);
    if (p.description) console.log(`   Description: ${p.description.substring(0, 150)}...`);
  });

  await browser.close();
}

const url = process.argv[2] || 'https://docs.tavily.com/documentation/api-reference/endpoint/search';
inspectPage(url);
import { chromium } from 'playwright';

async function inspectPage() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  const url = 'https://docs.tavily.com/documentation/api-reference/endpoint/search';
  console.log(`Loading ${url}...`);
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(5000);

  // Inspect primitive-param-field structure
  const paramInfo = await page.evaluate(() => {
    const results = [];

    // Check primitive-param-field elements
    const paramFields = document.querySelectorAll('[class*="primitive-param-field"]');
    console.log('Found param fields:', paramFields.length);

    paramFields.forEach((field, idx) => {
      if (idx < 8) { // First 8 only
        const classList = (field.className || '').toString();

        // Find code elements
        const codes = field.querySelectorAll('code');
        const codeTexts = Array.from(codes).map(c => c.textContent);

        // Find specific elements
        const firstCode = field.querySelector('code');
        const spans = field.querySelectorAll('span');

        // Get all direct children
        const children = Array.from(field.children).map(c => ({
          tag: c.tagName,
          class: (c.className || '').toString().substring(0, 50),
          text: c.textContent.substring(0, 100)
        }));

        results.push({
          index: idx,
          classList: classList,
          codeCount: codes.length,
          codeTexts: codeTexts,
          firstCodeText: firstCode ? firstCode.textContent : null,
          childrenCount: children.length,
          children: children.slice(0, 5),
          text: field.textContent.substring(0, 300)
        });
      }
    });

    return results;
  });

  console.log('\n=== Parameter Field Analysis ===\n');
  paramInfo.forEach(p => {
    console.log(`\n--- Field ${p.index} ---`);
    console.log(`Class: ${p.classList}`);
    console.log(`Code count: ${p.codeCount}`);
    console.log(`Code texts: ${JSON.stringify(p.codeTexts)}`);
    console.log(`Children: ${JSON.stringify(p.children, null, 2)}`);
    console.log(`Text preview: ${p.text}`);
  });

  await browser.close();
}

inspectPage().catch(console.error);
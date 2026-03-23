import { chromium } from 'playwright';

async function inspectDetailPage() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  const url = 'https://modelscope.cn/mcp/servers/@modelcontextprotocol/fetch';
  console.log(`Inspecting: ${url}\n`);

  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(5000);

  // Get full HTML structure of main content
  const htmlStructure = await page.evaluate(() => {
    const main = document.querySelector('main');
    if (!main) return 'No main element found';

    // Get all direct children and their structure
    const getStructure = (el, depth = 0) => {
      const indent = '  '.repeat(depth);
      let result = `${indent}<${el.tagName.toLowerCase()}`;
      if (el.id) result += ` id="${el.id}"`;
      if (el.className && typeof el.className === 'string') result += ` class="${el.className}"`;
      result += '>\n';

      // Get text content if this is a leaf-ish node
      if (el.children.length === 0 || depth > 3) {
        const text = el.innerText?.trim().substring(0, 200);
        if (text && el.children.length === 0) {
          result += `${indent}  "${text}"\n`;
        }
      }

      // Only show first 5 children at each level to avoid too much output
      const childrenToShow = Array.from(el.children).slice(0, 10);
      childrenToShow.forEach(child => {
        result += getStructure(child, depth + 1);
      });

      if (el.children.length > 10) {
        result += `${indent}  ... and ${el.children.length - 10} more children\n`;
      }

      return result;
    };

    return getStructure(main);
  });

  console.log('HTML Structure:');
  console.log(htmlStructure.substring(0, 5000));

  // Get all text content from main
  const allText = await page.evaluate(() => {
    const main = document.querySelector('main');
    return main?.innerText || 'No main element';
  });
  console.log('\n\nAll text from main:');
  console.log(allText);

  // Get code blocks
  const codeBlocks = await page.evaluate(() => {
    const blocks = [];
    document.querySelectorAll('pre, code').forEach(el => {
      const text = el.textContent.trim();
      if (text.length > 20) {
        blocks.push({
          tag: el.tagName,
          className: el.className,
          language: el.className?.match(/language-(\w+)/)?.[1] || 'unknown',
          code: text.substring(0, 500)
        });
      }
    });
    return blocks;
  });
  console.log('\n\nCode blocks:');
  codeBlocks.forEach((b, i) => {
    console.log(`\n--- Code Block ${i + 1} (${b.language}) ---`);
    console.log(b.code);
  });

  // Get tables
  const tables = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('table')).map(table => {
      const rows = Array.from(table.querySelectorAll('tr')).map(tr =>
        Array.from(tr.querySelectorAll('th, td')).map(td => td.textContent.trim())
      );
      return rows;
    });
  });
  if (tables.length > 0) {
    console.log('\n\nTables:');
    tables.forEach((t, i) => {
      console.log(`\n--- Table ${i + 1} ---`);
      t.forEach(row => console.log(row.join(' | ')));
    });
  }

  await browser.close();
}

inspectDetailPage().catch(console.error);
import { chromium } from 'playwright';

async function inspectPage() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  const urls = [
    'https://modelscope.cn/mcp',
    'https://modelscope.cn/mcp/servers/@modelcontextprotocol/fetch'
  ];

  for (const url of urls) {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`Inspecting: ${url}`);
    console.log('='.repeat(60));

    await page.goto(url, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3000);

    // Get page title
    const title = await page.evaluate(() => document.title);
    console.log(`\nPage Title: ${title}`);

    // Get all h1-h3 elements
    const headings = await page.evaluate(() => {
      const h1s = Array.from(document.querySelectorAll('h1')).map(e => ({ tag: 'h1', text: e.textContent.trim() }));
      const h2s = Array.from(document.querySelectorAll('h2')).map(e => ({ tag: 'h2', text: e.textContent.trim() }));
      const h3s = Array.from(document.querySelectorAll('h3')).map(e => ({ tag: 'h3', text: e.textContent.trim() }));
      return [...h1s, ...h2s, ...h3s].slice(0, 20);
    });
    console.log(`\nHeadings found: ${headings.length}`);
    headings.forEach(h => console.log(`  ${h.tag}: ${h.text}`));

    // Get main content structure
    const structure = await page.evaluate(() => {
      // Find main content containers
      const mainSelectors = ['main', 'article', '.content', '[class*="content"]', '[class*="main"]', '[class*="detail"]', '[class*="server"]', '#root'];
      const containers = [];

      mainSelectors.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => {
          const rect = el.getBoundingClientRect();
          if (rect.width > 100 && rect.height > 100) {
            containers.push({
              selector,
              id: el.id,
              className: el.className,
              width: Math.round(rect.width),
              height: Math.round(rect.height),
              children: el.children.length,
              textLength: el.innerText?.length || 0
            });
          }
        });
      });

      return containers;
    });
    console.log(`\nContent containers found:`);
    structure.forEach(c => console.log(`  ${c.selector}: ${c.width}x${c.height}, children=${c.children}, text=${c.textLength} chars`));

    // Get text content from the largest container
    const mainContent = await page.evaluate(() => {
      // Try to find the main content area
      const possibleContainers = [
        document.querySelector('main'),
        document.querySelector('article'),
        document.querySelector('[class*="content"]'),
        document.querySelector('[class*="detail"]'),
        document.querySelector('[class*="server"]'),
        document.querySelector('.ant-layout-content'),
        document.querySelector('#root')
      ].filter(Boolean);

      const largest = possibleContainers.reduce((max, el) => {
        const rect = el.getBoundingClientRect();
        const area = rect.width * rect.height;
        const maxArea = max ? max.getBoundingClientRect().width * max.getBoundingClientRect().height : 0;
        return area > maxArea ? el : max;
      }, null);

      if (largest) {
        return {
          tagName: largest.tagName,
          className: largest.className,
          id: largest.id,
          innerText: largest.innerText?.substring(0, 3000) || '',
          html: largest.innerHTML?.substring(0, 5000) || ''
        };
      }
      return null;
    });

    if (mainContent) {
      console.log(`\nMain content area:`);
      console.log(`  Tag: ${mainContent.tagName}, Class: ${mainContent.className}, ID: ${mainContent.id}`);
      console.log(`\nText preview (first 500 chars):`);
      console.log(mainContent.innerText.substring(0, 500));
    }

    // Get links
    const links = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('a[href*="/mcp"]'))
        .map(a => ({ href: a.href, text: a.textContent.trim().substring(0, 50) }))
        .slice(0, 10);
    });
    console.log(`\nMCP Links found: ${links.length}`);
    links.forEach(l => console.log(`  ${l.text}: ${l.href}`));

    // Get any tables
    const tables = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('table')).map(t => ({
        rows: t.querySelectorAll('tr').length,
        headers: Array.from(t.querySelectorAll('th')).map(th => th.textContent.trim())
      }));
    });
    if (tables.length > 0) {
      console.log(`\nTables found: ${tables.length}`);
      tables.forEach((t, i) => console.log(`  Table ${i+1}: ${t.rows} rows, headers: ${t.headers.join(', ')}`));
    }

    // Get any code blocks
    const codeBlocks = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('pre, code')).map(c => ({
        tag: c.tagName,
        className: c.className,
        text: c.textContent.trim().substring(0, 100)
      })).slice(0, 5);
    });
    if (codeBlocks.length > 0) {
      console.log(`\nCode blocks found: ${codeBlocks.length}`);
      codeBlocks.forEach((c, i) => console.log(`  ${i+1}. ${c.tag}.${c.className}: ${c.text}...`));
    }
  }

  await browser.close();
}

inspectPage().catch(console.error);
/**
 * 调试脚本：检查 EODHD 页面的 HTML 结构
 */
import { chromium } from 'playwright';

async function debugEodhdPage() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  const testUrl = 'https://eodhd.com/financial-apis/live-ohlcv-stocks-api';
  console.log(`正在访问: ${testUrl}`);

  await page.goto(testUrl, { waitUntil: 'domcontentloaded', timeout: 90000 });
  await page.waitForTimeout(8000);

  // 检查页面结构
  const pageInfo = await page.evaluate(() => {
    const info = {
      title: '',
      h1Classes: [],
      articleContainer: null,
      contentSelectors: {},
      tables: [],
      codeBlocks: []
    };

    // 检查 h1 标签
    const h1 = document.querySelector('h1');
    if (h1) {
      info.title = h1.textContent.trim();
      info.h1Classes = h1.className.split(' ').filter(c => c);
      info.h1Parent = h1.parentElement?.className || '';
      info.h1ParentTag = h1.parentElement?.tagName || '';
    }

    // 检查可能的内容容器
    const possibleContainers = [
      '.entry-content',
      '.article-content',
      'article',
      '.post-content',
      '.content',
      'main',
      '.main-content'
    ];

    for (const selector of possibleContainers) {
      const el = document.querySelector(selector);
      if (el) {
        info.contentSelectors[selector] = {
          exists: true,
          childCount: el.children.length,
          textLength: el.textContent.length,
          firstParagraph: el.querySelector('p')?.textContent.substring(0, 100) || ''
        };
      }
    }

    // 检查 article 标签
    const article = document.querySelector('article');
    if (article) {
      info.articleContainer = {
        className: article.className,
        id: article.id,
        children: Array.from(article.children).map(c => ({
          tag: c.tagName,
          className: c.className,
          textPreview: c.textContent.substring(0, 50)
        }))
      };
    }

    // 检查表格结构
    const tables = document.querySelectorAll('table');
    tables.forEach((table, idx) => {
      const rows = table.querySelectorAll('tr');
      if (rows.length > 0) {
        const headerRow = rows[0];
        const headers = Array.from(headerRow.querySelectorAll('th, td')).map(cell => cell.textContent.trim());
        const firstDataRow = rows[1];
        const firstData = firstDataRow ? Array.from(firstDataRow.querySelectorAll('td, th')).map(cell => cell.textContent.trim()) : [];

        info.tables.push({
          index: idx,
          headers,
          firstDataRow: firstData.slice(0, 5),
          rowCount: rows.length
        });
      }
    });

    // 检查代码块
    const preBlocks = document.querySelectorAll('pre');
    preBlocks.forEach((pre, idx) => {
      const className = pre.className;
      const text = pre.textContent.substring(0, 100);
      info.codeBlocks.push({
        index: idx,
        className,
        textPreview: text
      });
    });

    // 检查 API URL 元素
    const apiUrlElements = document.querySelectorAll('.api_url_text, pre[class*="api"]');
    info.apiUrlElements = Array.from(apiUrlElements).map(el => ({
      className: el.className,
      text: el.textContent.substring(0, 150)
    }));

    // 检查标题结构
    info.headings = [];
    document.querySelectorAll('h2, h3').forEach(h => {
      info.headings.push({
        tag: h.tagName,
        text: h.textContent.trim().substring(0, 100),
        className: h.className
      });
    });

    // 检查 entry-content 内的内容结构
    const entryContent = document.querySelector('.entry-content');
    if (entryContent) {
      info.entryContentChildren = Array.from(entryContent.children).map(c => ({
        tag: c.tagName,
        className: c.className,
        textPreview: c.textContent.substring(0, 100)
      }));
    }

    return info;
  });

  console.log('\n=== 页面结构分析 ===\n');
  console.log('标题:', pageInfo.title);
  console.log('H1 类名:', pageInfo.h1Classes);
  console.log('H1 父元素:', pageInfo.h1ParentTag, pageInfo.h1Parent);

  console.log('\n=== 内容容器检查 ===');
  for (const [selector, data] of Object.entries(pageInfo.contentSelectors)) {
    console.log(`${selector}:`, data);
  }

  console.log('\n=== Article 容器 ===');
  console.log(JSON.stringify(pageInfo.articleContainer, null, 2));

  console.log('\n=== 表格结构 ===');
  pageInfo.tables.forEach(t => {
    console.log(`表格 ${t.index}: headers=${t.headers}, firstRow=${t.firstDataRow}`);
  });

  console.log('\n=== 代码块 ===');
  pageInfo.codeBlocks.forEach(c => {
    console.log(`代码块 ${c.index}: class="${c.className}", preview="${c.textPreview}"`);
  });

  console.log('\n=== API URL 元素 ===');
  console.log(JSON.stringify(pageInfo.apiUrlElements, null, 2));

  console.log('\n=== 标题结构 ===');
  console.log(JSON.stringify(pageInfo.headings, null, 2));

  console.log('\n=== Entry-content 子元素 ===');
  console.log(JSON.stringify(pageInfo.entryContentChildren, null, 2));

  await browser.close();
}

debugEodhdPage().catch(console.error);
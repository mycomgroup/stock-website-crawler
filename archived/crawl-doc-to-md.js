/**
 * 遍历理杏仁开放平台所有 API 文档页 (doc?api-key=xxx)，
 * 解析每页的「简要描述、请求URL、请求方式、参数、当前支持」并生成一个 .md 文件。
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE_DOC = 'https://www.lixinger.com/open/api/doc';
const ACCOUNT = '13311390323';
const PASSWORD = '3228552';
const OUTPUT_DIR = path.join(__dirname, 'api-docs');

async function doLogin(page) {
  const loginLink = page.locator('text=登录').first();
  if (await loginLink.count() > 0) {
    await loginLink.click();
    await page.waitForTimeout(2000);
  }
  const phoneSelectors = ['input[placeholder*="手机"]', 'input[placeholder*="账号"]', 'input[type="tel"]', 'input[name="phone"]', 'input[name="username"]'];
  let phoneInput = page.locator('input').first();
  for (const sel of phoneSelectors) {
    const el = page.locator(sel).first();
    if (await el.count() > 0) {
      phoneInput = el;
      break;
    }
  }
  await phoneInput.fill(ACCOUNT);
  const pwdInput = page.locator('input[type="password"]').first();
  await pwdInput.fill(PASSWORD);
  const btn = page.locator('button:has-text("登录"), a:has-text("登录"), [type="submit"]').first();
  if (await btn.count() > 0) await btn.click();
  await page.waitForTimeout(4000);
}

/** 从文档首页/侧栏收集所有 doc?api-key= 的 URL */
async function collectDocUrls(page) {
  await page.goto(BASE_DOC, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(3000);
  
  // 检查是否需要登录
  if (page.url().includes('login') || (await page.locator('input[type="password"]').count()) > 0) {
    await doLogin(page);
    await page.goto(BASE_DOC, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000);
  }
  
  // 等待侧栏加载
  await page.waitForSelector('a[href*="api-key="]', { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(1500);
  
  // 展开所有折叠项
  await page.evaluate(() => {
    // 展开所有可能的折叠菜单
    document.querySelectorAll('[class*="collapse"], [class*="expand"], details, summary').forEach((el) => {
      try {
        if (el.tagName === 'DETAILS') {
          el.open = true;
        } else {
          el.click();
        }
      } catch (_) {}
    });
    
    // 点击所有可能的展开按钮
    document.querySelectorAll('button, a, span, div').forEach((el) => {
      const text = el.textContent || '';
      if (text.includes('展开') || text.includes('▶') || text.includes('>')) {
        try {
          el.click();
        } catch (_) {}
      }
    });
  });
  
  await page.waitForTimeout(2000);
  
  // 再次尝试展开
  await page.evaluate(() => {
    document.querySelectorAll('[class*="collapse"], [class*="expand"]').forEach((el) => {
      try {
        el.click();
      } catch (_) {}
    });
  });
  
  await page.waitForTimeout(1000);
  
  const urls = await page.evaluate(() => {
    const set = new Set();
    document.querySelectorAll('a[href*="api-key="]').forEach((a) => {
      const href = a.getAttribute('href');
      if (!href) return;
      try {
        const url = href.startsWith('http') ? href : new URL(href, window.location.origin).href;
        if (url.includes('/open/api/doc') && url.includes('api-key=')) {
          set.add(url);
        }
      } catch (_) {}
    });
    return Array.from(set);
  });
  
  return urls;
}

/** 解析单页文档内容为结构化数据（优先从 DOM 表格/标题提取） */
async function parseDocPage(page, docUrl) {
  await page.goto(docUrl, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(3000);

  const apiKeyMatch = docUrl.match(/api-key=([^&]+)/);
  const apiKey = apiKeyMatch ? decodeURIComponent(apiKeyMatch[1]) : 'unknown';

  // 提取API试用示例 - 需要逐个点击tab来获取不同的JSON
  const apiExamples = [];
  
  // 方法1: 查找所有"获取"按钮
  const buttons = await page.locator('button, a').evaluateAll(elements => 
    elements
      .map((el, index) => ({ text: el.textContent.trim(), index }))
      .filter(item => item.text.startsWith('获取'))
  );
  
  console.log(`  找到 ${buttons.length} 个示例按钮`);
  
  // 逐个点击按钮，提取对应的JSON
  for (const btn of buttons) {
    try {
      // 点击按钮 - 使用更精确的定位
      await page.evaluate((btnText) => {
        const buttons = Array.from(document.querySelectorAll('button, a'));
        const targetBtn = buttons.find(b => b.textContent.trim() === btnText);
        if (targetBtn) {
          targetBtn.click();
        }
      }, btn.text);
      
      await page.waitForTimeout(1000); // 等待JSON更新
      
      // 提取当前显示的JSON - 尝试多种选择器
      const code = await page.evaluate(() => {
        // 优先查找textarea
        let codeEl = document.querySelector('textarea[class*="json"], textarea');
        if (!codeEl) {
          // 查找包含JSON的code或pre
          const allCode = Array.from(document.querySelectorAll('pre code, pre, code'));
          codeEl = allCode.find(el => {
            const text = (el.textContent || '').trim();
            return text.startsWith('{') && text.includes('"');
          });
        }
        
        if (codeEl) {
          const text = (codeEl.value || codeEl.textContent || codeEl.innerText || '').trim();
          return text;
        }
        return '';
      });
      
      if (code && code.includes('{')) {
        apiExamples.push({ name: btn.text, code });
        console.log(`    ✓ ${btn.text} (${code.length}字符)`);
      } else {
        console.log(`    ✗ ${btn.text} (未找到JSON)`);
      }
    } catch (e) {
      console.log(`    ✗ ${btn.text} (错误: ${e.message})`);
    }
  }
  
  // 方法2: 如果没有找到"获取"按钮，尝试直接从textarea提取
  if (apiExamples.length === 0) {
    console.log(`  未找到"获取"按钮，尝试直接提取textarea内容`);
    const textareaCode = await page.evaluate(() => {
      const textarea = document.querySelector('textarea');
      if (textarea) {
        const value = (textarea.value || '').trim();
        if (value && value.includes('{')) {
          return value;
        }
      }
      return '';
    });
    
    if (textareaCode) {
      apiExamples.push({ name: 'API示例', code: textareaCode });
      console.log(`    ✓ 从textarea提取 (${textareaCode.length}字符)`);
    }
  }

  const extracted = await page.evaluate(() => {
    const root = document.querySelector('main') || document.querySelector('[class*="doc"]') || document.querySelector('[class*="content"]') || document.querySelector('#app') || document.body;
    const getText = (el) => (el ? el.innerText : '');
    const text = getText(root);

    let title = '';
    const h1 = root.querySelector('h1, h2');
    if (h1) title = h1.innerText.trim();
    if (!title && /[^\n]+API/.test(text)) title = (text.match(/([^\n]+API)/) || [])[1] || '';

    let briefDesc = '';
    const briefEl = Array.from(root.querySelectorAll('p, div')).find((el) => el.innerText.trim().startsWith('获取') && el.innerText.length < 500);
    if (briefEl) briefDesc = briefEl.innerText.trim();
    if (!briefDesc && /简要描述/.test(text)) {
      const m = text.match(/简要描述[：:]\s*\n?([^\n]+(?:\n(?!请求URL)[^\n]+)*)/);
      if (m) briefDesc = m[1].replace(/\s+/g, ' ').trim();
    }

    let requestUrl = '';
    const urlEl = root.querySelector('code, pre, [class*="url"]');
    if (urlEl && /open\.lixinger\.com|api\.lixinger/.test(urlEl.innerText)) requestUrl = urlEl.innerText.trim().split(/\s/)[0];
    if (!requestUrl && /请求URL/.test(text)) {
      const m = text.match(/请求URL[：:]\s*\n?([^\s\n]+)/);
      if (m) requestUrl = m[1].trim();
    }

    let requestMethod = '';
    if (/请求方式/.test(text)) {
      const m = text.match(/请求方式[：:]\s*\n?(\w+)/);
      if (m) requestMethod = m[1].trim();
    }

    const params = [];
    const tables = root.querySelectorAll('table');
    for (const table of tables) {
      const rows = table.querySelectorAll('tr');
      if (rows.length < 2) continue;
      const header = (rows[0].innerText || '').toLowerCase();
      if (!header.includes('必选') && !header.includes('参数')) continue;
      const cells0 = rows[0].querySelectorAll('th, td');
      const colCount = cells0.length;
      for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].querySelectorAll('td, th');
        if (cells.length < 2) continue;
        const name = (cells[0] && cells[0].innerText) ? cells[0].innerText.trim() : '';
        const required = (cells[1] && cells[1].innerText) ? cells[1].innerText.trim() : '';
        const type = (cells[2] && cells[2].innerText) ? cells[2].innerText.trim() : '';
        const desc = (cells[3] && cells[3].innerText) ? cells[3].innerText.trim() : (cells[2] && cells.length === 3 ? cells[2].innerText.trim() : '');
        if (name && !name.includes('参数名称')) params.push({ name, required, type, desc });
      }
      if (params.length > 0) break;
    }

    const metrics = [];
    const listItems = root.querySelectorAll('li, tr');
    for (const el of listItems) {
      const t = el.innerText || '';
      const colon = t.match(/([^：:\n]+)[：:]\s*(\S+)/);
      if (colon && t.length < 200 && !t.includes('参数名称')) {
        const name = colon[1].trim();
        const code = colon[2].trim();
        if (code && /^[a-z_0-9.]+$/i.test(code)) metrics.push({ name, code });
      }
    }
    if (metrics.length === 0 && /当前支持/.test(text)) {
      const block = text.match(/当前支持[：:]?\s*([\s\S]*?)(?=注意事项|参数格式|$)/i);
      if (block) {
        block[1].split('\n').forEach((line) => {
          const m = line.match(/([^：:]+)[：:]\s*(\S+)/);
          if (m) metrics.push({ name: m[1].trim(), code: m[2].trim() });
        });
      }
    }

    let responseDesc = '';
    const responseHeadings = ['返回数据说明', '返回说明', '响应数据', '响应说明', '返回数据'];
    for (const h of responseHeadings) {
      const re = new RegExp(h + '[：:]?\\s*\\n([\\s\\S]*?)(?=注意事项|API试用|$)', 'i');
      const m = text.match(re);
      if (m && m[1].trim()) {
        responseDesc = m[1].trim();
        break;
      }
    }
    
    const responseTable = [];
    for (const table of tables) {
      const rows = table.querySelectorAll('tr');
      if (rows.length < 2) continue;
      const header = (rows[0].innerText || '').toLowerCase();
      if (!header.includes('返回') && !header.includes('字段') && !header.includes('响应') && !header.includes('参数名称')) continue;
      if (header.includes('必选') && !header.includes('返回')) continue;
      
      const headerCells = rows[0].querySelectorAll('th, td');
      const hasThreeCols = headerCells.length >= 3;
      
      for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].querySelectorAll('td, th');
        if (cells.length < 2) continue;
        const name = (cells[0] && cells[0].innerText) ? cells[0].innerText.trim() : '';
        const type = (cells[1] && cells[1].innerText) ? cells[1].innerText.trim() : '';
        const desc = hasThreeCols && cells[2] ? cells[2].innerText.trim() : '';
        if (name && !name.includes('字段') && !name.includes('参数名称')) {
          responseTable.push({ name, type, desc });
        }
      }
      if (responseTable.length > 0) break;
    }
    
    // 如果没找到表格，尝试从文本中解析
    if (responseTable.length === 0 && /返回数据说明/.test(text)) {
      const block = text.match(/返回数据说明[：:]?\s*([\s\S]*?)(?=注意事项|示例|$)/i);
      if (block) {
        const lines = block[1].split('\n');
        for (const line of lines) {
          const match = line.match(/^([^\t\s]+)\s+([^\t\s]+)\s+(.+)$/);
          if (match && match[1] && match[2]) {
            responseTable.push({ name: match[1].trim(), type: match[2].trim(), desc: (match[3] || '').trim() });
          }
        }
      }
    }
    if (!responseDesc && responseTable.length === 0 && /返回数据说明/.test(text)) {
      const m = text.match(/返回数据说明[：:]?\s*([\s\S]*?)(?=注意事项|$)/i);
      if (m) responseDesc = m[1].trim();
    }

    return { title, briefDesc, requestUrl, requestMethod, params, metrics, responseDesc, responseTable, raw: text };
  });

  let title = (extracted.title || apiKey).replace(/购买\s*$/, '').trim();
  return {
    apiKey,
    title: title || apiKey,
    briefDesc: extracted.briefDesc,
    requestUrl: extracted.requestUrl,
    requestMethod: extracted.requestMethod,
    params: extracted.params,
    metrics: extracted.metrics,
    responseDesc: extracted.responseDesc,
    responseTable: extracted.responseTable,
    apiExamples: apiExamples, // 使用前面点击tab提取的示例
    raw: extracted.raw,
  };
}

/** 将解析结果写成 Markdown */
function toMarkdown(data) {
  const lines = [];
  lines.push(`# ${data.title}\n`);
  if (data.briefDesc) {
    lines.push('## 简要描述');
    lines.push('');
    lines.push(data.briefDesc);
    lines.push('');
  }
  lines.push('## 请求URL');
  lines.push('');
  lines.push('```');
  lines.push(data.requestUrl || '(未解析到)');
  lines.push('```');
  lines.push('');
  lines.push('## 请求方式');
  lines.push('');
  lines.push(data.requestMethod || '(未解析到)');
  lines.push('');
  if (data.params && data.params.length > 0) {
    lines.push('## 参数');
    lines.push('');
    lines.push('| 参数名称 | 必选 | 数据类型 | 说明 |');
    lines.push('| -------- | ---- | -------- | ---- |');
    for (const p of data.params) {
      // 保留完整的说明，包括"当前支持"部分
      let desc = p.desc.replace(/\|/g, '\\|').replace(/\n/g, '<br>');
      lines.push(`| ${p.name} | ${p.required} | ${p.type} | ${desc} |`);
    }
    lines.push('');
  }
  if (data.apiExamples && data.apiExamples.length > 0) {
    lines.push('## API试用示例');
    lines.push('');
    data.apiExamples.forEach((example, index) => {
      if (data.apiExamples.length > 1) {
        lines.push(`### ${example.name}`);
        lines.push('');
      }
      lines.push('```json');
      // 尝试格式化 JSON
      try {
        const parsed = JSON.parse(example.code);
        lines.push(JSON.stringify(parsed, null, 2));
      } catch {
        lines.push(example.code);
      }
      lines.push('```');
      lines.push('');
    });
  }
  if (data.responseDesc || (data.responseTable && data.responseTable.length > 0)) {
    lines.push('## 返回数据说明');
    lines.push('');
    if (data.responseTable && data.responseTable.length > 0) {
      const hasDesc = data.responseTable.some(r => r.desc);
      if (hasDesc) {
        lines.push('| 参数名称 | 数据类型 | 说明 |');
        lines.push('| -------- | -------- | ---- |');
        for (const r of data.responseTable) {
          lines.push(`| ${r.name} | ${r.type} | ${(r.desc || '').replace(/\|/g, '\\|').replace(/\n/g, ' ')} |`);
        }
      } else {
        lines.push('| 参数名称 | 数据类型 |');
        lines.push('| -------- | -------- |');
        for (const r of data.responseTable) {
          lines.push(`| ${r.name} | ${r.type} |`);
        }
      }
      lines.push('');
    }
    if (data.responseDesc) {
      const desc = data.responseDesc
        .replace(/\n(API试用|获取指定|执行|返回数据:)[^\n]*/g, '')
        .replace(/参数名称\s+数据类型[\s\S]*/g, '') // 移除文本格式的表格
        .trim();
      if (desc && !desc.includes('参数名称\t数据类型')) {
        if (data.responseTable && data.responseTable.length > 0) lines.push('');
        lines.push(desc);
        lines.push('');
      }
    }
  }
  return lines.join('\n');
}

function safeFilename(apiKey) {
  return apiKey.replace(/[\/\\?*:"<>|]/g, '_').replace(/_+/g, '_') || 'api';
}

(async () => {
  if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  const browser = await chromium.launch({ headless: false, channel: 'chrome' });
  const context = await browser.newContext();
  const page = await context.newPage();

  // 先登录
  console.log('开始登录...');
  try {
    await page.goto('https://www.lixinger.com/open/api/doc', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);
    
    // 检查是否需要登录
    if (page.url().includes('login') || (await page.locator('input[type="password"]').count()) > 0) {
      await doLogin(page);
      console.log('登录成功');
    } else {
      console.log('已登录状态');
    }
  } catch (e) {
    console.error('登录失败', e.message);
  }

  // 从 links.txt 读取URL列表
  let docUrls = [];
  const linksFile = path.join(__dirname, 'links.txt');
  if (fs.existsSync(linksFile)) {
    const content = fs.readFileSync(linksFile, 'utf8');
    docUrls = content.split('\n')
      .filter(line => line.trim())
      .filter(line => line.includes('api-key=')) // 只保留有api-key的URL
      .map(line => line.trim());
    console.log(`从 links.txt 读取到 ${docUrls.length} 个文档链接`);
  }

  if (docUrls.length === 0) {
    console.log('links.txt 为空，使用预设 api-key 列表');
    const known = [
      'cn/company',
      'cn/company/fundamental/non_financial',
      'cn/company/fundamental/financial',
      'cn/index',
      'hk/company',
      'cn/industry',
      'cn/fund',
    ];
    docUrls = known.map((k) => `${BASE_DOC}?api-key=${k}`);
  }

  console.log('待抓取文档数:', docUrls.length);
  console.log('');
  let written = 0;
  for (let i = 0; i < docUrls.length; i++) {
    const url = docUrls[i];
    console.log(`[${i + 1}/${docUrls.length}] ${url}`);
    try {
      const data = await parseDocPage(page, url);
      const hasContent = data.requestUrl || data.briefDesc || (data.params && data.params.length > 0) || (data.apiExamples && data.apiExamples.length > 0);
      if (!hasContent && !data.raw.includes('API')) {
        console.log('  跳过：无有效内容');
        await page.waitForTimeout(400);
        continue;
      }
      const md = toMarkdown(data);
      const filename = safeFilename(data.apiKey) + '.md';
      const outPath = path.join(OUTPUT_DIR, filename);
      fs.writeFileSync(outPath, md, 'utf8');
      written++;
      console.log('  已写入', filename, data.apiExamples && data.apiExamples.length > 0 ? `(${data.apiExamples.length}个示例)` : '');
    } catch (e) {
      console.error('  失败', e.message);
    }
    await page.waitForTimeout(600);
  }
  console.log('共生成', written, '个 md 文件');

  await browser.close();
  console.log('完成，输出目录:', OUTPUT_DIR);
})();

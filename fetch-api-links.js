const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const URL = 'https://www.lixinger.com/open/api/my-apis';
const ACCOUNT = '13311390323';
const PASSWORD = '3228552';
const OUTPUT_JSON = path.join(__dirname, 'api-links.json');

async function doLogin(page) {
  const currentUrl = page.url();
  if (currentUrl.includes('login') || (await page.locator('input[type="password"]').count()) > 0) {
    // 已在登录页
  } else {
    const loginLink = page.locator('text=登录').first();
    if (await loginLink.count() > 0) {
      await loginLink.click();
      await page.waitForTimeout(2000);
    }
  }

  const phoneSelectors = [
    'input[placeholder*="手机"]',
    'input[placeholder*="账号"]',
    'input[type="tel"]',
    'input[name="phone"]',
    'input[name="username"]',
    'input[name="account"]',
  ];
  let phoneInput = null;
  for (const sel of phoneSelectors) {
    const el = page.locator(sel).first();
    if (await el.count() > 0) {
      phoneInput = el;
      break;
    }
  }
  if (!phoneInput) phoneInput = page.locator('input').first();
  await phoneInput.fill(ACCOUNT);

  const pwdInput = page.locator('input[type="password"]').first();
  await pwdInput.fill(PASSWORD);

  const submitSelectors = [
    'button:has-text("登录")',
    'button:has-text("登 录")',
    'a:has-text("登录")',
    '[type="submit"]',
    'button[type="button"]:has-text("登录")',
  ];
  for (const sel of submitSelectors) {
    const btn = page.locator(sel).first();
    if (await btn.count() > 0) {
      await btn.click();
      break;
    }
  }
  await page.waitForTimeout(5000);
}

async function extractApiLinks(page) {
  return await page.evaluate(() => {
    const result = {
      byGroup: [],
      allLinks: [],
      linkSet: new Set(),
    };

    function addLink(url, text, region, groupName) {
      if (!url || typeof url !== 'string') return;
      let fullUrl = url.trim();
      if (fullUrl.startsWith('//')) fullUrl = 'https:' + fullUrl;
      else if (fullUrl.startsWith('/')) fullUrl = window.location.origin + fullUrl;
      else if (!fullUrl.startsWith('http')) fullUrl = window.location.origin + '/' + fullUrl;
      if (!fullUrl.includes('lixinger.com') || (!fullUrl.includes('/open/') && !fullUrl.includes('open/api'))) return;
      if (result.linkSet.has(fullUrl)) return;
      result.linkSet.add(fullUrl);
      const item = { url: fullUrl, name: (text || '').trim() };
      if (region) item.region = region;
      if (groupName) item.groupName = groupName;
      result.allLinks.push(item);
    }

    // 表格：表头 地区、接口组名、包含的接口、...
    const tables = document.querySelectorAll('table');
    for (const table of tables) {
      const headers = [];
      const ths = table.querySelectorAll('thead th');
      ths.forEach((th, i) => {
        headers.push((th.textContent || '').trim());
      });
      const colIndexApi = headers.findIndex(h => h.includes('包含的接口') || h === '包含的接口');
      const colIndexRegion = headers.findIndex(h => h === '地区' || h.includes('地区'));
      const colIndexGroup = headers.findIndex(h => h.includes('接口组') || h === '接口组名');

      const rows = table.querySelectorAll('tbody tr');
      for (const row of rows) {
        const cells = row.querySelectorAll('td');
        const region = colIndexRegion >= 0 && cells[colIndexRegion] ? (cells[colIndexRegion].textContent || '').trim() : '';
        const groupName = colIndexGroup >= 0 && cells[colIndexGroup] ? (cells[colIndexGroup].textContent || '').trim() : '';

        const apiCell = colIndexApi >= 0 ? cells[colIndexApi] : null;
        if (apiCell) {
          const links = apiCell.querySelectorAll('a[href]');
          const apis = [];
          links.forEach(a => {
            const href = a.getAttribute('href');
            const text = (a.textContent || '').trim();
            if (href) {
              addLink(href, text, region, groupName);
              apis.push({ name: text, url: href.startsWith('http') ? href : (window.location.origin + (href.startsWith('/') ? href : '/' + href)) });
            }
          });
          if (apis.length > 0) {
            result.byGroup.push({ region, groupName, apis });
          }
        }

        // 整行内的所有 API 相关链接（含相对路径）
        row.querySelectorAll('a[href*="/open/"], a[href*="open/api"]').forEach(a => {
          const href = a.getAttribute('href');
          addLink(href, a.textContent, region, groupName);
        });
      }
    }

    // 兜底：全页面所有开放平台/API 相关链接
    document.querySelectorAll('a[href*="/open/"], a[href*="open/api"]').forEach(a => {
      const href = a.getAttribute('href');
      addLink(href, a.textContent);
    });

    delete result.linkSet;
    return result;
  });
}

function isApiDocLink(url) {
  if (!url) return false;
  return url.includes('/open/api/detail') || url.includes('api-key=') || (url.includes('/open/api/doc') && url !== 'https://www.lixinger.com/open/api/doc');
}

(async () => {
  const browser = await chromium.launch({
    headless: false,
    channel: 'chrome',
  });
  const context = await browser.newContext();
  const page = await context.newPage();

  const capturedApiData = [];
  await page.route('**/*', (route) => {
    const url = route.request().url();
    if (url.includes('my-apis') || url.includes('api') && (url.includes('lixinger.com') || url.includes('graphql'))) {
      route.continue().then(() => {}).catch(() => {});
    } else {
      route.continue();
    }
  });
  page.on('response', async (response) => {
    const url = response.url();
    if (!url.includes('lixinger.com')) return;
    try {
      const ct = response.headers()['content-type'] || '';
      if (ct.includes('json')) {
        const body = await response.text();
        if (body.length > 50 && body.length < 800000) {
          const j = JSON.parse(body);
          if (j && typeof j === 'object') capturedApiData.push({ url, data: j });
        }
      }
    } catch (_) {}
  });

  try {
    await page.goto(URL, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000);

    if (page.url().includes('login') || (await page.locator('input[type="password"]').count()) > 0) {
      await doLogin(page);
      await page.waitForTimeout(2000);
    }
    const aclPromise = page.waitForResponse((r) => r.url().includes('open-api/acl/list') && r.status() === 200, { timeout: 20000 }).catch(() => null);
    await page.goto(URL, { waitUntil: 'networkidle', timeout: 30000 });
    const aclRes = await aclPromise;
    if (aclRes) {
      try {
        const aclBody = await aclRes.json();
        capturedApiData.push({ url: aclRes.url(), data: aclBody });
      } catch (_) {}
    }
    await page.waitForTimeout(2000);
    // 确保在「我的接口」子页：点击侧栏「我的接口」
    const myApisLink = page.locator('a[href*="my-apis"], a:has-text("我的接口")').first();
    if (await myApisLink.count() > 0) {
      await myApisLink.click();
      await page.waitForTimeout(3000);
    }
    await page.waitForSelector('text=包含的接口', { timeout: 15000 }).catch(() => {});
    await page.waitForSelector('text=购买', { timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(2000);

    // 若有「展开」按钮，先展开所有以显示接口链接
    const expandButtons = page.locator('button:has-text("展开"), a:has-text("展开"), [class*="expand"], .ant-table-row-expand-icon');
    const count = await expandButtons.count();
    for (let i = 0; i < Math.min(count, 50); i++) {
      try {
        await expandButtons.nth(i).click();
        await page.waitForTimeout(400);
      } catch (_) {}
    }
    await page.waitForTimeout(1000);

    let data = await extractApiLinks(page);

    // 若 API 文档链接很少，从开放平台文档页收集（含侧栏/折叠内的链接）
    if (data.allLinks.filter((l) => isApiDocLink(l.url)).length < 5) {
      await page.goto('https://www.lixinger.com/open/api/doc', { waitUntil: 'networkidle', timeout: 20000 }).catch(() => {});
      await page.waitForTimeout(2000);
      await page.evaluate(() => {
        document.querySelectorAll('[class*="expand"], [class*="collapse"], details, [class*="accordion"]').forEach((el) => {
          if (el.getAttribute('open') !== 'open') el.setAttribute('open', 'open');
          el.click && el.click();
        });
      });
      await page.waitForTimeout(1000);
      const docData = await extractApiLinks(page);
      docData.allLinks.forEach((item) => {
        if (!data.allLinks.some((l) => l.url === item.url)) data.allLinks.push(item);
      });
      if (docData.byGroup.length > 0) data.byGroup = data.byGroup.concat(docData.byGroup);
    }

    // 尝试从页面脚本/数据中提取：监听或读取 __NEXT_DATA__ / 全局变量等
    const extra = await page.evaluate(() => {
      const out = { nextData: null, scriptJson: [] };
      const el = document.getElementById('__NEXT_DATA__');
      if (el && el.textContent) {
        try {
          out.nextData = JSON.parse(el.textContent);
        } catch (_) {}
      }
      return out;
    });
    if (extra.nextData && extra.nextData.props && extra.nextData.props.pageProps) {
      const props = extra.nextData.props.pageProps;
      if (props.apiGroups || props.apis || props.data) {
        const raw = props.apiGroups || props.apis || props.data;
        if (Array.isArray(raw)) {
          raw.forEach((g) => {
            if (g.apis && Array.isArray(g.apis)) {
              data.byGroup.push({ region: g.region, groupName: g.name || g.groupName, apis: g.apis });
              g.apis.forEach((api) => {
                const url = api.url || api.link || (api.slug && `https://www.lixinger.com/open/api/doc/${api.slug}`);
                const name = api.name || api.title || api.slug;
                if (url && !data.allLinks.find((l) => l.url === url)) data.allLinks.push({ url, name, region: g.region, groupName: g.name || g.groupName });
              });
            }
          });
        }
      }
    }

    // 解析 acl/list 格式：可能为 { data: [ { region, apiGroups: [ { name, apis: [...] } ] } ] } 或 { list: [...] }
    function parseAclResponse(j) {
      const into = [];
      const list = j.data || j.list || j;
      const arr = Array.isArray(list) ? list : (list && list.apiGroups) ? [list] : list ? [list] : [];
      arr.forEach((item) => {
        const region = item.region || item.area || '';
        const groups = item.apiGroups || item.groups || (item.apis ? [{ name: item.name || item.groupName, apis: item.apis }] : []);
        groups.forEach((g) => {
          const groupName = g.name || g.groupName || '';
          (g.apis || g.list || []).forEach((api) => {
            const name = api.name || api.title || api.slug || api.apiName || '';
            const path = api.path || api.url || api.slug || api.id;
            const url = typeof path === 'string' && path.startsWith('http') ? path : (path ? `https://www.lixinger.com/open/api/doc/${path}` : '');
            if (name || url) into.push({ name, url, region, groupName });
          });
        });
      });
      return into;
    }
    function digApis(obj, into) {
      if (!obj) return;
      if (Array.isArray(obj)) {
        obj.forEach((item) => digApis(item, into));
        return;
      }
      if (obj.apis && Array.isArray(obj.apis)) {
        const region = obj.region || obj.area || '';
        const groupName = obj.name || obj.groupName || obj.apiGroupName || '';
        obj.apis.forEach((api) => {
          const name = api.name || api.title || api.slug || api.apiName || '';
          const path = api.path || api.url || api.slug || api.id;
          const url = typeof path === 'string' && path.startsWith('http') ? path : (path ? `https://www.lixinger.com/open/api/doc/${path}` : null);
          if (name || url) into.push({ name, url: url || '', region, groupName });
        });
        data.byGroup.push({ region: groupName ? '' : region, groupName, apis: obj.apis.map((a) => ({ name: a.name || a.title || a.slug, url: a.url || (a.slug ? `https://www.lixinger.com/open/api/doc/${a.slug}` : '') })) });
      }
      if (obj.data) digApis(obj.data, into);
      if (obj.props && obj.props.pageProps) digApis(obj.props.pageProps, into);
      ['apiGroups', 'groups', 'list', 'items'].forEach((key) => {
        if (obj[key]) digApis(obj[key], into);
      });
    }
    const extracted = [];
    capturedApiData.forEach(({ url: resUrl, data: j }) => {
      if (resUrl.includes('acl/list') && j && (j.data !== undefined || j.list !== undefined)) {
        parseAclResponse(j).forEach((item) => extracted.push(item));
      }
      digApis(j, extracted);
    });
    extracted.forEach((item) => {
      if (item.url && !data.allLinks.some((l) => l.url === item.url)) data.allLinks.push(item);
    });

    // 去重 allLinks（按 url）
    const seen = new Set();
    data.allLinks = data.allLinks.filter((item) => {
      if (seen.has(item.url)) return false;
      seen.add(item.url);
      return true;
    });

    // 单独列出「包含的接口」：仅 API 文档/详情链接
    const apiDocLinks = data.allLinks.filter((item) => isApiDocLink(item.url));
    const output = {
      apiDocLinks: apiDocLinks.length > 0 ? apiDocLinks : data.allLinks,
      byGroup: data.byGroup,
      allLinks: data.allLinks,
    };

    fs.writeFileSync(OUTPUT_JSON, JSON.stringify(output, null, 2), 'utf8');
    if (capturedApiData.length > 0) {
      fs.writeFileSync(path.join(__dirname, 'captured-responses.json'), JSON.stringify(capturedApiData.filter((c) => c.url.includes('acl')), null, 2), 'utf8');
      console.log('已保存 acl 相关响应数:', capturedApiData.filter((c) => c.url.includes('acl')).length);
    }
    console.log('已保存到', OUTPUT_JSON);
    console.log('包含的接口(API文档)数:', output.apiDocLinks.length);
    console.log('按组数量:', output.byGroup.length);
    console.log('链接总数:', output.allLinks.length);
  } catch (e) {
    console.error(e);
    await page.screenshot({ path: path.join(__dirname, 'fetch-error.png') });
  }

  await browser.close();
})();

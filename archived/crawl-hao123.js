import fs from 'fs';
import path from 'path';
import {
  buildSiteConfig,
  collectInternalHao123Links,
  extractAnchorLinks,
  extractWebsiteEntries,
  sanitizeHostToName
} from '../src/hao123-site-bootstrap.js';

const PROJECT_ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const CONFIGURE_DIR = path.join(PROJECT_ROOT, 'configure');
const OUTPUT_DIR = path.join(PROJECT_ROOT, 'output', 'hao123');
const SITES_FILE = path.join(OUTPUT_DIR, 'sites.json');
const LINK_LIST_FILE = path.join(OUTPUT_DIR, 'all-sites.txt');
const CRAWLED_PAGES_FILE = path.join(OUTPUT_DIR, 'crawled-pages.txt');

function ensureDirectories() {
  fs.mkdirSync(CONFIGURE_DIR, { recursive: true });
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

function getArgValue(flagName) {
  const index = process.argv.findIndex((arg) => arg === flagName);
  if (index === -1 || index + 1 >= process.argv.length) {
    return null;
  }
  return process.argv[index + 1];
}

function getArgInt(flagName, fallback) {
  const value = getArgValue(flagName);
  if (!value) {
    return fallback;
  }

  const parsed = Number.parseInt(value, 10);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    throw new Error(`${flagName} 必须是正整数`);
  }

  return parsed;
}

async function fetchHtml(url) {
  const response = await fetch(url, {
    headers: {
      'user-agent': 'Mozilla/5.0 (compatible; hao123-crawler/1.1)'
    }
  });

  if (!response.ok) {
    throw new Error(`请求失败 ${url}: HTTP ${response.status}`);
  }

  return response.text();
}

function normalizeMirrorPath(url) {
  const pathname = url.pathname.endsWith('/') ? `${url.pathname}index.html` : url.pathname;
  const normalizedPath = pathname.replace(/^\//, '') || 'index.html';
  return normalizedPath;
}

function createHtmlResolver(mirrorDir) {
  if (!mirrorDir) {
    return async (url) => fetchHtml(url);
  }

  const base = path.resolve(process.cwd(), mirrorDir);
  return async (url) => {
    const parsed = new URL(url);
    const fullPath = path.join(base, parsed.hostname, normalizeMirrorPath(parsed));
    if (!fs.existsSync(fullPath)) {
      throw new Error(`镜像文件不存在: ${fullPath}`);
    }
    return fs.readFileSync(fullPath, 'utf-8');
  };
}

function writeSiteArtifacts(entries, crawledPages) {
  fs.writeFileSync(SITES_FILE, JSON.stringify(entries, null, 2), 'utf-8');
  fs.writeFileSync(LINK_LIST_FILE, entries.map((item) => item.url).join('\n') + '\n', 'utf-8');
  fs.writeFileSync(CRAWLED_PAGES_FILE, crawledPages.join('\n') + '\n', 'utf-8');

  for (const entry of entries) {
    const name = sanitizeHostToName(entry.host);
    const configPath = path.join(CONFIGURE_DIR, `${name}.json`);
    fs.writeFileSync(configPath, JSON.stringify(buildSiteConfig(entry), null, 2), 'utf-8');
  }
}

async function crawlHao123AllSites({ maxPages, mirrorDir }) {
  const resolveHtml = createHtmlResolver(mirrorDir);
  const queue = ['https://www.hao123.com/'];
  const visited = new Set();
  const externalLinks = [];

  while (queue.length > 0 && visited.size < maxPages) {
    const currentUrl = queue.shift();
    if (visited.has(currentUrl)) {
      continue;
    }

    visited.add(currentUrl);

    let html;
    try {
      html = await resolveHtml(currentUrl);
    } catch (error) {
      console.warn(`跳过页面: ${currentUrl} (${error.message})`);
      continue;
    }

    const links = extractAnchorLinks(html);
    externalLinks.push(...links);

    const internalLinks = collectInternalHao123Links(links, currentUrl);
    for (const link of internalLinks) {
      if (!visited.has(link) && queue.length + visited.size < maxPages * 3) {
        queue.push(link);
      }
    }
  }

  const entries = extractWebsiteEntries(externalLinks);
  return {
    entries,
    crawledPages: Array.from(visited).sort()
  };
}

async function main() {
  ensureDirectories();

  const maxPages = getArgInt('--max-pages', 300);
  const mirrorDir = getArgValue('--mirror-dir');

  console.log(`开始抓取 hao123 站点 (maxPages=${maxPages})...`);
  if (mirrorDir) {
    console.log(`使用本地镜像目录: ${path.resolve(process.cwd(), mirrorDir)}`);
  }

  const { entries, crawledPages } = await crawlHao123AllSites({ maxPages, mirrorDir });

  if (entries.length === 0) {
    throw new Error('未抓取到任何外部站点链接，请检查网络或镜像数据。');
  }

  writeSiteArtifacts(entries, crawledPages);

  console.log(`完成：抓取 hao123 页面 ${crawledPages.length} 个，提取站点 ${entries.length} 个`);
  console.log(`站点汇总: ${path.relative(PROJECT_ROOT, SITES_FILE)}`);
  console.log(`链接列表: ${path.relative(PROJECT_ROOT, LINK_LIST_FILE)}`);
  console.log(`页面列表: ${path.relative(PROJECT_ROOT, CRAWLED_PAGES_FILE)}`);
  console.log(`配置目录: ${path.relative(PROJECT_ROOT, CONFIGURE_DIR)}`);
}

main().catch((error) => {
  console.error('抓取失败:', error.message);
  process.exit(1);
});

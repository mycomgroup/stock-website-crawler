/**
 * Hao123 3层深度抓取与分类探索脚本 (原型)
 * 
 * 作用:
 * 该脚本从 hao123.com 开始，采用广度优先搜索(BFS)算法，
 * 最多抓取 3 层深度的页面。目的是为了发现并验证更多的页面类型。
 * 
 * 注意：全量抓取 3 层可能会产生数以百万计的页面，
 * 建议在运行前配置 maxRequests 或限定只抓取特定域名的链接。
 */

import { chromium } from 'playwright';
import fs from 'fs/promises';
import path from 'path';

// --- 配置区域 ---
const START_URL = 'https://www.hao123.com/';
const MAX_DEPTH = 3;             // 最大抓取深度
const MAX_REQUESTS = 500;        // 最大总抓取页面数 (防止跑飞)
const OUTPUT_FILE = path.join(process.cwd(), 'output', 'hao123-deep-links.json');

// 等待队列: { url, depth, parentUrl }
const queue = [{ url: START_URL, depth: 0, parentUrl: null }];
const visited = new Set();
const results = [];

async function main() {
  console.log(`🚀 开始深度抓取任务: ${START_URL}`);
  console.log(`📌 最大深度: ${MAX_DEPTH}, 最大页面数: ${MAX_REQUESTS}`);

  // 确保输出目录存在
  await fs.mkdir(path.dirname(OUTPUT_FILE), { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  });
  
  const page = await context.newPage();

  let requestCount = 0;

  while (queue.length > 0 && requestCount < MAX_REQUESTS) {
    const current = queue.shift();
    
    // 跳过已访问的URL
    if (visited.has(current.url)) continue;
    visited.add(current.url);
    requestCount++;

    console.log(`[${requestCount}/${MAX_REQUESTS}] 深度:${current.depth} 正在抓取: ${current.url}`);

    try {
      // 设置超时时间防止卡死
      await page.goto(current.url, { waitUntil: 'domcontentloaded', timeout: 15000 });
      
      // 提取页面的基本特征，用于后续的类型分类分析
      const pageFeatures = await page.evaluate(() => {
        const title = document.title;
        const metaDesc = document.querySelector('meta[name="description"]')?.content || '';
        const links = Array.from(document.querySelectorAll('a[href]'))
                           .map(a => a.href)
                           .filter(href => href.startsWith('http'));
        
        // 简单提取几个关键标签的数量，用于聚类分析
        const counts = {
          img: document.querySelectorAll('img').length,
          video: document.querySelectorAll('video').length,
          article: document.querySelectorAll('article').length,
          table: document.querySelectorAll('table').length,
          form: document.querySelectorAll('form').length,
          h1: document.querySelectorAll('h1').length
        };

        return { title, metaDesc, links, counts };
      });

      // 保存页面分析结果
      results.push({
        url: current.url,
        depth: current.depth,
        title: pageFeatures.title,
        features: pageFeatures.counts
      });

      // 如果未达到最大深度，将页面内的链接加入队列
      if (current.depth < MAX_DEPTH) {
        // 去重并限制每页提取的链接数，防止队列爆炸
        const uniqueLinks = [...new Set(pageFeatures.links)].slice(0, 20); 
        
        for (const link of uniqueLinks) {
          if (!visited.has(link)) {
            queue.push({
              url: link,
              depth: current.depth + 1,
              parentUrl: current.url
            });
          }
        }
      }

    } catch (error) {
      console.log(`❌ 抓取失败 [${current.url}]: ${error.message.split('\n')[0]}`);
    }

    // 定期保存数据，防止中途崩溃
    if (requestCount % 50 === 0) {
      await fs.writeFile(OUTPUT_FILE, JSON.stringify(results, null, 2));
      console.log(`💾 已临时保存 ${results.length} 条数据`);
    }
  }

  // 最终保存
  await fs.writeFile(OUTPUT_FILE, JSON.stringify(results, null, 2));
  console.log(`\n✅ 抓取完成! 共抓取 ${results.length} 个页面，数据已保存至: ${OUTPUT_FILE}`);
  console.log(`💡 提示: 您可以基于这些页面的特征(features)数据，进行聚类分析，以验证120种页面分类的准确性。`);

  await browser.close();
}

main().catch(console.error);

/**
 * 清理 links.txt 文件中的锚点
 * 去掉所有URL中 # 后面的部分
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const linksFile = path.join(__dirname, '../output/lixinger-crawler/links.txt');

function cleanAnchors() {
  if (!fs.existsSync(linksFile)) {
    console.log('links.txt 文件不存在');
    return;
  }

  console.log('读取 links.txt...');
  const content = fs.readFileSync(linksFile, 'utf-8');
  const lines = content.split('\n').filter(line => line.trim() !== '');

  console.log(`找到 ${lines.length} 个链接`);

  // 解析并清理链接
  const cleanedLinks = [];
  const urlMap = new Map(); // 用于去重

  for (const line of lines) {
    try {
      const link = JSON.parse(line);
      
      // 去掉锚点
      const urlWithoutAnchor = link.url.split('#')[0];
      
      // 检查是否已存在（去重）
      if (urlMap.has(urlWithoutAnchor)) {
        const existing = urlMap.get(urlWithoutAnchor);
        // 如果现有的是 pending，新的是 crawled，则更新
        if (existing.status === 'pending' && link.status === 'crawled') {
          existing.status = 'crawled';
          existing.crawledAt = link.crawledAt;
        }
        console.log(`  去重: ${link.url} -> ${urlWithoutAnchor}`);
      } else {
        link.url = urlWithoutAnchor;
        urlMap.set(urlWithoutAnchor, link);
        cleanedLinks.push(link);
        
        if (link.url !== line.url) {
          console.log(`  清理: ${line.url} -> ${urlWithoutAnchor}`);
        }
      }
    } catch (e) {
      console.error(`解析失败: ${line}`);
    }
  }

  console.log(`\n清理后: ${cleanedLinks.length} 个唯一链接`);
  console.log(`去重: ${lines.length - cleanedLinks.length} 个重复链接`);

  // 保存清理后的链接
  const newContent = cleanedLinks.map(link => JSON.stringify(link)).join('\n');
  fs.writeFileSync(linksFile, newContent, 'utf-8');

  console.log('\n已保存到 links.txt');

  // 统计状态
  const stats = {
    pending: cleanedLinks.filter(l => l.status === 'pending').length,
    crawled: cleanedLinks.filter(l => l.status === 'crawled').length,
    failed: cleanedLinks.filter(l => l.status === 'failed').length
  };

  console.log('\n状态统计:');
  console.log(`  Pending: ${stats.pending}`);
  console.log(`  Crawled: ${stats.crawled}`);
  console.log(`  Failed: ${stats.failed}`);
}

cleanAnchors();

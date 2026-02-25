import fs from 'fs';
import path from 'path';

/**
 * 迁移脚本：更新链接状态字段名
 * pending -> unfetched
 * crawled -> fetched
 * crawledAt -> fetchedAt
 */

const linksFile = './output/lixinger-crawler/links.txt';

console.log('开始迁移链接状态字段名...');
console.log(`读取文件: ${linksFile}`);

if (!fs.existsSync(linksFile)) {
  console.error('错误: links.txt 文件不存在');
  process.exit(1);
}

// 读取文件
const fileContent = fs.readFileSync(linksFile, 'utf-8');
const lines = fileContent.split('\n').filter(line => line.trim() !== '');

console.log(`找到 ${lines.length} 个链接`);

// 解析并更新每个链接
const updatedLinks = lines.map(line => {
  const link = JSON.parse(line);
  
  // 更新状态名称
  if (link.status === 'pending') {
    link.status = 'unfetched';
  } else if (link.status === 'crawled') {
    link.status = 'fetched';
  }
  // failed 保持不变
  
  // 更新字段名
  if (link.crawledAt !== undefined) {
    link.fetchedAt = link.crawledAt;
    delete link.crawledAt;
  }
  
  return link;
});

// 统计
const stats = {
  unfetched: updatedLinks.filter(l => l.status === 'unfetched').length,
  fetching: updatedLinks.filter(l => l.status === 'fetching').length,
  fetched: updatedLinks.filter(l => l.status === 'fetched').length,
  failed: updatedLinks.filter(l => l.status === 'failed').length
};

console.log('\n迁移统计:');
console.log(`  unfetched (未抓取): ${stats.unfetched}`);
console.log(`  fetching (正在抓取): ${stats.fetching}`);
console.log(`  fetched (已完成): ${stats.fetched}`);
console.log(`  failed (失败): ${stats.failed}`);

// 保存更新后的文件
const updatedContent = updatedLinks.map(link => JSON.stringify(link)).join('\n');
fs.writeFileSync(linksFile, updatedContent, 'utf-8');

console.log(`\n✓ 迁移完成，已更新 ${linksFile}`);

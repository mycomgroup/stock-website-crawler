const fs = require('fs');
const path = require('path');

// 读取links.txt
const linksContent = fs.readFileSync('links.txt', 'utf8');
const urls = linksContent.split('\n').filter(line => line.includes('api-key='));

// 提取api-key
const apiKeys = urls.map(url => {
  const match = url.match(/api-key=([^&]+)/);
  return match ? decodeURIComponent(match[1]) : null;
}).filter(k => k);

// 读取已生成的文档
const docs = fs.readdirSync('api-docs').filter(f => f.endsWith('.md'));
const docKeys = docs.map(f => f.replace('.md', '').replace(/_/g, '/'));

// 找出缺失的
const missing = apiKeys.filter(key => {
  const filename = key.replace(/\//g, '_') + '.md';
  return !docs.includes(filename);
});

console.log('总URL数:', apiKeys.length);
console.log('已生成文档数:', docs.length);
console.log('缺失的API:');
missing.forEach(key => console.log('  -', key));

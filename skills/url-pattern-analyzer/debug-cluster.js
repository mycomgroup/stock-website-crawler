// 调试脚本：分析特定簇的市场分布
const fs = require('fs');

// 读取links.txt
const lines = fs.readFileSync('../../stock-crawler/output/lixinger-crawler/links.txt', 'utf-8').trim().split('\n');
const records = lines.map(line => JSON.parse(line));
const urls = records.filter(r => r.url).map(r => r.url);

// 过滤出 /analytics/index/detail/{market}/{code}/{id} 格式的URL
const pattern6 = urls.filter(url => {
  return url.includes('/analytics/index/detail/') && 
         !url.includes('?') &&
         !url.includes('/followed-users') &&
         !url.includes('/fund-list') &&
         !url.includes('/constituents') &&
         !url.includes('/fundamental');
});

console.log(`Total URLs matching pattern: ${pattern6.length}`);

// 统计市场分布
const markets = {};
pattern6.forEach(url => {
  const match = url.match(/\/analytics\/index\/detail\/([^\/]+)\//);
  if (match) {
    const market = match[1];
    markets[market] = (markets[market] || 0) + 1;
  }
});

console.log('\nMarket distribution:');
Object.entries(markets)
  .sort((a, b) => b[1] - a[1])
  .forEach(([market, count]) => {
    console.log(`  ${market}: ${count}`);
  });

console.log('\nSample URLs (first 3 per market):');
Object.keys(markets).forEach(market => {
  const samples = pattern6.filter(url => url.includes(`/detail/${market}/`)).slice(0, 3);
  console.log(`\n  ${market}:`);
  samples.forEach(s => console.log(`    ${s}`));
});

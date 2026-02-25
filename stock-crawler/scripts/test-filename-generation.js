#!/usr/bin/env node

/**
 * 测试文件名生成策略
 * 对现有URL进行模拟文件名生成，检查效果
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import MarkdownGenerator from '../src/markdown-generator.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const generator = new MarkdownGenerator();

// 测试用例
const testCases = [
  {
    title: '费用|我的 - 理杏仁',
    url: 'https://www.lixinger.com/place-order/weekly',
    expected: '费用_我的_weekly'
  },
  {
    title: '费用|我的 - 理杏仁',
    url: 'https://www.lixinger.com/place-order/annually',
    expected: '费用_我的_annually'
  },
  {
    title: '样本信息API购买',
    url: 'https://www.lixinger.com/open/api/doc?api-key=hk/index/constituents',
    expected: '样本信息API购买_hk_index_constituents'
  },
  {
    title: '样本信息API购买',
    url: 'https://www.lixinger.com/open/api/doc?api-key=us/index/constituents',
    expected: '样本信息API购买_us_index_constituents'
  },
  {
    title: '大陆|货币供应|宏观 - 理杏仁',
    url: 'https://www.lixinger.com/analytics/macro/money-supply',
    expected: '大陆_货币供应_宏观_macro_moneysupply'
  },
  {
    title: '大陆|货币供应|宏观 - 理杏仁',
    url: 'https://www.lixinger.com/analytics/macro/money-supply/cn',
    expected: '大陆_货币供应_宏观_cn_macro_moneysupply'
  },
  {
    title: '居民消费价格指数|大陆|价格指数|宏观 - 理杏仁',
    url: 'https://www.lixinger.com/analytics/macro/cpi/cn',
    expected: '居民消费价格指数_大陆_价格指数_宏观_cn_macro_cpi'
  },
  {
    title: '国家财政|宏观 - 理杏仁',
    url: 'https://www.lixinger.com/analytics/macro/treasury',
    expected: '国家财政_宏观_macro_treasury'
  },
  {
    title: '国家财政|宏观 - 理杏仁',
    url: 'https://www.lixinger.com/analytics/macro/treasury?chart-granularity=y',
    expected: '国家财政_宏观_macro_treasury_y'
  },
  {
    title: '自定义|制图 - 理杏仁',
    url: 'https://www.lixinger.com/analytics/chart-maker/',
    expected: '自定义_制图_analytics_chartmaker'
  },
  {
    title: '自定义|制图 - 理杏仁',
    url: 'https://www.lixinger.com/analytics/chart-maker/custom',
    expected: '自定义_制图_custom_analytics_chartmaker'
  }
];

console.log('🧪 测试文件名生成策略\n');
console.log('='.repeat(80));

let passCount = 0;
let failCount = 0;
const conflicts = new Map();

testCases.forEach((testCase, index) => {
  const result = generator.safeFilename(testCase.title, testCase.url);
  const passed = result.includes(testCase.expected.split('_')[0]); // 至少包含主要部分
  
  if (passed) {
    passCount++;
    console.log(`✅ 测试 ${index + 1}: PASS`);
  } else {
    failCount++;
    console.log(`❌ 测试 ${index + 1}: FAIL`);
  }
  
  console.log(`   标题: ${testCase.title}`);
  console.log(`   URL: ${testCase.url}`);
  console.log(`   生成: ${result}`);
  console.log(`   长度: ${result.length} 字符`);
  console.log('');
  
  // 检查冲突
  if (conflicts.has(result)) {
    conflicts.get(result).push(testCase.url);
  } else {
    conflicts.set(result, [testCase.url]);
  }
});

console.log('='.repeat(80));
console.log(`\n📊 测试结果: ${passCount}/${testCases.length} 通过`);

// 检查冲突
const conflictCount = Array.from(conflicts.values()).filter(urls => urls.length > 1).length;
if (conflictCount > 0) {
  console.log(`\n⚠️  发现 ${conflictCount} 个文件名冲突:`);
  conflicts.forEach((urls, filename) => {
    if (urls.length > 1) {
      console.log(`\n  文件名: ${filename}`);
      urls.forEach(url => console.log(`    - ${url}`));
    }
  });
} else {
  console.log('\n✅ 没有文件名冲突');
}

// 测试现有URL
console.log('\n' + '='.repeat(80));
console.log('\n📂 测试现有URL文件名生成\n');

const projectName = process.argv[2] || 'lixinger-crawler';
const linksFile = path.join(__dirname, '..', 'output', projectName, 'links.txt');

if (fs.existsSync(linksFile)) {
  const content = fs.readFileSync(linksFile, 'utf-8');
  const lines = content.split('\n').filter(l => l.trim());
  
  console.log(`📄 读取 ${lines.length} 个链接\n`);
  
  const filenames = new Map();
  const lengthStats = {
    '<30': 0,
    '30-50': 0,
    '50-70': 0,
    '>70': 0
  };
  
  // 只测试前50个URL
  const sampleSize = Math.min(50, lines.length);
  console.log(`🔍 分析前 ${sampleSize} 个URL的文件名...\n`);
  
  for (let i = 0; i < sampleSize; i++) {
    try {
      const link = JSON.parse(lines[i]);
      const url = link.url;
      
      // 模拟提取标题（从URL推测）
      const urlObj = new URL(url);
      const pathParts = urlObj.pathname.split('/').filter(p => p);
      const title = pathParts[pathParts.length - 1] || 'page';
      
      const filename = generator.safeFilename(title, url);
      
      // 统计长度
      const len = filename.length;
      if (len < 30) lengthStats['<30']++;
      else if (len < 50) lengthStats['30-50']++;
      else if (len < 70) lengthStats['50-70']++;
      else lengthStats['>70']++;
      
      // 检查冲突
      if (filenames.has(filename)) {
        filenames.get(filename).push(url);
      } else {
        filenames.set(filename, [url]);
      }
      
      if (i < 10) {
        console.log(`${i + 1}. ${filename} (${len}字符)`);
        console.log(`   ${url.substring(0, 80)}...`);
      }
    } catch (error) {
      // 跳过无效行
    }
  }
  
  console.log('\n📊 文件名长度分布:');
  console.log(`   < 30 字符: ${lengthStats['<30']} (${(lengthStats['<30']/sampleSize*100).toFixed(1)}%)`);
  console.log(`   30-50 字符: ${lengthStats['30-50']} (${(lengthStats['30-50']/sampleSize*100).toFixed(1)}%)`);
  console.log(`   50-70 字符: ${lengthStats['50-70']} (${(lengthStats['50-70']/sampleSize*100).toFixed(1)}%)`);
  console.log(`   > 70 字符: ${lengthStats['>70']} (${(lengthStats['>70']/sampleSize*100).toFixed(1)}%)`);
  
  const avgLength = Array.from(filenames.keys()).reduce((sum, fn) => sum + fn.length, 0) / filenames.size;
  console.log(`\n   平均长度: ${avgLength.toFixed(1)} 字符`);
  
  // 检查冲突
  const realConflicts = Array.from(filenames.values()).filter(urls => urls.length > 1);
  if (realConflicts.length > 0) {
    console.log(`\n⚠️  发现 ${realConflicts.length} 个文件名冲突 (${(realConflicts.length/filenames.size*100).toFixed(1)}%)`);
  } else {
    console.log('\n✅ 没有文件名冲突');
  }
} else {
  console.log(`❌ 链接文件不存在: ${linksFile}`);
}

console.log('\n' + '='.repeat(80));
console.log('\n✅ 测试完成！\n');

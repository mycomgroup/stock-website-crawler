#!/usr/bin/env node

import { DocGenerator } from '../lib/doc-generator.js';
import { PatternMatcher } from '../lib/pattern-matcher.js';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * 测试 Web API Generator Skill
 */
async function testSkill() {
  console.log('测试 Web API Generator Skill\n');

  const patternsPath = path.join(__dirname, '../../../stock-crawler/output/lixinger-crawler/url-patterns.json');
  
  if (!fs.existsSync(patternsPath)) {
    console.error(`错误: url-patterns.json 不存在: ${patternsPath}`);
    process.exit(1);
  }

  // 测试 1: Pattern Matcher
  console.log('测试 1: Pattern Matcher');
  const matcher = new PatternMatcher(patternsPath);
  console.log(`✓ 加载了 ${matcher.patterns.length} 个 patterns`);

  // 测试搜索
  const results = matcher.searchPatterns('公司详情');
  console.log(`✓ 搜索 "公司详情" 找到 ${results.length} 个结果`);
  if (results.length > 0) {
    console.log(`  第一个结果: ${results[0].name} - ${results[0].description}`);
  }

  // 测试 URL 构建
  if (results.length > 0) {
    const url = matcher.buildUrl(results[0], { param4: '600519', param5: '600519' });
    console.log(`✓ 构建 URL: ${url}`);
  }

  console.log('');

  // 测试 2: Doc Generator
  console.log('测试 2: Doc Generator');
  const outputDir = path.join(__dirname, '../output/test-docs');
  const generator = new DocGenerator(patternsPath, outputDir);
  
  // 只生成前 3 个文档作为测试
  const testPatterns = generator.patterns.slice(0, 3);
  console.log(`生成 ${testPatterns.length} 个测试文档...`);
  
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  for (const pattern of testPatterns) {
    generator.generateDoc(pattern);
    console.log(`✓ 生成文档: ${pattern.name}.md`);
  }

  console.log(`\n✓ 所有测试通过！`);
  console.log(`\n测试文档位置: ${outputDir}`);
}

testSkill().catch(error => {
  console.error('测试失败:', error);
  process.exit(1);
});

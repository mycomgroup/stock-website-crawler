#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * 将 url-patterns.json 转换为 API 文档格式
 */
class WebApiDocGenerator {
  constructor(patternsPath, outputDir) {
    this.patternsPath = patternsPath;
    this.outputDir = outputDir;
    
    const content = fs.readFileSync(patternsPath, 'utf-8');
    const data = JSON.parse(content);
    this.patterns = data.patterns || [];
  }

  /**
   * 生成所有文档
   */
  generateAll() {
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
    }

    console.log(`Generating API docs for ${this.patterns.length} patterns...\n`);

    let generated = 0;
    for (const pattern of this.patterns) {
      try {
        this.generateDoc(pattern);
        generated++;
      } catch (error) {
        console.error(`Error generating doc for ${pattern.name}:`, error.message);
      }
    }

    // 生成 README
    this.generateReadme();

    console.log(`\n✓ Generated ${generated} API docs in ${this.outputDir}`);
  }

  /**
   * 生成单个文档
   */
  generateDoc(pattern) {
    const filename = `${pattern.name}.md`;
    const filepath = path.join(this.outputDir, filename);

    const content = this.generateMarkdown(pattern);
    fs.writeFileSync(filepath, content);
  }

  /**
   * 生成 Markdown 内容
   */
  generateMarkdown(pattern) {
    const lines = [];

    // 标题
    lines.push(`# ${pattern.description || pattern.name}`);
    lines.push('');

    // 简要描述
    lines.push('## 简要描述');
    lines.push('');
    lines.push(pattern.description || '获取页面数据');
    lines.push('');

    // 请求URL
    lines.push('## 请求URL');
    lines.push('');
    lines.push('```');
    lines.push(pattern.samples[0]);
    lines.push('```');
    lines.push('');

    // URL 模式
    lines.push('## URL 模式');
    lines.push('');
    lines.push('```');
    lines.push(pattern.pathTemplate);
    lines.push('```');
    lines.push('');

    // 请求方式
    lines.push('## 请求方式');
    lines.push('');
    lines.push('GET (通过网页抓取)');
    lines.push('');

    // 参数
    lines.push('## 参数');
    lines.push('');
    
    const params = this.extractParameters(pattern);
    if (params.length > 0) {
      lines.push('| 参数名称 | 必选 | 数据类型 | 说明 |');
      lines.push('| -------- | ---- | -------- | ---- |');
      
      for (const param of params) {
        lines.push(`| ${param.name} | ${param.required ? 'Yes' : 'No'} | ${param.type} | ${param.description} |`);
      }
    } else {
      lines.push('无参数');
    }
    lines.push('');

    // 使用示例
    lines.push('## 使用示例');
    lines.push('');
    lines.push('```bash');
    lines.push(`node web-api-client.js ${pattern.name} ${this.generateExampleParams(params)}`);
    lines.push('```');
    lines.push('');

    // 示例 URL
    lines.push('## 示例 URL');
    lines.push('');
    for (let i = 0; i < Math.min(5, pattern.samples.length); i++) {
      lines.push(`- ${pattern.samples[i]}`);
    }
    lines.push('');

    // 返回数据说明
    lines.push('## 返回数据说明');
    lines.push('');
    lines.push('返回结构化的 JSON 数据，包含以下字段：');
    lines.push('');
    lines.push('| 参数名称 | 数据类型 | 说明 |');
    lines.push('| -------- | -------- | ---- |');
    lines.push('| type | String | 页面类型 |');
    lines.push('| url | String | 页面URL |');
    lines.push('| title | String | 页面标题 |');
    lines.push('| tables | Array | 表格数据 |');
    lines.push('| charts | Array | 图表数据 |');
    lines.push('| mainContent | Array | 主要内容 |');
    lines.push('');

    // 统计信息
    lines.push('## 统计信息');
    lines.push('');
    lines.push(`- 匹配的 URL 数量: ${pattern.urlCount}`);
    lines.push(`- 查询参数: ${pattern.queryParams.join(', ') || '无'}`);
    lines.push('');

    return lines.join('\n');
  }

  /**
   * 从 pattern 提取参数
   */
  extractParameters(pattern) {
    const params = [];

    // 提取路径参数
    const pathParams = pattern.pathTemplate.match(/\{([^}]+)\}/g) || [];
    for (const param of pathParams) {
      const name = param.replace(/[{}]/g, '');
      params.push({
        name,
        required: true,
        type: 'String',
        description: `路径参数 ${name}`
      });
    }

    // 提取查询参数
    for (const queryParam of pattern.queryParams) {
      params.push({
        name: queryParam,
        required: false,
        type: 'String',
        description: `查询参数 ${queryParam}`
      });
    }

    return params;
  }

  /**
   * 生成示例参数
   */
  generateExampleParams(params) {
    const required = params.filter(p => p.required);
    if (required.length === 0) {
      return '';
    }

    return required.map(p => `--${p.name}=value`).join(' ');
  }

  /**
   * 生成 README
   */
  generateReadme() {
    const lines = [];

    lines.push('# 理杏仁 Web API 文档');
    lines.push('');
    lines.push('本目录包含从 url-patterns.json 生成的 Web API 文档。');
    lines.push('');
    lines.push('## 说明');
    lines.push('');
    lines.push('这些 API 实际上是通过网页抓取实现的，但使用方式类似于标准 REST API。');
    lines.push('');
    lines.push('## 使用方法');
    lines.push('');
    lines.push('```bash');
    lines.push('# 查看所有可用 API');
    lines.push('node web-api-client.js list');
    lines.push('');
    lines.push('# 调用特定 API');
    lines.push('node web-api-client.js <api-name> [参数]');
    lines.push('');
    lines.push('# 示例');
    lines.push('node web-api-client.js detail-sh --param4=600519 --param5=600519');
    lines.push('```');
    lines.push('');

    lines.push('## API 分类');
    lines.push('');

    // 按分类组织
    const categories = {};
    for (const pattern of this.patterns) {
      const pathParts = pattern.pathTemplate.split('/').filter(p => p && !p.startsWith('{'));
      const category = pathParts[0] || 'other';

      if (!categories[category]) {
        categories[category] = [];
      }
      categories[category].push(pattern);
    }

    for (const [category, patterns] of Object.entries(categories)) {
      lines.push(`### ${category} (${patterns.length} APIs)`);
      lines.push('');
      
      for (const pattern of patterns.slice(0, 10)) {
        lines.push(`- [${pattern.name}](${pattern.name}.md) - ${pattern.description}`);
      }
      
      if (patterns.length > 10) {
        lines.push(`- ... 还有 ${patterns.length - 10} 个 API`);
      }
      lines.push('');
    }

    lines.push('## 统计');
    lines.push('');
    lines.push(`- 总 API 数: ${this.patterns.length}`);
    lines.push(`- 生成时间: ${new Date().toISOString()}`);
    lines.push('');

    fs.writeFileSync(path.join(this.outputDir, 'README.md'), lines.join('\n'));
  }
}

// 主程序
const patternsPath = path.join(__dirname, '../stock-crawler/output/lixinger-crawler/url-patterns.json');
const outputDir = path.join(__dirname, 'web-api-docs');

const generator = new WebApiDocGenerator(patternsPath, outputDir);
generator.generateAll();

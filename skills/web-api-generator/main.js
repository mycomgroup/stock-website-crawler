#!/usr/bin/env node

import { DocGenerator } from './lib/doc-generator.js';
import { WebApiClient } from './lib/api-client.js';
import { PatternMatcher } from './lib/pattern-matcher.js';
import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config({ path: path.join(__dirname, '../../.env') });

/**
 * Web API Generator Skill - 统一入口
 */
class WebApiGeneratorSkill {
  constructor() {
    this.commands = {
      'generate-docs': this.generateDocs.bind(this),
      'list': this.listApis.bind(this),
      'search': this.searchApis.bind(this),
      'call': this.callApi.bind(this)
    };
  }

  /**
   * 解析命令行参数
   */
  parseArgs(args) {
    const params = {};
    for (let i = 0; i < args.length; i++) {
      if (args[i].startsWith('--')) {
        const [key, value] = args[i].substring(2).split('=');
        params[key] = value || true;
      }
    }
    return params;
  }

  /**
   * 生成 API 文档
   */
  async generateDocs(params) {
    const patternsPath = params.patterns || path.join(__dirname, '../../stock-crawler/output/lixinger-crawler/url-patterns.json');
    const outputDir = params.output || path.join(__dirname, 'output/web-api-docs');

    console.log(`\n生成 API 文档...`);
    console.log(`Patterns: ${patternsPath}`);
    console.log(`Output: ${outputDir}\n`);

    const generator = new DocGenerator(patternsPath, outputDir);
    generator.generateAll();
  }

  /**
   * 列出所有 API
   */
  async listApis(params) {
    const patternsPath = params.patterns || path.join(__dirname, '../../stock-crawler/output/lixinger-crawler/url-patterns.json');
    
    const matcher = new PatternMatcher(patternsPath);
    const summary = matcher.getSummary();

    console.log('\n可用的 Web APIs:\n');
    for (const [category, patterns] of Object.entries(summary)) {
      console.log(`\n${category}:`);
      for (const pattern of patterns.slice(0, 5)) {
        console.log(`  - ${pattern.name}: ${pattern.description}`);
      }
      if (patterns.length > 5) {
        console.log(`  ... 还有 ${patterns.length - 5} 个`);
      }
    }
    console.log(`\n总计: ${matcher.patterns.length} 个 API\n`);
  }

  /**
   * 搜索 API
   */
  async searchApis(params) {
    if (!params.keyword) {
      console.error('错误: 请提供 --keyword 参数');
      process.exit(1);
    }

    const patternsPath = params.patterns || path.join(__dirname, '../../stock-crawler/output/lixinger-crawler/url-patterns.json');
    
    const matcher = new PatternMatcher(patternsPath);
    const results = matcher.searchPatterns(params.keyword);

    console.log(`\n找到 ${results.length} 个匹配的 API:\n`);
    for (const pattern of results.slice(0, 10)) {
      console.log(`- ${pattern.name}: ${pattern.description}`);
      console.log(`  示例: ${pattern.samples[0]}`);
      console.log('');
    }
  }

  /**
   * 调用 API
   */
  async callApi(params) {
    if (!params.api) {
      console.error('错误: 请提供 --api 参数');
      process.exit(1);
    }

    const patternsPath = params.patterns || path.join(__dirname, '../../stock-crawler/output/lixinger-crawler/url-patterns.json');
    const configPath = params.config || path.join(__dirname, 'output/web-api-docs/api-configs.json');
    const username = process.env.LIXINGER_USERNAME;
    const password = process.env.LIXINGER_PASSWORD;

    if (!username || !password) {
      console.error('错误: 请在 .env 文件中设置 LIXINGER_USERNAME 和 LIXINGER_PASSWORD');
      process.exit(1);
    }

    const client = new WebApiClient({
      patternsPath,
      configPath,
      username,
      password
    });

    try {
      await client.initialize();

      // 提取 API 参数
      const apiParams = {};
      for (const [key, value] of Object.entries(params)) {
        if (key !== 'api' && key !== 'patterns' && key !== 'config' && key !== 'output') {
          apiParams[key] = value;
        }
      }

      console.log(`\n调用 API: ${params.api}`);
      console.log(`参数:`, apiParams);
      console.log('');

      const result = await client.callApi(params.api, apiParams);
      
      console.log('\n结果:\n');
      
      // 根据输出格式显示
      if (result.outputFormat === 'csv' && result.data.tables && result.data.tables.length > 0) {
        console.log('CSV 格式输出:\n');
        for (let i = 0; i < result.data.tables.length; i++) {
          console.log(`表格 ${i + 1}:`);
          console.log(result.data.tables[i].csv);
          console.log('');
        }
        
        // 保存 CSV 文件
        if (params.output !== false) {
          const outputFile = params.output || `output-${params.api}-${Date.now()}.csv`;
          fs.writeFileSync(outputFile, result.data.tables[0].csv);
          console.log(`已保存到: ${outputFile}\n`);
        }
      } else {
        console.log(JSON.stringify(result, null, 2));
        
        // 保存 JSON 文件
        if (params.output !== false) {
          const outputFile = params.output || `output-${params.api}-${Date.now()}.json`;
          fs.writeFileSync(outputFile, JSON.stringify(result, null, 2));
          console.log(`\n已保存到: ${outputFile}\n`);
        }
      }

      await client.close();
    } catch (error) {
      console.error('\n错误:', error.message);
      await client.close();
      process.exit(1);
    }
  }

  /**
   * 显示帮助
   */
  showHelp() {
    console.log(`
Web API Generator Skill

使用方法:
  node main.js <command> [options]

命令:
  generate-docs    生成 API 文档
  list            列出所有 API
  search          搜索 API
  call            调用 API

选项:
  --patterns=<path>    url-patterns.json 文件路径
  --output=<path>      输出目录（仅用于 generate-docs）或输出文件（用于 call）
  --config=<path>      API 配置文件路径（用于 call）
  --keyword=<text>     搜索关键词（仅用于 search）
  --api=<name>         API 名称（仅用于 call）
  --param*=<value>     API 参数（仅用于 call）

示例:
  # 生成文档
  node main.js generate-docs --output=./output/docs

  # 列出所有 API
  node main.js list

  # 搜索 API
  node main.js search --keyword=公司详情

  # 调用 API
  node main.js call --api=detail-sh --param4=600519 --param5=600519
    `);
  }

  /**
   * 运行
   */
  async run(args) {
    if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
      this.showHelp();
      return;
    }

    const command = args[0];
    const params = this.parseArgs(args.slice(1));

    if (!this.commands[command]) {
      console.error(`错误: 未知命令 "${command}"`);
      this.showHelp();
      process.exit(1);
    }

    await this.commands[command](params);
  }
}

// 主程序
const skill = new WebApiGeneratorSkill();
skill.run(process.argv.slice(2)).catch(error => {
  console.error('错误:', error);
  process.exit(1);
});

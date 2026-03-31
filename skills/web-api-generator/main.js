#!/usr/bin/env node

import { DocGenerator } from './lib/doc-generator.js';
import { WebApiClient } from './lib/api-client.js';
import { PatternMatcher } from './lib/pattern-matcher.js';
import { FieldInferenceService } from './lib/field-inference.js';
import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs';
import readline from 'readline';
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
      'call': this.callApi.bind(this),
      'interactive': this.interactiveCall.bind(this)
    };
  }

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

  getPaths(params) {
    return {
      patternsPath: this.validatePath(params.patterns, path.join(__dirname, '../../stock-crawler/output/lixinger-crawler/url-patterns.json')),
      configPath: this.validatePath(params.config, path.join(__dirname, 'output/web-api-docs/api-configs.json'))
    };
  }

  createClient(paths) {
    const username = process.env.LIXINGER_USERNAME;
    const password = process.env.LIXINGER_PASSWORD;

    if (!username || !password) {
      throw new Error('请在 .env 文件中设置 LIXINGER_USERNAME 和 LIXINGER_PASSWORD');
    }

    return new WebApiClient({
      patternsPath: paths.patternsPath,
      configPath: paths.configPath,
      username,
      password
    });
  }

  createFieldInferenceService(params = {}) {
    const useLLM = params.useLLM !== 'false';
    return new FieldInferenceService({ enabled: useLLM });
  }

  validatePath(inputPath, defaultPath) {
    if (!inputPath) return defaultPath;
    const resolved = path.resolve(inputPath);
    const cwd = process.cwd();
    if (!resolved.startsWith(cwd) && !resolved.startsWith(path.join(__dirname, '..'))) {
      throw new Error(`路径遍历攻击检测: ${inputPath} 不在允许的目录范围内`);
    }
    return resolved;
  }

  async generateDocs(params) {
    const patternsPath = this.validatePath(params.patterns, path.join(__dirname, '../../stock-crawler/output/lixinger-crawler/url-patterns.json'));
    const outputDir = this.validatePath(params.output, path.join(__dirname, 'output/web-api-docs'));

    console.log(`\n生成 API 文档...`);
    console.log(`Patterns: ${patternsPath}`);
    console.log(`Output: ${outputDir}\n`);

    const generator = new DocGenerator(patternsPath, outputDir);
    await generator.generateAll();
  }

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

  async executeApiCall(params, options = {}) {
    const { patternsPath, configPath } = this.getPaths(params);
    const client = this.createClient({ patternsPath, configPath });

    try {
      await client.initialize();
      const result = await client.callApi(params.api, options.apiParams || {});
      if (!options.silent) {
        this.printResult(result, params);
      }
      return result;
    } finally {
      await client.close();
    }
  }

  printResult(result, params = {}) {
    console.log('\n结果:\n');

    if (result.outputFormat === 'csv' && result.data.tables && result.data.tables.length > 0) {
      console.log('CSV 格式输出:\n');
      for (let i = 0; i < result.data.tables.length; i++) {
        console.log(`表格 ${i + 1}:`);
        console.log(result.data.tables[i].csv);
        console.log('');
      }

      if (params.output !== false) {
        const outputFile = params.output || `output-${result.api}-${Date.now()}.csv`;
        fs.writeFileSync(outputFile, result.data.tables[0].csv);
        console.log(`已保存到: ${outputFile}\n`);
      }
      return;
    }

    console.log(JSON.stringify(result, null, 2));
    if (params.output !== false) {
      const outputFile = params.output || `output-${result.api}-${Date.now()}.json`;
      fs.writeFileSync(outputFile, JSON.stringify(result, null, 2));
      console.log(`\n已保存到: ${outputFile}\n`);
    }
  }

  async callApi(params) {
    if (!params.api) {
      console.error('错误: 请提供 --api 参数');
      process.exit(1);
    }

    const apiParams = {};
    for (const [key, value] of Object.entries(params)) {
      if (!['api', 'patterns', 'config', 'output', 'useLLM'].includes(key)) {
        apiParams[key] = value;
      }
    }

    console.log(`\n调用 API: ${params.api}`);
    console.log('参数:', apiParams);
    console.log('');

    try {
      await this.executeApiCall(params, { apiParams });
    } catch (error) {
      console.error('\n错误:', error.message);
      process.exit(1);
    }
  }

  createReadline() {
    return readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
  }

  async ask(rl, question) {
    return new Promise(resolve => {
      rl.question(question, answer => resolve(answer.trim()));
    });
  }

  async interactiveCall(params) {
    const { patternsPath } = this.getPaths(params);
    const matcher = new PatternMatcher(patternsPath);
    const fieldInference = this.createFieldInferenceService(params);
    const rl = this.createReadline();
    let exitCode = 0;

    try {
      console.log('\n=== 交互式 Web API 调用 ===');
      console.log('你可以输入 URL 类型 / 业务关键词，系统会推荐 API 并自动推导字段含义。\n');

      const query = await this.ask(rl, '请输入 URL 类型（例如 company/detail、fund、行业）: ');
      const candidates = matcher.findByUrlType(query || '');

      if (candidates.length === 0) {
        console.log('未找到匹配 API，请改用 search 命令进一步筛选。');
        return;
      }

      console.log('\n推荐 API:');
      candidates.slice(0, 8).forEach((item, index) => {
        console.log(`${index + 1}. ${item.name} - ${item.description}`);
        console.log(`   ${item.pathTemplate}`);
      });

      const selected = await this.ask(rl, '\n选择 API 编号（默认 1）: ');
      const selectedIndex = Math.max(1, parseInt(selected || '1', 10)) - 1;
      const pattern = candidates[selectedIndex] || candidates[0];

      console.log(`\n已选择: ${pattern.name}`);
      const paramNames = matcher.getPathParamNames(pattern);
      const apiParams = {};

      if (paramNames.length > 0) {
        const inferred = await fieldInference.inferFieldMeanings({
          userQuery: query,
          pattern: {
            name: pattern.name,
            description: pattern.description,
            pathTemplate: pattern.pathTemplate,
            samples: pattern.samples?.slice(0, 3) || []
          },
          paramNames
        });

        console.log(`\n字段语义推导来源: ${inferred.source}${inferred.note ? ` (${inferred.note})` : ''}`);
        for (const field of inferred.fields) {
          const tip = `${field.name}（${field.meaning}${field.suggestedValue ? `，建议值: ${field.suggestedValue}` : ''}）`;
          const answer = await this.ask(rl, `参数 ${tip}: `);
          if (answer) {
            apiParams[field.name] = answer;
          } else if (field.suggestedValue) {
            apiParams[field.name] = field.suggestedValue;
            console.log(`  使用建议值: ${field.suggestedValue}`);
          }
        }
      }

      const autoCall = await this.ask(rl, '确认调用？[Y/n]: ');
      if (autoCall.toLowerCase() === 'n') {
        console.log('已取消调用。');
        return;
      }

      const callParams = {
        ...params,
        api: pattern.name,
        output: params.output || false
      };

      console.log(`\n调用 API: ${pattern.name}`);
      console.log(`参数: ${JSON.stringify(apiParams)}\n`);

      const result = await this.executeApiCall(callParams, { apiParams, silent: true });
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('\n交互调用失败:', error.message);
      exitCode = 1;
    } finally {
      rl.close();
    }
    
    if (exitCode !== 0) {
      process.exit(exitCode);
    }
  }

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
  interactive     交互式调用（按 URL 类型推荐 API + 字段语义推导）

选项:
  --patterns=<path>    url-patterns.json 文件路径
  --output=<path>      输出目录（仅用于 generate-docs）或输出文件（用于 call）
  --config=<path>      API 配置文件路径（用于 call）
  --keyword=<text>     搜索关键词（仅用于 search）
  --api=<name>         API 名称（仅用于 call）
  --param*=<value>     API 参数（仅用于 call）
  --useLLM=false       关闭大模型推导（interactive）

LLM 环境变量（可选）:
  LLM_API_KEY / OPENAI_API_KEY
  LLM_API_BASE_URL / OPENAI_BASE_URL
  LLM_MODEL / OPENAI_MODEL

示例:
  node main.js interactive --useLLM=false
    `);
  }

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

const skill = new WebApiGeneratorSkill();
skill.run(process.argv.slice(2)).catch(error => {
  console.error('错误:', error);
  process.exit(1);
});

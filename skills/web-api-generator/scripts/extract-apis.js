#!/usr/bin/env node
/**
 * 从 HAR 文件提取 API 并生成代码
 */

import { HARParser } from '../lib/har-parser.js';
import { RequestGenerator } from '../lib/request-generator.js';
import fs from 'fs';
import path from 'path';

class APIExtractor {
  constructor(harPath, outputDir) {
    this.harPath = harPath;
    this.outputDir = outputDir;
    this.parser = new HARParser(harPath);
    this.generator = new RequestGenerator(this.parser);
  }

  /**
   * 执行提取
   */
  async extract(options = {}) {
    const {
      formats = ['python', 'node', 'curl'],
      generateClass = true,
      generateDocs = true
    } = options;

    console.log(`加载 HAR 文件: ${this.harPath}`);
    
    if (!this.parser.load()) {
      throw new Error('加载 HAR 文件失败');
    }

    const stats = this.parser.getStats();
    console.log(`\n统计信息:`);
    console.log(`- 总请求数: ${stats.totalRequests}`);
    console.log(`- API 请求数: ${stats.apiRequests}`);
    console.log(`- 域名数: ${stats.domains}`);
    console.log(`- 方法分布: ${JSON.stringify(stats.methods)}`);
    console.log();

    // 创建输出目录
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
    }

    // 生成各种格式的代码
    for (const format of formats) {
      await this.generateCode(format);
    }

    // 生成类
    if (generateClass) {
      await this.generateClasses();
    }

    // 生成文档
    if (generateDocs) {
      await this.generateDocumentation();
    }

    // 导出原始数据
    this.exportRawData();

    console.log(`\n✅ 提取完成！输出目录: ${this.outputDir}`);
  }

  /**
   * 生成指定格式的代码
   */
  async generateCode(format) {
    console.log(`生成 ${format} 代码...`);
    
    const codes = this.generator.generateAll(format);
    const formatDir = path.join(this.outputDir, format);
    
    if (!fs.existsSync(formatDir)) {
      fs.mkdirSync(formatDir, { recursive: true });
    }

    codes.forEach((item) => {
      const ext = this.getFileExtension(format);
      const filename = `api_${item.index}_${item.name}.${ext}`;
      const filepath = path.join(formatDir, filename);
      
      fs.writeFileSync(filepath, item.code);
    });

    console.log(`  ✓ 生成了 ${codes.length} 个文件`);
  }

  /**
   * 生成类文件
   */
  async generateClasses() {
    console.log(`生成 API 类...`);
    
    const apis = this.parser.extractDataAPIs();
    
    // Python 类
    const pythonClass = this.generator.generatePythonClass(apis);
    const pythonPath = path.join(this.outputDir, 'api_client.py');
    fs.writeFileSync(pythonPath, pythonClass);
    
    console.log(`  ✓ Python 类: api_client.py`);
  }

  /**
   * 生成文档
   */
  async generateDocumentation() {
    console.log(`生成文档...`);
    
    const apis = this.parser.extractDataAPIs();
    const categorized = this.parser.categorizeAPIs();
    const grouped = this.parser.groupByDomain();
    
    let md = `# API 提取报告\n\n`;
    md += `生成时间: ${new Date().toLocaleString()}\n\n`;
    
    md += `## 统计\n\n`;
    md += `- 总计: ${categorized.total} 个接口\n`;
    md += `- REST API: ${categorized.restCount} 个\n`;
    md += `- GraphQL: ${categorized.graphqlCount} 个\n`;
    md += `- 域名数: ${Object.keys(grouped).length}\n\n`;
    
    md += `## 按域名分组\n\n`;
    Object.entries(grouped).forEach(([domain, entries]) => {
      md += `### ${domain} (${entries.length})\n\n`;
      entries.forEach((entry, index) => {
        const details = this.parser.extractRequestDetails(entry);
        md += `${index + 1}. **${details.method}** ${details.url}\n`;
        
        // 检测签名
        const sig = this.parser.detectSignature(entry);
        if (sig.found) {
          md += `   - ⚠️ 检测到签名: ${sig.key} (${sig.location})\n`;
        }
      });
      md += `\n`;
    });
    
    md += `## 接口列表\n\n`;
    apis.forEach((entry, index) => {
      const details = this.parser.extractRequestDetails(entry);
      
      md += `### ${index + 1}. ${details.method} ${this.generator.extractAPIName(details.url)}\n\n`;
      md += `- URL: \`${details.url}\`\n`;
      md += `- 方法: ${details.method}\n`;
      md += `- 状态: ${details.status}\n`;
      
      if (Object.keys(details.queryParams).length > 0) {
        md += `- 查询参数:\n`;
        Object.entries(details.queryParams).forEach(([key, value]) => {
          md += `  - \`${key}\`: ${value}\n`;
        });
      }
      
      if (details.postData) {
        md += `- 请求体:\n\`\`\`json\n${this.formatJSON(details.postData)}\n\`\`\`\n`;
      }
      
      md += `\n`;
    });
    
    const docPath = path.join(this.outputDir, 'README.md');
    fs.writeFileSync(docPath, md);
    
    console.log(`  ✓ 文档: README.md`);
  }

  /**
   * 导出原始数据
   */
  exportRawData() {
    const jsonPath = path.join(this.outputDir, 'apis.json');
    this.parser.exportToJSON(jsonPath);
  }

  /**
   * 获取文件扩展名
   */
  getFileExtension(format) {
    const extensions = {
      python: 'py',
      node: 'js',
      curl: 'sh',
      fetch: 'js'
    };
    return extensions[format] || 'txt';
  }

  /**
   * 格式化 JSON
   */
  formatJSON(str) {
    try {
      return JSON.stringify(JSON.parse(str), null, 2);
    } catch {
      return str;
    }
  }
}

// CLI 使用
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log(`
使用方法:
  node extract-apis.js <har-file> <output-dir> [options]

示例:
  node extract-apis.js output/example.har output/apis
  node extract-apis.js output/example.har output/apis --formats python,node

选项:
  --formats <list>  生成的代码格式，逗号分隔 (默认: python,node,curl)
  --no-class        不生成类文件
  --no-docs         不生成文档
    `);
    process.exit(1);
  }
  
  const [harFile, outputDir] = args;
  
  // 解析选项
  const options = {
    formats: ['python', 'node', 'curl'],
    generateClass: true,
    generateDocs: true
  };
  
  for (let i = 2; i < args.length; i++) {
    if (args[i] === '--formats' && args[i + 1]) {
      options.formats = args[i + 1].split(',');
      i++;
    } else if (args[i] === '--no-class') {
      options.generateClass = false;
    } else if (args[i] === '--no-docs') {
      options.generateDocs = false;
    }
  }
  
  const extractor = new APIExtractor(harFile, outputDir);
  extractor.extract(options).catch(error => {
    console.error('错误:', error);
    process.exit(1);
  });
}

export { APIExtractor };

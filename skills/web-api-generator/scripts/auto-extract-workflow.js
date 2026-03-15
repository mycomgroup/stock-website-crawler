#!/usr/bin/env node
/**
 * 完整的自动化工作流
 * 录制 HAR -> 提取 API -> 验证 -> 生成代码
 */

import { recordHAR } from './record-har.js';
import { APIExtractor } from './extract-apis.js';
import { validateAPIs } from './validate-apis.js';
import fs from 'fs';
import path from 'path';

class AutoExtractWorkflow {
  constructor(config) {
    this.config = {
      outputDir: 'output/har-extraction',
      formats: ['python', 'node', 'curl'],
      validate: true,
      ...config
    };
  }

  /**
   * 执行完整工作流
   */
  async run(url, name) {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`开始自动提取工作流: ${name}`);
    console.log(`URL: ${url}`);
    console.log(`${'='.repeat(60)}\n`);

    const baseDir = path.join(this.config.outputDir, name);
    if (!fs.existsSync(baseDir)) {
      fs.mkdirSync(baseDir, { recursive: true });
    }

    const harPath = path.join(baseDir, `${name}.har`);
    const apisDir = path.join(baseDir, 'apis');

    try {
      // 步骤 1: 录制 HAR
      console.log(`\n[1/4] 录制 HAR 文件...`);
      await recordHAR(url, harPath, {
        waitTime: this.config.waitTime || 3000
      });

      // 步骤 2: 提取 API
      console.log(`\n[2/4] 提取 API...`);
      const extractor = new APIExtractor(harPath, apisDir);
      await extractor.extract({
        formats: this.config.formats,
        generateClass: true,
        generateDocs: true
      });

      // 步骤 3: 验证（可选）
      if (this.config.validate) {
        console.log(`\n[3/4] 验证 API...`);
        try {
          await validateAPIs(harPath, {
            maxConcurrent: 3,
            delay: 1000,
            outputReport: true
          });
        } catch (error) {
          console.warn(`验证失败: ${error.message}`);
        }
      } else {
        console.log(`\n[3/4] 跳过验证`);
      }

      // 步骤 4: 生成总结
      console.log(`\n[4/4] 生成总结...`);
      this.generateSummary(baseDir, name, url);

      console.log(`\n${'='.repeat(60)}`);
      console.log(`✅ 工作流完成！`);
      console.log(`输出目录: ${baseDir}`);
      console.log(`${'='.repeat(60)}\n`);

      return {
        success: true,
        outputDir: baseDir,
        harPath,
        apisDir
      };

    } catch (error) {
      console.error(`\n❌ 工作流失败: ${error.message}`);
      throw error;
    }
  }

  /**
   * 批量处理多个 URL
   */
  async batchRun(urls) {
    const results = [];

    for (const { url, name } of urls) {
      try {
        const result = await this.run(url, name);
        results.push({ name, success: true, ...result });
      } catch (error) {
        results.push({ name, success: false, error: error.message });
      }

      // 间隔避免请求过快
      await new Promise(resolve => setTimeout(resolve, 2000));
    }

    // 生成批量报告
    this.generateBatchReport(results);

    return results;
  }

  /**
   * 生成总结文档
   */
  generateSummary(baseDir, name, url) {
    const apisJsonPath = path.join(baseDir, 'apis', 'apis.json');
    const validationPath = path.join(baseDir, 'validation-report.json');

    let md = `# ${name} - API 提取总结\n\n`;
    md += `生成时间: ${new Date().toLocaleString()}\n\n`;
    md += `## 源信息\n\n`;
    md += `- URL: ${url}\n`;
    md += `- HAR 文件: ${name}.har\n\n`;

    // API 统计
    if (fs.existsSync(apisJsonPath)) {
      const data = JSON.parse(fs.readFileSync(apisJsonPath, 'utf8'));
      md += `## API 统计\n\n`;
      md += `- 总请求数: ${data.metadata.stats.totalRequests}\n`;
      md += `- API 数量: ${data.metadata.stats.apiRequests}\n`;
      md += `- 域名数: ${data.metadata.stats.domains}\n\n`;
    }

    // 验证结果
    if (fs.existsSync(validationPath)) {
      const validation = JSON.parse(fs.readFileSync(validationPath, 'utf8'));
      md += `## 验证结果\n\n`;
      md += `- 成功率: ${validation.summary.successRate}\n`;
      md += `- 直连率: ${validation.summary.bypassRate}\n`;
      md += `- 可直连: ${validation.summary.canBypass}/${validation.summary.total}\n\n`;
    }

    md += `## 生成的文件\n\n`;
    md += `### 代码文件\n\n`;
    this.config.formats.forEach(format => {
      md += `- \`apis/${format}/\` - ${format.toUpperCase()} 代码\n`;
    });
    md += `- \`apis/api_client.py\` - Python API 客户端类\n\n`;

    md += `### 文档\n\n`;
    md += `- \`apis/README.md\` - API 详细文档\n`;
    md += `- \`apis/apis.json\` - 原始 API 数据\n`;
    if (fs.existsSync(validationPath)) {
      md += `- \`validation-report.md\` - 验证报告\n`;
    }

    md += `\n## 使用方法\n\n`;
    md += `### Python\n\n`;
    md += `\`\`\`python\n`;
    md += `from api_client import APIClient\n\n`;
    md += `client = APIClient(base_url="...", headers={...})\n`;
    md += `result = client.some_method()\n`;
    md += `\`\`\`\n\n`;

    md += `### Node.js\n\n`;
    md += `\`\`\`javascript\n`;
    md += `import axios from 'axios';\n`;
    md += `// 参考 apis/node/ 目录中的代码\n`;
    md += `\`\`\`\n\n`;

    md += `### curl\n\n`;
    md += `\`\`\`bash\n`;
    md += `# 参考 apis/curl/ 目录中的脚本\n`;
    md += `bash apis/curl/api_1_*.sh\n`;
    md += `\`\`\`\n`;

    const summaryPath = path.join(baseDir, 'SUMMARY.md');
    fs.writeFileSync(summaryPath, md);
  }

  /**
   * 生成批量报告
   */
  generateBatchReport(results) {
    const reportPath = path.join(this.config.outputDir, 'BATCH_REPORT.md');

    let md = `# 批量提取报告\n\n`;
    md += `生成时间: ${new Date().toLocaleString()}\n\n`;

    const success = results.filter(r => r.success).length;
    const failed = results.filter(r => !r.success).length;

    md += `## 概览\n\n`;
    md += `- 总计: ${results.length}\n`;
    md += `- 成功: ${success}\n`;
    md += `- 失败: ${failed}\n\n`;

    md += `## 详细结果\n\n`;
    results.forEach((result, index) => {
      md += `### ${index + 1}. ${result.name}\n\n`;
      if (result.success) {
        md += `- 状态: ✅ 成功\n`;
        md += `- 输出: ${result.outputDir}\n`;
      } else {
        md += `- 状态: ❌ 失败\n`;
        md += `- 错误: ${result.error}\n`;
      }
      md += `\n`;
    });

    fs.writeFileSync(reportPath, md);
    console.log(`\n批量报告: ${reportPath}`);
  }
}

// CLI 使用
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log(`
使用方法:
  node auto-extract-workflow.js <url> <name> [options]

示例:
  node auto-extract-workflow.js https://example.com/api example
  node auto-extract-workflow.js https://example.com/api example --no-validate

选项:
  --output <dir>    输出目录 (默认: output/har-extraction)
  --formats <list>  代码格式 (默认: python,node,curl)
  --no-validate     跳过验证步骤
  --wait <ms>       等待时间 (默认: 3000)

批量模式:
  node auto-extract-workflow.js --batch urls.json
  
  urls.json 格式:
  [
    { "url": "https://example.com/api1", "name": "api1" },
    { "url": "https://example.com/api2", "name": "api2" }
  ]
    `);
    process.exit(1);
  }

  // 批量模式
  if (args[0] === '--batch' && args[1]) {
    const urlsFile = args[1];
    const urls = JSON.parse(fs.readFileSync(urlsFile, 'utf8'));
    
    const workflow = new AutoExtractWorkflow({
      outputDir: 'output/har-extraction',
      formats: ['python', 'node', 'curl'],
      validate: true
    });
    
    workflow.batchRun(urls).catch(error => {
      console.error('错误:', error);
      process.exit(1);
    });
    
  } else {
    // 单个模式
    const [url, name] = args;
    
    const config = {
      outputDir: 'output/har-extraction',
      formats: ['python', 'node', 'curl'],
      validate: true,
      waitTime: 3000
    };
    
    for (let i = 2; i < args.length; i++) {
      if (args[i] === '--output' && args[i + 1]) {
        config.outputDir = args[i + 1];
        i++;
      } else if (args[i] === '--formats' && args[i + 1]) {
        config.formats = args[i + 1].split(',');
        i++;
      } else if (args[i] === '--no-validate') {
        config.validate = false;
      } else if (args[i] === '--wait' && args[i + 1]) {
        config.waitTime = parseInt(args[i + 1]);
        i++;
      }
    }
    
    const workflow = new AutoExtractWorkflow(config);
    workflow.run(url, name).catch(error => {
      console.error('错误:', error);
      process.exit(1);
    });
  }
}

export { AutoExtractWorkflow };

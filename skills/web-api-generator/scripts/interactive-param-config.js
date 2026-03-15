#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import readline from 'readline';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * 交互式参数配置工具
 * 用于补充参数的取值范围和默认值
 */
class InteractiveParamConfig {
  constructor(configPath) {
    this.configPath = configPath;
    this.configs = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
  }

  /**
   * 询问用户问题
   */
  async ask(question) {
    return new Promise((resolve) => {
      this.rl.question(question, (answer) => {
        resolve(answer.trim());
      });
    });
  }

  /**
   * 运行交互式配置
   */
  async run() {
    console.log('='.repeat(60));
    console.log('交互式参数配置工具');
    console.log('='.repeat(60));
    console.log('');
    console.log('此工具帮助您为 API 参数添加取值范围和默认值');
    console.log('如果参数已有取值范围，可以直接跳过（按回车）');
    console.log('');

    // 筛选需要配置的 API
    const needsConfig = this.configs.filter(config => {
      return config.parameters.some(p => 
        p.required && (!p.valueRange || p.valueRange === '请参考示例')
      );
    });

    console.log(`找到 ${needsConfig.length} 个 API 需要配置参数取值范围\n`);

    const mode = await this.ask('选择模式: (1) 配置所有 (2) 选择性配置 [1/2]: ');
    
    if (mode === '2') {
      await this.selectiveConfig(needsConfig);
    } else {
      await this.configAll(needsConfig);
    }

    // 保存配置
    await this.saveConfig();
    
    this.rl.close();
  }

  /**
   * 配置所有 API
   */
  async configAll(needsConfig) {
    for (let i = 0; i < needsConfig.length; i++) {
      const config = needsConfig[i];
      console.log(`\n[${i + 1}/${needsConfig.length}] API: ${config.api}`);
      console.log(`描述: ${config.description}`);
      console.log(`样本: ${config.samples[0]}`);
      console.log('');

      await this.configApiParams(config);
    }
  }

  /**
   * 选择性配置
   */
  async selectiveConfig(needsConfig) {
    console.log('\n可配置的 API 列表:');
    needsConfig.forEach((config, index) => {
      console.log(`  ${index + 1}. ${config.api} - ${config.description}`);
    });
    console.log('');

    const selection = await this.ask('输入要配置的 API 编号（用逗号分隔，如: 1,3,5）: ');
    const indices = selection.split(',').map(s => parseInt(s.trim()) - 1);

    for (const index of indices) {
      if (index >= 0 && index < needsConfig.length) {
        const config = needsConfig[index];
        console.log(`\n配置 API: ${config.api}`);
        console.log(`描述: ${config.description}`);
        console.log(`样本: ${config.samples[0]}`);
        console.log('');

        await this.configApiParams(config);
      }
    }
  }

  /**
   * 配置单个 API 的参数
   */
  async configApiParams(config) {
    for (const param of config.parameters) {
      if (!param.required) continue;
      
      if (param.valueRange && param.valueRange !== '请参考示例') {
        console.log(`  参数 ${param.name}: ${param.valueRange} (已有取值范围，跳过)`);
        continue;
      }

      console.log(`  参数: ${param.name}`);
      console.log(`  说明: ${param.description}`);
      
      // 显示样本值
      const sampleValues = this.extractSampleValues(config, param.name);
      if (sampleValues.length > 0) {
        console.log(`  样本值: ${sampleValues.slice(0, 5).join(', ')}`);
      }

      const valueRange = await this.ask(`  取值范围 (直接回车跳过): `);
      
      if (valueRange) {
        param.valueRange = valueRange;
        console.log(`  ✓ 已设置取值范围: ${valueRange}`);
      } else {
        console.log(`  - 跳过`);
      }
      console.log('');
    }
  }

  /**
   * 从样本中提取参数值
   */
  extractSampleValues(config, paramName) {
    const values = [];
    
    for (const sample of config.samples.slice(0, 5)) {
      const regex = new RegExp(config.pattern);
      const match = sample.match(regex);
      
      if (!match) continue;
      
      const paramValues = match.slice(1).filter(v => v !== undefined && !v.startsWith('?'));
      
      // 简单匹配：假设参数按顺序出现
      const pathParams = config.pathTemplate.match(/\{([^}]+)\}/g) || [];
      const paramIndex = pathParams.findIndex(p => {
        const name = p.replace(/[{}]/g, '');
        return name === paramName || this.inferName(name) === paramName;
      });
      
      if (paramIndex >= 0 && paramIndex < paramValues.length) {
        values.push(paramValues[paramIndex]);
      }
    }
    
    return values;
  }

  /**
   * 简单的参数名推断
   */
  inferName(rawName) {
    // 简化版本，实际应该与 doc-generator.js 保持一致
    return rawName;
  }

  /**
   * 保存配置
   */
  async saveConfig() {
    const save = await this.ask('\n保存配置? [Y/n]: ');
    
    if (save.toLowerCase() !== 'n') {
      // 备份原文件
      const backupPath = this.configPath + '.backup';
      fs.copyFileSync(this.configPath, backupPath);
      console.log(`✓ 已备份原配置到: ${backupPath}`);
      
      // 保存新配置
      fs.writeFileSync(this.configPath, JSON.stringify(this.configs, null, 2));
      console.log(`✓ 已保存配置到: ${this.configPath}`);
      
      // 同时保存 JSONL 格式
      const jsonlPath = this.configPath.replace('.json', '.jsonl');
      const lines = this.configs.map(config => JSON.stringify(config));
      fs.writeFileSync(jsonlPath, lines.join('\n'));
      console.log(`✓ 已保存 JSONL 格式到: ${jsonlPath}`);
    } else {
      console.log('✗ 未保存配置');
    }
  }
}

// 主程序
async function main() {
  const configPath = process.argv[2] || path.join(__dirname, '../output/web-api-docs/api-configs.json');
  
  if (!fs.existsSync(configPath)) {
    console.error(`错误: 配置文件不存在: ${configPath}`);
    console.error('用法: node interactive-param-config.js [配置文件路径]');
    process.exit(1);
  }

  const tool = new InteractiveParamConfig(configPath);
  await tool.run();
}

main().catch(console.error);

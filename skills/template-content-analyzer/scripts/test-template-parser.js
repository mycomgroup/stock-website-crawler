#!/usr/bin/env node

/**
 * 测试脚本：验证配置驱动的TemplateParser
 * 
 * 任务 5.5: 验证配置效果（不集成到爬虫系统）
 * - 5.5.1 创建独立测试脚本 ✓
 * - 5.5.2 加载配置文件 ✓
 * - 5.5.3 创建TemplateParser实例 ✓
 * - 5.5.4 测试配置驱动的解析
 * 
 * 用法：
 *   node scripts/test-template-parser.js [config-file]
 * 
 * 示例：
 *   node scripts/test-template-parser.js examples/template-config.jsonl
 */

const ConfigLoader = require('../lib/config-loader');
const TemplateParser = require('../lib/template-parser');
const path = require('path');
const fs = require('fs');

/**
 * 主函数
 */
async function main() {
  console.log('='.repeat(60));
  console.log('TemplateParser 配置驱动测试');
  console.log('='.repeat(60));
  console.log();

  // 1. 解析命令行参数
  const args = process.argv.slice(2);
  let configPath = args[0];

  // 如果没有提供配置文件，使用示例配置
  if (!configPath) {
    configPath = path.join(__dirname, '../examples/template-config.jsonl');
    console.log(`未指定配置文件，使用示例配置: ${configPath}`);
  } else {
    console.log(`使用配置文件: ${configPath}`);
  }
  console.log();

  // 2. 检查配置文件是否存在
  if (!fs.existsSync(configPath)) {
    console.error(`❌ 错误: 配置文件不存在: ${configPath}`);
    console.log();
    console.log('提示: 请先生成配置文件，或使用示例配置');
    console.log('示例: node scripts/test-template-parser.js examples/template-config.jsonl');
    process.exit(1);
  }

  try {
    // 3. 加载配置文件
    console.log('步骤 1: 加载配置文件');
    console.log('-'.repeat(60));
    
    const configs = ConfigLoader.loadConfigs(configPath);
    console.log(`✓ 成功加载 ${configs.length} 个配置`);
    console.log();

    // 显示配置统计
    const stats = ConfigLoader.getConfigStats(configPath);
    console.log('配置统计:');
    console.log(`  - 总配置数: ${stats.totalConfigs}`);
    console.log(`  - 配置名称: ${stats.configNames.join(', ')}`);
    console.log(`  - 总提取器数: ${stats.totalExtractors}`);
    console.log(`  - 总过滤器数: ${stats.totalFilters}`);
    console.log(`  - 提取器类型分布:`, stats.extractorTypes);
    console.log(`  - 过滤器类型分布:`, stats.filterTypes);
    console.log();

    // 4. 创建TemplateParser实例
    console.log('步骤 2: 创建TemplateParser实例');
    console.log('-'.repeat(60));
    
    const parsers = [];
    for (const config of configs) {
      try {
        const parser = new TemplateParser(config);
        parsers.push(parser);
        console.log(`✓ 创建Parser: ${parser.getName()} (优先级: ${parser.getPriority()})`);
      } catch (error) {
        console.error(`✗ 创建Parser失败 [${config.name}]: ${error.message}`);
      }
    }
    console.log();
    console.log(`成功创建 ${parsers.length}/${configs.length} 个Parser实例`);
    console.log();

    // 5. 测试URL匹配
    console.log('步骤 3: 测试URL匹配');
    console.log('-'.repeat(60));
    
    // 测试URL列表
    const testUrls = [
      'https://www.lixinger.com/open/api/doc?api-key=cn/company',
      'https://www.lixinger.com/open/api/doc?api-key=hk/index',
      'https://www.lixinger.com/analytics/company/dashboard',
      'https://www.lixinger.com/other/page',
    ];

    for (const url of testUrls) {
      console.log(`\n测试URL: ${url}`);
      
      let matched = false;
      for (const parser of parsers) {
        if (parser.matches(url)) {
          console.log(`  ✓ 匹配Parser: ${parser.getName()}`);
          matched = true;
        }
      }
      
      if (!matched) {
        console.log(`  ✗ 无匹配的Parser`);
      }
    }
    console.log();

    // 6. 显示Parser详细信息
    console.log('步骤 4: Parser详细信息');
    console.log('-'.repeat(60));
    
    for (const parser of parsers) {
      const config = parser.getConfig();
      console.log(`\nParser: ${parser.getName()}`);
      console.log(`  描述: ${config.description || 'N/A'}`);
      console.log(`  优先级: ${parser.getPriority()}`);
      console.log(`  URL模式: ${config.urlPattern.pattern}`);
      console.log(`  路径模板: ${config.urlPattern.pathTemplate}`);
      console.log(`  查询参数: ${config.urlPattern.queryParams?.join(', ') || 'N/A'}`);
      console.log(`  提取器数量: ${config.extractors.length}`);
      
      // 显示提取器详情
      console.log(`  提取器列表:`);
      config.extractors.forEach((ext, idx) => {
        const required = ext.required ? ' [必需]' : '';
        console.log(`    ${idx + 1}. ${ext.field} (${ext.type})${required}`);
        console.log(`       选择器: ${ext.selector}`);
        if (ext.pattern) {
          console.log(`       模式: ${ext.pattern}`);
        }
        if (ext.columns) {
          console.log(`       列: ${ext.columns.join(', ')}`);
        }
      });
      
      // 显示过滤器详情
      if (config.filters && config.filters.length > 0) {
        console.log(`  过滤器数量: ${config.filters.length}`);
        console.log(`  过滤器列表:`);
        config.filters.forEach((filter, idx) => {
          console.log(`    ${idx + 1}. ${filter.type} - ${filter.target}`);
          console.log(`       模式: ${filter.pattern}`);
          console.log(`       原因: ${filter.reason}`);
        });
      }
      
      // 显示元数据
      if (config.metadata) {
        console.log(`  元数据:`);
        console.log(`    生成时间: ${config.metadata.generatedAt}`);
        console.log(`    页面数量: ${config.metadata.pageCount}`);
        console.log(`    版本: ${config.metadata.version}`);
      }
    }
    console.log();

    // 7. 总结
    console.log('='.repeat(60));
    console.log('测试完成');
    console.log('='.repeat(60));
    console.log(`✓ 配置文件加载成功`);
    console.log(`✓ 创建了 ${parsers.length} 个TemplateParser实例`);
    console.log(`✓ URL匹配测试完成`);
    console.log();
    console.log('下一步: 运行任务 5.5.4 测试配置驱动的解析（需要Playwright）');
    console.log();

  } catch (error) {
    console.error();
    console.error('❌ 错误:', error.message);
    console.error();
    if (error.stack) {
      console.error('堆栈跟踪:');
      console.error(error.stack);
    }
    process.exit(1);
  }
}

// 运行主函数
if (require.main === module) {
  main().catch(error => {
    console.error('未捕获的错误:', error);
    process.exit(1);
  });
}

module.exports = { main };

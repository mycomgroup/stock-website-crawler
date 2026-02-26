#!/usr/bin/env node

/**
 * 完整工作流测试脚本
 * 测试 Skill 1 → Skill 2 的完整数据流
 * 
 * 工作流:
 * 1. Skill 1: 读取 links.txt → 生成 url-patterns.json
 * 2. Skill 2: 读取 url-patterns.json + pages/ → 生成 template-rules.jsonl
 * 3. 验证: 检查数据流的正确性和完整性
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 测试配置
const TEST_CONFIG = {
  // 输入文件
  linksFile: 'stock-crawler/output/lixinger-crawler/links.txt',
  pagesDir: 'stock-crawler/output/lixinger-crawler/pages',
  
  // 中间输出
  urlPatternsJson: 'stock-crawler/output/lixinger-crawler/url-patterns-workflow-test.json',
  urlPatternsMd: 'stock-crawler/output/lixinger-crawler/url-patterns-workflow-test.md',
  
  // 最终输出
  templateRulesJsonl: 'stock-crawler/output/lixinger-crawler/template-rules-workflow-test.jsonl',
  
  // 测试报告
  reportFile: 'stock-crawler/output/lixinger-crawler/WORKFLOW_TEST_REPORT.md'
};

// 测试结果
const testResults = {
  startTime: new Date(),
  skill1: {},
  skill2: {},
  validation: {},
  errors: []
};

/**
 * 执行命令并记录结果
 */
function executeCommand(command, description) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`执行: ${description}`);
  console.log(`命令: ${command}`);
  console.log('='.repeat(60));
  
  const startTime = Date.now();
  try {
    const output = execSync(command, { 
      encoding: 'utf-8',
      stdio: 'pipe',
      maxBuffer: 10 * 1024 * 1024 // 10MB buffer
    });
    const duration = Date.now() - startTime;
    
    console.log(output);
    console.log(`✅ 成功 (耗时: ${duration}ms)`);
    
    return { success: true, output, duration };
  } catch (error) {
    const duration = Date.now() - startTime;
    console.error(`❌ 失败 (耗时: ${duration}ms)`);
    console.error(error.message);
    if (error.stdout) console.error('STDOUT:', error.stdout.toString());
    if (error.stderr) console.error('STDERR:', error.stderr.toString());
    
    return { success: false, error: error.message, duration };
  }
}

/**
 * 验证文件存在且非空
 */
function validateFile(filePath, description) {
  console.log(`\n验证文件: ${description}`);
  console.log(`路径: ${filePath}`);
  
  if (!fs.existsSync(filePath)) {
    console.error(`❌ 文件不存在`);
    return { exists: false, size: 0 };
  }
  
  const stats = fs.statSync(filePath);
  const sizeKB = (stats.size / 1024).toFixed(2);
  console.log(`✅ 文件存在 (大小: ${sizeKB} KB)`);
  
  return { exists: true, size: stats.size, sizeKB };
}

/**
 * 验证JSON文件格式
 */
function validateJsonFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const data = JSON.parse(content);
    console.log(`✅ JSON格式有效`);
    return { valid: true, data };
  } catch (error) {
    console.error(`❌ JSON格式无效: ${error.message}`);
    return { valid: false, error: error.message };
  }
}

/**
 * 验证JSONL文件格式
 */
function validateJsonlFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.trim().split('\n');
    const configs = lines.map((line, index) => {
      try {
        return JSON.parse(line);
      } catch (error) {
        throw new Error(`Line ${index + 1}: ${error.message}`);
      }
    });
    console.log(`✅ JSONL格式有效 (${configs.length}个配置)`);
    return { valid: true, configs, lineCount: lines.length };
  } catch (error) {
    console.error(`❌ JSONL格式无效: ${error.message}`);
    return { valid: false, error: error.message };
  }
}

/**
 * 验证数据流的一致性
 */
function validateDataFlow(urlPatternsData, templateConfigs) {
  console.log(`\n${'='.repeat(60)}`);
  console.log('验证数据流一致性');
  console.log('='.repeat(60));
  
  const validation = {
    totalPatterns: urlPatternsData.patterns.length,
    totalConfigs: templateConfigs.length,
    matched: 0,
    unmatched: [],
    details: []
  };
  
  // 检查每个URL模式是否有对应的配置
  for (const pattern of urlPatternsData.patterns) {
    const matchingConfig = templateConfigs.find(config => 
      config.name === pattern.name || 
      config.urlPattern?.pathTemplate === pattern.pathTemplate
    );
    
    if (matchingConfig) {
      validation.matched++;
      validation.details.push({
        pattern: pattern.name,
        pathTemplate: pattern.pathTemplate,
        urlCount: pattern.urlCount,
        configName: matchingConfig.name,
        extractorCount: matchingConfig.extractors?.length || 0,
        filterCount: matchingConfig.filters?.length || 0,
        pageCount: matchingConfig.metadata?.pageCount || 0,
        status: '✅ 匹配'
      });
      console.log(`✅ ${pattern.name}: 找到配置 (${pattern.urlCount} URLs → ${matchingConfig.metadata?.pageCount || 0} pages)`);
    } else {
      validation.unmatched.push(pattern.name);
      validation.details.push({
        pattern: pattern.name,
        pathTemplate: pattern.pathTemplate,
        urlCount: pattern.urlCount,
        status: '❌ 未匹配'
      });
      console.log(`❌ ${pattern.name}: 未找到配置`);
    }
  }
  
  console.log(`\n匹配率: ${validation.matched}/${validation.totalPatterns} (${(validation.matched / validation.totalPatterns * 100).toFixed(1)}%)`);
  
  return validation;
}

/**
 * 生成测试报告
 */
function generateReport() {
  const endTime = new Date();
  const totalDuration = endTime - testResults.startTime;
  
  let report = `# 完整工作流测试报告

**测试日期**: ${testResults.startTime.toISOString().split('T')[0]}
**测试时间**: ${testResults.startTime.toLocaleTimeString()} - ${endTime.toLocaleTimeString()}
**总耗时**: ${(totalDuration / 1000).toFixed(2)}秒

## 测试概述

测试完整的数据流：links.txt → Skill 1 → url-patterns.json → Skill 2 → template-rules.jsonl

## 测试环境

- **输入文件**: \`${TEST_CONFIG.linksFile}\`
- **Pages目录**: \`${TEST_CONFIG.pagesDir}\`
- **中间输出**: \`${TEST_CONFIG.urlPatternsJson}\`
- **最终输出**: \`${TEST_CONFIG.templateRulesJsonl}\`

## 测试步骤

### 步骤1: Skill 1 - URL模式分析

**命令**: 
\`\`\`bash
node skills/url-pattern-analyzer/main.js ${TEST_CONFIG.linksFile} ${TEST_CONFIG.urlPatternsJson} --markdown
\`\`\`

**结果**: ${testResults.skill1.success ? '✅ 成功' : '❌ 失败'}
**耗时**: ${testResults.skill1.duration}ms

`;

  if (testResults.skill1.success) {
    report += `**输出文件**:
- JSON: ${testResults.skill1.fileValidation?.exists ? '✅' : '❌'} (${testResults.skill1.fileValidation?.sizeKB || 0} KB)
- Markdown: ${testResults.skill1.mdValidation?.exists ? '✅' : '❌'} (${testResults.skill1.mdValidation?.sizeKB || 0} KB)

**统计信息**:
- 总URL数: ${testResults.skill1.jsonData?.summary?.totalUrls || 0}
- 模式数量: ${testResults.skill1.jsonData?.summary?.patternCount || 0}
- 生成时间: ${testResults.skill1.jsonData?.summary?.generatedAt || 'N/A'}

`;
  } else {
    report += `**错误**: ${testResults.skill1.error}\n\n`;
  }

  report += `### 步骤2: Skill 2 - 模板内容分析

**命令**: 
\`\`\`bash
node skills/template-content-analyzer/main.js ${TEST_CONFIG.urlPatternsJson} ${TEST_CONFIG.pagesDir} ${TEST_CONFIG.templateRulesJsonl}
\`\`\`

**结果**: ${testResults.skill2.success ? '✅ 成功' : '❌ 失败'}
**耗时**: ${testResults.skill2.duration}ms

`;

  if (testResults.skill2.success) {
    report += `**输出文件**:
- JSONL: ${testResults.skill2.fileValidation?.exists ? '✅' : '❌'} (${testResults.skill2.fileValidation?.sizeKB || 0} KB)

**统计信息**:
- 配置数量: ${testResults.skill2.jsonlData?.lineCount || 0}
- 总提取器: ${testResults.skill2.totalExtractors || 0}
- 总过滤器: ${testResults.skill2.totalFilters || 0}

`;
  } else {
    report += `**错误**: ${testResults.skill2.error}\n\n`;
  }

  report += `### 步骤3: 数据流验证

**验证项**:
- URL模式 → 模板配置的映射关系
- 数据一致性检查
- 配置完整性检查

**结果**: ${testResults.validation.matched === testResults.validation.totalPatterns ? '✅ 完全匹配' : '⚠️ 部分匹配'}

**匹配率**: ${testResults.validation.matched}/${testResults.validation.totalPatterns} (${testResults.validation.totalPatterns > 0 ? (testResults.validation.matched / testResults.validation.totalPatterns * 100).toFixed(1) : 0}%)

`;

  if (testResults.validation.details) {
    report += `#### 详细映射关系

| 模式名称 | 路径模板 | URL数量 | 页面数量 | 提取器 | 过滤器 | 状态 |
|---------|---------|---------|---------|--------|--------|------|
`;
    for (const detail of testResults.validation.details) {
      report += `| ${detail.pattern} | ${detail.pathTemplate} | ${detail.urlCount} | ${detail.pageCount || 'N/A'} | ${detail.extractorCount || 'N/A'} | ${detail.filterCount || 'N/A'} | ${detail.status} |\n`;
    }
    report += '\n';
  }

  if (testResults.validation.unmatched && testResults.validation.unmatched.length > 0) {
    report += `#### 未匹配的模式

以下URL模式没有生成对应的配置（可能是因为没有找到匹配的markdown文件）:

`;
    for (const pattern of testResults.validation.unmatched) {
      report += `- ${pattern}\n`;
    }
    report += '\n';
  }

  report += `## 性能测试

| 步骤 | 耗时 | 性能评价 |
|------|------|---------|
| Skill 1 (URL分析) | ${testResults.skill1.duration}ms | ${testResults.skill1.duration < 10000 ? '✅ 优秀' : testResults.skill1.duration < 30000 ? '✅ 良好' : '⚠️ 需优化'} |
| Skill 2 (内容分析) | ${testResults.skill2.duration}ms | ${testResults.skill2.duration < 30000 ? '✅ 优秀' : testResults.skill2.duration < 60000 ? '✅ 良好' : '⚠️ 需优化'} |
| 总耗时 | ${(totalDuration / 1000).toFixed(2)}s | ${totalDuration < 60000 ? '✅ 优秀' : '⚠️ 需优化'} |

**性能目标**: 总耗时 < 1分钟

## 验收标准检查

| 验收标准 | 状态 | 说明 |
|---------|------|------|
| Skill 1成功运行 | ${testResults.skill1.success ? '✅' : '❌'} | ${testResults.skill1.success ? '生成url-patterns.json' : '执行失败'} |
| Skill 2成功运行 | ${testResults.skill2.success ? '✅' : '❌'} | ${testResults.skill2.success ? '生成template-rules.jsonl' : '执行失败'} |
| 数据流正确 | ${testResults.validation.matched > 0 ? '✅' : '❌'} | ${testResults.validation.matched}/${testResults.validation.totalPatterns}个模式有配置 |
| 配置格式正确 | ${testResults.skill2.jsonlData?.valid ? '✅' : '❌'} | JSONL格式验证 |
| 性能合理 | ${totalDuration < 60000 ? '✅' : '❌'} | 总耗时${(totalDuration / 1000).toFixed(2)}s < 60s |

## 总体评价

`;

  const allSuccess = testResults.skill1.success && 
                     testResults.skill2.success && 
                     testResults.validation.matched > 0 &&
                     totalDuration < 60000;

  if (allSuccess) {
    report += `**测试结果**: ✅ **通过**

完整工作流测试成功！两个skills能够正确串联运行，数据流畅通，生成的配置文件格式正确且内容完整。

`;
  } else {
    report += `**测试结果**: ❌ **失败**

`;
    if (!testResults.skill1.success) {
      report += `- Skill 1执行失败\n`;
    }
    if (!testResults.skill2.success) {
      report += `- Skill 2执行失败\n`;
    }
    if (testResults.validation.matched === 0) {
      report += `- 数据流验证失败，没有匹配的配置\n`;
    }
    if (totalDuration >= 60000) {
      report += `- 性能不达标，耗时超过1分钟\n`;
    }
    report += '\n';
  }

  if (testResults.errors.length > 0) {
    report += `## 错误日志

`;
    for (const error of testResults.errors) {
      report += `- ${error}\n`;
    }
    report += '\n';
  }

  report += `## 结论

${allSuccess ? 
  '完整工作流测试通过，两个skills能够正确协作完成从URL分析到配置生成的完整流程。' :
  '完整工作流测试存在问题，需要修复上述错误后重新测试。'
}

## 下一步

${allSuccess ?
  '- ✅ 任务9.1.3完成\n- ⏭️ 可以进行任务9.1.4：验证生成的配置质量' :
  '- 修复上述问题\n- 重新运行完整工作流测试'
}

---

**测试脚本**: \`skills/test-complete-workflow.js\`
**报告生成时间**: ${new Date().toISOString()}
`;

  return report;
}

/**
 * 主测试流程
 */
async function runTest() {
  console.log('='.repeat(60));
  console.log('完整工作流测试');
  console.log('='.repeat(60));
  console.log(`开始时间: ${testResults.startTime.toLocaleString()}`);
  
  try {
    // 步骤1: 运行Skill 1
    console.log('\n\n步骤1: 运行Skill 1 (URL Pattern Analyzer)');
    const skill1Command = `node skills/url-pattern-analyzer/main.js ${TEST_CONFIG.linksFile} ${TEST_CONFIG.urlPatternsJson} --markdown`;
    const skill1Result = executeCommand(skill1Command, 'Skill 1 - URL模式分析');
    testResults.skill1 = skill1Result;
    
    if (!skill1Result.success) {
      testResults.errors.push('Skill 1执行失败');
      throw new Error('Skill 1执行失败，终止测试');
    }
    
    // 验证Skill 1输出
    console.log('\n验证Skill 1输出文件...');
    testResults.skill1.fileValidation = validateFile(TEST_CONFIG.urlPatternsJson, 'url-patterns.json');
    testResults.skill1.mdValidation = validateFile(TEST_CONFIG.urlPatternsMd, 'url-patterns.md');
    
    if (!testResults.skill1.fileValidation.exists) {
      testResults.errors.push('url-patterns.json文件未生成');
      throw new Error('url-patterns.json文件未生成');
    }
    
    const jsonValidation = validateJsonFile(TEST_CONFIG.urlPatternsJson);
    testResults.skill1.jsonValidation = jsonValidation;
    if (!jsonValidation.valid) {
      testResults.errors.push('url-patterns.json格式无效');
      throw new Error('url-patterns.json格式无效');
    }
    testResults.skill1.jsonData = jsonValidation.data;
    
    // 步骤2: 运行Skill 2
    console.log('\n\n步骤2: 运行Skill 2 (Template Content Analyzer)');
    const skill2Command = `node skills/template-content-analyzer/main.js ${TEST_CONFIG.urlPatternsJson} ${TEST_CONFIG.pagesDir} ${TEST_CONFIG.templateRulesJsonl}`;
    const skill2Result = executeCommand(skill2Command, 'Skill 2 - 模板内容分析');
    testResults.skill2 = skill2Result;
    
    if (!skill2Result.success) {
      testResults.errors.push('Skill 2执行失败');
      throw new Error('Skill 2执行失败，终止测试');
    }
    
    // 验证Skill 2输出
    console.log('\n验证Skill 2输出文件...');
    testResults.skill2.fileValidation = validateFile(TEST_CONFIG.templateRulesJsonl, 'template-rules.jsonl');
    
    if (!testResults.skill2.fileValidation.exists) {
      testResults.errors.push('template-rules.jsonl文件未生成');
      throw new Error('template-rules.jsonl文件未生成');
    }
    
    const jsonlValidation = validateJsonlFile(TEST_CONFIG.templateRulesJsonl);
    testResults.skill2.jsonlValidation = jsonlValidation;
    if (!jsonlValidation.valid) {
      testResults.errors.push('template-rules.jsonl格式无效');
      throw new Error('template-rules.jsonl格式无效');
    }
    testResults.skill2.jsonlData = jsonlValidation;
    
    // 计算统计信息
    testResults.skill2.totalExtractors = jsonlValidation.configs.reduce((sum, config) => 
      sum + (config.extractors?.length || 0), 0);
    testResults.skill2.totalFilters = jsonlValidation.configs.reduce((sum, config) => 
      sum + (config.filters?.length || 0), 0);
    
    // 步骤3: 验证数据流
    console.log('\n\n步骤3: 验证数据流一致性');
    testResults.validation = validateDataFlow(
      testResults.skill1.jsonData,
      jsonlValidation.configs
    );
    
    // 生成报告
    console.log('\n\n生成测试报告...');
    const report = generateReport();
    fs.writeFileSync(TEST_CONFIG.reportFile, report, 'utf-8');
    console.log(`✅ 报告已保存: ${TEST_CONFIG.reportFile}`);
    
    // 显示总结
    console.log('\n\n' + '='.repeat(60));
    console.log('测试完成');
    console.log('='.repeat(60));
    console.log(`总耗时: ${((new Date() - testResults.startTime) / 1000).toFixed(2)}秒`);
    console.log(`Skill 1: ${testResults.skill1.success ? '✅ 成功' : '❌ 失败'}`);
    console.log(`Skill 2: ${testResults.skill2.success ? '✅ 成功' : '❌ 失败'}`);
    console.log(`数据流: ${testResults.validation.matched}/${testResults.validation.totalPatterns} 匹配`);
    console.log(`报告: ${TEST_CONFIG.reportFile}`);
    
    const allSuccess = testResults.skill1.success && 
                       testResults.skill2.success && 
                       testResults.validation.matched > 0;
    
    if (allSuccess) {
      console.log('\n✅ 完整工作流测试通过！');
      process.exit(0);
    } else {
      console.log('\n❌ 完整工作流测试失败！');
      process.exit(1);
    }
    
  } catch (error) {
    console.error('\n\n❌ 测试过程中发生错误:');
    console.error(error.message);
    testResults.errors.push(error.message);
    
    // 即使出错也生成报告
    try {
      const report = generateReport();
      fs.writeFileSync(TEST_CONFIG.reportFile, report, 'utf-8');
      console.log(`\n报告已保存: ${TEST_CONFIG.reportFile}`);
    } catch (reportError) {
      console.error('生成报告失败:', reportError.message);
    }
    
    process.exit(1);
  }
}

// 运行测试
runTest();

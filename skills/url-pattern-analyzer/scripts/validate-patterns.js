#!/usr/bin/env node

/**
 * URL Pattern Quality Validator
 * 
 * 检查URL模式分析结果的质量，发现潜在问题
 */

const fs = require('fs');
const path = require('path');

/**
 * 质量检查规则
 */
const QUALITY_RULES = {
  // 规则1: 检查过大的簇
  largeClusters: {
    name: '过大簇检查',
    threshold: 500,
    severity: 'warning',
    check: (pattern) => pattern.urlCount > 500,
    message: (pattern) => `模式 "${pattern.name}" 包含 ${pattern.urlCount} 个URL，可能混合了不同类型的页面`
  },
  
  // 规则2: 检查样本URL是否结构一致
  sampleConsistency: {
    name: '样本一致性检查',
    severity: 'error',
    check: (pattern) => {
      if (!pattern.samples || pattern.samples.length < 2) return false;
      
      // 检查路径深度是否一致
      const depths = pattern.samples.map(url => {
        try {
          const urlObj = new URL(url);
          return urlObj.pathname.split('/').filter(s => s).length;
        } catch {
          return 0;
        }
      });
      
      const uniqueDepths = [...new Set(depths)];
      return uniqueDepths.length > 1;
    },
    message: (pattern) => `模式 "${pattern.name}" 的样本URL路径深度不一致，可能混合了不同结构`
  },
  
  // 规则3: 检查是否有相似的模式名称
  duplicateNames: {
    name: '重复名称检查',
    severity: 'warning',
    check: (pattern, allPatterns) => {
      const sameName = allPatterns.filter(p => p.name === pattern.name);
      return sameName.length > 1;
    },
    message: (pattern) => `模式名称 "${pattern.name}" 重复出现，应该进一步细分或合并`
  },
  
  // 规则4: 检查路径模板是否过于泛化
  overlyGeneric: {
    name: '过度泛化检查',
    severity: 'warning',
    check: (pattern) => {
      // 计算参数占比
      const template = pattern.pathTemplate;
      const segments = template.split('/').filter(s => s);
      const paramCount = segments.filter(s => s.startsWith('{')).length;
      const paramRatio = paramCount / segments.length;
      
      return paramRatio > 0.7 && pattern.urlCount > 100;
    },
    message: (pattern) => `模式 "${pattern.name}" 的路径模板过于泛化（${pattern.pathTemplate}），参数占比过高`
  },
  
  // 规则5: 检查样本URL中的固定段是否真的固定
  inconsistentSegments: {
    name: '不一致段检查',
    severity: 'error',
    check: (pattern) => {
      if (!pattern.samples || pattern.samples.length < 3) return false;
      
      try {
        const paths = pattern.samples.map(url => {
          const urlObj = new URL(url);
          return urlObj.pathname.split('/').filter(s => s);
        });
        
        if (paths.length === 0) return false;
        const segmentCount = paths[0].length;
        
        // 检查每个位置的段
        for (let i = 0; i < segmentCount; i++) {
          const segments = paths.map(p => p[i]).filter(s => s);
          const uniqueSegments = [...new Set(segments)];
          
          // 如果某个位置有2-5个不同的值，可能是半固定段
          if (uniqueSegments.length > 1 && uniqueSegments.length <= 5) {
            return true;
          }
        }
        
        return false;
      } catch {
        return false;
      }
    },
    message: (pattern) => `模式 "${pattern.name}" 的样本中发现半固定段，建议进一步细分`
  },
  
  // 规则6: 检查模式总数是否合理
  patternCountCheck: {
    name: '模式数量检查',
    severity: 'info',
    check: (pattern, allPatterns, totalUrls) => {
      const patternCount = allPatterns.length;
      
      // 模式数量应该在合理范围内
      if (totalUrls < 1000) {
        return patternCount > 50;
      } else if (totalUrls < 5000) {
        return patternCount > 100;
      } else if (totalUrls < 10000) {
        return patternCount > 150;
      } else {
        return patternCount > 200;
      }
    },
    message: (pattern, allPatterns, totalUrls) => {
      return `模式数量 ${allPatterns.length} 可能过多，建议增加 min-group-size 参数`;
    }
  },
  
  // 规则7: 检查覆盖率
  coverageCheck: {
    name: '覆盖率检查',
    severity: 'warning',
    check: (pattern, allPatterns, totalUrls) => {
      const coveredUrls = allPatterns.reduce((sum, p) => sum + p.urlCount, 0);
      const coverage = coveredUrls / totalUrls;
      return coverage < 0.9;
    },
    message: (pattern, allPatterns, totalUrls) => {
      const coveredUrls = allPatterns.reduce((sum, p) => sum + p.urlCount, 0);
      const coverage = (coveredUrls / totalUrls * 100).toFixed(2);
      return `覆盖率 ${coverage}% 较低，有 ${totalUrls - coveredUrls} 个URL未被分类`;
    }
  },
  
  // 规则8: 检查最大簇占比
  dominantCluster: {
    name: '主导簇检查',
    severity: 'warning',
    check: (pattern, allPatterns, totalUrls) => {
      const maxPattern = allPatterns[0]; // 假设已排序
      const ratio = maxPattern.urlCount / totalUrls;
      return ratio > 0.3;
    },
    message: (pattern, allPatterns, totalUrls) => {
      const maxPattern = allPatterns[0];
      const ratio = (maxPattern.urlCount / totalUrls * 100).toFixed(2);
      return `最大模式 "${maxPattern.name}" 占比 ${ratio}%，可能需要进一步细分`;
    }
  }
};

/**
 * 验证模式质量
 */
function validatePatterns(jsonFile) {
  console.log('=== URL Pattern Quality Validator ===\n');
  
  // 读取JSON文件
  const data = JSON.parse(fs.readFileSync(jsonFile, 'utf-8'));
  const patterns = data.patterns || [];
  const totalUrls = data.summary?.totalUrls || 0;
  
  console.log(`总URL数: ${totalUrls}`);
  console.log(`模式数量: ${patterns.length}\n`);
  
  const issues = {
    error: [],
    warning: [],
    info: []
  };
  
  // 应用所有规则
  patterns.forEach((pattern, index) => {
    Object.entries(QUALITY_RULES).forEach(([ruleKey, rule]) => {
      if (rule.check(pattern, patterns, totalUrls)) {
        const issue = {
          rule: rule.name,
          severity: rule.severity,
          pattern: pattern.name,
          message: rule.message(pattern, patterns, totalUrls)
        };
        issues[rule.severity].push(issue);
      }
    });
  });
  
  // 显示结果
  console.log('## 检查结果\n');
  
  if (issues.error.length > 0) {
    console.log('### ❌ 错误 (需要修复)\n');
    issues.error.forEach((issue, i) => {
      console.log(`${i + 1}. [${issue.rule}] ${issue.message}`);
    });
    console.log('');
  }
  
  if (issues.warning.length > 0) {
    console.log('### ⚠️  警告 (建议优化)\n');
    issues.warning.forEach((issue, i) => {
      console.log(`${i + 1}. [${issue.rule}] ${issue.message}`);
    });
    console.log('');
  }
  
  if (issues.info.length > 0) {
    console.log('### ℹ️  信息\n');
    issues.info.forEach((issue, i) => {
      console.log(`${i + 1}. [${issue.rule}] ${issue.message}`);
    });
    console.log('');
  }
  
  if (issues.error.length === 0 && issues.warning.length === 0 && issues.info.length === 0) {
    console.log('✅ 所有检查通过，质量良好！\n');
  }
  
  // 生成优化建议
  console.log('## 优化建议\n');
  
  if (issues.error.length > 0 || issues.warning.length > 0) {
    const suggestions = generateSuggestions(issues, patterns, totalUrls);
    suggestions.forEach((suggestion, i) => {
      console.log(`${i + 1}. ${suggestion}`);
    });
  } else {
    console.log('当前配置已经很好，无需调整。\n');
  }
  
  return {
    totalIssues: issues.error.length + issues.warning.length + issues.info.length,
    issues
  };
}

/**
 * 生成优化建议
 */
function generateSuggestions(issues, patterns, totalUrls) {
  const suggestions = [];
  
  // 检查是否有大簇问题
  const largeClusters = issues.warning.filter(i => i.rule === '过大簇检查');
  if (largeClusters.length > 0) {
    suggestions.push('尝试使用 --try-refine-top-n 10 参数智能拆分大簇');
    suggestions.push('或使用 --strict-top-n 5 --strict-match-ratio 0.85 对大簇应用严格规则');
  }
  
  // 检查是否有样本不一致问题
  const inconsistent = issues.error.filter(i => i.rule === '样本一致性检查' || i.rule === '不一致段检查');
  if (inconsistent.length > 0) {
    suggestions.push('发现样本不一致，建议增加 --refine-max-values 12 --refine-min-count 5 启用更激进的细分');
  }
  
  // 检查模式数量
  if (patterns.length > 150) {
    suggestions.push(`模式数量 ${patterns.length} 较多，建议增加 --min-group-size 15 减少模式数量`);
  } else if (patterns.length < 30 && totalUrls > 1000) {
    suggestions.push(`模式数量 ${patterns.length} 较少，建议降低 --min-group-size 5 或启用细分参数`);
  }
  
  // 检查覆盖率
  const coverageIssues = issues.warning.filter(i => i.rule === '覆盖率检查');
  if (coverageIssues.length > 0) {
    suggestions.push('覆盖率较低，建议降低 --min-group-size 参数以包含更多小簇');
  }
  
  return suggestions;
}

/**
 * 主函数
 */
function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help')) {
    console.log(`
URL Pattern Quality Validator

使用方式:
  node validate-patterns.js <json-file>

示例:
  node validate-patterns.js ../../stock-crawler/output/lixinger-crawler/url-patterns.json
    `);
    process.exit(0);
  }
  
  const jsonFile = args[0];
  
  if (!fs.existsSync(jsonFile)) {
    console.error(`错误: 文件不存在: ${jsonFile}`);
    process.exit(1);
  }
  
  try {
    const result = validatePatterns(jsonFile);
    
    // 如果有错误，返回非零退出码
    if (result.issues.error.length > 0) {
      process.exit(1);
    }
  } catch (error) {
    console.error('验证失败:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { validatePatterns, QUALITY_RULES };

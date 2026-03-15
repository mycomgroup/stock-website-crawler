import fs from 'fs';
import path from 'path';

/**
 * API 文档生成器
 */
export class DocGenerator {
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

    console.log(`生成 ${this.patterns.length} 个 API 文档...`);

    const configs = [];
    let generated = 0;
    
    for (const pattern of this.patterns) {
      try {
        // 生成用户文档
        this.generateDoc(pattern);
        
        // 生成配置
        const config = this.generateConfig(pattern);
        configs.push(config);
        
        generated++;
      } catch (error) {
        console.error(`生成 ${pattern.name} 文档失败:`, error.message);
      }
    }

    this.generateReadme();
    
    // 保存配置文件
    this.saveConfigs(configs);

    console.log(`✓ 成功生成 ${generated} 个文档和配置`);
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

    lines.push(`# ${pattern.description || pattern.name}`);
    lines.push('');
    lines.push('## 简要描述');
    lines.push('');
    lines.push(pattern.description || '获取页面数据');
    lines.push('');
    lines.push('## 请求URL');
    lines.push('');
    lines.push('```');
    lines.push(pattern.samples[0]);
    lines.push('```');
    lines.push('');
    lines.push('## URL 模式');
    lines.push('');
    lines.push('```');
    lines.push(pattern.pathTemplate);
    lines.push('```');
    lines.push('');
    lines.push('## 请求方式');
    lines.push('');
    lines.push('GET (通过网页抓取)');
    lines.push('');
    
    const params = this.extractParameters(pattern);
    const requiredParams = params.filter(p => p.required);
    const optionalParams = params.filter(p => !p.required);
    
    // 只显示必选参数
    if (requiredParams.length > 0) {
      lines.push('## 参数');
      lines.push('');
      lines.push('| 参数名称 | 数据类型 | 说明 | 取值范围 |');
      lines.push('| -------- | -------- | ---- | -------- |');
      
      for (const param of requiredParams) {
        const valueRange = param.valueRange || '请参考示例';
        lines.push(`| ${param.name} | ${param.type} | ${param.description} | ${valueRange} |`);
      }
      lines.push('');
    }
    
    // 可选参数单独列出
    if (optionalParams.length > 0) {
      lines.push('## 可选参数');
      lines.push('');
      lines.push('| 参数名称 | 数据类型 | 说明 | 默认值 |');
      lines.push('| -------- | -------- | ---- | ------ |');
      
      for (const param of optionalParams) {
        const defaultValue = param.defaultValue || '-';
        lines.push(`| ${param.name} | ${param.type} | ${param.description} | ${defaultValue} |`);
      }
      lines.push('');
    }
    
    lines.push('## 使用示例');
    lines.push('');
    lines.push('```bash');
    lines.push(`node main.js call --api=${pattern.name} ${this.generateExampleParams(requiredParams)}`);
    lines.push('```');
    lines.push('');
    lines.push('## 返回数据说明');
    lines.push('');
    lines.push('| 参数名称 | 数据类型 | 说明 |');
    lines.push('| -------- | -------- | ---- |');
    lines.push('| type | String | 页面类型 |');
    lines.push('| title | String | 页面标题 |');
    lines.push('| tables | Array | 表格数据 |');
    lines.push('| charts | Array | 图表数据 |');
    lines.push('');

    return lines.join('\n');
  }

  /**
   * 提取参数
   */
  extractParameters(pattern) {
    const params = [];
    const pathParams = pattern.pathTemplate.match(/\{([^}]+)\}/g) || [];
    
    // 检测重复参数
    const duplicateParams = this.detectDuplicateParams(pattern, pathParams);
    
    // 跟踪已使用的参数名，避免重复
    const usedNames = new Set();
    
    // 处理路径参数
    for (const param of pathParams) {
      const rawName = param.replace(/[{}]/g, '');
      
      // 如果是重复参数，跳过后续的
      if (duplicateParams.has(rawName)) {
        continue;
      }
      
      // 推断业务含义的参数名
      let inferredName = this.inferParameterName(pattern, rawName);
      
      // 如果推断的名称已经被使用，保持原始参数名
      if (usedNames.has(inferredName)) {
        inferredName = rawName;
      }
      
      usedNames.add(inferredName);
      
      // 提取参数的取值范围
      const valueRange = this.extractValueRange(pattern, inferredName);
      
      params.push({
        name: inferredName,
        required: true,
        type: 'String',
        description: this.generateParamDescription(pattern, inferredName, rawName),
        valueRange: valueRange
      });
    }

    // 处理查询参数（设为可选，并尝试推断默认值）
    for (const queryParam of pattern.queryParams) {
      const defaultValue = this.inferDefaultValue(pattern, queryParam);
      
      params.push({
        name: queryParam,
        required: false,
        type: 'String',
        description: `查询参数 ${queryParam}`,
        defaultValue: defaultValue
      });
    }

    return params;
  }

  /**
   * 提取参数的取值范围
   */
  extractValueRange(pattern, paramName) {
    // 从样本中提取参数值
    const values = new Set();
    
    for (const sample of pattern.samples.slice(0, 10)) {
      const regex = new RegExp(pattern.pattern);
      const match = sample.match(regex);
      
      if (!match) continue;
      
      // 提取所有参数值
      const paramValues = match.slice(1).filter(v => v !== undefined && !v.startsWith('?'));
      
      // 根据参数位置提取值
      const pathParams = pattern.pathTemplate.match(/\{([^}]+)\}/g) || [];
      const paramIndex = pathParams.findIndex(p => {
        const name = p.replace(/[{}]/g, '');
        return this.inferParameterName(pattern, name) === paramName;
      });
      
      if (paramIndex >= 0 && paramIndex < paramValues.length) {
        values.add(paramValues[paramIndex]);
      }
    }
    
    // 如果样本值少于等于5个，直接列出
    if (values.size > 0 && values.size <= 5) {
      return Array.from(values).join(', ');
    }
    
    // 如果样本值较多，尝试识别模式
    if (values.size > 5) {
      const valueArray = Array.from(values);
      
      // 检查是否都是数字
      if (valueArray.every(v => /^\d+$/.test(v))) {
        const numbers = valueArray.map(v => parseInt(v));
        const min = Math.min(...numbers);
        const max = Math.max(...numbers);
        return `数字范围: ${min}-${max}`;
      }
      
      // 检查是否有共同前缀
      const commonPrefix = this.findCommonPrefix(valueArray);
      if (commonPrefix && commonPrefix.length > 2) {
        return `${commonPrefix}* (${values.size}+ 个值)`;
      }
      
      return `多个值 (${values.size}+ 个)`;
    }
    
    return null;
  }

  /**
   * 推断查询参数的默认值
   */
  inferDefaultValue(pattern, queryParam) {
    // 常见的默认值推断
    const defaultValues = {
      'page': '1',
      'limit': '20',
      'size': '20',
      'offset': '0',
      'sort': 'desc',
      'order': 'desc',
      'format': 'json'
    };
    
    const lowerParam = queryParam.toLowerCase();
    for (const [key, value] of Object.entries(defaultValues)) {
      if (lowerParam.includes(key)) {
        return value;
      }
    }
    
    return null;
  }

  /**
   * 查找字符串数组的公共前缀
   */
  findCommonPrefix(strings) {
    if (strings.length === 0) return '';
    if (strings.length === 1) return strings[0];
    
    let prefix = strings[0];
    for (let i = 1; i < strings.length; i++) {
      while (strings[i].indexOf(prefix) !== 0) {
        prefix = prefix.substring(0, prefix.length - 1);
        if (prefix === '') return '';
      }
    }
    
    return prefix;
  }

  /**
   * 检测重复参数（值相同的参数）
   */
  detectDuplicateParams(pattern, pathParams) {
    const duplicates = new Set();
    
    if (pathParams.length < 2 || !pattern.samples || pattern.samples.length === 0) {
      return duplicates;
    }
    
    // 统计每个样本中相邻参数是否相同
    const duplicateCount = new Map();
    let totalSamples = 0;
    
    // 从样本中提取参数值
    for (const sample of pattern.samples.slice(0, 10)) {
      const regex = new RegExp(pattern.pattern);
      const match = sample.match(regex);
      
      if (!match) continue;
      
      totalSamples++;
      
      // 比较相邻参数的值
      const values = match.slice(1).filter(v => v !== undefined && !v.startsWith('?'));
      
      for (let i = 0; i < values.length - 1; i++) {
        if (values[i] === values[i + 1]) {
          // 找到重复的参数
          const key = `${i}-${i+1}`;
          duplicateCount.set(key, (duplicateCount.get(key) || 0) + 1);
        }
      }
    }
    
    // 只有当所有样本都显示重复时，才认为是真正的重复参数
    for (const [key, count] of duplicateCount.entries()) {
      if (count === totalSamples && totalSamples > 0) {
        const [, secondIndex] = key.split('-').map(Number);
        if (secondIndex < pathParams.length) {
          const paramName = pathParams[secondIndex].replace(/[{}]/g, '');
          duplicates.add(paramName);
        }
      }
    }
    
    return duplicates;
  }

  /**
   * 推断参数的业务含义名称
   */
  inferParameterName(pattern, rawName) {
    const path = pattern.pathTemplate.toLowerCase();
    const desc = pattern.description.toLowerCase();
    
    // 如果已经有业务含义，直接返回
    if (!rawName.startsWith('param')) {
      return rawName;
    }
    
    // 根据 URL 路径推断
    if (path.includes('/company/')) {
      if (path.includes('/sz/') || path.includes('/sh/') || path.includes('/hk/') || 
          path.includes('/nasdaq/') || path.includes('/nyse/')) {
        return 'stockCode';
      }
    }
    
    if (path.includes('/industry/')) {
      return 'industryCode';
    }
    
    if (path.includes('/index/')) {
      return 'indexCode';
    }
    
    if (path.includes('/fund/')) {
      if (path.includes('/fund-manager/')) {
        return 'managerId';
      }
      if (path.includes('/fund-collection/')) {
        if (path.includes('/jjgs/')) {
          return 'fundCompanyCode';
        }
        return 'fundCollectionId';
      }
      return 'fundCode';
    }
    
    if (path.includes('/user/')) {
      return 'userId';
    }
    
    if (path.includes('/chart-maker/')) {
      return 'chartType';
    }
    
    // 根据描述推断
    if (desc.includes('公司') || desc.includes('股票')) {
      return 'stockCode';
    }
    
    if (desc.includes('行业')) {
      return 'industryCode';
    }
    
    if (desc.includes('指数')) {
      return 'indexCode';
    }
    
    if (desc.includes('基金')) {
      return 'fundCode';
    }
    
    // 无法推断，保持原名
    return rawName;
  }

  /**
   * 生成参数描述
   */
  generateParamDescription(pattern, inferredName, rawName) {
    const descriptions = {
      'stockCode': '股票代码',
      'industryCode': '行业代码',
      'indexCode': '指数代码',
      'fundCode': '基金代码',
      'fundCompanyCode': '基金公司代码',
      'managerId': '基金经理ID',
      'userId': '用户ID',
      'chartType': '图表类型',
      'fundCollectionId': '基金集合ID'
    };
    
    if (descriptions[inferredName]) {
      return descriptions[inferredName];
    }
    
    return `路径参数 ${rawName}`;
  }

  /**
   * 生成示例参数
   */
  generateExampleParams(params) {
    const required = params.filter(p => p.required);
    return required.map(p => `--${p.name}=value`).join(' ');
  }

  /**
   * 生成配置
   */
  generateConfig(pattern) {
    // 判断输出格式：如果主要是表格数据，用 CSV，否则用 MD
    const outputFormat = this.determineOutputFormat(pattern);
    
    return {
      api: pattern.name,
      description: pattern.description,
      pathTemplate: pattern.pathTemplate,
      pattern: pattern.pattern,
      parameters: this.extractParameters(pattern),
      queryParams: pattern.queryParams,
      outputFormat: outputFormat,
      dataExtraction: {
        // 定义如何提取数据
        tables: outputFormat === 'csv' ? 'primary' : 'all',
        charts: outputFormat === 'md',
        images: outputFormat === 'md',
        mainContent: outputFormat === 'md'
      },
      dataSelectors: {
        // 数据选择器（需要通过 analyze-data-selectors.js 生成）
        primaryTable: null,  // 例如: 'table.data-table'
        primaryTableXPath: null,  // 例如: '//*[@id="main-table"]'
        allTables: [],  // 所有表格的选择器
        mainContent: 'main',  // 主内容区域
        dataContainers: []  // 数据容器选择器
      },
      samples: pattern.samples.slice(0, 3)
    };
  }

  /**
   * 判断输出格式
   */
  determineOutputFormat(pattern) {
    const name = pattern.name.toLowerCase();
    const desc = pattern.description.toLowerCase();
    
    // 包含这些关键词的通常是纯数据，用 CSV
    const csvKeywords = [
      'list', '列表', 'constituents', '成分股',
      'shareholders', '股东', 'fund-list', '基金列表',
      'valuation', '估值', 'fundamental', '基本面'
    ];
    
    for (const keyword of csvKeywords) {
      if (name.includes(keyword) || desc.includes(keyword)) {
        return 'csv';
      }
    }
    
    // 包含这些关键词的通常是详情页，用 MD
    const mdKeywords = [
      'detail', '详情', 'doc', '文档',
      'profile', '简介', 'chart-maker', '图表'
    ];
    
    for (const keyword of mdKeywords) {
      if (name.includes(keyword) || desc.includes(keyword)) {
        return 'md';
      }
    }
    
    // 默认用 MD
    return 'md';
  }

  /**
   * 保存配置文件
   */
  saveConfigs(configs) {
    // 保存为 JSONL 格式（每行一个 JSON）
    const jsonlPath = path.join(this.outputDir, 'api-configs.jsonl');
    const lines = configs.map(config => JSON.stringify(config));
    fs.writeFileSync(jsonlPath, lines.join('\n'));
    
    // 也保存为单个 JSON 文件方便查看
    const jsonPath = path.join(this.outputDir, 'api-configs.json');
    fs.writeFileSync(jsonPath, JSON.stringify(configs, null, 2));
    
    console.log(`✓ 配置文件已保存:`);
    console.log(`  - ${jsonlPath}`);
    console.log(`  - ${jsonPath}`);
  }

  /**
   * 生成 README
   */
  generateReadme() {
    const lines = [];
    lines.push('# Web API 文档');
    lines.push('');
    lines.push(`总计: ${this.patterns.length} 个 API`);
    lines.push('');
    lines.push('## 配置文件');
    lines.push('');
    lines.push('- `api-configs.json`: 所有 API 的配置（JSON 格式）');
    lines.push('- `api-configs.jsonl`: 所有 API 的配置（JSONL 格式，每行一个）');
    lines.push('');
    lines.push('配置文件定义了每个 API 的输入参数和输出格式（CSV 或 MD）。');
    lines.push('');
    
    fs.writeFileSync(path.join(this.outputDir, 'README.md'), lines.join('\n'));
  }
}

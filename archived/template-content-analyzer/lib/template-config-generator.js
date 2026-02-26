const fs = require('fs');
const path = require('path');

/**
 * TemplateConfigGenerator - 根据模板分析结果生成JSONL格式的配置文件
 * 
 * 职责：
 * 1. 生成模板配置对象
 * 2. 生成提取器配置（extractors）
 * 3. 生成过滤器配置（filters）
 * 4. 保存为JSONL格式
 */
class TemplateConfigGenerator {
  /**
   * 生成模板配置对象
   * @param {Object} urlPattern - URL模式对象
   * @param {Object} analysisResult - 模板分析结果
   * @returns {Object} 模板配置对象
   */
  generateConfig(urlPattern, analysisResult) {
    const { stats, classified, dataStructures, cleaningRules } = analysisResult;

    // 生成提取器和过滤器
    const extractors = this.generateExtractors(dataStructures, classified);
    const filters = this.generateFilters(cleaningRules, classified);

    // 返回完整配置
    return {
      name: urlPattern.name,
      description: `Parser configuration for ${urlPattern.pathTemplate}`,
      priority: 100,
      urlPattern: {
        pattern: urlPattern.pattern,
        pathTemplate: urlPattern.pathTemplate,
        queryParams: urlPattern.queryParams || []
      },
      extractors,
      filters,
      metadata: {
        generatedAt: new Date().toISOString(),
        pageCount: stats.totalPages,
        version: '1.0.0'
      }
    };
  }

  /**
   * 生成提取器配置
   * @param {Object} dataStructures - 数据结构信息
   * @param {Object} classified - 分类后的内容
   * @returns {Array<Object>} 提取器配置数组
   */
  generateExtractors(dataStructures, classified) {
    const extractors = [];

    // 1. 标题提取器（必需）
    extractors.push(this.generateTextExtractor('title', 'h1, h2, title', true));

    // 2. 表格提取器
    if (dataStructures.tables && dataStructures.tables.length > 0) {
      dataStructures.tables.forEach((table, index) => {
        const field = index === 0 ? 'mainTable' : `table${index}`;
        extractors.push(this.generateTableExtractor(field, 'table', table.columns));
      });
    }

    // 3. 代码块提取器
    if (dataStructures.codeBlocks && dataStructures.codeBlocks.length > 0) {
      extractors.push(this.generateCodeExtractor('codeBlocks', 'pre code, pre, textarea[readonly]'));
    }

    // 4. 列表提取器
    if (dataStructures.lists && dataStructures.lists.length > 0) {
      extractors.push(this.generateListExtractor('lists', 'ul, ol'));
    }

    return extractors;
  }

  /**
   * 生成文本提取器配置
   * @param {string} field - 字段名
   * @param {string} selector - CSS选择器
   * @param {boolean} required - 是否必需
   * @param {string} pattern - 可选的匹配模式
   * @returns {Object} 文本提取器配置
   */
  generateTextExtractor(field, selector, required = false, pattern = null) {
    const extractor = {
      field,
      type: 'text',
      selector,
      required
    };

    // 如果提供了匹配模式，添加到配置中
    if (pattern) {
      extractor.pattern = pattern;
    }

    return extractor;
  }

  /**
   * 生成表格提取器配置
   * @param {string} field - 字段名
   * @param {string} selector - CSS选择器
   * @param {Array<string>} columns - 表格列名
   * @returns {Object} 表格提取器配置
   */
  generateTableExtractor(field, selector, columns) {
    return {
      field,
      type: 'table',
      selector,
      columns
    };
  }

  /**
   * 生成代码块提取器配置
   * @param {string} field - 字段名
   * @param {string} selector - CSS选择器
   * @returns {Object} 代码块提取器配置
   */
  generateCodeExtractor(field, selector) {
    return {
      field,
      type: 'code',
      selector
    };
  }

  /**
   * 生成列表提取器配置
   * @param {string} field - 字段名
   * @param {string} selector - CSS选择器
   * @returns {Object} 列表提取器配置
   */
  generateListExtractor(field, selector) {
    return {
      field,
      type: 'list',
      selector
    };
  }

  /**
   * 生成过滤器配置
   * @param {Object} cleaningRules - 清洗规则
   * @param {Object} classified - 分类后的内容
   * @returns {Array<Object>} 过滤器配置数组
   */
  /**
     * 生成过滤器配置
     * @param {Object} cleaningRules - 清洗规则
     * @param {Object} classified - 分类后的内容
     * @returns {Array<Object>} 过滤器配置数组
     */
    generateFilters(cleaningRules, classified) {
      const filters = [];

      // 4.4.1: 基于清洗规则生成移除过滤器
      if (cleaningRules && cleaningRules.removePatterns) {
        cleaningRules.removePatterns.forEach(pattern => {
          filters.push({
            type: 'remove',
            target: pattern.target,
            pattern: pattern.pattern,
            reason: pattern.reason
          });
        });
      }

      // 4.4.1: 基于高频模板内容生成额外的移除过滤器
      if (classified && classified.template) {
        classified.template
          .filter(item => item.ratio > 0.95) // 只过滤出现率>95%的内容
          .slice(0, 5) // 最多添加5个
          .forEach(item => {
            // 避免重复
            const exists = filters.some(f => 
              f.pattern === this._escapeRegex(item.content.substring(0, 50))
            );

            if (!exists) {
              filters.push({
                type: 'remove',
                target: item.type,
                pattern: this._escapeRegex(item.content.substring(0, 50)),
                reason: `High frequency template content (${(item.ratio * 100).toFixed(1)}%)`
              });
            }
          });
      }

      // 4.4.2: 基于清洗规则生成保留过滤器
      if (cleaningRules && cleaningRules.keepPatterns) {
        cleaningRules.keepPatterns.forEach(pattern => {
          filters.push({
            type: 'keep',
            target: pattern.target,
            contentType: pattern.contentType,
            reason: pattern.reason
          });
        });
      }

      // 4.4.2: 基于低频独特内容生成保留过滤器
      if (classified && classified.unique) {
        classified.unique
          .filter(item => item.ratio < 0.2 && item.ratio > 0) // 低频但非零
          .slice(0, 3) // 最多添加3个保留规则
          .forEach(item => {
            // 生成保留规则的模式
            const contentType = this._inferContentType(item.content, item.type);

            if (contentType && contentType !== 'unknown') {
              filters.push({
                type: 'keep',
                target: item.type,
                contentType: contentType,
                reason: `Unique data content (${(item.ratio * 100).toFixed(1)}% frequency)`
              });
            }
          });
      }

      return filters;
    }

    /**
     * 推断内容类型
     * @param {string} content - 内容文本
     * @param {string} blockType - 块类型
     * @returns {string} 内容类型
     * @private
     */
    _inferContentType(content, blockType) {
      // 根据内容特征推断类型
      const lowerContent = content.toLowerCase();

      // API相关
      if (lowerContent.match(/获取|查询|创建|更新|删除|api|request|response/)) {
        return 'api_description';
      }

      // 数据字段
      if (lowerContent.match(/参数|字段|属性|类型|说明|必选|可选/)) {
        return 'data_field';
      }

      // 代码示例
      if (blockType === 'code' || lowerContent.match(/example|示例|代码/)) {
        return 'code_example';
      }

      // 表格数据
      if (blockType === 'table') {
        return 'structured_data';
      }

      // 列表数据
      if (blockType === 'list') {
        return 'list_data';
      }

      return 'unknown';
    }

  /**
   * 保存配置为JSONL格式
   * @param {Array<Object>} configs - 配置对象数组
   * @param {string} outputPath - 输出文件路径
   * @returns {Promise<void>}
   */
  async saveAsJSONL(configs, outputPath) {
    // 确保输出目录存在
    const outputDir = path.dirname(outputPath);
    await fs.promises.mkdir(outputDir, { recursive: true });

    // 将每个配置对象转换为JSON字符串，每行一个
    const jsonlContent = configs.map(config => JSON.stringify(config)).join('\n');

    // 写入文件
    await fs.promises.writeFile(outputPath, jsonlContent, 'utf-8');
  }

  /**
   * 转义正则表达式特殊字符
   * @param {string} str - 要转义的字符串
   * @returns {string} 转义后的字符串
   * @private
   */
  /**
     * 转义正则表达式特殊字符
     * @param {string} str - 要转义的字符串
     * @returns {string} 转义后的字符串
     * @private
     */
    _escapeRegex(str) {
      return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }
}

module.exports = TemplateConfigGenerator;

const fs = require('fs');
const path = require('path');
const TemplateConfigGenerator = require('./template-config-generator');

/**
 * ConfigLoader - 从JSONL文件加载模板配置并创建Parser实例
 * 
 * 职责：
 * 1. 从JSONL文件加载配置
 * 2. 验证配置格式
 * 3. 创建TemplateParser实例
 * 4. 处理加载错误
 */
class ConfigLoader {
  /**
   * 从JSONL文件加载配置
   * @param {string} jsonlPath - JSONL文件路径
   * @returns {Array<Object>} 配置对象数组
   * @throws {Error} 文件不存在或格式错误时抛出异常
   */
  static loadConfigs(jsonlPath) {
    // 检查文件是否存在
    if (!fs.existsSync(jsonlPath)) {
      throw new Error(`Config file not found: ${jsonlPath}`);
    }

    try {
      // 读取文件内容
      const content = fs.readFileSync(jsonlPath, 'utf-8');
      
      // 处理空文件
      if (!content.trim()) {
        throw new Error(`Config file is empty: ${jsonlPath}`);
      }

      // 按行分割并解析JSON
      const lines = content.trim().split('\n');
      const configs = [];
      const errors = [];

      lines.forEach((line, index) => {
        const lineNum = index + 1;
        
        // 跳过空行
        if (!line.trim()) {
          return;
        }

        try {
          const config = JSON.parse(line);
          
          // 验证配置
          const validationError = this.validateConfig(config, lineNum);
          if (validationError) {
            errors.push(validationError);
          } else {
            configs.push(config);
          }
        } catch (error) {
          errors.push(`Line ${lineNum}: Invalid JSON - ${error.message}`);
        }
      });

      // 如果有错误，抛出异常
      if (errors.length > 0) {
        throw new Error(`Config validation failed:\n${errors.join('\n')}`);
      }

      return configs;
    } catch (error) {
      if (error.message.includes('Config validation failed')) {
        throw error;
      }
      throw new Error(`Failed to load configs from ${jsonlPath}: ${error.message}`);
    }
  }

  /**
   * 验证配置对象
   * @param {Object} config - 配置对象
   * @param {number} lineNum - 行号（用于错误报告）
   * @returns {string|null} 错误信息，如果验证通过则返回null
   */
  static validateConfig(config, lineNum) {
    const errors = [];

    // 检查必需字段
    const requiredFields = ['name', 'urlPattern', 'extractors'];
    requiredFields.forEach(field => {
      if (!config[field]) {
        errors.push(`Missing required field: ${field}`);
      }
    });

    // 验证urlPattern
    if (config.urlPattern) {
      if (!config.urlPattern.pattern) {
        errors.push('urlPattern.pattern is required');
      }
      if (!config.urlPattern.pathTemplate) {
        errors.push('urlPattern.pathTemplate is required');
      }
    }

    // 验证extractors
    if (config.extractors) {
      if (!Array.isArray(config.extractors)) {
        errors.push('extractors must be an array');
      } else if (config.extractors.length === 0) {
        errors.push('extractors array cannot be empty');
      } else {
        config.extractors.forEach((extractor, idx) => {
          if (!extractor.field) {
            errors.push(`extractors[${idx}]: Missing field name`);
          }
          if (!extractor.type) {
            errors.push(`extractors[${idx}]: Missing type`);
          }
          if (!extractor.selector) {
            errors.push(`extractors[${idx}]: Missing selector`);
          }
          
          // 验证type是否有效
          const validTypes = ['text', 'table', 'code', 'list'];
          if (extractor.type && !validTypes.includes(extractor.type)) {
            errors.push(`extractors[${idx}]: Invalid type "${extractor.type}". Must be one of: ${validTypes.join(', ')}`);
          }
        });
      }
    }

    // 验证filters（可选）
    if (config.filters && !Array.isArray(config.filters)) {
      errors.push('filters must be an array');
    }

    if (errors.length > 0) {
      return `Line ${lineNum} (${config.name || 'unnamed'}): ${errors.join('; ')}`;
    }

    return null;
  }

  /**
   * 创建Parser实例
   * @param {string} jsonlPath - JSONL文件路径
   * @param {Class} ParserClass - Parser类（默认为TemplateParser）
   * @returns {Array<Object>} Parser实例数组
   * @throws {Error} 加载或创建失败时抛出异常
   */
  static createParsers(jsonlPath, ParserClass = null) {
    try {
      const configs = this.loadConfigs(jsonlPath);
      
      // 如果没有提供ParserClass，返回配置对象
      // 这样可以在没有TemplateParser的情况下测试ConfigLoader
      if (!ParserClass) {
        console.warn('No ParserClass provided, returning config objects');
        return configs;
      }

      // 创建Parser实例
      return configs.map(config => {
        try {
          return new ParserClass(config);
        } catch (error) {
          throw new Error(`Failed to create parser for "${config.name}": ${error.message}`);
        }
      });
    } catch (error) {
      throw new Error(`Failed to create parsers: ${error.message}`);
    }
  }

  /**
   * 加载单个配置（按名称）
   * @param {string} jsonlPath - JSONL文件路径
   * @param {string} name - 配置名称
   * @returns {Object|null} 配置对象，如果未找到则返回null
   */
  static loadConfigByName(jsonlPath, name) {
    const configs = this.loadConfigs(jsonlPath);
    return configs.find(config => config.name === name) || null;
  }

  /**
   * 获取配置统计信息
   * @param {string} jsonlPath - JSONL文件路径
   * @returns {Object} 统计信息
   */
  static getConfigStats(jsonlPath) {
    const configs = this.loadConfigs(jsonlPath);
    
    const stats = {
      totalConfigs: configs.length,
      configNames: configs.map(c => c.name),
      totalExtractors: 0,
      totalFilters: 0,
      extractorTypes: {},
      filterTypes: {}
    };

    configs.forEach(config => {
      // 统计extractors
      if (config.extractors) {
        stats.totalExtractors += config.extractors.length;
        config.extractors.forEach(ext => {
          stats.extractorTypes[ext.type] = (stats.extractorTypes[ext.type] || 0) + 1;
        });
      }

      // 统计filters
      if (config.filters) {
        stats.totalFilters += config.filters.length;
        config.filters.forEach(filter => {
          stats.filterTypes[filter.type] = (stats.filterTypes[filter.type] || 0) + 1;
        });
      }
    });

    return stats;
  }

  /**
   * 生成模板配置对象
   * @param {Object} urlPattern - URL模式对象
   * @param {Object} analysisResult - 模板分析结果
   * @returns {Object} 模板配置对象
   */
  static generateTemplateConfig(urlPattern, analysisResult) {
    const generator = new TemplateConfigGenerator();
    return generator.generateConfig(urlPattern, analysisResult);
  }
}

module.exports = ConfigLoader;

import fs from 'fs';
import path from 'path';

/**
 * Config Manager - 负责读取和验证配置文件
 */
class ConfigManager {
  /**
   * 加载配置文件
   * @param {string} configPath - 配置文件路径
   * @returns {Object} 配置对象
   * @throws {Error} 配置文件不存在或格式错误
   */
  loadConfig(configPath) {
    // 检查文件是否存在
    if (!fs.existsSync(configPath)) {
      throw new Error(`配置文件不存在: ${configPath}`);
    }

    try {
      // 读取文件内容
      const fileContent = fs.readFileSync(configPath, 'utf-8');
      
      // 解析JSON
      const config = JSON.parse(fileContent);
      
      // 验证配置
      this.validateConfig(config);
      
      return config;
    } catch (error) {
      if (error instanceof SyntaxError) {
        throw new Error(`配置文件JSON格式错误: ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * 验证配置完整性
   * @param {Object} config - 配置对象
   * @returns {boolean} 是否有效
   * @throws {Error} 配置无效时抛出错误
   */
  validateConfig(config) {
    // 首先检查config是否是有效对象
    if (!config || typeof config !== 'object' || Array.isArray(config)) {
      throw new Error('配置必须是有效的对象类型');
    }

    const requiredFields = {
      name: 'string',
      seedUrls: 'array',
      urlRules: 'object',
      crawler: 'object',
      output: 'object'
    };

    // 检查必需字段
    for (const [field, type] of Object.entries(requiredFields)) {
      if (!(field in config)) {
        throw new Error(`配置缺少必需字段: ${field}`);
      }

      // 类型检查
      if (type === 'array' && !Array.isArray(config[field])) {
        throw new Error(`配置字段 ${field} 必须是数组类型`);
      } else if (type === 'object' && (typeof config[field] !== 'object' || Array.isArray(config[field]))) {
        throw new Error(`配置字段 ${field} 必须是对象类型`);
      } else if (type === 'string' && typeof config[field] !== 'string') {
        throw new Error(`配置字段 ${field} 必须是字符串类型`);
      }
    }

    // 验证 seedUrls 不为空
    if (config.seedUrls.length === 0) {
      throw new Error('配置字段 seedUrls 不能为空数组');
    }

    // 验证 urlRules 包含 include 和 exclude
    if (!('include' in config.urlRules) || !Array.isArray(config.urlRules.include)) {
      throw new Error('配置字段 urlRules.include 必须存在且为数组类型');
    }
    if (!('exclude' in config.urlRules) || !Array.isArray(config.urlRules.exclude)) {
      throw new Error('配置字段 urlRules.exclude 必须存在且为数组类型');
    }

    // 验证 crawler 必需字段
    const crawlerRequiredFields = ['headless', 'timeout', 'waitBetweenRequests', 'maxRetries'];
    for (const field of crawlerRequiredFields) {
      if (!(field in config.crawler)) {
        throw new Error(`配置字段 crawler.${field} 必须存在`);
      }
    }

    // 验证 output 必需字段
    if (!('directory' in config.output)) {
      throw new Error('配置字段 output.directory 必须存在');
    }
    if (!('format' in config.output)) {
      throw new Error('配置字段 output.format 必须存在');
    }

    return true;
  }
}

export default ConfigManager;

/**
 * Links Reader - 读取和解析links.txt文件
 * 
 * 负责读取JSON格式的links文件并提取URL信息
 */

const fs = require('fs').promises;
const path = require('path');

class LinksReader {
  /**
   * 读取links.txt文件
   * @param {string} filePath - links.txt文件路径
   * @returns {Promise<Array>} URL记录数组
   */
  async readLinksFile(filePath) {
    try {
      // 读取文件内容
      const content = await fs.readFile(filePath, 'utf-8');
      
      // 按行分割
      const lines = content.trim().split('\n');
      
      // 解析每一行的JSON
      const records = [];
      const errors = [];
      
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        
        // 跳过空行
        if (!line) {
          continue;
        }
        
        try {
          const record = JSON.parse(line);
          records.push(record);
        } catch (error) {
          // 记录解析错误但继续处理其他行
          errors.push({
            line: i + 1,
            content: line.substring(0, 100), // 只记录前100个字符
            error: error.message
          });
        }
      }
      
      // 如果有错误，记录警告
      if (errors.length > 0) {
        console.warn(`Warning: Failed to parse ${errors.length} lines in ${filePath}`);
        errors.slice(0, 5).forEach(err => {
          console.warn(`  Line ${err.line}: ${err.error}`);
        });
        if (errors.length > 5) {
          console.warn(`  ... and ${errors.length - 5} more errors`);
        }
      }
      
      return records;
    } catch (error) {
      // 文件读取错误
      if (error.code === 'ENOENT') {
        throw new Error(`Links file not found: ${filePath}`);
      } else if (error.code === 'EACCES') {
        throw new Error(`Permission denied reading file: ${filePath}`);
      } else {
        throw new Error(`Failed to read links file: ${error.message}`);
      }
    }
  }
  
  /**
   * 从记录中提取URL列表
   * @param {Array} records - URL记录数组
   * @param {Object} options - 过滤选项
   * @param {string} options.status - 只包含特定状态的URL (如 'fetched')
   * @param {boolean} options.excludeErrors - 排除有错误的URL
   * @returns {string[]} URL字符串数组
   */
  extractURLs(records, options = {}) {
    const { status, excludeErrors = false } = options;
    
    return records
      .filter(record => {
        // 检查是否有url字段
        if (!record.url) {
          return false;
        }
        
        // 按状态过滤
        if (status && record.status !== status) {
          return false;
        }
        
        // 排除有错误的记录
        if (excludeErrors && record.error) {
          return false;
        }
        
        return true;
      })
      .map(record => record.url);
  }
  
  /**
   * 解析URL字符串为URL对象
   * @param {string[]} urlStrings - URL字符串数组
   * @param {Object} options - 解析选项
   * @param {boolean} options.skipInvalid - 跳过无效的URL（默认false）
   * @returns {URL[]} URL对象数组
   */
  parseURLs(urlStrings, options = {}) {
    const { skipInvalid = false } = options;
    const urlObjects = [];
    const errors = [];
    
    for (let i = 0; i < urlStrings.length; i++) {
      const urlString = urlStrings[i];
      
      try {
        const urlObject = new URL(urlString);
        urlObjects.push(urlObject);
      } catch (error) {
        // 记录解析错误
        errors.push({
          index: i,
          url: urlString,
          error: error.message
        });
        
        // 如果不跳过无效URL，抛出错误
        if (!skipInvalid) {
          throw new Error(`Invalid URL at index ${i}: ${urlString} - ${error.message}`);
        }
      }
    }
    
    // 如果有错误且选择跳过，记录警告
    if (errors.length > 0 && skipInvalid) {
      console.warn(`Warning: Skipped ${errors.length} invalid URLs`);
      errors.slice(0, 3).forEach(err => {
        console.warn(`  Index ${err.index}: ${err.url} - ${err.error}`);
      });
      if (errors.length > 3) {
        console.warn(`  ... and ${errors.length - 3} more errors`);
      }
    }
    
    return urlObjects;
  }
  
  /**
   * 获取统计信息
   * @param {Array} records - URL记录数组
   * @returns {Object} 统计信息
   */
  getStatistics(records) {
    const stats = {
      total: records.length,
      byStatus: {},
      withErrors: 0,
      withoutUrl: 0
    };
    
    records.forEach(record => {
      // 统计状态
      if (record.status) {
        stats.byStatus[record.status] = (stats.byStatus[record.status] || 0) + 1;
      }
      
      // 统计错误
      if (record.error) {
        stats.withErrors++;
      }
      
      // 统计缺少URL的记录
      if (!record.url) {
        stats.withoutUrl++;
      }
    });
    
    return stats;
  }
}

module.exports = LinksReader;

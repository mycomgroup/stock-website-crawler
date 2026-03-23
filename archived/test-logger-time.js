#!/usr/bin/env node

/**
 * 测试Logger的北京时间功能
 */

import Logger from '../stock-crawler/src/logger.js';
import fs from 'fs';

console.log('='.repeat(80));
console.log('Logger 北京时间测试');
console.log('='.repeat(80));
console.log('');

// 创建logger实例
const logger = new Logger('./logs/test', 'DEBUG');

console.log('当前系统时间（UTC）:', new Date().toISOString());
console.log('当前北京时间:', logger.getBeijingTime());
console.log('');

// 测试各种日志级别
console.log('测试各种日志级别:');
console.log('-'.repeat(80));
logger.debug('这是一条调试日志');
logger.info('这是一条信息日志');
logger.warn('这是一条警告日志');
logger.error('这是一条错误日志');
logger.success('这是一条成功日志');
console.log('');

// 测试URL状态日志
console.log('测试URL状态日志:');
console.log('-'.repeat(80));
logger.logUrlStatus('https://example.com/page1', 'success', '成功抓取');
logger.logUrlStatus('https://example.com/page2', 'failed', '连接超时');
logger.logUrlStatus('https://example.com/page3', 'skipped', '已存在');
console.log('');

// 测试进度日志
console.log('测试进度日志:');
console.log('-'.repeat(80));
logger.progress(5, 10, '正在处理...');
logger.progress(10, 10, '处理完成');
console.log('');

// 显示日志文件信息
console.log('日志文件信息:');
console.log('-'.repeat(80));
console.log('日志文件路径:', logger.getLogFile());
console.log('日志文件名格式: crawler-YYYYMMDD-HHmmss.log (北京时间)');
console.log('');

// 读取并显示日志文件内容
console.log('日志文件内容预览:');
console.log('-'.repeat(80));
try {
  const logContent = fs.readFileSync(logger.getLogFile(), 'utf-8');
  const lines = logContent.split('\n').slice(0, 10);
  lines.forEach(line => {
    if (line.trim()) {
      console.log(line);
    }
  });
  console.log('...');
} catch (error) {
  console.error('读取日志文件失败:', error.message);
}
console.log('');

console.log('='.repeat(80));
console.log('测试完成！');
console.log('='.repeat(80));
console.log('');
console.log('时间格式说明:');
console.log('- 日志内容时间格式: YYYY-MM-DD HH:mm:ss (北京时间)');
console.log('- 日志文件名格式: crawler-YYYYMMDD-HHmmss.log (北京时间)');
console.log('- 所有时间均为北京时间（UTC+8）');

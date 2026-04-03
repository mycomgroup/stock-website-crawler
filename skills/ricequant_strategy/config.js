// RiceQuant 改进配置
export const RICEQUANT_CONFIG = {
  // 重试配置
  retry: {
    maxRetries: 5,           // 最大重试次数
    baseDelay: 5000,         // 基础延迟（毫秒）
    maxDelay: 60000,         // 最大延迟（毫秒）
    backoffFactor: 2,         // 退避因子
  },
  
  // 超时配置
  timeout: {
    request: 30000,          // 请求超时（30秒）
    backtest: 600000,        // 回测超时（10分钟）
    polling: 5000,           // 轮询间隔（5秒）
    maxPolls: 120,           // 最大轮询次数（120次 = 10分钟）
  },
  
  // 需要重试的错误
  retryOnErrors: [
    'ECONNRESET',
    'ETIMEDOUT',
    'ENOTFOUND',
    'ECONNREFUSED',
    '502',
    '503',
    '504',
    'Gateway Time-out',
    'Bad Gateway',
    'Service Temporarily Unavailable',
    'network',
    'timeout'
  ]
};

// 重试函数
export async function retryWithBackoff(fn, options = {}) {
  const config = { ...RICEQUANT_CONFIG.retry, ...options };
  
  let lastError;
  
  for (let attempt = 0; attempt < config.maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      const errorMsg = error.message || String(error);
      
      // 检查是否应该重试
      const shouldRetry = RICEQUANT_CONFIG.retryOnErrors.some(pattern => 
        errorMsg.toLowerCase().includes(pattern.toLowerCase())
      );
      
      if (!shouldRetry || attempt === config.maxRetries - 1) {
        throw error;
      }
      
      // 计算延迟时间（指数退避 + 随机抖动）
      const delay = Math.min(
        config.baseDelay * Math.pow(config.backoffFactor, attempt),
        config.maxDelay
      ) + Math.random() * 1000;
      
      console.log(`   ⚠️  Attempt ${attempt + 1}/${config.maxRetries} failed`);
      console.log(`   📝 Error: ${errorMsg.slice(0, 100)}`);
      console.log(`   ⏳  Retrying in ${(delay/1000).toFixed(1)}s...`);
      
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  throw lastError;
}

// 带超时的请求
export async function fetchWithTimeout(url, options = {}, timeout = RICEQUANT_CONFIG.timeout.request) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);
  
  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal
    });
    return response;
  } finally {
    clearTimeout(timeoutId);
  }
}

// 使用示例
/*
import { retryWithBackoff, fetchWithTimeout, RICEQUANT_CONFIG } from './config.js';

// 重试API调用
const result = await retryWithBackoff(
  () => client.runBacktest(id, code, params),
  { maxRetries: 5, baseDelay: 5000 }
);

// 带超时的请求
const response = await fetchWithTimeout(url, { method: 'POST' }, 30000);
*/
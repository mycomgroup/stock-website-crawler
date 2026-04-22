/**
 * BigQuant 增强版HTTP客户端
 * 集成防封措施
 */

import { AntiDetection, RateLimiter, SessionManager } from '../lib/anti-detection.js';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const SESSION_FILE = path.join(__dirname, '../data/session.json');
const BASE_URL = 'https://bigquant.com';

/**
 * BigQuant增强版客户端
 */
export class EnhancedBigQuantClient {
  constructor(options = {}) {
    this.baseURL = options.baseURL || BASE_URL;
    this.sessionManager = new SessionManager(SESSION_FILE, {
      maxAge: options.sessionMaxAge || 7 * 24 * 60 * 60 * 1000,
      validateUrl: `${this.baseURL}/api/user/info`
    });
    this.limiter = new RateLimiter({
      minDelay: options.minDelay || 1000,
      maxDelay: options.maxDelay || 3000
    });
    this.session = null;
    this.retryOptions = {
      maxRetries: options.maxRetries || 3,
      retryDelay: options.retryDelay || 2000,
      backoff: true
    };
  }

  /**
   * 初始化客户端
   */
  async init() {
    console.log('🔧 Initializing BigQuant client...');
    
    // 加载session
    if (!(await this.sessionManager.isValid())) {
      throw new Error(
        'No valid session found. Please run anti-detection-capture.js first.'
      );
    }
    
    this.session = await this.sessionManager.load();
    console.log('✅ Session loaded successfully');
  }

  /**
   * 获取请求headers
   */
  getHeaders(customHeaders = {}) {
    if (!this.session) {
      throw new Error('Client not initialized. Call init() first.');
    }

    const cookieString = this.session.cookies
      .map(c => `${c.name}=${c.value}`)
      .join('; ');

    return AntiDetection.createRealisticHeaders({
      'Referer': this.baseURL,
      'Origin': this.baseURL,
      'Cookie': cookieString,
      ...customHeaders
    });
  }

  /**
   * 发送请求
   */
  async request(endpoint, options = {}) {
    // 限流
    await this.limiter.wait();

    const url = endpoint.startsWith('http') 
      ? endpoint 
      : `${this.baseURL}${endpoint}`;

    const headers = this.getHeaders(options.headers);

    console.log(`📡 ${options.method || 'GET'} ${endpoint}`);

    // 带重试的请求
    const response = await AntiDetection.fetchWithRetry(
      () => fetch(url, {
        ...options,
        headers
      }),
      this.retryOptions
    );

    // 检查session是否失效
    if (response.status === 401 || response.status === 403) {
      console.warn('⚠️ Session may be invalid (401/403)');
      await this.sessionManager.clear();
      throw new Error('Session invalid. Please re-capture session.');
    }

    return response;
  }

  /**
   * GET请求
   */
  async get(endpoint, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const url = queryString ? `${endpoint}?${queryString}` : endpoint;
    
    const response = await this.request(url, {
      method: 'GET'
    });
    
    return await response.json();
  }

  /**
   * POST请求
   */
  async post(endpoint, data = {}, options = {}) {
    const { headers: customHeaders, ...restOptions } = options;
    const response = await this.request(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...customHeaders
      },
      body: JSON.stringify(data),
      ...restOptions
    });
    
    return await response.json();
  }

  /**
   * PUT请求
   */
  async put(endpoint, data = {}) {
    const response = await this.request(endpoint, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    
    return await response.json();
  }

  /**
   * DELETE请求
   */
  async delete(endpoint) {
    const response = await this.request(endpoint, {
      method: 'DELETE'
    });
    
    return await response.json();
  }

  /**
   * 获取用户信息
   */
  async getUserInfo() {
    return await this.get('/api/user/info');
  }

  /**
   * 获取策略列表
   */
  async getStrategies(params = {}) {
    return await this.get('/api/strategies', params);
  }

  /**
   * 创建策略
   */
  async createStrategy(strategyData) {
    return await this.post('/api/strategies', strategyData);
  }

  /**
   * 更新策略
   */
  async updateStrategy(strategyId, strategyData) {
    return await this.put(`/api/strategies/${strategyId}`, strategyData);
  }

  /**
   * 运行回测
   */
  async runBacktest(strategyId, backtestConfig) {
    console.log(`🚀 Running backtest for strategy ${strategyId}...`);
    return await this.post(`/api/strategies/${strategyId}/backtest`, backtestConfig);
  }

  /**
   * 获取回测结果
   */
  async getBacktestResult(backtestId) {
    return await this.get(`/api/backtests/${backtestId}`);
  }

  /**
   * 轮询回测结果
   */
  async pollBacktestResult(backtestId, options = {}) {
    const maxAttempts = options.maxAttempts || 60;
    const pollInterval = options.pollInterval || 5000;
    
    console.log(`⏳ Polling backtest result (id: ${backtestId})...`);
    
    for (let i = 0; i < maxAttempts; i++) {
      const result = await this.getBacktestResult(backtestId);
      
      if (result.status === 'completed') {
        console.log('✅ Backtest completed!');
        return result;
      }
      
      if (result.status === 'failed') {
        throw new Error(`Backtest failed: ${result.error}`);
      }
      
      console.log(`⏳ Status: ${result.status} (${i + 1}/${maxAttempts})`);
      
      // 随机延迟
      await AntiDetection.randomDelay(
        pollInterval,
        pollInterval + 2000
      );
    }
    
    throw new Error('Backtest timeout');
  }

  /**
   * 批量运行回测
   */
  async batchRunBacktests(backtests) {
    console.log(`📊 Running ${backtests.length} backtests...`);
    
    const results = [];
    
    for (const [index, backtest] of backtests.entries()) {
      console.log(`\n[${index + 1}/${backtests.length}] ${backtest.name}`);
      
      try {
        // 运行回测
        const result = await this.runBacktest(
          backtest.strategyId,
          backtest.config
        );
        
        // 轮询结果
        const finalResult = await this.pollBacktestResult(result.backtestId);
        
        results.push({
          name: backtest.name,
          success: true,
          result: finalResult
        });
        
        // 额外的随机延迟
        await AntiDetection.randomDelay(2000, 5000);
        
      } catch (error) {
        console.error(`❌ Failed: ${error.message}`);
        results.push({
          name: backtest.name,
          success: false,
          error: error.message
        });
      }
    }
    
    // 统计
    const successCount = results.filter(r => r.success).length;
    console.log(`\n✅ Completed: ${successCount}/${backtests.length}`);
    
    return results;
  }
}

/**
 * 使用示例
 */
async function example() {
  const client = new EnhancedBigQuantClient({
    minDelay: 2000,
    maxDelay: 4000,
    maxRetries: 3
  });

  try {
    // 初始化
    await client.init();

    // 获取用户信息
    const userInfo = await client.getUserInfo();
    console.log('User:', userInfo);

    // 获取策略列表
    const strategies = await client.getStrategies({ limit: 10 });
    console.log('Strategies:', strategies);

    // 运行回测
    const backtest = await client.runBacktest('strategy-id', {
      startDate: '2023-01-01',
      endDate: '2023-12-31',
      initialCapital: 1000000
    });

    // 轮询结果
    const result = await client.pollBacktestResult(backtest.backtestId);
    console.log('Result:', result);

  } catch (error) {
    console.error('Error:', error.message);
  }
}

// 如果直接运行此脚本
if (import.meta.url === `file://${process.argv[1]}`) {
  example();
}

export default EnhancedBigQuantClient;

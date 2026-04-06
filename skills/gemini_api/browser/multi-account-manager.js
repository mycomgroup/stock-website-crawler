import { readFileSync, writeFileSync, existsSync, readdirSync } from 'fs';
import { PATHS } from '../paths.js';
import { captureSession, validateSessionInBrowser } from './capture-session.js';
import { SessionManager } from './session-manager.js';

/**
 * 多账号管理器
 * 支持多个 ChatGPT 账号，自动负载均衡
 */
export class MultiAccountManager {
  constructor() {
    this.accounts = [];
    this.currentIndex = 0;
    this.accountsDir = `${PATHS.data}/accounts`;
    this.configFile = `${PATHS.data}/accounts-config.json`;
    this.loadAccounts();
  }

  /**
   * 加载所有账号
   */
  loadAccounts() {
    if (!existsSync(this.accountsDir)) {
      return;
    }

    try {
      // 加载配置
      let config = { accounts: [], strategy: 'round-robin' };
      if (existsSync(this.configFile)) {
        config = JSON.parse(readFileSync(this.configFile, 'utf-8'));
      }

      // 加载所有 session 文件
      const files = readdirSync(this.accountsDir)
        .filter(f => f.endsWith('.json') && f.startsWith('session-'));

      this.accounts = files.map(file => {
        const accountId = file.replace('session-', '').replace('.json', '');
        const sessionPath = `${this.accountsDir}/${file}`;
        const sessionData = JSON.parse(readFileSync(sessionPath, 'utf-8'));
        
        // 查找配置
        const accountConfig = config.accounts.find(a => a.id === accountId) || {};
        
        return {
          id: accountId,
          name: accountConfig.name || accountId,
          sessionPath,
          sessionData,
          enabled: accountConfig.enabled !== false,
          weight: accountConfig.weight || 1,
          requestCount: 0,
          lastUsed: null,
          status: 'unknown' // unknown, active, expired, error
        };
      });

      this.strategy = config.strategy || 'round-robin';

      console.log(`📂 加载了 ${this.accounts.length} 个账号`);

    } catch (error) {
      console.error('❌ 加载账号失败:', error.message);
    }
  }

  /**
   * 保存配置
   */
  saveConfig() {
    const config = {
      strategy: this.strategy,
      accounts: this.accounts.map(acc => ({
        id: acc.id,
        name: acc.name,
        enabled: acc.enabled,
        weight: acc.weight
      }))
    };

    writeFileSync(this.configFile, JSON.stringify(config, null, 2), 'utf-8');
  }

  /**
   * 添加账号
   */
  async addAccount(options = {}) {
    const { name, id } = options;
    const accountId = id || `account-${Date.now()}`;

    console.log(`\n➕ 添加账号: ${name || accountId}`);

    // 捕获 session
    const sessionData = await captureSession(options);

    // 保存到账号目录
    if (!existsSync(this.accountsDir)) {
      const { mkdirSync } = await import('fs');
      mkdirSync(this.accountsDir, { recursive: true });
    }

    const sessionPath = `${this.accountsDir}/session-${accountId}.json`;
    writeFileSync(sessionPath, JSON.stringify(sessionData, null, 2), 'utf-8');

    // 添加到列表
    const account = {
      id: accountId,
      name: name || accountId,
      sessionPath,
      sessionData,
      enabled: true,
      weight: 1,
      requestCount: 0,
      lastUsed: null,
      status: 'active'
    };

    this.accounts.push(account);
    this.saveConfig();

    console.log(`✅ 账号已添加: ${account.name} (${account.id})`);
    return account;
  }

  /**
   * 删除账号
   */
  removeAccount(accountId) {
    const index = this.accounts.findIndex(a => a.id === accountId);
    if (index === -1) {
      throw new Error(`账号不存在: ${accountId}`);
    }

    const account = this.accounts[index];
    
    // 删除 session 文件
    const { unlinkSync } = await import('fs');
    if (existsSync(account.sessionPath)) {
      unlinkSync(account.sessionPath);
    }

    // 从列表移除
    this.accounts.splice(index, 1);
    this.saveConfig();

    console.log(`✅ 账号已删除: ${account.name}`);
  }

  /**
   * 启用/禁用账号
   */
  setAccountEnabled(accountId, enabled) {
    const account = this.accounts.find(a => a.id === accountId);
    if (!account) {
      throw new Error(`账号不存在: ${accountId}`);
    }

    account.enabled = enabled;
    this.saveConfig();

    console.log(`✅ 账号 ${account.name} 已${enabled ? '启用' : '禁用'}`);
  }

  /**
   * 设置账号权重
   */
  setAccountWeight(accountId, weight) {
    const account = this.accounts.find(a => a.id === accountId);
    if (!account) {
      throw new Error(`账号不存在: ${accountId}`);
    }

    account.weight = weight;
    this.saveConfig();

    console.log(`✅ 账号 ${account.name} 权重设置为 ${weight}`);
  }

  /**
   * 验证所有账号
   */
  async validateAllAccounts() {
    console.log('🔍 验证所有账号...\n');

    for (const account of this.accounts) {
      if (!account.enabled) {
        console.log(`⏭️  跳过禁用的账号: ${account.name}`);
        continue;
      }

      try {
        const isValid = await validateSessionInBrowser(account.sessionData);
        account.status = isValid ? 'active' : 'expired';
        
        if (isValid) {
          console.log(`✅ ${account.name}: 有效`);
        } else {
          console.log(`❌ ${account.name}: 已失效`);
        }
      } catch (error) {
        account.status = 'error';
        console.log(`❌ ${account.name}: 验证失败 - ${error.message}`);
      }
    }

    console.log('');
  }

  /**
   * 获取下一个可用账号（轮询策略）
   */
  getNextAccountRoundRobin() {
    const enabledAccounts = this.accounts.filter(a => a.enabled && a.status !== 'expired');
    
    if (enabledAccounts.length === 0) {
      throw new Error('没有可用的账号');
    }

    // 轮询
    const account = enabledAccounts[this.currentIndex % enabledAccounts.length];
    this.currentIndex++;

    return account;
  }

  /**
   * 获取下一个可用账号（加权轮询策略）
   */
  getNextAccountWeighted() {
    const enabledAccounts = this.accounts.filter(a => a.enabled && a.status !== 'expired');
    
    if (enabledAccounts.length === 0) {
      throw new Error('没有可用的账号');
    }

    // 计算总权重
    const totalWeight = enabledAccounts.reduce((sum, acc) => sum + acc.weight, 0);
    
    // 随机选择
    let random = Math.random() * totalWeight;
    for (const account of enabledAccounts) {
      random -= account.weight;
      if (random <= 0) {
        return account;
      }
    }

    return enabledAccounts[0];
  }

  /**
   * 获取下一个可用账号（最少使用策略）
   */
  getNextAccountLeastUsed() {
    const enabledAccounts = this.accounts.filter(a => a.enabled && a.status !== 'expired');
    
    if (enabledAccounts.length === 0) {
      throw new Error('没有可用的账号');
    }

    // 找到使用次数最少的
    return enabledAccounts.reduce((min, acc) => 
      acc.requestCount < min.requestCount ? acc : min
    );
  }

  /**
   * 获取下一个可用账号（最久未使用策略）
   */
  getNextAccountLeastRecent() {
    const enabledAccounts = this.accounts.filter(a => a.enabled && a.status !== 'expired');
    
    if (enabledAccounts.length === 0) {
      throw new Error('没有可用的账号');
    }

    // 找到最久未使用的
    return enabledAccounts.reduce((oldest, acc) => {
      if (!acc.lastUsed) return acc;
      if (!oldest.lastUsed) return oldest;
      return acc.lastUsed < oldest.lastUsed ? acc : oldest;
    });
  }

  /**
   * 获取下一个可用账号
   */
  getNextAccount() {
    switch (this.strategy) {
      case 'round-robin':
        return this.getNextAccountRoundRobin();
      case 'weighted':
        return this.getNextAccountWeighted();
      case 'least-used':
        return this.getNextAccountLeastUsed();
      case 'least-recent':
        return this.getNextAccountLeastRecent();
      default:
        return this.getNextAccountRoundRobin();
    }
  }

  /**
   * 使用账号（更新统计）
   */
  useAccount(account) {
    account.requestCount++;
    account.lastUsed = Date.now();
  }

  /**
   * 获取账号统计
   */
  getStats() {
    const total = this.accounts.length;
    const enabled = this.accounts.filter(a => a.enabled).length;
    const active = this.accounts.filter(a => a.status === 'active').length;
    const expired = this.accounts.filter(a => a.status === 'expired').length;
    const totalRequests = this.accounts.reduce((sum, a) => sum + a.requestCount, 0);

    return {
      total,
      enabled,
      active,
      expired,
      totalRequests,
      strategy: this.strategy,
      accounts: this.accounts.map(a => ({
        id: a.id,
        name: a.name,
        enabled: a.enabled,
        status: a.status,
        weight: a.weight,
        requestCount: a.requestCount,
        lastUsed: a.lastUsed ? new Date(a.lastUsed).toLocaleString() : 'Never'
      }))
    };
  }

  /**
   * 设置负载均衡策略
   */
  setStrategy(strategy) {
    const validStrategies = ['round-robin', 'weighted', 'least-used', 'least-recent'];
    if (!validStrategies.includes(strategy)) {
      throw new Error(`无效的策略: ${strategy}. 可用: ${validStrategies.join(', ')}`);
    }

    this.strategy = strategy;
    this.saveConfig();
    console.log(`✅ 负载均衡策略设置为: ${strategy}`);
  }

  /**
   * 列出所有账号
   */
  listAccounts() {
    if (this.accounts.length === 0) {
      console.log('📭 没有账号');
      return;
    }

    console.log(`\n📋 账号列表 (${this.accounts.length} 个):\n`);
    
    this.accounts.forEach((account, i) => {
      const status = account.enabled ? 
        (account.status === 'active' ? '✅' : 
         account.status === 'expired' ? '❌' : '❓') : '⏸️';
      
      console.log(`${i + 1}. ${status} ${account.name} (${account.id})`);
      console.log(`   状态: ${account.status}`);
      console.log(`   启用: ${account.enabled ? '是' : '否'}`);
      console.log(`   权重: ${account.weight}`);
      console.log(`   请求数: ${account.requestCount}`);
      console.log(`   最后使用: ${account.lastUsed ? new Date(account.lastUsed).toLocaleString() : '从未'}`);
      console.log('');
    });

    console.log(`负载均衡策略: ${this.strategy}`);
    console.log('');
  }
}

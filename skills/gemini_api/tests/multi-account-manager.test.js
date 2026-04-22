import { strict as assert } from 'assert';
import { readFileSync, writeFileSync, existsSync, mkdirSync, rmSync, readdirSync, unlinkSync } from 'fs';
import { tmpdir } from 'os';
import { join } from 'path';

const testDir = join(tmpdir(), 'multi-account-test-' + Date.now());
const dataDir = join(testDir, 'data');
const accountsDir = join(dataDir, 'accounts');
const configFile = join(dataDir, 'accounts-config.json');

function setupTestDir() {
  if (!existsSync(testDir)) {
    mkdirSync(testDir, { recursive: true });
  }
  if (!existsSync(dataDir)) {
    mkdirSync(dataDir, { recursive: true });
  }
  if (!existsSync(accountsDir)) {
    mkdirSync(accountsDir, { recursive: true });
  }
}

function cleanupTestDir() {
  if (existsSync(testDir)) {
    rmSync(testDir, { recursive: true, force: true });
  }
}

function createSessionData(accountId) {
  return {
    capturedAt: new Date().toISOString(),
    cookies: [{ name: `session-${accountId}`, value: `token-${accountId}` }],
    userAgent: `Agent-${accountId}`
  };
}

function createAccountSession(accountId) {
  const sessionPath = join(accountsDir, `session-${accountId}.json`);
  writeFileSync(sessionPath, JSON.stringify(createSessionData(accountId), null, 2), 'utf-8');
}

function createConfig(accounts, strategy = 'round-robin') {
  const config = {
    strategy,
    accounts: accounts.map(acc => ({
      id: acc.id,
      name: acc.name || acc.id,
      enabled: acc.enabled !== false,
      weight: acc.weight || 1
    }))
  };
  writeFileSync(configFile, JSON.stringify(config, null, 2), 'utf-8');
}

class TestableMultiAccountManager {
  constructor(accountsDirPath, configFilePath) {
    this.accounts = [];
    this.currentIndex = 0;
    this.accountsDir = accountsDirPath;
    this.configFile = configFilePath;
    this.strategy = 'round-robin';
    this._captureResult = null;
    this._validateResult = true;
    this.loadAccounts();
  }

  loadAccounts() {
    if (!existsSync(this.accountsDir)) {
      return;
    }

    try {
      let config = { accounts: [], strategy: 'round-robin' };
      if (existsSync(this.configFile)) {
        config = JSON.parse(readFileSync(this.configFile, 'utf-8'));
      }

      const files = readdirSync(this.accountsDir)
        .filter(f => f.endsWith('.json') && f.startsWith('session-'));

      this.accounts = files.map(file => {
        const accountId = file.replace('session-', '').replace('.json', '');
        const sessionPath = join(this.accountsDir, file);
        const sessionData = JSON.parse(readFileSync(sessionPath, 'utf-8'));
        
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
          status: 'unknown'
        };
      });

      this.strategy = config.strategy || 'round-robin';

    } catch (error) {
      console.error('❌ 加载账号失败:', error.message);
    }
  }

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

  async addAccount(options = {}) {
    const { name, id } = options;
    const accountId = id || `account-${Date.now()}`;

    const sessionData = this._captureResult || createSessionData(accountId);

    if (!existsSync(this.accountsDir)) {
      mkdirSync(this.accountsDir, { recursive: true });
    }

    const sessionPath = join(this.accountsDir, `session-${accountId}.json`);
    writeFileSync(sessionPath, JSON.stringify(sessionData, null, 2), 'utf-8');

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

    return account;
  }

  removeAccount(accountId) {
    const index = this.accounts.findIndex(a => a.id === accountId);
    if (index === -1) {
      throw new Error(`账号不存在: ${accountId}`);
    }

    const account = this.accounts[index];
    
    if (existsSync(account.sessionPath)) {
      unlinkSync(account.sessionPath);
    }

    this.accounts.splice(index, 1);
    this.saveConfig();
  }

  setAccountEnabled(accountId, enabled) {
    const account = this.accounts.find(a => a.id === accountId);
    if (!account) {
      throw new Error(`账号不存在: ${accountId}`);
    }

    account.enabled = enabled;
    this.saveConfig();
  }

  setAccountWeight(accountId, weight) {
    const account = this.accounts.find(a => a.id === accountId);
    if (!account) {
      throw new Error(`账号不存在: ${accountId}`);
    }

    account.weight = weight;
    this.saveConfig();
  }

  async validateAllAccounts() {
    for (const account of this.accounts) {
      if (!account.enabled) {
        continue;
      }

      try {
        account.status = this._validateResult ? 'active' : 'expired';
      } catch (error) {
        account.status = 'error';
      }
    }
  }

  getNextAccountRoundRobin() {
    const enabledAccounts = this.accounts.filter(a => a.enabled && a.status !== 'expired');
    
    if (enabledAccounts.length === 0) {
      throw new Error('没有可用的账号');
    }

    const account = enabledAccounts[this.currentIndex % enabledAccounts.length];
    this.currentIndex++;

    return account;
  }

  getNextAccountWeighted() {
    const enabledAccounts = this.accounts.filter(a => a.enabled && a.status !== 'expired');
    
    if (enabledAccounts.length === 0) {
      throw new Error('没有可用的账号');
    }

    const totalWeight = enabledAccounts.reduce((sum, acc) => sum + acc.weight, 0);
    
    let random = Math.random() * totalWeight;
    for (const account of enabledAccounts) {
      random -= account.weight;
      if (random <= 0) {
        return account;
      }
    }

    return enabledAccounts[0];
  }

  getNextAccountLeastUsed() {
    const enabledAccounts = this.accounts.filter(a => a.enabled && a.status !== 'expired');
    
    if (enabledAccounts.length === 0) {
      throw new Error('没有可用的账号');
    }

    return enabledAccounts.reduce((min, acc) => 
      acc.requestCount < min.requestCount ? acc : min
    );
  }

  getNextAccountLeastRecent() {
    const enabledAccounts = this.accounts.filter(a => a.enabled && a.status !== 'expired');
    
    if (enabledAccounts.length === 0) {
      throw new Error('没有可用的账号');
    }

    return enabledAccounts.reduce((oldest, acc) => {
      if (!acc.lastUsed) return acc;
      if (!oldest.lastUsed) return oldest;
      return acc.lastUsed < oldest.lastUsed ? acc : oldest;
    });
  }

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

  useAccount(account) {
    account.requestCount++;
    account.lastUsed = Date.now();
  }

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

  setStrategy(strategy) {
    const validStrategies = ['round-robin', 'weighted', 'least-used', 'least-recent'];
    if (!validStrategies.includes(strategy)) {
      throw new Error(`无效的策略: ${strategy}. 可用: ${validStrategies.join(', ')}`);
    }

    this.strategy = strategy;
    this.saveConfig();
  }
}

let testsPassed = 0;
let testsFailed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    testsPassed++;
  } catch (error) {
    console.log(`❌ ${name}`);
    console.log(`   Error: ${error.message}`);
    testsFailed++;
  }
}

async function testAsync(name, fn) {
  try {
    await fn();
    console.log(`✅ ${name}`);
    testsPassed++;
  } catch (error) {
    console.log(`❌ ${name}`);
    console.log(`   Error: ${error.message}`);
    testsFailed++;
  }
}

console.log('\n=== MultiAccountManager Unit Tests ===\n');
console.log(`Test directory: ${testDir}\n`);

setupTestDir();

test('constructor initializes with empty accounts when no accounts dir', () => {
  cleanupTestDir();
  mkdirSync(testDir, { recursive: true });
  mkdirSync(dataDir, { recursive: true });
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  
  assert.strictEqual(manager.accounts.length, 0);
  assert.strictEqual(manager.currentIndex, 0);
  assert.strictEqual(manager.strategy, 'round-robin');
});

test('loadAccounts loads all session files correctly', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('account1');
  createAccountSession('account2');
  createAccountSession('account3');
  createConfig([
    { id: 'account1', name: 'Account One', weight: 2 },
    { id: 'account2', name: 'Account Two' },
    { id: 'account3', name: 'Account Three', enabled: false }
  ]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  
  assert.strictEqual(manager.accounts.length, 3);
  assert.strictEqual(manager.accounts[0].id, 'account1');
  assert.strictEqual(manager.accounts[0].name, 'Account One');
  assert.strictEqual(manager.accounts[0].weight, 2);
  assert.strictEqual(manager.accounts[0].enabled, true);
  assert.strictEqual(manager.accounts[2].enabled, false);
});

test('loadAccounts loads strategy from config', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('test');
  createConfig([{ id: 'test' }], 'weighted');
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  
  assert.strictEqual(manager.strategy, 'weighted');
});

test('loadAccounts handles missing config file', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('test');
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  
  assert.strictEqual(manager.accounts.length, 1);
  assert.strictEqual(manager.strategy, 'round-robin');
});

test('loadAccounts handles corrupt JSON in config - catches error', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('test');
  writeFileSync(configFile, 'invalid json', 'utf-8');
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  
  assert.strictEqual(manager.accounts.length, 0);
});

test('loadAccounts ignores non-session JSON files', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('account1');
  createAccountSession('account2');
  writeFileSync(join(accountsDir, 'other-config.json'), JSON.stringify({ data: 'other' }), 'utf-8');
  writeFileSync(join(accountsDir, 'random.txt'), 'text', 'utf-8');
  createConfig([]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  
  assert.strictEqual(manager.accounts.length, 2);
  assert.ok(manager.accounts.every(a => a.id.startsWith('account')));
});

test('saveConfig writes correct structure', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('account1');
  createAccountSession('account2');
  createConfig([{ id: 'account1', weight: 2 }, { id: 'account2' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager.saveConfig();
  
  const savedConfig = JSON.parse(readFileSync(configFile, 'utf-8'));
  
  assert.strictEqual(savedConfig.strategy, 'round-robin');
  assert.strictEqual(savedConfig.accounts.length, 2);
  assert.strictEqual(savedConfig.accounts[0].id, 'account1');
  assert.strictEqual(savedConfig.accounts[0].weight, 2);
});

test('removeAccount throws error for non-existent account', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('test');
  createConfig([{ id: 'test' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  
  assert.throws(
    () => manager.removeAccount('non-existent'),
    { message: '账号不存在: non-existent' }
  );
});

test('removeAccount removes account from list', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('account1');
  createAccountSession('account2');
  createConfig([{ id: 'account1' }, { id: 'account2' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  const initialCount = manager.accounts.length;
  
  manager.removeAccount('account2');
  
  assert.strictEqual(manager.accounts.length, initialCount - 1);
  assert.strictEqual(manager.accounts.find(a => a.id === 'account2'), undefined);
});

test('removeAccount deletes session file', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('account1');
  createConfig([{ id: 'account1' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager.removeAccount('account1');
  
  assert.strictEqual(existsSync(join(accountsDir, 'session-account1.json')), false);
});

test('setAccountEnabled throws error for non-existent account', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('test');
  createConfig([{ id: 'test' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  
  assert.throws(
    () => manager.setAccountEnabled('non-existent', true),
    { message: '账号不存在: non-existent' }
  );
});

test('setAccountEnabled updates enabled status', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('test');
  createConfig([{ id: 'test' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager.setAccountEnabled('test', false);
  
  assert.strictEqual(manager.accounts[0].enabled, false);
});

test('setAccountWeight throws error for non-existent account', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('test');
  createConfig([{ id: 'test' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  
  assert.throws(
    () => manager.setAccountWeight('non-existent', 5),
    { message: '账号不存在: non-existent' }
  );
});

test('setAccountWeight updates weight', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('test');
  createConfig([{ id: 'test' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager.setAccountWeight('test', 10);
  
  assert.strictEqual(manager.accounts[0].weight, 10);
});

await testAsync('addAccount creates new account with default id', async () => {
  cleanupTestDir();
  setupTestDir();
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  const account = await manager.addAccount({ name: 'New Account' });
  
  assert.ok(account.id.startsWith('account-'));
  assert.strictEqual(account.name, 'New Account');
  assert.strictEqual(account.enabled, true);
  assert.strictEqual(account.status, 'active');
});

await testAsync('addAccount creates account with custom id', async () => {
  cleanupTestDir();
  setupTestDir();
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  const account = await manager.addAccount({ id: 'custom-id', name: 'Custom' });
  
  assert.strictEqual(account.id, 'custom-id');
  assert.strictEqual(account.name, 'Custom');
});

await testAsync('addAccount creates accounts directory if not exists', async () => {
  cleanupTestDir();
  mkdirSync(testDir, { recursive: true });
  mkdirSync(dataDir, { recursive: true });
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  await manager.addAccount({ id: 'test-id' });
  
  assert.strictEqual(existsSync(accountsDir), true);
});

await testAsync('addAccount uses captureResult', async () => {
  cleanupTestDir();
  setupTestDir();
  
  const customSession = createSessionData('custom');
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager._captureResult = customSession;
  
  const account = await manager.addAccount({ id: 'custom' });
  
  assert.deepStrictEqual(account.sessionData, customSession);
});

await testAsync('validateAllAccounts marks valid accounts as active', async () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('account1');
  createAccountSession('account2');
  createConfig([{ id: 'account1' }, { id: 'account2' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager._validateResult = true;
  await manager.validateAllAccounts();
  
  assert.strictEqual(manager.accounts[0].status, 'active');
  assert.strictEqual(manager.accounts[1].status, 'active');
});

await testAsync('validateAllAccounts marks invalid accounts as expired', async () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('account1');
  createAccountSession('account2');
  createConfig([{ id: 'account1' }, { id: 'account2' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager._validateResult = false;
  await manager.validateAllAccounts();
  
  assert.strictEqual(manager.accounts[0].status, 'expired');
  assert.strictEqual(manager.accounts[1].status, 'expired');
});

await testAsync('validateAllAccounts skips disabled accounts', async () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('account1');
  createAccountSession('account2');
  createConfig([{ id: 'account1' }, { id: 'account2', enabled: false }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager._validateResult = true;
  await manager.validateAllAccounts();
  
  assert.strictEqual(manager.accounts[0].status, 'active');
  assert.strictEqual(manager.accounts[1].status, 'unknown');
});

console.log('\n=== Load Balancing Strategy Tests ===\n');

test('getNextAccountRoundRobin throws when no enabled accounts', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('test');
  createConfig([{ id: 'test', enabled: false }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager.accounts[0].status = 'active';
  
  assert.throws(
    () => manager.getNextAccountRoundRobin(),
    { message: '没有可用的账号' }
  );
});

test('getNextAccountRoundRobin cycles through accounts', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('account1');
  createAccountSession('account2');
  createAccountSession('account3');
  createConfig([{ id: 'account1' }, { id: 'account2' }, { id: 'account3' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager.accounts.forEach(a => a.status = 'active');
  
  const first = manager.getNextAccountRoundRobin();
  const second = manager.getNextAccountRoundRobin();
  const third = manager.getNextAccountRoundRobin();
  const fourth = manager.getNextAccountRoundRobin();
  
  assert.strictEqual(first.id, 'account1');
  assert.strictEqual(second.id, 'account2');
  assert.strictEqual(third.id, 'account3');
  assert.strictEqual(fourth.id, 'account1');
});

test('getNextAccountRoundRobin skips expired accounts', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('account1');
  createAccountSession('account2');
  createAccountSession('account3');
  createConfig([{ id: 'account1' }, { id: 'account2' }, { id: 'account3' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager.accounts[0].status = 'expired';
  manager.accounts[1].status = 'active';
  manager.accounts[2].status = 'active';
  
  const account = manager.getNextAccountRoundRobin();
  
  assert.ok(account.id !== 'account1');
});

test('getNextAccountRoundRobin skips disabled accounts', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('account1');
  createAccountSession('account2');
  createAccountSession('account3');
  createConfig([{ id: 'account1' }, { id: 'account2' }, { id: 'account3' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager.accounts[0].enabled = false;
  manager.accounts[0].status = 'active';
  manager.accounts[1].enabled = true;
  manager.accounts[1].status = 'active';
  manager.accounts[2].enabled = true;
  manager.accounts[2].status = 'active';
  
  const account = manager.getNextAccountRoundRobin();
  
  assert.strictEqual(account.id, 'account2');
});

test('getNextAccountWeighted throws when no enabled accounts', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('test');
  createConfig([{ id: 'test', enabled: false }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  
  assert.throws(
    () => manager.getNextAccountWeighted(),
    { message: '没有可用的账号' }
  );
});

test('getNextAccountWeighted returns valid account', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('account1');
  createAccountSession('account2');
  createConfig([{ id: 'account1' }, { id: 'account2' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager.accounts.forEach(a => a.status = 'active');
  
  for (let i = 0; i < 10; i++) {
    const account = manager.getNextAccountWeighted();
    assert.ok(account.enabled);
    assert.notStrictEqual(account.status, 'expired');
  }
});

test('getNextAccountLeastUsed throws when no enabled accounts', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('test');
  createConfig([{ id: 'test', enabled: false }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  
  assert.throws(
    () => manager.getNextAccountLeastUsed(),
    { message: '没有可用的账号' }
  );
});

test('getNextAccountLeastUsed returns account with lowest request count', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('account1');
  createAccountSession('account2');
  createAccountSession('account3');
  createConfig([{ id: 'account1' }, { id: 'account2' }, { id: 'account3' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager.accounts.forEach(a => a.status = 'active');
  manager.accounts[0].requestCount = 10;
  manager.accounts[1].requestCount = 2;
  manager.accounts[2].requestCount = 5;
  
  const account = manager.getNextAccountLeastUsed();
  
  assert.strictEqual(account.id, 'account2');
});

test('getNextAccountLeastUsed handles equal request counts', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('account1');
  createAccountSession('account2');
  createConfig([{ id: 'account1' }, { id: 'account2' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager.accounts.forEach(a => {
    a.status = 'active';
    a.requestCount = 5;
  });
  
  const account = manager.getNextAccountLeastUsed();
  
  assert.ok(account.enabled);
});

test('getNextAccountLeastRecent throws when no enabled accounts', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('test');
  createConfig([{ id: 'test', enabled: false }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  
  assert.throws(
    () => manager.getNextAccountLeastRecent(),
    { message: '没有可用的账号' }
  );
});

test('getNextAccountLeastRecent returns account with oldest lastUsed', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('account1');
  createAccountSession('account2');
  createAccountSession('account3');
  createConfig([{ id: 'account1' }, { id: 'account2' }, { id: 'account3' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager.accounts.forEach(a => a.status = 'active');
  manager.accounts[0].lastUsed = Date.now() - 3600000;
  manager.accounts[1].lastUsed = Date.now() - 7200000;
  manager.accounts[2].lastUsed = Date.now() - 1800000;
  
  const account = manager.getNextAccountLeastRecent();
  
  assert.strictEqual(account.id, 'account2');
});

test('getNextAccountLeastRecent handles null lastUsed', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('account1');
  createAccountSession('account2');
  createAccountSession('account3');
  createConfig([{ id: 'account1' }, { id: 'account2' }, { id: 'account3' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager.accounts.forEach(a => a.status = 'active');
  manager.accounts[0].lastUsed = Date.now();
  manager.accounts[1].lastUsed = null;
  manager.accounts[2].lastUsed = Date.now();
  
  const account = manager.getNextAccountLeastRecent();
  
  assert.strictEqual(account.id, 'account2');
});

test('getNextAccount uses correct strategy', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('account1');
  createAccountSession('account2');
  createAccountSession('account3');
  createConfig([{ id: 'account1' }, { id: 'account2' }, { id: 'account3' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager.accounts.forEach(a => a.status = 'active');
  
  manager.strategy = 'round-robin';
  const rr = manager.getNextAccount();
  assert.strictEqual(rr.id, 'account1');
  
  manager.strategy = 'least-used';
  manager.accounts[1].requestCount = 0;
  manager.accounts[0].requestCount = 5;
  manager.accounts[2].requestCount = 10;
  const lu = manager.getNextAccount();
  assert.strictEqual(lu.id, 'account2');
  
  manager.strategy = 'unknown-strategy';
  const def = manager.getNextAccount();
  assert.ok(def.enabled);
});

console.log('\n=== useAccount and Stats Tests ===\n');

test('useAccount updates requestCount and lastUsed', () => {
  const account = {
    id: 'test',
    requestCount: 0,
    lastUsed: null
  };
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  const beforeTime = Date.now();
  manager.useAccount(account);
  const afterTime = Date.now();
  
  assert.strictEqual(account.requestCount, 1);
  assert.ok(account.lastUsed >= beforeTime && account.lastUsed <= afterTime);
});

test('useAccount increments requestCount multiple times', () => {
  const account = {
    id: 'test',
    requestCount: 0,
    lastUsed: null
  };
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager.useAccount(account);
  manager.useAccount(account);
  manager.useAccount(account);
  
  assert.strictEqual(account.requestCount, 3);
});

test('getStats returns correct statistics', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('account1');
  createAccountSession('account2');
  createAccountSession('account3');
  createConfig([{ id: 'account1' }, { id: 'account2' }, { id: 'account3' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  manager.accounts[0].status = 'active';
  manager.accounts[0].requestCount = 10;
  manager.accounts[1].status = 'expired';
  manager.accounts[1].requestCount = 5;
  manager.accounts[2].status = 'active';
  manager.accounts[2].requestCount = 3;
  
  const stats = manager.getStats();
  
  assert.strictEqual(stats.total, 3);
  assert.strictEqual(stats.enabled, 3);
  assert.strictEqual(stats.active, 2);
  assert.strictEqual(stats.expired, 1);
  assert.strictEqual(stats.totalRequests, 18);
  assert.strictEqual(stats.strategy, 'round-robin');
  assert.strictEqual(stats.accounts.length, 3);
});

test('setStrategy throws for invalid strategy', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('test');
  createConfig([{ id: 'test' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  
  assert.throws(
    () => manager.setStrategy('invalid'),
    /无效的策略/
  );
});

test('setStrategy accepts valid strategies', () => {
  cleanupTestDir();
  setupTestDir();
  
  createAccountSession('test');
  createConfig([{ id: 'test' }]);
  
  const manager = new TestableMultiAccountManager(accountsDir, configFile);
  
  manager.setStrategy('round-robin');
  assert.strictEqual(manager.strategy, 'round-robin');
  
  manager.setStrategy('weighted');
  assert.strictEqual(manager.strategy, 'weighted');
  
  manager.setStrategy('least-used');
  assert.strictEqual(manager.strategy, 'least-used');
  
  manager.setStrategy('least-recent');
  assert.strictEqual(manager.strategy, 'least-recent');
});

cleanupTestDir();

console.log('\n=== Test Summary ===');
console.log(`Passed: ${testsPassed}`);
console.log(`Failed: ${testsFailed}`);
console.log(`Total: ${testsPassed + testsFailed}`);

if (testsFailed > 0) {
  process.exit(1);
}
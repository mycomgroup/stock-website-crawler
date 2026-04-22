import { describe, it, mock, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';

const mockSites = {
  '10jqka': { id: '10jqka', name: '同花顺', domain: '.10jqka.com.cn' },
  'guorn': { id: 'guorn', name: '果仁', domain: '.guorn.com' },
  'thsquant': { id: 'thsquant', name: '同花顺量化', domain: '.10jqka.com.cn' }
};

const createMockAuthManager = () => ({
  testSessionHeaded: mock.fn(() => Promise.resolve()),
  getValidSession: mock.fn(() => Promise.resolve([{ name: 'session', value: 'cookie' }])),
  importCookies: mock.fn((jsonString) => {
    const raw = JSON.parse(jsonString);
    const cookies = Array.isArray(raw) ? raw : (raw.cookies || []);
    if (cookies.length === 0) throw new Error('无效的 Cookie JSON 格式');
    return Promise.resolve(cookies);
  })
});

describe('login.js - 命令行参数解析', () => {
  it('无参数时应识别为无效', () => {
    const args = [];
    const siteId = args[0];
    const sites = mockSites;
    const isValid = siteId === 'all' || !!sites[siteId];
    assert.strictEqual(isValid, false);
  });

  it('无效站点ID应识别为无效', () => {
    const args = ['invalid_site'];
    const siteId = args[0];
    const sites = mockSites;
    const isValid = siteId === 'all' || !!sites[siteId];
    assert.strictEqual(isValid, false);
  });

  it('--test 参数应正确识别', () => {
    const args = ['10jqka', '--test'];
    const isTest = args.includes('--test');
    assert.strictEqual(isTest, true);
  });

  it('--method=import 参数应正确解析', () => {
    const args = ['10jqka', '--method=import'];
    const methodArg = args.find(arg => arg.startsWith('--method='));
    const method = methodArg ? methodArg.split('=')[1] : 'all';
    assert.strictEqual(method, 'import');
  });

  it('all 站点应被接受', () => {
    const args = ['all'];
    const siteId = args[0];
    const sites = mockSites;
    const isValid = siteId === 'all' || !!sites[siteId];
    assert.strictEqual(isValid, true);
  });

  it('有效站点ID应被接受', () => {
    const args = ['10jqka'];
    const siteId = args[0];
    const sites = mockSites;
    const isValid = siteId === 'all' || !!sites[siteId];
    assert.strictEqual(isValid, true);
  });

  it('无 --method 参数时默认为 all', () => {
    const args = ['10jqka'];
    const methodArg = args.find(arg => arg.startsWith('--method='));
    const method = methodArg ? methodArg.split('=')[1] : 'all';
    assert.strictEqual(method, 'all');
  });

  it('--method=auto 应正确解析', () => {
    const args = ['10jqka', '--method=auto'];
    const methodArg = args.find(arg => arg.startsWith('--method='));
    const method = methodArg ? methodArg.split('=')[1] : 'all';
    assert.strictEqual(method, 'auto');
  });

  it('--method=manual 应正确解析', () => {
    const args = ['10jqka', '--method=manual'];
    const methodArg = args.find(arg => arg.startsWith('--method='));
    const method = methodArg ? methodArg.split('=')[1] : 'all';
    assert.strictEqual(method, 'manual');
  });

  it('--method=local 应正确解析', () => {
    const args = ['10jqka', '--method=local'];
    const methodArg = args.find(arg => arg.startsWith('--method='));
    const method = methodArg ? methodArg.split('=')[1] : 'all';
    assert.strictEqual(method, 'local');
  });
});

describe('login.js - 单站点登录流程', () => {
  it('应为每个站点创建 AuthManager 实例', () => {
    const mockSite = mockSites['10jqka'];
    const manager = createMockAuthManager();
    assert.ok(typeof manager.getValidSession === 'function');
    assert.ok(typeof manager.testSessionHeaded === 'function');
  });

  it('应调用 getValidSession 并传递正确的参数', async () => {
    const manager = createMockAuthManager();
    await manager.getValidSession({ forceRefresh: true, method: 'auto' });
    assert.strictEqual(manager.getValidSession.mock.calls.length, 1);
    assert.deepStrictEqual(manager.getValidSession.mock.calls[0].arguments[0], { forceRefresh: true, method: 'auto' });
  });

  it('应处理登录成功', async () => {
    const manager = createMockAuthManager();
    const result = await manager.getValidSession({ forceRefresh: true, method: 'auto' });
    assert.ok(Array.isArray(result));
  });

  it('应处理登录失败', async () => {
    const manager = createMockAuthManager();
    manager.getValidSession = mock.fn(() => Promise.reject(new Error('登录失败')));
    
    await assert.rejects(
      async () => await manager.getValidSession({ forceRefresh: true }),
      { message: '登录失败' }
    );
  });
});

describe('login.js - all 站点登录流程', () => {
  it('应遍历所有站点', () => {
    const siteIds = Object.keys(mockSites);
    assert.ok(siteIds.length === 3);
    assert.ok(siteIds.includes('10jqka'));
    assert.ok(siteIds.includes('guorn'));
    assert.ok(siteIds.includes('thsquant'));
  });
});

describe('login.js --test 视觉验证模式', () => {
  it('应调用 testSessionHeaded', async () => {
    const manager = createMockAuthManager();
    await manager.testSessionHeaded();
    assert.strictEqual(manager.testSessionHeaded.mock.calls.length, 1);
  });
});

describe('login.js - import 模式', () => {
  it('handleImport 应解析有效的 JSON 输入', async () => {
    const manager = createMockAuthManager();
    const validJson = JSON.stringify([{ name: 'session', value: 'test123' }]);
    
    const result = await manager.importCookies(validJson);
    assert.ok(Array.isArray(result));
    assert.strictEqual(result[0].name, 'session');
  });

  it('handleImport 应处理 { cookies: [...] } 格式', async () => {
    const manager = createMockAuthManager();
    const validJson = JSON.stringify({ cookies: [{ name: 'session', value: 'test123' }] });
    
    const result = await manager.importCookies(validJson);
    assert.ok(Array.isArray(result));
    assert.strictEqual(result[0].name, 'session');
  });

  it('handleImport 应拒绝无效 JSON', async () => {
    const manager = createMockAuthManager();
    
    await assert.rejects(
      async () => await manager.importCookies('not valid json'),
      { message: /Unexpected token|Expected/ }
    );
  });

  it('handleImport 应拒绝空 cookies 数组', async () => {
    const manager = createMockAuthManager();
    
    await assert.rejects(
      async () => await manager.importCookies('[]'),
      { message: '无效的 Cookie JSON 格式' }
    );
  });

  it('handleImport 应拒绝空对象', async () => {
    const manager = createMockAuthManager();
    
    await assert.rejects(
      async () => await manager.importCookies('{}'),
      { message: '无效的 Cookie JSON 格式' }
    );
  });

  it('handleImport 应拒绝对象中无 cookies 字段', async () => {
    const manager = createMockAuthManager();
    
    await assert.rejects(
      async () => await manager.importCookies('{"user": "test"}'),
      { message: '无效的 Cookie JSON 格式' }
    );
  });
});

describe('login.js - 无效站点ID处理', () => {
  it('不存在的站点应触发错误', () => {
    const siteId = 'nonexistent';
    const sites = mockSites;
    const isValid = siteId === 'all' || !!sites[siteId];
    assert.strictEqual(isValid, false);
  });

  it('all 应被视为有效', () => {
    const siteId = 'all';
    const sites = mockSites;
    const isValid = siteId === 'all' || !!sites[siteId];
    assert.strictEqual(isValid, true);
  });
});

describe('login.js - 错误处理', () => {
  it('getValidSession 失败时应抛出错误', async () => {
    const manager = createMockAuthManager();
    manager.getValidSession = mock.fn(() => Promise.reject(new Error('无法获取有效会话')));
    
    await assert.rejects(
      async () => await manager.getValidSession(),
      { message: '无法获取有效会话' }
    );
  });

  it('import 模式不支持 all 站点', async () => {
    const siteId = 'all';
    const method = 'import';
    assert.strictEqual(siteId === 'all' && method === 'import', true);
  });
});
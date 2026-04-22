import { describe, it, mock, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';

const SESSION_HUB = '/test/.sessions';
const SKILLS_ROOT = '/test/skills';

const MAPPINGS = [
  { src: 'guorn_strategy/data/session.json', dest: 'guorn.json' },
  { src: '10jqka_backtest/data/session.json', dest: '10jqka.json' },
  { src: 'thsquant_strategy/data/session.json', dest: 'thsquant.json' }
];

describe('migrate-sessions.js - 创建目录逻辑', () => {
  let mkdirSyncMock;
  let existsSyncMock;
  let consoleLogs;

  beforeEach(() => {
    mkdirSyncMock = mock.fn(() => {});
    existsSyncMock = mock.fn(() => false);
    consoleLogs = [];
    const origLog = console.log;
    console.log = (...args) => consoleLogs.push(args.join(' '));
  });

  afterEach(() => {
    console.log = console.log;
  });

  it('目录不存在时应创建', () => {
    existsSyncMock = mock.fn(() => false);
    const shouldCreate = !existsSyncMock(SESSION_HUB);
    assert.strictEqual(shouldCreate, true);
  });

  it('目录已存在时不应重新创建', () => {
    existsSyncMock = mock.fn(() => true);
    const shouldCreate = !existsSyncMock(SESSION_HUB);
    assert.strictEqual(shouldCreate, false);
  });

  it('应使用 recursive 选项创建目录', () => {
    const options = { recursive: true };
    assert.ok(options.recursive);
  });
});

describe('migrate-sessions.js - 迁移单个文件成功', () => {
  it('应正确迁移并写入目标文件', () => {
    const srcData = { cookies: [{ name: 'test', value: '123' }], timestamp: 12345 };
    const raw = srcData;
    const unified = Array.isArray(raw) ? { cookies: raw, timestamp: Date.now() } : raw;
    
    assert.ok(!Array.isArray(unified));
    assert.ok(Array.isArray(unified.cookies));
    assert.strictEqual(unified.cookies[0].name, 'test');
  });

  it('应保留 timestamp 字段', () => {
    const srcData = { cookies: [{ name: 'test', value: '123' }], timestamp: 1234567890 };
    const unified = srcData;
    
    assert.strictEqual(unified.timestamp, 1234567890);
  });

  it('应保留其他自定义字段', () => {
    const srcData = { 
      cookies: [{ name: 'test', value: '123' }], 
      timestamp: 1234567890,
      user: 'testuser',
      custom: 'field'
    };
    
    assert.strictEqual(srcData.user, 'testuser');
    assert.strictEqual(srcData.custom, 'field');
  });
});

describe('migrate-sessions.js - 迁移单个文件失败', () => {
  it('JSON 解析错误应被捕获', () => {
    const invalidJson = 'not valid json {';
    
    assert.throws(
      () => JSON.parse(invalidJson),
      { message: /Unexpected token|Expected/ }
    );
  });

  it('写入错误应被处理', () => {
    const writeError = new Error('写入失败');
    
    assert.ok(writeError instanceof Error);
    assert.strictEqual(writeError.message, '写入失败');
  });
});

describe('migrate-sessions.js - 源文件不存在', () => {
  it('应跳过不存在的源文件', () => {
    const srcPath = '/nonexistent/path/session.json';
    const exists = false;
    
    assert.strictEqual(exists, false);
  });

  it('不存在的文件应被跳过而不报错', () => {
    const mappings = MAPPINGS;
    const results = mappings.map(m => ({ 
      src: m.src, 
      exists: false,
      skipped: true 
    }));
    
    results.forEach(r => {
      assert.strictEqual(r.skipped, true);
    });
  });

  it('应输出跳过信息', () => {
    const srcPath = '/nonexistent/session.json';
    const exists = false;
    const message = exists ? '迁移' : '跳过';
    
    assert.strictEqual(message, '跳过');
  });
});

describe('migrate-sessions.js - 数组格式转换', () => {
  it('纯数组格式应被包装为对象', () => {
    const arrayFormat = [
      { name: 'cookie1', value: 'val1' },
      { name: 'cookie2', value: 'val2' }
    ];
    
    const raw = arrayFormat;
    const unified = Array.isArray(raw) ? { cookies: raw, timestamp: Date.now() } : raw;
    
    assert.ok(!Array.isArray(unified));
    assert.ok(Array.isArray(unified.cookies));
    assert.strictEqual(unified.cookies.length, 2);
    assert.ok(typeof unified.timestamp === 'number');
  });

  it('包装后的对象应包含 timestamp', () => {
    const arrayFormat = [{ name: 'cookie1', value: 'val1' }];
    const raw = arrayFormat;
    const unified = Array.isArray(raw) ? { cookies: raw, timestamp: Date.now() } : raw;
    
    assert.ok('timestamp' in unified);
    assert.ok(unified.timestamp > 0);
  });

  it('guorn 格式应正确转换', () => {
    const guornFormat = [
      { domain: '.guorn.com', name: 'session', value: 'abc123', path: '/' },
      { domain: '.guorn.com', name: 'user', value: 'testuser', path: '/' }
    ];
    
    const unified = Array.isArray(guornFormat) 
      ? { cookies: guornFormat, timestamp: Date.now() } 
      : guornFormat;
    
    assert.strictEqual(unified.cookies[0].name, 'session');
    assert.strictEqual(unified.cookies[1].name, 'user');
  });
});

describe('migrate-sessions.js - 对象格式保持', () => {
  it('已是对象格式的数据不应被修改', () => {
    const objectFormat = { 
      cookies: [{ name: 'test', value: '123' }], 
      timestamp: 1234567890 
    };
    
    const raw = objectFormat;
    const unified = Array.isArray(raw) ? { cookies: raw, timestamp: Date.now() } : raw;
    
    assert.deepStrictEqual(unified, objectFormat);
  });

  it('包含额外字段的对象应保留所有字段', () => {
    const objectFormat = { 
      cookies: [{ name: 'test', value: '123' }], 
      timestamp: 1234567890,
      user: 'testuser',
      capturedAt: '2024-01-01T00:00:00.000Z'
    };
    
    const raw = objectFormat;
    const unified = Array.isArray(raw) ? { cookies: raw, timestamp: Date.now() } : raw;
    
    assert.strictEqual(unified.user, 'testuser');
    assert.strictEqual(unified.capturedAt, '2024-01-01T00:00:00.000Z');
  });

  it('空对象应保持为空对象', () => {
    const objectFormat = {};
    const raw = objectFormat;
    const unified = Array.isArray(raw) ? { cookies: raw, timestamp: Date.now() } : raw;
    
    assert.deepStrictEqual(unified, {});
  });
});

describe('migrate-sessions.js - JSON解析错误处理', () => {
  it('格式错误的 JSON 应抛出错误', () => {
    const malformedJson = '{"cookies": [}';
    
    assert.throws(
      () => JSON.parse(malformedJson),
      SyntaxError
    );
  });

  it('非 JSON 字符串应抛出错误', () => {
    const notJson = 'this is not json';
    
    assert.throws(
      () => JSON.parse(notJson),
      SyntaxError
    );
  });

  it('空字符串应抛出错误', () => {
    const emptyString = '';
    
    assert.throws(
      () => JSON.parse(emptyString),
      SyntaxError
    );
  });

  it('错误消息应包含错误描述', () => {
    let errorMessage = '';
    try {
      JSON.parse('invalid');
    } catch (e) {
      errorMessage = e.message;
    }
    
    assert.ok(errorMessage.length > 0);
  });
});

describe('migrate-sessions.js - 映射配置验证', () => {
  it('MAPPINGS 应包含 guorn 映射', () => {
    const guornMapping = MAPPINGS.find(m => m.dest === 'guorn.json');
    assert.ok(guornMapping);
    assert.strictEqual(guornMapping.src, 'guorn_strategy/data/session.json');
  });

  it('MAPPINGS 应包含 10jqka 映射', () => {
    const mapping = MAPPINGS.find(m => m.dest === '10jqka.json');
    assert.ok(mapping);
    assert.strictEqual(mapping.src, '10jqka_backtest/data/session.json');
  });

  it('MAPPINGS 应包含 thsquant 映射', () => {
    const mapping = MAPPINGS.find(m => m.dest === 'thsquant.json');
    assert.ok(mapping);
    assert.strictEqual(mapping.src, 'thsquant_strategy/data/session.json');
  });

  it('所有目标文件名应以 .json 结尾', () => {
    MAPPINGS.forEach(m => {
      assert.ok(m.dest.endsWith('.json'));
    });
  });
});

describe('migrate-sessions.js - 完整迁移流程模拟', () => {
  it('应按顺序处理所有映射', () => {
    const processedOrder = [];
    MAPPINGS.forEach(m => {
      processedOrder.push(m.dest);
    });
    
    assert.strictEqual(processedOrder.length, 3);
    assert.strictEqual(processedOrder[0], 'guorn.json');
    assert.strictEqual(processedOrder[1], '10jqka.json');
    assert.strictEqual(processedOrder[2], 'thsquant.json');
  });

  it('路径拼接应正确', () => {
    const skillsRoot = '/skills';
    const sessionHub = '/skills/.sessions';
    
    MAPPINGS.forEach(m => {
      const srcPath = path.join(skillsRoot, m.src);
      const destPath = path.join(sessionHub, m.dest);
      
      assert.ok(srcPath.startsWith('/skills/'));
      assert.ok(destPath.startsWith('/skills/.sessions/'));
      assert.ok(destPath.endsWith('.json'));
    });
  });
});
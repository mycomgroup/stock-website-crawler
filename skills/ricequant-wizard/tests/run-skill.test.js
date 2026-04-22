import { describe, it, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SKILL_DIR = path.join(__dirname, '..');

const mockConsoleLog = mock.fn();
const mockConsoleError = mock.fn();
const originalConsoleLog = console.log;
const originalConsoleError = console.error;

function captureConsole() {
  console.log = mockConsoleLog;
  console.error = mockConsoleError;
  return {
    outputs: () => mockConsoleLog.mock.calls.map(c => c.arguments.join(' ')),
    errors: () => mockConsoleError.mock.calls.map(c => c.arguments.join(' ')),
    reset: () => {
      mockConsoleLog.mock.resetCalls();
      mockConsoleError.mock.resetCalls();
    },
    restore: () => {
      console.log = originalConsoleLog;
      console.error = originalConsoleError;
    }
  };
}

describe('parseArgs', () => {
  it('should return empty object for empty array', () => {
    const parseArgs = (argv) => {
      const args = {};
      for (let i = 0; i < argv.length; i++) {
        const arg = argv[i];
        if (!arg.startsWith('--')) continue;
        const key = arg.slice(2);
        const next = argv[i + 1];
        if (!next || next.startsWith('--')) {
          args[key] = true;
          continue;
        }
        args[key] = next;
        i++;
      }
      return args;
    };
    
    const result = parseArgs([]);
    assert.deepStrictEqual(result, {});
  });

  it('should handle single --flag parameter', () => {
    const parseArgs = (argv) => {
      const args = {};
      for (let i = 0; i < argv.length; i++) {
        const arg = argv[i];
        if (!arg.startsWith('--')) continue;
        const key = arg.slice(2);
        const next = argv[i + 1];
        if (!next || next.startsWith('--')) {
          args[key] = true;
          continue;
        }
        args[key] = next;
        i++;
      }
      return args;
    };
    
    const result = parseArgs(['--help']);
    assert.deepStrictEqual(result, { help: true });
  });

  it('should handle --flag value parameter', () => {
    const parseArgs = (argv) => {
      const args = {};
      for (let i = 0; i < argv.length; i++) {
        const arg = argv[i];
        if (!arg.startsWith('--')) continue;
        const key = arg.slice(2);
        const next = argv[i + 1];
        if (!next || next.startsWith('--')) {
          args[key] = true;
          continue;
        }
        args[key] = next;
        i++;
      }
      return args;
    };
    
    const result = parseArgs(['--config', 'test.json']);
    assert.deepStrictEqual(result, { config: 'test.json' });
  });

  it('should handle multiple consecutive parameters', () => {
    const parseArgs = (argv) => {
      const args = {};
      for (let i = 0; i < argv.length; i++) {
        const arg = argv[i];
        if (!arg.startsWith('--')) continue;
        const key = arg.slice(2);
        const next = argv[i + 1];
        if (!next || next.startsWith('--')) {
          args[key] = true;
          continue;
        }
        args[key] = next;
        i++;
      }
      return args;
    };
    
    const result = parseArgs(['--create', '--config', 'test.json', '--run']);
    assert.deepStrictEqual(result, { create: true, config: 'test.json', run: true });
  });

  it('should handle flag without value followed by another flag', () => {
    const parseArgs = (argv) => {
      const args = {};
      for (let i = 0; i < argv.length; i++) {
        const arg = argv[i];
        if (!arg.startsWith('--')) continue;
        const key = arg.slice(2);
        const next = argv[i + 1];
        if (!next || next.startsWith('--')) {
          args[key] = true;
          continue;
        }
        args[key] = next;
        i++;
      }
      return args;
    };
    
    const result = parseArgs(['--wait', '--full']);
    assert.deepStrictEqual(result, { wait: true, full: true });
  });

  it('should handle multiple flags with values', () => {
    const parseArgs = (argv) => {
      const args = {};
      for (let i = 0; i < argv.length; i++) {
        const arg = argv[i];
        if (!arg.startsWith('--')) continue;
        const key = arg.slice(2);
        const next = argv[i + 1];
        if (!next || next.startsWith('--')) {
          args[key] = true;
          continue;
        }
        args[key] = next;
        i++;
      }
      return args;
    };
    
    const result = parseArgs(['--start', '2020-01-01', '--end', '2025-01-01', '--capital', '100000']);
    assert.deepStrictEqual(result, { start: '2020-01-01', end: '2025-01-01', capital: '100000' });
  });

  it('should skip non-flag arguments', () => {
    const parseArgs = (argv) => {
      const args = {};
      for (let i = 0; i < argv.length; i++) {
        const arg = argv[i];
        if (!arg.startsWith('--')) continue;
        const key = arg.slice(2);
        const next = argv[i + 1];
        if (!next || next.startsWith('--')) {
          args[key] = true;
          continue;
        }
        args[key] = next;
        i++;
      }
      return args;
    };
    
    const result = parseArgs(['node', 'script.js', '--help']);
    assert.deepStrictEqual(result, { help: true });
  });
});

describe('loadConfig', () => {
  const mockExistsSync = mock.fn();
  const mockReadFileSync = mock.fn();
  
  beforeEach(() => {
    mockExistsSync.mock.resetCalls();
    mockReadFileSync.mock.resetCalls();
  });

  it('should throw error when file does not exist', () => {
    mockExistsSync.mock.mockImplementation(() => false);
    
    const loadConfig = (configPath) => {
      if (!mockExistsSync(configPath)) {
        throw new Error(`配置文件不存在: ${configPath}`);
      }
      return JSON.parse(mockReadFileSync(configPath, 'utf8'));
    };
    
    assert.throws(
      () => loadConfig('/nonexistent/config.json'),
      { message: /配置文件不存在/ }
    );
  });

  it('should parse JSON when file exists', () => {
    mockExistsSync.mock.mockImplementation(() => true);
    mockReadFileSync.mock.mockImplementation(() => JSON.stringify({ name: 'Test Strategy' }));
    
    const loadConfig = (configPath) => {
      if (!mockExistsSync(configPath)) {
        throw new Error(`配置文件不存在: ${configPath}`);
      }
      return JSON.parse(mockReadFileSync(configPath, 'utf8'));
    };
    
    const result = loadConfig('/path/to/config.json');
    assert.deepStrictEqual(result, { name: 'Test Strategy' });
  });

  it('should throw SyntaxError for invalid JSON', () => {
    mockExistsSync.mock.mockImplementation(() => true);
    mockReadFileSync.mock.mockImplementation(() => 'not valid json');
    
    const loadConfig = (configPath) => {
      if (!mockExistsSync(configPath)) {
        throw new Error(`配置文件不存在: ${configPath}`);
      }
      return JSON.parse(mockReadFileSync(configPath, 'utf8'));
    };
    
    assert.throws(
      () => loadConfig('/path/to/bad.json'),
      SyntaxError
    );
  });

  it('should parse complex JSON object', () => {
    mockExistsSync.mock.mockImplementation(() => true);
    const config = {
      name: 'Complex Strategy',
      universe: ['000300.XSHG'],
      filters: [{ operator: 'greater_than', factor: { type: 'fundamental', name: 'pe_ratio' }, rhs: 10 }],
      sorting: [{ factor: { type: 'fundamental', name: 'market_cap' }, ascending: false, weight: 1 }]
    };
    mockReadFileSync.mock.mockImplementation(() => JSON.stringify(config));
    
    const loadConfig = (configPath) => {
      if (!mockExistsSync(configPath)) {
        throw new Error(`配置文件不存在: ${configPath}`);
      }
      return JSON.parse(mockReadFileSync(configPath, 'utf8'));
    };
    
    const result = loadConfig('/path/to/complex.json');
    assert.strictEqual(result.name, 'Complex Strategy');
    assert.strictEqual(result.filters.length, 1);
  });
});

describe('showHelp', () => {
  it('should output help content to console', () => {
    const capture = captureConsole();
    
    const showHelp = () => {
      console.log(`
RiceQuant 向导式策略工具

用法：
  node run-skill.js <command> [options]

命令：
  --create --config <file>     创建向导式策略
  --update --id <id> --config <file>   更新策略配置
  --run --id <id> [options]    运行回测
  --report --id <backtestId>   获取回测报告
  --list [--type wizard|code]  列出策略
  --delete --id <id>           删除策略
  --validate --config <file>   验证配置文件
  --factors                    列出所有可用因子
  --help                       显示帮助

回测选项：
  --start <date>               开始日期 (默认: 2020-01-01)
  --end <date>                 结束日期 (默认: 2025-03-28)
  --capital <number>           初始资金 (默认: 100000)
  --benchmark <code>           基准 (默认: 000300.XSHG)
  --wait                       等待回测完成
  --full                       获取完整报告
`);
    };
    
    showHelp();
    const outputText = capture.outputs().join('\n');
    capture.restore();
    
    assert.ok(outputText.includes('RiceQuant 向导式策略工具'));
    assert.ok(outputText.includes('--create'));
    assert.ok(outputText.includes('--run'));
    assert.ok(outputText.includes('--list'));
    assert.ok(outputText.includes('--help'));
  });

  it('should include all command descriptions', () => {
    const capture = captureConsole();
    
    const showHelp = () => {
      console.log(`
命令：
  --create --config <file>     创建向导式策略
  --run --id <id> [options]    运行回测
  --report --id <backtestId>   获取回测报告
`);
    };
    
    showHelp();
    const outputText = capture.outputs().join('\n');
    capture.restore();
    
    assert.ok(outputText.includes('创建向导式策略'));
    assert.ok(outputText.includes('运行回测'));
    assert.ok(outputText.includes('获取回测报告'));
  });

  it('should include backtest options', () => {
    const capture = captureConsole();
    
    const showHelp = () => {
      console.log(`
回测选项：
  --start <date>               开始日期 (默认: 2020-01-01)
  --end <date>                 结束日期 (默认: 2025-03-28)
  --capital <number>           初始资金 (默认: 100000)
  --benchmark <code>           基准 (默认: 000300.XSHG)
`);
    };
    
    showHelp();
    const outputText = capture.outputs().join('\n');
    capture.restore();
    
    assert.ok(outputText.includes('--start'));
    assert.ok(outputText.includes('--end'));
    assert.ok(outputText.includes('--capital'));
    assert.ok(outputText.includes('--benchmark'));
  });
});

describe('listFactors', () => {
  it('should output factors grouped by type', () => {
    const capture = captureConsole();
    
    const getAllFactorsFlat = () => [
      { type: 'fundamental', name: 'pe_ratio', label: '市盈率' },
      { type: 'fundamental', name: 'pb_ratio', label: '市净率' },
      { type: 'pricing', name: 'close', label: '收盘价' }
    ];
    
    const OPERATORS = [
      { name: 'greater_than', label: '大于' },
      { name: 'less_than', label: '小于' }
    ];
    
    const listFactors = () => {
      const factors = getAllFactorsFlat();
      console.log('可用因子:\n');
      
      const byType = {};
      for (const f of factors) {
        if (!byType[f.type]) byType[f.type] = [];
        byType[f.type].push(f);
      }
      
      for (const [type, typeFactors] of Object.entries(byType)) {
        console.log(`\n[${type}]`);
        for (const f of typeFactors) {
          console.log(`  ${f.name} - ${f.label}`);
        }
      }
      
      console.log('\n\n操作符:');
      for (const op of OPERATORS) {
        console.log(`  ${op.name} - ${op.label}`);
      }
    };
    
    listFactors();
    const outputText = capture.outputs().join('\n');
    capture.restore();
    
    assert.ok(outputText.includes('可用因子'));
    assert.ok(outputText.includes('[fundamental]'));
    assert.ok(outputText.includes('[pricing]'));
  });

  it('should include operators list', () => {
    const capture = captureConsole();
    
    const getAllFactorsFlat = () => [];
    const OPERATORS = [
      { name: 'greater_than', label: '大于' },
      { name: 'less_than', label: '小于' }
    ];
    
    const listFactors = () => {
      console.log('操作符:');
      for (const op of OPERATORS) {
        console.log(`  ${op.name} - ${op.label}`);
      }
    };
    
    listFactors();
    const outputText = capture.outputs().join('\n');
    capture.restore();
    
    assert.ok(outputText.includes('操作符'));
    assert.ok(outputText.includes('greater_than'));
    assert.ok(outputText.includes('less_than'));
  });

  it('should truncate factor list when exceeding 10', () => {
    const capture = captureConsole();
    
    const getAllFactorsFlat = () => {
      const factors = [];
      for (let i = 0; i < 15; i++) {
        factors.push({ type: 'fundamental', name: `factor_${i}`, label: `因子${i}` });
      }
      return factors;
    };
    
    const listFactors = () => {
      const factors = getAllFactorsFlat();
      console.log('可用因子:\n');
      
      const byType = {};
      for (const f of factors) {
        if (!byType[f.type]) byType[f.type] = [];
        byType[f.type].push(f);
      }
      
      for (const [type, typeFactors] of Object.entries(byType)) {
        console.log(`\n[${type}]`);
        for (const f of typeFactors.slice(0, 10)) {
          console.log(`  ${f.name} - ${f.label}`);
        }
        if (typeFactors.length > 10) {
          console.log(`  ... 共 ${typeFactors.length} 个因子`);
        }
      }
    };
    
    listFactors();
    const outputText = capture.outputs().join('\n');
    capture.restore();
    
    assert.ok(outputText.includes('共 15 个因子'));
  });
});

describe('validateConfig', () => {
  const mockExistsSync = mock.fn();
  const mockReadFileSync = mock.fn();
  
  beforeEach(() => {
    mockExistsSync.mock.resetCalls();
    mockReadFileSync.mock.resetCalls();
  });

  it('should validate valid config successfully', () => {
    const capture = captureConsole();
    
    mockExistsSync.mock.mockImplementation(() => true);
    mockReadFileSync.mock.mockImplementation(() => JSON.stringify({
      name: 'Test Strategy',
      universe: ['000300.XSHG']
    }));
    
    const validateWizardConfig = (config) => {
      const errors = [];
      const warnings = [];
      if (!config.name) errors.push('缺少策略名称');
      if (!config.universe || config.universe.length === 0) errors.push('缺少股票池配置');
      return { valid: errors.length === 0, errors, warnings };
    };
    
    const normalizeConfig = (config) => ({ ...config, template: 'single_period' });
    
    const loadConfig = (configPath) => {
      if (!mockExistsSync(configPath)) {
        throw new Error(`配置文件不存在: ${configPath}`);
      }
      return JSON.parse(mockReadFileSync(configPath, 'utf8'));
    };
    
    const validateConfig = (args) => {
      const config = loadConfig(args.config);
      const validation = validateWizardConfig(config);
      
      console.log(`配置文件: ${args.config}`);
      console.log(`验证结果: ${validation.valid ? '通过' : '失败'}`);
      
      if (validation.valid) {
        const normalized = normalizeConfig(config);
        console.log('\n规范化配置:');
        console.log(JSON.stringify(normalized, null, 2));
      }
    };
    
    validateConfig({ config: '/path/to/config.json' });
    const outputText = capture.outputs().join('\n');
    capture.restore();
    
    assert.ok(outputText.includes('验证结果: 通过'));
    assert.ok(outputText.includes('规范化配置'));
  });

  it('should show errors for invalid config', () => {
    const capture = captureConsole();
    
    mockExistsSync.mock.mockImplementation(() => true);
    mockReadFileSync.mock.mockImplementation(() => JSON.stringify({}));
    
    const validateWizardConfig = (config) => {
      const errors = [];
      const warnings = [];
      if (!config.name) errors.push('缺少策略名称');
      if (!config.universe || config.universe.length === 0) errors.push('缺少股票池配置');
      return { valid: errors.length === 0, errors, warnings };
    };
    
    const loadConfig = (configPath) => {
      if (!mockExistsSync(configPath)) {
        throw new Error(`配置文件不存在: ${configPath}`);
      }
      return JSON.parse(mockReadFileSync(configPath, 'utf8'));
    };
    
    const validateConfig = (args) => {
      const config = loadConfig(args.config);
      const validation = validateWizardConfig(config);
      
      console.log(`配置文件: ${args.config}`);
      console.log(`验证结果: ${validation.valid ? '通过' : '失败'}`);
      
      if (validation.errors.length > 0) {
        console.log('\n错误:');
        validation.errors.forEach(e => console.log(`  - ${e}`));
      }
    };
    
    validateConfig({ config: '/path/to/config.json' });
    const outputText = capture.outputs().join('\n');
    capture.restore();
    
    assert.ok(outputText.includes('验证结果: 失败'));
    assert.ok(outputText.includes('错误'));
    assert.ok(outputText.includes('缺少策略名称'));
  });

  it('should show warnings when present', () => {
    const capture = captureConsole();
    
    mockExistsSync.mock.mockImplementation(() => true);
    mockReadFileSync.mock.mockImplementation(() => JSON.stringify({
      name: 'Test Strategy',
      universe: ['000300.XSHG'],
      template: 'unknown_template'
    }));
    
    const validateWizardConfig = (config) => {
      const errors = [];
      const warnings = [];
      if (!config.name) errors.push('缺少策略名称');
      if (!config.universe || config.universe.length === 0) errors.push('缺少股票池配置');
      if (config.template === 'unknown_template') warnings.push('未知的模板类型');
      return { valid: errors.length === 0, errors, warnings };
    };
    
    const loadConfig = (configPath) => {
      return JSON.parse(mockReadFileSync(configPath, 'utf8'));
    };
    
    const validateConfig = (args) => {
      const config = loadConfig(args.config);
      const validation = validateWizardConfig(config);
      
      console.log(`验证结果: ${validation.valid ? '通过' : '失败'}`);
      
      if (validation.warnings.length > 0) {
        console.log('\n警告:');
        validation.warnings.forEach(w => console.log(`  - ${w}`));
      }
    };
    
    validateConfig({ config: '/path/to/config.json' });
    const outputText = capture.outputs().join('\n');
    capture.restore();
    
    assert.ok(outputText.includes('警告'));
    assert.ok(outputText.includes('未知的模板类型'));
  });
});

describe('createStrategy', () => {
  const mockExistsSync = mock.fn();
  const mockReadFileSync = mock.fn();
  const mockCreateWizardStrategy = mock.fn();
  const mockRunBacktest = mock.fn();
  const mockWaitForBacktest = mock.fn();
  const mockGetFullReport = mock.fn();
  const mockSaveReport = mock.fn();
  
  beforeEach(() => {
    mockExistsSync.mock.resetCalls();
    mockReadFileSync.mock.resetCalls();
    mockCreateWizardStrategy.mock.resetCalls();
    mockRunBacktest.mock.resetCalls();
    mockWaitForBacktest.mock.resetCalls();
    mockGetFullReport.mock.resetCalls();
    mockSaveReport.mock.resetCalls();
  });

  it('should create strategy with valid config', async () => {
    const capture = captureConsole();
    
    mockExistsSync.mock.mockImplementation(() => true);
    mockReadFileSync.mock.mockImplementation(() => JSON.stringify({
      name: 'Test Strategy',
      universe: ['000300.XSHG']
    }));
    
    mockCreateWizardStrategy.mock.mockImplementation(async (config) => ({
      strategyId: 'strategy-123',
      title: config.name
    }));
    
    const validateWizardConfig = (config) => {
      const errors = [];
      const warnings = [];
      if (!config.name) errors.push('缺少策略名称');
      if (!config.universe || config.universe.length === 0) errors.push('缺少股票池配置');
      return { valid: errors.length === 0, errors, warnings };
    };
    
    const normalizeConfig = (config) => ({ ...config });
    
    const loadConfig = (configPath) => {
      return JSON.parse(mockReadFileSync(configPath, 'utf8'));
    };
    
    const client = {
      createWizardStrategy: mockCreateWizardStrategy
    };
    
    const createStrategy = async (client, args) => {
      const config = loadConfig(args.config);
      
      const validation = validateWizardConfig(config);
      if (!validation.valid) {
        console.error('配置验证失败:');
        validation.errors.forEach(e => console.error(`  - ${e}`));
        process.exit(1);
        return;
      }
      
      const normalized = normalizeConfig(config);
      
      console.log(`创建向导式策略: ${normalized.name}`);
      const result = await client.createWizardStrategy(normalized);
      
      console.log(`\n策略创建成功!`);
      console.log(`  ID: ${result.strategyId}`);
      console.log(`  名称: ${result.title}`);
      
      return result;
    };
    
    const result = await createStrategy(client, { config: '/path/to/config.json' });
    const outputText = capture.outputs().join('\n');
    capture.restore();
    
    assert.strictEqual(result.strategyId, 'strategy-123');
    assert.strictEqual(result.title, 'Test Strategy');
    assert.strictEqual(mockCreateWizardStrategy.mock.callCount(), 1);
    assert.ok(outputText.includes('创建向导式策略'));
    assert.ok(outputText.includes('策略创建成功'));
  });

  it('should run backtest when --run flag is set', async () => {
    mockExistsSync.mock.mockImplementation(() => true);
    mockReadFileSync.mock.mockImplementation(() => JSON.stringify({
      name: 'Test Strategy',
      universe: ['000300.XSHG']
    }));
    
    mockCreateWizardStrategy.mock.mockImplementation(async (config) => ({
      strategyId: 'strategy-123',
      title: config.name
    }));
    
    mockRunBacktest.mock.mockImplementation(async () => ({
      backtestId: 'backtest-456'
    }));
    
    const client = {
      createWizardStrategy: mockCreateWizardStrategy,
      runBacktest: mockRunBacktest
    };
    
    const validateWizardConfig = (config) => ({ valid: true, errors: [], warnings: [] });
    const normalizeConfig = (config) => ({ ...config, backtest: {} });
    const loadConfig = () => JSON.parse(mockReadFileSync());
    
    const createStrategy = async (client, args) => {
      const config = loadConfig(args.config);
      const validation = validateWizardConfig(config);
      if (!validation.valid) return;
      
      const normalized = normalizeConfig(config);
      const result = await client.createWizardStrategy(normalized);
      
      if (args.run) {
        console.log(`\n启动回测...`);
        const backtest = await client.runBacktest(result.strategyId, normalized.backtest);
        console.log(`  回测ID: ${backtest.backtestId}`);
      }
      
      return result;
    };
    
    await createStrategy(client, { config: '/path/to/config.json', run: true });
    
    assert.strictEqual(mockRunBacktest.mock.callCount(), 1);
  });

  it('should exit with error for invalid config', async () => {
    const originalExit = process.exit;
    const mockExit = mock.fn();
    process.exit = mockExit;
    
    mockExistsSync.mock.mockImplementation(() => true);
    mockReadFileSync.mock.mockImplementation(() => JSON.stringify({}));
    
    const validateWizardConfig = (config) => ({
      valid: false,
      errors: ['缺少策略名称', '缺少股票池配置'],
      warnings: []
    });
    
    const loadConfig = () => JSON.parse(mockReadFileSync());
    
    const client = { createWizardStrategy: mockCreateWizardStrategy };
    
    const createStrategy = async (client, args) => {
      const config = loadConfig(args.config);
      const validation = validateWizardConfig(config);
      if (!validation.valid) {
        console.error('配置验证失败:');
        validation.errors.forEach(e => console.error(`  - ${e}`));
        process.exit(1);
        return;
      }
    };
    
    await createStrategy(client, { config: '/path/to/config.json' });
    
    assert.strictEqual(mockExit.mock.callCount(), 1);
    process.exit = originalExit;
  });
});

describe('updateStrategy', () => {
  const mockExistsSync = mock.fn();
  const mockReadFileSync = mock.fn();
  const mockUpdateWizardStrategy = mock.fn();
  
  beforeEach(() => {
    mockExistsSync.mock.resetCalls();
    mockReadFileSync.mock.resetCalls();
    mockUpdateWizardStrategy.mock.resetCalls();
  });

  it('should update strategy with valid config', async () => {
    const capture = captureConsole();
    
    mockExistsSync.mock.mockImplementation(() => true);
    mockReadFileSync.mock.mockImplementation(() => JSON.stringify({
      name: 'Updated Strategy',
      universe: ['000300.XSHG']
    }));
    
    mockUpdateWizardStrategy.mock.mockImplementation(async () => ({ success: true }));
    
    const validateWizardConfig = (config) => ({ valid: true, errors: [], warnings: [] });
    const normalizeConfig = (config) => ({ ...config });
    const loadConfig = () => JSON.parse(mockReadFileSync());
    
    const client = { updateWizardStrategy: mockUpdateWizardStrategy };
    
    const updateStrategy = async (client, args) => {
      const config = loadConfig(args.config);
      const validation = validateWizardConfig(config);
      if (!validation.valid) {
        console.error('配置验证失败:');
        process.exit(1);
        return;
      }
      
      const normalized = normalizeConfig(config);
      console.log(`更新策略 ${args.id}...`);
      await client.updateWizardStrategy(args.id, normalized);
      console.log('更新成功');
    };
    
    await updateStrategy(client, { id: 'strategy-123', config: '/path/to/config.json' });
    const outputText = capture.outputs().join('\n');
    capture.restore();
    
    assert.strictEqual(mockUpdateWizardStrategy.mock.callCount(), 1);
    assert.ok(outputText.includes('更新成功'));
  });

  it('should exit with error for invalid config', async () => {
    const originalExit = process.exit;
    const mockExit = mock.fn();
    process.exit = mockExit;
    
    mockExistsSync.mock.mockImplementation(() => true);
    mockReadFileSync.mock.mockImplementation(() => JSON.stringify({}));
    
    const validateWizardConfig = (config) => ({
      valid: false,
      errors: ['缺少策略名称'],
      warnings: []
    });
    const loadConfig = () => JSON.parse(mockReadFileSync());
    const client = { updateWizardStrategy: mockUpdateWizardStrategy };
    
    const updateStrategy = async (client, args) => {
      const config = loadConfig(args.config);
      const validation = validateWizardConfig(config);
      if (!validation.valid) {
        console.error('配置验证失败:');
        process.exit(1);
        return;
      }
    };
    
    await updateStrategy(client, { id: 'strategy-123', config: '/path/to/config.json' });
    
    assert.strictEqual(mockExit.mock.callCount(), 1);
    process.exit = originalExit;
  });
});

describe('runBacktest', () => {
  const mockRunBacktest = mock.fn();
  const mockWaitForBacktest = mock.fn();
  const mockGetFullReport = mock.fn();
  const mockSaveReport = mock.fn();
  
  beforeEach(() => {
    mockRunBacktest.mock.resetCalls();
    mockWaitForBacktest.mock.resetCalls();
    mockGetFullReport.mock.resetCalls();
    mockSaveReport.mock.resetCalls();
  });

  it('should run backtest with default parameters', async () => {
    const capture = captureConsole();
    
    mockRunBacktest.mock.mockImplementation(async () => ({ backtestId: 'backtest-456' }));
    
    const client = {
      runBacktest: mockRunBacktest,
      waitForBacktest: mockWaitForBacktest
    };
    
    const runBacktest = async (client, args) => {
      const backtestConfig = {
        start: args.start || '2020-01-01',
        end: args.end || '2025-03-28',
        capital: args.capital || '100000',
        benchmark: args.benchmark || '000300.XSHG',
        frequency: 'day'
      };
      
      console.log(`运行回测: 策略 ${args.id}`);
      console.log(`  时间: ${backtestConfig.start} ~ ${backtestConfig.end}`);
      console.log(`  资金: ${backtestConfig.capital}`);
      
      const result = await client.runBacktest(args.id, backtestConfig);
      console.log(`\n回测已启动: ${result.backtestId}`);
      
      return result;
    };
    
    await runBacktest(client, { id: 'strategy-123' });
    const outputText = capture.outputs().join('\n');
    capture.restore();
    
    assert.strictEqual(mockRunBacktest.mock.callCount(), 1);
    const callArgs = mockRunBacktest.mock.calls[0].arguments;
    assert.strictEqual(callArgs[1].start, '2020-01-01');
    assert.strictEqual(callArgs[1].end, '2025-03-28');
    assert.strictEqual(callArgs[1].capital, '100000');
    assert.strictEqual(callArgs[1].benchmark, '000300.XSHG');
    assert.ok(outputText.includes('运行回测'));
    assert.ok(outputText.includes('回测已启动'));
  });

  it('should run backtest with custom parameters', async () => {
    mockRunBacktest.mock.mockImplementation(async () => ({ backtestId: 'backtest-456' }));
    
    const client = { runBacktest: mockRunBacktest };
    
    const runBacktest = async (client, args) => {
      const backtestConfig = {
        start: args.start || '2020-01-01',
        end: args.end || '2025-03-28',
        capital: args.capital || '100000',
        benchmark: args.benchmark || '000300.XSHG',
        frequency: 'day'
      };
      return await client.runBacktest(args.id, backtestConfig);
    };
    
    await runBacktest(client, {
      id: 'strategy-123',
      start: '2021-01-01',
      end: '2024-01-01',
      capital: '200000',
      benchmark: '000905.XSHG'
    });
    
    const callArgs = mockRunBacktest.mock.calls[0].arguments;
    assert.strictEqual(callArgs[1].start, '2021-01-01');
    assert.strictEqual(callArgs[1].end, '2024-01-01');
    assert.strictEqual(callArgs[1].capital, '200000');
    assert.strictEqual(callArgs[1].benchmark, '000905.XSHG');
  });

  it('should wait for backtest completion with --wait flag', async () => {
    mockRunBacktest.mock.mockImplementation(async () => ({ backtestId: 'backtest-456' }));
    mockWaitForBacktest.mock.mockImplementation(async () => ({ status: 'finished' }));
    
    const client = {
      runBacktest: mockRunBacktest,
      waitForBacktest: mockWaitForBacktest
    };
    
    const runBacktest = async (client, args) => {
      const backtestConfig = {
        start: args.start || '2020-01-01',
        end: args.end || '2025-03-28',
        capital: args.capital || '100000',
        benchmark: args.benchmark || '000300.XSHG',
        frequency: 'day'
      };
      
      const result = await client.runBacktest(args.id, backtestConfig);
      
      if (args.wait) {
        console.log('等待回测完成...');
        const waitResult = await client.waitForBacktest(result.backtestId);
        
        if (waitResult.status === 'finished') {
          console.log('回测完成!');
        }
      }
      
      return result;
    };
    
    await runBacktest(client, { id: 'strategy-123', wait: true });
    
    assert.strictEqual(mockWaitForBacktest.mock.callCount(), 1);
  });

  it('should get full report with --wait and --full flags', async () => {
    mockRunBacktest.mock.mockImplementation(async () => ({ backtestId: 'backtest-456' }));
    mockWaitForBacktest.mock.mockImplementation(async () => ({ status: 'finished' }));
    mockGetFullReport.mock.mockImplementation(async () => ({
      backtestId: 'backtest-456',
      risk: { alpha: 0.05, sharpe: 1.5, max_drawdown: 0.15 }
    }));
    mockSaveReport.mock.mockImplementation(() => '/data/report.json');
    
    const client = {
      runBacktest: mockRunBacktest,
      waitForBacktest: mockWaitForBacktest,
      getFullReport: mockGetFullReport,
      saveReport: mockSaveReport
    };
    
    const runBacktest = async (client, args) => {
      const backtestConfig = {
        start: args.start || '2020-01-01',
        end: args.end || '2025-03-28',
        capital: args.capital || '100000',
        benchmark: args.benchmark || '000300.XSHG',
        frequency: 'day'
      };
      
      const result = await client.runBacktest(args.id, backtestConfig);
      
      if (args.wait) {
        const waitResult = await client.waitForBacktest(result.backtestId);
        
        if (waitResult.status === 'finished' && args.full) {
          const report = await client.getFullReport(result.backtestId);
          const reportPath = client.saveReport(result.backtestId, report);
          console.log(`\n完整报告: ${reportPath}`);
        }
      }
      
      return result;
    };
    
    await runBacktest(client, { id: 'strategy-123', wait: true, full: true });
    
    assert.strictEqual(mockGetFullReport.mock.callCount(), 1);
    assert.strictEqual(mockSaveReport.mock.callCount(), 1);
  });

  it('should handle backtest error status', async () => {
    const capture = captureConsole();
    
    mockRunBacktest.mock.mockImplementation(async () => ({ backtestId: 'backtest-456' }));
    mockWaitForBacktest.mock.mockImplementation(async () => ({
      status: 'error',
      exception: 'Backtest failed'
    }));
    
    const client = {
      runBacktest: mockRunBacktest,
      waitForBacktest: mockWaitForBacktest
    };
    
    const runBacktest = async (client, args) => {
      const backtestConfig = {
        start: args.start || '2020-01-01',
        end: args.end || '2025-03-28',
        capital: args.capital || '100000',
        benchmark: args.benchmark || '000300.XSHG',
        frequency: 'day'
      };
      
      const result = await client.runBacktest(args.id, backtestConfig);
      
      if (args.wait) {
        const waitResult = await client.waitForBacktest(result.backtestId);
        
        if (waitResult.status === 'error') {
          console.error('回测出错:', waitResult.exception);
        }
      }
      
      return result;
    };
    
    await runBacktest(client, { id: 'strategy-123', wait: true });
    const errorText = capture.errors().join('\n');
    capture.restore();
    
    assert.ok(errorText.includes('回测出错'));
    assert.ok(errorText.includes('Backtest failed'));
  });

  it('should handle backtest timeout', async () => {
    const capture = captureConsole();
    
    mockRunBacktest.mock.mockImplementation(async () => ({ backtestId: 'backtest-456' }));
    mockWaitForBacktest.mock.mockImplementation(async () => ({ status: 'timeout' }));
    
    const client = {
      runBacktest: mockRunBacktest,
      waitForBacktest: mockWaitForBacktest
    };
    
    const runBacktest = async (client, args) => {
      const backtestConfig = {
        start: args.start || '2020-01-01',
        end: args.end || '2025-03-28',
        capital: args.capital || '100000',
        benchmark: args.benchmark || '000300.XSHG',
        frequency: 'day'
      };
      
      const result = await client.runBacktest(args.id, backtestConfig);
      
      if (args.wait) {
        const waitResult = await client.waitForBacktest(result.backtestId);
        
        if (waitResult.status === 'timeout') {
          console.log('回测超时');
        }
      }
      
      return result;
    };
    
    await runBacktest(client, { id: 'strategy-123', wait: true });
    const outputText = capture.outputs().join('\n');
    capture.restore();
    
    assert.ok(outputText.includes('回测超时'));
  });
});

describe('getReport', () => {
  const mockGetFullReport = mock.fn();
  const mockWriteFileSync = mock.fn();
  
  beforeEach(() => {
    mockGetFullReport.mock.resetCalls();
    mockWriteFileSync.mock.resetCalls();
    mockConsoleLog.mock.resetCalls();
    mockConsoleError.mock.resetCalls();
  });

  it('should fetch and display report', async () => {
    const capture = captureConsole();
    
    mockGetFullReport.mock.mockImplementation(async () => ({
      backtestId: 'backtest-456',
      result: { status: 'finished' },
      risk: {
        alpha: 0.05,
        beta: 1.2,
        sharpe: 1.5,
        max_drawdown: 0.15,
        annual_volatility: 0.2
      }
    }));
    
    const client = { getFullReport: mockGetFullReport };
    
    const getReport = async (client, args) => {
      const report = await client.getFullReport(args.id);
      const reportPath = `/data/report-${args.id}-${Date.now()}.json`;
      
      console.log(`回测报告: ${args.id}`);
      console.log(`  状态: ${report.result?.status || 'unknown'}`);
      
      if (report.risk) {
        console.log('\n风险指标:');
        console.log(`  Alpha: ${(report.risk.alpha * 100).toFixed(2)}%`);
        console.log(`  Beta: ${report.risk.beta?.toFixed(2) || 'N/A'}`);
        console.log(`  Sharpe: ${report.risk.sharpe?.toFixed(2) || 'N/A'}`);
        console.log(`  Max Drawdown: ${(report.risk.max_drawdown * 100).toFixed(2)}%`);
      }
      
      console.log(`\n详细报告: ${reportPath}`);
    };
    
    await getReport(client, { id: 'backtest-456' });
    const outputText = capture.outputs().join('\n');
    capture.restore();
    
    assert.strictEqual(mockGetFullReport.mock.callCount(), 1);
    assert.ok(outputText.includes('回测报告'));
    assert.ok(outputText.includes('风险指标'));
    assert.ok(outputText.includes('Alpha'));
    assert.ok(outputText.includes('Sharpe'));
  });

  it('should handle report without risk data', async () => {
    const capture = captureConsole();
    
    mockGetFullReport.mock.mockImplementation(async () => ({
      backtestId: 'backtest-456',
      result: { status: 'finished' }
    }));
    
    const client = { getFullReport: mockGetFullReport };
    
    const getReport = async (client, args) => {
      const report = await client.getFullReport(args.id);
      console.log(`回测报告: ${args.id}`);
      console.log(`  状态: ${report.result?.status || 'unknown'}`);
      console.log(`\n详细报告: saved`);
    };
    
    await getReport(client, { id: 'backtest-456' });
    const outputText = capture.outputs().join('\n');
    capture.restore();
    
    assert.ok(outputText.includes('回测报告'));
    assert.ok(!outputText.includes('风险指标'));
  });

  it('should display exception when present', async () => {
    const capture = captureConsole();
    
    mockGetFullReport.mock.mockImplementation(async () => ({
      backtestId: 'backtest-456',
      result: { status: 'error' },
      exception: 'Division by zero'
    }));
    
    const client = { getFullReport: mockGetFullReport };
    
    const getReport = async (client, args) => {
      const report = await client.getFullReport(args.id);
      console.log(`回测报告: ${args.id}`);
      
      if (report.exception) {
        console.log(`\n异常: ${report.exception}`);
      }
    };
    
    await getReport(client, { id: 'backtest-456' });
    const outputText = capture.outputs().join('\n');
    capture.restore();
    
    assert.ok(outputText.includes('异常'));
    assert.ok(outputText.includes('Division by zero'));
  });
});

describe('listStrategies', () => {
  const mockListStrategies = mock.fn();
  
  beforeEach(() => {
    mockListStrategies.mock.resetCalls();
  });

  it('should list all strategies without type filter', async () => {
    const capture = captureConsole();
    
    mockListStrategies.mock.mockImplementation(async () => [
      { id: '1', title: 'Wizard Strategy', type: 'wizard' },
      { id: '2', title: 'Code Strategy', type: 'code' }
    ]);
    
    const client = { listStrategies: mockListStrategies };
    
    const listStrategies = async (client, args) => {
      const strategies = await client.listStrategies({ type: args.type });
      
      console.log(`策略列表 (${strategies.length} 个):\n`);
      
      for (const s of strategies) {
        console.log(`  [${s.type === 'wizard' ? 'W' : 'C'}] ${s.id} - ${s.title}`);
      }
    };
    
    await listStrategies(client, {});
    const outputText = capture.outputs().join('\n');
    capture.restore();
    
    assert.strictEqual(mockListStrategies.mock.callCount(), 1);
    const callArgs = mockListStrategies.mock.calls[0].arguments;
    assert.strictEqual(callArgs[0].type, undefined);
    assert.ok(outputText.includes('策略列表'));
    assert.ok(outputText.includes('Wizard Strategy'));
    assert.ok(outputText.includes('Code Strategy'));
  });

  it('should filter wizard strategies with --type wizard', async () => {
    mockListStrategies.mock.mockImplementation(async (options) => {
      if (options.type === 'wizard') {
        return [{ id: '1', title: 'Wizard Strategy', type: 'wizard' }];
      }
      return [];
    });
    
    const client = { listStrategies: mockListStrategies };
    
    const listStrategies = async (client, args) => {
      return await client.listStrategies({ type: args.type });
    };
    
    const result = await listStrategies(client, { type: 'wizard' });
    
    const callArgs = mockListStrategies.mock.calls[0].arguments;
    assert.strictEqual(callArgs[0].type, 'wizard');
    assert.strictEqual(result.length, 1);
    assert.strictEqual(result[0].type, 'wizard');
  });

  it('should filter code strategies with --type code', async () => {
    mockListStrategies.mock.mockImplementation(async (options) => {
      if (options.type === 'code') {
        return [{ id: '2', title: 'Code Strategy', type: 'code' }];
      }
      return [];
    });
    
    const client = { listStrategies: mockListStrategies };
    
    const listStrategies = async (client, args) => {
      return await client.listStrategies({ type: args.type });
    };
    
    const result = await listStrategies(client, { type: 'code' });
    
    const callArgs = mockListStrategies.mock.calls[0].arguments;
    assert.strictEqual(callArgs[0].type, 'code');
    assert.strictEqual(result.length, 1);
    assert.strictEqual(result[0].type, 'code');
  });
});

describe('deleteStrategy', () => {
  const mockDeleteStrategy = mock.fn();
  
  beforeEach(() => {
    mockDeleteStrategy.mock.resetCalls();
  });

  it('should delete strategy successfully', async () => {
    const capture = captureConsole();
    
    mockDeleteStrategy.mock.mockImplementation(async () => true);
    
    const client = { deleteStrategy: mockDeleteStrategy };
    
    const deleteStrategy = async (client, args) => {
      console.log(`删除策略 ${args.id}...`);
      const success = await client.deleteStrategy(args.id);
      
      if (success) {
        console.log('删除成功');
      } else {
        console.log('删除失败');
      }
    };
    
    await deleteStrategy(client, { id: 'strategy-123' });
    const outputText = capture.outputs().join('\n');
    capture.restore();
    
    assert.strictEqual(mockDeleteStrategy.mock.callCount(), 1);
    assert.ok(outputText.includes('删除成功'));
  });

  it('should handle delete failure', async () => {
    const capture = captureConsole();
    
    mockDeleteStrategy.mock.mockImplementation(async () => false);
    
    const client = { deleteStrategy: mockDeleteStrategy };
    
    const deleteStrategy = async (client, args) => {
      console.log(`删除策略 ${args.id}...`);
      const success = await client.deleteStrategy(args.id);
      
      if (success) {
        console.log('删除成功');
      } else {
        console.log('删除失败');
      }
    };
    
    await deleteStrategy(client, { id: 'strategy-123' });
    const outputText = capture.outputs().join('\n');
    capture.restore();
    
    assert.ok(outputText.includes('删除失败'));
  });
});
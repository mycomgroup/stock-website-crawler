import { strict as assert } from 'assert';
import { describe, it } from 'node:test';

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = argv[i + 1];
      if (value && !value.startsWith('--')) {
        args[key] = value;
        i++;
      } else {
        args[key] = true;
      }
    }
  }
  return args;
}

describe('parseArgs', () => {
  it('should parse empty array', () => {
    const result = parseArgs([]);
    assert.deepStrictEqual(result, {});
  });

  it('should parse single flag without value', () => {
    const result = parseArgs(['--help']);
    assert.deepStrictEqual(result, { help: true });
  });

  it('should parse flag with value', () => {
    const result = parseArgs(['--message', 'hello']);
    assert.deepStrictEqual(result, { message: 'hello' });
  });

  it('should parse multiple flags', () => {
    const result = parseArgs(['--login', '--headed']);
    assert.deepStrictEqual(result, { login: true, headed: true });
  });

  it('should parse flag with value followed by another flag', () => {
    const result = parseArgs(['--model', 'gpt-4', '--headed']);
    assert.deepStrictEqual(result, { model: 'gpt-4', headed: true });
  });

  it('should parse flag with value containing spaces', () => {
    const result = parseArgs(['--message', 'hello world']);
    assert.deepStrictEqual(result, { message: 'hello world' });
  });

  it('should handle consecutive flags without values', () => {
    const result = parseArgs(['--login', '--force', '--headed']);
    assert.deepStrictEqual(result, { login: true, force: true, headed: true });
  });

  it('should parse --use-profile with path', () => {
    const result = parseArgs(['--use-profile', '/path/to/profile']);
    assert.deepStrictEqual(result, { 'use-profile': '/path/to/profile' });
  });

  it('should parse --set-weight with id and value separately', () => {
    const result = parseArgs(['--set-weight', 'account-1']);
    assert.deepStrictEqual(result, { 'set-weight': 'account-1' });
  });

  it('should parse complex command with multiple options', () => {
    const result = parseArgs([
      '--message', 'test message',
      '--model', 'gemini-pro',
      '--conversation', 'conv-123'
    ]);
    assert.deepStrictEqual(result, {
      message: 'test message',
      model: 'gemini-pro',
      conversation: 'conv-123'
    });
  });

  it('should handle empty string value (treated as flag)', () => {
    const result = parseArgs(['--message', '']);
    assert.deepStrictEqual(result, { message: true });
  });

  it('should not treat flag as value for previous flag', () => {
    const result = parseArgs(['--message', '--login']);
    assert.deepStrictEqual(result, { message: true, login: true });
  });

  it('should parse --batch with file path', () => {
    const result = parseArgs(['--batch', 'questions.txt']);
    assert.deepStrictEqual(result, { batch: 'questions.txt' });
  });

  it('should parse --file with file path', () => {
    const result = parseArgs(['--file', 'prompt.txt']);
    assert.deepStrictEqual(result, { file: 'prompt.txt' });
  });

  it('should parse --search with query', () => {
    const result = parseArgs(['--search', 'JavaScript']);
    assert.deepStrictEqual(result, { search: 'JavaScript' });
  });

  it('should parse --show with conversation id', () => {
    const result = parseArgs(['--show', 'conv-abc123']);
    assert.deepStrictEqual(result, { show: 'conv-abc123' });
  });

  it('should parse --delete with conversation id', () => {
    const result = parseArgs(['--delete', 'conv-abc123']);
    assert.deepStrictEqual(result, { delete: 'conv-abc123' });
  });

  it('should parse --add-account without name', () => {
    const result = parseArgs(['--add-account']);
    assert.deepStrictEqual(result, { 'add-account': true });
  });

  it('should parse --add-account with name', () => {
    const result = parseArgs(['--add-account', 'work-account']);
    assert.deepStrictEqual(result, { 'add-account': 'work-account' });
  });

  it('should parse --remove-account with id', () => {
    const result = parseArgs(['--remove-account', 'account-123']);
    assert.deepStrictEqual(result, { 'remove-account': 'account-123' });
  });

  it('should parse --enable-account with id', () => {
    const result = parseArgs(['--enable-account', 'account-123']);
    assert.deepStrictEqual(result, { 'enable-account': 'account-123' });
  });

  it('should parse --disable-account with id', () => {
    const result = parseArgs(['--disable-account', 'account-123']);
    assert.deepStrictEqual(result, { 'disable-account': 'account-123' });
  });

  it('should parse --set-strategy with value', () => {
    const result = parseArgs(['--set-strategy', 'weighted']);
    assert.deepStrictEqual(result, { 'set-strategy': 'weighted' });
  });

  it('should parse validate flag', () => {
    const result = parseArgs(['--validate']);
    assert.deepStrictEqual(result, { validate: true });
  });

  it('should parse list flag', () => {
    const result = parseArgs(['--list']);
    assert.deepStrictEqual(result, { list: true });
  });

  it('should parse list-all flag', () => {
    const result = parseArgs(['--list-all']);
    assert.deepStrictEqual(result, { 'list-all': true });
  });

  it('should parse models flag', () => {
    const result = parseArgs(['--models']);
    assert.deepStrictEqual(result, { models: true });
  });

  it('should parse account flag', () => {
    const result = parseArgs(['--account']);
    assert.deepStrictEqual(result, { account: true });
  });

  it('should parse validate-accounts flag', () => {
    const result = parseArgs(['--validate-accounts']);
    assert.deepStrictEqual(result, { 'validate-accounts': true });
  });

  it('should parse account-stats flag', () => {
    const result = parseArgs(['--account-stats']);
    assert.deepStrictEqual(result, { 'account-stats': true });
  });

  it('should parse list-accounts flag', () => {
    const result = parseArgs(['--list-accounts']);
    assert.deepStrictEqual(result, { 'list-accounts': true });
  });

  it('should handle kebab-case flag names correctly', () => {
    const result = parseArgs(['--use-profile', '/path', '--set-weight', '5']);
    assert.deepStrictEqual(result, { 'use-profile': '/path', 'set-weight': '5' });
  });

  it('should handle special characters in values', () => {
    const result = parseArgs(['--message', 'Hello!@#$%^&*()']);
    assert.strictEqual(result.message, 'Hello!@#$%^&*()');
  });

  it('should handle unicode in values', () => {
    const result = parseArgs(['--message', '你好世界']);
    assert.strictEqual(result.message, '你好世界');
  });

  it('should handle numeric string values', () => {
    const result = parseArgs(['--set-weight', '5']);
    assert.strictEqual(result['set-weight'], '5');
  });

  it('should handle path with spaces', () => {
    const result = parseArgs(['--use-profile', '/path/with spaces/profile']);
    assert.strictEqual(result['use-profile'], '/path/with spaces/profile');
  });

  it('should handle multiple hyphens in value', () => {
    const result = parseArgs(['--conversation', 'conv-abc-123-xyz']);
    assert.strictEqual(result.conversation, 'conv-abc-123-xyz');
  });

  it('should handle value that starts with single hyphen', () => {
    const result = parseArgs(['--message', '-not-a-flag']);
    assert.strictEqual(result.message, '-not-a-flag');
  });
});

describe('Argument combinations', () => {
  it('should handle login with headed option', () => {
    const result = parseArgs(['--login', '--headed']);
    assert.strictEqual(result.login, true);
    assert.strictEqual(result.headed, true);
  });

  it('should handle login with force option', () => {
    const result = parseArgs(['--login', '--force']);
    assert.strictEqual(result.login, true);
    assert.strictEqual(result.force, true);
  });

  it('should handle force alone (triggers login)', () => {
    const result = parseArgs(['--force']);
    assert.strictEqual(result.force, true);
  });

  it('should handle message with model and conversation', () => {
    const result = parseArgs([
      '--message', 'Hello',
      '--model', 'gemini-pro',
      '--conversation', 'conv-123'
    ]);
    assert.strictEqual(result.message, 'Hello');
    assert.strictEqual(result.model, 'gemini-pro');
    assert.strictEqual(result.conversation, 'conv-123');
  });

  it('should handle use-profile with path', () => {
    const result = parseArgs(['--login', '--use-profile', '/Users/test/Chrome/Default']);
    assert.strictEqual(result.login, true);
    assert.strictEqual(result['use-profile'], '/Users/test/Chrome/Default');
  });
});

describe('Command flow logic tests', () => {
  it('should identify help command correctly', () => {
    const args = parseArgs(['--help']);
    const shouldShowHelp = args.help || Object.keys(args).length === 0;
    assert.strictEqual(shouldShowHelp, true);
  });

  it('should show help when no args provided', () => {
    const args = parseArgs([]);
    const shouldShowHelp = args.help || Object.keys(args).length === 0;
    assert.strictEqual(shouldShowHelp, true);
  });

  it('should not show help when valid command provided', () => {
    const args = parseArgs(['--validate']);
    const shouldShowHelp = args.help || Object.keys(args).length === 0;
    assert.strictEqual(shouldShowHelp, false);
  });

  it('should identify login command', () => {
    const args = parseArgs(['--login']);
    const isLogin = args.login || args.force;
    assert.strictEqual(isLogin, true);
  });

  it('should identify force login command', () => {
    const args = parseArgs(['--force']);
    const isLogin = args.login || args.force;
    assert.strictEqual(isLogin, true);
  });

  it('should identify validate command', () => {
    const args = parseArgs(['--validate']);
    assert.strictEqual(args.validate, true);
  });

  it('should identify list command', () => {
    const args = parseArgs(['--list']);
    const isList = args.list || args['list-all'];
    assert.strictEqual(isList, true);
  });

  it('should identify list-all command', () => {
    const args = parseArgs(['--list-all']);
    const isList = args.list || args['list-all'];
    assert.strictEqual(isList, true);
  });

  it('should identify search command', () => {
    const args = parseArgs(['--search', 'query']);
    assert.strictEqual(args.search, 'query');
  });

  it('should identify show command', () => {
    const args = parseArgs(['--show', 'conv-123']);
    assert.strictEqual(args.show, 'conv-123');
  });

  it('should identify delete command', () => {
    const args = parseArgs(['--delete', 'conv-123']);
    assert.strictEqual(args.delete, 'conv-123');
  });

  it('should identify models command', () => {
    const args = parseArgs(['--models']);
    assert.strictEqual(args.models, true);
  });

  it('should identify account command', () => {
    const args = parseArgs(['--account']);
    assert.strictEqual(args.account, true);
  });

  it('should identify add-account command without name', () => {
    const args = parseArgs(['--add-account']);
    const isAddAccount = args['add-account'] !== undefined;
    assert.strictEqual(isAddAccount, true);
    assert.strictEqual(args['add-account'], true);
  });

  it('should identify add-account command with name', () => {
    const args = parseArgs(['--add-account', 'my-account']);
    const isAddAccount = args['add-account'] !== undefined;
    assert.strictEqual(isAddAccount, true);
    assert.strictEqual(args['add-account'], 'my-account');
  });

  it('should identify list-accounts command', () => {
    const args = parseArgs(['--list-accounts']);
    assert.strictEqual(args['list-accounts'], true);
  });

  it('should identify remove-account command', () => {
    const args = parseArgs(['--remove-account', 'acc-123']);
    assert.strictEqual(args['remove-account'], 'acc-123');
  });

  it('should identify enable-account command', () => {
    const args = parseArgs(['--enable-account', 'acc-123']);
    assert.strictEqual(args['enable-account'], 'acc-123');
  });

  it('should identify disable-account command', () => {
    const args = parseArgs(['--disable-account', 'acc-123']);
    assert.strictEqual(args['disable-account'], 'acc-123');
  });

  it('should identify set-weight command', () => {
    const args = parseArgs(['--set-weight', 'acc-123']);
    assert.strictEqual(args['set-weight'], 'acc-123');
  });

  it('should identify set-strategy command', () => {
    const args = parseArgs(['--set-strategy', 'weighted']);
    assert.strictEqual(args['set-strategy'], 'weighted');
  });

  it('should identify validate-accounts command', () => {
    const args = parseArgs(['--validate-accounts']);
    assert.strictEqual(args['validate-accounts'], true);
  });

  it('should identify account-stats command', () => {
    const args = parseArgs(['--account-stats']);
    assert.strictEqual(args['account-stats'], true);
  });

  it('should identify message sending commands', () => {
    const messageArgs = parseArgs(['--message', 'hello']);
    assert.strictEqual(messageArgs.message, 'hello');

    const fileArgs = parseArgs(['--file', 'prompt.txt']);
    assert.strictEqual(fileArgs.file, 'prompt.txt');

    const batchArgs = parseArgs(['--batch', 'questions.txt']);
    assert.strictEqual(batchArgs.batch, 'questions.txt');
  });
});

describe('headless option detection', () => {
  it('should detect headed mode', () => {
    const args = parseArgs(['--login', '--headed']);
    const headless = !args.headed;
    assert.strictEqual(headless, false);
  });

  it('should be headless by default', () => {
    const args = parseArgs(['--login']);
    const headless = !args.headed;
    assert.strictEqual(headless, true);
  });
});

describe('Option value type checking', () => {
  it('should return string for flag with value', () => {
    const args = parseArgs(['--message', 'hello']);
    assert.strictEqual(typeof args.message, 'string');
  });

  it('should return boolean true for flag without value', () => {
    const args = parseArgs(['--login']);
    assert.strictEqual(typeof args.login, 'boolean');
    assert.strictEqual(args.login, true);
  });

  it('should return string for kebab-case flag with value', () => {
    const args = parseArgs(['--use-profile', '/path']);
    assert.strictEqual(typeof args['use-profile'], 'string');
  });

  it('should return boolean true for kebab-case flag without value', () => {
    const args = parseArgs(['--list-accounts']);
    assert.strictEqual(typeof args['list-accounts'], 'boolean');
    assert.strictEqual(args['list-accounts'], true);
  });
});

describe('Edge cases for argument parsing', () => {
  it('should handle very long values', () => {
    const longValue = 'a'.repeat(1000);
    const result = parseArgs(['--message', longValue]);
    assert.strictEqual(result.message.length, 1000);
  });

  it('should handle JSON-like values', () => {
    const result = parseArgs(['--message', '{"key": "value"}']);
    assert.strictEqual(result.message, '{"key": "value"}');
  });

  it('should handle URL values', () => {
    const result = parseArgs(['--use-profile', 'https://example.com/path']);
    assert.strictEqual(result['use-profile'], 'https://example.com/path');
  });

  it('should handle newline in values', () => {
    const result = parseArgs(['--message', 'line1\nline2']);
    assert.ok(result.message.includes('\n'));
  });

  it('should handle tab in values', () => {
    const result = parseArgs(['--message', 'col1\tcol2']);
    assert.ok(result.message.includes('\t'));
  });
});
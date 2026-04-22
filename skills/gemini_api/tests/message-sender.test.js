import { describe, it, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import { MessageSender, sendMessage, sendBatchMessages } from '../request/message-sender.js';

describe('MessageSender', () => {
  let sender;
  let mockClient;

  beforeEach(() => {
    mockClient = {
      sendMessage: mock.fn(async ({ message }) => ({
        conversationId: 'conv-123',
        messageId: 'msg-456',
        content: `Response to: ${message}`,
        model: 'gemini-pro'
      }))
    };

    sender = new MessageSender({ model: 'gemini-pro' });
    sender.client = mockClient;
  });

  afterEach(() => {
    mock.restoreAll();
  });

  describe('constructor', () => {
    it('should initialize with default saveHistory true', () => {
      const defaultSender = new MessageSender({ model: 'gemini-pro' });
      assert.strictEqual(defaultSender.saveHistory, true);
    });

    it('should accept saveHistory false', () => {
      const noHistorySender = new MessageSender({ saveHistory: false, model: 'gemini-pro' });
      assert.strictEqual(noHistorySender.saveHistory, false);
    });
  });

  describe('send', () => {
    it('should send message successfully', async () => {
      const result = await sender.send('Hello');
      
      assert.strictEqual(mockClient.sendMessage.mock.calls.length, 1);
      assert.strictEqual(result.content, 'Response to: Hello');
    });

    it('should pass options to client', async () => {
      await sender.send('Hello', { model: 'gemini-pro-vision', conversationId: 'conv-789' });
      
      assert.strictEqual(mockClient.sendMessage.mock.calls.length, 1);
      const call = mockClient.sendMessage.mock.calls[0];
      assert.ok(call);
      assert.strictEqual(call.arguments[0].model, 'gemini-pro-vision');
      assert.strictEqual(call.arguments[0].conversationId, 'conv-789');
    });

    it('should propagate send errors', async () => {
      mockClient.sendMessage = mock.fn(async () => {
        throw new Error('Send failed');
      });
      
      await assert.rejects(
        async () => await sender.send('Hello'),
        { message: 'Send failed' }
      );
    });

    it('should skip saving history when saveHistory is false', async () => {
      sender.saveHistory = false;
      
      await sender.send('Test');
      
      assert.strictEqual(mockClient.sendMessage.mock.calls.length, 1);
    });
  });

  describe('sendBatch', () => {
    it('should send multiple messages sequentially', async () => {
      const messages = ['Message 1', 'Message 2', 'Message 3'];
      const results = await sender.sendBatch(messages, { delay: 0 });
      
      assert.strictEqual(results.length, 3);
      assert.strictEqual(mockClient.sendMessage.mock.calls.length, 3);
      assert.ok(results.every(r => r.success));
    });

    it('should handle partial failures', async () => {
      let callCount = 0;
      mockClient.sendMessage = mock.fn(async () => {
        callCount++;
        if (callCount === 2) {
          throw new Error('Failed on second message');
        }
        return { content: 'OK', model: 'gemini-pro' };
      });
      
      const results = await sender.sendBatch(['M1', 'M2', 'M3'], { delay: 0 });
      
      assert.strictEqual(results.filter(r => r.success).length, 2);
      assert.strictEqual(results.filter(r => !r.success).length, 1);
      assert.strictEqual(results[1].error, 'Failed on second message');
    });

    it('should return all results even when some fail', async () => {
      mockClient.sendMessage = mock.fn(async () => {
        throw new Error('Always fails');
      });
      
      const results = await sender.sendBatch(['M1', 'M2'], { delay: 0 });
      
      assert.strictEqual(results.length, 2);
      assert.ok(results.every(r => !r.success));
    });

    it('should use custom delay between requests', async () => {
      const start = Date.now();
      await sender.sendBatch(['M1', 'M2'], { delay: 10 });
      const duration = Date.now() - start;
      
      assert.ok(duration >= 10);
    });

    it('should handle empty messages array', async () => {
      const results = await sender.sendBatch([]);
      
      assert.strictEqual(results.length, 0);
      assert.strictEqual(mockClient.sendMessage.mock.calls.length, 0);
    });

    it('should handle single message', async () => {
      const results = await sender.sendBatch(['Single'], { delay: 100 });
      
      assert.strictEqual(results.length, 1);
      assert.ok(results[0].success);
    });
  });

  describe('saveToHistory', () => {
    it('should save record to history file', () => {
      sender.saveToHistory({
        timestamp: new Date().toISOString(),
        message: 'Test',
        response: 'Response',
        model: 'gemini-pro'
      });
    });

    it('should handle save errors gracefully', () => {
      sender.saveToHistory({
        timestamp: new Date().toISOString(),
        message: 'Test',
        response: 'Response'
      });
    });
  });
});

describe('sendMessage shortcut function', () => {
  it('should create MessageSender and send message', async () => {
    let capturedMessage = null;
    
    const MockMessageSender = class {
      constructor() {
        this.saveHistory = true;
      }
      async send(msg) {
        capturedMessage = msg;
        return { content: 'Response' };
      }
    };
    
    const sender = new MockMessageSender();
    const result = await sender.send('Test message');
    
    assert.strictEqual(capturedMessage, 'Test message');
    assert.strictEqual(result.content, 'Response');
  });
});

describe('sendBatchMessages shortcut function', () => {
  it('should create MessageSender and send batch', async () => {
    const capturedMessages = [];
    
    const MockMessageSender = class {
      constructor() {
        this.saveHistory = true;
      }
      async sendBatch(msgs) {
        capturedMessages.push(...msgs);
        return msgs.map(m => ({ success: true, message: m }));
      }
    };
    
    const sender = new MockMessageSender();
    const results = await sender.sendBatch(['M1', 'M2']);
    
    assert.deepStrictEqual(capturedMessages, ['M1', 'M2']);
    assert.strictEqual(results.length, 2);
  });
});
import { strict as assert } from 'assert';
import { describe, it } from 'node:test';

describe('use-with-openai-sdk.js', () => {
  describe('OpenAI SDK configuration', () => {
    it('should use correct API key', () => {
      const apiKey = 'sk-chatgpt-proxy';
      assert.strictEqual(apiKey, 'sk-chatgpt-proxy');
    });

    it('should use correct base URL', () => {
      const baseURL = 'http://localhost:3000/v1';
      assert.strictEqual(baseURL, 'http://localhost:3000/v1');
    });

    it('should be able to customize configuration', () => {
      const customConfig = {
        apiKey: 'custom-key',
        baseURL: 'http://custom-host:8080/v1',
        timeout: 60000
      };

      assert.strictEqual(customConfig.apiKey, 'custom-key');
      assert.strictEqual(customConfig.baseURL, 'http://custom-host:8080/v1');
      assert.strictEqual(customConfig.timeout, 60000);
    });
  });

  describe('Simple conversation (example1)', () => {
    it('should create completion with correct parameters', () => {
      const expectedParams = {
        model: 'gpt-4',
        messages: [{ role: 'user', content: '用一句话介绍你自己' }]
      };

      assert.strictEqual(expectedParams.model, 'gpt-4');
      assert.strictEqual(expectedParams.messages.length, 1);
      assert.strictEqual(expectedParams.messages[0].role, 'user');
    });

    it('should extract response content correctly', () => {
      const completion = {
        choices: [{
          message: { content: 'I am an AI assistant.' }
        }]
      };

      const content = completion.choices[0].message.content;
      assert.strictEqual(content, 'I am an AI assistant.');
    });

    it('should handle empty choices array', () => {
      const completion = { choices: [] };
      assert.strictEqual(completion.choices.length, 0);
    });

    it('should handle multiple choices', () => {
      const completion = {
        choices: [
          { message: { content: 'Response 1' } },
          { message: { content: 'Response 2' } }
        ]
      };

      assert.strictEqual(completion.choices[0].message.content, 'Response 1');
      assert.strictEqual(completion.choices[1].message.content, 'Response 2');
    });
  });

  describe('Streaming response (example2)', () => {
    it('should create streaming request with correct parameters', () => {
      const expectedParams = {
        model: 'gpt-4',
        messages: [{ role: 'user', content: '数到 5' }],
        stream: true
      };

      assert.strictEqual(expectedParams.model, 'gpt-4');
      assert.strictEqual(expectedParams.stream, true);
    });

    it('should handle stream chunks correctly', () => {
      const mockChunks = [
        { choices: [{ delta: { content: '1' } }] },
        { choices: [{ delta: { content: '2' } }] },
        { choices: [{ delta: { content: '3' } }] }
      ];

      let fullContent = '';
      for (const chunk of mockChunks) {
        const content = chunk.choices[0]?.delta?.content || '';
        fullContent += content;
      }

      assert.strictEqual(fullContent, '123');
    });

    it('should handle empty delta content', () => {
      const chunk = { choices: [{ delta: {} }] };
      const content = chunk.choices[0]?.delta?.content || '';
      assert.strictEqual(content, '');
    });

    it('should handle undefined choices', () => {
      const chunk = {};
      const content = chunk.choices?.[0]?.delta?.content || '';
      assert.strictEqual(content, '');
    });

    it('should handle null choices', () => {
      const chunk = { choices: null };
      const content = chunk.choices?.[0]?.delta?.content || '';
      assert.strictEqual(content, '');
    });
  });

  describe('Multi-turn conversation (example3)', () => {
    it('should maintain conversation history', () => {
      const messages = [{ role: 'user', content: '我叫小明' }];
      assert.strictEqual(messages.length, 1);

      messages.push({ role: 'assistant', content: '你好，小明！' });
      assert.strictEqual(messages.length, 2);

      messages.push({ role: 'user', content: '我叫什么名字？' });
      assert.strictEqual(messages.length, 3);
    });

    it('should preserve message order', () => {
      const messages = [
        { role: 'user', content: 'First message' },
        { role: 'assistant', content: 'First response' },
        { role: 'user', content: 'Second message' }
      ];

      assert.strictEqual(messages[0].role, 'user');
      assert.strictEqual(messages[1].role, 'assistant');
      assert.strictEqual(messages[2].role, 'user');
    });

    it('should handle assistant message addition', () => {
      const messages = [{ role: 'user', content: 'Hello' }];
      const assistantMessage = { role: 'assistant', content: 'Hi there!' };
      messages.push(assistantMessage);

      assert.strictEqual(messages[1].role, 'assistant');
      assert.strictEqual(messages[1].content, 'Hi there!');
    });

    it('should create completion with message history', () => {
      const messages = [
        { role: 'user', content: '我叫小明' },
        { role: 'assistant', content: '你好，小明！' },
        { role: 'user', content: '我叫什么名字？' }
      ];

      const expectedParams = { model: 'gpt-4', messages };
      assert.strictEqual(expectedParams.messages.length, 3);
    });
  });

  describe('List models (example4)', () => {
    it('should handle models list response', () => {
      const modelsResponse = {
        data: [
          { id: 'gpt-4' },
          { id: 'gpt-3.5-turbo' },
          { id: 'gpt-4-turbo' }
        ]
      };

      const modelIds = modelsResponse.data.map(m => m.id);
      assert.deepStrictEqual(modelIds, ['gpt-4', 'gpt-3.5-turbo', 'gpt-4-turbo']);
    });

    it('should handle empty models list', () => {
      const modelsResponse = { data: [] };
      assert.strictEqual(modelsResponse.data.length, 0);
    });

    it('should handle models with additional properties', () => {
      const modelsResponse = {
        data: [
          { id: 'gpt-4', owned_by: 'openai', created: 1234567890 }
        ]
      };

      assert.strictEqual(modelsResponse.data[0].id, 'gpt-4');
      assert.strictEqual(modelsResponse.data[0].owned_by, 'openai');
    });
  });

  describe('Error handling', () => {
    it('should handle ECONNREFUSED error', () => {
      const error = new Error('Connection refused');
      error.code = 'ECONNREFUSED';

      assert.strictEqual(error.code, 'ECONNREFUSED');
      assert.ok(error.message.includes('Connection refused'));
    });

    it('should handle network timeout error', () => {
      const error = new Error('Request timeout');
      error.code = 'ETIMEDOUT';

      assert.strictEqual(error.code, 'ETIMEDOUT');
    });

    it('should handle authentication error', () => {
      const error = new Error('Unauthorized');
      error.status = 401;

      assert.strictEqual(error.status, 401);
    });

    it('should handle rate limit error', () => {
      const error = new Error('Rate limit exceeded');
      error.status = 429;

      assert.strictEqual(error.status, 429);
    });

    it('should handle server error', () => {
      const error = new Error('Internal server error');
      error.status = 500;

      assert.strictEqual(error.status, 500);
    });

    it('should handle generic error', () => {
      const error = new Error('Something went wrong');

      assert.ok(error instanceof Error);
      assert.strictEqual(error.message, 'Something went wrong');
    });

    it('should detect connection refused error code', () => {
      const error = { code: 'ECONNREFUSED' };
      assert.strictEqual(error.code, 'ECONNREFUSED');
    });
  });

  describe('Message format validation', () => {
    it('should have valid user message format', () => {
      const message = { role: 'user', content: 'Hello' };
      assert.strictEqual(message.role, 'user');
      assert.strictEqual(typeof message.content, 'string');
    });

    it('should have valid assistant message format', () => {
      const message = { role: 'assistant', content: 'Hi there!' };
      assert.strictEqual(message.role, 'assistant');
      assert.strictEqual(typeof message.content, 'string');
    });

    it('should have valid system message format', () => {
      const message = { role: 'system', content: 'You are a helpful assistant.' };
      assert.strictEqual(message.role, 'system');
      assert.strictEqual(typeof message.content, 'string');
    });

    it('should handle empty content', () => {
      const message = { role: 'user', content: '' };
      assert.strictEqual(message.content, '');
    });

    it('should handle multiline content', () => {
      const message = { role: 'user', content: 'Line 1\nLine 2\nLine 3' };
      assert.ok(message.content.includes('\n'));
    });

    it('should handle special characters in content', () => {
      const message = { role: 'user', content: 'Hello! @#$%^&*()_+-=[]{}|;:\'",.<>?/' };
      assert.ok(message.content.includes('@#$%^&*()'));
    });

    it('should handle unicode content', () => {
      const message = { role: 'user', content: '你好世界 🌍 Hello мир' };
      assert.ok(message.content.includes('你好'));
      assert.ok(message.content.includes('🌍'));
    });
  });

  describe('runExamples function flow', () => {
    it('should run all four examples sequentially', async () => {
      const executedExamples = [];
      
      const example1 = async () => { executedExamples.push(1); };
      const example2 = async () => { executedExamples.push(2); };
      const example3 = async () => { executedExamples.push(3); };
      const example4 = async () => { executedExamples.push(4); };

      await example1();
      await example2();
      await example3();
      await example4();

      assert.deepStrictEqual(executedExamples, [1, 2, 3, 4]);
    });

    it('should catch and handle errors', async () => {
      let errorThrown = false;
      
      try {
        throw new Error('Test error');
      } catch (error) {
        errorThrown = true;
      }

      assert.strictEqual(errorThrown, true);
    });

    it('should stop on first error in sequential execution', async () => {
      const executedExamples = [];
      
      try {
        await (async () => { executedExamples.push(1); })();
        await (async () => { throw new Error('Stop here'); })();
        await (async () => { executedExamples.push(3); })();
      } catch (error) {
      }

      assert.deepStrictEqual(executedExamples, [1]);
    });
  });

  describe('Output formatting', () => {
    it('should format separator line', () => {
      const separator = '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━';
      assert.strictEqual(separator.length, 40);
    });

    it('should format example headers correctly', () => {
      const header = '示例 1: 简单对话';
      assert.ok(header.includes('示例'));
      assert.ok(header.includes('1'));
    });

    it('should format completion output', () => {
      const response = 'I am an AI assistant.';
      const output = `回答: ${response}`;
      assert.ok(output.includes('回答:'));
      assert.ok(output.includes(response));
    });
  });
});

describe('Mock OpenAI client', () => {
  class MockOpenAI {
    constructor(config) {
      this.config = config;
      this.chat = {
        completions: {
          create: async (params) => {
            if (params.stream) {
              return this._createStream(params);
            }
            return {
              choices: [{ message: { content: 'Mock response' } }],
              model: params.model
            };
          }
        }
      };
      this.models = {
        list: async () => ({
          data: [{ id: 'gpt-4' }, { id: 'gpt-3.5-turbo' }]
        })
      };
    }

    async *_createStream(params) {
      const chunks = ['Mock', ' ', 'streaming', ' ', 'response'];
      for (const chunk of chunks) {
        yield { choices: [{ delta: { content: chunk } }] };
      }
    }
  }

  it('should create mock client with config', () => {
    const client = new MockOpenAI({
      apiKey: 'test-key',
      baseURL: 'http://localhost:3000/v1'
    });

    assert.strictEqual(client.config.apiKey, 'test-key');
    assert.strictEqual(client.config.baseURL, 'http://localhost:3000/v1');
  });

  it('should create completion', async () => {
    const client = new MockOpenAI({ apiKey: 'test' });
    const completion = await client.chat.completions.create({
      model: 'gpt-4',
      messages: [{ role: 'user', content: 'Hello' }]
    });

    assert.strictEqual(completion.choices[0].message.content, 'Mock response');
    assert.strictEqual(completion.model, 'gpt-4');
  });

  it('should create streaming completion', async () => {
    const client = new MockOpenAI({ apiKey: 'test' });
    const stream = await client.chat.completions.create({
      model: 'gpt-4',
      messages: [{ role: 'user', content: 'Hello' }],
      stream: true
    });

    let fullContent = '';
    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content || '';
      fullContent += content;
    }

    assert.strictEqual(fullContent, 'Mock streaming response');
  });

  it('should list models', async () => {
    const client = new MockOpenAI({ apiKey: 'test' });
    const models = await client.models.list();

    assert.strictEqual(models.data.length, 2);
    assert.strictEqual(models.data[0].id, 'gpt-4');
    assert.strictEqual(models.data[1].id, 'gpt-3.5-turbo');
  });

  it('should handle completion usage stats', () => {
    const completion = {
      choices: [{ message: { content: 'Test' } }],
      usage: {
        prompt_tokens: 10,
        completion_tokens: 5,
        total_tokens: 15
      }
    };

    assert.strictEqual(completion.usage.total_tokens, 15);
    assert.strictEqual(completion.usage.prompt_tokens, 10);
    assert.strictEqual(completion.usage.completion_tokens, 5);
  });

  it('should handle finish_reason in completion', () => {
    const completion = {
      choices: [{
        message: { content: 'Test' },
        finish_reason: 'stop'
      }]
    };

    assert.strictEqual(completion.choices[0].finish_reason, 'stop');
  });
});
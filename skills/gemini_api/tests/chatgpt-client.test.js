import { describe, it, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import { ChatGPTClient } from '../request/chatgpt-client.js';

const createMockResponse = (responseData, options = {}) => {
  const { status = 200, statusText = 'OK', shouldFail = false } = options;
  
  return {
    ok: status >= 200 && status < 300,
    status,
    statusText,
    text: async () => responseData,
    json: async () => JSON.parse(responseData)
  };
};

describe('ChatGPTClient', () => {
  let client;
  let mockSessionManager;
  let originalFetch;

  beforeEach(() => {
    mockSessionManager = {
      ensureValidSession: mock.fn(async () => ({ cookies: [] })),
      getCookies: mock.fn(() => 'session=test-cookie'),
      getUserAgent: mock.fn(() => 'TestUserAgent/1.0')
    };

    client = new ChatGPTClient({ model: 'gpt-4' });
    client.sessionManager = mockSessionManager;
    
    originalFetch = global.fetch;
  });

  afterEach(() => {
    global.fetch = originalFetch;
    mock.restoreAll();
  });

  describe('constructor', () => {
    it('should initialize with default values', () => {
      const defaultClient = new ChatGPTClient({ model: 'gpt-4' });
      assert.strictEqual(defaultClient.baseUrl, 'https://chatgpt.com');
      assert.strictEqual(defaultClient.apiUrl, 'https://chatgpt.com/backend-api');
    });

    it('should accept custom model option', () => {
      const customClient = new ChatGPTClient({ model: 'gpt-4-turbo' });
      assert.strictEqual(customClient.model, 'gpt-4-turbo');
    });
  });

  describe('ensureAuthenticated', () => {
    it('should call sessionManager.ensureValidSession', async () => {
      await client.ensureAuthenticated();
      assert.strictEqual(mockSessionManager.ensureValidSession.mock.calls.length, 1);
    });

    it('should propagate authentication errors', async () => {
      mockSessionManager.ensureValidSession = mock.fn(async () => {
        throw new Error('Auth failed');
      });
      
      await assert.rejects(
        async () => await client.ensureAuthenticated(),
        { message: 'Auth failed' }
      );
    });
  });

  describe('sendMessage', () => {
    it('should throw error when message is missing', async () => {
      await assert.rejects(
        async () => await client.sendMessage({}),
        { message: 'Message is required' }
      );
    });

    it('should throw error when message is empty string', async () => {
      await assert.rejects(
        async () => await client.sendMessage({ message: '' }),
        { message: 'Message is required' }
      );
    });

    it('should send message successfully', async () => {
      const sseResponse = `data: {"conversation_id":"conv-123","message":{"id":"msg-456","content":{"parts":["Hello response"]},"metadata":{"model_slug":"gpt-4"}}}
data: [DONE]`;
      
      global.fetch = mock.fn(async () => createMockResponse(sseResponse));
      
      const result = await client.sendMessage({ message: 'Hello' });
      
      assert.strictEqual(result.conversationId, 'conv-123');
      assert.strictEqual(result.messageId, 'msg-456');
      assert.strictEqual(result.content, 'Hello response');
      assert.strictEqual(result.model, 'gpt-4');
    });

    it('should handle 401 authentication error', async () => {
      global.fetch = mock.fn(async () => createMockResponse('', { status: 401, statusText: 'Unauthorized' }));
      
      await assert.rejects(
        async () => await client.sendMessage({ message: 'Hello' }),
        { message: 'Authentication failed. Please login again.' }
      );
    });

    it('should handle 403 authentication error', async () => {
      global.fetch = mock.fn(async () => createMockResponse('', { status: 403, statusText: 'Forbidden' }));
      
      await assert.rejects(
        async () => await client.sendMessage({ message: 'Hello' }),
        { message: 'Authentication failed. Please login again.' }
      );
    });

    it('should handle other HTTP errors', async () => {
      global.fetch = mock.fn(async () => createMockResponse('', { status: 500, statusText: 'Server Error' }));
      
      await assert.rejects(
        async () => await client.sendMessage({ message: 'Hello' }),
        { message: 'HTTP 500: Server Error' }
      );
    });

    it('should handle network errors', async () => {
      global.fetch = mock.fn(async () => {
        throw new Error('Network error');
      });
      
      await assert.rejects(
        async () => await client.sendMessage({ message: 'Hello' }),
        { message: 'Network error' }
      );
    });
  });

  describe('parseSSEResponse', () => {
    it('should parse SSE response with conversation_id', () => {
      const text = `data: {"conversation_id":"conv-123"}
data: [DONE]`;
      
      const result = client.parseSSEResponse(text);
      
      assert.strictEqual(result.conversationId, 'conv-123');
    });

    it('should parse SSE response with message content', () => {
      const text = `data: {"message":{"id":"msg-456","content":{"parts":["Hello"," World"]},"metadata":{"model_slug":"gpt-4"}}}
data: [DONE]`;
      
      const result = client.parseSSEResponse(text);
      
      assert.strictEqual(result.messageId, 'msg-456');
      assert.strictEqual(result.content, 'Hello World');
      assert.strictEqual(result.model, 'gpt-4');
    });

    it('should handle multiple data lines', () => {
      const text = `data: {"conversation_id":"conv-123"}
data: {"message":{"id":"msg-456","content":{"parts":["Response"]}}}
data: [DONE]`;
      
      const result = client.parseSSEResponse(text);
      
      assert.strictEqual(result.conversationId, 'conv-123');
      assert.strictEqual(result.messageId, 'msg-456');
      assert.strictEqual(result.content, 'Response');
    });

    it('should stop at [DONE]', () => {
      const text = `data: {"conversation_id":"conv-123"}
data: [DONE]
data: {"conversation_id":"ignored"}`;
      
      const result = client.parseSSEResponse(text);
      
      assert.strictEqual(result.conversationId, 'conv-123');
    });

    it('should handle empty lines', () => {
      const text = `data: {"conversation_id":"conv-123"}

data: [DONE]
`;
      
      const result = client.parseSSEResponse(text);
      
      assert.strictEqual(result.conversationId, 'conv-123');
    });

    it('should handle invalid JSON gracefully', () => {
      const text = `data: not valid json
data: {"conversation_id":"conv-123"}
data: [DONE]`;
      
      const result = client.parseSSEResponse(text);
      
      assert.strictEqual(result.conversationId, 'conv-123');
    });

    it('should return default values for empty response', () => {
      const result = client.parseSSEResponse('data: [DONE]');
      
      assert.strictEqual(result.conversationId, null);
      assert.strictEqual(result.messageId, null);
      assert.strictEqual(result.content, '');
      assert.strictEqual(result.model, null);
    });

    it('should include rawResponse', () => {
      const text = 'data: [DONE]';
      const result = client.parseSSEResponse(text);
      
      assert.strictEqual(result.rawResponse, text);
    });
  });

  describe('getConversations', () => {
    it('should fetch conversations with default options', async () => {
      const response = JSON.stringify({
        items: [{ id: '1', title: 'Test' }],
        total: 1,
        limit: 20,
        offset: 0,
        has_missing_conversations: false
      });
      global.fetch = mock.fn(async () => createMockResponse(response));
      
      const result = await client.getConversations();
      
      assert.strictEqual(result.items.length, 1);
      assert.strictEqual(result.total, 1);
      assert.strictEqual(result.hasMore, false);
    });

    it('should handle HTTP errors', async () => {
      global.fetch = mock.fn(async () => createMockResponse('', { status: 404, statusText: 'Not Found' }));
      
      await assert.rejects(
        async () => await client.getConversations(),
        { message: 'HTTP 404: Not Found' }
      );
    });

    it('should handle network errors', async () => {
      global.fetch = mock.fn(async () => {
        throw new Error('Connection refused');
      });
      
      await assert.rejects(
        async () => await client.getConversations(),
        { message: 'Connection refused' }
      );
    });
  });

  describe('getConversation', () => {
    it('should fetch specific conversation', async () => {
      const response = JSON.stringify({ id: 'conv-123', title: 'Test Conversation' });
      global.fetch = mock.fn(async () => createMockResponse(response));
      
      const result = await client.getConversation('conv-123');
      
      assert.strictEqual(result.id, 'conv-123');
      assert.strictEqual(result.title, 'Test Conversation');
    });

    it('should handle HTTP errors', async () => {
      global.fetch = mock.fn(async () => createMockResponse('', { status: 404, statusText: 'Not Found' }));
      
      await assert.rejects(
        async () => await client.getConversation('invalid-id'),
        { message: 'HTTP 404: Not Found' }
      );
    });
  });

  describe('deleteConversation', () => {
    it('should delete conversation successfully', async () => {
      global.fetch = mock.fn(async () => createMockResponse('', { status: 200 }));
      
      const result = await client.deleteConversation('conv-123');
      
      assert.strictEqual(result.success, true);
      assert.strictEqual(result.conversationId, 'conv-123');
    });

    it('should handle delete errors', async () => {
      global.fetch = mock.fn(async () => createMockResponse('', { status: 500, statusText: 'Server Error' }));
      
      await assert.rejects(
        async () => await client.deleteConversation('conv-123'),
        { message: 'HTTP 500: Server Error' }
      );
    });
  });

  describe('clearConversations', () => {
    it('should clear all conversations successfully', async () => {
      global.fetch = mock.fn(async () => createMockResponse('', { status: 200 }));
      
      const result = await client.clearConversations();
      
      assert.strictEqual(result.success, true);
    });

    it('should handle clear errors', async () => {
      global.fetch = mock.fn(async () => createMockResponse('', { status: 500, statusText: 'Server Error' }));
      
      await assert.rejects(
        async () => await client.clearConversations(),
        { message: 'HTTP 500: Server Error' }
      );
    });
  });

  describe('renameConversation', () => {
    it('should rename conversation successfully', async () => {
      global.fetch = mock.fn(async () => createMockResponse('', { status: 200 }));
      
      const result = await client.renameConversation('conv-123', 'New Title');
      
      assert.strictEqual(result.success, true);
      assert.strictEqual(result.conversationId, 'conv-123');
      assert.strictEqual(result.title, 'New Title');
    });

    it('should handle rename errors', async () => {
      global.fetch = mock.fn(async () => createMockResponse('', { status: 404, statusText: 'Not Found' }));
      
      await assert.rejects(
        async () => await client.renameConversation('conv-123', 'New Title'),
        { message: 'HTTP 404: Not Found' }
      );
    });
  });

  describe('getModels', () => {
    it('should fetch models successfully', async () => {
      const response = JSON.stringify({
        models: [
          { slug: 'gpt-4', title: 'GPT-4' },
          { slug: 'gpt-3.5-turbo', title: 'GPT-3.5 Turbo' }
        ]
      });
      global.fetch = mock.fn(async () => createMockResponse(response));
      
      const result = await client.getModels();
      
      assert.strictEqual(result.length, 2);
      assert.strictEqual(result[0].slug, 'gpt-4');
      assert.strictEqual(result[1].slug, 'gpt-3.5-turbo');
    });

    it('should handle models fetch errors', async () => {
      global.fetch = mock.fn(async () => createMockResponse('', { status: 500, statusText: 'Server Error' }));
      
      await assert.rejects(
        async () => await client.getModels(),
        { message: 'HTTP 500: Server Error' }
      );
    });
  });

  describe('getAccountInfo', () => {
    it('should fetch account info successfully', async () => {
      const response = JSON.stringify({ email: 'test@example.com', name: 'Test User' });
      global.fetch = mock.fn(async () => createMockResponse(response));
      
      const result = await client.getAccountInfo();
      
      assert.strictEqual(result.email, 'test@example.com');
      assert.strictEqual(result.name, 'Test User');
    });

    it('should handle account info fetch errors', async () => {
      global.fetch = mock.fn(async () => createMockResponse('', { status: 401, statusText: 'Unauthorized' }));
      
      await assert.rejects(
        async () => await client.getAccountInfo(),
        { message: 'HTTP 401: Unauthorized' }
      );
    });
  });

  describe('searchConversations', () => {
    it('should search conversations successfully', async () => {
      const response = JSON.stringify({
        items: [{ id: '1', title: 'Test Result' }]
      });
      global.fetch = mock.fn(async () => createMockResponse(response));
      
      const result = await client.searchConversations('test query');
      
      assert.strictEqual(result.length, 1);
      assert.strictEqual(result[0].title, 'Test Result');
    });

    it('should handle search errors', async () => {
      global.fetch = mock.fn(async () => createMockResponse('', { status: 500, statusText: 'Server Error' }));
      
      await assert.rejects(
        async () => await client.searchConversations('test'),
        { message: 'HTTP 500: Server Error' }
      );
    });
  });

  describe('generateId', () => {
    it('should generate valid UUID format', () => {
      const id = client.generateId();
      
      assert.ok(typeof id === 'string');
      assert.strictEqual(id.length, 36);
      assert.ok(/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(id));
    });

    it('should generate unique IDs', () => {
      const ids = new Set();
      for (let i = 0; i < 100; i++) {
        ids.add(client.generateId());
      }
      assert.strictEqual(ids.size, 100);
    });

    it('should have correct version (4) in UUID', () => {
      const id = client.generateId();
      assert.strictEqual(id.charAt(14), '4');
    });

    it('should have correct variant in UUID', () => {
      const id = client.generateId();
      const variantChar = id.charAt(19);
      assert.ok(['8', '9', 'a', 'b'].includes(variantChar));
    });
  });
});
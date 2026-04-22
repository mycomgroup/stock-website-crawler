import { describe, it, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import { GeminiClient } from '../request/gemini-client.js';

describe('GeminiClient', () => {
  let client;
  let mockSessionManager;
  let mockSecureClient;

  beforeEach(() => {
    mockSessionManager = {
      ensureValidSession: mock.fn(async () => ({ cookies: [] })),
      getCookies: mock.fn(() => 'session=test'),
    };

    mockSecureClient = {
      request: mock.fn(async () => JSON.stringify({
        conversation_id: 'conv-123',
        message_id: 'msg-123',
        text: 'Hello, this is a test response.'
      })),
      baseUrl: 'https://gemini.google.com',
      maxRequestsPerMinute: 10
    };

    client = new GeminiClient({ model: 'gemini-pro' });
    client.sessionManager = mockSessionManager;
    client.secureClient = mockSecureClient;
  });

  afterEach(() => {
    mock.restoreAll();
  });

  describe('constructor', () => {
    it('should initialize with default values', () => {
      const defaultClient = new GeminiClient({ model: 'gemini-pro' });
      assert.strictEqual(defaultClient.baseUrl, 'https://gemini.google.com');
      assert.strictEqual(defaultClient.apiUrl, 'https://gemini.google.com/api');
      assert.strictEqual(defaultClient.model, 'gemini-pro');
    });

    it('should accept custom model option', () => {
      const customClient = new GeminiClient({ model: 'gemini-pro-vision' });
      assert.strictEqual(customClient.model, 'gemini-pro-vision');
    });

    it('should initialize SecureHttpClient', () => {
      assert.ok(client.secureClient);
    });
  });

  describe('ensureAuthenticated', () => {
    it('should call sessionManager.ensureValidSession', async () => {
      await client.ensureAuthenticated();
      assert.strictEqual(mockSessionManager.ensureValidSession.mock.calls.length, 1);
    });

    it('should propagate authentication errors', async () => {
      const authError = new Error('Authentication failed');
      mockSessionManager.ensureValidSession = mock.fn(async () => { throw authError; });
      
      await assert.rejects(
        async () => await client.ensureAuthenticated(),
        { message: 'Authentication failed' }
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
      const result = await client.sendMessage({ message: 'Hello Gemini' });
      
      assert.strictEqual(mockSessionManager.ensureValidSession.mock.calls.length, 1);
      assert.strictEqual(mockSecureClient.request.mock.calls.length, 1);
      assert.strictEqual(result.conversationId, 'conv-123');
      assert.strictEqual(result.messageId, 'msg-123');
      assert.strictEqual(result.content, 'Hello, this is a test response.');
    });

    it('should use custom model when provided', async () => {
      const result = await client.sendMessage({ 
        message: 'Hello', 
        model: 'gemini-pro-vision' 
      });
      
      assert.strictEqual(result.model, 'gemini-pro-vision');
    });

    it('should use conversationId when provided', async () => {
      await client.sendMessage({ 
        message: 'Hello', 
        conversationId: 'existing-conv-456' 
      });
      
      assert.strictEqual(mockSecureClient.request.mock.calls.length, 1);
    });

    it('should handle authentication errors (401)', async () => {
      mockSecureClient.request = mock.fn(async () => {
        throw new Error('HTTP 401: Unauthorized');
      });
      
      await assert.rejects(
        async () => await client.sendMessage({ message: 'Hello' }),
        { message: 'Authentication failed. Please login again.' }
      );
    });

    it('should handle authentication errors (403)', async () => {
      mockSecureClient.request = mock.fn(async () => {
        throw new Error('HTTP 403: Forbidden');
      });
      
      await assert.rejects(
        async () => await client.sendMessage({ message: 'Hello' }),
        { message: 'Authentication failed. Please login again.' }
      );
    });

    it('should propagate other errors', async () => {
      mockSecureClient.request = mock.fn(async () => {
        throw new Error('Network error');
      });
      
      await assert.rejects(
        async () => await client.sendMessage({ message: 'Hello' }),
        { message: 'Network error' }
      );
    });

    it('should handle response without conversation_id', async () => {
      mockSecureClient.request = mock.fn(async () => JSON.stringify({
        text: 'Response without conversation id'
      }));
      
      const result = await client.sendMessage({ message: 'Hello' });
      assert.strictEqual(result.conversationId, null);
      assert.ok(result.messageId);
    });

    it('should handle response with nested structure', async () => {
      mockSecureClient.request = mock.fn(async () => JSON.stringify({
        conversation_id: 'conv-789',
        response: 'Nested response content'
      }));
      
      const result = await client.sendMessage({ message: 'Hello' });
      assert.strictEqual(result.content, 'Nested response content');
    });
  });

  describe('getConversations', () => {
    it('should fetch conversations with default pagination', async () => {
      mockSecureClient.request = mock.fn(async () => JSON.stringify({
        conversations: [{ id: '1', title: 'Test' }],
        total: 1
      }));
      
      const result = await client.getConversations();
      
      assert.strictEqual(mockSessionManager.ensureValidSession.mock.calls.length, 1);
      assert.strictEqual(result.items.length, 1);
      assert.strictEqual(result.total, 1);
      assert.strictEqual(result.limit, 20);
      assert.strictEqual(result.offset, 0);
    });

    it('should fetch conversations with custom pagination', async () => {
      mockSecureClient.request = mock.fn(async () => JSON.stringify({
        conversations: [],
        total: 100
      }));
      
      const result = await client.getConversations({ offset: 10, limit: 5 });
      
      assert.strictEqual(result.offset, 10);
      assert.strictEqual(result.limit, 5);
    });

    it('should handle empty conversations response', async () => {
      mockSecureClient.request = mock.fn(async () => JSON.stringify({}));
      
      const result = await client.getConversations();
      
      assert.deepStrictEqual(result.items, []);
      assert.strictEqual(result.total, 0);
    });

    it('should propagate getConversations errors', async () => {
      mockSecureClient.request = mock.fn(async () => {
        throw new Error('Failed to fetch conversations');
      });
      
      await assert.rejects(
        async () => await client.getConversations(),
        { message: 'Failed to fetch conversations' }
      );
    });
  });

  describe('getConversation', () => {
    it('should fetch specific conversation', async () => {
      mockSecureClient.request = mock.fn(async () => JSON.stringify({
        id: 'conv-123',
        title: 'Test Conversation',
        messages: []
      }));
      
      const result = await client.getConversation('conv-123');
      
      assert.strictEqual(result.id, 'conv-123');
      assert.strictEqual(result.title, 'Test Conversation');
    });

    it('should propagate getConversation errors', async () => {
      mockSecureClient.request = mock.fn(async () => {
        throw new Error('Conversation not found');
      });
      
      await assert.rejects(
        async () => await client.getConversation('invalid-id'),
        { message: 'Conversation not found' }
      );
    });
  });

  describe('deleteConversation', () => {
    it('should delete conversation successfully', async () => {
      mockSecureClient.request = mock.fn(async () => '');
      
      const result = await client.deleteConversation('conv-123');
      
      assert.strictEqual(result.success, true);
      assert.strictEqual(result.conversationId, 'conv-123');
    });

    it('should propagate deleteConversation errors', async () => {
      mockSecureClient.request = mock.fn(async () => {
        throw new Error('Delete failed');
      });
      
      await assert.rejects(
        async () => await client.deleteConversation('conv-123'),
        { message: 'Delete failed' }
      );
    });
  });

  describe('getModels', () => {
    it('should return model list', async () => {
      const models = await client.getModels();
      
      assert.ok(Array.isArray(models));
      assert.strictEqual(models.length, 2);
      assert.strictEqual(models[0].slug, 'gemini-pro');
      assert.strictEqual(models[1].slug, 'gemini-pro-vision');
    });

    it('should include model details', async () => {
      const models = await client.getModels();
      
      assert.ok(models[0].title);
      assert.ok(models[0].description);
      assert.ok(models[0].max_tokens);
    });
  });

  describe('getAccountInfo', () => {
    it('should fetch account info successfully', async () => {
      mockSecureClient.request = mock.fn(async () => JSON.stringify({
        email: 'test@example.com',
        name: 'Test User'
      }));
      
      const result = await client.getAccountInfo();
      
      assert.strictEqual(result.email, 'test@example.com');
      assert.strictEqual(result.name, 'Test User');
    });

    it('should propagate getAccountInfo errors', async () => {
      mockSecureClient.request = mock.fn(async () => {
        throw new Error('Account info fetch failed');
      });
      
      await assert.rejects(
        async () => await client.getAccountInfo(),
        { message: 'Account info fetch failed' }
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
  });
});
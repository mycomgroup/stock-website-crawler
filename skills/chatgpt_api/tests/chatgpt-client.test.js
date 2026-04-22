import { describe, it, beforeEach, mock } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

describe('ChatGPTClient - utility methods', () => {
  describe('generateId', () => {
    it('should generate UUID format', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js');
      
      const client = new ChatGPTClient();
      const id = client.generateId();
      
      assert.strictEqual(id.length, 36);
      assert.ok(id.includes('-'));
    });

    it('should generate unique IDs', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      const ids = new Set();
      
      for (let i = 0; i < 100; i++) {
        ids.add(client.generateId());
      }
      
      assert.strictEqual(ids.size, 100);
    });

    it('should have version 4 in UUID', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      const id = client.generateId();
      
      assert.strictEqual(id.charAt(14), '4');
    });

    it('should have valid variant in UUID', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      const id = client.generateId();
      
      const variantChar = id.charAt(19);
      assert.ok(['8', '9', 'a', 'b'].includes(variantChar));
    });
  });

  describe('parseSSEResponse', () => {
    it('should parse valid SSE response', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      const text = 'data: {"conversation_id":"conv-1","message":{"id":"msg-1","content":{"parts":["Hello"]},"metadata":{"model_slug":"gpt-4"}}}\ndata: [DONE]';
      
      const result = client.parseSSEResponse(text);
      
      assert.strictEqual(result.conversationId, 'conv-1');
      assert.strictEqual(result.messageId, 'msg-1');
      assert.strictEqual(result.content, 'Hello');
      assert.strictEqual(result.model, 'gpt-4');
    });

    it('should handle empty response', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      const result = client.parseSSEResponse('');
      
      assert.strictEqual(result.conversationId, null);
      assert.strictEqual(result.messageId, null);
      assert.strictEqual(result.content, '');
    });

    it('should handle response with only [DONE]', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      const result = client.parseSSEResponse('data: [DONE]');
      
      assert.strictEqual(result.conversationId, null);
      assert.strictEqual(result.messageId, null);
      assert.strictEqual(result.content, '');
    });

    it('should skip invalid JSON lines', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      const text = 'data: invalid json\ndata: {"conversation_id":"conv-2"}\ndata: [DONE]';
      
      const result = client.parseSSEResponse(text);
      
      assert.strictEqual(result.conversationId, 'conv-2');
    });

    it('should handle multiple content parts', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      const text = 'data: {"message":{"content":{"parts":["Hello"," World"]}}}\ndata: [DONE]';
      
      const result = client.parseSSEResponse(text);
      
      assert.strictEqual(result.content, 'Hello World');
    });

    it('should handle response without message', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      const text = 'data: {"conversation_id":"conv-3"}\ndata: [DONE]';
      
      const result = client.parseSSEResponse(text);
      
      assert.strictEqual(result.conversationId, 'conv-3');
      assert.strictEqual(result.messageId, null);
      assert.strictEqual(result.content, '');
    });

    it('should preserve raw response', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      const text = 'data: {"test":1}\ndata: [DONE]';
      
      const result = client.parseSSEResponse(text);
      
      assert.strictEqual(result.rawResponse, text);
    });

    it('should handle lines without data prefix', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      const text = ': comment line\ndata: {"conversation_id":"conv-4"}\ndata: [DONE]';
      
      const result = client.parseSSEResponse(text);
      
      assert.strictEqual(result.conversationId, 'conv-4');
    });

    it('should handle multiple messages', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      const text = 'data: {"conversation_id":"conv"}\ndata: {"message":{"id":"m1","content":{"parts":["Part1"]}}}\ndata: {"message":{"id":"m2","content":{"parts":["Part2"]}}}\ndata: [DONE]';
      
      const result = client.parseSSEResponse(text);
      
      assert.strictEqual(result.content, 'Part2');
    });
  });

  describe('isHtmlProtectionResponse', () => {
    it('should return true for HTML content type', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      const response = { headers: new Map([['content-type', 'text/html']]) };
      
      assert.strictEqual(client.isHtmlProtectionResponse(response), true);
    });

    it('should return true for HTML content starting with <!doctype', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      const response = { headers: new Map([['content-type', 'text/plain']]) };
      const text = '<!doctype html><html>';
      
      assert.strictEqual(client.isHtmlProtectionResponse(response, text), true);
    });

    it('should return true for HTML content starting with <html', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      const response = { headers: new Map() };
      const text = '<html><body>';
      
      assert.strictEqual(client.isHtmlProtectionResponse(response, text), true);
    });

    it('should return false for JSON content type', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      const response = { headers: new Map([['content-type', 'application/json']]) };
      const text = '{"data": "value"}';
      
      assert.strictEqual(client.isHtmlProtectionResponse(response, text), false);
    });

    it('should return false for empty response text', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      const response = { headers: new Map() };
      const text = '';
      
      assert.strictEqual(client.isHtmlProtectionResponse(response, text), false);
    });

    it('should only check first 200 characters', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      const response = { headers: new Map() };
      const text = 'normal text'.repeat(50) + '<!doctype html>';
      
      assert.strictEqual(client.isHtmlProtectionResponse(response, text), false);
    });

    it('should handle case insensitive HTML detection', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      const response = { headers: new Map() };
      const text = '<!DOCTYPE HTML>';
      
      assert.strictEqual(client.isHtmlProtectionResponse(response, text), true);
    });
  });

  describe('constructor', () => {
    it('should initialize with default options', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      
      assert.strictEqual(client.baseUrl, 'https://chatgpt.com');
      assert.strictEqual(client.apiUrl, 'https://chatgpt.com/backend-api');
      assert.ok(client.sessionManager);
      assert.ok(client.secureClient);
    });

    it('should use default model from ENV', async () => {
      const { ChatGPTClient } = await import('../request/chatgpt-client.js?cachebuster=' + Date.now());
      
      const client = new ChatGPTClient();
      
      assert.ok(client.model);
    });
  });
});
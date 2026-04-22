import { describe, it, beforeEach, mock } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { EventEmitter } from 'node:events';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function createMockRequest(options = {}) {
  const req = new EventEmitter();
  req.method = options.method || 'GET';
  req.url = options.url || '/';
  req.headers = options.headers || {};
  
  if (options.body) {
    req._body = JSON.stringify(options.body);
  }
  
  return req;
}

function createMockResponse() {
  const res = new EventEmitter();
  res.writeHead = mock.fn((statusCode, headers) => {
    res._statusCode = statusCode;
    res._headers = headers;
  });
  res.write = mock.fn((data) => {
    res._writtenData = (res._writtenData || '') + data;
  });
  res.end = mock.fn((data) => {
    res._ended = true;
    if (data) res._endedData = data;
  });
  return res;
}

describe('OpenAI Server - utility functions', () => {
  describe('parseBody simulation', () => {
    it('should parse JSON body from request', async () => {
      const req = createMockRequest();
      req._body = '{"test": "value"}';
      
      const parseBody = async (req) => {
        return new Promise((resolve, reject) => {
          let body = '';
          req.on('data', chunk => { body += chunk.toString(); });
          req.on('end', () => {
            try { resolve(JSON.parse(body)); } catch (e) { reject(e); }
          });
          req.on('error', reject);
          req.emit('data', req._body);
          req.emit('end');
        });
      };
      
      const result = await parseBody(req);
      assert.deepStrictEqual(result, { test: 'value' });
    });

    it('should reject on invalid JSON', async () => {
      const req = createMockRequest();
      req._body = 'invalid json';
      
      const parseBody = async (req) => {
        return new Promise((resolve, reject) => {
          let body = '';
          req.on('data', chunk => { body += chunk.toString(); });
          req.on('end', () => {
            try { resolve(JSON.parse(body)); } catch (e) { reject(e); }
          });
          req.on('error', reject);
          req.emit('data', req._body);
          req.emit('end');
        });
      };
      
      await assert.rejects(async () => await parseBody(req), SyntaxError);
    });

    it('should handle chunked data', async () => {
      const req = createMockRequest();
      
      const parseBody = async (req) => {
        return new Promise((resolve, reject) => {
          let body = '';
          req.on('data', chunk => { body += chunk.toString(); });
          req.on('end', () => {
            try { resolve(JSON.parse(body)); } catch (e) { reject(e); }
          });
          req.on('error', reject);
          req.emit('data', '{"part1":');
          req.emit('data', '"value"}');
          req.emit('end');
        });
      };
      
      const result = await parseBody(req);
      assert.deepStrictEqual(result, { part1: 'value' });
    });
  });

  describe('verifyApiKey simulation', () => {
    const verifyApiKey = (req, apiKey) => {
      const authHeader = req.headers.authorization;
      if (!authHeader) return false;
      const token = authHeader.replace('Bearer ', '');
      return token === apiKey;
    };

    it('should return false when no authorization header', () => {
      const req = createMockRequest({ headers: {} });
      assert.strictEqual(verifyApiKey(req, 'test-api-key'), false);
    });

    it('should return true for valid API key', () => {
      const req = createMockRequest({ headers: { authorization: 'Bearer test-api-key' } });
      assert.strictEqual(verifyApiKey(req, 'test-api-key'), true);
    });

    it('should return false for invalid API key', () => {
      const req = createMockRequest({ headers: { authorization: 'Bearer wrong-key' } });
      assert.strictEqual(verifyApiKey(req, 'test-api-key'), false);
    });

    it('should handle authorization header without Bearer prefix', () => {
      const req = createMockRequest({ headers: { authorization: 'test-api-key' } });
      assert.strictEqual(verifyApiKey(req, 'test-api-key'), true);
    });

    it('should be case sensitive', () => {
      const req = createMockRequest({ headers: { authorization: 'Bearer TEST-API-KEY' } });
      assert.strictEqual(verifyApiKey(req, 'test-api-key'), false);
    });
  });

  describe('sendJSON simulation', () => {
    const sendJSON = (res, statusCode, data) => {
      res.writeHead(statusCode, {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      });
      res.end(JSON.stringify(data));
    };

    it('should write correct headers', () => {
      const res = createMockResponse();
      
      sendJSON(res, 200, { status: 'ok' });
      
      assert.strictEqual(res._statusCode, 200);
      assert.strictEqual(res._headers['Content-Type'], 'application/json');
    });

    it('should end with JSON stringified data', () => {
      const res = createMockResponse();
      
      sendJSON(res, 200, { message: 'success' });
      
      assert.strictEqual(res._ended, true);
      assert.strictEqual(res._endedData, '{"message":"success"}');
    });

    it('should handle 400 status', () => {
      const res = createMockResponse();
      
      sendJSON(res, 400, { error: { message: 'Bad request' } });
      
      assert.strictEqual(res._statusCode, 400);
    });

    it('should handle 500 status', () => {
      const res = createMockResponse();
      
      sendJSON(res, 500, { error: { message: 'Server error' } });
      
      assert.strictEqual(res._statusCode, 500);
    });

    it('should handle null data', () => {
      const res = createMockResponse();
      
      sendJSON(res, 200, null);
      
      assert.strictEqual(res._endedData, 'null');
    });

    it('should handle array data', () => {
      const res = createMockResponse();
      
      sendJSON(res, 200, [1, 2, 3]);
      
      assert.strictEqual(res._endedData, '[1,2,3]');
    });
  });

  describe('sendSSE simulation', () => {
    const sendSSE = (res, data) => {
      res.write(`data: ${JSON.stringify(data)}\n\n`);
    };

    it('should write SSE formatted data', () => {
      const res = createMockResponse();
      
      sendSSE(res, { id: 'test', content: 'message' });
      
      assert.ok(res._writtenData.includes('data: '));
      assert.ok(res._writtenData.includes('\n\n'));
    });

    it('should JSON stringify the data', () => {
      const res = createMockResponse();
      
      sendSSE(res, { test: 'value' });
      
      assert.ok(res._writtenData.includes('"test":"value"'));
    });

    it('should handle simple string data', () => {
      const res = createMockResponse();
      
      sendSSE(res, 'simple message');
      
      assert.strictEqual(res._writtenData, 'data: "simple message"\n\n');
    });

    it('should handle numeric data', () => {
      const res = createMockResponse();
      
      sendSSE(res, 123);
      
      assert.strictEqual(res._writtenData, 'data: 123\n\n');
    });
  });

  describe('handleChatCompletions simulation', () => {
    const createHandleChatCompletions = () => {
      return async (req, res, body) => {
        const { messages, model = 'gpt-4', stream = false } = body;
        
        if (!messages || !Array.isArray(messages)) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: { message: 'messages is required', type: 'invalid_request_error' } }));
          return;
        }
        
        const userMessages = messages.filter(m => m.role === 'user');
        const lastMessage = userMessages[userMessages.length - 1];
        
        if (!lastMessage) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: { message: 'No user message found', type: 'invalid_request_error' } }));
          return;
        }
        
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
          id: 'chatcmpl-test',
          model,
          choices: [{ message: { role: 'assistant', content: 'Test response' }, finish_reason: 'stop' }]
        }));
      };
    };

    it('should return 400 when messages is missing', async () => {
      const req = createMockRequest({ method: 'POST', url: '/v1/chat/completions' });
      const res = createMockResponse();
      
      const handler = createHandleChatCompletions();
      await handler(req, res, {});
      
      assert.strictEqual(res._statusCode, 400);
    });

    it('should return 400 when messages is not an array', async () => {
      const req = createMockRequest({ method: 'POST', url: '/v1/chat/completions' });
      const res = createMockResponse();
      
      const handler = createHandleChatCompletions();
      await handler(req, res, { messages: 'not an array' });
      
      assert.strictEqual(res._statusCode, 400);
    });

    it('should return 400 when no user message found', async () => {
      const req = createMockRequest({ method: 'POST', url: '/v1/chat/completions' });
      const res = createMockResponse();
      
      const handler = createHandleChatCompletions();
      await handler(req, res, { messages: [{ role: 'system', content: 'system msg' }] });
      
      assert.strictEqual(res._statusCode, 400);
    });

    it('should handle valid request', async () => {
      const req = createMockRequest({ method: 'POST', url: '/v1/chat/completions' });
      const res = createMockResponse();
      
      const handler = createHandleChatCompletions();
      await handler(req, res, { messages: [{ role: 'user', content: 'Hello' }] });
      
      assert.strictEqual(res._statusCode, 200);
      const data = JSON.parse(res._endedData);
      assert.strictEqual(data.choices[0].message.role, 'assistant');
    });
  });

  describe('handleModels simulation', () => {
    const createHandleModels = () => {
      return async (req, res) => {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
          object: 'list',
          data: [
            { id: 'gpt-4', object: 'model', owned_by: 'openai' },
            { id: 'gpt-3.5-turbo', object: 'model', owned_by: 'openai' }
          ]
        }));
      };
    };

    it('should return models list', async () => {
      const req = createMockRequest({ method: 'GET', url: '/v1/models' });
      const res = createMockResponse();
      
      const handler = createHandleModels();
      await handler(req, res);
      
      assert.strictEqual(res._statusCode, 200);
      const data = JSON.parse(res._endedData);
      assert.strictEqual(data.object, 'list');
      assert.strictEqual(data.data.length, 2);
    });
  });

  describe('handleRequest simulation', () => {
    const createHandleRequest = (apiKey) => {
      return async (req, res) => {
        const { method, url } = req;
        
        if (method === 'OPTIONS') {
          res.writeHead(200, { 'Access-Control-Allow-Origin': '*' });
          res.end();
          return;
        }
        
        const authHeader = req.headers.authorization;
        if (!authHeader || authHeader.replace('Bearer ', '') !== apiKey) {
          res.writeHead(401, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: { message: 'Invalid API key' } }));
          return;
        }
        
        if (url === '/health' && method === 'GET') {
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ status: 'ok' }));
          return;
        }
        
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: { message: 'Not found' } }));
      };
    };

    it('should handle OPTIONS request (CORS preflight)', async () => {
      const req = createMockRequest({ method: 'OPTIONS' });
      const res = createMockResponse();
      
      const handler = createHandleRequest('test-api-key');
      await handler(req, res);
      
      assert.strictEqual(res._statusCode, 200);
    });

    it('should return 401 for wrong API key', async () => {
      const req = createMockRequest({ 
        method: 'GET', 
        url: '/v1/models',
        headers: { authorization: 'Bearer wrong-key' }
      });
      const res = createMockResponse();
      
      const handler = createHandleRequest('test-api-key');
      await handler(req, res);
      
      assert.strictEqual(res._statusCode, 401);
    });

    it('should handle /health endpoint', async () => {
      const req = createMockRequest({ 
        method: 'GET', 
        url: '/health',
        headers: { authorization: 'Bearer test-api-key' }
      });
      const res = createMockResponse();
      
      const handler = createHandleRequest('test-api-key');
      await handler(req, res);
      
      assert.strictEqual(res._statusCode, 200);
      const data = JSON.parse(res._endedData);
      assert.strictEqual(data.status, 'ok');
    });

    it('should return 404 for unknown route', async () => {
      const req = createMockRequest({ 
        method: 'GET', 
        url: '/unknown',
        headers: { authorization: 'Bearer test-api-key' }
      });
      const res = createMockResponse();
      
      const handler = createHandleRequest('test-api-key');
      await handler(req, res);
      
      assert.strictEqual(res._statusCode, 404);
    });
  });
});
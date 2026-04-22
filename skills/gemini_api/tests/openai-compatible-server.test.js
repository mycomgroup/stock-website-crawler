import { strict as assert } from 'assert';
import http from 'http';

const PORT = 3099;
const API_KEY = 'test-api-key';

let testsPassed = 0;
let testsFailed = 0;
let server;
let originalEnv;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    testsPassed++;
  } catch (error) {
    console.log(`❌ ${name}`);
    console.log(`   Error: ${error.message}`);
    testsFailed++;
  }
}

async function testAsync(name, fn) {
  try {
    await fn();
    console.log(`✅ ${name}`);
    testsPassed++;
  } catch (error) {
    console.log(`❌ ${name}`);
    console.log(`   Error: ${error.message}`);
    testsFailed++;
  }
}

function parseBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => {
      try {
        resolve(JSON.parse(body));
      } catch (error) {
        reject(error);
      }
    });
    req.on('error', reject);
  });
}

function verifyApiKey(req, key) {
  const authHeader = req.headers.authorization;
  if (!authHeader) return false;
  const token = authHeader.replace('Bearer ', '');
  return token === key;
}

function sendJSON(res, statusCode, data) {
  res.writeHead(statusCode, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
  });
  res.end(JSON.stringify(data));
}

function sendSSE(res, data) {
  res.write(`data: ${JSON.stringify(data)}\n\n`);
}

class MockGeminiClient {
  constructor() {
    this.sendMessageResult = {
      messageId: 'msg-123',
      content: 'Hello, this is a test response.'
    };
    this.getModelsResult = [
      { slug: 'gpt-4', title: 'GPT-4' },
      { slug: 'gpt-3.5-turbo', title: 'GPT-3.5 Turbo' }
    ];
  }

  async sendMessage(options) {
    return this.sendMessageResult;
  }

  async getModels() {
    return this.getModelsResult;
  }
}

class MockSessionManager {
  constructor() {
    this.sessionData = { cookies: [], capturedAt: new Date().toISOString() };
  }

  async ensureValidSession() {
    return this.sessionData;
  }

  getCookies() {
    return 'session=test';
  }
}

class MockMultiAccountManager {
  constructor() {
    this.accounts = [
      { id: 'acc-1', name: 'Account 1', status: 'active', requestCount: 0, sessionData: {} }
    ];
    this.strategy = 'round-robin';
    this.currentIndex = 0;
  }

  getNextAccount() {
    return this.accounts[0];
  }

  useAccount(account) {
    account.requestCount++;
    account.lastUsed = Date.now();
  }

  async validateAllAccounts() {
    this.accounts[0].status = 'active';
  }
}

async function makeRequest(options, body = null) {
  return new Promise((resolve, reject) => {
    const req = http.request({
      hostname: 'localhost',
      port: PORT,
      ...options
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve({
            statusCode: res.statusCode,
            headers: res.headers,
            body: data,
            json: data ? JSON.parse(data) : null
          });
        } catch (e) {
          resolve({
            statusCode: res.statusCode,
            headers: res.headers,
            body: data
          });
        }
      });
    });
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

function createTestServer(client, sessionManager, multiAccountManager, useMultiAccount = false) {
  return http.createServer(async (req, res) => {
    const { method, url } = req;

    if (method === 'OPTIONS') {
      res.writeHead(200, {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      });
      res.end();
      return;
    }

    if (!verifyApiKey(req, API_KEY)) {
      return sendJSON(res, 401, {
        error: { message: 'Invalid API key', type: 'invalid_request_error' }
      });
    }

    if (url === '/v1/chat/completions' && method === 'POST') {
      try {
        const body = await parseBody(req);
        const { messages, model = 'gpt-4', stream = false } = body;

        if (!messages || !Array.isArray(messages)) {
          return sendJSON(res, 400, {
            error: { message: 'messages is required and must be an array', type: 'invalid_request_error' }
          });
        }

        const userMessages = messages.filter(m => m.role === 'user');
        const lastMessage = userMessages[userMessages.length - 1];

        if (!lastMessage) {
          return sendJSON(res, 400, {
            error: { message: 'No user message found', type: 'invalid_request_error' }
          });
        }

        const response = await client.sendMessage({ message: lastMessage.content, model });

        if (stream) {
          res.writeHead(200, {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*'
          });

          const streamContent = response.content || '';
          const chunks = streamContent.split(' ').filter(c => c.length > 0);

          for (let i = 0; i < chunks.length; i++) {
            sendSSE(res, {
              id: `chatcmpl-${response.messageId}`,
              object: 'chat.completion.chunk',
              created: Math.floor(Date.now() / 1000),
              model: model,
              choices: [{
                index: 0,
                delta: { content: (i > 0 ? ' ' : '') + chunks[i] },
                finish_reason: null
              }]
            });
          }

          sendSSE(res, {
            id: `chatcmpl-${response.messageId}`,
            object: 'chat.completion.chunk',
            created: Math.floor(Date.now() / 1000),
            model: model,
            choices: [{ index: 0, delta: {}, finish_reason: 'stop' }]
          });

          res.write('data: [DONE]\n\n');
          res.end();
        } else {
          sendJSON(res, 200, {
            id: `chatcmpl-${response.messageId}`,
            object: 'chat.completion',
            created: Math.floor(Date.now() / 1000),
            model: model,
            choices: [{
              index: 0,
              message: { role: 'assistant', content: response.content },
              finish_reason: 'stop'
            }],
            usage: {
              prompt_tokens: lastMessage.content.length,
              completion_tokens: response.content.length,
              total_tokens: lastMessage.content.length + response.content.length
            }
          });
        }
      } catch (error) {
        sendJSON(res, 500, {
          error: { message: error.message, type: 'server_error' }
        });
      }
    } else if (url === '/v1/models' && method === 'GET') {
      try {
        const models = await client.getModels();
        sendJSON(res, 200, {
          object: 'list',
          data: models.map(model => ({
            id: model.slug,
            object: 'model',
            created: Math.floor(Date.now() / 1000),
            owned_by: 'openai'
          }))
        });
      } catch (error) {
        sendJSON(res, 200, {
          object: 'list',
          data: [
            { id: 'gpt-4', object: 'model', created: Math.floor(Date.now() / 1000), owned_by: 'openai' },
            { id: 'gpt-3.5-turbo', object: 'model', created: Math.floor(Date.now() / 1000), owned_by: 'openai' }
          ]
        });
      }
    } else if (url === '/health' && method === 'GET') {
      sendJSON(res, 200, { status: 'ok' });
    } else {
      sendJSON(res, 404, {
        error: { message: 'Not found', type: 'invalid_request_error' }
      });
    }
  });
}

console.log('\n=== OpenAI Compatible Server Unit Tests ===\n');

test('verifyApiKey returns false when no authorization header', () => {
  const req = { headers: {} };
  assert.strictEqual(verifyApiKey(req, API_KEY), false);
});

test('verifyApiKey returns false when wrong token', () => {
  const req = { headers: { authorization: 'Bearer wrong-key' } };
  assert.strictEqual(verifyApiKey(req, API_KEY), false);
});

test('verifyApiKey returns true when correct token', () => {
  const req = { headers: { authorization: `Bearer ${API_KEY}` } };
  assert.strictEqual(verifyApiKey(req, API_KEY), true);
});

test('verifyApiKey handles token without Bearer prefix', () => {
  const req = { headers: { authorization: 'test-api-key' } };
  assert.strictEqual(verifyApiKey(req, API_KEY), true);
});

test('sendJSON sends correct response', () => {
  const mockRes = {
    headers: {},
    body: null,
    writeHead(statusCode, headers) {
      this.statusCode = statusCode;
      this.headers = headers;
    },
    end(body) {
      this.body = body;
    }
  };

  sendJSON(mockRes, 200, { test: 'data' });

  assert.strictEqual(mockRes.statusCode, 200);
  assert.strictEqual(mockRes.headers['Content-Type'], 'application/json');
  assert.strictEqual(mockRes.headers['Access-Control-Allow-Origin'], '*');
  assert.strictEqual(mockRes.body, '{"test":"data"}');
});

test('sendSSE writes SSE formatted data', () => {
  const mockRes = {
    writtenData: '',
    write(data) {
      this.writtenData += data;
    }
  };

  sendSSE(mockRes, { id: 1, content: 'test' });

  assert.ok(mockRes.writtenData.includes('data:'));
  assert.ok(mockRes.writtenData.includes('"id":1'));
});

async function runServerTests() {
  const client = new MockGeminiClient();
  const sessionManager = new MockSessionManager();
  const multiAccountManager = new MockMultiAccountManager();

  server = createTestServer(client, sessionManager, multiAccountManager);

  await new Promise(resolve => server.listen(PORT, resolve));

  await testAsync('OPTIONS request returns CORS headers', async () => {
    const result = await makeRequest({
      method: 'OPTIONS',
      path: '/v1/chat/completions'
    });
    assert.strictEqual(result.statusCode, 200);
    assert.strictEqual(result.headers['access-control-allow-origin'], '*');
  });

  await testAsync('Request without API key returns 401', async () => {
    const result = await makeRequest({
      method: 'POST',
      path: '/v1/chat/completions',
      headers: { 'Content-Type': 'application/json' }
    }, { messages: [] });
    assert.strictEqual(result.statusCode, 401);
    assert.strictEqual(result.json.error.message, 'Invalid API key');
  });

  await testAsync('Health endpoint returns ok', async () => {
    const result = await makeRequest({
      method: 'GET',
      path: '/health',
      headers: { Authorization: `Bearer ${API_KEY}` }
    });
    assert.strictEqual(result.statusCode, 200);
    assert.strictEqual(result.json.status, 'ok');
  });

  await testAsync('Invalid route returns 404', async () => {
    const result = await makeRequest({
      method: 'GET',
      path: '/invalid-route',
      headers: { Authorization: `Bearer ${API_KEY}` }
    });
    assert.strictEqual(result.statusCode, 404);
    assert.strictEqual(result.json.error.message, 'Not found');
  });

  await testAsync('/v1/models returns model list', async () => {
    const result = await makeRequest({
      method: 'GET',
      path: '/v1/models',
      headers: { Authorization: `Bearer ${API_KEY}` }
    });
    assert.strictEqual(result.statusCode, 200);
    assert.strictEqual(result.json.object, 'list');
    assert.ok(Array.isArray(result.json.data));
    assert.strictEqual(result.json.data.length, 2);
    assert.strictEqual(result.json.data[0].id, 'gpt-4');
  });

  await testAsync('/v1/chat/completions requires messages array', async () => {
    const result = await makeRequest({
      method: 'POST',
      path: '/v1/chat/completions',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${API_KEY}`
      }
    }, { model: 'gpt-4' });
    assert.strictEqual(result.statusCode, 400);
    assert.strictEqual(result.json.error.message, 'messages is required and must be an array');
  });

  await testAsync('/v1/chat/completions requires user message', async () => {
    const result = await makeRequest({
      method: 'POST',
      path: '/v1/chat/completions',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${API_KEY}`
      }
    }, { messages: [{ role: 'system', content: 'test' }] });
    assert.strictEqual(result.statusCode, 400);
    assert.strictEqual(result.json.error.message, 'No user message found');
  });

  await testAsync('/v1/chat/completions returns valid response', async () => {
    const result = await makeRequest({
      method: 'POST',
      path: '/v1/chat/completions',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${API_KEY}`
      }
    }, { model: 'gpt-4', messages: [{ role: 'user', content: 'Hello' }] });
    assert.strictEqual(result.statusCode, 200);
    assert.ok(result.json.id);
    assert.strictEqual(result.json.object, 'chat.completion');
    assert.strictEqual(result.json.model, 'gpt-4');
    assert.strictEqual(result.json.choices[0].message.role, 'assistant');
    assert.ok(result.json.choices[0].message.content);
    assert.strictEqual(result.json.choices[0].finish_reason, 'stop');
    assert.ok(result.json.usage);
    assert.ok(result.json.usage.prompt_tokens >= 0);
    assert.ok(result.json.usage.completion_tokens >= 0);
  });

  await testAsync('/v1/chat/completions returns stream response', async () => {
    const result = await makeRequest({
      method: 'POST',
      path: '/v1/chat/completions',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${API_KEY}`
      }
    }, { model: 'gpt-4', messages: [{ role: 'user', content: 'Hello' }], stream: true });
    assert.strictEqual(result.statusCode, 200);
    assert.strictEqual(result.headers['content-type'], 'text/event-stream');
    assert.ok(result.body.includes('data:'));
    assert.ok(result.body.includes('[DONE]'));
  });

  await testAsync('/v1/chat/completions handles empty response content', async () => {
    client.sendMessage = async () => ({ messageId: 'msg-empty', content: '' });
    const result = await makeRequest({
      method: 'POST',
      path: '/v1/chat/completions',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${API_KEY}`
      }
    }, { model: 'gpt-4', messages: [{ role: 'user', content: 'Hello' }], stream: true });
    assert.strictEqual(result.statusCode, 200);
    assert.ok(result.body.includes('[DONE]'));
    client.sendMessage = async () => ({ messageId: 'msg-123', content: 'Test response' });
  });

  await testAsync('/v1/chat/completions handles null response content', async () => {
    client.sendMessage = async () => ({ messageId: 'msg-null', content: null });
    const result = await makeRequest({
      method: 'POST',
      path: '/v1/chat/completions',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${API_KEY}`
      }
    }, { model: 'gpt-4', messages: [{ role: 'user', content: 'Hello' }], stream: true });
    assert.strictEqual(result.statusCode, 200);
    assert.ok(result.body.includes('[DONE]'));
    client.sendMessage = async () => ({ messageId: 'msg-123', content: 'Test response' });
  });

  await testAsync('/v1/chat/completions handles multiple user messages', async () => {
    const result = await makeRequest({
      method: 'POST',
      path: '/v1/chat/completions',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${API_KEY}`
      }
    }, {
      model: 'gpt-4',
      messages: [
        { role: 'user', content: 'First message' },
        { role: 'assistant', content: 'Response' },
        { role: 'user', content: 'Second message' }
      ]
    });
    assert.strictEqual(result.statusCode, 200);
  });

  await testAsync('/v1/chat/completions handles error from client', async () => {
    client.sendMessage = async () => {
      throw new Error('Client error');
    };
    const result = await makeRequest({
      method: 'POST',
      path: '/v1/chat/completions',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${API_KEY}`
      }
    }, { model: 'gpt-4', messages: [{ role: 'user', content: 'Hello' }] });
    assert.strictEqual(result.statusCode, 500);
    assert.strictEqual(result.json.error.message, 'Client error');
    assert.strictEqual(result.json.error.type, 'server_error');
    client.sendMessage = async () => ({ messageId: 'msg-123', content: 'Test response' });
  });

  await testAsync('/v1/models returns default list on error', async () => {
    client.getModels = async () => {
      throw new Error('Models error');
    };
    const result = await makeRequest({
      method: 'GET',
      path: '/v1/models',
      headers: { Authorization: `Bearer ${API_KEY}` }
    });
    assert.strictEqual(result.statusCode, 200);
    assert.ok(Array.isArray(result.json.data));
    client.getModels = async () => [
      { slug: 'gpt-4', title: 'GPT-4' },
      { slug: 'gpt-3.5-turbo', title: 'GPT-3.5 Turbo' }
    ];
  });

  server.close();
}

await runServerTests();

console.log('\n=== parseBody Function Tests ===\n');

async function runParseBodyTests() {
  await testAsync('parseBody parses valid JSON body', async () => {
    const mockReq = {
      on(event, handler) {
        if (event === 'data') handler(Buffer.from('{"test":"value"}'));
        if (event === 'end') handler();
      }
    };
    const result = await parseBody(mockReq);
    assert.strictEqual(result.test, 'value');
  });

  await testAsync('parseBody rejects invalid JSON', async () => {
    const mockReq = {
      on(event, handler) {
        if (event === 'data') handler(Buffer.from('invalid json'));
        if (event === 'end') handler();
      }
    };
    try {
      await parseBody(mockReq);
      assert.fail('Should have thrown error');
    } catch (error) {
      assert.ok(error instanceof SyntaxError);
    }
  });

  await testAsync('parseBody handles empty body', async () => {
    const mockReq = {
      on(event, handler) {
        if (event === 'data') handler(Buffer.from(''));
        if (event === 'end') handler();
      }
    };
    try {
      await parseBody(mockReq);
      assert.fail('Should have thrown error');
    } catch (error) {
      assert.ok(error instanceof SyntaxError);
    }
  });

  await testAsync('parseBody handles chunked data', async () => {
    const mockReq = {
      on(event, handler) {
        if (event === 'data') {
          handler(Buffer.from('{"part1":'));
          handler(Buffer.from('"value","part2":'));
          handler(Buffer.from('"value2"}'));
        }
        if (event === 'end') handler();
      }
    };
    const result = await parseBody(mockReq);
    assert.strictEqual(result.part1, 'value');
    assert.strictEqual(result.part2, 'value2');
  });

  await testAsync('parseBody propagates request error', async () => {
    const mockReq = {
      on(event, handler) {
        if (event === 'error') handler(new Error('Request failed'));
      }
    };
    try {
      await parseBody(mockReq);
      assert.fail('Should have thrown error');
    } catch (error) {
      assert.strictEqual(error.message, 'Request failed');
    }
  });
}

await runParseBodyTests();

console.log('\n=== getClient Function Tests (Multi-account) ===\n');

function createGetClientFunction(useMultiAccount, client, multiAccountManager) {
  return function getClient() {
    if (useMultiAccount) {
      const account = multiAccountManager.getNextAccount();
      multiAccountManager.useAccount(account);
      return {
        sendMessage: async (options) => client.sendMessage(options),
        getModels: async () => client.getModels()
      };
    } else {
      return client;
    }
  };
}

async function runGetClientTests() {
  const client = new MockGeminiClient();
  const multiAccountManager = new MockMultiAccountManager();

  test('getClient returns same client in single account mode', () => {
    const getClient = createGetClientFunction(false, client, multiAccountManager);
    const result1 = getClient();
    const result2 = getClient();
    assert.strictEqual(result1, result2);
  });

  test('getClient updates request count in multi-account mode', () => {
    const getClient = createGetClientFunction(true, client, multiAccountManager);
    getClient();
    assert.strictEqual(multiAccountManager.accounts[0].requestCount, 1);
    getClient();
    assert.strictEqual(multiAccountManager.accounts[0].requestCount, 2);
  });

  test('getClient updates lastUsed in multi-account mode', async () => {
    const getClient = createGetClientFunction(true, client, multiAccountManager);
    const before = Date.now();
    getClient();
    assert.ok(multiAccountManager.accounts[0].lastUsed >= before);
  });

  await testAsync('getClient returns working client in multi-account mode', async () => {
    const getClient = createGetClientFunction(true, client, multiAccountManager);
    const currentClient = getClient();
    const result = await currentClient.sendMessage({ message: 'test' });
    assert.ok(result.content);
  });
}

await runGetClientTests();

console.log('\n=== Test Summary ===');
console.log(`Passed: ${testsPassed}`);
console.log(`Failed: ${testsFailed}`);
console.log(`Total: ${testsPassed + testsFailed}`);

if (testsFailed > 0) {
  process.exit(1);
}
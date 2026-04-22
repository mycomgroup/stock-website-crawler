#!/usr/bin/env node

/**
 * OpenAI 兼容 API 服务器
 * 将 Google Gemini session 转换为标准的 OpenAI API 接口
 */

import http from 'http';
import { GeminiClient } from '../request/gemini-client.js';
import { SessionManager } from '../browser/session-manager.js';
import { MultiAccountManager } from '../browser/multi-account-manager.js';

const PORT = process.env.PORT || 3000;
const API_KEY = process.env.API_KEY || 'sk-gemini-proxy';
const USE_MULTI_ACCOUNT = process.env.USE_MULTI_ACCOUNT === 'true';

// 初始化客户端
let sessionManager;
let multiAccountManager;
let client;

if (USE_MULTI_ACCOUNT) {
  multiAccountManager = new MultiAccountManager();
  console.log(`🔄 使用多账号模式 (${multiAccountManager.accounts.length} 个账号)`);
} else {
  sessionManager = new SessionManager();
  client = new GeminiClient();
  console.log('👤 使用单账号模式');
}

/**
 * 解析请求体
 */
async function parseBody(req) {
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

/**
 * 验证 API Key
 */
function verifyApiKey(req) {
  const authHeader = req.headers.authorization;
  if (!authHeader) return false;
  
  const token = authHeader.replace('Bearer ', '');
  return token === API_KEY;
}

/**
 * 发送 JSON 响应
 */
function sendJSON(res, statusCode, data) {
  res.writeHead(statusCode, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
  });
  res.end(JSON.stringify(data));
}

/**
 * 发送 SSE 响应
 */
function sendSSE(res, data) {
  res.write(`data: ${JSON.stringify(data)}\n\n`);
}

/**
 * 获取客户端（支持多账号）
 */
function getClient() {
  if (USE_MULTI_ACCOUNT) {
    // 获取下一个可用账号
    const account = multiAccountManager.getNextAccount();
    multiAccountManager.useAccount(account);
    
    console.log(`📍 使用账号: ${account.name} (请求数: ${account.requestCount})`);
    
    // 创建临时客户端
    const tempSessionManager = new SessionManager();
    tempSessionManager.sessionData = account.sessionData;
    
    const tempClient = new GeminiClient();
    tempClient.sessionManager = tempSessionManager;
    
    return tempClient;
  } else {
    return client;
  }
}

/**
 * 处理 /v1/chat/completions
 */
async function handleChatCompletions(req, res, body) {
  const { messages, model = 'gpt-4', stream = false, temperature, max_tokens } = body;

  if (!messages || !Array.isArray(messages)) {
    return sendJSON(res, 400, {
      error: {
        message: 'messages is required and must be an array',
        type: 'invalid_request_error'
      }
    });
  }

  try {
    // 提取最后一条用户消息
    const userMessages = messages.filter(m => m.role === 'user');
    const lastMessage = userMessages[userMessages.length - 1];
    
    if (!lastMessage) {
      return sendJSON(res, 400, {
        error: {
          message: 'No user message found',
          type: 'invalid_request_error'
        }
      });
    }

    // 获取客户端（支持多账号）
    const currentClient = getClient();

    // 发送到 Gemini
    const response = await currentClient.sendMessage({
      message: lastMessage.content,
      model: model.includes('gemini') ? model : 'gemini-pro'
    });

    if (stream) {
      const streamContent = response.content || '';
      
      res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Access-Control-Allow-Origin': '*'
      });

      const chunks = streamContent.split(' ').filter(c => c.length > 0);
      
      for (let i = 0; i < chunks.length; i++) {
        sendSSE(res, {
          id: `chatcmpl-${response.messageId}`,
          object: 'chat.completion.chunk',
          created: Math.floor(Date.now() / 1000),
          model: model,
          choices: [{
            index: 0,
            delta: {
              content: (i > 0 ? ' ' : '') + chunks[i]
            },
            finish_reason: null
          }]
        });
        
        // 模拟延迟
        await new Promise(resolve => setTimeout(resolve, 50));
      }

      // 发送结束标记
      sendSSE(res, {
        id: `chatcmpl-${response.messageId}`,
        object: 'chat.completion.chunk',
        created: Math.floor(Date.now() / 1000),
        model: model,
        choices: [{
          index: 0,
          delta: {},
          finish_reason: 'stop'
        }]
      });

      res.write('data: [DONE]\n\n');
      res.end();

    } else {
      // 非流式响应
      sendJSON(res, 200, {
        id: `chatcmpl-${response.messageId}`,
        object: 'chat.completion',
        created: Math.floor(Date.now() / 1000),
        model: model,
        choices: [{
          index: 0,
          message: {
            role: 'assistant',
            content: response.content
          },
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
    console.error('Error:', error);
    sendJSON(res, 500, {
      error: {
        message: error.message,
        type: 'server_error'
      }
    });
  }
}

/**
 * 处理 /v1/models
 */
async function handleModels(req, res) {
  try {
    const currentClient = getClient();
    const models = await currentClient.getModels();
    
    sendJSON(res, 200, {
      object: 'list',
      data: models.map(model => ({
        id: model.slug,
        object: 'model',
        created: Math.floor(Date.now() / 1000),
        owned_by: 'openai',
        permission: [],
        root: model.slug,
        parent: null
      }))
    });
  } catch (error) {
    // 返回默认模型列表
    sendJSON(res, 200, {
      object: 'list',
      data: [
        {
          id: 'gpt-4',
          object: 'model',
          created: Math.floor(Date.now() / 1000),
          owned_by: 'openai'
        },
        {
          id: 'gpt-3.5-turbo',
          object: 'model',
          created: Math.floor(Date.now() / 1000),
          owned_by: 'openai'
        }
      ]
    });
  }
}

/**
 * 主请求处理器
 */
async function handleRequest(req, res) {
  const { method, url } = req;

  // CORS 预检
  if (method === 'OPTIONS') {
    res.writeHead(200, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    });
    res.end();
    return;
  }

  // 验证 API Key
  if (!verifyApiKey(req)) {
    return sendJSON(res, 401, {
      error: {
        message: 'Invalid API key',
        type: 'invalid_request_error'
      }
    });
  }

  // 路由
  if (url === '/v1/chat/completions' && method === 'POST') {
    const body = await parseBody(req);
    await handleChatCompletions(req, res, body);
  } else if (url === '/v1/models' && method === 'GET') {
    await handleModels(req, res);
  } else if (url === '/health' && method === 'GET') {
    sendJSON(res, 200, { status: 'ok' });
  } else {
    sendJSON(res, 404, {
      error: {
        message: 'Not found',
        type: 'invalid_request_error'
      }
    });
  }
}

/**
 * 启动服务器
 */
async function startServer() {
  console.log('🚀 启动 OpenAI 兼容 API 服务器...\n');

  // 确保 session 有效
  try {
    if (USE_MULTI_ACCOUNT) {
      if (multiAccountManager.accounts.length === 0) {
        console.error('❌ 没有可用的账号');
        console.log('💡 请先添加账号: node run-skill.js --add-account\n');
        process.exit(1);
      }
      
      await multiAccountManager.validateAllAccounts();
      
      const activeAccounts = multiAccountManager.accounts.filter(a => a.status === 'active');
      if (activeAccounts.length === 0) {
        console.error('❌ 没有有效的账号');
        console.log('💡 请重新登录账号\n');
        process.exit(1);
      }
      
      console.log(`✅ ${activeAccounts.length} 个账号可用\n`);
    } else {
      await sessionManager.ensureValidSession();
      console.log('✅ Session 验证成功\n');
    }
  } catch (error) {
    console.error('❌ Session 验证失败:', error.message);
    console.log('💡 请先运行: node run-skill.js --login\n');
    process.exit(1);
  }

  // 创建服务器
  const server = http.createServer(handleRequest);

  server.listen(PORT, () => {
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('✅ 服务器已启动！');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log(`📡 监听端口: ${PORT}`);
    console.log(`🔑 API Key: ${API_KEY}`);
    
    if (USE_MULTI_ACCOUNT) {
      console.log(`🔄 多账号模式: ${multiAccountManager.accounts.length} 个账号`);
      console.log(`⚖️  负载均衡策略: ${multiAccountManager.strategy}`);
    } else {
      console.log('👤 单账号模式');
    }
    
    console.log('');
    console.log('端点:');
    console.log(`  POST http://localhost:${PORT}/v1/chat/completions`);
    console.log(`  GET  http://localhost:${PORT}/v1/models`);
    console.log(`  GET  http://localhost:${PORT}/health`);
    console.log('');
    console.log('使用示例:');
    console.log('');
    console.log('  curl http://localhost:' + PORT + '/v1/chat/completions \\');
    console.log('    -H "Content-Type: application/json" \\');
    console.log('    -H "Authorization: Bearer ' + API_KEY + '" \\');
    console.log('    -d \'{"model":"gpt-4","messages":[{"role":"user","content":"你好"}]}\'');
    console.log('');
    console.log('OpenAI SDK 配置:');
    console.log('');
    console.log('  import OpenAI from "openai";');
    console.log('  ');
    console.log('  const openai = new OpenAI({');
    console.log('    apiKey: "' + API_KEY + '",');
    console.log('    baseURL: "http://localhost:' + PORT + '/v1"');
    console.log('  });');
    console.log('');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  });

  // 错误处理
  server.on('error', (error) => {
    console.error('❌ 服务器错误:', error.message);
    process.exit(1);
  });

  // 优雅关闭
  process.on('SIGINT', () => {
    console.log('\n\n🛑 正在关闭服务器...');
    server.close(() => {
      console.log('✅ 服务器已关闭');
      process.exit(0);
    });
  });
}

// 启动
startServer().catch(error => {
  console.error('❌ 启动失败:', error);
  process.exit(1);
});

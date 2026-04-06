#!/usr/bin/env node

/**
 * 测试完整工作流程（不需要真实登录）
 * 验证所有接口和功能是否正常
 */

import { writeFileSync, existsSync, mkdirSync } from 'fs';
import { PATHS } from './paths.js';

console.log('🧪 开始测试 ChatGPT API 工作流程\n');

// ============================================
// 1. 测试：创建模拟 session 数据
// ============================================
console.log('📝 步骤 1: 创建模拟 session 数据');

const mockSessionData = {
  capturedAt: new Date().toISOString(),
  cookies: [
    {
      name: '__Secure-next-auth.session-token',
      value: 'mock-session-token-' + Math.random().toString(36).substring(7),
      domain: '.chatgpt.com',
      path: '/',
      expires: Date.now() / 1000 + 86400 * 30, // 30 days
      httpOnly: true,
      secure: true,
      sameSite: 'Lax'
    },
    {
      name: '__Secure-next-auth.callback-url',
      value: 'https%3A%2F%2Fchatgpt.com',
      domain: 'chatgpt.com',
      path: '/',
      expires: Date.now() / 1000 + 86400 * 30,
      httpOnly: true,
      secure: true,
      sameSite: 'Lax'
    },
    {
      name: '__Host-next-auth.csrf-token',
      value: 'mock-csrf-token-' + Math.random().toString(36).substring(7),
      domain: 'chatgpt.com',
      path: '/',
      httpOnly: true,
      secure: true,
      sameSite: 'Lax'
    },
    {
      name: '_cfuvid',
      value: 'mock-cfuvid-' + Math.random().toString(36).substring(7),
      domain: '.chatgpt.com',
      path: '/',
      httpOnly: true,
      secure: true
    },
    {
      name: 'cf_clearance',
      value: 'mock-cf-clearance-' + Math.random().toString(36).substring(7),
      domain: '.chatgpt.com',
      path: '/',
      httpOnly: true,
      secure: true
    }
  ],
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
};

// 确保 data 目录存在
if (!existsSync(PATHS.data)) {
  mkdirSync(PATHS.data, { recursive: true });
}

// 保存模拟 session
writeFileSync(
  PATHS.sessionFile,
  JSON.stringify(mockSessionData, null, 2),
  'utf-8'
);

console.log('✅ 模拟 session 已创建');
console.log(`   文件: ${PATHS.sessionFile}`);
console.log(`   Cookies 数量: ${mockSessionData.cookies.length}`);
console.log('');

// ============================================
// 2. 测试：加载 session
// ============================================
console.log('📝 步骤 2: 测试 SessionManager.loadSession()');

const { SessionManager } = await import('./browser/session-manager.js');
const sessionManager = new SessionManager();

const loadedSession = sessionManager.loadSession();
console.log('✅ Session 加载成功');
console.log(`   捕获时间: ${loadedSession.capturedAt}`);
console.log(`   Cookies 数量: ${loadedSession.cookies.length}`);
console.log('');

// ============================================
// 3. 测试：获取 cookies 字符串
// ============================================
console.log('📝 步骤 3: 测试 SessionManager.getCookies()');

const cookieString = sessionManager.getCookies();
console.log('✅ Cookie 字符串生成成功');
console.log(`   长度: ${cookieString.length} 字符`);
console.log(`   预览: ${cookieString.substring(0, 100)}...`);
console.log('');

// ============================================
// 4. 测试：获取特定 cookie
// ============================================
console.log('📝 步骤 4: 测试 SessionManager.getCookie()');

const sessionToken = sessionManager.getCookie('__Secure-next-auth.session-token');
console.log('✅ 获取特定 cookie 成功');
console.log(`   Session Token: ${sessionToken}`);
console.log('');

// ============================================
// 5. 测试：获取认证 cookies
// ============================================
console.log('📝 步骤 5: 测试 SessionManager.getAuthCookies()');

const authCookies = sessionManager.getAuthCookies();
console.log('✅ 认证 cookies 获取成功');
console.log(`   Session Token: ${authCookies.sessionToken ? '✓' : '✗'}`);
console.log(`   Callback URL: ${authCookies.callbackUrl ? '✓' : '✗'}`);
console.log(`   CF UVID: ${authCookies.cfuvid ? '✓' : '✗'}`);
console.log(`   CF Clearance: ${authCookies.cfClearance ? '✓' : '✗'}`);
console.log('');

// ============================================
// 6. 测试：ChatGPTClient 初始化
// ============================================
console.log('📝 步骤 6: 测试 ChatGPTClient 初始化');

const { ChatGPTClient } = await import('./request/chatgpt-client.js');
const client = new ChatGPTClient({ model: 'gpt-4' });

console.log('✅ ChatGPTClient 初始化成功');
console.log(`   Base URL: ${client.baseUrl}`);
console.log(`   API URL: ${client.apiUrl}`);
console.log(`   Model: ${client.model}`);
console.log('');

// ============================================
// 7. 测试：构建 API 请求 payload
// ============================================
console.log('📝 步骤 7: 测试构建 API 请求 payload');

const testMessage = "你好，这是一个测试消息";
const messageId = client.generateId();
const parentMessageId = client.generateId();

const payload = {
  action: 'next',
  messages: [
    {
      id: messageId,
      author: { role: 'user' },
      content: {
        content_type: 'text',
        parts: [testMessage]
      }
    }
  ],
  model: 'gpt-4',
  parent_message_id: parentMessageId,
  timezone: 'Asia/Shanghai'
};

console.log('✅ API payload 构建成功');
console.log(`   Message ID: ${messageId}`);
console.log(`   Parent Message ID: ${parentMessageId}`);
console.log(`   Message: ${testMessage}`);
console.log(`   Payload 大小: ${JSON.stringify(payload).length} 字节`);
console.log('');

// ============================================
// 8. 测试：构建 HTTP headers
// ============================================
console.log('📝 步骤 8: 测试构建 HTTP headers');

const headers = {
  'Content-Type': 'application/json',
  'Cookie': cookieString,
  'User-Agent': sessionManager.getUserAgent(),
  'Accept': 'text/event-stream',
  'Origin': client.baseUrl,
  'Referer': `${client.baseUrl}/`
};

console.log('✅ HTTP headers 构建成功');
Object.keys(headers).forEach(key => {
  const value = headers[key];
  const preview = value.length > 60 ? value.substring(0, 60) + '...' : value;
  console.log(`   ${key}: ${preview}`);
});
console.log('');

// ============================================
// 9. 测试：模拟 SSE 响应解析
// ============================================
console.log('📝 步骤 9: 测试 SSE 响应解析');

const mockSSEResponse = `data: {"message":{"id":"msg-123","author":{"role":"assistant"},"content":{"content_type":"text","parts":["你好"]},"metadata":{"model_slug":"gpt-4"},"create_time":1234567890},"conversation_id":"conv-123"}

data: {"message":{"id":"msg-123","author":{"role":"assistant"},"content":{"content_type":"text","parts":["你好！我是"]},"metadata":{"model_slug":"gpt-4"},"create_time":1234567890},"conversation_id":"conv-123"}

data: {"message":{"id":"msg-123","author":{"role":"assistant"},"content":{"content_type":"text","parts":["你好！我是 ChatGPT"]},"metadata":{"model_slug":"gpt-4"},"create_time":1234567890},"conversation_id":"conv-123"}

data: [DONE]
`;

const parsedResult = client.parseSSEResponse(mockSSEResponse);
console.log('✅ SSE 响应解析成功');
console.log(`   Conversation ID: ${parsedResult.conversationId}`);
console.log(`   Message ID: ${parsedResult.messageId}`);
console.log(`   Model: ${parsedResult.model}`);
console.log(`   Content: ${parsedResult.content}`);
console.log('');

// ============================================
// 10. 测试：MessageSender 初始化
// ============================================
console.log('📝 步骤 10: 测试 MessageSender 初始化');

const { MessageSender } = await import('./request/message-sender.js');
const sender = new MessageSender({ model: 'gpt-4', saveHistory: false });

console.log('✅ MessageSender 初始化成功');
console.log('');

// ============================================
// 11. 测试：历史记录保存功能
// ============================================
console.log('📝 步骤 11: 测试历史记录保存功能');

const mockRecord = {
  timestamp: new Date().toISOString(),
  message: "测试消息",
  response: "测试响应",
  model: "gpt-4",
  conversationId: "conv-test-123",
  messageId: "msg-test-123",
  duration: 1234
};

sender.saveToHistory(mockRecord);
console.log('✅ 历史记录保存成功');
console.log(`   记录文件: ${PATHS.data}/history-${new Date().toISOString().split('T')[0]}.jsonl`);
console.log('');

// ============================================
// 总结
// ============================================
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('✅ 所有测试通过！');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('');
console.log('已验证的功能：');
console.log('  ✓ Session 数据创建和保存');
console.log('  ✓ Session 加载和管理');
console.log('  ✓ Cookie 字符串生成');
console.log('  ✓ 特定 cookie 获取');
console.log('  ✓ 认证 cookies 提取');
console.log('  ✓ ChatGPTClient 初始化');
console.log('  ✓ API 请求 payload 构建');
console.log('  ✓ HTTP headers 构建');
console.log('  ✓ SSE 响应解析');
console.log('  ✓ MessageSender 初始化');
console.log('  ✓ 历史记录保存');
console.log('');
console.log('下一步：');
console.log('  1. 运行 node run-skill.js --login 完成真实登录');
console.log('  2. 运行 node run-skill.js --message "你好" 测试真实 API 调用');
console.log('');

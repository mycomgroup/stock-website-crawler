import { SessionManager } from '../browser/session-manager.js';
import { ENV } from '../load-env.js';
import { proxyFetch } from './proxy-fetch.js';
import { SecureHttpClient } from '../../common/http-security.js';

/**
 * ChatGPT API 客户端
 * 使用 session cookies 与 ChatGPT 后端通信
 */
export class ChatGPTClient {
  constructor(options = {}) {
    this.sessionManager = new SessionManager();
    this.baseUrl = 'https://chatgpt.com';
    this.apiUrl = 'https://chatgpt.com/backend-api';
    this.model = options.model || ENV.DEFAULT_MODEL;
    
    // Initialize secure HTTP client
    this.secureClient = new SecureHttpClient({
      baseUrl: this.baseUrl,
      maxRequestsPerMinute: 10,
      sessionValidator: async () => {
        const cookies = this.sessionManager.getCookies();
        return cookies && cookies.length > 0;
      }
    });
  }

  /**
   * 确保已登录
   */
  async ensureAuthenticated() {
    await this.sessionManager.ensureValidSession();
  }

  isHtmlProtectionResponse(response, responseText = '') {
    const contentType = response.headers.get('content-type') || '';
    const preview = responseText.trim().slice(0, 200).toLowerCase();

    return contentType.includes('text/html') ||
           preview.startsWith('<!doctype html') ||
           preview.startsWith('<html');
  }

  async throwForBadResponse(response, action = '请求') {
    const responseText = await response.text();
    const preview = responseText.substring(0, 200);

    console.error(`HTTP ${response.status}: ${preview}`);

    if (response.status === 401) {
      console.error('❌ 认证失败，session 可能已失效');
      console.log('💡 请运行: node run-skill.js --login');
      throw new Error('Authentication failed. Please login again.');
    }

    if (response.status === 403 && this.isHtmlProtectionResponse(response, responseText)) {
      console.error('❌ 纯 HTTP 模式被浏览器侧风控拦截');
      console.log('💡 当前登录态在浏览器里通常仍然可用，请改用: node run-skill.js --use-browser --message "..."');
      console.log('💡 这通常不是重新登录就能解决的问题，而是缺少浏览器运行时生成的授权头和风控令牌');
      throw new Error(`Pure HTTP mode is blocked by browser-side protection while trying to${action}。请改用 --use-browser。`);
    }

    if (response.status === 403) {
      console.error('❌ 访问被拒绝，session 可能已失效，或请求缺少浏览器运行时状态');
      console.log('💡 可先尝试: node run-skill.js --login');
      console.log('💡 如果浏览器模式可用而纯 HTTP 不可用，请改用 --use-browser');
      throw new Error(`Access denied while trying to${action}.`);
    }

    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  /**
   * 发送消息到 ChatGPT
   */
  async sendMessage(options = {}) {
    const {
      message,
      model = this.model,
      conversationId = null,
      parentMessageId = null
    } = options;

    if (!message) {
      throw new Error('Message is required');
    }

    await this.ensureAuthenticated();

    console.log(`💬 发送消息到 ChatGPT (${model})...`);
    console.log(`📝 消息: ${message.substring(0, 100)}${message.length > 100 ? '...' : ''}`);

    const cookies = this.sessionManager.getCookies();
    const userAgent = this.sessionManager.getUserAgent();
    
    // Get additional cookies for headers
    const oaiDeviceId = this.sessionManager.getCookie('oai-did') || '';
    const oaiSc = this.sessionManager.getCookie('oai-sc') || '';
    
    // Debug: log cookie count
    const cookieCount = cookies.split('; ').length;
    console.log(`🍪 使用 ${cookieCount} 个 cookies`);

    // Prepare request payload
    const payload = {
      action: 'next',
      messages: [
        {
          id: this.generateId(),
          author: { role: 'user' },
          content: {
            content_type: 'text',
            parts: [message]
          },
          metadata: {}
        }
      ],
      model,
      parent_message_id: parentMessageId || this.generateId(),
      timezone: 'Asia/Shanghai',
      timezone_offset_min: -480,
      history_and_training_disabled: false,
      conversation_mode: { kind: 'primary_assistant' },
      force_paragen: false,
      force_rate_limit: false
    };

    if (conversationId) {
      payload.conversation_id = conversationId;
    }

    try {
      const response = await proxyFetch(`${this.apiUrl}/conversation`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Cookie': cookies,
          'User-Agent': userAgent,
          'Accept': '*/*',
          'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
          'Accept-Encoding': 'gzip, deflate, br',
          'Origin': this.baseUrl,
          'Referer': `${this.baseUrl}/`,
          'Sec-Ch-Ua': '"Chromium";v="131", "Not_A Brand";v="24"',
          'Sec-Ch-Ua-Mobile': '?0',
          'Sec-Ch-Ua-Platform': '"macOS"',
          'Sec-Fetch-Dest': 'empty',
          'Sec-Fetch-Mode': 'cors',
          'Sec-Fetch-Site': 'same-origin',
          'Priority': 'u=1, i',
          'Pragma': 'no-cache',
          'Cache-Control': 'no-cache',
          'Oai-Device-Id': oaiDeviceId,
          'Oai-Language': 'zh-CN'
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        await this.throwForBadResponse(response, '发送消息');
      }

      // Parse SSE response
      const text = await response.text();
      const result = this.parseSSEResponse(text);

      console.log('✅ 收到响应');
      
      return result;

    } catch (error) {
      console.error('❌ 发送消息失败:', error.message);
      throw error;
    }
  }

  /**
   * 解析 Server-Sent Events 响应
   */
  parseSSEResponse(text) {
    const lines = text.split('\n').filter(line => line.trim());
    
    let conversationId = null;
    let messageId = null;
    let content = '';
    let model = null;

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.substring(6);
        
        if (data === '[DONE]') {
          break;
        }

        try {
          const json = JSON.parse(data);
          
          if (json.conversation_id) {
            conversationId = json.conversation_id;
          }

          if (json.message) {
            messageId = json.message.id;
            model = json.message.metadata?.model_slug;
            
            if (json.message.content?.parts) {
              content = json.message.content.parts.join('');
            }
          }
        } catch (e) {
          // Skip invalid JSON
        }
      }
    }

    return {
      conversationId,
      messageId,
      content,
      model,
      rawResponse: text
    };
  }

  /**
   * 获取对话列表
   */
  async getConversations(options = {}) {
    const { offset = 0, limit = 20, order = 'updated' } = options;

    await this.ensureAuthenticated();

    const cookies = this.sessionManager.getCookies();
    const userAgent = this.sessionManager.getUserAgent();

    try {
      const response = await proxyFetch(
        `${this.apiUrl}/conversations?offset=${offset}&limit=${limit}&order=${order}`,
        {
          headers: {
            'Cookie': cookies,
            'User-Agent': userAgent,
            'Accept': 'application/json',
            'Origin': this.baseUrl,
            'Referer': `${this.baseUrl}/`
          }
        }
      );

      if (!response.ok) {
        await this.throwForBadResponse(response, '获取对话列表');
      }

      const data = await response.json();
      return {
        items: data.items || [],
        total: data.total || 0,
        limit: data.limit || limit,
        offset: data.offset || offset,
        hasMore: data.has_missing_conversations || false
      };

    } catch (error) {
      console.error('❌ 获取对话列表失败:', error.message);
      throw error;
    }
  }

  /**
   * 获取特定对话
   */
  async getConversation(conversationId) {
    await this.ensureAuthenticated();

    const cookies = this.sessionManager.getCookies();
    const userAgent = this.sessionManager.getUserAgent();

    try {
      const response = await proxyFetch(
        `${this.apiUrl}/conversation/${conversationId}`,
        {
          headers: {
            'Cookie': cookies,
            'User-Agent': userAgent,
            'Accept': 'application/json',
            'Origin': this.baseUrl,
            'Referer': `${this.baseUrl}/`
          }
        }
      );

      if (!response.ok) {
        await this.throwForBadResponse(response, '获取对话');
      }

      return await response.json();

    } catch (error) {
      console.error('❌ 获取对话失败:', error.message);
      throw error;
    }
  }

  /**
   * 删除对话
   */
  async deleteConversation(conversationId) {
    await this.ensureAuthenticated();

    const cookies = this.sessionManager.getCookies();
    const userAgent = this.sessionManager.getUserAgent();

    try {
      const response = await proxyFetch(
        `${this.apiUrl}/conversation/${conversationId}`,
        {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Cookie': cookies,
            'User-Agent': userAgent,
            'Accept': 'application/json',
            'Origin': this.baseUrl,
            'Referer': `${this.baseUrl}/`
          },
          body: JSON.stringify({ is_visible: false })
        }
      );

      if (!response.ok) {
        await this.throwForBadResponse(response, '删除对话');
      }

      return { success: true, conversationId };

    } catch (error) {
      console.error('❌ 删除对话失败:', error.message);
      throw error;
    }
  }

  /**
   * 清空所有对话
   */
  async clearConversations() {
    await this.ensureAuthenticated();

    const cookies = this.sessionManager.getCookies();
    const userAgent = this.sessionManager.getUserAgent();

    try {
      const response = await proxyFetch(
        `${this.apiUrl}/conversations`,
        {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Cookie': cookies,
            'User-Agent': userAgent,
            'Accept': 'application/json',
            'Origin': this.baseUrl,
            'Referer': `${this.baseUrl}/`
          },
          body: JSON.stringify({ is_visible: false })
        }
      );

      if (!response.ok) {
        await this.throwForBadResponse(response, '清空对话');
      }

      return { success: true };

    } catch (error) {
      console.error('❌ 清空对话失败:', error.message);
      throw error;
    }
  }

  /**
   * 重命名对话
   */
  async renameConversation(conversationId, title) {
    await this.ensureAuthenticated();

    const cookies = this.sessionManager.getCookies();
    const userAgent = this.sessionManager.getUserAgent();

    try {
      const response = await proxyFetch(
        `${this.apiUrl}/conversation/${conversationId}`,
        {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Cookie': cookies,
            'User-Agent': userAgent,
            'Accept': 'application/json',
            'Origin': this.baseUrl,
            'Referer': `${this.baseUrl}/`
          },
          body: JSON.stringify({ title })
        }
      );

      if (!response.ok) {
        await this.throwForBadResponse(response, '重命名对话');
      }

      return { success: true, conversationId, title };

    } catch (error) {
      console.error('❌ 重命名对话失败:', error.message);
      throw error;
    }
  }

  /**
   * 获取可用模型列表
   */
  async getModels() {
    await this.ensureAuthenticated();

    const cookies = this.sessionManager.getCookies();
    const userAgent = this.sessionManager.getUserAgent();

    try {
      const response = await proxyFetch(
        `${this.apiUrl}/models`,
        {
          headers: {
            'Cookie': cookies,
            'User-Agent': userAgent,
            'Accept': 'application/json',
            'Origin': this.baseUrl,
            'Referer': `${this.baseUrl}/`
          }
        }
      );

      if (!response.ok) {
        await this.throwForBadResponse(response, '获取模型列表');
      }

      const data = await response.json();
      return data.models || [];

    } catch (error) {
      console.error('❌ 获取模型列表失败:', error.message);
      throw error;
    }
  }

  /**
   * 获取账户信息
   */
  async getAccountInfo() {
    await this.ensureAuthenticated();

    const cookies = this.sessionManager.getCookies();
    const userAgent = this.sessionManager.getUserAgent();

    try {
      const response = await proxyFetch(
        `${this.apiUrl}/me`,
        {
          headers: {
            'Cookie': cookies,
            'User-Agent': userAgent,
            'Accept': 'application/json',
            'Origin': this.baseUrl,
            'Referer': `${this.baseUrl}/`
          }
        }
      );

      if (!response.ok) {
        await this.throwForBadResponse(response, '获取账户信息');
      }

      return await response.json();

    } catch (error) {
      console.error('❌ 获取账户信息失败:', error.message);
      if (error.cause) {
        console.error('原因:', error.cause);
      }
      throw error;
    }
  }

  /**
   * 搜索对话
   */
  async searchConversations(query, options = {}) {
    const { limit = 20 } = options;

    await this.ensureAuthenticated();

    const cookies = this.sessionManager.getCookies();
    const userAgent = this.sessionManager.getUserAgent();

    try {
      const response = await proxyFetch(
        `${this.apiUrl}/conversations/search?q=${encodeURIComponent(query)}&limit=${limit}`,
        {
          headers: {
            'Cookie': cookies,
            'User-Agent': userAgent,
            'Accept': 'application/json',
            'Origin': this.baseUrl,
            'Referer': `${this.baseUrl}/`
          }
        }
      );

      if (!response.ok) {
        await this.throwForBadResponse(response, '搜索对话');
      }

      const data = await response.json();
      return data.items || [];

    } catch (error) {
      console.error('❌ 搜索对话失败:', error.message);
      throw error;
    }
  }

  /**
   * 生成随机 ID
   */
  generateId() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }
}

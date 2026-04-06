import { SessionManager } from '../browser/session-manager.js';
import { ENV } from '../load-env.js';

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
  }

  /**
   * 确保已登录
   */
  async ensureAuthenticated() {
    await this.sessionManager.ensureValidSession();
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
          }
        }
      ],
      model,
      parent_message_id: parentMessageId || this.generateId(),
      timezone: 'Asia/Shanghai'
    };

    if (conversationId) {
      payload.conversation_id = conversationId;
    }

    try {
      const response = await fetch(`${this.apiUrl}/conversation`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Cookie': cookies,
          'User-Agent': userAgent,
          'Accept': 'text/event-stream',
          'Origin': this.baseUrl,
          'Referer': `${this.baseUrl}/`
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        if (response.status === 401 || response.status === 403) {
          console.error('❌ 认证失败，session 可能已失效');
          console.log('💡 请运行: node run-skill.js --login');
          throw new Error('Authentication failed. Please login again.');
        }
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
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
      const response = await fetch(
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
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
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
      const response = await fetch(
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
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
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
      const response = await fetch(
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
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
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
      const response = await fetch(
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
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
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
      const response = await fetch(
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
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
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
      const response = await fetch(
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
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
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
      const response = await fetch(
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
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();

    } catch (error) {
      console.error('❌ 获取账户信息失败:', error.message);
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
      const response = await fetch(
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
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
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

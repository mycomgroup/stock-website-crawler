import { SessionManager } from '../browser/session-manager.js';
import { ENV } from '../load-env.js';
import { SecureHttpClient } from '../../common/http-security.js';

/**
 * Google Gemini API 客户端
 * 使用 session cookies 与 Gemini 后端通信
 */
export class GeminiClient {
  constructor(options = {}) {
    this.sessionManager = new SessionManager();
    this.baseUrl = 'https://gemini.google.com';
    this.apiUrl = 'https://gemini.google.com/api';
    this.model = options.model || ENV.DEFAULT_MODEL || 'gemini-pro';
    
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

  /**
   * 发送消息到 Gemini
   */
  async sendMessage(options = {}) {
    const {
      message,
      model = this.model,
      conversationId = null
    } = options;

    if (!message) {
      throw new Error('Message is required');
    }

    await this.ensureAuthenticated();

    console.log(`💬 发送消息到 Gemini (${model})...`);
    console.log(`📝 消息: ${message.substring(0, 100)}${message.length > 100 ? '...' : ''}`);

    const cookies = this.sessionManager.getCookies();

    // Gemini API 请求格式
    const payload = {
      prompt: {
        text: message
      },
      model: model,
      conversation_id: conversationId
    };

    try {
      // Use secure client for the request
      const response = await this.secureClient.request(`${this.apiUrl}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Cookie': cookies,
          'Accept': 'application/json',
          'Origin': this.baseUrl,
          'Referer': `${this.baseUrl}/`
        },
        body: JSON.stringify(payload),
        timeout: 30000
      });

      const data = JSON.parse(response);

      console.log('✅ 收到响应');
      
      return {
        conversationId: data.conversation_id || conversationId,
        messageId: data.message_id || this.generateId(),
        content: data.text || data.response || '',
        model: model,
        rawResponse: data
      };

    } catch (error) {
      if (error.message.includes('401') || error.message.includes('403')) {
        console.error('❌ 认证失败，session 可能已失效');
        console.log('💡 请运行: node run-skill.js --login');
        throw new Error('Authentication failed. Please login again.');
      }
      console.error('❌ 发送消息失败:', error.message);
      throw error;
    }
  }

  /**
   * 获取对话列表
   */
  async getConversations(options = {}) {
    const { offset = 0, limit = 20 } = options;

    await this.ensureAuthenticated();

    const cookies = this.sessionManager.getCookies();

    try {
      const response = await this.secureClient.request(
        `${this.apiUrl}/conversations?offset=${offset}&limit=${limit}`,
        {
          method: 'GET',
          headers: {
            'Cookie': cookies,
            'Accept': 'application/json',
            'Origin': this.baseUrl,
            'Referer': `${this.baseUrl}/`
          },
          timeout: 30000
        }
      );

      const data = JSON.parse(response);
      return {
        items: data.conversations || [],
        total: data.total || 0,
        limit: limit,
        offset: offset
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

    try {
      const response = await this.secureClient.request(
        `${this.apiUrl}/conversation/${conversationId}`,
        {
          method: 'GET',
          headers: {
            'Cookie': cookies,
            'Accept': 'application/json',
            'Origin': this.baseUrl,
            'Referer': `${this.baseUrl}/`
          },
          timeout: 30000
        }
      );

      return JSON.parse(response);

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

    try {
      await this.secureClient.request(
        `${this.apiUrl}/conversation/${conversationId}`,
        {
          method: 'DELETE',
          headers: {
            'Cookie': cookies,
            'Accept': 'application/json',
            'Origin': this.baseUrl,
            'Referer': `${this.baseUrl}/`
          },
          timeout: 30000
        }
      );

      return { success: true, conversationId };

    } catch (error) {
      console.error('❌ 删除对话失败:', error.message);
      throw error;
    }
  }

  /**
   * 获取可用模型列表
   */
  async getModels() {
    // Gemini 模型列表
    return [
      {
        slug: 'gemini-pro',
        title: 'Gemini Pro',
        description: 'Most capable model for complex tasks',
        max_tokens: 32000
      },
      {
        slug: 'gemini-pro-vision',
        title: 'Gemini Pro Vision',
        description: 'Multimodal model for text and images',
        max_tokens: 16000
      }
    ];
  }

  /**
   * 获取账户信息
   */
  async getAccountInfo() {
    await this.ensureAuthenticated();

    const cookies = this.sessionManager.getCookies();

    try {
      const response = await this.secureClient.request(
        `${this.apiUrl}/user/info`,
        {
          method: 'GET',
          headers: {
            'Cookie': cookies,
            'Accept': 'application/json',
            'Origin': this.baseUrl,
            'Referer': `${this.baseUrl}/`
          },
          timeout: 30000
        }
      );

      return JSON.parse(response);

    } catch (error) {
      console.error('❌ 获取账户信息失败:', error.message);
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

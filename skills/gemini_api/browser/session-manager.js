import { readFileSync, existsSync } from 'fs';
import { PATHS } from '../paths.js';
import { captureSession, validateSessionInBrowser } from './capture-session.js';

/**
 * Session 管理器
 * 负责加载、验证、刷新 session
 */
export class SessionManager {
  constructor() {
    this.sessionData = null;
  }

  /**
   * 加载已保存的 session
   */
  loadSession() {
    if (!existsSync(PATHS.sessionFile)) {
      console.log('⚠️  未找到 session 文件，需要先登录');
      return null;
    }

    try {
      const content = readFileSync(PATHS.sessionFile, 'utf-8');
      this.sessionData = JSON.parse(content);
      
      const capturedAt = new Date(this.sessionData.capturedAt);
      const daysAgo = Math.floor((Date.now() - capturedAt.getTime()) / (1000 * 60 * 60 * 24));
      
      console.log(`📂 加载 session (捕获于 ${daysAgo} 天前)`);
      
      return this.sessionData;
    } catch (error) {
      console.error('❌ 加载 session 失败:', error.message);
      return null;
    }
  }

  /**
   * 获取 cookies 对象（用于 HTTP 请求）
   */
  getCookies() {
    if (!this.sessionData) {
      this.loadSession();
    }

    if (!this.sessionData) {
      throw new Error('No session data available. Please login first.');
    }

    // Convert cookies array to cookie string
    const cookieString = this.sessionData.cookies
      .map(cookie => `${cookie.name}=${cookie.value}`)
      .join('; ');

    return cookieString;
  }

  /**
   * 获取特定 cookie 的值
   */
  getCookie(name) {
    if (!this.sessionData) {
      this.loadSession();
    }

    if (!this.sessionData) {
      return null;
    }

    const cookie = this.sessionData.cookies.find(c => c.name === name);
    return cookie ? cookie.value : null;
  }

  /**
   * 获取关键认证 cookies
   */
  getAuthCookies() {
    return {
      sessionToken: this.getCookie('__Secure-next-auth.session-token'),
      callbackUrl: this.getCookie('__Secure-next-auth.callback-url'),
      cfuvid: this.getCookie('_cfuvid'),
      cfClearance: this.getCookie('cf_clearance')
    };
  }

  /**
   * 验证 session 是否有效
   */
  async validateSession() {
    if (!this.sessionData) {
      this.loadSession();
    }

    if (!this.sessionData) {
      return false;
    }

    // Check if session is too old (> 30 days)
    const capturedAt = new Date(this.sessionData.capturedAt);
    const daysAgo = Math.floor((Date.now() - capturedAt.getTime()) / (1000 * 60 * 60 * 24));
    
    if (daysAgo > 30) {
      console.log('⚠️  Session 已过期（超过 30 天）');
      return false;
    }

    // Validate in browser
    return await validateSessionInBrowser(this.sessionData);
  }

  /**
   * 刷新 session（重新登录）
   */
  async refreshSession(options = {}) {
    console.log('🔄 刷新 session...');
    this.sessionData = await captureSession(options);
    return this.sessionData;
  }

  /**
   * 确保有有效的 session
   */
  async ensureValidSession(options = {}) {
    // Try to load existing session
    if (!this.sessionData) {
      this.loadSession();
    }

    // If no session, capture new one
    if (!this.sessionData) {
      console.log('🔐 首次使用，需要登录');
      return await this.refreshSession(options);
    }

    // Validate existing session
    const isValid = await this.validateSession();
    
    if (!isValid) {
      console.log('🔄 Session 已失效，需要重新登录');
      return await this.refreshSession(options);
    }

    return this.sessionData;
  }

  /**
   * 获取 User-Agent
   */
  getUserAgent() {
    if (!this.sessionData) {
      this.loadSession();
    }

    return this.sessionData?.userAgent || 
           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';
  }
}

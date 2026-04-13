import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import dotenv from 'dotenv';
import { BrowserEngine } from './core/browser-engine.js';

// 加载全局 .env
dotenv.config({ path: path.join(import.meta.dirname, '.env') });

const SESSION_ROOT = path.resolve(import.meta.dirname, '../.sessions');

export class AuthManager {
  constructor(siteAdapter) {
    this.site = siteAdapter;
    this.sessionPath = path.join(SESSION_ROOT, `${this.site.id}.json`);
    this.engine = new BrowserEngine();
  }

  // 统一处理 verifySession 的返回值（支持 boolean 或 {success, user, message} 两种格式）
  normalizeVerify(result) {
    if (typeof result === 'boolean') {
      return { success: result, user: result ? '已登录' : '', message: result ? '' : '验证失败' };
    }
    if (typeof result === 'object' && result !== null) {
      return { success: !!result.success, user: result.user || '', message: result.message || '' };
    }
    return { success: false, user: '', message: '未知返回格式' };
  }

  sanitizeCookies(cookies) {
    return cookies.map(c => {
      const copy = { ...c };
      // Playwright expects expires as float (unix timestamp in seconds) or undefined.
      // null is an object in JS, which causes "expected float, got object" error.
      if (copy.expires === null || typeof copy.expires !== 'number') {
        delete copy.expires;
      }
      // Ensure sameSite is one of top-level capitalized values
      if (copy.sameSite) {
        const s = copy.sameSite.toLowerCase();
        if (s === 'lax') copy.sameSite = 'Lax';
        else if (s === 'strict') copy.sameSite = 'Strict';
        else if (s === 'none') copy.sameSite = 'None';
      }
      return copy;
    });
  }

  async getValidSession(options = {}) {
    const { forceRefresh = false, method = 'all' } = options;

    if (!forceRefresh) {
      const session = this.loadSession();
      if (session && session.cookies) {
        console.log(`🔍 [${this.site.id}] 正在验证缓存 Session...`);
        const v = this.normalizeVerify(await this.site.verifySession(session.cookies));
        if (v.success) {
          console.log(`✅ [${this.site.id}] 缓存验证成功: ${v.user}`);
          return session.cookies;
        } else {
          console.log(`⚠️ [${this.site.id}] 缓存已失效: ${v.message}`);
        }
      }
    }

    let cookies = null;

    if (method === 'local' || method === 'all') {
      cookies = await this.tryLocalExtraction();
      if (cookies) return cookies;
    }

    if (method === 'auto' || method === 'all') {
      cookies = await this.tryAutomatedLogin();
      if (cookies) return cookies;
    }

    if (method === 'manual' || method === 'all') {
      return await this.tryManualCapture();
    }

    throw new Error(`无法获取 [${this.site.id}] 的有效会话。`);
  }

  loadSession() {
    if (!fs.existsSync(this.sessionPath)) return null;
    return JSON.parse(fs.readFileSync(this.sessionPath, 'utf8'));
  }

  async saveSessionWithVerify(cookies, url = '') {
    console.log(`🛡️ [${this.site.id}] 正在执行最终验证...`);
    const v = this.normalizeVerify(await this.site.verifySession(cookies));

    if (!v.success) {
      console.error(`❌ [${this.site.id}] 验证失败: ${v.message}`);
      return false;
    }

    const data = {
      cookies,
      timestamp: Date.now(),
      url,
      user: v.user || 'unknown'
    };
    if (!fs.existsSync(SESSION_ROOT)) fs.mkdirSync(SESSION_ROOT, { recursive: true });
    fs.writeFileSync(this.sessionPath, JSON.stringify(data, null, 2));
    console.log(`💾 [${this.site.id}] Session 验证成功 (${v.user || 'unknown'})并已存档。`);
    return true;
  }

  async tryLocalExtraction() {
    console.log(`🔍 [${this.site.id}] 尝试从本地浏览器提取...`);
    const extractorPath = path.join(import.meta.dirname, 'core/extractor.py');
    try {
      const output = execSync(`python3 "${extractorPath}" "${this.site.domain}"`, { encoding: 'utf8' });
      const cookies = JSON.parse(output);
      if (cookies && cookies.length > 0) {
        const success = await this.saveSessionWithVerify(cookies, this.site.loginUrl);
        if (success) return cookies;
      }
    } catch (e) {
      console.warn(`⚠️ 本地提取失败: ${e.message}`);
    }
    return null;
  }

  async tryAutomatedLogin() {
    console.log(`🤖 [${this.site.id}] 尝试执行自动化表单登录...`);
    const { browser, context } = await this.engine.launchContext();
    const page = await context.newPage();
    try {
      await page.goto(this.site.loginUrl, { waitUntil: 'networkidle', timeout: 30000 });
      await this.site.automatedLogin(page, process.env);
      
      const loggedIn = await this.site.checkLoggedIn(page);
      if (loggedIn) {
        const cookies = await context.cookies();
        const success = await this.saveSessionWithVerify(cookies, page.url());
        if (success) return cookies;
      }
    } catch (e) {
      console.warn(`⚠️ 自动登录失败: ${e.message}`);
    } finally {
      await browser.close();
    }
    return null;
  }

  async tryManualCapture() {
    console.log(`👋 [${this.site.id}] 需要手动登录。正在启动浏览器...`);
    const browser = await this.engine.launchHeaded();
    const context = await browser.newContext();
    const page = await context.newPage();

    await page.goto(this.site.loginUrl);

    console.log('\n=========================================');
    console.log(`请在打开的浏览器中完成 [${this.site.name}] 的登录。`);
    console.log('脚本将等待您登录成功并完成验证...');
    console.log('=========================================\n');

    return new Promise((resolve, reject) => {
      let isSaving = false;

      const doSaveAndExit = async (cookies, url, message = '手动登录成功，Cookie 已存档。') => {
        if (isSaving) return;
        isSaving = true;
        clearInterval(checkInterval);
        clearTimeout(timeoutId);

        const data = {
          cookies,
          timestamp: Date.now(),
          url,
          user: 'manual-login'
        };
        const fs = (await import('node:fs')).default;
        const SESSION_ROOT = this.sessionPath.replace(/\/[^/]+$/, '');
        if (!fs.existsSync(SESSION_ROOT)) fs.mkdirSync(SESSION_ROOT, { recursive: true });
        fs.writeFileSync(this.sessionPath, JSON.stringify(data, null, 2));
        console.log(`💾 [${this.site.id}] ${message}`);

        await browser.close().catch(() => {});
        resolve(cookies);
      };

      const trySaveCookiesBeforeExit = async (reason) => {
        if (isSaving) return;
        isSaving = true;
        clearInterval(checkInterval);
        clearTimeout(timeoutId);

        try {
          const cookies = await context.cookies();
          if (cookies && cookies.length > 0) {
            const data = {
              cookies,
              timestamp: Date.now(),
              url: this.site.loginUrl,
              user: 'manual-login'
            };
            const fs = (await import('node:fs')).default;
            const SESSION_ROOT = this.sessionPath.replace(/\/[^/]+$/, '');
            if (!fs.existsSync(SESSION_ROOT)) fs.mkdirSync(SESSION_ROOT, { recursive: true });
            fs.writeFileSync(this.sessionPath, JSON.stringify(data, null, 2));
            console.log(`💾 [${this.site.id}] 浏览器退出前已保存 Cookie。`);
            resolve(cookies);
            return;
          }
        } catch (e) {
          // 无法获取 cookie
        }
        reject(new Error(reason));
      };

      const checkInterval = setInterval(async () => {
        if (isSaving) return;
        try {
          if (!browser.isConnected()) {
            await trySaveCookiesBeforeExit('浏览器已被手动关闭。');
            return;
          }

          if (await this.site.checkLoggedIn(page)) {
            const cookies = await context.cookies();
            await doSaveAndExit(cookies, page.url());
          }
        } catch (e) {
          if (
            e.message.includes('Target page, context or browser has been closed') ||
            e.message.includes('Browser has been closed') ||
            e.message.includes('has been closed')
          ) {
            await trySaveCookiesBeforeExit('浏览器已被手动关闭。');
            return;
          }
        }
      }, 3000);

      const timeoutId = setTimeout(async () => {
        if (isSaving) return;
        await trySaveCookiesBeforeExit('手动登录超时（5分钟）');
      }, 300000);
    });
  }

  async testSessionHeaded() {
    const session = this.loadSession();
    if (!session || !session.cookies) {
      console.error(`❌ [${this.site.id}] 找不到本地 Session，请先登录。`);
      return;
    }

    console.log(`📺 [${this.site.id}] 正在启动视觉验证浏览器...`);
    const browser = await this.engine.launchHeaded();
    const context = await browser.newContext();
    await context.addCookies(this.sanitizeCookies(session.cookies));
    const page = await context.newPage();
    
    await page.goto(this.site.dashboardUrl || this.site.loginUrl);
    
    console.log('\n=========================================');
    console.log(`正在查看 [${this.site.name}] 的视觉状态。`);
    console.log('如果页面显示已登录，说明 Session 正确。');
    console.log('请在看清楚后手动关闭浏览器。');
    console.log('=========================================\n');

    await page.waitForEvent('close', { timeout: 0 }); // Wait until user closes
    await browser.close();
  }

  async importCookies(jsonString) {
    try {
      const raw = JSON.parse(jsonString);
      const cookies = Array.isArray(raw) ? raw : (raw.cookies || []);
      if (cookies.length === 0) throw new Error('无效的 Cookie JSON 格式');
      
      const success = await this.saveSessionWithVerify(cookies, 'manual-import');
      if (success) {
        console.log(`✅ [${this.site.id}] 手动导入并验证成功！`);
        return cookies;
      }
    } catch (e) {
      console.error(`❌ 导入失败: ${e.message}`);
      throw e;
    }
  }
}

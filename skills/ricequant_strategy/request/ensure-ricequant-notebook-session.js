import fs from 'node:fs';
import path from 'node:path';
import '../load-env.js';
import { SESSION_FILE } from '../paths.js';
import { captureRiceQuantNotebookSession } from '../browser/capture-ricequant-notebook-session.js';
import { RiceQuantNotebookClient } from './ricequant-notebook-client.js';

function resolveSessionFile(sessionFile) {
  return path.resolve(sessionFile || SESSION_FILE);
}

function isSessionExpired(sessionData) {
  if (!sessionData?.capturedAt) return true;
  const capturedAt = new Date(sessionData.capturedAt);
  const now = new Date();
  const hoursSinceCapture = (now - capturedAt) / (1000 * 60 * 60);
  return hoursSinceCapture > 24 * 7;
}

function hasValidCookies(sessionData) {
  if (!sessionData?.cookies || !Array.isArray(sessionData.cookies)) return false;
  const now = Date.now() / 1000;
  const validCookies = sessionData.cookies.filter(cookie => {
    if (cookie.name === 'RQSESSION' || cookie.name === 'session') return true;
    if (cookie.expires && cookie.expires > 0 && cookie.expires < now) return false;
    return true;
  });
  return validCookies.length >= 2;
}

function shouldRefreshSession(error) {
  const message = String(error?.stack || error?.message || error || '');
  if (!message) return true;
  if (message.includes('404')) return false;
  return /ENOENT|Unexpected token|缺少 `_xsrf` cookie|请求失败 401|请求失败 403|接口未返回 JSON|Failed to fetch|fetch failed|ECONNRESET|socket hang up/i.test(message);
}

export async function ensureRiceQuantNotebookSession(options = {}) {
  const sessionFile = resolveSessionFile(options.sessionFile);
  const notebookUrl = options.notebookUrl;

  if (!notebookUrl) {
    throw new Error('ensureRiceQuantNotebookSession 缺少 notebookUrl');
  }

  if (fs.existsSync(sessionFile) && !options.forceRefresh) {
    try {
      const sessionData = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));
      
      if (!isSessionExpired(sessionData) && sessionData.login?.loggedIn && hasValidCookies(sessionData)) {
        console.log('✓ 使用现有 session（未过期）');
        console.log(`  Session 文件: ${sessionFile}`);
        console.log(`  Session 时间: ${sessionData.capturedAt}`);
        
        const client = new RiceQuantNotebookClient({
          sessionFile,
          notebookUrl,
          outputRoot: options.outputRoot
        });
        
        try {
          await client.getNotebookMetadata();
          console.log('✓ Session 验证成功');
          return {
            sessionFile,
            refreshed: false,
            reason: 'existing-session-valid'
          };
        } catch (verifyError) {
          console.log(`✗ Session 验证失败: ${verifyError.message}`);
          console.log('  需要重新登录...');
        }
      } else {
        if (isSessionExpired(sessionData)) {
          console.log('✗ Session 已过期（超过7天）');
        } else if (!sessionData.login?.loggedIn) {
          console.log('✗ Session 未登录');
        } else if (!hasValidCookies(sessionData)) {
          console.log('✗ Session cookies 无效');
        }
      }
    } catch (error) {
      console.log(`✗ 读取 session 失败: ${error.message}`);
    }
  }

  console.log('开始浏览器登录获取新 session...');
  const captureResult = await captureRiceQuantNotebookSession({
    notebookUrl,
    headed: options.headed || false,
    headless: options.headless !== false
  });

  return {
    sessionFile,
    refreshed: true,
    reason: 'captured-new-session',
    captureResult
  };
}
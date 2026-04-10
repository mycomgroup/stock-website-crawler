import fs from 'node:fs';
import path from 'node:path';
import { captureRiceQuantSession } from './capture-session.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function loadJson(filePath) {
  if (!fs.existsSync(filePath)) return null;
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (e) {
    return null;
  }
}

function saveJson(filePath, data) {
  ensureDir(filePath);
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
}

/**
 * 检查会话是否有效
 */
function isSessionValid(session) {
  if (!session || !session.cookies || session.cookies.length === 0) {
    return false;
  }
  
  // RiceQuant 关键 cookie: sid 或 rqjwt
  const hasValidCookie = session.cookies.some(c => 
    c.name === 'sid' ||
    c.name === 'rqjwt' ||
    c.name.toLowerCase().includes('session') ||
    c.name.toLowerCase().includes('token') ||
    c.name.toLowerCase().includes('auth')
  );
  
  if (!hasValidCookie) {
    console.log('No valid session cookie found (need sid or rqjwt)');
    return false;
  }
  
  // 检查是否过期（RiceQuant session 有效期较长，设为 7 天）
  const SESSION_DURATION = 7 * 24 * 60 * 60 * 1000; // 7天
  const isExpired = Date.now() - (session.timestamp || 0) > SESSION_DURATION;
  
  if (isExpired) {
    console.log('Session expired (> 7 days old)');
    return false;
  }
  
  return true;
}

/**
 * 执行登录并保存 session
 */
async function doLogin(credentials) {
  if (!credentials || !credentials.username || !credentials.password) {
    throw new Error('Missing credentials. Please provide username and password.');
  }
  console.log('Launching browser to capture new session...');
  const session = await captureRiceQuantSession(credentials);
  saveJson(SESSION_FILE, session);
  console.log(`Session saved to ${SESSION_FILE}`);
  return session.cookies;
}

/**
 * 确保有有效的RiceQuant会话
 * @param {Object} credentials - { username, password }
 * @param {boolean} forceRefresh - 强制重新登录
 * @returns {Promise<Array>} - cookies数组
 */
export async function ensureRiceQuantSession(credentials, forceRefresh = false) {
  console.log('Checking RiceQuant session...');

  if (!forceRefresh) {
    const existingSession = loadJson(SESSION_FILE);
    if (isSessionValid(existingSession)) {
      console.log('Using existing valid session');
      return existingSession.cookies;
    }
  }

  console.log(forceRefresh ? 'Force refreshing session...' : 'Session invalid or expired, need to login...');
  return doLogin(credentials);
}

/**
 * 当 API 返回 session 失效错误时，自动重新登录并重试
 * @param {Object} credentials - { username, password }
 * @param {Function} fn - 使用 cookies 的异步函数 (cookies) => result
 * @returns {Promise<*>}
 */
export async function withAutoRelogin(credentials, fn) {
  // 先尝试用现有 session
  let cookies = await ensureRiceQuantSession(credentials);
  try {
    return await fn(cookies);
  } catch (err) {
    const isSessionError = 
      err.message.includes('No workspace found') ||
      err.message.includes('401') ||
      err.message.includes('403') ||
      err.message.includes('Unauthorized') ||
      err.message.includes('not logged in') ||
      err.message.includes('login');

    if (!isSessionError) throw err;

    console.error(`Session appears invalid (${err.message}), re-logging in...`);
    // 删除旧 session 文件，强制重新登录
    try { fs.unlinkSync(SESSION_FILE); } catch (_) {}
    cookies = await ensureRiceQuantSession(credentials, true);
    return await fn(cookies);
  }
}

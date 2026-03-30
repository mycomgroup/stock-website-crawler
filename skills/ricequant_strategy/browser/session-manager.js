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
  
  // 检查是否有必要的cookie（如sessionid）
  const hasSessionCookie = session.cookies.some(c => 
    c.name.toLowerCase().includes('session') ||
    c.name.toLowerCase().includes('token') ||
    c.name.toLowerCase().includes('auth')
  );
  
  if (!hasSessionCookie) {
    console.log('No session cookie found');
    return false;
  }
  
  // 检查是否过期（假设24小时有效）
  const SESSION_DURATION = 24 * 60 * 60 * 1000; // 24小时
  const isExpired = Date.now() - session.timestamp > SESSION_DURATION;
  
  if (isExpired) {
    console.log('Session expired');
    return false;
  }
  
  return true;
}

/**
 * 确保有有效的RiceQuant会话
 * @param {Object} credentials - { username, password }
 * @returns {Promise<Array>} - cookies数组
 */
export async function ensureRiceQuantSession(credentials) {
  console.log('Checking RiceQuant session...');
  
  // 1. 尝试加载已有会话
  const existingSession = loadJson(SESSION_FILE);
  
  if (isSessionValid(existingSession)) {
    console.log('Using existing valid session');
    return existingSession.cookies;
  }
  
  // 2. 需要重新登录
  console.log('Session invalid or expired, need to login...');
  
  if (!credentials || !credentials.username || !credentials.password) {
    throw new Error('Missing credentials. Please provide username and password.');
  }
  
  console.log('Launching browser to capture new session...');
  const session = await captureRiceQuantSession(credentials);
  
  // 3. 保存会话
  saveJson(SESSION_FILE, session);
  console.log(`Session saved to ${SESSION_FILE}`);
  
  return session.cookies;
}

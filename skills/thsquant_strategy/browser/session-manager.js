import fs from 'node:fs';
import path from 'node:path';
import { captureTHSQuantSession } from './capture-session.js';
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

function isSessionValid(session) {
  if (!session || !session.cookies || session.cookies.length === 0) {
    return false;
  }
  
  const hasValidCookie = session.cookies.some(c => 
    c.name.includes('sid') ||
    c.name.includes('token') ||
    c.name.includes('session') ||
    c.name.includes('auth') ||
    c.name.includes('ths')
  );
  
  if (!hasValidCookie) {
    console.log('No valid session cookie found');
    return false;
  }
  
  const SESSION_DURATION = 7 * 24 * 60 * 60 * 1000;
  const isExpired = Date.now() - (session.timestamp || 0) > SESSION_DURATION;
  
  if (isExpired) {
    console.log('Session expired (> 7 days old)');
    return false;
  }
  
  return true;
}

async function doLogin(credentials) {
  if (!credentials || !credentials.username || !credentials.password) {
    throw new Error('Missing credentials. Please provide username and password.');
  }
  console.log('Launching browser to capture new session...');
  const session = await captureTHSQuantSession(credentials);
  saveJson(SESSION_FILE, session);
  console.log(`Session saved to ${SESSION_FILE}`);
  return session.cookies;
}

export async function ensureTHSQuantSession(credentials, forceRefresh = false) {
  console.log('Checking THSQuant session...');

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
 */
export async function withAutoRelogin(credentials, fn) {
  let cookies = await ensureTHSQuantSession(credentials);
  try {
    return await fn(cookies);
  } catch (err) {
    const isSessionError =
      err.message.includes('Not logged in') ||
      err.message.includes('401') ||
      err.message.includes('403') ||
      err.message.includes('Unauthorized') ||
      err.message.includes('login') ||
      err.message.includes('session');

    if (!isSessionError) throw err;

    console.error(`Session appears invalid (${err.message}), re-logging in...`);
    try { fs.unlinkSync(SESSION_FILE); } catch (_) {}
    cookies = await ensureTHSQuantSession(credentials, true);
    return await fn(cookies);
  }
}
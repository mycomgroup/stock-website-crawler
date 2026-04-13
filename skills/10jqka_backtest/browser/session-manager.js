import fs from 'node:fs';
import path from 'node:path';
import { SESSION_FILE } from '../paths.js';

export function loadSession() {
  if (!fs.existsSync(SESSION_FILE)) return null;
  try {
    return JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  } catch (e) {
    return null;
  }
}

export function saveSession(cookies, url = '') {
  const sessionData = {
    cookies,
    timestamp: Date.now(),
    url
  };
  const dir = path.dirname(SESSION_FILE);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(SESSION_FILE, JSON.stringify(sessionData, null, 2), 'utf8');
  return sessionData;
}

export function isSessionValid(session) {
  if (!session || !session.cookies || session.cookies.length === 0) return false;
  
  // 检查是否有关键的 cookie (比如 v, CID, ths_quant 等)
  const hasKeyCookie = session.cookies.some(c => 
    c.name.includes('v') || c.name.includes('SID') || c.name.includes('token')
  );
  
  if (!hasKeyCookie) return false;

  // Session 默认有效期 7 天
  const SESSION_DURATION = 7 * 24 * 60 * 60 * 1000;
  const isExpired = Date.now() - (session.timestamp || 0) > SESSION_DURATION;
  
  return !isExpired;
}

/**
 * BigQuant HTTP 登录认证
 * 通过用户名/密码直接获取 bigjwt token，无需浏览器
 */

import fs from 'node:fs';
import path from 'node:path';
import '../load-env.js';
import { SESSION_FILE } from '../paths.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';
const ORIGIN = 'https://bigquant.com';

function ensureDir(p) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
}

function loadJson(p) {
  if (!fs.existsSync(p)) return null;
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return null; }
}

function saveJson(p, data) {
  ensureDir(p);
  fs.writeFileSync(p, JSON.stringify(data, null, 2), 'utf8');
}

/**
 * 解析 Set-Cookie 头，返回 cookie 对象数组
 */
function parseSetCookies(headers) {
  const raw = headers.getSetCookie ? headers.getSetCookie() : [];
  return raw.map(c => {
    const parts = c.split(';').map(s => s.trim());
    const [nameVal, ...attrs] = parts;
    const eqIdx = nameVal.indexOf('=');
    const name = nameVal.slice(0, eqIdx);
    const value = nameVal.slice(eqIdx + 1);
    const attrMap = {};
    for (const a of attrs) {
      const [k, v] = a.split('=');
      attrMap[k.toLowerCase()] = v || true;
    }
    return {
      name,
      value,
      domain: attrMap.domain || 'bigquant.com',
      path: attrMap.path || '/',
      expires: attrMap.expires ? new Date(attrMap.expires).getTime() / 1000 : -1,
      httpOnly: 'httponly' in attrMap,
      secure: 'secure' in attrMap,
      sameSite: attrMap.samesite || 'Lax'
    };
  });
}

/**
 * 合并 cookie 数组，新的覆盖旧的（按 name+domain）
 */
function mergeCookies(existing, incoming) {
  const map = new Map();
  for (const c of existing) map.set(`${c.name}@${c.domain}`, c);
  for (const c of incoming) map.set(`${c.name}@${c.domain}`, c);
  return [...map.values()];
}

/**
 * 检查 JWT 是否有效（未过期）
 */
function isJwtValid(jwt) {
  if (!jwt) return false;
  try {
    const payload = JSON.parse(Buffer.from(jwt.split('.')[1], 'base64').toString());
    return payload.exp > Date.now() / 1000 + 60; // 至少还有 60 秒
  } catch {
    return false;
  }
}

/**
 * 检查 session 是否有效
 */
export function isSessionValid(session) {
  if (!session?.cookies?.length) return false;
  const jwt = session.cookies.find(c => c.name === 'bigjwt')?.value;
  return isJwtValid(jwt);
}

/**
 * 从 session 中提取 userId（兼容旧格式）
 */
export function extractUserId(session) {
  if (session.userId) return session.userId;
  // 从 JWT payload 提取
  const jwt = session.cookies?.find(c => c.name === 'bigjwt')?.value;
  if (jwt) {
    try {
      const payload = JSON.parse(Buffer.from(jwt.split('.')[1], 'base64').toString());
      return payload.user?.id || payload.sub;
    } catch { return null; }
  }
  // 从 biguid cookie 提取
  return session.cookies?.find(c => c.name === 'biguid')?.value || null;
}

/**
 * 通过用户名密码登录，返回 session（含 cookies）
 */
export async function loginWithPassword(username, password) {
  console.log(`[Auth] 登录 BigQuant: ${username}`);

  // Step 1: 获取首页 cookies（bigdid 等）
  const homeResp = await fetch(`${ORIGIN}/`, {
    headers: { 'User-Agent': USER_AGENT },
    redirect: 'follow'
  });
  const initCookies = parseSetCookies(homeResp.headers);

  const cookieHeader = (cookies) => cookies.map(c => `${c.name}=${c.value}`).join('; ');

  // Step 2: 登录 API
  const loginResp = await fetch(`${ORIGIN}/bigapis/auth/v1/users/@login`, {
    method: 'POST',
    headers: {
      'User-Agent': USER_AGENT,
      'Content-Type': 'application/json',
      'Referer': `${ORIGIN}/`,
      'Origin': ORIGIN,
      'Cookie': cookieHeader(initCookies)
    },
    body: JSON.stringify({ username, password }),
    redirect: 'manual'
  });

  const loginCookies = parseSetCookies(loginResp.headers);
  const loginBody = await loginResp.text();

  let loginData;
  try { loginData = JSON.parse(loginBody); } catch { loginData = {}; }

  if (loginResp.status !== 200 || loginData.code !== 0) {
    // 尝试备用登录端点
    console.log('[Auth] 主登录端点失败，尝试备用...');
    return await loginWithPasswordAlt(username, password, initCookies);
  }

  const allCookies = mergeCookies(initCookies, loginCookies);

  // Step 3: 验证登录
  const meResp = await fetch(`${ORIGIN}/bigapis/auth/v1/users/me`, {
    headers: {
      'User-Agent': USER_AGENT,
      'Cookie': cookieHeader(allCookies)
    }
  });
  const meData = await meResp.json();

  if (meData.code !== 0) {
    throw new Error(`登录验证失败: ${JSON.stringify(meData)}`);
  }

  const userId = meData.data?.id;
  console.log(`[Auth] 登录成功: ${meData.data?.username} (${userId})`);

  const session = {
    cookies: allCookies,
    userId,
    username: meData.data?.username,
    timestamp: Date.now()
  };

  return session;
}

/**
 * 备用登录方式（手机号/邮箱）
 */
async function loginWithPasswordAlt(username, password, initCookies) {
  const cookieHeader = (cookies) => cookies.map(c => `${c.name}=${c.value}`).join('; ');

  // 尝试 phone 登录
  const resp = await fetch(`${ORIGIN}/bigapis/auth/v1/users/@login_by_phone`, {
    method: 'POST',
    headers: {
      'User-Agent': USER_AGENT,
      'Content-Type': 'application/json',
      'Referer': `${ORIGIN}/`,
      'Origin': ORIGIN,
      'Cookie': cookieHeader(initCookies)
    },
    body: JSON.stringify({ phone: username, password }),
    redirect: 'manual'
  });

  const loginCookies = parseSetCookies(resp.headers);
  const body = await resp.text();
  let data;
  try { data = JSON.parse(body); } catch { data = {}; }

  if (resp.status !== 200 || data.code !== 0) {
    throw new Error(`登录失败 (${resp.status}): ${body.slice(0, 200)}`);
  }

  const allCookies = mergeCookies(initCookies, loginCookies);
  const userId = data.data?.id || data.data?.user_id;

  console.log(`[Auth] 备用登录成功: ${data.data?.username}`);

  return {
    cookies: allCookies,
    userId,
    username: data.data?.username,
    timestamp: Date.now()
  };
}

/**
 * 确保有效 session，自动刷新
 */
export async function ensureSession(options = {}) {
  const sessionFile = options.sessionFile || SESSION_FILE;
  const existing = loadJson(sessionFile);

  if (isSessionValid(existing)) {
    // 补充 userId（兼容旧格式）
    if (!existing.userId) {
      existing.userId = extractUserId(existing);
    }
    console.log('[Auth] 使用已有 session, userId:', existing.userId);
    return existing;
  }

  const username = options.username || process.env.BIGQUANT_USERNAME;
  const password = options.password || process.env.BIGQUANT_PASSWORD;

  if (!username || !password) {
    throw new Error('Session 已过期，请设置 BIGQUANT_USERNAME 和 BIGQUANT_PASSWORD');
  }

  const session = await loginWithPassword(username, password);
  saveJson(sessionFile, session);
  console.log(`[Auth] Session 已保存: ${sessionFile}`);

  return session;
}

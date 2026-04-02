import fs from 'node:fs';
import path from 'node:path';
import { captureBigQuantSession } from './capture-session.js';
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
    c.name.toLowerCase().includes('session') ||
    c.name.toLowerCase().includes('token') ||
    c.name.toLowerCase().includes('auth') ||
    c.name.toLowerCase().includes('jwt')
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

export async function ensureBigQuantSession(credentials) {
  console.log('Checking BigQuant session...');
  
  const existingSession = loadJson(SESSION_FILE);
  
  if (isSessionValid(existingSession)) {
    console.log('Using existing valid session');
    return existingSession.cookies;
  }
  
  console.log('Session invalid or expired, need to login...');
  
  if (!credentials || !credentials.username || !credentials.password) {
    throw new Error('Missing credentials. Please provide username and password.');
  }
  
  console.log('Launching browser to capture new session...');
  const session = await captureBigQuantSession(credentials);
  
  saveJson(SESSION_FILE, session);
  console.log(`Session saved to ${SESSION_FILE}`);
  
  return session.cookies;
}
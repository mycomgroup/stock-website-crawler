#!/usr/bin/env node
import './load-env.js';
import { SESSION_FILE } from './paths.js';
import fs from 'fs';

const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
const cookieStr = session.cookies.filter(c => c.domain.includes('bigquant')).map(c => `${c.name}=${c.value}`).join('; ');
const studioId = 'e6277718-0f37-11ed-93bb-da75731aa77c';
const base = `https://bigquant.com/aistudio/studios/${studioId}/proxy/8888`;

async function req(method, path, body) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), 5000);
  try {
    const r = await fetch(base + path, {
      method, signal: ctrl.signal,
      headers: { 'Cookie': cookieStr, 'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json', 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined
    });
    clearTimeout(t);
    const text = await r.text();
    return { status: r.status, body: text.slice(0, 400) };
  } catch(e) {
    clearTimeout(t);
    return { status: 0, body: e.message.slice(0, 50) };
  }
}

// GET 所有 405 端点
const paths = [
  '/api/v0/run',
  '/api/v0/exec',
  '/api/v0/applications',
  '/api/terminal',
  '/bigquant/api/run',
  '/bigquant/api/execute',
  '/bigquant/run',
  '/stable-fb2afbd9d62532be3952118adafff3972c63f3bc/api/v0/run',
];

for (const path of paths) {
  const r = await req('GET', path);
  console.log(`GET ${path}: ${r.status} | ${r.body}`);
}

// 尝试 OPTIONS 获取允许的方法
console.log('\n=== OPTIONS ===');
for (const path of ['/api/v0/run', '/api/terminal', '/bigquant/run']) {
  const r = await req('OPTIONS', path);
  console.log(`OPTIONS ${path}: ${r.status} | ${r.body}`);
}

// 尝试 PUT/PATCH
console.log('\n=== PUT/PATCH ===');
for (const path of ['/api/v0/run', '/api/terminal']) {
  const r = await req('PUT', path, { command: 'python3 -c "print(1)"' });
  console.log(`PUT ${path}: ${r.status} | ${r.body}`);
}

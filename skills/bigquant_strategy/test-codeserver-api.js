#!/usr/bin/env node
/**
 * 测试 code-server 特有的 API
 * code-server 6.x 有 /api/v0/ 端点
 */
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
    return { status: r.status, body: text.slice(0, 300) };
  } catch(e) {
    clearTimeout(t);
    return { status: 0, body: e.message.slice(0, 50) };
  }
}

// code-server API 端点
const paths = [
  // code-server v4+ API
  ['/api/v0/applications', 'GET'],
  ['/api/v0/run', 'POST'],
  ['/api/v0/exec', 'POST'],
  // code-server 内置终端 API
  ['/api/terminal', 'GET'],
  ['/api/terminal', 'POST'],
  // VS Code server API
  ['/vscode/api', 'GET'],
  // 通过 stable hash 路径
  [`/stable-fb2afbd9d62532be3952118adafff3972c63f3bc/api/v0/run`, 'POST'],
  // 直接访问 extension host
  ['/extension-host', 'GET'],
  ['/extension-host/api', 'GET'],
  // BigQuant 自定义扩展 API
  ['/bigquant/api/run', 'POST'],
  ['/bigquant/api/execute', 'POST'],
  ['/bigquant/run', 'POST'],
  // Jupyter 可能在子路径
  ['/jupyter/api/kernels', 'GET'],
  ['/jupyter/api/sessions', 'GET'],
  ['/notebook/api/kernels', 'GET'],
];

for (const [path, method] of paths) {
  const body = method === 'POST' ? { code: 'print(1)' } : undefined;
  const r = await req(method, path, body);
  if (r.status !== 404 && r.status !== 0) {
    console.log(`${method} ${path}: ${r.status} | ${r.body}`);
  }
}

// 特别测试：通过 vscode-remote-resource 读取文件
console.log('\n=== 读取文件系统 ===');
const filePaths = [
  '/home/aiuser/work',
  '/home/aiuser',
  '/home/aiuser/.jupyter',
  '/home/aiuser/.local/share/aistudio',
  '/tmp',
];

for (const fp of filePaths) {
  const r = await req('GET', `/vscode-remote-resource?path=${encodeURIComponent(fp)}`);
  if (r.status !== 400 && r.status !== 0) {
    console.log(`vscode-remote-resource ${fp}: ${r.status} | ${r.body}`);
  }
}

console.log('\n完成');

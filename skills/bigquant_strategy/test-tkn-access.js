#!/usr/bin/env node
import './load-env.js';
import { SESSION_FILE } from './paths.js';
import fs from 'fs';

const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
const cookieStr = session.cookies.filter(c => c.domain.includes('bigquant')).map(c => `${c.name}=${c.value}`).join('; ');
const studioId = 'e6277718-0f37-11ed-93bb-da75731aa77c';
const hash = 'fb2afbd9d62532be3952118adafff3972c63f3bc';
const base = `https://bigquant.com/aistudio/studios/${studioId}/stable-${hash}`;

async function req(url, timeout = 5000) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), timeout);
  try {
    const r = await fetch(url, { signal: ctrl.signal, headers: { 'Cookie': cookieStr, 'User-Agent': 'Mozilla/5.0' } });
    clearTimeout(t);
    const text = await r.text();
    return { status: r.status, body: text.slice(0, 200) };
  } catch(e) {
    clearTimeout(t);
    return { status: 0, body: e.message.slice(0, 50) };
  }
}

// 获取 mint-key
const keyResp = await fetch(`https://bigquant.com/aistudio/studios/${studioId}/mint-key`, {
  method: 'POST',
  headers: { 'Cookie': cookieStr, 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json' },
  body: '{}'
});
const keyBuf = Buffer.from(await keyResp.arrayBuffer());
const keyHex = keyBuf.toString('hex');
console.log('key:', keyHex);

// 用 tkn 读取文件
const paths = [
  '/home/aiuser/work',
  '/home/aiuser',
  '/tmp',
];

for (const p of paths) {
  const url = `${base}/vscode-remote-resource?path=${encodeURIComponent(p)}&tkn=${keyHex}`;
  const r = await req(url);
  console.log(r.status, p, '|', r.body.slice(0, 100));
}

// 不带 tkn
const r0 = await req(`${base}/vscode-remote-resource?path=${encodeURIComponent('/home/aiuser/work')}&tkn=`);
console.log('no tkn:', r0.status, r0.body.slice(0, 100));

console.log('done');

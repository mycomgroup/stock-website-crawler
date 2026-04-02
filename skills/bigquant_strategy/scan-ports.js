#!/usr/bin/env node
import './load-env.js';
import { SESSION_FILE } from './paths.js';
import fs from 'fs';

const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
const cookieStr = session.cookies.filter(c => c.domain.includes('bigquant')).map(c => `${c.name}=${c.value}`).join('; ');
const studioId = 'e6277718-0f37-11ed-93bb-da75731aa77c';

async function test(url) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), 3000);
  try {
    const r = await fetch(url, { signal: ctrl.signal, headers: { 'Cookie': cookieStr, 'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json' } });
    clearTimeout(t);
    const text = await r.text();
    return { status: r.status, body: text.slice(0, 80) };
  } catch(e) {
    clearTimeout(t);
    return { status: 0, body: e.message.slice(0, 40) };
  }
}

const ports = [8080, 8888, 8889, 8890, 9000, 9999, 5000, 6006, 7777, 3000, 4040];

for (const port of ports) {
  const base = `https://bigquant.com/aistudio/studios/${studioId}/proxy/${port}`;
  const r1 = await test(`${base}/api/kernels`);
  const r2 = await test(`${base}/healthz`);
  const r3 = await test(`${base}/`);
  
  if (r1.status !== 0 && r1.status !== 404) {
    console.log(`PORT ${port} /api/kernels: ${r1.status} | ${r1.body}`);
  }
  if (r2.status !== 0 && r2.status !== 404) {
    console.log(`PORT ${port} /healthz: ${r2.status} | ${r2.body}`);
  }
  if (r3.status !== 0 && r3.status !== 404 && port !== 8888) {
    console.log(`PORT ${port} /: ${r3.status} | ${r3.body}`);
  }
}

console.log('扫描完成');

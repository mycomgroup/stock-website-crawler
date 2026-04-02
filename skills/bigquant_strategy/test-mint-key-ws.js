#!/usr/bin/env node
/**
 * 用 mint-key 认证连接 VS Code WebSocket
 * mint-key 是 VS Code server 的认证 token
 */
import './load-env.js';
import { SESSION_FILE } from './paths.js';
import { WebSocket } from 'ws';
import fs from 'fs';

const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
const cookieStr = session.cookies.filter(c => c.domain.includes('bigquant')).map(c => `${c.name}=${c.value}`).join('; ');
const studioId = 'e6277718-0f37-11ed-93bb-da75731aa77c';

// 1. 获取 mint-key
const keyResp = await fetch(`https://bigquant.com/aistudio/studios/${studioId}/mint-key`, {
  method: 'POST',
  headers: { 'Cookie': cookieStr, 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json' },
  body: '{}'
});
const keyBuf = Buffer.from(await keyResp.arrayBuffer());
const keyHex = keyBuf.toString('hex');
const keyBase64 = keyBuf.toString('base64');
console.log('mint-key hex:', keyHex);
console.log('mint-key base64:', keyBase64);

// 2. 获取 stable hash
const hashResp = await fetch(`https://bigquant.com/aistudio/studios/${studioId}/proxy/8888/version`, {
  headers: { 'Cookie': cookieStr }
});
const hash = await hashResp.text();
console.log('hash:', hash);

// 3. 连接 WebSocket，带 tkn 参数
const reconnToken = Date.now().toString();
const wsUrl = `wss://bigquant.com/aistudio/studios/${studioId}/stable-${hash}?reconnectionToken=${reconnToken}&reconnection=false&skipWebSocketFrames=false&tkn=${keyHex}`;
console.log('\n连接 WS:', wsUrl.slice(-100));

const ws = new WebSocket(wsUrl, {
  headers: {
    'Cookie': cookieStr,
    'User-Agent': 'Mozilla/5.0',
    'Origin': 'https://bigquant.com'
  }
});

let msgCount = 0;

ws.on('open', () => {
  console.log('✓ 连接成功');
  
  // 发送 VS Code server 握手
  // 参考 code-server 源码: src/node/routes/vscode.ts
  // 握手消息格式: { type: "auth", token: "..." }
  setTimeout(() => {
    // 方式1: 发送 auth token
    const authMsg = JSON.stringify({ type: 'auth', token: keyHex });
    ws.send(authMsg);
    console.log('发送 auth:', authMsg);
  }, 200);
  
  setTimeout(() => {
    // 方式2: 发送 base64 token
    const authMsg2 = JSON.stringify({ type: 'auth', token: keyBase64 });
    ws.send(authMsg2);
    console.log('发送 auth base64:', authMsg2);
  }, 500);
});

ws.on('message', (data, isBinary) => {
  msgCount++;
  const buf = Buffer.isBuffer(data) ? data : Buffer.from(data);
  
  if (buf.length === 13 && buf[0] === 9) {
    console.log(`[${msgCount}] keepalive ping`);
    return;
  }
  
  console.log(`\n[${msgCount}] ${isBinary ? 'binary' : 'text'} ${buf.length} bytes`);
  console.log('  hex:', buf.slice(0, 40).toString('hex'));
  
  if (!isBinary) {
    console.log('  text:', buf.toString('utf8').slice(0, 300));
  } else if (buf.length > 13) {
    const type = buf[0];
    const id = buf.readUInt32LE(1);
    const ack = buf.readUInt32LE(5);
    const len = buf.readUInt32LE(9);
    console.log(`  type=${type} id=${id} ack=${ack} len=${len}`);
    if (len > 0 && buf.length >= 13 + len) {
      const payload = buf.slice(13, 13 + Math.min(len, 200));
      try {
        const text = payload.toString('utf8');
        console.log('  payload:', text.slice(0, 200));
      } catch(e) {}
    }
  }
  
  if (msgCount >= 10) {
    ws.close();
  }
});

ws.on('error', err => console.error('错误:', err.message));
ws.on('close', (code, reason) => {
  console.log('\n关闭:', code, reason.toString());
  process.exit(0);
});

setTimeout(() => { ws.close(); process.exit(0); }, 15000);

#!/usr/bin/env node
/**
 * 通过 VS Code server WebSocket 执行 Python 代码
 * 
 * VS Code IPC 协议 (src/vs/base/parts/ipc/common/ipc.net.ts):
 * - 帧格式: [type(1)] [id(4 LE)] [ack(4 LE)] [len(4 LE)] [data(len)]
 * - type: 0=regular, 1=control, 9=keepalive
 * 
 * VS Code remote 握手 (src/vs/server/node/remoteExtensionHostAgentServer.ts):
 * - 连接后发送 auth 消息
 * - 然后发送 extensionHostProxy 消息
 */
import './load-env.js';
import { SESSION_FILE } from './paths.js';
import { WebSocket } from 'ws';
import fs from 'fs';

const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
const cookieStr = session.cookies.filter(c => c.domain.includes('bigquant')).map(c => `${c.name}=${c.value}`).join('; ');
const studioId = 'e6277718-0f37-11ed-93bb-da75731aa77c';

// 获取 stable hash
const hashResp = await fetch(`https://bigquant.com/aistudio/studios/${studioId}/proxy/8888/version`, {
  headers: { 'Cookie': cookieStr }
});
const hash = await hashResp.text();
console.log('Hash:', hash);

// 构建 VS Code IPC 帧
function buildFrame(type, id, ack, data) {
  const dataLen = data ? data.length : 0;
  const buf = Buffer.allocUnsafe(13 + dataLen);
  buf[0] = type;
  buf.writeUInt32LE(id, 1);
  buf.writeUInt32LE(ack, 5);
  buf.writeUInt32LE(dataLen, 9);
  if (data) data.copy(buf, 13);
  return buf;
}

// 构建 JSON 消息帧 (type=0, regular)
function buildJsonFrame(id, ack, obj) {
  const data = Buffer.from(JSON.stringify(obj), 'utf8');
  return buildFrame(0, id, ack, data);
}

const wsUrl = `wss://bigquant.com/aistudio/studios/${studioId}/stable-${hash}?reconnectionToken=${Date.now()}&reconnection=false&skipWebSocketFrames=false`;

const ws = new WebSocket(wsUrl, {
  headers: {
    'Cookie': cookieStr,
    'User-Agent': 'Mozilla/5.0',
    'Origin': 'https://bigquant.com'
  }
});

let msgId = 1;
let ackId = 0;

ws.on('open', () => {
  console.log('✓ 连接成功');
  
  // VS Code server 握手: 发送 auth 消息
  // 参考: src/vs/server/node/remoteExtensionHostAgentServer.ts
  setTimeout(() => {
    // 方式1: 发送 JSON auth
    const authMsg = buildJsonFrame(msgId++, ackId, {
      type: 'auth',
      auth: '00000000000000000000000000000000'
    });
    console.log('发送 auth 帧:', authMsg.toString('hex').slice(0, 60));
    ws.send(authMsg);
  }, 500);
  
  setTimeout(() => {
    // 方式2: 发送 management 连接请求
    const mgmtMsg = buildJsonFrame(msgId++, ackId, {
      type: 'management',
      reconnectionToken: String(Date.now()),
      reconnection: false,
      skipWebSocketFrames: false
    });
    console.log('发送 management 帧');
    ws.send(mgmtMsg);
  }, 1000);
  
  setTimeout(() => {
    // 方式3: 发送 extensionHost 连接请求
    const extMsg = buildJsonFrame(msgId++, ackId, {
      type: 'extensionHost',
      reconnectionToken: String(Date.now()),
      reconnection: false,
      skipWebSocketFrames: false
    });
    console.log('发送 extensionHost 帧');
    ws.send(extMsg);
  }, 1500);
});

ws.on('message', (data, isBinary) => {
  const buf = Buffer.isBuffer(data) ? data : Buffer.from(data);
  
  if (buf.length === 13 && buf[0] === 9) {
    // keepalive ping, ignore
    return;
  }
  
  console.log(`收到 ${buf.length} bytes: hex=${buf.slice(0, 40).toString('hex')}`);
  
  if (buf.length > 13) {
    const type = buf[0];
    const id = buf.readUInt32LE(1);
    const len = buf.readUInt32LE(9);
    if (len > 0) {
      const payload = buf.slice(13, 13 + len);
      try {
        const text = payload.toString('utf8');
        console.log('  payload:', text.slice(0, 300));
      } catch(e) {}
    }
  }
});

ws.on('error', err => console.error('错误:', err.message));
ws.on('close', code => { console.log('关闭:', code); process.exit(0); });
setTimeout(() => { ws.close(); process.exit(0); }, 10000);

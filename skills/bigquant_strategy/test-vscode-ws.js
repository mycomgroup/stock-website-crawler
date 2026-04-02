#!/usr/bin/env node
/**
 * 测试通过 VS Code WebSocket 发送执行命令
 * VS Code server 使用 JSON-RPC over WebSocket
 */
import './load-env.js';
import { SESSION_FILE } from './paths.js';
import { WebSocket } from 'ws';
import fs from 'fs';

const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
const cookieStr = session.cookies.filter(c => c.domain.includes('bigquant')).map(c => `${c.name}=${c.value}`).join('; ');
const studioId = 'e6277718-0f37-11ed-93bb-da75731aa77c';

// VS Code server WebSocket URL
const wsUrl = `wss://bigquant.com/aistudio/studios/${studioId}/stable-fb2afbd9d62532be3952118adafff3972c63f3bc`;

console.log('连接 VS Code WebSocket:', wsUrl.slice(-60));

const ws = new WebSocket(wsUrl, {
  headers: {
    'Cookie': cookieStr,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Origin': 'https://bigquant.com',
    'Upgrade': 'websocket',
    'Connection': 'Upgrade'
  }
});

let msgCount = 0;

ws.on('open', () => {
  console.log('✓ WebSocket 已连接');
  
  // VS Code server 握手：发送 reconnectionToken
  // 格式参考 VS Code source: src/vs/server/node/remoteExtensionHostAgentServer.ts
  setTimeout(() => {
    // 尝试发送 JSON-RPC 消息
    const msg = JSON.stringify({
      type: 'auth',
      auth: cookieStr.match(/bigjwt=([^;]+)/)?.[1] || ''
    });
    console.log('发送 auth 消息...');
    ws.send(msg);
  }, 1000);
});

ws.on('message', (data) => {
  msgCount++;
  const raw = data.toString();
  console.log(`[${msgCount}] 收到消息 (${data.length} bytes):`, raw.slice(0, 200));
  
  if (msgCount >= 5) {
    console.log('收到足够消息，关闭连接');
    ws.close();
  }
});

ws.on('error', (err) => {
  console.error('WebSocket 错误:', err.message);
});

ws.on('close', (code, reason) => {
  console.log('WebSocket 关闭:', code, reason.toString());
  process.exit(0);
});

setTimeout(() => {
  console.log('超时，关闭');
  ws.close();
  process.exit(0);
}, 10000);

#!/usr/bin/env node
/**
 * 解码 VS Code WebSocket 二进制帧格式
 * 参考: https://github.com/microsoft/vscode/blob/main/src/vs/base/parts/ipc/common/ipc.net.ts
 */
import './load-env.js';
import { SESSION_FILE } from './paths.js';
import { WebSocket } from 'ws';
import fs from 'fs';

const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
const cookieStr = session.cookies.filter(c => c.domain.includes('bigquant')).map(c => `${c.name}=${c.value}`).join('; ');
const studioId = 'e6277718-0f37-11ed-93bb-da75731aa77c';

// 获取最新的 stable hash
async function getStableHash() {
  const r = await fetch(`https://bigquant.com/aistudio/studios/${studioId}/proxy/8888/version`, {
    headers: { 'Cookie': cookieStr }
  });
  return await r.text();
}

const hash = await getStableHash();
console.log('Stable hash:', hash);

const wsUrl = `wss://bigquant.com/aistudio/studios/${studioId}/stable-${hash}?reconnectionToken=${Date.now()}&reconnection=false&skipWebSocketFrames=false`;
console.log('WS URL:', wsUrl.slice(-80));

const ws = new WebSocket(wsUrl, {
  headers: {
    'Cookie': cookieStr,
    'User-Agent': 'Mozilla/5.0',
    'Origin': 'https://bigquant.com'
  }
});

let msgCount = 0;
const messages = [];

ws.on('open', () => {
  console.log('✓ 已连接');
});

ws.on('message', (data, isBinary) => {
  msgCount++;
  const buf = Buffer.isBuffer(data) ? data : Buffer.from(data);
  
  console.log(`\n[${msgCount}] ${isBinary ? 'binary' : 'text'} ${buf.length} bytes`);
  console.log('  hex:', buf.slice(0, 32).toString('hex'));
  console.log('  ascii:', buf.slice(0, 64).toString('ascii').replace(/[^\x20-\x7e]/g, '.'));
  
  // VS Code IPC 帧格式:
  // byte 0: type (0=regular, 1=control)
  // bytes 1-4: id (uint32 LE)
  // bytes 5-8: ack (uint32 LE)
  // bytes 9-12: length (uint32 LE)
  // bytes 13+: data
  if (buf.length >= 13) {
    const type = buf[0];
    const id = buf.readUInt32LE(1);
    const ack = buf.readUInt32LE(5);
    const len = buf.readUInt32LE(9);
    console.log(`  type=${type} id=${id} ack=${ack} len=${len}`);
    if (len > 0 && buf.length >= 13 + len) {
      const payload = buf.slice(13, 13 + len);
      console.log('  payload hex:', payload.slice(0, 32).toString('hex'));
      try {
        const text = payload.toString('utf8');
        if (text.startsWith('{') || text.startsWith('[')) {
          console.log('  payload JSON:', text.slice(0, 200));
        } else {
          console.log('  payload ascii:', text.slice(0, 100).replace(/[^\x20-\x7e]/g, '.'));
        }
      } catch(e) {}
    }
  }
  
  messages.push({ binary: isBinary, hex: buf.toString('hex'), length: buf.length });
  
  if (msgCount >= 3) {
    fs.writeFileSync('./data/vscode-frames.json', JSON.stringify(messages, null, 2));
    console.log('\n已保存帧数据到 data/vscode-frames.json');
    ws.close();
  }
});

ws.on('error', err => console.error('错误:', err.message));
ws.on('close', (code) => { console.log('关闭:', code); process.exit(0); });
setTimeout(() => { ws.close(); process.exit(0); }, 15000);

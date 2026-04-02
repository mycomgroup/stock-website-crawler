#!/usr/bin/env node
/**
 * 直接通过 WebSocket 连接 BigQuant AIStudio
 *
 * BigQuant 使用 VS Code Web (code-server)，任务执行通过 WebSocket 协议。
 * 本脚本尝试：
 * 1. 连接 VS Code WebSocket
 * 2. 探索执行协议
 * 3. 发送执行命令
 */

import WebSocket from 'ws';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function connectWebSocket() {
  const sessionFile = path.join(__dirname, 'data/session.json');
  const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));

  // 从 session 中获取认证信息
  const bigjwt = session.cookies.find(c => c.name === 'bigjwt');
  if (!bigjwt) {
    console.error('No bigjwt cookie found');
    return;
  }

  // Studio ID
  const studioId = 'e6277718-0f37-11ed-93bb-da75731aa77c';

  // WebSocket URL (从捕获的请求中获得)
  // stable-{hash} 是版本标识
  const wsUrl = `wss://bigquant.com/aistudio/studios/${studioId}/stable-fb2afbd9d62532be3952118adafff3972c63f3bc?reconnection=false&skipWebSocketFrames=false`;

  console.log('Connecting to:', wsUrl);

  // 创建 WebSocket 连接
  const ws = new WebSocket(wsUrl, {
    headers: {
      'Cookie': `bigjwt=${bigjwt.value}`,
      'Origin': 'https://bigquant.com',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
  });

  const messages = [];

  ws.on('open', () => {
    console.log('\n=== WebSocket Connected ===');
    console.log('Ready to receive messages...');
  });

  ws.on('message', (data) => {
    const msg = data.toString();
    const timestamp = new Date().toISOString();

    messages.push({ timestamp, data: msg.substring(0, 2000) });

    // 尝试解析消息
    try {
      const parsed = JSON.parse(msg);
      console.log('\n[Received]', JSON.stringify(parsed, null, 2).substring(0, 500));

      // VS Code 协议消息类型
      if (parsed.type) {
        console.log('Message type:', parsed.type);
      }

      // 检查是否有执行相关的消息
      if (parsed.method || parsed.command) {
        console.log('Method/Command:', parsed.method || parsed.command);
      }

    } catch (e) {
      // 非 JSON 消息
      console.log('\n[Raw]', msg.substring(0, 300));
    }
  });

  ws.on('error', (err) => {
    console.error('WebSocket error:', err.message);
  });

  ws.on('close', () => {
    console.log('\n=== WebSocket Closed ===');

    // 保存消息记录
    const outputPath = path.join(__dirname, 'data/websocket-messages.json');
    fs.writeFileSync(outputPath, JSON.stringify(messages, null, 2));
    console.log('Messages saved to:', outputPath);
  });

  // 等待收集消息
  console.log('\nListening for 30 seconds...');
  console.log('Press Ctrl+C to stop early\n');

  await new Promise(r => setTimeout(r, 30000));

  // 尝试发送一些探索性消息
  console.log('\n=== Sending exploratory messages ===');

  // VS Code 协议格式
  const testMessages = [
    // 初始化请求
    { type: 'request', seq: 1, command: 'initialize', arguments: {} },
    // 获取任务列表
    { type: 'request', seq: 2, command: 'bigquant.tasks', arguments: {} },
    // 运行任务
    { type: 'request', seq: 3, command: 'bigquant.run', arguments: { taskId: 'test' } }
  ];

  for (const msg of testMessages) {
    console.log('Sending:', JSON.stringify(msg));
    ws.send(JSON.stringify(msg));
    await new Promise(r => setTimeout(r, 1000));
  }

  // 再等待一下看响应
  await new Promise(r => setTimeout(r, 5000));

  ws.close();
}

connectWebSocket().catch(console.error);
#!/usr/bin/env node
/**
 * VS Code WebSocket Protocol Handler
 *
 * VS Code Web (code-server) 使用特定的 WebSocket 协议:
 * 1. 消息格式: Content-Length header + JSON body
 * 2. 需要特定的握手序列
 * 3. 支持请求/响应模式
 */

import WebSocket from 'ws';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// VS Code WebSocket 消息编码
function encodeMessage(json) {
  const content = JSON.stringify(json);
  const length = Buffer.byteLength(content, 'utf8');

  // VS Code 协议格式: Content-Length header + \r\n\r\n + body
  const header = `Content-Length: ${length}\r\n\r\n`;
  return header + content;
}

// VS Code WebSocket 消息解码
function decodeMessage(data) {
  const str = data.toString('utf8');

  // 检查是否是 Content-Length 格式
  if (str.startsWith('Content-Length:')) {
    const headerEnd = str.indexOf('\r\n\r\n');
    if (headerEnd !== -1) {
      const header = str.substring(0, headerEnd);
      const lengthMatch = header.match(/Content-Length: (\d+)/);
      if (lengthMatch) {
        const length = parseInt(lengthMatch[1]);
        const bodyStart = headerEnd + 4;
        const body = str.substring(bodyStart, bodyStart + length);
        return JSON.parse(body);
      }
    }
  }

  // 尝试直接解析 JSON
  try {
    return JSON.parse(str);
  } catch (e) {
    // 可能是二进制 ping/pong
    return { raw: str.substring(0, 100) };
  }
}

async function connectVSCodeWebSocket() {
  const sessionFile = path.join(__dirname, 'data/session.json');
  const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));

  const bigjwt = session.cookies.find(c => c.name === 'bigjwt');
  if (!bigjwt) {
    console.error('No bigjwt cookie found');
    return;
  }

  const studioId = 'e6277718-0f37-11ed-93bb-da75731aa77c';

  // WebSocket URL
  const wsUrl = `wss://bigquant.com/aistudio/studios/${studioId}/stable-fb2afbd9d62532be3952118adafff3972c63f3bc?reconnection=false&skipWebSocketFrames=false`;

  console.log('Connecting to VS Code WebSocket...');
  console.log('URL:', wsUrl);

  const ws = new WebSocket(wsUrl, {
    headers: {
      'Cookie': `bigjwt=${bigjwt.value}`,
      'Origin': 'https://bigquant.com',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
  });

  const messages = [];
  let messageSeq = 1;

  ws.on('open', async () => {
    console.log('\n=== WebSocket Connected ===');

    // VS Code 协议握手
    // 参考: https://code.visualstudio.com/api/extension-guides/remote-extensions

    console.log('\nSending handshake...');

    // 发送初始化请求 (VS Code Debug Adapter Protocol 格式)
    const initRequest = {
      seq: messageSeq++,
      type: 'request',
      command: 'initialize',
      arguments: {
        clientID: 'bigquant-cli',
        adapterID: 'bigquant',
        pathFormat: 'path',
        linesStartAt1: true,
        columnsStartAt1: true,
        supportsVariableType: true,
        supportsVariablePaging: true,
        supportsRunInTerminalRequest: true,
        locale: 'en-us'
      }
    };

    ws.send(encodeMessage(initRequest));
    console.log('Sent: initialize');

    await new Promise(r => setTimeout(r, 1000));

    // 尝试 BigQuant 特定命令
    const commands = [
      // 尝试获取任务
      { seq: messageSeq++, type: 'request', command: 'bigquant.getTasks', arguments: {} },
      // 尝试运行
      { seq: messageSeq++, type: 'request', command: 'bigquant.runTask', arguments: {} },
      // 尝试获取状态
      { seq: messageSeq++, type: 'request', command: 'bigquant.getStatus', arguments: {} },
    ];

    for (const cmd of commands) {
      console.log(`\nSending command: ${cmd.command}`);
      ws.send(encodeMessage(cmd));
      await new Promise(r => setTimeout(r, 500));
    }
  });

  ws.on('message', (data) => {
    const decoded = decodeMessage(data);
    const timestamp = new Date().toISOString();

    messages.push({ timestamp, decoded });

    console.log('\n[Received]', JSON.stringify(decoded, null, 2).substring(0, 500));

    // 处理响应
    if (decoded.type === 'response') {
      console.log('Response to:', decoded.request_seq);
      console.log('Command:', decoded.command);
      console.log('Success:', decoded.success);
      if (decoded.body) {
        console.log('Body:', JSON.stringify(decoded.body, null, 2).substring(0, 500));
      }
    }

    // 处理事件
    if (decoded.type === 'event') {
      console.log('Event:', decoded.event);
      if (decoded.body) {
        console.log('Body:', JSON.stringify(decoded.body, null, 2).substring(0, 500));
      }
    }
  });

  ws.on('error', (err) => {
    console.error('WebSocket error:', err.message);
  });

  ws.on('close', (code, reason) => {
    console.log('\n=== WebSocket Closed ===');
    console.log('Code:', code);
    console.log('Reason:', reason.toString());

    const outputPath = path.join(__dirname, 'data/vscode-websocket-messages.json');
    fs.writeFileSync(outputPath, JSON.stringify(messages, null, 2));
    console.log('Messages saved to:', outputPath);
  });

  // 等待收集响应
  console.log('\nListening for responses (30 seconds)...');
  await new Promise(r => setTimeout(r, 30000));

  ws.close();
}

connectVSCodeWebSocket().catch(console.error);
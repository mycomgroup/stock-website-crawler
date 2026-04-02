#!/usr/bin/env node
/**
 * 深度捕获 WebSocket 消息帧
 *
 * 使用 Playwright 打开 AIStudio，捕获完整的 WebSocket 消息内容。
 */

import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function captureWebSocketFrames() {
  const sessionFile = path.join(__dirname, 'data/session.json');
  const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  await context.addCookies(session.cookies);

  const page = await context.newPage();

  const wsFrames = [];
  const wsConnections = [];

  // 捕获 WebSocket 连接
  page.on('websocket', ws => {
    const wsUrl = ws.url();
    console.log('\n=== WebSocket Connected ===');
    console.log('URL:', wsUrl);

    wsConnections.push({
      url: wsUrl,
      timestamp: new Date().toISOString()
    });

    // 捕获发送的消息
    ws.on('frames-sent', frames => {
      for (const frame of frames) {
        const content = frame.payload;
        wsFrames.push({
          direction: 'sent',
          url: wsUrl,
          timestamp: new Date().toISOString(),
          payload: typeof content === 'string' ? content.substring(0, 5000) : '[binary]',
          payloadRaw: content
        });
        console.log('\n[SENT]', content.substring(0, 500));
      }
    });

    // 捕获接收的消息
    ws.on('frames-received', frames => {
      for (const frame of frames) {
        const content = frame.payload;
        wsFrames.push({
          direction: 'received',
          url: wsUrl,
          timestamp: new Date().toISOString(),
          payload: typeof content === 'string' ? content.substring(0, 5000) : '[binary]',
          payloadRaw: content
        });

        // 打印非 ping 消息
        if (typeof content === 'string' && content.length > 20) {
          console.log('\n[RECV]', content.substring(0, 500));
        }

        // 尝试解析 JSON
        if (typeof content === 'string' && content.startsWith('{')) {
          try {
            const parsed = JSON.parse(content);
            console.log('Parsed:', JSON.stringify(parsed, null, 2).substring(0, 500));
          } catch (e) {}
        }
      }
    });

    ws.on('close', () => {
      console.log('\nWebSocket Closed:', wsUrl);
    });

    ws.on('error', err => {
      console.log('\nWebSocket Error:', err);
    });
  });

  // 捕获 HTTP 请求
  page.on('request', request => {
    const url = request.url();
    if (url.includes('/aiflow/') || url.includes('/taskrun') || url.includes('/run')) {
      console.log('\n[HTTP]', request.method(), url.substring(0, 100));
      if (request.postData()) {
        console.log('  Body:', request.postData().substring(0, 300));
      }
    }
  });

  page.on('response', async response => {
    const url = response.url();
    if (url.includes('/aiflow/') || url.includes('/taskrun') || url.includes('/run')) {
      try {
        const body = await response.text();
        if (body.length < 5000) {
          console.log('  <- Response:', body.substring(0, 300));
        }
      } catch (e) {}
    }
  });

  // 打开 AIStudio
  const studioId = 'e6277718-0f37-11ed-93bb-da75731aa77c';
  console.log('\n=== 打开 AIStudio ===');
  await page.goto(`https://bigquant.com/aistudio/studios/${studioId}/`, { waitUntil: 'networkidle' });

  console.log('\n页面加载完成，请在浏览器中：');
  console.log('1. 打开一个已有的策略文件 (.ipynb)');
  console.log('2. 点击运行按钮（通常是 Ctrl+Enter 或工具栏的运行按钮）');
  console.log('3. 等待策略执行完成');
  console.log('\n按 Ctrl+C 结束捕获...\n');

  // 等待用户操作 (5分钟)
  await page.waitForTimeout(300000);

  // 保存结果
  const outputPath = path.join(__dirname, 'data/websocket-capture-full.json');
  fs.writeFileSync(outputPath, JSON.stringify({
    connections: wsConnections,
    frames: wsFrames
  }, null, 2));
  console.log('\n捕获结果已保存到:', outputPath);

  await browser.close();
}

captureWebSocketFrames().catch(console.error);
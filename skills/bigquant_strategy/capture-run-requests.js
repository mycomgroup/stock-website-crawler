#!/usr/bin/env node
/**
 * 捕获 AIStudio 运行任务的网络请求
 *
 * 使用 Playwright 打开 AIStudio，监听所有网络请求
 */

import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function captureNetwork() {
  const sessionFile = path.join(__dirname, 'data/session.json');
  const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  await context.addCookies(session.cookies);

  const page = await context.newPage();

  // 捕获所有请求
  const requests = [];

  page.on('request', request => {
    const url = request.url();
    const method = request.method();

    // 只记录 API 请求
    if (url.includes('/bigapis/') || url.includes('/aistudio/') ||
        url.includes('websocket') || url.includes('ws://') || url.includes('wss://')) {
      const req = {
        timestamp: new Date().toISOString(),
        method,
        url,
        postData: request.postData()?.substring(0, 1000),
        headers: request.headers()
      };
      requests.push(req);
      console.log(`[${method}] ${url.substring(0, 100)}`);

      if (req.postData) {
        console.log(`  Body: ${req.postData.substring(0, 200)}`);
      }
    }
  });

  page.on('response', async response => {
    const url = response.url();

    if (url.includes('/bigapis/') || url.includes('/aistudio/')) {
      try {
        const body = await response.text();
        if (body && body.length > 0 && body.length < 5000) {
          console.log(`  <- Response: ${body.substring(0, 300)}`);

          const req = requests.find(r => r.url === url && !r.response);
          if (req) {
            req.response = body.substring(0, 2000);
          }
        }
      } catch (e) {}
    }
  });

  // 监听 WebSocket
  page.on('websocket', ws => {
    console.log('\n=== WebSocket 连接 ===');
    console.log('URL:', ws.url());

    ws.on('frames-received', frames => {
      for (const frame of frames) {
        console.log('WS Frame:', frame.payload?.substring(0, 500));
      }
    });

    ws.on('close', () => console.log('WS Closed'));
  });

  // 打开 AIStudio
  console.log('\n=== 打开 AIStudio ===');
  const studioId = 'e6277718-0f37-11ed-93bb-da75731aa77c';
  await page.goto(`https://bigquant.com/aistudio/studios/${studioId}/`, { waitUntil: 'networkidle' });

  console.log('\n页面加载完成，请在浏览器中操作：');
  console.log('1. 创建或打开一个策略');
  console.log('2. 点击运行按钮');
  console.log('3. 观察终端输出的 API 请求');
  console.log('\n按 Ctrl+C 结束捕获...\n');

  // 等待用户操作
  await page.waitForTimeout(300000); // 5分钟

  // 保存结果
  const outputPath = path.join(__dirname, 'data/captured-run-requests.json');
  fs.writeFileSync(outputPath, JSON.stringify(requests, null, 2));
  console.log('\n捕获的请求已保存到:', outputPath);

  await browser.close();
}

captureNetwork().catch(console.error);
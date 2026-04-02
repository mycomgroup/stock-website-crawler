#!/usr/bin/env node
/**
 * 探索 BigQuant 任务触发方法
 *
 * 目标：找到触发 manual 队列执行的方法
 */

import './load-env.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function exploreTrigger() {
  const client = new BigQuantAPIClient();

  console.log('='.repeat(60));
  console.log('BigQuant 任务触发探索');
  console.log('='.repeat(60));

  // ========================================
  // 1. 查看队列状态
  // ========================================
  console.log('\n[1] 探索队列 API...');

  const queueEndpoints = [
    '/aiflow/v1/queues',
    '/aiflow/v1/queues/manual',
    '/aiflow/v1/queues/dailyflow',
    '/aiflow/v1/taskruns/queues',
  ];

  for (const ep of queueEndpoints) {
    try {
      const result = await client.request('GET', ep);
      if (result.data || result.items) {
        console.log(`✓ GET ${ep}:`);
        console.log('  响应:', JSON.stringify(result).substring(0, 500));
      }
    } catch (e) {
      const status = e.message.match(/Request failed (\d+)/)?.[1];
      if (status !== '404') {
        console.log(`? GET ${ep}: ${status}`);
      }
    }
  }

  // ========================================
  // 2. 探索任务执行相关端点
  // ========================================
  console.log('\n[2] 探索任务执行端点...');

  const tasks = await client.listTasks({ size: 1 });
  const taskId = tasks.data?.items?.[0]?.id;

  const executeEndpoints = [
    { method: 'POST', path: `/aiflow/v1/tasks/${taskId}/execute`, body: {} },
    { method: 'POST', path: `/aiflow/v1/tasks/${taskId}/start`, body: {} },
    { method: 'POST', path: `/aiflow/v1/tasks/${taskId}/trigger`, body: {} },
    { method: 'POST', path: `/aiflow/v1/tasks/${taskId}/dispatch`, body: {} },
    { method: 'POST', path: `/aiflow/v1/tasks/${taskId}/schedule`, body: {} },
    { method: 'PUT', path: `/aiflow/v1/tasks/${taskId}`, body: { status: 'running' } },
    { method: 'PATCH', path: `/aiflow/v1/tasks/${taskId}`, body: { status: 'running' } },
    { method: 'POST', path: `/aiflow/v1/executions`, body: { task_id: taskId } },
    { method: 'POST', path: `/aiflow/v1/runs`, body: { task_id: taskId } },
  ];

  for (const ep of executeEndpoints) {
    try {
      const result = await client.request(ep.method, ep.path, ep.body);
      console.log(`✓ ${ep.method} ${ep.path}: 成功!`);
      console.log('  响应:', JSON.stringify(result).substring(0, 300));
    } catch (e) {
      const status = e.message.match(/Request failed (\d+)/)?.[1];
      if (status && status !== '404' && status !== '405') {
        console.log(`? ${ep.method} ${ep.path}: ${status}`);
      }
    }
  }

  // ========================================
  // 3. 浏览器自动化探索 - 查看网络请求
  // ========================================
  console.log('\n[3] 浏览器自动化探索 - 捕获运行请求...');

  const sessionFile = path.join(__dirname, 'data/session.json');
  const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  await context.addCookies(session.cookies);

  const page = await context.newPage();

  // 捕获所有请求
  const capturedRequests = [];

  page.on('request', request => {
    const url = request.url();
    const method = request.method();
    if (url.includes('aiflow') || url.includes('taskrun') || url.includes('execute') || url.includes('run')) {
      capturedRequests.push({
        method,
        url,
        postData: request.postData()?.substring(0, 500)
      });
      console.log(`[请求] ${method} ${url.substring(0, 80)}`);
    }
  });

  page.on('response', async response => {
    const url = response.url();
    const status = response.status();
    if (url.includes('aiflow') || url.includes('taskrun')) {
      try {
        const body = await response.text();
        console.log(`[响应 ${status}] ${url.substring(0, 60)}`);
        capturedRequests.find(r => r.url === url)?.responseBody = body.substring(0, 500);
      } catch (e) {}
    }
  });

  // 打开任务页面
  const studioId = 'e6277718-0f37-11ed-93bb-da75731aa77c';
  const webUrl = `https://bigquant.com/aistudio/studios/${studioId}/?task=${taskId}`;
  console.log('打开:', webUrl);

  await page.goto(webUrl, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(5000);

  // 尝试各种运行方式
  console.log('\n尝试运行快捷键...');

  // Ctrl+Enter 运行单元格
  await page.keyboard.down('Control');
  await page.keyboard.press('Enter');
  await page.keyboard.up('Control');
  await page.waitForTimeout(3000);

  // Ctrl+Shift+A 运行全部
  await page.keyboard.down('Control');
  await page.keyboard.down('Shift');
  await page.keyboard.press('KeyA');
  await page.keyboard.up('Shift');
  await page.keyboard.up('Control');
  await page.waitForTimeout(3000);

  // F5 运行
  await page.keyboard.press('F5');
  await page.waitForTimeout(5000);

  // 尝试命令面板
  console.log('尝试命令面板...');
  await page.keyboard.down('Control');
  await page.keyboard.down('Shift');
  await page.keyboard.press('KeyP');
  await page.keyboard.up('Shift');
  await page.keyboard.up('Control');
  await page.waitForTimeout(1000);

  await page.keyboard.type('Run Task');
  await page.waitForTimeout(1000);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(5000);

  // 等待用户手动操作
  console.log('\n请在浏览器中手动尝试运行任务（点击运行按钮）...');
  console.log('等待 30 秒捕获网络请求...');
  await page.waitForTimeout(30000);

  // 保存截图
  await page.screenshot({ path: path.join(__dirname, 'data/trigger-explore.png'), fullPage: true });

  await browser.close();

  // 保存捕获的请求
  fs.writeFileSync(
    path.join(__dirname, 'data/trigger-captured-requests.json'),
    JSON.stringify(capturedRequests, null, 2)
  );

  console.log('\n捕获的请求数量:', capturedRequests.length);
  console.log('保存到: data/trigger-captured-requests.json');

  // 分析请求
  console.log('\n[4] 分析捕获的请求...');
  const postRequests = capturedRequests.filter(r => r.method === 'POST');
  console.log('POST 请求:', postRequests.length);

  for (const req of postRequests) {
    console.log('\n', req.method, req.url.substring(0, 100));
    if (req.postData) {
      console.log('Body:', req.postData.substring(0, 200));
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log('探索完成');
  console.log('='.repeat(60));
}

exploreTrigger().catch(console.error);
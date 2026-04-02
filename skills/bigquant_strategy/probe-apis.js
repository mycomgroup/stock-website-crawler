#!/usr/bin/env node
/**
 * 探测 BigQuant 可用 API
 * 运行: node probe-apis.js
 */

import './load-env.js';
import { ensureSession } from './request/bigquant-auth.js';
import { BigQuantRunner } from './request/bigquant-runner.js';

async function probe() {
  console.log('='.repeat(60));
  console.log('BigQuant API 探测');
  console.log('='.repeat(60));

  // 1. 登录
  console.log('\n[1] 登录...');
  const session = await ensureSession({
    username: process.env.BIGQUANT_USERNAME,
    password: process.env.BIGQUANT_PASSWORD
  });
  console.log('✓ 用户:', session.username, '| ID:', session.userId);

  const runner = new BigQuantRunner(session);

  // 2. 激活 Studio
  console.log('\n[2] 激活 Studio...');
  await runner.activateStudio();

  // 3. 探测 Jupyter API
  console.log('\n[3] 探测 Jupyter API...');
  const endpoints = [
    '/api/kernels',
    '/api/sessions',
    '/api/contents',
    '/api/contents/work',
    '/api/spec.yaml',
    '/api/status'
  ];

  for (const ep of endpoints) {
    try {
      const result = await runner.jupyterRequest('GET', ep);
      const preview = JSON.stringify(result).slice(0, 120);
      console.log(`  ✓ GET ${ep}: ${preview}`);
    } catch (e) {
      const status = e.message.match(/HTTP (\d+)/)?.[1] || 'err';
      console.log(`  ✗ GET ${ep}: ${status}`);
    }
  }

  // 4. 探测 userbox API
  console.log('\n[4] 探测 userbox API...');
  const userboxEndpoints = [
    '/bigapis/userbox/v1/workspaces/',
    '/bigapis/userbox/v1/workspaces',
    `/bigapis/userbox/v1/workspaces/${session.userId}`,
  ];

  for (const ep of userboxEndpoints) {
    try {
      const result = await runner.request('GET', ep);
      console.log(`  ✓ GET ${ep}: ${JSON.stringify(result).slice(0, 200)}`);
    } catch (e) {
      const status = e.message.match(/HTTP (\d+)/)?.[1] || 'err';
      console.log(`  ✗ GET ${ep}: ${status}`);
    }
  }

  // 5. 列出现有 tasks
  console.log('\n[5] 列出现有 tasks...');
  const tasks = await runner.listTasks(5);
  const items = tasks.data?.items || [];
  console.log(`  共 ${items.length} 个 tasks:`);
  for (const t of items) {
    console.log(`  - ${t.name} (${t.id}) state=${t.last_run?.state || 'none'}`);
  }

  // 6. 如果有已完成的 task，尝试读取 outputs
  const successTask = items.find(t => t.last_run?.state === 'success');
  if (successTask) {
    console.log(`\n[6] 读取已完成 task 的 outputs: ${successTask.name}`);
    const outputs = await runner.readTaskOutputs(successTask.id);
    console.log(`  outputs 数量: ${outputs.length}`);
    if (outputs.length > 0) {
      console.log('  第一个 output:', JSON.stringify(outputs[0]).slice(0, 200));
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log('探测完成');
}

probe().catch(console.error);

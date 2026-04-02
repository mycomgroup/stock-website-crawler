/**
 * BigQuant 策略工作流 - 对齐 JoinQuant 接口
 */

import fs from 'node:fs';
import '../load-env.js';
import { ensureSession } from './bigquant-auth.js';
import { BigQuantRunner } from './bigquant-runner.js';

export async function runStrategyWorkflow(options = {}) {
  const {
    strategyId,
    codeFilePath,
    startTime,
    endTime,
    baseCapital,
    frequency = 'day',
    benchmark = '000300.XSHG'
  } = options;

  if (!codeFilePath || !fs.existsSync(codeFilePath)) {
    throw new Error(`策略文件不存在: ${codeFilePath}`);
  }

  const code = fs.readFileSync(codeFilePath, 'utf8');
  const name = options.name || codeFilePath.split('/').pop().replace('.py', '');

  // 1. 确保 session 有效（自动登录）
  const session = await ensureSession({
    username: process.env.BIGQUANT_USERNAME,
    password: process.env.BIGQUANT_PASSWORD
  });

  // 2. 如果指定了 studioId，覆盖默认值
  if (strategyId) {
    process.env.BIGQUANT_STUDIO_ID = strategyId;
  }

  const runner = new BigQuantRunner(session);

  // 3. 运行策略
  const result = await runner.runStrategy(name, code, {
    startDate: startTime || '2023-01-01',
    endDate: endTime || '2023-12-31',
    capital: baseCapital || 100000,
    benchmark,
    frequency
  });

  return {
    success: result.success,
    outputPath: result.outputPath,
    webUrl: result.webUrl,
    summary: result.report?.metrics || result.result || {}
  };
}

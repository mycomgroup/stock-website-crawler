#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function main() {
  console.log('=' * 80);
  console.log('任务05v2：提交卖出规则对比策略到JoinQuant');
  console.log('=' * 80);
  
  // 读取策略代码
  const strategyFile = path.join(__dirname, 'exit_rules_comparison.py');
  const code = fs.readFileSync(strategyFile, 'utf8');
  console.log(`\n读取策略文件: ${strategyFile}`);
  console.log(`策略代码长度: ${code.length} 字符`);
  
  // 检查request模块
  const requestDir = path.join(__dirname, 'request');
  if (!fs.existsSync(requestDir)) {
    console.error('错误: request目录不存在');
    console.log('可用的目录内容:');
    console.log(fs.readdirSync(__dirname));
    process.exit(1);
  }
  
  // 尝试导入JoinQuant客户端
  let JoinQuantStrategyClient, ensureJoinQuantSession;
  try {
    const clientModule = await import('./request/joinquant-strategy-client.js');
    const sessionModule = await import('./request/ensure-session.js');
    JoinQuantStrategyClient = clientModule.JoinQuantStrategyClient;
    ensureJoinQuantSession = sessionModule.ensureJoinQuantSession;
    console.log('✓ 成功导入JoinQuant客户端模块');
  } catch (err) {
    console.error('导入JoinQuant客户端失败:', err.message);
    console.log('\n可用文件:');
    console.log(fs.readdirSync(requestDir));
    process.exit(1);
  }
  
  // 确保session有效
  console.log('\n检查JoinQuant session...');
  try {
    const context = await ensureJoinQuantSession();
    console.log('✓ Session有效');
    console.log('User ID:', context.userId);
    
    // 创建客户端
    const client = new JoinQuantStrategyClient(context);
    
    // 策略名称
    const strategyName = 'exit_rules_comparison_05v2';
    const ALGORITHM_ID = 'test_exit_rules'; // 这个需要是有效的策略ID
    
    console.log(`\n提交策略: ${strategyName}`);
    console.log('注意: 需要手动在JoinQuant平台创建策略或使用现有策略ID');
    
    // 尝试保存策略
    console.log('\n尝试保存策略...');
    try {
      const saveResult = await client.saveStrategy(ALGORITHM_ID, strategyName, code, context);
      console.log('保存结果:', saveResult);
    } catch (err) {
      console.log('保存失败 (可能需要手动创建策略):', err.message);
    }
    
    // 运行回测配置
    const BACKTEST_CONFIG = {
      startTime: '2022-01-01',
      endTime: '2024-12-31',
      baseCapital: '100000',
      frequency: 'day'
    };
    
    // 尝试运行回测
    console.log('\n尝试运行回测...');
    try {
      const buildResult = await client.runBacktest(ALGORITHM_ID, code, BACKTEST_CONFIG, context);
      console.log('回测提交成功!');
      console.log('回测ID:', buildResult.backtestId);
      
      const backtestId = buildResult.backtestId;
      
      // 轮询等待结果
      console.log('\n等待回测完成...');
      let attempts = 0;
      const maxAttempts = 120; // 最多等10分钟
      
      while (attempts < maxAttempts) {
        await new Promise(resolve => setTimeout(resolve, 5000));
        attempts++;
        
        try {
          const result = await client.getBacktestResult(backtestId, context);
          const bt = result.data?.result?.backtest || {};
          
          process.stdout.write(`\r[${attempts}/${maxAttempts}] Status: ${bt.status || 'unknown'}, Progress: ${bt.progress || 0}%`);
          
          if (bt.finished_time || bt.status === 'finished') {
            console.log('\n\n✓ 回测完成!');
            console.log('\n结果摘要:');
            console.log('- 状态:', bt.status);
            console.log('- 完成时间:', bt.finished_time);
            
            // 获取日志输出
            if (result.data?.result?.log) {
              console.log('\n日志输出:');
              console.log(result.data.result.log);
            }
            
            return;
          }
          
          if (bt.status === 'failed') {
            console.log('\n\n✗ 回测失败');
            console.log('错误:', result.message || '未知错误');
            return;
          }
        } catch (err) {
          console.log(`\n轮询错误 (${attempts}/${maxAttempts}):`, err.message);
        }
      }
      
      console.log('\n\n超时: 回测未在预期时间内完成');
      console.log('回测ID:', backtestId);
      console.log('请在JoinQuant平台手动查看结果');
      
    } catch (err) {
      console.log('运行回测失败:', err.message);
      console.log('\n请手动在JoinQuant平台运行策略:');
      console.log('1. 访问 https://www.joinquant.com/');
      console.log('2. 登录账号');
      console.log('3. 策略编辑器 -> 新建策略');
      console.log('4. 复制策略代码并运行');
    }
    
  } catch (err) {
    console.error('Session获取失败:', err.message);
    console.log('\n请确保:');
    console.log('1. 已配置.env文件 (JOINQUANT_USERNAME, JOINQUANT_PASSWORD)');
    console.log('2. 手动登录JoinQuant并保持session有效');
    process.exit(1);
  }
}

main().catch(err => {
  console.error('执行失败:', err);
  process.exit(1);
});
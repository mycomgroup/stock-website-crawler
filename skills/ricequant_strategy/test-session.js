#!/usr/bin/env node
/**
 * Session 管理测试脚本
 * 
 * 测试内容：
 * 1. 检查现有 session 是否有效
 * 2. 如果有效，直接使用
 * 3. 如果无效，自动登录获取新 session（headless模式）
 */

import { ensureRiceQuantNotebookSession } from './request/ensure-ricequant-notebook-session.js';
import { RiceQuantNotebookClient } from './request/ricequant-notebook-client.js';

async function testSessionManagement() {
  console.log('=== RiceQuant Session 管理测试 ===\n');
  
  try {
    const notebookUrl = process.env.RICEQUANT_NOTEBOOK_URL;
    
    if (!notebookUrl) {
      throw new Error('请设置 RICEQUANT_NOTEBOOK_URL 环境变量');
    }
    
    console.log(`Notebook URL: ${notebookUrl}\n`);
    
    // 测试 session 管理
    console.log('步骤 1: 检查 session 状态...\n');
    const sessionResult = await ensureRiceQuantNotebookSession({
      notebookUrl,
      headless: true
    });
    
    console.log('\n步骤 2: Session 管理结果:');
    console.log(`  状态: ${sessionResult.refreshed ? '新建' : '复用'}`);
    console.log(`  原因: ${sessionResult.reason}`);
    console.log(`  文件: ${sessionResult.sessionFile}`);
    
    // 测试使用 session
    console.log('\n步骤 3: 测试使用 session...');
    const client = new RiceQuantNotebookClient({
      notebookUrl,
      outputRoot: './data'
    });
    
    const metadata = await client.getNotebookMetadata();
    console.log(`✓ Session 有效，可以访问 notebook`);
    console.log(`  Notebook 路径: ${metadata.path}`);
    console.log(`  最后修改: ${metadata.last_modified}`);
    
    console.log('\n=== 测试成功 ===');
    console.log('Session 管理正常工作！');
    
    process.exit(0);
    
  } catch (error) {
    console.error('\n=== 测试失败 ===');
    console.error(`错误: ${error.message}`);
    console.error('\n可能的原因:');
    console.error('1. RICEQUANT_NOTEBOOK_URL 未设置');
    console.error('2. RICEQUANT_USERNAME 或 RICEQUANT_PASSWORD 未设置');
    console.error('3. 网络连接问题');
    console.error('4. RiceQuant 平台问题');
    
    process.exit(1);
  }
}

testSessionManagement();
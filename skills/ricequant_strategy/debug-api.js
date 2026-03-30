import './load-env.js';
import { RiceQuantClient } from './request/ricequant-client.js';
import { ensureRiceQuantSession } from './browser/session-manager.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TRACES_FILE = path.join(__dirname, 'data', 'api_traces.json');

async function main() {
  console.log('=== RiceQuant API Debug ===\n');
  
  // 1. 检查 session
  console.log('1. Checking session...');
  const credentials = {
    username: process.env.RICEQUANT_USERNAME,
    password: process.env.RICEQUANT_PASSWORD
  };
  
  const cookies = await ensureRiceQuantSession(credentials);
  console.log(`Session cookies: ${cookies.length}`);
  
  // 2. 打印 cookie 详情
  console.log('\n2. Cookie details:');
  cookies.forEach(c => {
    console.log(`  ${c.name}: ${c.value.substring(0, 30)}...`);
    console.log(`    domain: ${c.domain}, path: ${c.path}`);
    console.log(`    httpOnly: ${c.httpOnly}, secure: ${c.secure}, sameSite: ${c.sameSite}`);
  });
  
  const client = new RiceQuantClient({ cookies });
  
  // 3. 测试不同的 API 端点格式
  console.log('\n3. Testing API endpoints...');
  
  const testEndpoints = [
    { method: 'GET', url: '/api/user/v1/workspaces' },
    { method: 'GET', url: '/api/workspace' },
    { method: 'GET', url: '/api/strategies' },
    { method: 'POST', url: '/api/workspace/list', body: '{}' },
    { method: 'GET', url: '/workspace/api/strategies' },
  ];
  
  for (const test of testEndpoints) {
    console.log(`\n  ${test.method} ${test.url}`);
    try {
      const result = await client.request(test.url, {
        method: test.method,
        body: test.body,
        headers: test.body ? { 'Content-Type': 'application/json' } : {}
      });
      
      if (typeof result === 'string') {
        console.log(`    => HTML response (${result.length} bytes)`);
      } else {
        console.log(`    => ${JSON.stringify(result).substring(0, 100)}`);
      }
    } catch (e) {
      console.log(`    => Error: ${e.message.substring(0, 100)}`);
    }
  }
  
  // 4. 尝试直接访问 workspace 页面
  console.log('\n4. Checking workspace page...');
  try {
    const html = await client.request('/workspace');
    console.log(`    => HTML response (${html.length} bytes)`);
    
    // 提取 API 相关的 JS 文件
    const jsFiles = html.match(/src="(https:\/\/assets\.ricequant\.com\/[^"]+\.js)"/g) || [];
    console.log(`    Found ${jsFiles.length} JS files`);
    
    // 保存 HTML 用于分析
    fs.writeFileSync(path.join(__dirname, 'data', 'workspace_page.html'), html);
    console.log('    Saved to data/workspace_page.html');
    
  } catch (e) {
    console.log(`    => Error: ${e.message}`);
  }
  
  // 5. 检查 JWT payload
  console.log('\n5. Analyzing JWT token...');
  const rqjwt = cookies.find(c => c.name === 'rqjwt');
  if (rqjwt) {
    try {
      const parts = rqjwt.value.split('.');
      if (parts.length >= 2) {
        const payload = JSON.parse(Buffer.from(parts[1], 'base64').toString());
        console.log('    JWT payload:', JSON.stringify(payload, null, 4));
        
        const exp = payload.exp;
        const now = Math.floor(Date.now() / 1000);
        const remaining = exp - now;
        console.log(`    Token expires in: ${Math.floor(remaining / 3600)} hours ${Math.floor((remaining % 3600) / 60)} minutes`);
        
        if (remaining < 0) {
          console.log('    WARNING: Token has EXPIRED!');
        }
      }
    } catch (e) {
      console.log('    Could not parse JWT');
    }
  }
  
  console.log('\n=== Debug Complete ===');
  console.log('\nIf APIs still fail, please:');
  console.log('1. Run: node browser/capture-api.js');
  console.log('2. Manually login in the browser window');
  console.log('3. The script will capture the real API calls');
}

main().catch(console.error);
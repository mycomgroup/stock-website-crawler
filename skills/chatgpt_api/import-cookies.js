#!/usr/bin/env node

import { writeFileSync, mkdirSync, existsSync, readFileSync } from 'fs';
import { PATHS } from './paths.js';
import readline from 'readline';

/**
 * 交互式导入 cookies
 */
async function importCookies(accountName) {
  console.log('');
  console.log('🍪 手动导入 Cookies');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('');
  console.log('请按照以下步骤操作：');
  console.log('');
  console.log('1. 在正常浏览器中打开 https://chatgpt.com/ 并登录');
  console.log('2. 按 F12 打开开发者工具，切换到 Console 标签');
  console.log('3. 运行以下代码：');
  console.log('');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`
copy(JSON.stringify(document.cookie.split('; ').map(c => {
  const [name, ...v] = c.split('=');
  return {
    name,
    value: v.join('='),
    domain: '.chatgpt.com',
    path: '/',
    secure: true,
    httpOnly: false,
    sameSite: 'Lax'
  };
}).filter(c => c.name.includes('auth') || c.name.includes('session') || c.name.includes('cf') || c.name.includes('token') || c.name.includes('Secure')), null, 2));
console.log('✅ Cookies 已复制到剪贴板');
  `);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('');
  console.log('4. 复制后，粘贴到下面（按 Ctrl+D 或 Cmd+D 结束输入）：');
  console.log('');

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  let input = '';
  
  return new Promise((resolve, reject) => {
    rl.on('line', (line) => {
      input += line + '\n';
    });

    rl.on('close', () => {
      try {
        // Parse cookies
        const cookies = JSON.parse(input.trim());
        
        if (!Array.isArray(cookies) || cookies.length === 0) {
          throw new Error('无效的 cookies 格式');
        }

        console.log('');
        console.log(`✅ 解析成功，找到 ${cookies.length} 个 cookies`);
        
        // Normalize cookies format
        const normalizedCookies = cookies.map(cookie => {
          // Convert sameSite to standard format
          let sameSite = cookie.sameSite || cookie.SameSite || 'Lax';
          if (typeof sameSite === 'string') {
            sameSite = sameSite.toLowerCase();
            if (sameSite === 'no_restriction') sameSite = 'None';
            if (sameSite === 'unspecified') sameSite = 'Lax';
            // Capitalize first letter
            sameSite = sameSite.charAt(0).toUpperCase() + sameSite.slice(1);
          }
          
          return {
            name: cookie.name,
            value: cookie.value,
            domain: cookie.domain,
            path: cookie.path || '/',
            secure: cookie.secure !== false,
            httpOnly: cookie.httpOnly || false,
            sameSite: sameSite
          };
        });
        
        // Log cookie names
        normalizedCookies.forEach(cookie => {
          console.log(`   - ${cookie.name}`);
        });

        // Create session data
        const sessionData = {
          capturedAt: new Date().toISOString(),
          cookies: normalizedCookies,
          userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
          method: 'manual-import'
        };

        // Ensure directories exist
        const accountsDir = `${PATHS.data}/accounts`;
        if (!existsSync(accountsDir)) {
          mkdirSync(accountsDir, { recursive: true });
        }

        // Save session file
        const accountId = accountName || `account-${Date.now()}`;
        const sessionPath = `${accountsDir}/session-${accountId}.json`;
        
        writeFileSync(sessionPath, JSON.stringify(sessionData, null, 2), 'utf-8');
        
        console.log('');
        console.log(`💾 Session 已保存到: ${sessionPath}`);

        // Update accounts config
        const configFile = `${PATHS.data}/accounts-config.json`;
        let config = { accounts: [], strategy: 'round-robin' };
        
        if (existsSync(configFile)) {
          config = JSON.parse(readFileSync(configFile, 'utf-8'));
        }

        // Add or update account
        const existingIndex = config.accounts.findIndex(a => a.id === accountId);
        const accountConfig = {
          id: accountId,
          name: accountName || accountId,
          enabled: true,
          weight: 1
        };

        if (existingIndex >= 0) {
          config.accounts[existingIndex] = accountConfig;
        } else {
          config.accounts.push(accountConfig);
        }

        writeFileSync(configFile, JSON.stringify(config, null, 2), 'utf-8');

        console.log('');
        console.log('✅ 账号配置已更新');
        console.log('');
        console.log('现在可以使用以下命令测试：');
        console.log(`  node run-skill.js --message "你好" --account ${accountId}`);
        console.log('');
        console.log('或启动多账号服务器：');
        console.log('  USE_MULTI_ACCOUNT=true npm run server');
        console.log('');

        resolve(sessionData);
      } catch (error) {
        console.error('');
        console.error('❌ 导入失败:', error.message);
        console.error('');
        console.error('请确保：');
        console.error('1. 粘贴的是有效的 JSON 格式');
        console.error('2. 已经在浏览器中运行了提供的代码');
        console.error('3. 复制了完整的输出');
        reject(error);
      }
    });
  });
}

// Run if called directly
if (process.argv[1] === new URL(import.meta.url).pathname) {
  const accountName = process.argv[2];
  
  if (!accountName) {
    console.error('❌ 请提供账号名称');
    console.error('用法: node import-cookies.js <账号名称>');
    process.exit(1);
  }

  importCookies(accountName)
    .then(() => process.exit(0))
    .catch(() => process.exit(1));
}

export { importCookies };

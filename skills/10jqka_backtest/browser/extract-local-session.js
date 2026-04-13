import { execSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { DATA_DIR, SKILL_ROOT } from '../paths.js';
import { saveSession } from './session-manager.js';

async function main() {
  console.log('🔬 启动“第三种方式”：从本地浏览器提取有效 Session...');
  
  const tempFile = path.join(DATA_DIR, 'session_temp.json');
  const pythonScript = path.join(SKILL_ROOT, 'browser/extract_cookies.py');

  try {
    console.log('🐍 正在调用 Python 提取脚本 (需开启 Chrome 且已登录)...');
    
    // 执行 Python 脚本
    execSync(`python3 "${pythonScript}" > "${tempFile}"`);
    
    if (!fs.existsSync(tempFile)) {
      throw new Error('Python 脚本未生成输出文件');
    }

    const rawCookies = JSON.parse(fs.readFileSync(tempFile, 'utf8'));
    
    if (!rawCookies || rawCookies.length === 0) {
      console.error('\n❌ 提取失败：未在 Chrome 中发现已登录的 10jqka Cookie。');
      console.log('请确保您在 Chrome 中打开并登入了: https://backtest.10jqka.com.cn/');
      process.exit(1);
    }

    // 转换为 Playwright 兼容格式 (处理 expires 等字段)
    const formattedCookies = rawCookies.map(c => ({
      name: c.name,
      value: c.value,
      domain: c.domain,
      path: c.path,
      expires: c.expires || -1,
      secure: Boolean(c.secure),
      httpOnly: Boolean(c.httpOnly),
      sameSite: 'Lax'
    }));

    console.log(`✅ 成功捕获 ${formattedCookies.length} 个 Cookie！`);
    
    saveSession(formattedCookies, 'https://backtest.10jqka.com.cn/');
    
    console.log('\n✨ 端到端提取完成！现在您可以直接运行命令了。');
    
    // 清理临时文件
    try { fs.unlinkSync(tempFile); } catch (e) {}
    
  } catch (error) {
    console.error(`\n❌ 提取流程出错: ${error.message}`);
    console.log('提示：如果是权限问题，请确保终端有权访问 Chrome 的配置目录。');
    process.exit(1);
  }
}

main().catch(console.error);

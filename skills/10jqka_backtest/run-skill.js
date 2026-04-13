import fs from 'node:fs';
import path from 'node:path';
import { StrategyRunner } from './request/strategy-runner.js';
import { loadSession, isSessionValid } from './browser/session-manager.js';
import { login } from './browser/automated-login.js';
import './load-env.js';

async function main() {
  const args = process.argv.slice(2);
  let configFile = args[0];

  if (!configFile) {
    configFile = 'examples/formula_strategy.json';
    console.log(`未指定策略文件，使用默认示例: ${configFile}`);
  }

  const cwd = process.cwd();
  const resolvedPath = path.resolve(cwd, configFile);

  if (!fs.existsSync(resolvedPath)) {
    console.error(`❌ 找不到文件: ${resolvedPath}`);
    process.exit(1);
  }

  console.log(`📂 加载配置: ${configFile}`);
  const config = JSON.parse(fs.readFileSync(resolvedPath, 'utf8'));

  const runner = new StrategyRunner({ verbose: true });

  try {
    // 第一次尝试运行
    await runner.run(config);
    console.log('\n✅ 运行脚本完成。');
  } catch (err) {
    const isAuthError = err.message.includes('未授权') || err.message.includes('noauth') || err.message.includes('401');
    
    if (isAuthError) {
      console.log('\n⚠️ 检测到登录失效，正在尝试自动化登录...');
      try {
        await login();
        // 登录成功后重试一次
        console.log('🔄 登录成功，正在重试提交策略...');
        await runner.run(config);
        console.log('\n✅ 运行脚本完成（重试成功）。');
      } catch (retryErr) {
        console.error(`\n❌ 自动登录或重试失败: ${retryErr.message}`);
        process.exit(1);
      }
    } else {
      // 非授权类错误，直接退出
      console.error(`\n❌ 运行出错: ${err.message}`);
      process.exit(1);
    }
  }
}

main();

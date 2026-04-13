import { AuthManager } from './auth-manager.js';
import site10jqka from './sites/10jqka.js';
import siteGuorn from './sites/guorn.js';
import siteThsQuant from './sites/thsquant.js';
import siteJoinQuant from './sites/joinquant.js';
import siteRiceQuant from './sites/ricequant.js';
import siteBigQuant from './sites/bigquant.js';
import siteLixinger from './sites/lixinger.js';
import siteChatGPT from './sites/chatgpt.js';
import siteGemini from './sites/gemini.js';
import readline from 'node:readline';

const sites = {
  '10jqka': site10jqka,
  'guorn': siteGuorn,
  'thsquant': siteThsQuant,
  'joinquant': siteJoinQuant,
  'ricequant': siteRiceQuant,
  'bigquant': siteBigQuant,
  'lixinger': siteLixinger,
  'chatgpt': siteChatGPT,
  'gemini': siteGemini
};

async function main() {
  const args = process.argv.slice(2);
  const siteId = args[0];
  const isTest = args.includes('--test');
  
  if (!siteId || (siteId !== 'all' && !sites[siteId])) {
    console.error('使用方法: node login.js <site_id|all> [--method=auto|manual|local|import] [--test]');
    console.log('可用站点:', Object.keys(sites).join(', '), ', all');
    process.exit(1);
  }

  const methodArg = args.find(arg => arg.startsWith('--method='));
  const method = methodArg ? methodArg.split('=')[1] : 'all';

  // 视觉验证模式
  if (isTest) {
    if (siteId === 'all') {
      for (const id of Object.keys(sites)) {
        await new AuthManager(sites[id]).testSessionHeaded();
      }
    } else {
      await new AuthManager(sites[siteId]).testSessionHeaded();
    }
    process.exit(0);
  }

  // 手动导入模式
  if (method === 'import') {
    if (siteId === 'all') {
      console.error('❌ "all" 暂不支持手动导入模式。');
      process.exit(1);
    }
    await handleImport(siteId);
    process.exit(0);
  }

  const sitesToLogin = siteId === 'all' ? Object.keys(sites) : [siteId];

  for (const id of sitesToLogin) {
    console.log(`\n🚀 启动 [${id}] 登录流程 (方式: ${method})...`);
    const manager = new AuthManager(sites[id]);
    try {
      const cookies = await manager.getValidSession({ forceRefresh: true, method });
      console.log(`✨ [${id}] 完成！`);
    } catch (err) {
      console.error(`❌ [${id}] 失败: ${err.message}`);
    }
  }

  process.exit(0);
}

async function handleImport(siteId) {
  const manager = new AuthManager(sites[siteId]);
  console.log(`\n🍪 正在为 [${siteId}] 手动导入 Cookies...`);
  console.log('请从浏览器插件导出 JSON 并粘贴到此处（粘贴完成后按 Ctrl+D 结束）：');
  console.log('--------------------------------------------------');

  const rl = readline.createInterface({ input: process.stdin });
  let buffer = '';
  
  return new Promise((resolve) => {
    rl.on('line', line => buffer += line);
    rl.on('close', async () => {
      try {
        await manager.importCookies(buffer);
        resolve();
      } catch (e) {
        resolve();
      }
    });
  });
}

main();

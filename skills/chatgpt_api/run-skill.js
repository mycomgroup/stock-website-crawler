#!/usr/bin/env node

import { readFileSync } from 'fs';
import { captureSession } from './browser/capture-session.js';
import { captureSessionStealth } from './browser/capture-session-stealth.js';
import { importCookies } from './import-cookies.js';
import { SessionManager } from './browser/session-manager.js';
import { sendMessage, sendBatchMessages } from './request/message-sender.js';
import { sendMessageWithBrowser, sendBatchMessagesWithBrowser } from './request/browser-message-sender.js';
import { ENV } from './load-env.js';

/**
 * 解析命令行参数
 */
function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = argv[i + 1];
      if (value && !value.startsWith('--')) {
        args[key] = value;
        i++;
      } else {
        args[key] = true;
      }
    }
  }
  return args;
}

/**
 * 显示帮助信息
 */
function showHelp() {
  console.log(`
ChatGPT API Skill - 程序化提交问题到 ChatGPT

用法:
  node run-skill.js [选项]

选项:
  --login              打开浏览器进行 Google 登录
  --force              强制重新登录（即使 session 有效）
  --headed             使用有头模式（显示浏览器窗口）
  --use-profile <path> 使用现有的 Chrome profile

  --message <text>     发送单条消息
  --file <path>        从文件读取消息内容
  --batch <path>       批量发送消息（每行一条）
  
  --use-browser        使用浏览器模式（推荐，不会被 Cloudflare 阻止）
  --keep-open          保持浏览器打开（用于交互）
  
  --model <name>       指定模型 (gpt-4, gpt-3.5-turbo 等)
  --conversation <id>  继续已有对话
  
  --validate           验证 session 是否有效
  --list               列出最近的对话
  --list-all           列出所有对话（分页）
  --search <query>     搜索对话
  --show <id>          显示特定对话的详细内容
  --delete <id>        删除特定对话
  --rename <id> <title> 重命名对话
  --clear              清空所有对话
  --models             列出可用模型
  --account            显示账户信息
  
  # 多账号管理
  --add-account [name]    添加新账号
  --list-accounts         列出所有账号
  --remove-account <id>   删除账号
  --enable-account <id>   启用账号
  --disable-account <id>  禁用账号
  --set-weight <id> <weight>  设置账号权重
  --set-strategy <strategy>   设置负载均衡策略
  --validate-accounts     验证所有账号
  --account-stats         显示账号统计
  
  --import-cookies <name> 手动导入 cookies（推荐）
  
  --help               显示此帮助信息

示例:
  # 首次登录
  node run-skill.js --login

  # 发送单条消息
  node run-skill.js --message "解释一下 JavaScript 的闭包"

  # 从文件读取消息
  node run-skill.js --file prompt.txt

  # 指定模型
  node run-skill.js --message "写一个快速排序算法" --model gpt-4

  # 批量发送
  node run-skill.js --batch questions.txt

  # 验证 session
  node run-skill.js --validate

  # 列出对话
  node run-skill.js --list
  node run-skill.js --list-all

  # 搜索对话
  node run-skill.js --search "JavaScript"

  # 查看对话详情
  node run-skill.js --show conv-abc123

  # 删除对话
  node run-skill.js --delete conv-abc123

  # 重命名对话
  node run-skill.js --rename conv-abc123 "新标题"

  # 列出可用模型
  node run-skill.js --models

  # 查看账户信息
  node run-skill.js --account

  # 使用现有 Chrome profile
  node run-skill.js --login --use-profile "/Users/username/Library/Application Support/Google/Chrome/Profile 5"
`);
}

/**
 * 主函数
 */
async function main() {
  const args = parseArgs(process.argv.slice(2));

  // Show help
  if (args.help || Object.keys(args).length === 0) {
    showHelp();
    return;
  }

  try {
    // Login
    if (args.login || args.force) {
      console.log('🔐 开始登录流程...');
      console.log('');
      
      // Use stealth mode by default
      await captureSessionStealth({
        headless: !args.headed,
        useProfile: args['use-profile'] || ENV.CHROME_PROFILE_PATH
      });
      
      console.log('');
      console.log('✅ 登录完成！现在可以发送消息了');
      return;
    }

    // Validate session
    if (args.validate) {
      const sessionManager = new SessionManager();
      const isValid = await sessionManager.validateSession();
      
      if (isValid) {
        console.log('✅ Session 有效');
        
        // Show auth cookies
        const authCookies = sessionManager.getAuthCookies();
        console.log('');
        console.log('关键 Cookies:');
        console.log(`  - Session Token: ${authCookies.sessionToken ? '✓' : '✗'}`);
        console.log(`  - Callback URL: ${authCookies.callbackUrl ? '✓' : '✗'}`);
        console.log(`  - CF UVID: ${authCookies.cfuvid ? '✓' : '✗'}`);
        console.log(`  - CF Clearance: ${authCookies.cfClearance ? '✓' : '✗'}`);
      } else {
        console.log('❌ Session 已失效');
        console.log('💡 请运行: node run-skill.js --login');
        process.exit(1);
      }
      return;
    }

    // List conversations
    if (args.list || args['list-all']) {
      const { ChatGPTClient } = await import('./request/chatgpt-client.js');
      const client = new ChatGPTClient();
      
      const limit = args['list-all'] ? 100 : 10;
      console.log(`📋 获取对话列表 (最多 ${limit} 个)...`);
      
      const result = await client.getConversations({ limit });
      
      console.log('');
      console.log(`找到 ${result.items.length} 个对话 (总共 ${result.total} 个):`);
      console.log('');
      
      result.items.forEach((conv, i) => {
        const date = new Date(conv.create_time * 1000).toLocaleString('zh-CN');
        const updateDate = new Date(conv.update_time * 1000).toLocaleString('zh-CN');
        console.log(`${i + 1}. ${conv.title || 'Untitled'}`);
        console.log(`   ID: ${conv.id}`);
        console.log(`   创建: ${date}`);
        console.log(`   更新: ${updateDate}`);
        console.log('');
      });
      
      if (result.hasMore) {
        console.log('💡 还有更多对话，使用 --list-all 查看更多');
      }
      
      return;
    }

    // Search conversations
    if (args.search) {
      const { ChatGPTClient } = await import('./request/chatgpt-client.js');
      const client = new ChatGPTClient();
      
      console.log(`🔍 搜索对话: "${args.search}"...`);
      const results = await client.searchConversations(args.search);
      
      console.log('');
      console.log(`找到 ${results.length} 个匹配的对话:`);
      console.log('');
      
      results.forEach((conv, i) => {
        const date = new Date(conv.create_time * 1000).toLocaleString('zh-CN');
        console.log(`${i + 1}. ${conv.title || 'Untitled'}`);
        console.log(`   ID: ${conv.id}`);
        console.log(`   创建: ${date}`);
        console.log('');
      });
      
      return;
    }

    // Show conversation
    if (args.show) {
      const { ChatGPTClient } = await import('./request/chatgpt-client.js');
      const client = new ChatGPTClient();
      
      console.log(`📖 获取对话详情: ${args.show}...`);
      const conv = await client.getConversation(args.show);
      
      console.log('');
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log(`标题: ${conv.title || 'Untitled'}`);
      console.log(`ID: ${conv.id}`);
      console.log(`创建时间: ${new Date(conv.create_time * 1000).toLocaleString('zh-CN')}`);
      console.log(`更新时间: ${new Date(conv.update_time * 1000).toLocaleString('zh-CN')}`);
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log('');
      
      // Show messages
      if (conv.mapping) {
        const messages = Object.values(conv.mapping)
          .filter(m => m.message && m.message.content && m.message.content.parts)
          .sort((a, b) => (a.message.create_time || 0) - (b.message.create_time || 0));
        
        console.log(`消息数量: ${messages.length}`);
        console.log('');
        
        messages.forEach((m, i) => {
          const role = m.message.author.role;
          const content = m.message.content.parts.join('');
          const icon = role === 'user' ? '👤' : '🤖';
          
          console.log(`${icon} ${role.toUpperCase()}:`);
          console.log(content);
          console.log('');
        });
      }
      
      return;
    }

    // Delete conversation
    if (args.delete) {
      const { ChatGPTClient } = await import('./request/chatgpt-client.js');
      const client = new ChatGPTClient();
      
      console.log(`🗑️  删除对话: ${args.delete}...`);
      await client.deleteConversation(args.delete);
      
      console.log('✅ 对话已删除');
      return;
    }

    // Rename conversation
    if (args.rename) {
      const conversationId = args.rename;
      const title = process.argv[process.argv.indexOf('--rename') + 2];
      
      if (!title) {
        console.error('❌ 请提供新标题');
        console.log('💡 用法: node run-skill.js --rename <id> <新标题>');
        process.exit(1);
      }
      
      const { ChatGPTClient } = await import('./request/chatgpt-client.js');
      const client = new ChatGPTClient();
      
      console.log(`✏️  重命名对话: ${conversationId} -> "${title}"...`);
      await client.renameConversation(conversationId, title);
      
      console.log('✅ 对话已重命名');
      return;
    }

    // Clear all conversations
    if (args.clear) {
      const { ChatGPTClient } = await import('./request/chatgpt-client.js');
      const client = new ChatGPTClient();
      
      console.log('⚠️  确认要清空所有对话吗？(y/N)');
      // For now, just proceed (in production, add confirmation)
      console.log('🗑️  清空所有对话...');
      await client.clearConversations();
      
      console.log('✅ 所有对话已清空');
      return;
    }

    // List models
    if (args.models) {
      const { ChatGPTClient } = await import('./request/chatgpt-client.js');
      const client = new ChatGPTClient();
      
      console.log('🤖 获取可用模型列表...');
      const models = await client.getModels();
      
      console.log('');
      console.log(`可用模型 (${models.length} 个):`);
      console.log('');
      
      models.forEach((model, i) => {
        console.log(`${i + 1}. ${model.slug}`);
        if (model.title) console.log(`   名称: ${model.title}`);
        if (model.description) console.log(`   描述: ${model.description}`);
        if (model.max_tokens) console.log(`   最大 tokens: ${model.max_tokens}`);
        console.log('');
      });
      
      return;
    }

    // Account info
    if (args.account) {
      const { ChatGPTClient } = await import('./request/chatgpt-client.js');
      const client = new ChatGPTClient();
      
      console.log('👤 获取账户信息...');
      
      try {
        const account = await client.getAccountInfo();
        
        console.log('');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('账户信息');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        if (account.email) console.log(`邮箱: ${account.email}`);
        if (account.name) console.log(`名称: ${account.name}`);
        if (account.picture) console.log(`头像: ${account.picture}`);
        if (account.plan_type) console.log(`计划类型: ${account.plan_type}`);
        console.log('');
      } catch (error) {
        console.log('');
        console.log('⚠️  无法获取账户信息，但这不影响发送消息');
        console.log('💡 可以尝试直接发送消息测试');
        console.log('');
      }
      
      return;
    }

    // ============================================
    // 多账号管理
    // ============================================

    // Import cookies manually
    if (args['import-cookies']) {
      const accountName = args['import-cookies'];
      await importCookies(accountName);
      return;
    }

    // Add account
    if (args['add-account'] !== undefined) {
      const { MultiAccountManager } = await import('./browser/multi-account-manager.js');
      const manager = new MultiAccountManager();
      
      const name = typeof args['add-account'] === 'string' ? args['add-account'] : undefined;
      
      await manager.addAccount({
        name,
        headless: !args.headed,
        useStealth: true  // Use stealth mode for multi-account
      });
      
      return;
    }

    // List accounts
    if (args['list-accounts']) {
      const { MultiAccountManager } = await import('./browser/multi-account-manager.js');
      const manager = new MultiAccountManager();
      
      manager.listAccounts();
      return;
    }

    // Remove account
    if (args['remove-account']) {
      const { MultiAccountManager } = await import('./browser/multi-account-manager.js');
      const manager = new MultiAccountManager();
      
      manager.removeAccount(args['remove-account']);
      return;
    }

    // Enable account
    if (args['enable-account']) {
      const { MultiAccountManager } = await import('./browser/multi-account-manager.js');
      const manager = new MultiAccountManager();
      
      manager.setAccountEnabled(args['enable-account'], true);
      return;
    }

    // Disable account
    if (args['disable-account']) {
      const { MultiAccountManager } = await import('./browser/multi-account-manager.js');
      const manager = new MultiAccountManager();
      
      manager.setAccountEnabled(args['disable-account'], false);
      return;
    }

    // Set weight
    if (args['set-weight']) {
      const accountId = args['set-weight'];
      const weight = parseInt(process.argv[process.argv.indexOf('--set-weight') + 2]);
      
      if (!weight || weight < 1) {
        console.error('❌ 权重必须是大于 0 的整数');
        process.exit(1);
      }
      
      const { MultiAccountManager } = await import('./browser/multi-account-manager.js');
      const manager = new MultiAccountManager();
      
      manager.setAccountWeight(accountId, weight);
      return;
    }

    // Set strategy
    if (args['set-strategy']) {
      const { MultiAccountManager } = await import('./browser/multi-account-manager.js');
      const manager = new MultiAccountManager();
      
      manager.setStrategy(args['set-strategy']);
      return;
    }

    // Validate accounts
    if (args['validate-accounts']) {
      const { MultiAccountManager } = await import('./browser/multi-account-manager.js');
      const manager = new MultiAccountManager();
      
      await manager.validateAllAccounts();
      return;
    }

    // Account stats
    if (args['account-stats']) {
      const { MultiAccountManager } = await import('./browser/multi-account-manager.js');
      const manager = new MultiAccountManager();
      
      const stats = manager.getStats();
      
      console.log('');
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log('账号统计');
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log(`总账号数: ${stats.total}`);
      console.log(`启用账号: ${stats.enabled}`);
      console.log(`有效账号: ${stats.active}`);
      console.log(`失效账号: ${stats.expired}`);
      console.log(`总请求数: ${stats.totalRequests}`);
      console.log(`负载均衡策略: ${stats.strategy}`);
      console.log('');
      
      console.log('账号详情:');
      stats.accounts.forEach((acc, i) => {
        const status = acc.enabled ? 
          (acc.status === 'active' ? '✅' : '❌') : '⏸️';
        console.log(`  ${i + 1}. ${status} ${acc.name}`);
        console.log(`     请求数: ${acc.requestCount}`);
        console.log(`     权重: ${acc.weight}`);
        console.log(`     最后使用: ${acc.lastUsed}`);
      });
      console.log('');
      
      return;
    }

    // Send message
    const options = {
      model: args.model || ENV.DEFAULT_MODEL,
      conversationId: args.conversation || null
    };

    const useBrowser = args['use-browser'];
    const keepOpen = args['keep-open'];

    if (args.message) {
      // Single message
      if (useBrowser) {
        await sendMessageWithBrowser(args.message, { keepOpen });
      } else {
        await sendMessage(args.message, options);
      }
      
    } else if (args.file) {
      // Message from file
      const content = readFileSync(args.file, 'utf-8').trim();
      if (useBrowser) {
        await sendMessageWithBrowser(content, { keepOpen });
      } else {
        await sendMessage(content, options);
      }
      
    } else if (args.batch) {
      // Batch messages
      const content = readFileSync(args.batch, 'utf-8');
      const messages = content.split('\n')
        .map(line => line.trim())
        .filter(line => line && !line.startsWith('#'));
      
      if (useBrowser) {
        await sendBatchMessagesWithBrowser(messages, { keepOpen });
      } else {
        await sendBatchMessages(messages, options);
      }
      
    } else {
      console.error('❌ 请指定 --message, --file 或 --batch');
      console.log('💡 运行 --help 查看使用说明');
      process.exit(1);
    }

  } catch (error) {
    console.error('');
    console.error('❌ 执行失败:', error.message);
    console.error('');
    
    if (error.message.includes('Authentication failed')) {
      console.log('💡 请运行: node run-skill.js --login');
    }
    
    process.exit(1);
  }
}

// Run
main();

import { ChatGPTBrowserClient } from '../browser/chatgpt-browser-client.js';
import { PATHS } from '../paths.js';

/**
 * 使用浏览器发送消息
 */
export async function sendMessageWithBrowser(message, options = {}) {
  const {
    sessionPath = PATHS.sessionFile,
    headless = false,
    keepOpen = false
  } = options;

  const client = new ChatGPTBrowserClient({
    headless,
    sessionPath
  });

  try {
    // Launch browser
    await client.launch();

    // Send message
    const response = await client.sendMessage(message);

    console.log('');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('💬 ChatGPT 回复:');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('');
    console.log(response.content);
    console.log('');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('');

    if (keepOpen) {
      await client.keepAlive();
    } else {
      await client.close();
    }

    return response;

  } catch (error) {
    console.error('');
    console.error('❌ 发送失败:', error.message);
    console.error('');
    
    await client.close();
    throw error;
  }
}

/**
 * 批量发送消息
 */
export async function sendBatchMessagesWithBrowser(messages, options = {}) {
  const {
    sessionPath = PATHS.sessionFile,
    headless = false,
    newChatPerMessage = false
  } = options;

  const client = new ChatGPTBrowserClient({
    headless,
    sessionPath
  });

  const results = [];

  try {
    // Launch browser once
    await client.launch();

    for (let i = 0; i < messages.length; i++) {
      const message = messages[i];
      
      console.log('');
      console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
      console.log(`📝 消息 ${i + 1}/${messages.length}`);
      console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
      console.log('');

      if (newChatPerMessage && i > 0) {
        await client.newChat();
      }

      const response = await client.sendMessage(message);
      
      console.log('');
      console.log('💬 回复:');
      console.log('');
      console.log(response.content);
      console.log('');

      results.push({
        message,
        response: response.content,
        timestamp: response.timestamp
      });

      // Wait between messages
      if (i < messages.length - 1) {
        console.log('⏳ 等待 2 秒...');
        await new Promise(resolve => setTimeout(resolve, 2000));
      }
    }

    await client.close();

    console.log('');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log(`✅ 完成！共发送 ${messages.length} 条消息`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('');

    return results;

  } catch (error) {
    console.error('');
    console.error('❌ 批量发送失败:', error.message);
    console.error('');
    
    await client.close();
    throw error;
  }
}

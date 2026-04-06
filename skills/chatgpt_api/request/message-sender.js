import { ChatGPTClient } from './chatgpt-client.js';
import { writeFileSync, existsSync, mkdirSync, appendFileSync } from 'fs';
import { PATHS } from '../paths.js';

/**
 * 消息发送器
 * 封装消息发送的完整流程
 */
export class MessageSender {
  constructor(options = {}) {
    this.client = new ChatGPTClient(options);
    this.saveHistory = options.saveHistory !== false;
  }

  /**
   * 发送单条消息
   */
  async send(message, options = {}) {
    const startTime = Date.now();

    try {
      const response = await this.client.sendMessage({
        message,
        ...options
      });

      const duration = Date.now() - startTime;

      console.log('');
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log('📨 ChatGPT 响应:');
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log(response.content);
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log(`⏱️  耗时: ${(duration / 1000).toFixed(2)}s`);
      console.log(`🤖 模型: ${response.model || options.model || 'unknown'}`);
      console.log(`🆔 对话 ID: ${response.conversationId || 'new'}`);
      console.log('');

      // Save to history
      if (this.saveHistory) {
        this.saveToHistory({
          timestamp: new Date().toISOString(),
          message,
          response: response.content,
          model: response.model,
          conversationId: response.conversationId,
          messageId: response.messageId,
          duration
        });
      }

      return response;

    } catch (error) {
      console.error('');
      console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.error('❌ 发送失败');
      console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.error(error.message);
      console.error('');
      throw error;
    }
  }

  /**
   * 批量发送消息
   */
  async sendBatch(messages, options = {}) {
    const results = [];
    const { delay = 2000 } = options;

    console.log(`📦 批量发送 ${messages.length} 条消息...`);
    console.log('');

    for (let i = 0; i < messages.length; i++) {
      const message = messages[i];
      console.log(`[${i + 1}/${messages.length}] 发送消息...`);

      try {
        const response = await this.send(message, options);
        results.push({ success: true, message, response });

        // Delay between requests
        if (i < messages.length - 1 && delay > 0) {
          console.log(`⏳ 等待 ${delay / 1000}s...`);
          await new Promise(resolve => setTimeout(resolve, delay));
        }

      } catch (error) {
        results.push({ success: false, message, error: error.message });
      }
    }

    // Summary
    const successCount = results.filter(r => r.success).length;
    console.log('');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('📊 批量发送完成');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log(`✅ 成功: ${successCount}/${messages.length}`);
    console.log(`❌ 失败: ${messages.length - successCount}/${messages.length}`);
    console.log('');

    return results;
  }

  /**
   * 保存到历史记录
   */
  saveToHistory(record) {
    try {
      // Ensure data directory exists
      if (!existsSync(PATHS.data)) {
        mkdirSync(PATHS.data, { recursive: true });
      }

      const filename = `history-${new Date().toISOString().split('T')[0]}.jsonl`;
      const filepath = `${PATHS.data}/${filename}`;

      const line = JSON.stringify(record) + '\n';
      
      // Append to file
      appendFileSync(filepath, line, 'utf-8');

    } catch (error) {
      console.warn('⚠️  保存历史记录失败:', error.message);
    }
  }
}

/**
 * 快捷函数：发送单条消息
 */
export async function sendMessage(message, options = {}) {
  const sender = new MessageSender(options);
  return await sender.send(message, options);
}

/**
 * 快捷函数：批量发送消息
 */
export async function sendBatchMessages(messages, options = {}) {
  const sender = new MessageSender(options);
  return await sender.sendBatch(messages, options);
}

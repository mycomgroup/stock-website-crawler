import { JqkaBacktestClient } from './10jqka-client.js';
import { normalizeConfig } from './config-normalizer.js';
import fs from 'node:fs';

export class StrategyRunner {
  constructor(options = {}) {
    this.client = new JqkaBacktestClient(options);
    this.verbose = options.verbose !== false;
  }

  log(...args) {
    if (this.verbose) console.log(...args);
  }

  async run(rawConfig) {
    try {
      this.log('🧮 格式化策略参数...');
      const config = normalizeConfig(rawConfig);
      this.log('📝 提交给问财引擎的参数:', JSON.stringify(config, null, 2));

      this.log('\n🚀 正在提交10jqka问财回测...');
      const runResult = await this.client.runBacktest(config);
      
      this.log('✅ 回测发起成功!');
      
      // 注意：问财接口实际行为可能不是返回taskId，而是同步或短轮询。
      // 当前根据 payload 初步构建，后续待补充真实的 taskId 并在这一层做轮询
      
      // 占位代码
      this.log('返回结果示例:', JSON.stringify(runResult.data).slice(0, 300) + '...');
      
      return {
        success: true,
        payload: config,
        response: runResult.data
      };
      
    } catch (error) {
      this.log(`\n❌ 回测执行失败: ${error.message}`);
      throw error;
    }
  }
}

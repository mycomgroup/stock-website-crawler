#!/usr/bin/env node

/**
 * 测试 OpenAI 兼容服务器
 * 使用标准的 OpenAI SDK
 */

const PORT = process.env.PORT || 3000;
const API_KEY = process.env.API_KEY || 'sk-chatgpt-proxy';
const BASE_URL = `http://localhost:${PORT}/v1`;

console.log('🧪 测试 OpenAI 兼容服务器\n');

/**
 * 测试 1: 使用 fetch 测试
 */
async function testWithFetch() {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('测试 1: 使用 fetch API');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  try {
    // 测试健康检查
    console.log('1. 健康检查...');
    const healthRes = await fetch(`http://localhost:${PORT}/health`);
    const health = await healthRes.json();
    console.log(`   ✅ 状态: ${health.status}\n`);

    // 测试模型列表
    console.log('2. 获取模型列表...');
    const modelsRes = await fetch(`${BASE_URL}/models`, {
      headers: {
        'Authorization': `Bearer ${API_KEY}`
      }
    });
    const models = await modelsRes.json();
    console.log(`   ✅ 找到 ${models.data.length} 个模型:`);
    models.data.forEach(model => {
      console.log(`      - ${model.id}`);
    });
    console.log('');

    // 测试聊天完成（非流式）
    console.log('3. 测试聊天完成（非流式）...');
    const chatRes = await fetch(`${BASE_URL}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`
      },
      body: JSON.stringify({
        model: 'gpt-4',
        messages: [
          { role: 'user', content: '用一句话介绍你自己' }
        ]
      })
    });

    const chat = await chatRes.json();
    console.log(`   ✅ 响应:`);
    console.log(`      模型: ${chat.model}`);
    console.log(`      内容: ${chat.choices[0].message.content}`);
    console.log('');

    // 测试流式响应
    console.log('4. 测试聊天完成（流式）...');
    const streamRes = await fetch(`${BASE_URL}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`
      },
      body: JSON.stringify({
        model: 'gpt-4',
        messages: [
          { role: 'user', content: '数到5' }
        ],
        stream: true
      })
    });

    console.log('   ✅ 流式响应:');
    console.log('      ', end='');
    
    const reader = streamRes.body.getReader();
    const decoder = new TextDecoder();
    
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      const chunk = decoder.decode(value);
      const lines = chunk.split('\n').filter(line => line.trim());
      
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.substring(6);
          if (data === '[DONE]') continue;
          
          try {
            const json = JSON.parse(data);
            const content = json.choices[0]?.delta?.content;
            if (content) {
              process.stdout.write(content);
            }
          } catch (e) {
            // Skip invalid JSON
          }
        }
      }
    }
    console.log('\n');

    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('✅ 所有测试通过！');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  } catch (error) {
    console.error('❌ 测试失败:', error.message);
    console.log('\n💡 请确保服务器正在运行:');
    console.log('   node server/openai-compatible-server.js\n');
  }
}

/**
 * 测试 2: 使用 OpenAI SDK（如果已安装）
 */
async function testWithOpenAISDK() {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('测试 2: 使用 OpenAI SDK');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  try {
    const { default: OpenAI } = await import('openai');
    
    const openai = new OpenAI({
      apiKey: API_KEY,
      baseURL: BASE_URL
    });

    console.log('1. 测试聊天完成...');
    const completion = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        { role: 'user', content: '你好，请用一句话介绍你自己' }
      ]
    });

    console.log(`   ✅ 响应: ${completion.choices[0].message.content}\n`);

    console.log('2. 测试流式响应...');
    const stream = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        { role: 'user', content: '数到3' }
      ],
      stream: true
    });

    console.log('   ✅ 流式响应: ', end='');
    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content || '';
      process.stdout.write(content);
    }
    console.log('\n');

    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('✅ OpenAI SDK 测试通过！');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  } catch (error) {
    if (error.code === 'ERR_MODULE_NOT_FOUND') {
      console.log('⚠️  OpenAI SDK 未安装');
      console.log('💡 安装: npm install openai\n');
    } else {
      console.error('❌ 测试失败:', error.message);
    }
  }
}

// 运行测试
async function runTests() {
  await testWithFetch();
  await testWithOpenAISDK();
}

runTests();

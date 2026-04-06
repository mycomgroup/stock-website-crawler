/**
 * 使用 OpenAI SDK 连接到本地服务器的示例
 * 
 * 前提条件:
 * 1. npm install openai
 * 2. 启动服务器: npm run server
 */

// 如果没有安装 openai，会提示安装
let OpenAI;
try {
  OpenAI = (await import('openai')).default;
} catch (error) {
  console.error('❌ OpenAI SDK 未安装');
  console.log('💡 请运行: npm install openai\n');
  process.exit(1);
}

const openai = new OpenAI({
  apiKey: 'sk-chatgpt-proxy',
  baseURL: 'http://localhost:3000/v1'
});

console.log('🤖 使用 OpenAI SDK 连接到 ChatGPT 代理服务器\n');

// 示例 1: 简单对话
async function example1() {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('示例 1: 简单对话');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  const completion = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      { role: 'user', content: '用一句话介绍你自己' }
    ]
  });

  console.log('回答:', completion.choices[0].message.content);
  console.log('');
}

// 示例 2: 流式响应
async function example2() {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('示例 2: 流式响应');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  const stream = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      { role: 'user', content: '数到 5' }
    ],
    stream: true
  });

  process.stdout.write('回答: ');
  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content || '';
    process.stdout.write(content);
  }
  console.log('\n');
}

// 示例 3: 多轮对话
async function example3() {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('示例 3: 多轮对话');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  const messages = [
    { role: 'user', content: '我叫小明' }
  ];

  // 第一轮
  let completion = await openai.chat.completions.create({
    model: 'gpt-4',
    messages
  });

  console.log('用户: 我叫小明');
  console.log('助手:', completion.choices[0].message.content);
  console.log('');

  // 添加助手回复到历史
  messages.push(completion.choices[0].message);

  // 第二轮
  messages.push({ role: 'user', content: '我叫什么名字？' });
  
  completion = await openai.chat.completions.create({
    model: 'gpt-4',
    messages
  });

  console.log('用户: 我叫什么名字？');
  console.log('助手:', completion.choices[0].message.content);
  console.log('');
}

// 示例 4: 获取模型列表
async function example4() {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('示例 4: 获取模型列表');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  const models = await openai.models.list();

  console.log('可用模型:');
  for (const model of models.data) {
    console.log(`  - ${model.id}`);
  }
  console.log('');
}

// 运行所有示例
async function runExamples() {
  try {
    await example1();
    await example2();
    await example3();
    await example4();

    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('✅ 所有示例运行完成！');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  } catch (error) {
    console.error('\n❌ 错误:', error.message);
    
    if (error.code === 'ECONNREFUSED') {
      console.log('\n💡 请确保服务器正在运行:');
      console.log('   npm run server\n');
    }
  }
}

runExamples();

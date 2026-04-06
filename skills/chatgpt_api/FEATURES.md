# ChatGPT API 功能列表

## ✅ 已实现功能

### 1. 认证和 Session 管理

- ✅ 浏览器自动化登录（支持任意登录方式）
- ✅ Session cookies 自动捕获和保存
- ✅ Session 有效性验证
- ✅ Session 自动刷新
- ✅ Cookie 管理和提取
- ✅ 支持使用现有 Chrome profile

### 2. 消息发送

- ✅ 发送单条消息
- ✅ 从文件读取消息
- ✅ 批量发送消息
- ✅ 指定模型（gpt-4, gpt-3.5-turbo 等）
- ✅ 继续已有对话
- ✅ SSE 响应解析
- ✅ 历史记录保存

### 3. 对话管理

- ✅ 获取对话列表（支持分页）
- ✅ 获取对话详情（包含完整消息历史）
- ✅ 删除对话
- ✅ 清空所有对话
- ✅ 重命名对话
- ✅ 搜索对话

### 4. 模型和账户

- ✅ 获取可用模型列表
- ✅ 获取账户信息
- ✅ 切换模型

### 5. CLI 工具

- ✅ 完整的命令行界面
- ✅ 参数解析
- ✅ 帮助信息
- ✅ 错误处理
- ✅ 友好的输出格式

## 📋 API 端点

### 已实现

| 方法 | 端点 | 功能 | 状态 |
|------|------|------|------|
| POST | `/backend-api/conversation` | 发送消息 | ✅ |
| GET | `/backend-api/conversations` | 获取对话列表 | ✅ |
| GET | `/backend-api/conversation/:id` | 获取对话详情 | ✅ |
| PATCH | `/backend-api/conversation/:id` | 更新对话（删除/重命名） | ✅ |
| PATCH | `/backend-api/conversations` | 清空所有对话 | ✅ |
| GET | `/backend-api/conversations/search` | 搜索对话 | ✅ |
| GET | `/backend-api/models` | 获取模型列表 | ✅ |
| GET | `/backend-api/me` | 获取账户信息 | ✅ |

## 🎯 使用场景

### 场景 1: 自动化问答

```bash
# 批量提问
node run-skill.js --batch questions.txt
```

### 场景 2: 对话管理

```bash
# 查看所有对话
node run-skill.js --list-all

# 搜索特定主题
node run-skill.js --search "JavaScript"

# 查看对话详情
node run-skill.js --show conv-abc123

# 清理旧对话
node run-skill.js --delete conv-abc123
```

### 场景 3: 模型切换

```bash
# 使用 GPT-4
node run-skill.js --message "复杂问题" --model gpt-4

# 使用 GPT-3.5
node run-skill.js --message "简单问题" --model gpt-3.5-turbo
```

### 场景 4: 编程集成

```javascript
import { ChatGPTClient } from './request/chatgpt-client.js';

const client = new ChatGPTClient();

// 发送消息
const response = await client.sendMessage({
  message: "你好"
});

// 获取对话列表
const conversations = await client.getConversations();

// 搜索对话
const results = await client.searchConversations("JavaScript");
```

## 📊 功能对比

| 功能 | 网页版 | 本工具 | 优势 |
|------|--------|--------|------|
| 发送消息 | ✅ | ✅ | 自动化 |
| 查看历史 | ✅ | ✅ | 编程访问 |
| 搜索对话 | ✅ | ✅ | CLI 快速搜索 |
| 批量操作 | ❌ | ✅ | 批量发送/删除 |
| 导出数据 | ❌ | ✅ | JSON 格式 |
| 脚本集成 | ❌ | ✅ | 自动化工作流 |

## 🔧 技术特性

### 架构设计

- 模块化设计，职责清晰
- Session 管理与业务逻辑分离
- 支持多种使用方式（CLI / 编程）
- 完善的错误处理

### 安全性

- Session 数据本地存储
- 支持 .gitignore 保护敏感信息
- Cookie 加密传输（HTTPS）
- 自动检测 session 失效

### 可扩展性

- 易于添加新的 API 端点
- 支持自定义请求参数
- 插件化的消息处理
- 灵活的配置选项

## 📝 使用示例

### 基础使用

```bash
# 1. 首次登录
node run-skill.js --login

# 2. 发送消息
node run-skill.js --message "你好"

# 3. 查看对话
node run-skill.js --list
```

### 高级使用

```bash
# 批量提问
cat questions.txt | while read line; do
  node run-skill.js --message "$line"
  sleep 2
done

# 导出所有对话
node run-skill.js --list-all > conversations.txt

# 搜索并删除
CONV_ID=$(node run-skill.js --search "test" | grep "ID:" | head -1 | awk '{print $2}')
node run-skill.js --delete $CONV_ID
```

### 编程使用

```javascript
// 自动化工作流
import { MessageSender } from './request/message-sender.js';

const sender = new MessageSender();

// 批量处理
const questions = [
  "什么是 JavaScript?",
  "什么是 Python?",
  "什么是 Go?"
];

for (const question of questions) {
  const response = await sender.send(question);
  console.log(`Q: ${question}`);
  console.log(`A: ${response.content}\n`);
  
  // 等待 2 秒
  await new Promise(resolve => setTimeout(resolve, 2000));
}
```

## 🚀 性能优化

- Session 缓存，减少重复登录
- 批量请求支持延迟控制
- SSE 流式响应解析
- 最小化网络请求

## 🔒 安全建议

1. 不要分享 session.json 文件
2. 定期更换密码
3. 使用环境变量存储敏感信息
4. 监控账户活动
5. 及时清理历史记录

## 📈 未来计划

### 高优先级

- [ ] 流式响应实时显示
- [ ] 支持上传文件/图片
- [ ] 多轮对话上下文管理
- [ ] 代理支持

### 中优先级

- [ ] 自定义 system prompt
- [ ] 对话导出（Markdown/PDF）
- [ ] 统计和分析功能
- [ ] Web UI 界面

### 低优先级

- [ ] 插件系统
- [ ] 多账户管理
- [ ] 对话分享
- [ ] 语音输入/输出

## 📚 文档

- [README.md](./README.md) - 快速开始
- [API_REFERENCE.md](./API_REFERENCE.md) - API 参考
- [TECHNICAL_DETAILS.md](./TECHNICAL_DETAILS.md) - 技术细节
- [TEST_SUMMARY.md](./TEST_SUMMARY.md) - 测试总结
- [FEATURES.md](./FEATURES.md) - 本文档

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可

MIT License

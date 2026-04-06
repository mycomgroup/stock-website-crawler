# Gemini API 快速开始指南

## 5 分钟快速上手

### 第 1 步：安装依赖（1 分钟）

```bash
cd skills/gemini_api
npm install
```

### 第 2 步：首次登录（3 分钟）

```bash
node run-skill.js --login
```

浏览器会自动打开 Gemini 登录页面：
1. 使用你的 Google 账号登录
2. 完成所有验证步骤
3. 等待脚本自动捕获 session（会等待 5 分钟）
4. 看到 "✅ Session 数据已保存" 即成功

### 第 3 步：发送第一条消息（1 分钟）

```bash
node run-skill.js --message "你好，Gemini！请介绍一下你自己。"
```

成功！你已经可以程序化使用 Gemini 了。

## 常用场景

### 场景 1：批量提问

创建文件 `questions.txt`：
```
什么是量子计算？
什么是机器学习？
什么是区块链？
```

运行：
```bash
node run-skill.js --batch questions.txt
```

### 场景 2：从文件读取长提示词

创建文件 `prompt.txt`：
```
请帮我分析以下代码的性能问题：

[你的代码]

请给出优化建议。
```

运行：
```bash
node run-skill.js --file prompt.txt
```

### 场景 3：使用不同模型

```bash
# 使用 Gemini Pro（默认）
node run-skill.js --message "写一个快速排序算法"

# 使用 Gemini Pro Vision（支持图像）
node run-skill.js --message "分析这张图片" --model gemini-pro-vision
```

### 场景 4：管理对话历史

```bash
# 查看最近的对话
node run-skill.js --list

# 搜索对话
node run-skill.js --search "量子计算"

# 查看特定对话
node run-skill.js --show conv-abc123

# 删除对话
node run-skill.js --delete conv-abc123
```

### 场景 5：多账号负载均衡

```bash
# 添加多个账号
node run-skill.js --add-account "主账号"
node run-skill.js --add-account "备用账号"

# 查看账号状态
node run-skill.js --list-accounts

# 启动多账号服务器
USE_MULTI_ACCOUNT=true node server/openai-compatible-server.js
```

### 场景 6：作为 OpenAI API 使用

启动服务器：
```bash
node server/openai-compatible-server.js
```

在你的代码中使用：
```javascript
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: "sk-gemini-proxy",
  baseURL: "http://localhost:3000/v1"
});

const completion = await openai.chat.completions.create({
  model: "gemini-pro",
  messages: [{ role: "user", content: "你好" }]
});

console.log(completion.choices[0].message.content);
```

现在任何支持 OpenAI API 的工具都可以使用你的 Gemini session！

## 常见问题

### Q: Session 失效了怎么办？

```bash
node run-skill.js --login --force
```

### Q: 如何查看 session 是否有效？

```bash
node run-skill.js --validate
```

### Q: 批量发送时如何设置延迟？

编辑代码或使用环境变量（默认 2 秒）。

### Q: 可以同时使用 ChatGPT 和 Gemini 吗？

可以！分别启动两个服务器，使用不同端口：

```bash
# Terminal 1 - ChatGPT
cd skills/chatgpt_api
PORT=3000 node server/openai-compatible-server.js

# Terminal 2 - Gemini
cd skills/gemini_api
PORT=3001 node server/openai-compatible-server.js
```

### Q: 如何提高并发能力？

使用多账号：

```bash
# 添加多个账号
node run-skill.js --add-account "账号1"
node run-skill.js --add-account "账号2"
node run-skill.js --add-account "账号3"

# 启动多账号服务器
USE_MULTI_ACCOUNT=true node server/openai-compatible-server.js
```

## 下一步

- 📖 阅读 [完整文档](./README.md)
- 🔧 查看 [使用指南](./USAGE_GUIDE.md)
- 📚 了解 [API 参考](./API_REFERENCE.md)
- 🔄 学习 [多账号管理](./MULTI_ACCOUNT.md)
- 🌐 探索 [OpenAI 服务器](./OPENAI_SERVER.md)

## 获取帮助

```bash
node run-skill.js --help
```

---

**祝你使用愉快！** 🎉

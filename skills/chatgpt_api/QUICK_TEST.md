# 快速测试浏览器模式

## 现在就试试！

```bash
cd skills/chatgpt_api

# 测试发送消息
node run-skill.js --message "你好，请用中文回复" --use-browser
```

## 会发生什么？

1. 🚀 启动 Chrome 浏览器
2. 📂 加载你之前导入的 cookies
3. 🌐 打开 https://chatgpt.com/
4. ✅ 检查登录状态
   - 如果已登录：继续
   - 如果未登录：等待你手动登录，然后按回车
5. 💬 在输入框中输入消息
6. 📤 点击发送按钮
7. ⏳ 等待 ChatGPT 回复
8. ✅ 显示回复内容
9. 🔒 关闭浏览器

## 预期输出

```
🔌 使用代理: http://127.0.0.1:7897
🚀 启动浏览器...
📂 使用 session: /Users/yuping/.../data/session.json
🌐 打开 ChatGPT...
✅ 浏览器已就绪
💬 发送消息: 你好，请用中文回复
📤 消息已发送
⏳ 等待回复...
✅ 收到回复

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 ChatGPT 回复:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

你好！有什么我可以帮助你的吗？

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔒 关闭浏览器...
```

## 如果遇到问题

### 问题 1: 显示"未登录"

**原因**: Cookies 可能过期了

**解决方案**:
1. 在浏览器中手动登录 ChatGPT
2. 按回车继续

或者重新导入 cookies:
```bash
node import-cookies.js yuping3222
cp data/accounts/session-yuping3222.json data/session.json
```

### 问题 2: 浏览器无法打开

**解决方案**:
```bash
npx playwright install chromium
```

### 问题 3: 代理连接失败

**解决方案**:
检查 Clash 是否在运行，或临时禁用代理：
```bash
# 编辑 .env，注释掉代理配置
# HTTP_PROXY=http://127.0.0.1:7897
# HTTPS_PROXY=http://127.0.0.1:7897
```

## 更多示例

### 从文件读取

```bash
echo "解释一下 React Hooks" > question.txt
node run-skill.js --file question.txt --use-browser
```

### 批量发送

```bash
cat > questions.txt << 'EOF'
什么是 TypeScript？
什么是 Docker？
什么是 Kubernetes？
EOF

node run-skill.js --batch questions.txt --use-browser
```

### 保持浏览器打开

```bash
node run-skill.js --message "你好" --use-browser --keep-open
```

浏览器会保持打开，你可以手动继续对话。按 Ctrl+C 退出。

## 成功了吗？

如果成功了，恭喜！你现在可以：

1. 发送任意消息到 ChatGPT
2. 批量处理问题
3. 集成到你的工作流中

如果还有问题，查看 `BROWSER_MODE_GUIDE.md` 获取详细文档。

# 多 Profile 和浏览器复用指南

## 功能 1: 使用 Chrome Profile

### 你的 Chrome Profiles

```bash
# 查看所有 profiles
ls -la ~/Library/Application\ Support/Google/Chrome/ | grep Profile
```

你有以下 profiles：
- `Default` - 默认 profile
- `Profile 2` - 用户1
- `Profile 3` - 用户1
- `Profile 5` - 用户1
- `Profile 6` - 用户1
- `Profile 7` - sys3222
- `Profile 8` - 用户1

### 使用特定 Profile

```bash
# 使用 Default profile
node use-chrome-profile.js "/Users/yuping/Library/Application Support/Google/Chrome/Default"

# 使用 Profile 7 (sys3222)
node use-chrome-profile.js "/Users/yuping/Library/Application Support/Google/Chrome/Profile 7"

# 使用 Profile 并发送消息
node use-chrome-profile.js "/Users/yuping/Library/Application Support/Google/Chrome/Profile 7" "你好"
```

### 优点

- ✅ 使用已登录的账号，无需导入 cookies
- ✅ 保留浏览历史和设置
- ✅ 多个 profile = 多个账号
- ✅ 浏览器保持打开，可以手动操作

### 注意事项

⚠️ **不能同时使用同一个 Profile**

如果你的 Chrome 已经打开了某个 profile，脚本无法再次使用它。需要：
1. 关闭 Chrome 中的该 profile
2. 或使用不同的 profile

## 功能 2: 复用浏览器实例

### 交互模式（推荐）

启动一次浏览器，可以连续发送多条消息：

```bash
# 使用 session cookies（交互模式）
node reusable-browser-client.js --interactive

# 使用 Chrome profile（交互模式）
node reusable-browser-client.js --profile "/Users/yuping/Library/Application Support/Google/Chrome/Profile 7" --interactive
```

交互模式下：
- 输入消息并按回车发送
- 输入 `new` 开始新对话
- 输入 `exit` 或 `quit` 退出

### 批量发送模式

```bash
# 发送多条消息（复用浏览器）
node reusable-browser-client.js \
  --message "第一个问题" \
  --message "第二个问题" \
  --message "第三个问题"

# 使用 profile 批量发送
node reusable-browser-client.js \
  --profile "/Users/yuping/Library/Application Support/Google/Chrome/Profile 7" \
  --message "问题1" \
  --message "问题2"
```

### 性能对比

| 模式 | 启动时间 | 每条消息 | 总时间（3条消息） |
|------|---------|---------|-----------------|
| 每次启动新浏览器 | 10秒 | 15秒 | 10 + 15×3 = 55秒 |
| 复用浏览器 | 10秒 | 15秒 | 10 + 15×3 = 55秒 |
| 交互模式 | 10秒 | 10秒 | 10 + 10×3 = 40秒 |

复用浏览器的优势：
- ✅ 减少启动开销
- ✅ 保持对话上下文
- ✅ 更快的响应速度
- ✅ 更少的资源占用

## 使用场景

### 场景 1: 多个账号轮流使用

```bash
# 账号 1 (Profile 7)
node use-chrome-profile.js "/Users/yuping/Library/Application Support/Google/Chrome/Profile 7" "账号1的问题"

# 账号 2 (Profile 2)
node use-chrome-profile.js "/Users/yuping/Library/Application Support/Google/Chrome/Profile 2" "账号2的问题"
```

### 场景 2: 长时间交互

```bash
# 启动交互模式
node reusable-browser-client.js --interactive

# 然后可以连续对话
💬 你: 什么是 Docker？
✅ 收到回复: Docker 是...

💬 你: 如何安装？
✅ 收到回复: 安装步骤...

💬 你: new
🆕 开始新对话...

💬 你: 新的问题
```

### 场景 3: 批量处理问题

```bash
# 创建问题列表
cat > questions.txt << 'EOF'
什么是 Kubernetes？
什么是微服务？
什么是 DevOps？
EOF

# 使用脚本批量发送
while IFS= read -r question; do
  node reusable-browser-client.js --message "$question"
done < questions.txt
```

或者更高效：

```bash
# 一次启动，发送所有问题
node reusable-browser-client.js \
  --message "什么是 Kubernetes？" \
  --message "什么是微服务？" \
  --message "什么是 DevOps？"
```

### 场景 4: 不同 Profile 的不同任务

```bash
# Profile 7 用于工作相关
node reusable-browser-client.js \
  --profile "/Users/yuping/Library/Application Support/Google/Chrome/Profile 7" \
  --message "写一个 Python 脚本" \
  --interactive

# Profile 2 用于学习
node reusable-browser-client.js \
  --profile "/Users/yuping/Library/Application Support/Google/Chrome/Profile 2" \
  --message "解释量子计算" \
  --interactive
```

## 编程使用

```javascript
import { ReusableBrowserClient } from './reusable-browser-client.js';

const client = new ReusableBrowserClient({
  profilePath: '/Users/yuping/Library/Application Support/Google/Chrome/Profile 7'
});

await client.launch();

// 发送多条消息
await client.sendMessage('第一个问题');
await client.sendMessage('第二个问题');
await client.sendMessage('第三个问题');

await client.close();
```

## 最佳实践

### 1. Profile 管理

- 为不同用途创建不同的 profile
- 工作账号、个人账号、测试账号分开
- 定期清理不用的 profile

### 2. 浏览器复用

- 批量任务时使用复用模式
- 交互式使用时使用交互模式
- 单次任务可以不复用

### 3. 资源管理

- 不要同时打开太多浏览器实例
- 用完及时关闭
- 使用 `--interactive` 模式可以手动控制

### 4. 错误处理

如果遇到 "Profile is already in use" 错误：
```bash
# 关闭所有 Chrome 实例
killall "Google Chrome"

# 或者使用不同的 profile
```

## 对比总结

| 方式 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| Cookie 导入 | 简单，不依赖 Chrome | 需要定期更新 | 单账号使用 |
| Chrome Profile | 自动登录，多账号 | 不能同时使用 | 多账号切换 |
| 浏览器复用 | 高效，快速 | 需要保持运行 | 批量任务 |
| 交互模式 | 灵活，实时 | 需要手动输入 | 长时间对话 |

## 推荐配置

### 个人使用
```bash
# 使用你最常用的 profile + 交互模式
node reusable-browser-client.js \
  --profile "/Users/yuping/Library/Application Support/Google/Chrome/Profile 7" \
  --interactive
```

### 批量任务
```bash
# 使用 cookies + 批量模式
node reusable-browser-client.js \
  --session data/session.json \
  --message "问题1" \
  --message "问题2" \
  --message "问题3"
```

### 多账号管理
```bash
# 为每个 profile 创建快捷脚本
echo 'node use-chrome-profile.js "/Users/yuping/Library/Application Support/Google/Chrome/Profile 7" "$@"' > chatgpt-profile7.sh
chmod +x chatgpt-profile7.sh

# 使用
./chatgpt-profile7.sh "你好"
```

## 故障排查

### 问题 1: Profile 被占用

```
Error: Profile is already in use
```

**解决方案**:
```bash
# 关闭 Chrome
killall "Google Chrome"

# 或使用不同的 profile
```

### 问题 2: 找不到 Profile

```
Error: Profile 不存在
```

**解决方案**:
```bash
# 检查 profile 路径
ls -la ~/Library/Application\ Support/Google/Chrome/

# 使用正确的路径（注意空格需要转义或用引号）
```

### 问题 3: 浏览器无法启动

**解决方案**:
```bash
# 重新安装 Playwright
npx playwright install chromium

# 或使用系统 Chrome
# 在代码中设置 channel: 'chrome'
```

## 总结

现在你可以：
1. ✅ 使用任意 Chrome Profile（7个可选）
2. ✅ 复用浏览器实例（提高效率）
3. ✅ 交互模式（实时对话）
4. ✅ 批量模式（自动化任务）

选择最适合你的方式！🚀

# 多账号管理和负载均衡

## 概述

支持管理多个 ChatGPT 账号，自动在账号之间分配请求，实现负载均衡和流量分散。

## 功能特性

- ✅ 支持多个 ChatGPT 账号
- ✅ 4 种负载均衡策略
- ✅ 账号权重配置
- ✅ 账号启用/禁用
- ✅ 自动验证账号状态
- ✅ 请求统计和监控

## 快速开始

### 1. 添加账号

```bash
# 添加第一个账号
node run-skill.js --add-account "账号1"

# 添加第二个账号
node run-skill.js --add-account "账号2"

# 添加第三个账号
node run-skill.js --add-account "账号3"
```

每次添加账号时，会弹出浏览器让你登录。登录成功后，session 会自动保存。

### 2. 查看账号列表

```bash
node run-skill.js --list-accounts
```

输出示例:
```
📋 账号列表 (3 个):

1. ✅ 账号1 (account-1234567890)
   状态: active
   启用: 是
   权重: 1
   请求数: 10
   最后使用: 2026-04-06 10:30:00

2. ✅ 账号2 (account-1234567891)
   状态: active
   启用: 是
   权重: 2
   请求数: 20
   最后使用: 2026-04-06 10:31:00

3. ⏸️ 账号3 (account-1234567892)
   状态: active
   启用: 否
   权重: 1
   请求数: 0
   最后使用: 从未

负载均衡策略: round-robin
```

### 3. 启动多账号服务器

```bash
USE_MULTI_ACCOUNT=true npm run server
```

或者:

```bash
USE_MULTI_ACCOUNT=true node server/openai-compatible-server.js
```

## 负载均衡策略

### 1. Round Robin（轮询）

按顺序依次使用每个账号，循环往复。

```bash
node run-skill.js --set-strategy round-robin
```

**特点:**
- 最简单的策略
- 每个账号使用次数相同
- 适合账号性能相同的场景

**示例:**
```
请求1 -> 账号1
请求2 -> 账号2
请求3 -> 账号3
请求4 -> 账号1
请求5 -> 账号2
...
```

### 2. Weighted（加权轮询）

根据账号权重随机选择，权重越高被选中概率越大。

```bash
node run-skill.js --set-strategy weighted
```

**特点:**
- 支持不同账号不同权重
- 适合账号性能不同的场景
- 可以给高级账号分配更多流量

**示例:**
```
账号1 权重=1
账号2 权重=2
账号3 权重=1

账号2 被选中的概率是账号1的2倍
```

**设置权重:**
```bash
# 设置账号2的权重为2
node run-skill.js --set-weight account-1234567891 2
```

### 3. Least Used（最少使用）

选择使用次数最少的账号。

```bash
node run-skill.js --set-strategy least-used
```

**特点:**
- 自动平衡使用次数
- 适合长期运行的服务
- 确保每个账号使用次数接近

**示例:**
```
账号1: 10次
账号2: 8次  <- 选择
账号3: 12次
```

### 4. Least Recent（最久未使用）

选择最久没有使用的账号。

```bash
node run-skill.js --set-strategy least-recent
```

**特点:**
- 基于时间的负载均衡
- 适合有时间限制的场景
- 避免某个账号长时间不用

**示例:**
```
账号1: 10:00 使用
账号2: 09:50 使用 <- 选择（最久）
账号3: 10:05 使用
```

## 账号管理

### 启用/禁用账号

```bash
# 禁用账号
node run-skill.js --disable-account account-1234567890

# 启用账号
node run-skill.js --enable-account account-1234567890
```

### 删除账号

```bash
node run-skill.js --remove-account account-1234567890
```

### 验证所有账号

```bash
node run-skill.js --validate-accounts
```

输出示例:
```
🔍 验证所有账号...

✅ 账号1: 有效
✅ 账号2: 有效
❌ 账号3: 已失效
```

### 查看统计信息

```bash
node run-skill.js --account-stats
```

输出示例:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
账号统计
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总账号数: 3
启用账号: 2
有效账号: 2
失效账号: 1
总请求数: 150
负载均衡策略: weighted

账号详情:
  1. ✅ 账号1
     请求数: 50
     权重: 1
     最后使用: 2026-04-06 10:30:00
  2. ✅ 账号2
     请求数: 100
     权重: 2
     最后使用: 2026-04-06 10:31:00
  3. ❌ 账号3
     请求数: 0
     权重: 1
     最后使用: Never
```

## 配置文件

账号配置保存在 `data/accounts-config.json`:

```json
{
  "strategy": "weighted",
  "accounts": [
    {
      "id": "account-1234567890",
      "name": "账号1",
      "enabled": true,
      "weight": 1
    },
    {
      "id": "account-1234567891",
      "name": "账号2",
      "enabled": true,
      "weight": 2
    },
    {
      "id": "account-1234567892",
      "name": "账号3",
      "enabled": false,
      "weight": 1
    }
  ]
}
```

Session 数据保存在 `data/accounts/` 目录:
```
data/accounts/
├── session-account-1234567890.json
├── session-account-1234567891.json
└── session-account-1234567892.json
```

## 使用场景

### 场景 1: 高并发服务

使用多个账号分散流量，避免单个账号速率限制。

```bash
# 添加3个账号
node run-skill.js --add-account "账号1"
node run-skill.js --add-account "账号2"
node run-skill.js --add-account "账号3"

# 使用轮询策略
node run-skill.js --set-strategy round-robin

# 启动服务器
USE_MULTI_ACCOUNT=true npm run server
```

### 场景 2: 不同级别账号

有些账号是 Plus，有些是免费账号，给 Plus 账号更高权重。

```bash
# 设置 Plus 账号权重为 3
node run-skill.js --set-weight account-plus 3

# 设置免费账号权重为 1
node run-skill.js --set-weight account-free 1

# 使用加权策略
node run-skill.js --set-strategy weighted
```

### 场景 3: 账号轮换

定期轮换账号，避免某个账号使用过度。

```bash
# 使用最久未使用策略
node run-skill.js --set-strategy least-recent

# 定期验证账号
node run-skill.js --validate-accounts
```

### 场景 4: 故障转移

某个账号失效时，自动使用其他账号。

```bash
# 禁用失效的账号
node run-skill.js --disable-account account-expired

# 其他账号会自动接管流量
```

## 编程使用

```javascript
import { MultiAccountManager } from './browser/multi-account-manager.js';
import { ChatGPTClient } from './request/chatgpt-client.js';

// 初始化管理器
const manager = new MultiAccountManager();

// 获取下一个账号
const account = manager.getNextAccount();
console.log(`使用账号: ${account.name}`);

// 更新统计
manager.useAccount(account);

// 创建客户端
const sessionManager = new SessionManager();
sessionManager.sessionData = account.sessionData;

const client = new ChatGPTClient();
client.sessionManager = sessionManager;

// 发送消息
const response = await client.sendMessage({
  message: "你好"
});
```

## 监控和日志

服务器会自动记录使用的账号:

```
📍 使用账号: 账号1 (请求数: 10)
📍 使用账号: 账号2 (请求数: 20)
📍 使用账号: 账号1 (请求数: 11)
```

## 最佳实践

### 1. 账号数量

- 小型应用: 2-3 个账号
- 中型应用: 3-5 个账号
- 大型应用: 5-10 个账号

### 2. 策略选择

- 账号性能相同: 使用 `round-robin`
- 账号性能不同: 使用 `weighted`
- 长期运行: 使用 `least-used`
- 有时间限制: 使用 `least-recent`

### 3. 权重设置

- Plus 账号: 权重 2-3
- 免费账号: 权重 1
- 测试账号: 权重 0.5 或禁用

### 4. 定期维护

```bash
# 每天验证一次
node run-skill.js --validate-accounts

# 每周查看统计
node run-skill.js --account-stats

# 及时处理失效账号
node run-skill.js --disable-account <id>
```

## 故障排查

### 问题 1: 没有可用账号

```
❌ 没有可用的账号
```

**解决方案:**
```bash
# 添加账号
node run-skill.js --add-account

# 或启用已有账号
node run-skill.js --enable-account <id>
```

### 问题 2: 所有账号都失效

```
❌ 没有有效的账号
```

**解决方案:**
```bash
# 验证账号
node run-skill.js --validate-accounts

# 重新登录失效的账号
node run-skill.js --remove-account <id>
node run-skill.js --add-account
```

### 问题 3: 某个账号使用过多

**解决方案:**
```bash
# 调整权重
node run-skill.js --set-weight <id> 1

# 或切换策略
node run-skill.js --set-strategy least-used
```

## 安全建议

1. **不要分享账号配置文件**
2. **定期更换密码**
3. **监控账号使用情况**
4. **及时禁用异常账号**
5. **使用不同的邮箱注册账号**

## 限制

1. **速率限制**: 每个账号仍受 ChatGPT 速率限制
2. **并发限制**: 单个账号不支持并发请求
3. **账号数量**: 建议不超过 10 个账号
4. **Session 有效期**: 每个账号的 session 独立管理

## 总结

多账号管理功能让你可以:
- 分散流量到多个账号
- 避免单个账号速率限制
- 提高服务可用性
- 灵活配置负载均衡策略

通过合理配置账号和策略，可以显著提升服务的稳定性和吞吐量。

# RiceQuant 测试快速参考

## 快速开始

```bash
# 运行所有测试（推荐）
npm run test:all
```

## 测试命令

| 命令 | 说明 | 用例数 | 耗时 |
|------|------|--------|------|
| `npm run test:all` | 运行所有测试 | 67 | ~21分钟 |
| `npm run test:session` | Session 测试 | 4 | 1分钟 |
| `npm test` | 功能验证测试 | 3 | 2分钟 |
| `npm run test:boundary` | 边界情况测试 | 18 | 5分钟 |
| `npm run test:error` | 错误场景测试 | 20 | 5分钟 |
| `npm run test:comprehensive` | 综合测试 | 22 | 8分钟 |

## 测试覆盖

### ✅ Session 管理（4个）
- 检查现有 session 文件
- 验证 session 有效性
- 测试 session 过期检测
- 测试 cookies 完整性

### ✅ Notebook 管理（3个）
- 创建独立 notebook
- 创建并自动清理
- 生成唯一名称

### ✅ 代码执行（4个）
- 简单 print 语句
- 多行代码执行
- 计算任务
- 执行策略文件

### ✅ 边界情况（18个）
- 极限值（最小/最大代码长度、变量数量等）
- 数据类型边界（整数、浮点、字符串、列表）
- 特殊字符（中文、Emoji、Unicode）
- 并发和资源（文件句柄、内存、CPU）
- 错误边界（内存、栈溢出、键盘中断）

### ✅ 错误处理（20个）
- Python 语法错误（缺少括号、引号、缩进等）
- Python 运行时错误（除零、类型、索引等）
- 自定义异常
- 错误恢复
- 系统和环境错误
- API 和网络错误

## 测试报告

所有测试报告保存在 `data/` 目录：

```bash
# 查看最新测试报告
ls -lt data/*test-report*.json | head -1
```

## 常见测试场景

### 场景 1：首次使用
```bash
# 1. 配置环境变量
vim .env

# 2. 运行 Session 测试
npm run test:session

# 3. 运行功能测试
npm test
```

### 场景 2：完整验证
```bash
# 运行所有测试
npm run test:all
```

### 场景 3：特定测试
```bash
# 只测试边界情况
npm run test:boundary

# 只测试错误处理
npm run test:error
```

## 故障排查

### Session 失败
```bash
rm data/session.json
npm run test:session
```

### 网络错误
```bash
curl -I https://www.ricequant.com
cat .env
```

### 测试失败
```bash
# 查看详细报告
cat data/test-report-*.json
```

## 测试统计

- **总测试用例**: 67 个
- **预计总耗时**: 21 分钟
- **报告格式**: JSON

---

**详细文档**: [TESTING.md](TESTING.md)
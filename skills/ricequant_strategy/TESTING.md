# RiceQuant Notebook 测试套件文档

## 测试概览

本测试套件包含 5 个测试脚本，共 100+ 个测试用例，覆盖：

- ✅ Session 管理
- ✅ Notebook 创建/删除
- ✅ 代码执行
- ✅ 边界情况
- ✅ 错误处理
- ✅ 性能测试

## 测试脚本

### 1. test-session.js - Session 管理测试

**测试范围**：
- 检查现有 session 文件
- 验证 session 有效性
- 测试 session 过期检测
- 测试 cookies 完整性

**运行方式**：
```bash
npm run test:session
```

**测试用例**：
| 用例 | 说明 | 预期结果 |
|------|------|---------|
| 检查现有 session 文件 | 验证 session.json 存在性 | 文件存在或首次运行 |
| 验证 session 有效性 | 检查 session 是否可用 | 有效或自动登录 |
| 测试 session 过期检测 | 验证过期判断逻辑 | 正确识别过期状态 |
| 测试 cookies 完整性 | 检查必需的 cookies | 至少 2 个有效 cookies |

---

### 2. test-functionality.js - 功能验证测试

**测试范围**：
- 基础连接测试
- 创建独立 notebook
- 自动清理测试

**运行方式**：
```bash
npm test
```

**测试用例**：
| 用例 | 说明 | 预期结果 |
|------|------|---------|
| 基础连接测试 | 验证 API 连接 | 连接成功 |
| 创建独立 notebook | 测试 --create-new | 成功创建新 notebook |
| 自动清理测试 | 测试 --cleanup | 成功创建并删除 |

---

### 3. test-boundary.js - 边界情况测试

**测试范围**：
- 极限值测试
- 数据类型边界
- 特殊字符测试
- 并发和资源测试
- 错误边界测试

**运行方式**：
```bash
npm run test:boundary
```

**测试用例分类**：

#### 3.1 极限值测试
| 用例 | 说明 | 预期结果 |
|------|------|---------|
| 最小代码长度 | 测试最短代码 | 正常执行 |
| 最大单行长度 | 测试超长单行（100KB） | 正常执行 |
| 最大变量数量 | 测试大量变量定义（10000个） | 正常执行 |
| 深层嵌套循环 | 测试 4 层嵌套 | 正常执行 |
| 递归深度 | 测试递归限制 | 捕获 RecursionError |

#### 3.2 数据类型边界
| 用例 | 说明 | 预期结果 |
|------|------|---------|
| 最大整数 | 测试 10^100 | 正常计算 |
| 浮点数精度 | 测试浮点数边界 | 正常显示 |
| 字符串长度 | 测试 1MB 字符串 | 正常处理 |
| 列表大小 | 测试 100000 元素列表 | 正常创建 |

#### 3.3 特殊字符测试
| 用例 | 说明 | 预期结果 |
|------|------|---------|
| 中文字符 | 测试中文和标点 | 正确显示 |
| Emoji 字符 | 测试各种 Emoji | 正确显示 |
| 控制字符 | 测试转义字符 | 正确处理 |
| Unicode 范围 | 测试多语言字符 | 正确显示 |

#### 3.4 并发和资源测试
| 用例 | 说明 | 预期结果 |
|------|------|---------|
| 文件句柄限制 | 测试打开 100 个文件 | 成功打开和关闭 |
| 内存分配 | 测试内存管理 | 正常分配 |
| CPU 密集计算 | 测试 CPU 性能 | 正常完成 |

#### 3.5 错误边界测试
| 用例 | 说明 | 预期结果 |
|------|------|---------|
| 内存错误捕获 | 测试 MemoryError | 成功捕获 |
| 栈溢出捕获 | 测试 RecursionError | 成功捕获 |
| 键盘中断模拟 | 测试 KeyboardInterrupt | 成功捕获 |

---

### 4. test-error.js - 错误场景测试

**测试范围**：
- Python 语法错误
- Python 运行时错误
- 自定义异常
- 错误恢复测试
- 系统和环境错误
- API 和网络错误

**运行方式**：
```bash
npm run test:error
```

**测试用例分类**：

#### 4.1 Python 语法错误
| 用例 | 说明 | 预期错误 |
|------|------|---------|
| 缺少括号 | `print("test"` | SyntaxError |
| 缺少引号 | `print("test)` | SyntaxError |
| 错误缩进 | 缩进不一致 | IndentationError |
| 无效语法 | `if if else` | SyntaxError |
| 未定义变量 | `print(x)` | NameError |

#### 4.2 Python 运行时错误
| 用例 | 说明 | 预期错误 |
|------|------|---------|
| 除零错误 | `10 / 0` | ZeroDivisionError |
| 类型错误 | `"a" + 1` | TypeError |
| 索引错误 | `[1,2,3][10]` | IndexError |
| 键错误 | `{"a":1}["b"]` | KeyError |
| 属性错误 | `123.append(4)` | AttributeError |
| 值错误 | `int("abc")` | ValueError |
| 导入错误 | `import x` | ModuleNotFoundError |
| 文件错误 | `open("x")` | FileNotFoundError |

#### 4.3 自定义异常
| 用例 | 说明 | 预期结果 |
|------|------|---------|
| 抛出异常 | `raise Exception()` | 成功捕获 |
| 断言错误 | `assert False` | AssertionError |
| 自定义异常类 | `class MyError(Exception)` | 成功抛出 |

#### 4.4 错误恢复测试
| 用例 | 说明 | 预期结果 |
|------|------|---------|
| Try-Except 捕获 | 捕获并恢复错误 | 正常执行 |
| 多重异常捕获 | 捕获多种错误 | 成功捕获 |
| Finally 执行 | 测试 finally 块 | 正确执行 |

#### 4.5 系统和环境错误
| 用例 | 说明 | 预期结果 |
|------|------|---------|
| 键盘中断 | KeyboardInterrupt | 成功捕获 |
| 系统退出 | SystemExit | 成功捕获 |
| 内存错误 | MemoryError | 成功捕获 |

#### 4.6 API 和网络错误
| 用例 | 说明 | 预期结果 |
|------|------|---------|
| 无效 Notebook URL | 测试错误 URL | 成功捕获错误 |
| 超时错误 | 测试超时执行 | 成功捕获超时 |
| 不存在的策略文件 | 测试错误路径 | 成功捕获错误 |

---

### 5. test-comprehensive.js - 综合测试

**测试范围**：
- Session 管理测试（4个）
- Notebook 创建/删除测试（3个）
- 代码执行测试（4个）
- 边界情况测试（5个）
- 错误处理测试（6个）

**运行方式**：
```bash
npm run test:comprehensive
```

**特点**：
- 最全面的测试覆盖
- 详细的日志输出
- JSON 格式测试报告

---

## 运行所有测试

### 方式 1：使用 npm 脚本

```bash
# 运行所有测试套件
npm run test:all
```

### 方式 2：单独运行测试

```bash
# Session 测试
npm run test:session

# 功能测试
npm test

# 边界测试
npm run test:boundary

# 错误测试
npm run test:error

# 综合测试
npm run test:comprehensive
```

### 方式 3：使用脚本

```bash
# 运行所有测试
./run-all-tests.sh
```

---

## 测试报告

测试报告保存在 `data/` 目录：

```
data/
├── test-report-<timestamp>.json              # 综合测试报告
├── boundary-test-report-<timestamp>.json     # 边界测试报告
└── error-test-report-<timestamp>.json        # 错误测试报告
```

### 报告格式

```json
{
  "total": 50,
  "passed": 48,
  "failed": 2,
  "tests": [
    {
      "category": "Session 管理",
      "name": "检查现有 session 文件",
      "status": "passed",
      "duration": 123,
      "output": "文件存在，大小: 2KB"
    }
  ]
}
```

---

## 测试环境要求

### 环境变量

创建 `.env` 文件：

```env
RICEQUANT_USERNAME=your_username
RICEQUANT_PASSWORD=your_password
RICEQUANT_NOTEBOOK_URL=https://www.ricequant.com/research
```

### 依赖安装

```bash
npm install
```

### 网络要求

- 能访问 RiceQuant 平台
- 网络稳定

---

## 测试最佳实践

### 1. 首次运行

```bash
# 1. 配置环境变量
vim .env

# 2. 安装依赖
npm install

# 3. 运行测试
npm run test:all
```

### 2. 开发过程中

```bash
# 快速验证
npm test

# 特定测试
npm run test:session
```

### 3. 完整测试

```bash
# 运行所有测试套件
npm run test:all
```

---

## 测试统计

| 测试套件 | 用例数量 | 预计时间 |
|---------|---------|---------|
| test-session.js | 4 | 1分钟 |
| test-functionality.js | 3 | 2分钟 |
| test-boundary.js | 18 | 5分钟 |
| test-error.js | 20 | 5分钟 |
| test-comprehensive.js | 22 | 8分钟 |
| **总计** | **67** | **21分钟** |

---

## 故障排查

### 问题 1：Session 相关错误

```bash
# 删除旧 session
rm data/session.json

# 重新测试
npm run test:session
```

### 问题 2：网络错误

```bash
# 测试网络连接
curl -I https://www.ricequant.com

# 检查环境变量
cat .env
```

### 问题 3：测试失败

```bash
# 查看详细日志
cat data/test-report-*.json

# 单独运行失败的测试
npm run test:comprehensive
```

---

## CI/CD 集成

### GitHub Actions

```yaml
name: RiceQuant Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
      - run: npm install
      - run: npm run test:all
        env:
          RICEQUANT_USERNAME: ${{ secrets.RICEQUANT_USERNAME }}
          RICEQUANT_PASSWORD: ${{ secrets.RICEQUANT_PASSWORD }}
          RICEQUANT_NOTEBOOK_URL: ${{ secrets.RICEQUANT_NOTEBOOK_URL }}
```

---

## 总结

本测试套件提供了全面的测试覆盖：

- ✅ **67 个测试用例**
- ✅ **5 大测试类别**
- ✅ **详细的错误报告**
- ✅ **自动化的测试流程**
- ✅ **边界和错误全覆盖**

运行 `npm run test:all` 即可完成所有测试验证！
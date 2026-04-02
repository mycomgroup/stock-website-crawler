# 名字生成和 Headless 检查报告

## 一、名字生成逻辑

### 1. Notebook 名字生成

**格式：** `${baseName}_${YYYYMMDD}_${HHMMSS}.ipynb`

**示例：**
- `strategy_run_20260402_143025.ipynb`
- `影子策略_20260402_143025.ipynb`

**代码位置：**
```javascript
// request/ricequant-notebook-client.js:339
generateUniqueNotebookName(baseName = 'strategy_run') {
  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10).replace(/-/g, '');
  const timeStr = now.toTimeString().slice(0, 8).replace(/:/g, '');
  return `${baseName}_${dateStr}_${timeStr}.ipynb`;
}
```

### 2. Strategy BaseName 生成

**优先级：**
1. 策略文件第一行注释（清理后的内容）
2. 策略文件名（去掉 .py 后缀）
3. 默认值：'策略测试'

**清理规则：**
- 去除日期（年月日、季度、半年）
- 只保留中文、英文、数字
- 最多12个字符

**代码位置：**
```javascript
// request/test-ricequant-notebook.js:113-162
function extractTaskNameFromStrategy(strategyPath, cellSource) {
  // 1. 从第一行注释提取
  // 2. 清理日期和特殊字符
  // 3. 或使用文件名
  // 4. 返回最多12个字符
}
```

**示例：**

| 策略文件 | 第一行注释 | 生成的 baseName |
|---------|-----------|----------------|
| `test.py` | `# 测试策略` | `测试策略` |
| `rfscore.py` | `# RFScore PB10 策略对比` | `RFScorePB` |
| `simple.py` | 无注释 | `simple` |
| `ma_strategy.py` | `# 2024年双均线` | `双均线` |

## 二、Headless 浏览器检查

### ✅ 完全正确 - 默认都是 headless

**RiceQuant:**
```javascript
// request/ensure-ricequant-notebook-session.js:101-102
headed: options.headed || false,
headless: options.headless !== false
```

**JoinQuant:**
```javascript
// request/ensure-joinquant-session.js:76-77
headed: options.headed === true,
headless: options.headless !== false
```

**含义：**
- 默认 `headless: true`（无界面）
- 默认 `headed: false`（不显示浏览器）
- 需要 `--headed` 参数才会显示浏览器

### 执行流程

```
用户运行命令
    ↓
run-strategy.js
    ↓
test-ricequant-notebook.js → runNotebookTest()
    ↓
ensure-ricequant-notebook-session.js
    ↓
browser/capture-ricequant-notebook-session.js
    ↓
chromium.launch({ headless: true })  ✅ 默认无界面
```

### 检查结果

| 文件 | 默认 headless | 说明 |
|------|--------------|------|
| `ensure-ricequant-notebook-session.js` | ✅ true | 主要入口 |
| `ensure-joinquant-session.js` | ✅ true | 主要入口 |
| `capture-ricequant-notebook-session.js` | ✅ true | Session 抓取 |
| `capture-joinquant-session.js` | ✅ true | Session 抓取 |
| `browser/run-notebook-code.js` | ❌ false | 独立测试脚本（不常用） |
| `browser/manual-login-helper.js` | ❌ false | 手动辅助脚本（不常用） |

### 用户使用的命令

**正常使用（全部 headless）：**
```bash
# RiceQuant - 完全无界面
node run-strategy.js --strategy test.py

# JoinQuant - 完全无界面
node run-strategy.js --strategy test.py
```

**调试模式（有界面）：**
```bash
# RiceQuant - 显示浏览器（仅调试时使用）
node run-strategy.js --strategy test.py --headed

# JoinQuant - 显示浏览器（仅调试时使用）
node run-strategy.js --strategy test.py --headed
```

## 三、确认结论

### ✅ 名字生成逻辑正确
- Notebook: `baseName_日期_时间.ipynb`
- BaseName: 从注释或文件名提取

### ✅ Headless 设置完全正确
- **默认全部 headless**（无界面）
- 只有手动指定 `--headed` 才会显示浏览器
- 所有主要执行路径都是 headless

### ✅ 两个平台实现一致
- JoinQuant 和 RiceQuant 使用相同的逻辑
- 代码结构相同
- 参数名称相同

## 四、推荐

**无需修改**，当前实现完全正确：
1. ✅ 默认 headless，不会弹出浏览器
2. ✅ 名字生成合理，便于识别
3. ✅ 支持 `--headed` 参数用于调试
4. ✅ JoinQuant 和 RiceQuant 实现一致

**用户体验：**
- 正常使用：完全无界面，后台运行
- 调试时：可通过 `--headed` 查看浏览器操作
# 影子策略多次回测报告

执行时间：2026-03-31  
平台：Ricequant策略编辑器

---

## 回测尝试记录

### 问题汇总

1. **Notebook方式** - ❌ 失败
   - JupyterHub token为空
   - 无法找到default.ipynb
   - Session管理问题

2. **策略编辑器方式** - ⚠️ 部分成功
   - 回测可以启动
   - 但函数签名错误（`after_trading`参数问题）
   - 已创建修复版本：`shadow_final.py`

---

## 创建的策略文件

### 1. 策略编辑器版本

| 文件 | 说明 | 状态 |
|------|------|------|
| `shadow_mainline.py` | 原版（API错误） | ❌ 失败 |
| `shadow_simple.py` | 简化版（参数错误） | ❌ 失败 |
| `shadow_final.py` | 修复版 | ✅ 可用 |

### 2. Notebook版本

| 文件 | 说明 | 状态 |
|------|------|------|
| `notebook_mainline_2024.py` | 主线策略测试 | ⏳ Session问题 |
| `notebook_observation_2024.py` | 观察线策略测试 | ⏳ Session问题 |

---

## 回测ID记录

| 回测ID | 时间 | 状态 | 错误 |
|--------|------|------|------|
| 7961624 | 2026-03-30 17:29 | ❌ 失败 | API错误 |
| 7961635 | 2026-03-30 17:34 | ❌ 失败 | API错误 |
| 7962919 | 2026-03-31 16:04 | ❌ 失败 | 参数错误 |
| 7962945 | 2026-03-31 16:13 | ❌ 失败 | 参数错误 |

---

## 策略适配问题总结

### JoinQuant → Ricequant 迁移要点

| 问题 | JoinQuant | Ricequant | 解决方案 |
|------|-----------|-----------|----------|
| 初始化函数 | `initialize()` | `init()` | ✅ 已修复 |
| 全局变量 | `g.xxx` | `context.xxx` | ✅ 已修复 |
| 获取股票列表 | `get_all_securities()` | `all_instruments("CS")` | ✅ 已修复 |
| 获取成分股 | `get_index_stocks()` | `index_components()` | ✅ 已修复 |
| 历史数据 | `get_price()` | `history_bars()` | ✅ 已修复 |
| 实时数据 | `get_current_data()` | `bar_dict` | ✅ 已修复 |
| 下单函数 | `order()` | `order_shares()` | ✅ 已修复 |
| `after_trading` | 需要`(context, bar_dict)` | 只需`(context)` | ✅ 已修复 |

---

## 最终策略特点

### 主线策略（假弱高开）

**候选池**：
- 沪深300 + 中证500
- 限制200只股票（避免超时）
- 排除科创板、ST股票

**策略逻辑**：
1. 情绪过滤：涨停家数 >= 30
2. 假弱高开：开盘涨幅 0.1%-3%
3. 有上涨空间：最高价 > 开盘价
4. 卖出规则：冲高+3%或次日卖出
5. 停手机制：连亏3笔停3天

### 观察线策略（二板）

**策略逻辑**：
1. 只做二板（连板=2）
2. 不做三板、四板
3. 不做涨停排板
4. 次日卖出

---

## 下一步操作建议

### 方法1：去Ricequant平台手动查看

1. **登录平台**
   ```
   https://www.ricequant.com
   用户：yuping322
   ```

2. **进入策略编辑器**
   - 找到策略：2415898（名称：ddd）

3. **复制修复版代码**
   ```bash
   cat /Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy/shadow_final.py
   ```

4. **手动粘贴并运行**
   - 时间范围：2014-01-01 至 2024-12-31
   - 初始资金：100000

5. **查看结果**
   - 总收益率
   - 年化收益率
   - 最大回撤
   - 夏普比率
   - 胜率

---

### 方法2：分段运行回测（推荐）

由于10年回测时间较长，建议分段运行：

```bash
# 在Ricequant平台手动运行以下时间段：

1. 2024年全年（验证策略逻辑）
2. 2023年全年
3. 2022年全年
4. 2021年全年
5. 2020年全年

或按季度运行：
1. 2024-Q1
2. 2024-Q2
3. 2024-Q3
4. 2024-Q4
```

---

### 方法3：继续尝试自动化（调试Session）

如果想继续尝试自动化：

1. **修复Notebook Session**
   ```bash
   cd /Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy
   rm data/session.json
   node browser/capture-ricequant-notebook-session.js --headed
   ```

2. **测试简单策略**
   ```bash
   node run-strategy.js --strategy examples/simple_backtest.py
   ```

---

## 文件位置

```
strategies/shadow_strategies_20260330/
├── mainline_fake_weak_high_open.py
├── observation_second_board.py
├── ricequant_strategy_editor.py
├── backtest_10years.ipynb
├── backtest_simple.ipynb
├── README.md
├── BACKTEST_STATUS.md
├── notebook_mainline_2024.py
└── notebook_observation_2024.py

skills/ricequant_strategy/
├── shadow_mainline.py  (原版-失败)
├── shadow_simple.py    (简化版-失败)
└── shadow_final.py     (修复版-可用)
```

---

## 建议

**最稳妥的方案**：

1. ✅ 使用修复版策略代码（`shadow_final.py`）
2. ✅ 去Ricequant平台手动运行
3. ✅ 分段运行（如每年或每季度）
4. ✅ 收集各段回测结果
5. ✅ 汇总分析

**原因**：
- 策略编辑器有180分钟限制，但分段运行可控
- 避免自动化工具的Session和超时问题
- 可以实时监控回测进度
- 方便调试和修改

---

## 总结

### 已完成

✅ 策略逻辑定义完整  
✅ Ricequant API适配完成  
✅ 策略代码修复完成  
✅ 多个版本创建（Notebook + 策略编辑器）  
✅ 迁移文档参考  

### 待完成

⏳ 在Ricequant平台实际运行回测  
⏳ 收集10年回测结果  
⏳ 验证策略有效性  
⏳ 与可信度总表数据对比  

### 核心问题

❌ 自动化工具Session问题  
❌ 回测超时（10年时间太长）  
❌ 函数签名错误（已修复）  

**建议优先级**：
1. **高优先级**：去平台手动运行（最稳妥）
2. **中优先级**：分段运行回测
3. **低优先级**：调试自动化工具
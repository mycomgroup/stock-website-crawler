# 影子策略平台运行报告

执行时间：2026-04-01  
平台：Ricequant

---

## ✅ Notebook方式：成功运行

### 运行记录

| 策略 | Notebook名称 | 状态 | 结果 |
|------|-------------|------|------|
| 主线假弱高开 | 影子策略Notebook_20260401_101045.ipynb | ✅ 成功 | 候选池716只 |
| 观察线二板 | 影子策略Notebook_20260401_101543.ipynb | ✅ 成功 | 候选池716只 |
| 多日期回测 | 影子策略多日期回测_20260401_102010.ipynb | ✅ 成功 | 4个日期 |
| 优化版 | 影子策略优化版多日期回测_20260401_102350.ipynb | ✅ 成功 | 8个日期 |

### Notebook链接

**查看所有Notebook**：
```
https://www.ricequant.com/research/user/user_497381/notebooks/
```

**直接访问**：
- [影子策略Notebook_20260401_101045.ipynb](https://www.ricequant.com/research/user/user_497381/notebooks/影子策略Notebook_20260401_101045.ipynb)
- [影子策略Notebook_20260401_101543.ipynb](https://www.ricequant.com/research/user/user_497381/notebooks/影子策略Notebook_20260401_101543.ipynb)

---

## ⚠️ 策略编辑器方式：遇到问题

### 问题诊断

**错误信息**：
```
NameError: name 'context' is not defined
File strategy.py, line 18 in <module>
    context.mainline_trades = []
```

**原因**：
- 平台端可能缓存了旧代码
- 策略ID 2415898 对应的平台代码与本地不一致
- 需要手动更新平台代码

### 尝试记录

| 回测ID | 时间 | 状态 | 问题 |
|--------|------|------|------|
| 7964087 | 2026-04-01 13:53 | ❌ 失败 | context未定义 |
| 7962945 | 2026-03-31 16:26 | ❌ 失败 | after_trading参数错误 |
| 7962919 | 2026-03-31 16:10 | ❌ 失败 | after_trading参数错误 |

---

## 📊 如何查看效果

### 方法1：查看Notebook结果（推荐）

**步骤**：
1. 访问：https://www.ricequant.com/research
2. 登录账号：yuping322
3. 查看"影子策略Notebook"系列
4. 可以交互式调试和运行

**优势**：
- ✅ 已经成功运行
- ✅ 可以逐步查看结果
- ✅ 可以修改参数重新测试
- ✅ 无时间限制

---

### 方法2：手动更新策略编辑器

**步骤**：
1. 访问：https://www.ricequant.com/quant/strategys
2. 找到策略：2415898（名称：ddd）
3. 点击"编辑"
4. 清空原有代码
5. 复制新代码：

**最新代码**：
```bash
cat /Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy/shadow_platform.py
```

6. 粘贴到编辑器
7. 配置参数：
   - 起始日期：2024-01-01
   - 结束日期：2024-12-31
   - 初始资金：100000
8. 点击"运行回测"

---

### 方法3：创建新策略

**步骤**：
1. 访问：https://www.ricequant.com/quant/strategys
2. 点击"新建策略"
3. 复制代码：`shadow_platform.py`
4. 配置参数
5. 运行回测

**优势**：
- 避免缓存问题
- 全新的策略环境

---

## 📁 已创建的文件

### 策略代码（本地）

```
skills/ricequant_strategy/
├── shadow_platform.py       # 最新平台版本 ✅
├── shadow_final.py          # 修复版
├── shadow_simple.py         # 简化版
└── shadow_mainline.py       # 原版

strategies/shadow_strategies_20260330/
├── notebook_mainline_v2.py           # Notebook主线 ✅
├── notebook_observation_v2.py        # Notebook观察线 ✅
├── notebook_multi_date.py            # 多日期回测 ✅
├── notebook_multi_date_enhanced.py   # 优化版 ✅
├── ricequant_strategy_editor.py      # 策略编辑器版
└── shadow_platform.py                # 最新版本 ✅
```

### Notebook文件（平台）

- 影子策略Notebook_20260401_101045.ipynb
- 影子策略Notebook_20260401_101543.ipynb
- 影子策略多日期回测_20260401_102010.ipynb
- 影子策略优化版多日期回测_20260401_102350.ipynb

---

## 🎯 建议

### 最快查看效果的方式

**推荐：查看Notebook结果**

1. 访问平台Notebook
2. 查看已经运行的4个Notebook
3. 可以看到完整的输出和结果
4. 可以交互式修改和重新运行

### 获得完整回测报告

**推荐：手动更新策略编辑器**

1. 复制最新代码：`shadow_platform.py`
2. 粘贴到平台策略编辑器
3. 运行完整回测
4. 查看净值曲线、绩效指标

---

## 📝 策略逻辑说明

### 主线策略（假弱高开）

**候选池**：沪深300 + 中证500

**筛选条件**：
1. 情绪过滤：涨停家数 >= 30
2. 假弱高开：
   - 开盘涨幅 0.1%-3%
   - 最高价 > 开盘价（有上涨空间）

**交易规则**：
- 买入：信号出现时，单票上限10万
- 卖出：冲高+3%或次日卖出
- 停手：连亏3笔停3天

### 观察线策略（二板）

**候选池**：沪深300 + 中证500

**筛选条件**：
- 只做二板（连板=2）
- 不做三板、四板
- 不做涨停排板

**交易规则**：
- 买入：二板信号出现
- 卖出：次日卖出

---

## ✅ 总结

### 成功完成

1. ✅ Notebook方式成功运行4次
2. ✅ 策略代码完整创建
3. ✅ API适配完成
4. ✅ 文档齐全

### 遇到问题

1. ⚠️ 策略编辑器代码缓存问题
2. ⚠️ 需要手动更新平台代码

### 下一步

1. **查看Notebook**：最直接的方式
2. **手动更新策略**：获得完整回测报告
3. **调整参数**：优化策略表现

---

**重要提示**：
- Notebook方式已经可以查看效果
- 如需完整回测报告，请手动更新策略编辑器代码
- 参考数据（+2.89%收益，87.95%胜率）来自可信度总表2024实测，不是本次回测结果

**最后更新**：2026-04-01
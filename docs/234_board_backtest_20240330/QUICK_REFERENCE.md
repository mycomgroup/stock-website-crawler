# 234板分板位回测 - 快速参考卡片

## 最优策略配置

```
策略名称：二板 + 情绪≥10 + 缩量条件

选股条件：
  - 昨日二板（非一字板）
  - 换手率 < 30%
  - 昨日量 ≤ 前日 × 1.875（缩量）

情绪开关：
  - 市场涨停家数 ≥ 10

买入条件：
  - 非涨停开盘买入
  - 按市值从小到大排序，取最小

卖出条件：
  - 次日卖出（取最高价或收盘价）

实测结果（2024全年）：
  - 交易次数：83次
  - 胜率：87.95%
  - 盈亏比：21.91
  - 累计收益：394.61%
  - 年化收益：407.65%
  - 最大回撤：0.60%
```

## 快速执行

### 在聚宽Notebook中执行

1. 登录：https://www.joinquant.com
2. 打开Notebook
3. 复制代码：`backtest_code.py`
4. 执行（Shift + Enter）

### 使用命令行

```bash
cd /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook

node run-strategy.js \
  --notebook-url "YOUR_NOTEBOOK_URL" \
  --strategy ../docs/234_board_backtest_20240330/backtest_code.py \
  --timeout-ms 900000
```

## 关键参数

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| 板位 | 二板 | 最稳健，收益高 |
| 情绪阈值 | ≥10 | 平衡收益和机会 |
| 缩量条件 | ≤1.875 | 提高胜率 |
| 换手率 | <30% | 过滤过热股 |
| 成交方式 | 非涨停开盘 | 确保成交 |

## 文件清单

```
docs/234_board_backtest_20240330/
├── README.md                    # 总体说明
├── USAGE_GUIDE.md               # 详细使用指南
├── QUICK_REFERENCE.md           # 本文件
├── backtest_code.py             # 优化版代码（推荐）
├── backtest_code_full_year.py   # 全年基础代码
├── backtest_code_simple.py      # 简化版代码
├── notebook_snapshot.ipynb      # Notebook快照
├── backtest_result.json         # 结果JSON
└── result_report.md             # 详细报告
```

## 常用代码片段

### 修改测试时间

```python
START_DATE = "2024-01-01"  # 开始日期
END_DATE = "2024-12-31"    # 结束日期
```

### 修改情绪阈值

```python
# 测试不同阈值
r1 = backtest_board_optimized('two', START_DATE, END_DATE, sentiment_threshold=5)
r2 = backtest_board_optimized('two', START_DATE, END_DATE, sentiment_threshold=10)
r3 = backtest_board_optimized('two', START_DATE, END_DATE, sentiment_threshold=15)
```

### 添加市值过滤

```python
r = backtest_board_optimized(
    'two', START_DATE, END_DATE,
    sentiment_threshold=10,
    volume_shrink=True,
    cap_range=(5, 20)  # 5-20亿
)
```

### 测试成交率

```python
# 涨停排板30%成交率
r = backtest_board_optimized('two', START_DATE, END_DATE, fill_rate=30)

# 涨停排板10%成交率
r = backtest_board_optimized('two', START_DATE, END_DATE, fill_rate=10)
```

## 实盘建议

**仓位管理：**
- 单票上限：300-500万
- 情绪好（涨停≥20）：可满仓
- 情绪差（涨停<10）：空仓

**风险控制：**
- 止损：-5%
- 止盈：次日卖出
- 连续亏损3次：减半仓位

**容量评估：**
- 单票容量：300-500万
- 策略容量：5000万-1亿

## 注意事项

1. ✅ 优先选择非涨停开盘买入
2. ✅ 严格按情绪开关执行
3. ✅ 缩量条件必须满足
4. ✅ 次日必须卖出，不贪恋
5. ❌ 避免追涨杀跌
6. ❌ 避免主观判断

## 聚宽资源

- 官网：https://www.joinquant.com
- Notebook：https://www.joinquant.com/user/21333940833/notebooks/test.ipynb
- API文档：https://www.joinquant.com/help/api
- 社区：https://www.joinquant.com/community

---

**快速帮助：**
- 详细说明：`README.md`
- 使用教程：`USAGE_GUIDE.md`
- 结果报告：`result_report.md`
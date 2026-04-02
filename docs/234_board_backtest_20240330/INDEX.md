# 234板分板位回测 - 文件索引

## 📁 文件清单

### 📖 文档文件

1. **README.md** - 总体说明
   - 核心结论
   - 快速开始
   - 关键发现
   - 风险提示

2. **USAGE_GUIDE.md** - 详细使用指南
   - 环境准备
   - 在聚宽Notebook执行
   - 命令行执行
   - 代码修改指南
   - 常见问题
   - 进阶用法

3. **QUICK_REFERENCE.md** - 快速参考卡片
   - 最优策略配置
   - 关键参数
   - 常用代码片段
   - 实盘建议

4. **result_report.md** - 详细结果报告
   - 完整测试结果
   - 优化前后对比
   - 风险分析
   - 实施建议

### 💻 代码文件

1. **backtest_code.py** - 优化版回测代码（⭐推荐）
   - 情绪开关优化（涨停≥10/15/20）
   - 缩量条件验证
   - 市值上下限测试
   - 成交率场景测试
   - 执行时间：10-15分钟

2. **backtest_code_full_year.py** - 全年基础回测代码
   - 二板/三板/四板分板位测试
   - 无情绪 vs 有情绪对比
   - 执行时间：5-10分钟

3. **backtest_code_simple.py** - 简化版回测代码
   - 快速验证逻辑
   - 测试2024Q1数据
   - 执行时间：2-3分钟

### 📊 结果文件

1. **notebook_snapshot.ipynb** - Notebook快照
   - 完整执行过程
   - 所有输出结果
   - 可在Jupyter中打开
   - 文件大小：1.0MB

2. **backtest_result.json** - 完整结果JSON
   - Notebook URL
   - Kernel ID
   - Session ID
   - 执行时间
   - 完整输出
   - 文件大小：22KB

---

## 🎯 快速导航

### 我是新手，从哪里开始？

1. 阅读 `README.md` 了解基本情况
2. 阅读 `QUICK_REFERENCE.md` 了解最优配置
3. 打开 `backtest_code.py` 查看代码
4. 按照 `USAGE_GUIDE.md` 执行回测

### 我想快速验证结果

1. 打开 `QUICK_REFERENCE.md`
2. 复制核心配置
3. 在聚宽Notebook中执行 `backtest_code_simple.py`

### 我想修改参数测试

1. 阅读 `USAGE_GUIDE.md` 的"代码修改指南"
2. 参考 `QUICK_REFERENCE.md` 的"常用代码片段"
3. 修改 `backtest_code.py` 中的参数

### 我想查看详细结果

1. 打开 `result_report.md` 查看详细报告
2. 打开 `notebook_snapshot.ipynb` 查看完整执行过程
3. 查看 `backtest_result.json` 了解原始数据

---

## 🔑 核心结果速查

### 最优配置（2024全年）

```
策略：二板 + 情绪≥10 + 缩量条件

交易次数：83次
胜率：87.95%
盈亏比：21.91
累计收益：394.61%
年化收益：407.65%
最大回撤：0.60%
```

### 三板配置（2024全年）

```
策略：三板 + 情绪≥20 + 缩量条件

交易次数：20次
胜率：75.00%
盈亏比：21.99
累计收益：93.99%
年化收益：97.10%
最大回撤：0.50%
```

### 关键参数

| 参数 | 二板推荐值 | 三板推荐值 |
|------|----------|----------|
| 情绪阈值 | ≥10 | ≥20 |
| 缩量条件 | ≤1.875 | ≤1.875 |
| 换手率 | <30% | <30% |
| 成交方式 | 非涨停开盘 | 非涨停开盘 |

---

## 📝 文件用途对照表

| 需求 | 推荐文件 |
|------|---------|
| 了解基本情况 | README.md |
| 学习如何使用 | USAGE_GUIDE.md |
| 快速查阅参数 | QUICK_REFERENCE.md |
| 查看详细结果 | result_report.md |
| 执行优化回测 | backtest_code.py ⭐ |
| 执行基础回测 | backtest_code_full_year.py |
| 快速验证逻辑 | backtest_code_simple.py |
| 查看完整执行 | notebook_snapshot.ipynb |
| 获取原始数据 | backtest_result.json |

---

## 🔗 相关链接

### 聚宽平台

- 官网：https://www.joinquant.com
- Notebook：https://www.joinquant.com/user/21333940833/notebooks/test.ipynb
- API文档：https://www.joinquant.com/help/api
- 社区：https://www.joinquant.com/community

### 本地文件

```
/Users/fengzhi/Downloads/git/testlixingren/docs/234_board_backtest_20240330/
```

---

## ⚠️ 重要提示

1. **所有回测结果均为真实执行**，不是模拟数据
2. **测试时间：2024-01-01 至 2024-12-31**
3. **建议在实盘前进行更多年份的验证**
4. **注意小市值股票的流动性风险**
5. **严格执行止损纪律**

---

## 📞 获取帮助

遇到问题时：

1. 查看 `USAGE_GUIDE.md` 的"常见问题"部分
2. 查看 `result_report.md` 的"风险分析"部分
3. 检查代码注释和输出日志
4. 参考聚宽社区：https://www.joinquant.com/community

---

**创建日期：** 2024-03-30  
**最后更新：** 2024-03-30  
**版本：** v1.0  
**状态：** ✅ 已验证
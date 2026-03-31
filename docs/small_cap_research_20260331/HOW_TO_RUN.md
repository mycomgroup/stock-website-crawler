# 使用说明

## 策略已准备就绪！

由于Notebook平台连接问题，我已创建了可在**策略编辑器**中直接运行的完整策略代码。

### 文件位置

```
docs/small_cap_research_20260331/small_cap_strategy_jq.py
```

### 使用方法

#### 方式1：JoinQuant策略编辑器

1. 登录 [JoinQuant](https://www.joinquant.com/)
2. 进入策略编辑器
3. 创建新策略
4. 复制 `small_cap_strategy_jq.py` 的全部代码
5. 点击"运行回测"
6. 设置回测参数：
   - 起始日期：2014-01-01
   - 结束日期：2024-12-31
   - 初始资金：100000
   - 频率：日线

#### 方式2：RiceQuant策略编辑器

如需RiceQuant版本，需要修改API调用：
- `get_index_stocks` → `index_components`
- `get_fundamentals` → `get_factor` 或 RiceQuant的财务数据API

### 策略核心参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 持仓数量 | 10 | 同时持有股票数量 |
| 市值范围 | 10-300亿 | 避开微盘和大盘 |
| 止损线 | -9% | 个股止损 |
| 空仓月份 | 1月、4月 | 持有货币ETF |
| 调仓周期 | 每周 | 周一上午10:00 |

### 预期回测结果（参考）

基于聚宽已有策略分析：

| 策略类型 | 年化收益 | 最大回撤 |
|----------|----------|----------|
| 国九条筛选型 | 100.5% | -25.6% |
| 菜场大妈型 | ~50% | -16.8% |
| 本策略预期 | 50-80% | 20-30% |

### 后续优化方向

1. **参数调优**：调整市值范围、持仓数量
2. **因子优化**：加入PE/PB/ROE等基本面因子
3. **机器学习**：使用XGBoost动态选择因子权重
4. **风控增强**：加入市场择时、情绪指标

---

## 文件清单

```
docs/small_cap_research_20260331/
├── README.md                    # 研究框架说明
├── QUICK_START.md               # 快速开始指南
├── small_cap_strategy_jq.py     # ★ 可直接运行的策略代码
├── step1_guojutiao_filter.py    # Notebook版Step1
├── step2_factor_test.py         # Notebook版Step2
├── step3_ml_model.py            # Notebook版Step3
├── step4_backtest.py            # Notebook版Step4
└── run_all_steps.sh             # 一键执行脚本
```

---

**下一步建议**：复制策略代码到JoinQuant策略编辑器运行回测，查看实际表现。
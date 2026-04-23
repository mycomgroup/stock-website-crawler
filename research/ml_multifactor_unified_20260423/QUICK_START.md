# 快速开始指南（先整理代码，再跑回测）

## 0) 先回答你的问题

**Q：这个是需要提交回测才能跑吗？**  
**A：是的，当前这套脚本是按 JoinQuant 环境写的，正常方式是通过 `skills/joinquant_notebook/run-strategy.js` 提交到 JoinQuant Notebook 执行。**

**Q：可以先把所有代码整理清楚吗？**  
**A：可以，已先完成代码归档与路径统一，代码集中在 `code/` 下。**

---

## 1) 代码位置

- 快速/完整回测脚本：
  - `code/backtest_scripts/ml_ultra_quick.py`
  - `code/backtest_scripts/ml_walkforward_real.py`
  - `code/backtest_scripts/ml_walkforward_fixed.py`
- 参考策略与教程：
  - `code/reference_strategies/STRATEGY_CODE.md`
  - `code/reference_strategies/41 手把手教你“机器学习-动态多因子选股”(附保姆级教程)/`
  - `code/reference_strategies/92 【机器学习研究】动态多因子选股策略研究.ipynb`

---

## 2) 运行方式（JoinQuant 提交执行）

```bash
cd /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook

export JOINQUANT_USERNAME="13311390323"
export JOINQUANT_PASSWORD="#Ff09173228552"

node run-strategy.js \
  --strategy ../research/ml_multifactor_unified_20260423/code/backtest_scripts/ml_ultra_quick.py \
  --timeout-ms 180000
```

完整回测：

```bash
node run-strategy.js \
  --strategy ../research/ml_multifactor_unified_20260423/code/backtest_scripts/ml_walkforward_real.py \
  --timeout-ms 600000
```

---

## 3) 结果查看

```bash
ls -lt /Users/fengzhi/Downloads/git/testlixingren/output/joinquant-notebook-result-*.json | head -1
cat /Users/fengzhi/Downloads/git/testlixingren/output/joinquant-notebook-result-*.json | jq '.executions[0].textOutput'
```

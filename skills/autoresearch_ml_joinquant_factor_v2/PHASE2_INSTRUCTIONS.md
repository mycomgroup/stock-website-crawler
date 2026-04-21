# Phase 2 训练说明

## 📋 准备工作

✅ 已完成：
1. 合并2026年数据到训练集 → `train_merged_all_with_2026.csv` (1.5GB)
2. 创建Phase 2训练脚本 → `run_phase2.py`

## 🚀 运行Phase 2训练

### 方法1：直接运行（推荐）

```bash
cd /Users/yuping/Downloads/git/stock-website-crawler
python3 skills/autoresearch_ml_joinquant_factor_v2/run_phase2.py
```

**预计时间**: 30-60分钟（取决于机器性能）

### 方法2：后台运行

```bash
cd /Users/yuping/Downloads/git/stock-website-crawler
nohup python3 skills/autoresearch_ml_joinquant_factor_v2/run_phase2.py > phase2_training.log 2>&1 &
```

查看进度：
```bash
tail -f phase2_training.log
```

## 📊 训练配置

- **训练数据**: 2015-2025年 (616,117行)
- **测试数据**: 2026年 (11,869行，13周)
- **Holdout期**: 52周
- **因子数量**: 260个
- **因子家族**: 9个

## 📁 输出文件

训练完成后，会在 `output/phase2/` 目录生成：

1. **oof_predictions_phase2.csv** - OOF预测结果
2. **run_snapshot_phase2.json** - 运行快照（包含因子权重）

## 🔍 训练完成后的分析

训练完成后，运行以下脚本分析Phase 2在2026年的表现：

```bash
python3 skills/autoresearch_ml_joinquant_factor_v2/analyze_phase2_on_2026.py
```

这个脚本会：
1. 加载Phase 2的OOF预测
2. 在2026年数据上计算IC、收益等指标
3. 与Phase 1对比
4. 生成分析报告

## ⏱️ 预期结果

如果Phase 2成功，我们期望看到：

| 指标 | Phase 1 (2015-2023训练) | Phase 2 (2015-2025训练) | 期望变化 |
|------|------------------------|------------------------|---------|
| 2026 IC | ? | ? | ↑ 提升 |
| 2026 IC IR | ? | ? | ↑ 提升 |
| 2026超额收益 | +1.47%/年 | ? | ↑ 提升 |

## 🐛 故障排除

### 问题1：内存不足
```
MemoryError: Unable to allocate array
```

**解决方案**：
- 关闭其他程序释放内存
- 或者减少数据量（只使用2020-2025年数据）

### 问题2：找不到模块
```
ModuleNotFoundError: No module named 'xxx'
```

**解决方案**：
```bash
pip install pandas numpy scipy scikit-learn
```

### 问题3：训练中断
如果训练中断，可以从日志中查看进度，然后重新运行。

## 📝 下一步

Phase 2训练完成后：

1. ✅ 分析Phase 2在2026年的表现
2. ✅ 对比Phase 1 vs Phase 2
3. ✅ 如果Phase 2表现更好，使用Phase 2模型
4. ✅ 如果Phase 2表现不佳，分析原因（过拟合？数据质量？）

---

**创建时间**: 2026-04-20  
**状态**: 准备就绪，可以开始训练

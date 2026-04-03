# 快速开始指南

## 一、环境准备

### 1.1 所需账号

- JoinQuant 账号（手机号: 13311390323）
- 密码: #Ff09173228552

### 1.2 安装依赖

```bash
cd /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook
npm install
```

### 1.3 验证环境

```bash
# 测试登录
node browser/capture-joinquant-session.js --headed
```

---

## 二、运行验证脚本

### 2.1 快速验证（推荐首次运行）

**脚本**: `scripts/ml_ultra_quick.py`  
**特点**: 仅4个因子、100只股票、季度调仓  
**耗时**: 约2-3分钟

```bash
cd /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook

export JOINQUANT_USERNAME="13311390323"
export JOINQUANT_PASSWORD="#Ff09173228552"

node run-strategy.js \
  --strategy ../docs/ml_multifactor_validation_20260401/scripts/ml_ultra_quick.py \
  --timeout-ms 180000
```

### 2.2 完整验证（耗时较长）

**脚本**: `scripts/ml_walkforward_real.py`  
**特点**: 13个因子、全部500只股票、月度调仓  
**耗时**: 约5-10分钟

```bash
node run-strategy.js \
  --strategy ../docs/ml_multifactor_validation_20260401/scripts/ml_walkforward_real.py \
  --timeout-ms 600000
```

---

## 三、查看结果

### 3.1 结果文件位置

```bash
# 查看最新结果
ls -lt /Users/fengzhi/Downloads/git/testlixingren/output/joinquant-notebook-result-*.json | head -1

# 查看具体内容
cat /Users/fengzhi/Downloads/git/testlixingren/output/joinquant-notebook-result-*.json | jq '.executions[0].textOutput'
```

### 3.2 结果解读

成功运行后，会看到类似输出：

```
ML多因子快速验证
==================================================
调仓日期: 12个季度

训练: ['2023-01-03', '2023-04-03']
测试: 2023-07-03 -> 2023-10-09
  逻辑回归: 选股10只, 收益=2.50%
  SVM: 选股10只, 收益=-9.45%
  随机森林: 选股10只, 收益=-0.32%

...

==================================================
【汇总结果】
==================================================
逻辑回归: 累计=57.35%, 胜率=88.9%, 季均=5.35%
SVM: 累计=50.38%, 胜率=66.7%, 季均=5.18%
随机森林: 累计=25.35%, 胜率=66.7%, 季均=2.85%

验证完成!
```

### 3.3 关键指标说明

- **累计收益**: 整个测试期的总收益
- **胜率**: 盈利季度占比
- **季均收益**: 每个季度的平均收益

---

## 四、常见问题

### Q1: Session 过期怎么办？

```bash
# 重新登录
node browser/capture-joinquant-session.js --headed
```

### Q2: 超时怎么办？

```bash
# 增加超时时间
node run-strategy.js --strategy xxx.py --timeout-ms 600000  # 10分钟
```

### Q3: 如何调试？

在脚本中添加更多 print 语句：

```python
print(f"调试: 当前股票数={len(stocks)}")
print(f"调试: 特征维度={X_train.shape}")
```

---

## 五、下一步

1. 查看 `README.md` 了解详细结论
2. 查看 `docs/` 目录下的详细报告
3. 根据结果调整参数重新测试
4. 小资金试跑实盘策略

---

**注意**: 所有测试结果已保存在 `results/` 目录。
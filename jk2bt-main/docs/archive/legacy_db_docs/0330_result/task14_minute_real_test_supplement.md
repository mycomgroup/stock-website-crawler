# Task 14 实际运行测试补充报告

## 测试样本
测试了 3 个代表性分钟策略

## 测试结果

### 94 小资金短线策略.txt
- **说明**: 使用1m数据计算尾盘因子
- **状态**: ✗ 异常
- **可日线运行**: False
- **错误**: attempted relative import beyond top-level package

### 89 2020年效果很好的策略-龙回头策略v3.0.txt
- **说明**: 使用1m过滤涨跌停
- **状态**: ✗ 异常
- **可日线运行**: False
- **错误**: attempted relative import beyond top-level package

### 72 【股指期货】收盘折溢价策略.txt
- **说明**: 使用attribute_history 1m
- **状态**: ✗ 异常
- **可日线运行**: False
- **错误**: attempted relative import beyond top-level package

## 总结
- 成功: 0
- 失败: 3

### 失败原因分析
- 94 小资金短线策略.txt: attempted relative import beyond top-level package
- 89 2020年效果很好的策略-龙回头策略v3.0.txt: attempted relative import beyond top-level package
- 72 【股指期货】收盘折溢价策略.txt: attempted relative import beyond top-level package

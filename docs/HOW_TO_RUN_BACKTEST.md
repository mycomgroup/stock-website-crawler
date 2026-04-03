# 使用指南 - 在 RiceQuant 策略编辑器中运行

## 🎯 目标
在 RiceQuant 策略编辑器中运行完整回测，获取真实的回测结果

---

## 📋 操作步骤

### 步骤 1: 登录 RiceQuant

访问: https://www.ricequant.com/quant

使用你的账号登录：
- 用户名: 13311390323
- 密码: ******

---

### 步骤 2: 创建新策略

1. 点击左侧菜单 **"策略研究"** → **"策略编辑器"**
2. 点击 **"新建策略"**
3. 输入策略名称，例如：`小市值成长股策略_2024`
4. 选择 Python 3 环境

---

### 步骤 3: 复制策略代码

选择你要运行的策略文件，复制全部代码：

#### 策略 1: 小市值成长股策略
```
文件位置: /strategies/Ricequant/migrated/01_small_cap_backtest.py
```

#### 策略 2: 股息率价值策略
```
文件位置: /strategies/Ricequant/migrated/02_dividend_backtest.py
```

#### 策略 3: ETF动量轮动策略
```
文件位置: /strategies/Ricequant/migrated/03_etf_momentum_backtest.py
```

---

### 步骤 4: 设置回测参数

在策略代码底部的 `__config__` 中设置：

```python
__config__ = {
    "base": {
        "start_date": "2024-01-01",  # 开始日期
        "end_date": "2024-12-31",    # 结束日期
        "frequency": "1d",           # 日频
        "accounts": {"stock": 1000000}  # 初始资金100万
    },
    "extra": {
        "log_level": "info",
    },
    "mod": {
        "sys_progress": {
            "enabled": True,
            "show": True,
        }
    }
}
```

---

### 步骤 5: 运行回测

1. 点击页面右上角的 **"运行回测"** 按钮
2. 等待回测完成（通常需要 1-3 分钟）
3. 查看回测结果

---

## 📊 查看回测结果

回测完成后，你将看到以下内容：

### 1. 总体表现
- 总收益率
- 年化收益率
- 最大回撤
- 夏普比率
- 胜率

### 2. 收益曲线
- 策略收益曲线
- 基准收益曲线
- 对比图

### 3. 持仓记录
- 每日持仓明细
- 交易记录
- 盈亏统计

### 4. 风险指标
- 波动率
- 最大连续亏损
- Beta、Alpha 等

---

## 📂 策略文件位置

所有策略文件都在：
```
/Users/fengzhi/Downloads/git/testlixingren/strategies/Ricequant/migrated/
```

推荐使用的策略（适合在编辑器中运行）：
- ✅ `01_small_cap_backtest.py` - 小市值策略
- ✅ `02_dividend_backtest.py` - 股息率策略
- ✅ `03_etf_momentum_backtest.py` - ETF动量策略

---

## 💡 提示

### 如何查看策略代码？

**方式 1: 在终端查看**
```bash
cat /Users/fengzhi/Downloads/git/testlixingren/strategies/Ricequant/migrated/01_small_cap_backtest.py
```

**方式 2: 在编辑器打开**
```bash
code /Users/fengzhi/Downloads/git/testlixingren/strategies/Ricequant/migrated/
```

### 回测参数建议

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| 开始日期 | 2024-01-01 | 近一年数据 |
| 结束日期 | 2024-12-31 | 到最近 |
| 初始资金 | 1000000 | 100万 |
| 频率 | 1d | 日级回测 |
| 基准 | 000300.XSHG | 沪深300 |

---

## 🎯 预期结果

根据策略类型，预期回测结果：

### 小市值成长股策略
- 预期年化收益: 15-30%
- 预期最大回撤: 15-25%
- 适合: 牛市行情

### 股息率价值策略
- 预期年化收益: 8-15%
- 预期最大回撤: 10-20%
- 适合: 震荡市

### ETF动量轮动策略
- 预期年化收益: 10-20%
- 预期最大回撤: 10-15%
- 适合: 趋势行情

---

## ⚠️ 注意事项

1. **首次运行**可能需要等待数据加载
2. **运行时间**取决于策略复杂度和时间范围
3. **失败处理**：
   - 检查语法错误
   - 确认API调用正确
   - 查看日志输出

---

## 📞 需要帮助？

如果在运行过程中遇到问题，可以：
1. 查看 RiceQuant 官方文档
2. 检查策略代码中的错误提示
3. 联系我继续协助

---

**立即开始**: 
1. 打开 https://www.ricequant.com/quant
2. 创建新策略
3. 复制策略代码
4. 运行回测
5. 查看结果！
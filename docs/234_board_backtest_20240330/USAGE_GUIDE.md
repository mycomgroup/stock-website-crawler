# 234板分板位回测 - 使用指南

本文档提供详细的使用指南，帮助你在真实环境中运行回测。

---

## 一、环境准备

### 1.1 聚宽账号

- **注册地址：** https://www.joinquant.com
- **账号要求：** 需要实名认证
- **费用：** Notebook功能免费

### 1.2 本地环境（可选）

如果需要在本地执行，需要安装：

```bash
# Node.js（用于自动化执行）
brew install node

# 依赖包
cd /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook
npm install
```

---

## 二、在聚宽Notebook中执行（推荐）

### 2.1 登录聚宽

1. 打开浏览器
2. 访问：https://www.joinquant.com
3. 输入账号密码登录

### 2.2 创建Notebook

1. 点击顶部菜单"研究"
2. 点击"Notebook"
3. 点击"新建Notebook"
4. 命名为"234_board_backtest"或其他名称

### 2.3 复制代码

**方法1：从本地文件复制**

```bash
# 查看代码
cat /Users/fengzhi/Downloads/git/testlixingren/docs/234_board_backtest_20240330/backtest_code.py
```

复制全部内容。

**方法2：直接打开文件**

用文本编辑器打开：
```
/Users/fengzhi/Downloads/git/testlixingren/docs/234_board_backtest_20240330/backtest_code.py
```

### 2.4 粘贴到Notebook

1. 在Notebook中创建新的cell
2. 选择cell类型为"Code"
3. 粘贴代码
4. 按 `Shift + Enter` 执行

### 2.5 查看结果

执行完成后，会输出：

```
======================================================================
234板分板位回测 - 优化版本
======================================================================

测试1：情绪开关优化（涨停≥15/10）
...

最终结果对比
...
最优配置: two板 | 情绪=10 | 缩量=True
  累计收益: 394.61%
  最大回撤: 0.60%
  胜率: 87.95%

回测完成!
```

---

## 三、使用命令行工具执行

### 3.1 准备工作

**步骤1：创建聚宽Notebook**

1. 登录聚宽
2. 创建Notebook，命名为"test"
3. 复制Notebook URL

URL格式：
```
https://www.joinquant.com/user/notebook?url=/user/YOUR_USER_ID/notebooks/test.ipynb
```

**步骤2：抓取Session**

```bash
cd /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook

# 有头模式（推荐，可以看到浏览器操作）
node browser/capture-joinquant-session.js \
  --notebook-url "https://www.joinquant.com/user/notebook?url=/user/YOUR_USER_ID/notebooks/test.ipynb" \
  --headed
```

执行后会打开浏览器，自动登录并抓取session。

**步骤3：验证Session**

```bash
# 查看session文件
cat data/session.json
```

应该看到类似内容：
```json
{
  "capturedAt": "2024-03-30T...",
  "notebookUrl": "https://www.joinquant.com/user/notebook?url=/user/...",
  "cookies": [...]
}
```

### 3.2 执行回测

```bash
cd /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook

# 执行优化版回测
node run-strategy.js \
  --notebook-url "https://www.joinquant.com/user/notebook?url=/user/YOUR_USER_ID/notebooks/test.ipynb" \
  --strategy ../docs/234_board_backtest_20240330/backtest_code.py \
  --timeout-ms 900000
```

**参数说明：**
- `--notebook-url`：你的Notebook URL
- `--strategy`：回测代码路径
- `--timeout-ms`：超时时间（900000ms = 15分钟）

### 3.3 查看结果

执行完成后，结果保存在：

```bash
# 查看输出目录
ls -lh /Users/fengzhi/Downloads/git/testlixingren/output/

# 最新结果文件
joinquant-notebook-result-TIMESTAMP.json  # 结果JSON
joinquant-notebook-TIMESTAMP.ipynb          # Notebook快照
```

---

## 四、代码修改指南

### 4.1 修改测试时间范围

打开 `backtest_code.py`，找到：

```python
START_DATE = "2024-01-01"
END_DATE = "2024-12-31"
```

修改为你需要的时间范围：

```python
START_DATE = "2023-01-01"  # 开始日期
END_DATE = "2023-12-31"    # 结束日期
```

### 4.2 修改情绪阈值

找到测试配置：

```python
# 二板：放宽情绪阈值
r1 = backtest_board_optimized('two', START_DATE, END_DATE, sentiment_threshold=15)
r2 = backtest_board_optimized('two', START_DATE, END_DATE, sentiment_threshold=10)
```

修改为：

```python
# 测试不同情绪阈值
r1 = backtest_board_optimized('two', START_DATE, END_DATE, sentiment_threshold=5)   # 更宽松
r2 = backtest_board_optimized('two', START_DATE, END_DATE, sentiment_threshold=10)  # 推荐值
r3 = backtest_board_optimized('two', START_DATE, END_DATE, sentiment_threshold=20)  # 更严格
```

### 4.3 修改缩量条件

找到缩量条件：

```python
def check_volume_shrink(stock, date, threshold=1.875):
    """检查缩量条件：昨日量 <= 前日量 * threshold"""
```

修改阈值：

```python
# 更严格的缩量条件
if volume_shrink:
    low_hsl = [s for s in low_hsl if check_volume_shrink(s, date, 1.5)]  # 改为1.5

# 更宽松的缩量条件
if volume_shrink:
    low_hsl = [s for s in low_hsl if check_volume_shrink(s, date, 2.0)]  # 改为2.0
```

### 4.4 添加新的测试场景

在代码末尾添加：

```python
# 测试新场景
r9 = backtest_board_optimized(
    'two',                          # 板位
    START_DATE,                     # 开始日期
    END_DATE,                       # 结束日期
    sentiment_threshold=10,         # 情绪阈值
    volume_shrink=True,             # 缩量条件
    cap_range=(5, 30),              # 市值范围（亿）
    fill_rate=None                  # 成交率
)
```

---

## 五、常见问题

### Q1: 执行时间太长怎么办？

**问题：** 代码执行超过15分钟还没完成

**解决：**
1. 缩小测试范围：
   ```python
   START_DATE = "2024-01-01"
   END_DATE = "2024-06-30"  # 只测试半年
   ```

2. 减少测试场景：
   ```python
   # 只测试最优配置
   r1 = backtest_board_optimized('two', START_DATE, END_DATE, sentiment_threshold=10)
   ```

3. 增加超时时间：
   ```bash
   node run-strategy.js --timeout-ms 1800000  # 30分钟
   ```

### Q2: Session过期怎么办？

**问题：** 提示"请登录"或"Session过期"

**解决：**
```bash
# 重新抓取session
node browser/capture-joinquant-session.js \
  --notebook-url "YOUR_NOTEBOOK_URL" \
  --headed
```

### Q3: 代码执行报错怎么办？

**常见错误：**

1. **内存不足**
   ```
   MemoryError: Unable to allocate...
   ```
   
   解决：减少股票数量
   ```python
   # 将all_stocks[:500]改为[:300]
   df = get_price(all_stocks[:300], ...)
   ```

2. **数据不存在**
   ```
   KeyError: '...'
   ```
   
   解决：检查日期是否为交易日
   ```python
   # 检查日期
   trade_days = get_trade_days(start_date, end_date)
   ```

3. **API限流**
   ```
   请求频率过快...
   ```
   
   解决：添加延时
   ```python
   import time
   time.sleep(0.5)  # 延时0.5秒
   ```

### Q4: 如何保存结果到文件？

**方法1：保存到聚宽服务器**

```python
import json

result = {
    "total_return": 394.61,
    "win_rate": 87.95,
    # ... 其他数据
}

with open('backtest_result.json', 'w') as f:
    json.dump(result, f, indent=2)
```

**方法2：保存到本地**

```python
result_file = "/Users/fengzhi/Downloads/git/testlixingren/output/my_result.json"
with open(result_file, 'w') as f:
    json.dump(result, f, indent=2)
```

### Q5: 如何对比不同时间的结果？

**方法：**

```python
# 测试不同年份
results = {}

for year in [2022, 2023, 2024]:
    start = f"{year}-01-01"
    end = f"{year}-12-31"
    
    r = backtest_board_optimized('two', start, end, sentiment_threshold=10)
    if r:
        results[year] = r

# 对比结果
for year, r in results.items():
    print(f"{year}: 收益={r['total_return']:.2f}%, 胜率={r['win_rate']:.2f}%")
```

---

## 六、进阶用法

### 6.1 批量测试多个策略

创建批量测试脚本：

```python
# batch_test.py
test_configs = [
    {'board': 'two', 'sentiment': 5, 'volume_shrink': False},
    {'board': 'two', 'sentiment': 10, 'volume_shrink': False},
    {'board': 'two', 'sentiment': 10, 'volume_shrink': True},
    {'board': 'two', 'sentiment': 15, 'volume_shrink': True},
    {'board': 'three', 'sentiment': 20, 'volume_shrink': True},
]

results = []
for config in test_configs:
    r = backtest_board_optimized(
        config['board'],
        START_DATE,
        END_DATE,
        sentiment_threshold=config['sentiment'],
        volume_shrink=config['volume_shrink']
    )
    if r:
        results.append(r)

# 找出最优配置
best = max(results, key=lambda x: x['total_return'])
print(f"最优配置: {best['config']}")
```

### 6.2 参数调优

使用网格搜索：

```python
# 参数范围
sentiment_range = [5, 10, 15, 20]
volume_shrink_options = [True, False]

best_result = None
best_config = None

for sentiment in sentiment_range:
    for volume_shrink in volume_shrink_options:
        r = backtest_board_optimized(
            'two',
            START_DATE,
            END_DATE,
            sentiment_threshold=sentiment,
            volume_shrink=volume_shrink
        )
        
        if r:
            if best_result is None or r['total_return'] > best_result['total_return']:
                best_result = r
                best_config = {
                    'sentiment': sentiment,
                    'volume_shrink': volume_shrink
                }

print(f"最优配置: {best_config}")
print(f"累计收益: {best_result['total_return']:.2f}%")
```

### 6.3 滚动回测

模拟真实交易：

```python
# 滚动回测：训练期12个月，测试期3个月
train_months = 12
test_months = 3

all_results = []

for year in [2022, 2023, 2024]:
    for month in [1, 4, 7, 10]:
        # 训练期
        train_start = f"{year}-{month:02d}-01"
        train_end = f"{year + (month + train_months - 1) // 12}-{(month + train_months - 1) % 12 + 1:02d}-01"
        
        # 测试期
        test_start = train_end
        test_end = f"{year + (month + train_months + test_months - 1) // 12}-{(month + train_months + test_months - 1) % 12 + 1:02d}-01"
        
        # 在训练期找最优参数（简化示例）
        # ... 参数优化逻辑
        
        # 在测试期验证
        r = backtest_board_optimized('two', test_start, test_end, sentiment_threshold=10)
        if r:
            all_results.append(r)

# 统计平均表现
avg_return = np.mean([r['total_return'] for r in all_results])
avg_win_rate = np.mean([r['win_rate'] for r in all_results])

print(f"平均收益: {avg_return:.2f}%")
print(f"平均胜率: {avg_win_rate:.2f}%")
```

---

## 七、结果验证

### 7.1 检查代码正确性

**验证步骤：**

1. **检查选股逻辑**
   ```python
   # 单独测试某一天
   date = '2024-01-02'
   # ... 完整选股逻辑
   print(f"选出的股票: {stock_list}")
   ```

2. **检查买卖价格**
   ```python
   # 打印买卖价格
   print(f"买入价: {buy_price:.2f}")
   print(f"卖出价: {sell_price:.2f}")
   print(f"收益: {profit_pct:.2f}%")
   ```

3. **检查统计逻辑**
   ```python
   # 手动计算验证
   total_trades = len(results)
   wins = len([r for r in results if r['profit'] > 0])
   win_rate = wins / total_trades * 100
   print(f"手动计算的胜率: {win_rate:.2f}%")
   ```

### 7.2 对比聚宽回测结果

如果需要精确回测，建议在聚宽策略编辑器中运行：

1. 创建新策略
2. 复制选股逻辑
3. 设置回测参数：
   - 开始日期：2024-01-01
   - 结束日期：2024-12-31
   - 初始资金：100000
   - 频率：日线

4. 运行回测，对比结果

---

## 八、生产环境部署

### 8.1 实盘建议

**仓位管理：**
- 单票上限：300-500万
- 总仓位：根据情绪动态调整
- 情绪好（涨停≥20）：可满仓
- 情绪差（涨停<10）：空仓

**风险控制：**
- 止损：单票亏损-5%止损
- 止盈：次日卖出，不贪恋
- 回撤控制：连续亏损3次减半仓位

**执行纪律：**
- 严格按信号执行
- 不追涨杀跌
- 不主观判断

### 8.2 监控指标

**每日监控：**
1. 市场涨停家数（情绪指标）
2. 持仓股票表现
3. 策略累计收益
4. 最大回撤

**每周回顾：**
1. 交易胜率
2. 平均盈亏比
3. 策略容量
4. 滑点影响

---

## 九、技术支持

### 9.1 文档资源

- 本地文档：`/Users/fengzhi/Downloads/git/testlixingren/docs/234_board_backtest_20240330/`
- 聚宽文档：https://www.joinquant.com/help
- API文档：https://www.joinquant.com/help/api

### 9.2 问题反馈

如有问题，请：
1. 查看本文档FAQ部分
2. 查看 `README.md` 和 `result_report.md`
3. 检查代码注释和输出日志

---

**最后更新：** 2024-03-30  
**版本：** v1.0
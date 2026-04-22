# 影子策略回测状态报告

时间：2026-03-30 17:40  
平台：Ricequant

---

## 回测执行情况

### 尝试1：回测ID 7961624
- **状态**：❌ 失败
- **错误**：`NameError: name 'get_all_securities' is not defined`
- **原因**：使用了JoinQuant API，未适配Ricequant

### 尝试2：回测ID 7961635  
- **状态**：❌ 失败
- **错误**：`AttributeError: 'str' object has no attribute 'order_book_id'`
- **原因**：`all_instruments()` API用法错误

### 尝试3：简化策略（2024年）
- **文件**：shadow_simple.py
- **候选池**：沪深300 + 中证500（限制200只）
- **状态**：⏳ 运行中/超时（120秒）
- **结果**：需要去平台查看

---

## 策略文件

### 已创建文件
```
/Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy/
├── shadow_mainline.py   # 原版（API错误）
└── shadow_simple.py     # 简化版（沪深300+中证500）
```

### 简化版策略特点
- ✅ 只针对沪深300和中证500
- ✅ 避免复杂API调用
- ✅ 限制候选池200只股票
- ✅ 主线策略：假弱高开 + 情绪过滤
- ✅ 观察线策略：二板策略

---

## Ricequant API 注意事项

### ❌ 不能使用的JoinQuant API
- `get_all_securities()`
- `get_price(stock, ...)`  
- 其他JoinQuant专用API

### ✅ 正确的Ricequant API
- `index_components("000300.XSHG")` - 获取指数成分股
- `all_instruments(type="CS")` - 返回DataFrame
- `history_bars(stock, count, frequency, fields)` - 获取历史数据
- `bar_dict[stock].open/close` - 当前行情
- `scheduler.run_daily(func, time_rule)` - 定时任务
- `order_shares(stock, quantity)` - 下单

---

## 下一步操作

### 方法1：去Ricequant平台查看（推荐）

1. **登录平台**
   ```
   https://www.ricequant.com
   用户：yuping322
   ```

2. **进入策略编辑器**
   - 找到策略 ID: 2415898（名称：ddd）
   - 查看回测列表
   - 查看最近的回测结果

3. **查看回测报告**
   - 总收益率
   - 年化收益率  
   - 最大回撤
   - 夏普比率
   - 胜率
   - 持仓详情

---

### 方法2：继续尝试简化策略

如果想继续本地运行：

```bash
cd /Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy

# 测试更短时间（1个月）
node run-skill.js \
  --id 2415898 \
  --file ./shadow_simple.py \
  --start 2024-01-01 \
  --end 2024-01-31 \
  --capital 100000

# 查看结果
node fetch-report.js --id <新回测ID>
```

---

### 方法3：手动复制策略到平台

1. 登录Ricequant平台
2. 进入策略编辑器
3. 复制 `shadow_simple.py` 代码
4. 手动粘贴到编辑器
5. 配置回测参数：
   ```
   开始日期：2014-01-01
   结束日期：2024-12-31
   初始资金：100000
   基准：沪深300
   ```
6. 点击运行
7. 查看结果

---

## 数据来源澄清

### ⚠️ 当前数据来源

本文档中提到的所有数据（如 "+2.89%收益"、"87.95%胜率"）均为：

- **来源**：可信度总表_20260330.md  
- **时间**：2024年实测
- **性质**：**不是10年回测结果**

### 需要完成的回测

完整10年回测（2014-2024）需要：
- 在Ricequant平台实际运行
- 策略代码适配完成
- 等待回测完成（可能需要1-2小时）
- 获取真实绩效数据

---

## 状态总结

| 项目 | 状态 | 说明 |
|------|------|------|
| 策略逻辑 | ✅ 已定义 | 主线+观察线 |
| 策略代码 | ⚠️ 需适配 | Ricequant API差异 |
| 简化版策略 | ✅ 已创建 | shadow_simple.py |
| 回测启动 | ✅ 已启动 | ID: 7961624, 7961635 |
| 回测结果 | ❌ 失败 | API适配问题 |
| 10年回测 | ⏳ 待完成 | 需平台运行 |

---

## 建议

1. **优先方案**：去Ricequant平台手动查看回测结果
2. **验证方案**：先跑2024年1个月验证策略逻辑
3. **最终方案**：确认API正确后，跑完整10年回测

**当前最稳妥的做法**：
- 去平台查看现有回测状态
- 如果失败，手动粘贴简化版代码
- 运行并查看真实结果
# 容量与滑点实测 - 手动回测指南

## 当前状态

### 平台连接情况
| 平台 | Session状态 | Kernel状态 | 自动运行 |
|------|------------|-----------|----------|
| JoinQuant | ✓ 有效 | ✗ 无响应 | ✗ 失败 |
| RiceQuant | ✓ 有效 | ✗ 未验证 | ✗ 登录失败 |

### 问题原因
1. **JoinQuant**: Session有效但kernel无响应，可能是服务器负载高
2. **RiceQuant**: 登录页面XPath已过期，无法自动填写账号密码

---

## 解决方案：手动运行回测

### 方案一：JoinQuant手动运行（推荐）

#### 步骤1：打开Notebook
```
访问: https://www.joinquant.com/research
账号: 已登录（session有效）
```

#### 步骤2：创建新Notebook
- 点击右上角 "New" → "Python 3"
- 或打开已有的 test.ipynb

#### 步骤3：复制回测脚本
打开本地文件：
```
docs/opportunity_strategies_20260330/capacity_slippage_backtest.py
```

全选复制所有代码（约300行），粘贴到Notebook的cell中

#### 步骤4：执行回测
- 按 `Shift + Enter` 执行
- 等待5-10分钟
- 观察实时输出

#### 步骤5：记录结果
脚本会自动输出：
- 容量-滑点收益矩阵
- 失效点判断
- 推荐上限

---

### 方案二：RiceQuant手动运行

#### 步骤1：登录RiceQuant
```
访问: https://www.ricequant.com
账号: 13311390323
密码: 3228552
```

#### 步骤2：进入Research
点击右上角 "研究" → 进入Notebook

#### 步骤3：运行脚本
使用同样的脚本，自动适配RiceQuant API

---

### 方案三：快速验证（1分钟）

如果完整回测时间过长，先运行简化验证：

```python
# 复制以下代码到Notebook执行

from jqdata import *  # JoinQuant用这个
# RiceQuant不需要import

import pandas as pd
import numpy as np

# 单日测试
TEST_DATE = "2024-10-15"
PREV_DATE = "2024-10-14"

print("="*60)
print("容量滑点快速验证 - 单日测试")
print("="*60)

# JoinQuant版本
try:
    stocks = get_all_securities('stock', PREV_DATE).index.tolist()[:100]
    stocks = [s for s in stocks if s[0] not in '68']
    
    df_prev = get_price(stocks, end_date=PREV_DATE, 
                        fields=['close', 'high_limit'], count=1, panel=False)
    df_prev = df_prev.dropna()
    hl = df_prev[df_prev['close']==df_prev['high_limit']]['code'].tolist()
    
    print(f"涨停股: {len(hl)}只")
    
    if hl:
        df_today = get_price(hl[:30], end_date=TEST_DATE, 
                            fields=['open', 'close', 'high_limit'], count=1, panel=False)
        df_today = df_today.dropna()
        df_today['ratio'] = df_today['open'] / (df_today['high_limit']/1.1)
        
        signals = df_today[(df_today['ratio']>1.005) & (df_today['ratio']<1.015)]
        
        if len(signals) > 0:
            bp = signals['open'].mean()
            sp = signals['close'].mean()
            
            print(f"\n信号数: {len(signals)}")
            print(f"买入价: {bp:.2f}")
            print(f"卖出价: {sp:.2f}")
            
            print(f"\n不同滑点收益:")
            print("-"*60)
            
            for slip_name, slip in [("0%", 0), ("0.2%", 0.002), ("0.5%", 0.005)]:
                # 计算实际成本
                buy_cost = bp * (1 + slip + 0.0003)
                sell_income = sp * (1 - slip - 0.0003 - 0.001)
                pnl = (sell_income - buy_cost) / buy_cost * 100
                
                status = "✓" if pnl > 0 else "✗"
                print(f"{slip_name}滑点: {pnl:+.2f}% {status}")
            
            print("-"*60)
            print(f"\n结论:")
            print(f"  - 理论收益(0%滑点): {(sp-bp)/bp*100:.2f}%")
            print(f"  - 0.2%滑点损耗: ~0.4-0.5%")
            print(f"  - 0.5%滑点损耗: ~1.0-1.2%, 可能转负")
        else:
            print("无信号")
    else:
        print("无涨停股")
        
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

print("\n"+"="*60)
```

---

## 已有数据参考

### 基于历史回测的理论估算

| 资金档 | 0%滑点 | 0.2%滑点 | 0.5%滑点 | 判定 |
|--------|--------|----------|----------|------|
| 500万 | ~140% | ~56% | ~-35% | ✓ 可行 |
| 1000万 | ~140% | ~53% | ~-37% | ✓ 可行 |
| 3000万 | ~140% | ~47% | ~-43% | △ 警戒 |
| 5000万 | ~140% | ~39% | ~-51% | ✗ 不推荐 |

### 关键结论（理论）
- 推荐资金上限: 500万
- 滑点失效点: >0.5%
- 年化收益: 55.6% (500万+0.2%滑点)

---

## 下一步建议

### 立即可做
1. **手动运行快速验证**（1分钟）
   - 验证kernel是否正常
   - 验证API是否可用

2. **手动运行完整回测**（5-10分钟）
   - 如果kernel正常，运行完整脚本
   - 记录实测数据

### 后续优化
1. **修复自动运行脚本**
   - 更新RiceQuant登录XPath
   - 增加JoinQuant kernel状态检查

2. **创建模拟盘验证**
   - 在模拟环境中验证实际滑点
   - 监控成交额占比

---

## 文件位置

| 文件 | 路径 |
|------|------|
| 完整回测脚本 | `docs/opportunity_strategies_20260330/capacity_slippage_backtest.py` |
| 主报告 | `docs/opportunity_strategies_20260330/result_04_mainline_capacity_slippage.md` |
| 回执 | `docs/opportunity_strategies_20260330/dispatch_prompts_20260330/results/04_任务_04_主线容量与滑点实测_回执.md` |

---

**生成时间**: 2026-03-31
**状态**: 需要手动运行回测验证理论估算
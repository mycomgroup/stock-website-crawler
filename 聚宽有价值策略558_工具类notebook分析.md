# 数据/回测/工程优化类 Notebook 分析

## 1. 概述

这一类别包含 **5 个** 实用工具类 notebook，主要解决量化研究中的工程化问题：
- 回测框架搭建
- 数据过滤优化（ST/退市/停牌/新股）
- 因子库获取
- 业绩预告工具
- Barra 风险因子归因

---

## 2. Notebook 详情

### 2.1 `44 研究 借助JqData搭建简易回测框架.ipynb`

**核心功能**：自定义轻量级回测框架

**主要类/模块**：
- `Context`：账户管理（资金、持仓、交易历史）
- `Order`：下单交易（买入/卖出）
- `Trade`：回测执行与评估

**评估指标**：
- 基准收益、策略收益
- 年化收益率
- 最大回撤
- 夏普比率
- 盈亏比、胜率
- 交易次数
- Beta、Alpha

**代码示例**：
```python
class Context:
    def __init__(self):
        self.cash = 100000  # 默认初始资金
        self.base = '000300.XSHG'  # 默认参考基准
        self.position = {}  # 持仓

class Order:
    def buy(self, security, price, count): ...
    def sell(self, security, price, count): ...

class Trade:
    def trade(self, func, show=True, log=False): ...
    def get_result(self): ...
```

**实测建议**：在最近数据上测试框架的基本功能是否正常

---

### 2.2 `100 研究 回测提速十倍,过滤ST,退市,停牌,新股优化方法.ipynb`

**核心功能**：快速过滤 ST、停牌、新股、科创板股票

**优化要点**：
- `get_current_data` 全A股遍历，1个字段约 **100ms**
- 每增加一个字段增加约 **30ms**
- 新股过滤约 **30ms-40ms**
- 整个函数调用平均 **160ms**

**核心函数**：
```python
def filter_st_paused_new(stock_list, days, context):
    df = get_all_securities(types=['stock'], date=context.current_dt)
    kcb = list(df[df.index.str.startswith('688')].index.unique())  # 排除科创板
    start_date = (context.current_dt - timedelta(days=days)).date()
    df_new_stock = df[df['start_date'] > start_date]  # 新股过滤
    stock_list = list(set(stock_list).difference(set(df_new_stock.index)).difference(set(kcb)))
    
    curr_data = get_current_data()
    stock_list = [stock for stock in stock_list if not curr_data[stock].is_st]  # 非ST
    stock_list = [stock for stock in stock_list if not curr_data[stock].paused]  # 非停牌
    stock_list = [curr_data[stock].code for stock in stock_list if '退' not in curr_data[stock].name]  # 排除退市
    return stock_list
```

**优化建议**：
- 层层过滤，缩小股票池，减少 API 调用次数
- 使用 `get_current_data` 过滤，[无需再 name 字段过滤](https://www.joinquant.com/view/community/detail/27592)

---

### 2.3 `68 业绩预告研究环境小工具--已更新.ipynb`

**核心功能**：业绩预告数据查询与分析工具

**待验证**：需要查看具体实现内容

---

### 2.4 `78 获取聚宽因子库和国盛因子的研究.ipynb`

**核心功能**：
1. 获取聚宽因子库所有因子
2. 获取国盛因子

**因子分类统计**（聚宽）：
- `quality`：71 个
- `basics`：37 个
- `emotion`：36 个
- `momentum`：34 个
- `style`：30 个
- `technical`：16 个
- `pershare`：15 个
- `risk`：12 个
- `growth`：9 个

**总计**：约 260+ 个因子

**使用示例**：
```python
from jqfactor import get_all_factors
all_factors = get_all_factors()
all_factors['category'].value_counts()
```

**获取国盛因子**：需要进一步查看实现

---

### 2.5 `100 barra风险因子收益归因-全市场-修改版.ipynb`

**核心功能**：Barra 风险因子模型收益归因

**待验证**：需要查看具体实现内容

---

## 3. 实测计划

### 3.1 测试目标

| 序号 | Notebook | 测试内容 | 预期结果 |
|------|----------|----------|----------|
| 1 | 44 简易回测框架 | 基本框架初始化 | 正常初始化 |
| 2 | 100 过滤优化 | 过滤函数调用 | 160ms 左右 |
| 3 | 78 因子库获取 | 因子查询 | 返回因子列表 |
| 4 | 100 Barra归因 | 因子收益归因 | 全市场归因结果 |

### 3.2 测试环境

- 聚宽研究环境
- 测试时间范围：2024-01-01 ~ 2025-03-27（最近数据）

### 3.3 测试方法

1. 连接到聚宽研究环境
2. 运行核心代码单元
3. 记录输出结果

---

## 4. 后续工作

- [ ] 根据实测结果优化文档
- [ ] 提取更多核心代码片段
- [ ] 与策略类 notebook 联动测试
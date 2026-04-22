# 二板接力策略OOS验证系统

**版本**: V1.0  
**创建时间**: 2026-04-02  
**状态**: 可运行  

---

## 一、系统概述

本系统是二板接力策略的样本外（OOS）验证自动化系统，集成了数据管理、衰退检测、自动化验证和报告生成四大核心模块，实现对策略的持续监控和预警。

### 核心功能

- **数据管理**：行情、情绪、广度数据的存储、查询和质量检查
- **衰退检测**：四级预警机制，自动检测策略衰减
- **自动化验证**：日/周/月三级验证频率，自动计算指标
- **报告生成**：自动生成日报、周报、月报

---

## 二、系统架构

```
secondboard_oos_system/
├── core/                      # 核心模块
│   └── decay_detector.py      # 衰退检测
├── data/                      # 数据管理
│   └── data_manager.py        # 数据管理器
├── validation/                # 验证引擎
│   └── validation_engine.py   # 验证引擎
├── reports/                   # 报告生成
│   └── report_generator.py    # 报告生成器
├── utils/                     # 工具模块
├── main.py                    # 主入口
└── README.md                  # 本文档
```

---

## 三、快速开始

### 3.1 安装依赖

```bash
pip install pandas numpy scipy
```

### 3.2 运行测试

```bash
cd strategies/secondboard_oos_system
python main.py --mode test --db test_oos.db
```

### 3.3 运行验证

**日频验证**：
```bash
python main.py --mode daily --date 2024-01-01
```

**周频验证**：
```bash
python main.py --mode weekly --date 2024-01-05
```

**月频验证**：
```bash
python main.py --mode monthly --date 2024-01-31
```

---

## 四、核心模块说明

### 4.1 数据管理模块 (DataManager)

**功能**：
- 数据库初始化（SQLite）
- 行情数据存储与查询
- 情绪数据存储与查询
- 广度数据存储与查询
- 交易记录存储与查询
- 数据质量检查

**示例**：
```python
from data.data_manager import DataManager

dm = DataManager('secondboard_oos.db')

# 保存交易记录
record = {
    'signal_date': '2024-01-01',
    'signal_stock_code': '000001.SZ',
    'signal_price': 10.0,
    'execution_date': '2024-01-01',
    'execution_price': 10.1,
    'execution_volume': 1000,
    'sell_date': '2024-01-02',
    'sell_price': 10.5,
    'sell_reason': '高位回落',
    'profit_loss_pct': 0.04
}
dm.save_trade_record(record)

# 查询交易记录
trades = dm.query_trade_records('2024-01-01', '2024-01-31')

# 检查数据质量
quality = dm.check_data_completeness('price', '2024-01-01')

dm.close()
```

### 4.2 衰退检测模块 (DecayDetector)

**功能**：
- 四级衰退定义（轻度、中度、重度、失效）
- 四级预警判定（绿色、黄色、橙色、红色）
- 多指标综合评估
- 统计检验（t检验）
- 趋势检测
- 应对措施生成

**示例**：
```python
from core.decay_detector import DecayDetector

is_baseline = {
    'annual_return': 394,
    'win_rate': 87.95,
    'max_drawdown': 0.60,
    'sharpe_ratio': 20,
    'profit_loss_ratio': 21.91
}

detector = DecayDetector(is_baseline)

current_metrics = {
    'annual_return': 350,
    'win_rate': 85,
    'max_drawdown': 3.0,
    'sharpe_ratio': 18,
    'profit_loss_ratio': 20
}

decay_result = detector.detect_decay(current_metrics, duration_days=30)

print(f"预警级别: {decay_result['alert_level']}")
print(f"衰退程度: {decay_result['decay_degree']}")
print(f"触发指标: {decay_result['triggered_metrics']}")
```

### 4.3 验证引擎 (ValidationEngine)

**功能**：
- 日频验证（单日验证）
- 周频验证（近20日滚动窗口）
- 月频验证（近60日滚动窗口）
- 指标自动计算（收益、风险、质量）
- 验证结果存储

**示例**：
```python
from validation.validation_engine import ValidationEngine

engine = ValidationEngine('secondboard_oos.db')

# 日频验证
daily_result = engine.run_daily_validation('2024-01-01')

# 周频验证
weekly_result = engine.run_weekly_validation('2024-01-05')

# 月频验证
monthly_result = engine.run_monthly_validation('2024-01-31')

print(f"月频预警: {monthly_result['alert_level']}")
print(f"年化收益: {monthly_result['annual_return']:.2f}%")

engine.close()
```

### 4.4 报告生成模块 (ReportGenerator)

**功能**：
- 日报生成
- 周报生成
- 月报生成
- Markdown格式输出

**示例**：
```python
from reports.report_generator import ReportGenerator
import pandas as pd

generator = ReportGenerator()

validation_result = {
    'annual_return': 350,
    'cumulative_return': 15,
    'win_rate': 85,
    'profit_loss_ratio': 20,
    'max_drawdown': 3.0,
    'sharpe_ratio': 18,
    'alert_level': 'green',
    'triggered_metrics': []
}

# 生成月报
report = generator.generate_monthly_report(
    '2024-01-31',
    pd.DataFrame(),
    validation_result
)

print(report)
```

---

## 五、集成使用

### 5.1 完整集成示例

```python
from main import OOSValidationSystem

# 初始化系统
system = OOSValidationSystem('my_oos.db')

# 添加交易记录
trade = {
    'signal_date': '2024-01-01',
    'signal_stock_code': '000001.SZ',
    'signal_price': 10.0,
    'execution_date': '2024-01-01',
    'execution_price': 10.1,
    'execution_volume': 1000,
    'sell_date': '2024-01-02',
    'sell_price': 10.5,
    'sell_reason': '高位回落',
    'profit_loss_pct': 0.04
}
system.add_trade_record(trade)

# 执行验证
result = system.run_daily_validation('2024-01-01')

# 输出结果
print(f"预警级别: {result['alert_level']}")
print(f"年化收益: {result['annual_return']:.2f}%")
print(f"胜率: {result['win_rate']:.2f}%")

# 关闭系统
system.close()
```

### 5.2 定时验证脚本

```python
from main import OOSValidationSystem
from datetime import datetime

def run_scheduled_validation():
    """定时验证任务"""
    system = OOSValidationSystem('secondboard_oos.db')
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 日频验证（每日）
    system.run_daily_validation(today)
    
    # 周频验证（周五）
    if datetime.now().weekday() == 4:
        system.run_weekly_validation(today)
    
    # 月频验证（月末）
    if is_month_end(today):
        system.run_monthly_validation(today)
    
    system.close()

def is_month_end(date_str):
    """判断是否月末"""
    date = datetime.strptime(date_str, '%Y-%m-%d')
    next_month = date.replace(day=28) + timedelta(days=4)
    return date.day == (next_month - timedelta(days=next_month.day)).day
```

---

## 六、数据结构

### 6.1 数据库表结构

**daily_price（行情数据）**：
- stock_code: 股票代码
- trade_date: 交易日期
- open, high, low, close: OHLC价格
- volume, amount: 成交量、成交额
- pct_change: 涨跌幅
- turnover_rate: 换手率

**trade_records（交易记录）**：
- signal_date: 信号日期
- signal_stock_code: 信号股票代码
- signal_price: 信号价格
- execution_date: 执行日期
- execution_price: 执行价格
- execution_volume: 执行数量
- sell_date: 卖出日期
- sell_price: 卖出价格
- sell_reason: 卖出原因
- profit_loss_pct: 盈亏比例

**validation_results（验证结果）**：
- validation_date: 验证日期
- validation_type: 验证类型（daily/weekly/monthly）
- window_type: 窗口类型（single_day/rolling_20d/rolling_60d）
- annual_return: 年化收益
- cumulative_return: 累计收益
- win_rate: 胜率
- profit_loss_ratio: 盈亏比
- max_drawdown: 最大回撤
- sharpe_ratio: 夏普比率
- alert_level: 预警级别
- triggered_metrics: 触发指标

---

## 七、验证指标

### 7.1 收益指标

| 指标 | 计算方法 | IS基准 | 达标标准 |
|------|---------|--------|---------|
| 年化收益率 | (1+累计收益)^(365/天数)-1 | 394% | >200% |
| 累计收益率 | (1+收益).prod()-1 | 500% (3年) | 月度>5% |

### 7.2 风险指标

| 指标 | 计算方法 | IS基准 | 达标标准 |
|------|---------|--------|---------|
| 最大回撤 | max((峰值-谷值)/峰值) | 0.60% | <10% |
| 波动率 | std(收益)*sqrt(252) | 2% | <3% |

### 7.3 质量指标

| 指标 | 计算方法 | IS基准 | 达标标准 |
|------|---------|--------|---------|
| 胜率 | 盈利次数/总次数 | 87.95% | >80% |
| 盈亏比 | 平均盈利/平均亏损 | 21.91 | >15 |

### 7.4 风险调整收益

| 指标 | 计算方法 | IS基准 | 达标标准 |
|------|---------|--------|---------|
| 夏普比率 | (年化收益-无风险利率)/波动率 | 20+ | >3.0 |
| 卡玛比率 | 年化收益/最大回撤 | 30+ | >10 |

---

## 八、预警机制

### 8.1 四级预警体系

| 级别 | 颜色 | 触发条件 | 应对措施 |
|------|------|---------|---------|
| 正常 | 绿色 | 所有指标达标 | 正常执行 |
| 观察 | 黄色 | 个别指标观察范围，持续≥2周 | 加强监控 |
| 警告 | 橙色 | 多个指标警告范围，持续≥1个月 | 降仓50% |
| 降级 | 红色 | 关键指标失效或收益显著为负 | 暂停策略 |

### 8.2 衰退定义

| 级别 | 定义 | 表现下降幅度 |
|------|------|------------|
| 轻度衰退 | 表现略有下降 | 10-20% |
| 中度衰退 | 表现明显下降 | 20-40% |
| 重度衰退 | 表现严重下降 | >40% |
| 失效 | 策略失效 | 显著为负（p<0.05） |

---

## 九、注意事项

### 9.1 数据要求

- 交易记录需包含完整的买入和卖出信息
- 盈亏比例(profit_loss_pct)为必需字段
- 建议每日更新交易记录

### 9.2 验证频率

- 日频验证：每日收盘后执行
- 周频验证：每周五收盘后执行
- 月频验证：每月末收盘后执行

### 9.3 预警响应

- 黄色预警：持续观察，准备预案
- 橙色预警：立即降仓，深度分析
- 红色预警：暂停策略，全面复盘

---

## 十、后续优化

### 10.1 待开发功能

- [ ] 分钟级验证（可选）
- [ ] 多策略对比验证
- [ ] 市场环境适应性评估
- [ ] Web界面监控仪表盘
- [ ] 实时数据更新接口
- [ ] 多渠道通知系统（Email、短信、电话）

### 10.2 参数优化

- 验证窗口长度优化（近20日、近60日）
- 预警阈值调整（降低误报率）
- 衰退检测方法组合优化

---

## 十一、技术支持

**开发者**: AI Assistant  
**创建时间**: 2026-04-02  
**版本**: V1.0  
**状态**: 可运行  

**相关文档**：
- [任务06完成总结](../../docs/secondboard_engineering_20260401/task06_outputs/README.md)
- [OOS验证框架设计](../../docs/secondboard_engineering_20260401/task06_outputs/01_oos_validation_framework.md)
- [衰退检测机制设计](../../docs/secondboard_engineering_20260401/task06_outputs/02_decay_detection_mechanism.md)

---

**使用建议**：

1. 首次使用请运行测试模式：`python main.py --mode test`
2. 定期检查数据质量，确保数据完整性
3. 关注月频验证的衰退检测结果
4. 如触发橙色或红色预警，立即启动人工审核流程
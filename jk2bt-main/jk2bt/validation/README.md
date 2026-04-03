# jk2bt 数据验证模块

验证本地 AkShare 数据与 JoinQuant 平台数据的一致性。

## 快速开始

### 1. 生成 JoinQuant 采集脚本

```bash
cd /Users/yuping/Downloads/git/jk2bt-main
python -m jk2bt.validation --generate-scripts
```

这将在 `validation_results/` 目录下生成:
- `jq_collect_valuation.py` - 估值数据采集脚本
- `jq_collect_trade_status.py` - 交易状态采集脚本

### 2. 在 JoinQuant Notebook 中执行脚本

1. 打开 JoinQuant Notebook
2. 复制生成的脚本内容
3. 执行脚本
4. 将输出结果保存为 JSON 文件:
   - `jq_valuation_YYYY-MM-DD.json`
   - `jq_trade_status_YYYY-MM-DD.json`

### 3. 运行验证

```bash
# 使用默认配置
python -m jk2bt.validation

# 使用配置文件
python -m jk2bt.validation --config validation_config.yaml

# 指定参数
python -m jk2bt.validation --stocks 600519.XSHG,000858.XSHE --start 2024-01-01 --end 2024-03-31
```

## 模块说明

```
jk2bt/validation/
├── __init__.py          # 模块入口
├── config.py            # 配置管理
├── data_collector.py    # 数据采集器
├── comparison_engine.py # 对比引擎
├── validator.py         # 验证执行器
├── report_generator.py  # 报告生成器
└── __main__.py          # 命令行入口
```

## API 使用

```python
from jk2bt.validation import DataValidator, ValidationConfig

# 创建配置
config = ValidationConfig(
    stocks=["600519.XSHG", "000858.XSHE"],
    start_date="2024-01-01",
    end_date="2024-03-31",
    data_types=["valuation", "trade_status"],
)

# 创建验证器
validator = DataValidator(config)

# 生成 JQ 采集脚本
validator.generate_jq_collector_scripts("validation_results")

# 运行验证（需要先获取 JQ 数据）
report = validator.run_full_validation()

# 保存报告
report.save_json("validation_result.json")
```

## 数据类型

### 估值数据 (valuation)
- PE/PB/PS 等估值指标
- 市值/流通市值
- 股息率

### 交易状态数据 (trade_status)
- 涨停价/跌停价
- ST 状态
- 停牌状态

### 因子数据 (factors)
- 动量因子
- 波动率因子
- 技术分析因子

## 容差配置

默认容差:
| 字段 | 容差 |
|------|------|
| PE/PB/PS/市值 | 1% |
| 涨跌停价 | 0.01 元 |
| ST/停牌状态 | 精确匹配 |
| 因子 | 5% |

## 输出

- `validation_report_*.md` - Markdown 报告
- `validation_diff_*.csv` - 差异详情
- `validation_result.json` - JSON 结果
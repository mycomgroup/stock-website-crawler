# Task 16 Result

## 修改文件
- `jqdata_akshare_backtrader_utility/runtime_resource_pack.py` (新增)
- `jqdata_akshare_backtrader_utility/runtime_io.py` (修改)
- `jqdata_akshare_backtrader_utility/jq_strategy_runner.py` (修改)
- `tests/test_runtime_resource_pack.py` (新增)

## 完成内容

### 1. 创建 RuntimeResourcePack 模块
实现了完整的资源管理功能：
- 策略级别的资源目录隔离
- 资源类型分类（输入/输出）
- 智能路径映射和资源类型推断
- 资源打包和清理功能

### 2. 增强 runtime_io.py
新增功能：
- `set_strategy_name()` - 设置策略名称，启用资源隔离
- `get_current_strategy_name()` - 获取当前策略名称
- `get_resource_pack()` - 获取当前资源包实例
- 智能读写路径映射，自动识别资源类型

### 3. 集成到策略运行器
`jq_strategy_runner.py` 集成资源管理：
- 运行策略时自动设置策略名称
- 启用策略资源隔离
- 运行结束后输出资源摘要

## 资源目录方案

```
runtime_data/
  ├── strategy_name_1/
  │   ├── input/              # 输入资源（只读或预置）
  │   │   ├── config/         # 配置文件 (JSON/YAML/TXT)
  │   │   ├── models/         # 模型文件 (PKL/H5/PTH)
  │   │   ├── data/           # 数据文件 (CSV/JSON/PKL)
  │   │   └── params/         # 参数文件
  │   └── output/             # 输出资源（运行时生成）
  │       ├── logs/           # 日志文件
  │       ├── trades/         # 交易记录
  │       ├── research/       # 研究产物
  │       └── signals/        # 信号记录
  ├── strategy_name_2/
  └── ...
```

### 资源类型映射
| 文件扩展名/路径关键词 | 资源类型 | 目录 |
|----------------------|---------|------|
| .pkl, .h5, .pth, .model | models | input/models/ |
| .json, .yaml, .ini (含config/param) | config | input/config/ |
| .csv, .json, .pkl (含train/test) | data | input/data/ |
| 含 trade, signal, result | trades | output/trades/ |
| .log (不含 trade/signal) | logs | output/logs/ |

## 验证方式

### 单元测试
```bash
.venv/bin/python -m pytest tests/test_runtime_resource_pack.py -v
```

测试覆盖：
- 资源包创建和目录结构
- 读写输入/输出资源
- 策略资源隔离
- 路径安全验证
- 批量运行场景
- 机器学习策略资源场景

### 真实策略验证
在真实 ML 策略中验证（如 `jkcode/jkcode/49 干货贴《机器学习5折保形回归》.py`）：
```python
# 策略中读取训练数据
df1 = pd.read_csv(BytesIO(read_file('train_conformal_base.csv')))
df2 = pd.read_csv(BytesIO(read_file('test_conformal_base.csv')))
```

通过 `set_strategy_name()` 后，文件自动路由到策略专属目录。

## 使用示例

### 基本使用
```python
from jqdata_akshare_backtrader_utility.runtime_io import (
    set_strategy_name, read_file, write_file, get_resource_pack
)

# 设置策略名称，启用资源隔离
set_strategy_name("my_ml_strategy")

# 写入模型文件 -> input/models/
write_file("trained_model.pkl", model_bytes)

# 写入交易日志 -> output/trades/
write_file("trades.csv", trade_log)

# 读取训练数据
data = read_file("train_data.csv")

# 查看资源摘要
pack = get_resource_pack()
print(pack.get_resource_summary())
```

### 运行策略
```python
from jqdata_akshare_backtrader_utility.jq_strategy_runner import run_jq_strategy

result = run_jq_strategy(
    strategy_file="my_strategy.txt",
    start_date="2020-01-01",
    end_date="2023-12-31",
    enable_resource_pack=True,  # 启用资源隔离
)

# 获取资源包
pack = result["resource_pack"]
```

## 已知边界

1. **编码限制**: 文本文件默认使用 UTF-8 编码
2. **路径安全**: 不允许绝对路径和上级目录引用 (`..`)
3. **并发安全**: 使用线程锁保护全局状态，但多进程场景需要额外处理
4. **资源清理**: 手动调用 `clear_output_resources()` 或 `clear_all_resources()`

## 后续优化建议

1. 添加资源打包/解包功能，支持策略迁移
2. 实现资源版本管理
3. 添加资源大小限制和清理策略
4. 支持远程资源同步（如 S3）
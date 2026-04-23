# RF7 主仓正式版项目（项目级）

本目录已升级为**项目级实现**，不是仅有研究计划。

## 范围（冻结）
- PB10 主池 + PB20 次池
- RFScore 必须严格等于 7（不允许降级到 >=6）
- 四档持仓
- 硬过滤
- 行业上限
- 候选不足留现金
- 研究/监控/生产一致性校验

## 代码结构
- `project/config.py`: 冻结规则配置（Universe + 四档权重）
- `project/selector.py`: PB 主次池 + RF7 + 硬过滤 + 可交易筛选
- `project/allocator.py`: 四档持仓 + 行业上限 + 留现金
- `project/pipeline.py`: 一体化执行入口
- `project/validator.py`: 研究/监控/生产一致性对账
- `project/cli.py`: 命令行运行入口
- `tests/test_rf7_pipeline.py`: 核心约束单元测试

## 快速运行
```bash
python jk2bt-main/strategies/rfscore7_main_portfolio_research/project/cli.py \
  --input jk2bt-main/strategies/rfscore7_main_portfolio_research/examples/universe_sample.csv \
  --selected-out /tmp/rf7_selected.csv \
  --allocation-out /tmp/rf7_allocation.csv
```

## 开发原则
本目录只服务 RF7 正式版主题；新增逻辑必须经过一致性验证，不可绕开 RFScore=7 门槛。

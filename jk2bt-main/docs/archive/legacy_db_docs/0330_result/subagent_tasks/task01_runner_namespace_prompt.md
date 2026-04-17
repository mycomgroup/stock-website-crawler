# 任务 1：Runner 命名空间纠偏

## 任务目标

修复 `txt` 策略运行器中的全局命名空间绑定错误，并增强策略文本加载的编码兼容性。

## 负责范围

- `jqdata_akshare_backtrader_utility/jq_strategy_runner.py`
- 如确有必要，可补充与 runner 直接耦合的测试文件

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 任务结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task01_runner_namespace_result.md`

## 给子 Agent 的提示词

你负责修复 `txt` 策略运行器中的命名空间绑定问题。请直接实现，不要只做分析。

具体要求：

- 确保 `load_jq_strategy()` 暴露给策略代码的 API 优先绑定到真正的 JQ 风格兼容实现，而不是内部简化版或错误签名版本。
- 重点检查并修正：
  - `get_price`
  - `get_current_data`
  - `get_all_trade_days`
  - `get_extras`
  - `get_billboard_list`
- 为策略文本读取增加编码回退，至少支持：
  - `utf-8`
  - `gbk`
  - `gb2312`
  - `latin-1`
- 加载失败时要抛出清晰异常，不要静默返回 `None`。
- 不要改变策略作者的调用方式。
- 不要做大范围重构，不要改与 runner 无关的模块。

实现完成后，请补最小测试，至少覆盖：

- UTF-8 文本策略可加载
- GBK 文本策略可加载
- `get_price(count=..., frequency=..., panel=False)` 不会因为绑定错函数直接报签名错误

## 任务验证

至少完成以下验证：

```bash
python3 -m pytest -q tests/test_jq_runner.py
```

如果你新增了更细的测试，也请一起跑并写入结果。

## 任务成功总结模板

请在结果文档中使用下面结构：

```md
# Task 01 Result

## 修改文件
- ...

## 完成内容
- ...

## 验证命令
```bash
...
```

## 验证结果
- ...

## 已知边界
- ...
```

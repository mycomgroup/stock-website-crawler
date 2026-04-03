# 数据对齐子 Agent 任务包

本目录包含 10 个可并行分发的子任务文档，专门用于完成 JoinQuant 文档与当前实现之间的严格数据对齐工作。

参考资料：

- 原始文档目录：
  - https://github.com/mycomgroup/stock-website-crawler/tree/main/skills/joinquant_nookbook/joinquant_doc/doc
- 当前严格对照清单：
  - `/Users/yuping/Downloads/git/jk2bt-main/docs/strict_data_api_comparison.md`
- 原始拆解任务：
  - `/Users/yuping/Downloads/git/jk2bt-main/docs/data_api_tasks.md`

使用约定：

- 每个任务一个独立文件，可直接复制给一个子 agent。
- 每个任务文档都包含：
  - 任务目标
  - 负责范围
  - 建议写入目录
  - 给子 Agent 的提示词
  - 任务验证
  - 任务成功总结模板
- 所有子 agent 都应遵守：
  - 不要回退其他人的改动
  - 不要做大范围重构
  - 只在自己负责的范围内修改
  - 如果发现别的 agent 已经改了公共入口，优先兼容，不要强行覆盖
  - 完成后写清楚修改文件、验证结果、已知边界

任务列表：

- `task01_company_info_alignment_prompt.md`
- `task02_shareholder_alignment_prompt.md`
- `task03_dividend_alignment_prompt.md`
- `task04_share_change_alignment_prompt.md`
- `task05_unlock_alignment_prompt.md`
- `task06_conversion_bond_alignment_prompt.md`
- `task07_option_alignment_prompt.md`
- `task08_index_components_alignment_prompt.md`
- `task09_industry_sw_alignment_prompt.md`
- `task10_macro_alignment_prompt.md`

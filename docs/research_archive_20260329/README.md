# Research Archive 2026-03-29

这个目录用于集中归档仓库里的研究文档、实验脚本、回顾脚本，避免它们继续散落在根目录和技能目录里。

归档原则：

- 保留基础功能入口不动
- 把明显属于调研/实验/复盘的文件移入 `docs`
- 尽量按来源目录分层，方便回溯

目录说明：

- `root/`
  - 原来散落在仓库根目录的研究文档与实验脚本
- `skills_joinquant_nookbook/`
  - 原 `skills/joinquant_nookbook/` 里的 RFScore / ML / 研究型 notebook 脚本
- `skills_joinquant_strategy/`
  - 原 `skills/joinquant_strategy/` 里的 RFScore 仓位规则实验脚本

未迁移的文件：

- `skills/joinquant_nookbook/.env`
- `skills/joinquant_nookbook/load-env.js`
- `skills/joinquant_nookbook/main.js`
- `skills/joinquant_nookbook/package*.json`
- `skills/joinquant_nookbook/paths.js`
- `skills/joinquant_nookbook/run-skill.js`
- `skills/joinquant_strategy/.env`
- `skills/joinquant_strategy/debug-env.js`
- `skills/joinquant_strategy/fetch-report.js`
- `skills/joinquant_strategy/list-strategies.js`
- `skills/joinquant_strategy/load-env.js`
- `skills/joinquant_strategy/package*.json`
- `skills/joinquant_strategy/paths.js`
- `skills/joinquant_strategy/run-skill.js`

这些文件保留在原位置，是为了不影响现有技能基础功能。

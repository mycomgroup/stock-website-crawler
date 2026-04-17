# Task 12: API 缺失矩阵分析报告

**生成时间**: 2026-03-31 14:31:54

## 1. 执行摘要

- **扫描策略数**: 428
- **发现 API 数**: 46

### API 支持状态分布

- **已完整支持**: 39
- **部分支持**: 2
- **仅占位支持**: 2
- **完全未支持**: 3

## 2. API 详细分析

### 完全未支持的 API

| API | 命中策略数 | 优先级 | 代表策略样本 | 备注 |
|-----|-----------|--------|-------------|------|
| get_fundamentals_continuously | 3 | 🔥 HIGH | 36 最简强者恒强策略.txt, 49 修改成一创版本.txt, 56 一创PEG+EBIT+turnover_volatility.txt | 完全未支持但有策略使用，需实现 |
| get_locked_shares | 2 | ⚡ MEDIUM | 12 用子账户模拟多策略分仓.txt, 47 多策略整合大E小十年百倍（年化64%回撤28%）.txt | 未支持，有少量策略使用 |
| get_fund_info | 1 | ⚡ MEDIUM | 84 多大规模的基金收益最好？偏股基金规模研究.txt | 未支持，有少量策略使用 |

### 仅占位支持的 API

| API | 命中策略数 | 优先级 | 代表策略样本 | 备注 |
|-----|-----------|--------|-------------|------|
| get_ticks | 14 | 🔥 HIGH | 02 龙头底分型战法-两年23倍.txt, 03 多策略融合-80倍.txt, 04 集合竞价摸奖策略1.0-致敬2022.txt | 仅占位但策略实际使用，需实现 |
| get_contract_multiplier | 1 | ⚪ LOW | 36 致敬市场(6) ，指数期货贴水.txt | 仅占位，使用较少 |

### 部分支持的 API

| API | 命中策略数 | 优先级 | 代表策略样本 | 备注 |
|-----|-----------|--------|-------------|------|
| get_billboard_list | 5 | ⚡ MEDIUM | 01 龙回头3.0回测速度优化版.txt, 26 这个可入得了你们法眼.txt, 85 价值策略重开，再次向Jqz1226致敬.txt | 部分支持且中等频使用 |
| get_beta | 1 | ⚪ LOW | 23 大盘择时，逻辑简单.txt | 部分支持但低频使用 |

### 已完整支持的 API

| API | 命中策略数 | 代表策略样本 |
|-----|-----------|-------------|
| set_option | 420 | 01 7年40倍模拟超过两年年化高回撤低.txt, 01 wywy1995大侠的小市值AI因子选股 5组参数50股.txt, 01 一颗耀眼的星—【回顾2】小市值成长股策略更新—改.txt |
| set_benchmark | 379 | 01 wywy1995大侠的小市值AI因子选股 5组参数50股.txt, 01 一颗耀眼的星—【回顾2】小市值成长股策略更新—改.txt, 02 7年40倍绩优低价超跌缩量小盘 扩容到50只.txt |
| run_daily | 347 | 01 7年40倍模拟超过两年年化高回撤低.txt, 01 wywy1995大侠的小市值AI因子选股 5组参数50股.txt, 01 一颗耀眼的星—【回顾2】小市值成长股策略更新—改.txt |
| set_order_cost | 326 | 01 wywy1995大侠的小市值AI因子选股 5组参数50股.txt, 02 7年40倍绩优低价超跌缩量小盘 扩容到50只.txt, 02 ETF动量轮动RSRS择时-魔改3小优化.txt |
| order_target_value | 324 | 01 7年40倍模拟超过两年年化高回撤低.txt, 01 wywy1995大侠的小市值AI因子选股 5组参数50股.txt, 01 一颗耀眼的星—【回顾2】小市值成长股策略更新—改.txt |
| get_current_data | 315 | 01 7年40倍模拟超过两年年化高回撤低.txt, 01 wywy1995大侠的小市值AI因子选股 5组参数50股.txt, 01 一颗耀眼的星—【回顾2】小市值成长股策略更新—改.txt |
| query | 242 | 01 7年40倍模拟超过两年年化高回撤低.txt, 01 wywy1995大侠的小市值AI因子选股 5组参数50股.txt, 01 一颗耀眼的星—【回顾2】小市值成长股策略更新—改.txt |
| set_slippage | 233 | 01 wywy1995大侠的小市值AI因子选股 5组参数50股.txt, 02 7年40倍绩优低价超跌缩量小盘 扩容到50只.txt, 02 ETF动量轮动RSRS择时-魔改3小优化.txt |
| get_all_securities | 211 | 01 wywy1995大侠的小市值AI因子选股 5组参数50股.txt, 01 一颗耀眼的星—【回顾2】小市值成长股策略更新—改.txt, 01 首板低开策略.txt |
| get_security_info | 207 | 01 7年40倍模拟超过两年年化高回撤低.txt, 01 wywy1995大侠的小市值AI因子选股 5组参数50股.txt, 01 首板低开策略.txt |
| get_price | 202 | 01 wywy1995大侠的小市值AI因子选股 5组参数50股.txt, 01 一颗耀眼的星—【回顾2】小市值成长股策略更新—改.txt, 01 首板低开策略.txt |
| get_fundamentals | 201 | 01 7年40倍模拟超过两年年化高回撤低.txt, 01 wywy1995大侠的小市值AI因子选股 5组参数50股.txt, 01 一颗耀眼的星—【回顾2】小市值成长股策略更新—改.txt |
| order_target | 167 | 01 龙回头3.0回测速度优化版.txt, 02 龙头底分型战法-两年23倍.txt, 03 5年15倍的收益，年化79.93%，可实盘，拿走不谢！.txt |
| attribute_history | 164 | 01 7年40倍模拟超过两年年化高回撤低.txt, 01 龙回头3.0回测速度优化版.txt, 02 7年40倍绩优低价超跌缩量小盘 扩容到50只.txt |
| history | 158 | 01 7年40倍模拟超过两年年化高回撤低.txt, 01 wywy1995大侠的小市值AI因子选股 5组参数50股.txt, 01 一颗耀眼的星—【回顾2】小市值成长股策略更新—改.txt |
| order_value | 130 | 01 7年40倍模拟超过两年年化高回撤低.txt, 02 连板龙头策略.txt, 02 龙头底分型战法-两年23倍.txt |
| get_index_stocks | 112 | 04 红利搬砖_测试版.txt, 04 红利搬砖，年化29%.txt, 04 苦咖啡-默默赚钱系列-改.txt |
| run_monthly | 100 | 03 5年15倍的收益，年化79.93%，可实盘，拿走不谢！.txt, 03 一个简单而持续稳定的懒人超额收益策略.txt, 04 红利搬砖_测试版.txt |
| run_weekly | 82 | 01 wywy1995大侠的小市值AI因子选股 5组参数50股.txt, 01 一颗耀眼的星—【回顾2】小市值成长股策略更新—改.txt, 02 7年40倍绩优低价超跌缩量小盘 扩容到50只.txt |
| get_factor_values | 71 | 01 wywy1995大侠的小市值AI因子选股 5组参数50股.txt, 01 一颗耀眼的星—【回顾2】小市值成长股策略更新—改.txt, 02 连板龙头策略.txt |
| get_bars | 62 | 01 龙回头3.0回测速度优化版.txt, 04 集合竞价摸奖策略1.0-致敬2022.txt, 11 缠论交易策略.txt |
| log | 51 | 01 7年40倍模拟超过两年年化高回撤低.txt, 02 7年40倍绩优低价超跌缩量小盘 扩容到50只.txt, 03 高评分ETF策略之核心资产轮动.txt |
| record | 44 | 02 连板龙头策略.txt, 03 高评分ETF策略之核心资产轮动.txt, 04 高股息低市盈率高增长的价投策略.txt |
| get_all_trade_days | 41 | 01 首板低开策略.txt, 02 连板龙头策略.txt, 04 首板低开策略.txt |
| get_industry_stocks | 36 | 05 四大搅屎棍策略.txt, 08 因子分析 营业利润TTM.txt, 10 10年52倍，年化59%，全新因子方法超稳定.txt |
| get_extras | 32 | 01 首板低开策略.txt, 02 连板龙头策略.txt, 04 首板低开策略.txt |
| order | 30 | 11 缠论交易策略.txt, 17 基金跟随策略，19年年化60%.txt, 20 人人可躺平16年3400%.txt |
| send_message | 25 | 06 87.5%胜率之分歧反包二板.txt, 10 多因子宽基ETF择时轮动改进版-高收益大资金低回撤.txt, 14 FOF养老成长基金-v2.0.txt |
| read_file | 23 | 05 随机森林策略，低换手率，年化近50%.txt, 19 【复现】高频价量相关性，意想不到的选股因子.txt, 20 【复现】因子择时？？？.txt |
| get_hl_stock | 15 | 01 首板低开策略.txt, 02 连板龙头策略.txt, 04 首板低开策略.txt |
| standardlize | 12 | 10 10年52倍，年化59%，全新因子方法超稳定.txt, 15 10年52倍，年化59%，全新因子方法超稳定.txt, 28 XGBoost模型多因子策略分享.txt |
| write_file | 11 | 34 韶华研究之十八 首板低开201系列.txt, 46 大盘股也能穿越牛熊市.txt, 53 TSmall-100, 微盘三正.txt |
| get_continue_count_df | 8 | 01 首板低开策略.txt, 02 连板龙头策略.txt, 04 首板低开策略.txt |
| get_future_contracts | 8 | 27 中证500指增+CTA，胜率52%盈亏比1.9。不输顶尖私募.txt, 32 北向资金A股择时策略（5年16倍）.txt, 35 超稳+翻倍，贝塔值只有0.048的期指策略.txt |
| neutralize | 7 | 08 因子分析 营业利润TTM.txt, 28 XGBoost模型多因子策略分享.txt, 39 大资金强基本面优质股组合策略 收益1217% 无小市值因子.txt |
| get_relative_position_df | 5 | 01 首板低开策略.txt, 04 首板低开策略.txt, 16 集合竞价三合一，今年收益1067%，年化198%.txt |
| get_index_weights | 3 | 03 一个简单而持续稳定的懒人超额收益策略.txt, 11 一个简单而持续稳定的懒人超额收益策略.txt, 31 跟着基金报团！！！174%  回撤  7.33%.txt |
| winsorize | 3 | 08 因子分析 营业利润TTM.txt, 39 大资金强基本面优质股组合策略 收益1217% 无小市值因子.txt, 67 三因子策略年化21%简单多因子策略框架.txt |
| g | 1 | field_map_output.txt |

## 3. Top 20 最值得优先补的 API

| 排名 | API | 命中策略数 | 当前状态 | 优先级 | 建议行动 |
|------|-----|-----------|----------|--------|----------|
| 1 | get_fundamentals_continuously | 3 | not_supported | HIGH | 需要完整实现 |
| 2 | get_ticks | 14 | placeholder | HIGH | 需要实现具体功能 |
| 3 | get_locked_shares | 2 | not_supported | MEDIUM | 需要完整实现 |
| 4 | get_fund_info | 1 | not_supported | MEDIUM | 需要完整实现 |
| 5 | get_billboard_list | 5 | partial_support | MEDIUM | 需要完善功能 |

## 4. 策略 API 使用示例

| 策略文件 | API 数量 | 主要 API |
|----------|----------|----------|
| 64 大小外择时小市值3.0.txt | 21 | set_option, set_benchmark, run_daily, set_order_cost, order_target_value |
| 12 用子账户模拟多策略分仓.txt | 19 | set_option, set_benchmark, run_daily, set_order_cost, order_target_value |
| 47 多策略整合大E小十年百倍（年化64%回撤28%）.txt | 19 | set_option, set_benchmark, run_daily, set_order_cost, order_target_value |
| 56 双人工智能AI配合，样本外夏普3.9.txt | 19 | set_option, set_benchmark, run_daily, set_order_cost, order_target_value |
| 23 大盘择时，逻辑简单.txt | 18 | set_option, set_benchmark, run_daily, set_order_cost, get_current_data |
| 28 XGBoost模型多因子策略分享.txt | 18 | set_option, set_benchmark, order_target_value, get_current_data, query |
| 71 （乱改一版）股票加“钱粮”ETF组合.txt | 18 | set_option, set_benchmark, run_daily, set_order_cost, order_target_value |
| 83 大小外择时小市值.txt | 18 | set_option, set_benchmark, run_daily, set_order_cost, order_target_value |
| 03 5年15倍的收益，年化79.93%，可实盘，拿走不谢！.txt | 17 | set_option, set_benchmark, run_daily, set_order_cost, order_target_value |
| 13 5年15倍的收益，年化79.93%，可实盘策略，拿走不谢！.txt | 17 | set_option, set_benchmark, run_daily, set_order_cost, order_target_value |

## 5. 验证方式

- 本报告基于 AST 解析和正则表达式扫描策略文件
- API 支持状态基于代码库实际实现判断
- 优先级计算综合考虑命中策略数和支持状态
- 已抽查若干 API 与策略样本的一致性

## 6. 已知边界

- 只扫描了策略目录下的 txt 文件
- AST 解析可能遗漏某些特殊的 API 调用形式
- API 支持状态判断基于已知列表，可能遗漏新增实现
- 优先级建议仅供参考，实际优先级需结合业务需求

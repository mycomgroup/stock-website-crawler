# 任务优先级清单（P0 / P1 / P2）

说明：本清单合并了 `119` 个迁移任务与 `27` 个旧 `py` 修复任务。

## 概览

- 迁移任务总数：`119`
- 旧 `py` 修复任务：`27`
- `P0` 迁移任务：`71`
- `P1` 迁移任务：`18`
- `P2` 迁移任务：`30`
- `P0` 旧 `py` 修复：`27`

## ✅ 修复进度（2026-04-05）

- R001~R027 全部 27 个旧 `py` 修复任务已完成（`get_fundamentals` 缺失 / `df` 未赋值 / 变量引用错误）
- P1 全部 18 个任务已完成：
  - 16 个文件已有完整实现，通过静态检查
  - 6 个文件修复了 `bare except` / `.last` 属性 / 多字段 `history_bars` 问题
  - 所有 18 个文件通过 Python AST 语法检查 + API 合规检查
- P2 全部 30 个任务已完成：
  - 17 个文件已有完整实现，通过静态检查
  - 13 个文件修复了 `bare except` / `.last` 属性问题
  - 所有 30 个文件通过 Python AST 语法检查 + API 合规检查

## P0

先处理确定性的硬阻塞：残留聚宽语法、云端 `error_exit`、明显逻辑错误，以及审计里已标红的旧 `py`。

- `T001` `rq_18 国庆节献礼：实例说明白马股攻防转换策略.txt`
  当前文件：`rq_18 国庆节献礼：实例说明白马股攻防转换策略.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T003` `rq_19 机器学习线性回归小市值.txt`
  当前文件：`rq_19 机器学习线性回归小市值.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T004` `rq_20 【复现】因子择时？？？.txt`
  当前文件：`rq_20 【复现】因子择时？？？.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T006` `rq_20 小市值高频交易法有赚就好 2年3.86%低回撤.txt`
  当前文件：`rq_20 小市值高频交易法有赚就好 2年3.86%低回撤.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T008` `rq_21 利用宏观经济数据的中长线策略深度研究.txt`
  当前文件：`rq_21 利用宏观经济数据的中长线策略深度研究.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T011` `rq_22 截止到21年12月依然有效的小市值适配因子.txt`
  当前文件：`rq_22 截止到21年12月依然有效的小市值适配因子.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T012` `rq_22 菜场大妈高质低价法策略.txt`
  当前文件：`rq_22 菜场大妈高质低价法策略.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T013` `rq_23 wywy1995大神机器学习策略年化提升版.txt`
  当前文件：`rq_23 wywy1995大神机器学习策略年化提升版.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T014` `rq_23 大盘择时，逻辑简单.txt`
  当前文件：`rq_23 大盘择时，逻辑简单.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T015` `rq_24 低AH溢价选股.txt`
  当前文件：`rq_24 低AH溢价选股.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T016` `rq_24 多因子线性回归组合策略.txt`
  当前文件：`rq_24 多因子线性回归组合策略.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T017` `rq_24 大容量低回撤价值投资-排除小市值因子.txt`
  当前文件：`rq_24 大容量低回撤价值投资-排除小市值因子.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T018` `rq_25 ROE-PB模型的优化.txt`
  当前文件：`rq_25 ROE-PB模型的优化.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T020` `rq_26 【深度解析 六】高股息率-低PEG-低股价-市值序列模型.txt`
  当前文件：`rq_26 【深度解析 六】高股息率-低PEG-低股价-市值序列模型.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T021` `rq_26 稳定高回报周期股策略2.txt`
  当前文件：`rq_26 稳定高回报周期股策略2.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T022` `rq_26 近几年一直有效的股票BOLL择时策略.txt`
  当前文件：`rq_26 近几年一直有效的股票BOLL择时策略.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T027` `rq_28 XGBoost模型多因子策略分享.txt`
  当前文件：`rq_28 XGBoost模型多因子策略分享.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T028` `rq_28 韶华研究之十九，一致性用在微盘控制回撤.txt`
  当前文件：`rq_28 韶华研究之十九，一致性用在微盘控制回撤.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T029` `rq_29 北上资金（北向资金港资外资）因子分析与策略分享.txt`
  当前文件：`rq_29 北上资金（北向资金港资外资）因子分析与策略分享.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T031` `rq_30 价值成长轮动策略.txt`
  当前文件：`rq_30 价值成长轮动策略.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T032` `rq_30 挖掘特色估值体系因子，把握投资机会，年化150%+.txt`
  当前文件：`rq_30 挖掘特色估值体系因子，把握投资机会，年化150%+.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T033` `rq_30 错杀反弹，掌握人性规律，开启投资新纪元.txt`
  当前文件：`rq_30 错杀反弹，掌握人性规律，开启投资新纪元.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T035` `rq_31 RSRS择时+货币基金--6年8倍行业周期股策略.txt`
  当前文件：`rq_31 RSRS择时+货币基金--6年8倍行业周期股策略.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T036` `rq_31 蛇皮走位小市值策略V1.0.txt`
  当前文件：`rq_31 蛇皮走位小市值策略V1.0.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T037` `rq_31 跟着基金报团！！！174%  回撤  7.33%.txt`
  当前文件：`rq_31 跟着基金报团！！！174%  回撤  7.33%.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T039` `rq_32 北向资金A股择时策略（5年16倍）.txt`
  当前文件：`rq_32 北向资金A股择时策略（5年16倍）.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T041` `rq_32 非线性关系市值（不是小市值）4只绩优股组合.txt`
  当前文件：`rq_32 非线性关系市值（不是小市值）4只绩优股组合.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T042` `rq_33 alpha191短周期价量特征因子选股，年化46.77.txt`
  当前文件：`rq_33 alpha191短周期价量特征因子选股，年化46.77.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T043` `rq_33 回馈社区顺便搞积分《一个完整的机器学习pipeline》.txt`
  当前文件：`rq_33 回馈社区顺便搞积分《一个完整的机器学习pipeline》.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T044` `rq_33 最适合上班族的策略-神奇公式策略.txt`
  当前文件：`rq_33 最适合上班族的策略-神奇公式策略.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T046` `rq_34 【回撤二波2.0】透过一次过拟合的机器学习摸底策略的收益上限.txt`
  当前文件：`rq_34 【回撤二波2.0】透过一次过拟合的机器学习摸底策略的收益上限.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T047` `rq_34 十年回测 年化103.32% 最大回撤23.89%.txt`
  当前文件：`rq_34 十年回测 年化103.32% 最大回撤23.89%.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T049` `rq_35 【菜场大妈】股息率小市值策略,10年206倍,5年10.8倍.txt`
  当前文件：`rq_35 【菜场大妈】股息率小市值策略,10年206倍,5年10.8倍.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T050` `rq_35 小市值市场轮动版 5年12倍.txt`
  当前文件：`rq_35 小市值市场轮动版 5年12倍.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T051` `rq_35 自适应量化终极算法2.0 （全新升级）.txt`
  当前文件：`rq_35 自适应量化终极算法2.0 （全新升级）.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T053` `rq_46 【深度解析 四】聚宽三因子基本面周线模型策略.txt`
  当前文件：`rq_46 【深度解析 四】聚宽三因子基本面周线模型策略.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T054` `rq_47 别人恐惧我贪婪——重视大盘择时.txt`
  当前文件：`rq_47 别人恐惧我贪婪——重视大盘择时.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T055` `rq_47 多策略整合大E小十年百倍（年化64%回撤28%）.txt`
  当前文件：`rq_47 多策略整合大E小十年百倍（年化64%回撤28%）.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T057` `rq_47 随机森林量价多因子选股短线交易机器学习.txt`
  当前文件：`rq_47 随机森林量价多因子选股短线交易机器学习.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T058` `rq_47 高收益低回撤的小市值策略.txt`
  当前文件：`rq_47 高收益低回撤的小市值策略.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T059` `rq_48 一种宏观数据的中长线策略，年化15%，最大回撤9%.txt`
  当前文件：`rq_48 一种宏观数据的中长线策略，年化15%，最大回撤9%.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T060` `rq_48 低代码迁移成本的实盘方案：jqtrade+one quant.txt`
  当前文件：`rq_48 低代码迁移成本的实盘方案：jqtrade+one quant.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T062` `rq_48 投资回报率ROIC中等市值.txt`
  当前文件：`rq_48 投资回报率ROIC中等市值.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`from_jqdata | jq_fundamentals_syntax | jq_indicator_orm | jq_valuation_orm `
- `T063` `rq_48 研究 聚宽高手文章300篇列表.txt`
  当前文件：`rq_48 研究 聚宽高手文章300篇列表.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`from_jqdata | jq_fundamentals_syntax | jq_indicator_orm | jq_valuation_orm `
- `T065` `rq_49 【漂亮50 2.0止损版本】为了降低回撤，加入择时止损模块.txt`
  当前文件：`rq_49 【漂亮50 2.0止损版本】为了降低回撤，加入择时止损模块.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`from_jqdata | jq_fundamentals_syntax | jq_indicator_orm | jq_valuation_orm `
- `T066` `rq_49 修改成一创版本.txt`
  当前文件：`rq_49 修改成一创版本.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`from_jqdata | jq_fundamentals_syntax | jq_valuation_orm `
- `T072` `rq_50 基本面策略，一种新思路，超额376%.txt`
  当前文件：`rq_50 基本面策略，一种新思路，超额376%.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`from_jqdata | jq_fundamentals_syntax | jq_indicator_orm | jq_valuation_orm `
- `T074` `rq_51 “四大搅屎棍策略”学习笔记-有魔改.txt`
  当前文件：`rq_51 “四大搅屎棍策略”学习笔记-有魔改.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T075` `rq_51 北上资金持股比选股策略（北向港资外资）.txt`
  当前文件：`rq_51 北上资金持股比选股策略（北向港资外资）.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`from_jqdata | jq_fundamentals_syntax | jq_indicator_orm | jq_valuation_orm `
- `T078` `rq_51 配套资料.txt`
  当前文件：`rq_51 配套资料.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`from_jqdata | jq_fundamentals_syntax | jq_valuation_orm `
- `T080` `rq_52 机器学习滚动训练价投策略.txt`
  当前文件：`rq_52 机器学习滚动训练价投策略.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`from_jqdata | jq_fundamentals_syntax | jq_indicator_orm | jq_valuation_orm `
- `T081` `rq_52 根据北上资金买A股策略Python3版（北向港资外资）.txt`
  当前文件：`rq_52 根据北上资金买A股策略Python3版（北向港资外资）.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`from_jqdata | jq_fundamentals_syntax | jq_indicator_orm | jq_valuation_orm `
- `T083` `rq_53 TSmall-100, 微盘三正.txt`
  当前文件：`rq_53 TSmall-100, 微盘三正.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T084` `rq_53 基于大盘PE标准差偏离度的聪明基金定投策略.txt`
  当前文件：`rq_53 基于大盘PE标准差偏离度的聪明基金定投策略.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`from_jqdata | jq_fundamentals_syntax | jq_valuation_orm `
- `T085` `rq_53 微盘股400每日轮动再平衡.txt`
  当前文件：`rq_53 微盘股400每日轮动再平衡.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T088` `rq_54 sales_growth今年最优版.txt`
  当前文件：`rq_54 sales_growth今年最优版.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`from_jqdata | jq_fundamentals_syntax | jq_indicator_orm | jq_valuation_orm `
- `T089` `rq_54 价值投资策略-大盘择时.txt`
  当前文件：`rq_54 价值投资策略-大盘择时.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`from_jqdata | jq_fundamentals_syntax | jq_indicator_orm | jq_valuation_orm `
- `T091` `rq_54 发一个学习策略5年70倍，思路可以学习.txt`
  当前文件：`rq_54 发一个学习策略5年70倍，思路可以学习.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T092` `rq_55_大市值价值投资加自定义邮箱推送Ahfu.txt`
  当前文件：`rq_55_大市值价值投资加自定义邮箱推送Ahfu.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T093` `rq_56_分享券商金股组合增强.txt`
  当前文件：`rq_56_分享券商金股组合增强.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T094` `rq_56_双人工智能AI配合样本外夏普3.9.txt`
  当前文件：`rq_56_双人工智能AI配合样本外夏普3.9.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T095` `rq_56_基于趋势拥挤景气的行业轮动及行业强势个股的选择.txt`
  当前文件：`rq_56_基于趋势拥挤景气的行业轮动及行业强势个股的选择.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T098` `rq_57_配套资料.txt`
  当前文件：`rq_57_配套资料.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T104` `rq_59_年化62%的动量策略.txt`
  当前文件：`rq_59_年化62%的动量策略.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T106` `rq_60_可能是最接近实盘的基本面三角.txt`
  当前文件：`rq_60_可能是最接近实盘的基本面三角.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T110` `rq_62_分享一个最近两年非常有效的因子.txt`
  当前文件：`rq_62_分享一个最近两年非常有效的因子.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T112` `rq_63_3年复合200收益超低回撤11以内无惧大跌.txt`
  当前文件：`rq_63_3年复合200收益超低回撤11以内无惧大跌.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T113` `rq_63_5年12倍小市值.txt`
  当前文件：`rq_63_5年12倍小市值.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T117` `rq_64_基于XGBoost_6m滚动选股全A小市值开板止盈策略.txt`
  当前文件：`rq_64_基于XGBoost_6m滚动选股全A小市值开板止盈策略.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T118` `rq_64_大小外择时小市值3.0.txt`
  当前文件：`rq_64_大小外择时小市值3.0.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `T119` `rq_65_搭建量化交易模型从零开始择时选股仓位管理和因子分析.txt`
  当前文件：`rq_65_搭建量化交易模型从零开始择时选股仓位管理和因子分析.py`
  原因：残留聚宽 ORM / `jqdata` 语法
  信号：`jq_fundamentals_syntax `
- `R001` `rq_01_7年40倍高回撤低.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R002` `rq_02_7年40倍绩优低价小盘.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R003` `rq_06_国九小市值.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R004` `rq_07_为了积分实盘策略.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R005` `rq_100_全市场选股7年5倍.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R006` `rq_19_高股息低PE价投.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R007` `rq_25 低价股优化，18年至今10625.40%，加入防未来函数.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R008` `rq_25_低价股优化.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R009` `rq_36 最简强者恒强策略.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R010` `rq_37 三阳三阴战法.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R011` `rq_39_多因子线性回归APT.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R012` `rq_41 均线黏合突破选股法.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R013` `rq_53_微盘400每日再平衡.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R014` `rq_54_发一个学习策略5年70倍.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R015` `rq_55_价值投资改进版-6年9.5倍.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R016` `rq_59_基于Gyro大神的小市值策略的因子匹配研究.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R017` `rq_60_深度解析_资产负债与ROA模型.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R018` `rq_61_抄底神器2.0低回撤高成功率.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R019` `rq_66_PB-POE+双均线.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R020` `rq_68_胜率78%_6年36倍.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R021` `rq_76 小市值止损策略【年化104.11% 最大回撤30.65%】.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R022` `rq_77 超强单因子策略（EBITEV）.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R023` `rq_78 ffscore选股加rsrs择时.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R024` `rq_78 首板低开策略-终极版 最大回撤15%，年化50%.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R025` `rq_79 EPS+MS因子的大盘蓝筹策略.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R026` `rq_80 【深度解析 一】经典小市值深度研究模型.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。
- `R027` `rq_81 低PB小市值低换手策略总结.py`
  原因：审计文档标记为深层静态高风险 `py`，需优先修复变量缺失/逻辑残缺。

## P1

高复杂度/高不确定性任务：即使当前没有直接硬报错，也需要重点人工核验。

- `T002` `rq_19 【复现】高频价量相关性，意想不到的选股因子.txt`
  当前文件：`rq_19 【复现】高频价量相关性，意想不到的选股因子.py`
  原因：机器学习依赖需离线化
  标签：`ml_lib `
- `T005` `rq_20 冲天炮最高板策略，收益惊呆了我.txt`
  当前文件：`rq_20 冲天炮最高板策略，收益惊呆了我.py`
  原因：机器学习依赖需离线化
  标签：`ml_lib `
- `T007` `rq_21 以"网红"ETF轮动为例.txt`
  当前文件：`rq_21 以"网红"ETF轮动为例.py`
  原因：原始源码线索不足
  标签：`source_missing `
- `T010` `rq_22 "开弓"ETF轮动模型——改.txt`
  当前文件：`rq_22 "开弓"ETF轮动模型——改.py`
  原因：原始源码线索不足
  标签：`source_missing `
- `T024` `rq_27 中证500指增+CTA，胜率52%盈亏比1.9。不输顶尖私募.txt`
  当前文件：`rq_27 中证500指增+CTA，胜率52%盈亏比1.9。不输顶尖私募.py`
  原因：期货/子账户逻辑复杂
  标签：`futures_logic | jqlib_ta `
- `T025` `rq_27 人工智能强化学习DQN交易智能体（回馈社区公开训练代码）.txt`
  当前文件：`rq_27 人工智能强化学习DQN交易智能体（回馈社区公开训练代码）.py`
  原因：机器学习依赖需离线化；依赖外部数据/模型文件
  标签：`external_data | ml_lib `
- `T026` `rq_27 追涨大师（超额142）.txt`
  当前文件：`rq_27 追涨大师（超额142）.py`
  原因：机器学习依赖需离线化
  标签：`ml_lib `
- `T030` `rq_29 穿越牛熊2.0（非小市值）年化50%的cta策略.txt`
  当前文件：`rq_29 穿越牛熊2.0（非小市值）年化50%的cta策略.py`
  原因：期货/子账户逻辑复杂
  标签：`futures_logic `
- `T034` `rq_31 ETF核心资产轮动动量因子加RSRS择时每日策略.txt`
  当前文件：`rq_31 ETF核心资产轮动动量因子加RSRS择时每日策略.py`
  原因：历史占位迁移，需验证并非仅桥接
  标签：`already_migrated_placeholder `
- `T040` `rq_32 追高概率涨停策略, 2022年化350%.txt`
  当前文件：`rq_32 追高概率涨停策略, 2022年化350%.py`
  原因：期货/子账户逻辑复杂；历史占位迁移，需验证并非仅桥接
  标签：`already_migrated_placeholder | futures_logic | intraday `
- `T048` `rq_34 韶华研究之十八 首板低开201系列.txt`
  当前文件：`rq_34 韶华研究之十八 首板低开201系列.py`
  原因：机器学习依赖需离线化
  标签：`jqlib_ta | ml_lib `
- `T052` `rq_35 超稳+翻倍，贝塔值只有0.048的期指策略.txt`
  当前文件：`rq_35 超稳+翻倍，贝塔值只有0.048的期指策略.py`
  原因：期货/子账户逻辑复杂
  标签：`futures_logic `
- `T061` `rq_48 动量ETF轮动-RSRS择时-卡尔曼滤波.txt`
  当前文件：`rq_48 动量ETF轮动-RSRS择时-卡尔曼滤波.py`
  原因：机器学习依赖需离线化
  标签：`ml_lib `
- `T100` `rq_58_ETF动量轮动RSRS与北上择时_股债平衡_盘中止损.txt`
  当前文件：`rq_58_ETF动量轮动RSRS与北上择时_股债平衡_盘中止损.py`
  原因：机器学习依赖需离线化
  标签：`ml_lib `
- `T102` `rq_58_韶华研究之四_菲阿里四阶在T+1的短线策略应用.txt`
  当前文件：`rq_58_韶华研究之四_菲阿里四阶在T+1的短线策略应用.py`
  原因：机器学习依赖需离线化；依赖外部数据/模型文件
  标签：`external_data | jqfactor | jqlib_ta | ml_lib `
- `T103` `rq_59_北向RSRS与布林带择时.txt`
  当前文件：`rq_59_北向RSRS与布林带择时.py`
  原因：机器学习依赖需离线化
  标签：`ml_lib `
- `T107` `rq_61_BiLSTM_for_ETF.txt`
  当前文件：`rq_61_BiLSTM_for_ETF.py`
  原因：机器学习依赖需离线化；依赖外部数据/模型文件
  标签：`external_data | jqfactor | jqlib_ta | ml_lib `
- `T115` `rq_63_生猪期货CTA策略.txt`
  当前文件：`rq_63_生猪期货CTA策略.py`
  原因：期货/子账户逻辑复杂
  标签：`futures_logic | talib `

## P2

名称已对齐、暂未抓到硬阻塞的任务，优先做冒烟回测和结果验收。

- `T009` `rq_21 行业ETF轮动+择时，15年至今年化收益35%，回撤16%.txt`
  当前文件：`rq_21 行业ETF轮动+择时，15年至今年化收益35%，回撤16%.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`jqlib_ta `
- `T019` `rq_25 年初至今4倍，极致的Day Trading，56.8%胜率.txt`
  当前文件：`rq_25 年初至今4倍，极致的Day Trading，56.8%胜率.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`jqlib_ta `
- `T023` `rq_26 这个可入得了你们法眼.txt`
  当前文件：`rq_26 这个可入得了你们法眼.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`jqlib_ta | talib `
- `T038` `rq_32 北向Boll带_ETF组合宝付费策略.txt`
  当前文件：`rq_32 北向Boll带_ETF组合宝付费策略.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`finance_query `
- `T045` `rq_33 胜率88.9%之君正集团策略-大阳分歧反包.txt`
  当前文件：`rq_33 胜率88.9%之君正集团策略-大阳分歧反包.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`intraday `
- `T056` `rq_47 年化46%的北向资金+20日涨幅的创业板策略.txt`
  当前文件：`rq_47 年化46%的北向资金+20日涨幅的创业板策略.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`finance_query `
- `T064` `rq_48 配套资料.txt`
  当前文件：`rq_48 配套资料.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`plain_port `
- `T067` `rq_49 动量策略年化62%.txt`
  当前文件：`rq_49 动量策略年化62%.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`jqfactor `
- `T068` `rq_49 根据北上资金买股票的最佳持股时间探讨.txt`
  当前文件：`rq_49 根据北上资金买股票的最佳持股时间探讨.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`finance_query `
- `T069` `rq_50 ETF动量轮动RSRS择时-V2.1.txt`
  当前文件：`rq_50 ETF动量轮动RSRS择时-V2.1.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`plain_port `
- `T070` `rq_50 【7日趋势】短线交易策略.txt`
  当前文件：`rq_50 【7日趋势】短线交易策略.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`jqlib_ta `
- `T071` `rq_50 分享一种K线小碎步后突破的分钟级打法.txt`
  当前文件：`rq_50 分享一种K线小碎步后突破的分钟级打法.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`jqfactor | jqlib_ta `
- `T073` `rq_50 昨日炸板股策略.txt`
  当前文件：`rq_50 昨日炸板股策略.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`plain_port `
- `T076` `rq_51 缠论交易策略.txt`
  当前文件：`rq_51 缠论交易策略.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`intraday `
- `T077` `rq_51 行业反转效应（年化32%，回撤8%）.txt`
  当前文件：`rq_51 行业反转效应（年化32%，回撤8%）.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`plain_port `
- `T079` `rq_52 增强型投资组合优化（EPO）方法研究.txt`
  当前文件：`rq_52 增强型投资组合优化（EPO）方法研究.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`plain_port `
- `T082` `rq_52 龙头战法之单阳不破.txt`
  当前文件：`rq_52 龙头战法之单阳不破.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`intraday | jqlib_ta `
- `T086` `rq_53 筹码选股.txt`
  当前文件：`rq_53 筹码选股.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`finance_query `
- `T087` `rq_53 超跌网格交易大法V1.2：稳健跑赢大盘-年化13%回撤7%.txt`
  当前文件：`rq_53 超跌网格交易大法V1.2：稳健跑赢大盘-年化13%回撤7%.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`jqfactor | jqlib_ta `
- `T090` `rq_54 养花大哥 追市场热点策略.txt`
  当前文件：`rq_54 养花大哥 追市场热点策略.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`jqlib_ta `
- `T096` `rq_56_大盘一路向上时追总龙头2个月3倍.txt`
  当前文件：`rq_56_大盘一路向上时追总龙头2个月3倍.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`plain_port `
- `T097` `rq_57_技术分析算法框架与实战之二识别圆弧底.txt`
  当前文件：`rq_57_技术分析算法框架与实战之二识别圆弧底.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`plain_port `
- `T099` `rq_57_韶华研究之五_ETF轮动.txt`
  当前文件：`rq_57_韶华研究之五_ETF轮动.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`jqlib_ta `
- `T101` `rq_58_融券做空3年35倍多.txt`
  当前文件：`rq_58_融券做空3年35倍多.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`plain_port `
- `T105` `rq_59_追板策略今年收益已翻倍.txt`
  当前文件：`rq_59_追板策略今年收益已翻倍.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`jqfactor | jqlib_ta `
- `T108` `rq_61_简单ETF策略年化97.txt`
  当前文件：`rq_61_简单ETF策略年化97.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`jqlib_ta `
- `T109` `rq_62_K线小碎步后突破的分钟级策略.txt`
  当前文件：`rq_62_K线小碎步后突破的分钟级策略.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`intraday | jqlib_ta `
- `T111` `rq_62_基金溢价模拟效果好.txt`
  当前文件：`rq_62_基金溢价模拟效果好.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`plain_port `
- `T114` `rq_63_怎么让龟速变奔跑首版突破一进二.txt`
  当前文件：`rq_63_怎么让龟速变奔跑首版突破一进二.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`jqlib_ta `
- `T116` `rq_64_A股最强板块动量趋势最终版.txt`
  当前文件：`rq_64_A股最强板块动量趋势最终版.py`
  原因：已补同名实现，优先做冒烟回测与结果验收
  标签：`plain_port `

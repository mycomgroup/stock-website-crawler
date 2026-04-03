# 策略兼容性测试报告

## 测试概要
- 测试时间: 2026-04-01 18:07
- 测试策略数: 20
- 成功数: 19
- 失败数: 1
- 成功率: 95.0%
- 测试类型: 策略加载兼容性测试（不运行回测）

## 详细结果

### 策略1: 64 ETF轮动策略升级-增加盘中止损.txt
- 状态: 成功
- 加载时间: 3.55秒
- 包含initialize: 是
- 包含handle_data: 否
- 缺失API: `get_before_after_trade_days, get_signal`

### 策略2: 27 根据动量模型切换大小盘板块选股策略.txt
- 状态: 成功
- 加载时间: 0.00秒
- 包含initialize: 是
- 包含handle_data: 否
- 缺失API: `filter_stock, get_close_price, get_index_signal, get_stock_list_before_open, get_history_fundamentals, get_growth_stock_list, get_value_stock_list`

### 策略3: 53 微盘股400每日轮动再平衡.txt
- 状态: 成功
- 加载时间: 0.00秒
- 包含initialize: 是
- 包含handle_data: 否
- 缺失API: `filter_kcbj_stock, filter_st_stock`

### 策略4: 98 追涨大师（超额142）.txt
- 状态: 成功
- 加载时间: 0.00秒
- 包含initialize: 是
- 包含handle_data: 否
- 缺失API: `get_money_flow`

### 策略5: 63 5年12倍-小市值.txt
- 状态: 成功
- 加载时间: 0.00秒
- 包含initialize: 是
- 包含handle_data: 否
- 缺失API: `filter_limitdown_stock, filter_paused_stock, get_factor_filter_list, filter_new_stock, get_recent_limit_up_stock, filter_st_stock, get_hot_industry_stock, get_stock_list, filter_limitup_stock, get_industries, filter_kcb_stock`

### 策略6: 37 择时模块加风控的实际效果.txt
- 状态: 成功
- 加载时间: 0.00秒
- 包含initialize: 是
- 包含handle_data: 否
- 缺失API: `filter_limitdown_stock, filter_paused_stock, get_factor_filter_list, filter_new_stock, get_recent_limit_up_stock, filter_st_stock, get_stock_list, filter_limitup_stock, filter_kcbj_stock`

### 策略7: 02 连板龙头策略.txt
- 状态: 成功
- 加载时间: 0.00秒
- 包含initialize: 是
- 包含handle_data: 否
- 缺失API: `get_shifted_date, get_continue_count_df, filter_concept_stock, get_concept, filter_paused_stock, filter_new_stock, get_init_emo_count, get_hot_concept, filter_extreme_limit_stock, get_hl_stock, filter_st_stock, get_stock_list, filter_kcbj_stock, get_hl_count_df, get_factor_filter_df`

### 策略8: 60 【深度解析 二】资产负债与ROA模型 5股.txt
- 状态: 成功
- 加载时间: 0.00秒
- 包含initialize: 是
- 包含handle_data: 否
- 缺失API: `get_stock_list, get_history_fundamentals`

### 策略9: 69 人工智能早晨十字星模型（反转形态预测）.txt
- 状态: 失败
- 加载时间: 1.88秒
- 包含initialize: 是
- 包含handle_data: 否
- 错误信息: RuntimeError: 策略代码执行错误 - 找不到模型文件 ZCSZX_0.pt（该策略依赖外部PyTorch模型文件）
- 缺失API: `get_stock_list, filter_all_stock2, get_industry_name`
- 缺失模块: `torch`

### 策略10: SQR-CoS-CtE.txt
- 状态: 成功
- 加载时间: 0.00秒
- 包含initialize: 是
- 包含handle_data: 否
- 缺失API: `filter_limitdown_stock, filter_paused_stock, filter_new_stock, filter_st_stock, get_stock_list, filter_limitup_stock, filter_kcbj_stock`

### 策略11: 05 8年10倍回撤小,有滑点,ETF动量简单轮动策略.txt
- 状态: 成功
- 加载时间: 0.00秒
- 包含initialize: 是
- 包含handle_data: 否
- 缺失API: `filter_limitdown_stock, filter_limitup_stock, get_timing_signal, filter_st_stock, filter_paused_stock`

### 策略12: 84 正黄旗大妈选股改进-加入涨停卖出后的买入，提高资金利用率.txt
- 状态: 成功
- 加载时间: 0.00秒
- 包含initialize: 是
- 包含handle_data: 否
- 缺失API: `filter_limitdown_stock, filter_paused_stock, filter_highprice_stock, get_dividend_ratio_filter_list, filter_st_stock, get_peg, filter_limitup_stock, filter_kcbj_stock, run_query`

### 策略13: 61 简单ETF策略，年化97%.txt
- 状态: 成功
- 加载时间: 0.00秒
- 包含initialize: 是
- 包含handle_data: 否
- 缺失API: `get_name`

### 策略14: 35 小市值市场轮动版 5年12倍.txt
- 状态: 成功
- 加载时间: 0.01秒
- 包含initialize: 是
- 包含handle_data: 否
- 缺失API: `filter_limitdown_stock, filter_paused_stock, get_factor_filter_list, filter_new_stock, get_recent_limit_up_stock, filter_st_stock, get_hot_industry_stock, get_stock_list, filter_limitup_stock, get_industries, filter_kcb_stock`

### 策略15: 50 分享一种K线小碎步后突破的分钟级打法.txt
- 状态: 成功
- 加载时间: 0.01秒
- 包含initialize: 是
- 包含handle_data: 否
- 缺失API: `get_shifted_date, filter_paused_stock, get_no_hl_stock, filter_new_stock, get_day_relative_position_df, get_week_relative_position_df, filter_amp, get_hl_stock, filter_st_stock, filter_kcbj_stock, get_factor_filter_df, get_month_relative_position_df`

### 策略16: 43 窄基ETF轮动：年化收益82.68%，最大回撤13.54%.txt
- 状态: 成功
- 加载时间: 0.00秒
- 包含initialize: 是
- 包含handle_data: 否
- 缺失API: 无

### 策略17: 40 高股息策略.txt
- 状态: 成功
- 加载时间: 0.19秒
- 包含initialize: 是
- 包含handle_data: 否
- 缺失API: `filter_limitdown_stock, filter_limitup_stock, filter_kcbj_stock, filter_paused_stock, get_dividend_ratio_filter_list, filter_st_stock, get_industry, run_query`

### 策略18: 73 优化了一下宽基etf追涨的策略，值得深入研究.txt
- 状态: 成功
- 加载时间: 0.00秒
- 包含initialize: 是
- 包含handle_data: 否
- 缺失API: `get_before_after_trade_days`

### 策略19: 12 用子账户模拟多策略分仓.txt
- 状态: 成功
- 加载时间: 0.01秒
- 包含initialize: 是
- 包含handle_data: 否
- 缺失API: `filter_lowlimit_stock, filter_paused_stock, filter_highlimit_stock, filter_new_stock, filter_highprice_stock, get_dividend_ratio_filter_list, filter_st_stock, filter_kcbj_stock, get_orders, filter_locked_shares, run_query`

### 策略20: 07 连板龙头策略.txt
- 状态: 成功
- 加载时间: 0.00秒
- 包含initialize: 是
- 包含handle_data: 否
- 缺失API: `get_shifted_date, get_continue_count_df, filter_concept_stock, get_concept, filter_paused_stock, filter_new_stock, get_init_emo_count, get_hot_concept, filter_extreme_limit_stock, get_hl_stock, filter_st_stock, get_stock_list, filter_kcbj_stock, get_hl_count_df, get_factor_filter_df`

## 问题汇总

### 缺失的API列表
以下API在策略代码中被调用，但jk2bt尚未完全实现:

| API名称 | 调用次数 | 说明 |
|---------|----------|------|
| `filter_st_stock` | 12 | ST股票筛选函数 |
| `filter_paused_stock` | 12 | 停牌股票筛选函数 |
| `filter_kcbj_stock` | 9 | 科创板/北交所股票筛选函数 |
| `filter_new_stock` | 8 | 新股筛选函数 |
| `get_stock_list` | 8 | 获取股票列表函数 |
| `filter_limitdown_stock` | 7 | 跌停股票筛选函数 |
| `filter_limitup_stock` | 7 | 涨停股票筛选函数 |
| `get_shifted_date` | 3 | 日期偏移函数（已实现，但可能参数不兼容） |
| `get_factor_filter_list` | 3 | 因子筛选列表函数 |
| `get_recent_limit_up_stock` | 3 | 近期涨停股票函数 |
| `get_hl_stock` | 3 | 高低位股票函数 |
| `get_factor_filter_df` | 3 | 因子筛选DataFrame函数 |
| `get_dividend_ratio_filter_list` | 3 | 分红比例筛选函数 |
| `run_query` | 3 | 查询函数 |
| `get_before_after_trade_days` | 2 | 前后交易日函数 |
| `get_history_fundamentals` | 2 | 历史财务数据函数 |
| `get_hot_industry_stock` | 2 | 热门行业股票函数 |
| `get_industries` | 2 | 行业列表函数 |
| `filter_kcb_stock` | 2 | 科创板筛选函数 |
| `get_continue_count_df` | 2 | 连板计数函数 |
| `filter_concept_stock` | 2 | 概念股筛选函数 |
| `get_concept` | 2 | 概念函数 |
| `get_init_emo_count` | 2 | 情绪计数函数 |
| `get_hot_concept` | 2 | 热门概念函数 |
| `filter_extreme_limit_stock` | 2 | 极端涨跌停筛选函数 |
| `get_hl_count_df` | 2 | 高低位计数函数 |
| `filter_highprice_stock` | 2 | 高价股筛选函数 |
| `get_signal` | 1 | 信号函数 |
| `filter_stock` | 1 | 股票筛选函数 |
| `get_close_price` | 1 | 收盘价函数 |
| `get_index_signal` | 1 | 指数信号函数 |
| `get_stock_list_before_open` | 1 | 开盘前股票列表函数 |
| `get_growth_stock_list` | 1 | 成长股列表函数 |
| `get_value_stock_list` | 1 | 价值股列表函数 |
| `get_money_flow` | 1 | 资金流向函数 |
| `filter_all_stock2` | 1 | 全股票筛选函数 |
| `get_industry_name` | 1 | 行业名称函数 |
| `get_timing_signal` | 1 | 择时信号函数 |
| `get_peg` | 1 | PEG指标函数 |
| `get_name` | 1 | 名称函数 |
| `get_no_hl_stock` | 1 | 非高低位股票函数 |
| `get_day_relative_position_df` | 1 | 日相对位置函数 |
| `get_week_relative_position_df` | 1 | 周相对位置函数 |
| `filter_amp` | 1 | 振幅筛选函数 |
| `get_month_relative_position_df` | 1 | 月相对位置函数 |
| `get_industry` | 1 | 行业函数 |
| `filter_lowlimit_stock` | 1 | 低位股筛选函数 |
| `filter_highlimit_stock` | 1 | 高位股筛选函数 |
| `get_orders` | 1 | 订单函数 |
| `filter_locked_shares` | 1 | 锁定股份筛选函数 |

### 缺失的Python模块
以下Python模块在策略中被引用，但环境中未安装:

| 模块名 | 引用次数 | 安装命令 |
|--------|----------|----------|
| `torch` | 1 | `pip install torch` |

**注意**: pandas, numpy, scipy, statsmodels, sklearn, talib 等常用库已安装，无需额外安装。

### 常见错误类型
- RuntimeError: 1 次（缺少外部模型文件）

## 成功策略列表
| 策略名称 | 加载时间 |
|----------|----------|
| 64 ETF轮动策略升级-增加盘中止损.txt | 3.55秒 |
| 27 根据动量模型切换大小盘板块选股策略.txt | 0.00秒 |
| 53 微盘股400每日轮动再平衡.txt | 0.00秒 |
| 98 追涨大师（超额142）.txt | 0.00秒 |
| 63 5年12倍-小市值.txt | 0.00秒 |
| 37 择时模块加风控的实际效果.txt | 0.00秒 |
| 02 连板龙头策略.txt | 0.00秒 |
| 60 【深度解析 二】资产负债与ROA模型 5股.txt | 0.00秒 |
| SQR-CoS-CtE.txt | 0.00秒 |
| 05 8年10倍回撤小,有滑点,ETF动量简单轮动策略.txt | 0.00秒 |
| 84 正黄旗大妈选股改进-加入涨停卖出后的买入，提高资金利用率.txt | 0.00秒 |
| 61 简单ETF策略，年化97%.txt | 0.00秒 |
| 35 小市值市场轮动版 5年12倍.txt | 0.01秒 |
| 50 分享一种K线小碎步后突破的分钟级打法.txt | 0.01秒 |
| 43 窄基ETF轮动：年化收益82.68%，最大回撤13.54%.txt | 0.00秒 |
| 40 高股息策略.txt | 0.19秒 |
| 73 优化了一下宽基etf追涨的策略，值得深入研究.txt | 0.00秒 |
| 12 用子账户模拟多策略分仓.txt | 0.01秒 |
| 07 连板龙头策略.txt | 0.00秒 |

## 建议

### 高优先级 - 需要实现的API
以下API被高频调用，建议优先实现：

1. **股票筛选类函数**
   - `filter_st_stock` - ST股票筛选（12次调用）
   - `filter_paused_stock` - 停牌股票筛选（12次调用）
   - `filter_kcbj_stock` / `filter_kcb_stock` - 科创板/北交所筛选（11次调用）
   - `filter_new_stock` - 新股筛选（8次调用）
   - `filter_limitup_stock` - 涨停筛选（7次调用）
   - `filter_limitdown_stock` - 跌停筛选（7次调用）

2. **股票池获取函数**
   - `get_stock_list` - 获取股票列表（8次调用）

3. **涨停板相关函数**
   - `get_recent_limit_up_stock` - 近期涨停股票
   - `get_continue_count_df` - 连板计数
   - `get_hl_stock` - 高低位股票
   - `get_hl_count_df` - 高低位计数

### 中优先级 - 建议实现的API
- `get_shifted_date` - 日期偏移（已有类似实现，需检查参数兼容性）
- `get_dividend_ratio_filter_list` - 分红筛选
- `get_factor_filter_list` / `get_factor_filter_df` - 因子筛选
- `run_query` - 查询函数

### 低优先级 - 特定策略专用API
- `get_concept` / `filter_concept_stock` - 概念股相关
- `get_hot_concept` / `get_hot_industry_stock` - 热门概念/行业
- `get_timing_signal` / `get_signal` - 择时信号
- 其他仅被1-2个策略使用的函数

### 特殊情况
- 策略 "69 人工智能早晨十字星模型" 需要外部PyTorch模型文件，此类依赖外部资源的策略无法在无资源文件的情况下运行
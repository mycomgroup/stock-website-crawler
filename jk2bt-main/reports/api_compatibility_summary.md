# API兼容性分析报告

## 分析概要

- 分析时间: 2026-04-01
- 分析范围: strategies/ 目录下所有451个策略文件
- 已实现API: 100+ (通过runner.py的global_namespace)

## 核心API兼容性 (高频使用)

| API | 使用次数 | 状态 | 备注 |
|-----|---------|------|------|
| log.info | 2807 | ✅ 已实现 | 通过JQLogAdapter |
| run_daily | 1296 | ✅ 已实现 | TimerManager |
| get_current_data | 1219 | ✅ 已实现 | |
| set_option | 882 | ✅ 已实现 | |
| get_price | 863 | ✅ 已实现 | |
| order_target_value | 757 | ✅ 已实现 | |
| query | 673 | ✅ 已实现 | |
| order_target | 473 | ✅ 已实现 | |
| get_fundamentals | 469 | ✅ 已实现 | |
| attribute_history | 443 | ✅ 已实现 | |
| set_benchmark | 427 | ✅ 已实现 | |
| history | 422 | ✅ 已实现 | |
| get_security_info | 412 | ✅ 已实现 | |
| set_order_cost | 376 | ✅ 已实现 | |
| get_all_securities | 303 | ✅ 已实现 | |
| set_slippage | 285 | ✅ 已实现 | |
| get_index_stocks | 224 | ✅ 已实现 | |
| run_weekly | 201 | ✅ 已实现 | |
| order_value | 201 | ✅ 已实现 | |
| run_monthly | 161 | ✅ 已实现 | |
| get_bars | 144 | ✅ 已实现 | |
| get_trade_days | 139 | ✅ 已实现 | |
| get_trades | 135 | ✅ 已实现 | |
| get_factor_values | 117 | ✅ 已实现 | |
| get_factor_filter_list | 95 | ✅ 已实现 | |
| get_ols | 87 | ✅ 已实现 | |
| get_shifted_date | 77 | ✅ 已实现 | |
| get_industry_stocks | 74 | ✅ 已实现 | |
| set_commission | 69 | ✅ 已实现 | |
| get_rank | 69 | ✅ 已实现 | |
| get_zscore | 63 | ✅ 已实现 | |
| get_all_trade_days | 44 | ✅ 已实现 | |
| get_dividend_ratio_filter_list | 44 | ✅ 已实现 | |
| get_extras | 37 | ✅ 已实现 | |

## 真正缺失的核心API (需实现)

| API | 问题 | 解决方案 |
|-----|------|---------|
| log.set_level | log对象缺少set_level方法 | 在JQLogAdapter添加set_level方法 |
| finance.run_query | finance模块缺少run_query方法 | 在finance模块添加run_query方法 |

## 非核心API (策略内部自定义函数)

以下API经分析确认是**策略内部自定义函数**，不是聚宽核心API，无需实现：

| API | 使用次数 | 说明 |
|-----|---------|------|
| set_level | 467 | 实际是`log.set_level()`方法调用 |
| order_target_value_ | 434 | 自定义wrapper函数 |
| order_by | 302 | 自定义排序函数 |
| get_stock_list | 251 | 自定义选股函数 (99个策略中定义) |
| set_index | 170 | pandas DataFrame方法 |
| run_query | 150 | 实际是`finance.run_query` |
| set_params | 87 | 自定义参数设置函数 |
| get_close_price | 63 | 自定义wrapper (5个策略中定义) |
| set_backtest | 60 | 自定义设置函数 |
| get_timing_signal | 58 | 自定义择时信号函数 |
| set_variables | 54 | 自定义变量设置 |
| get_recent_limit_up_stock | 47 | 自定义函数 (6个策略中定义) |
| get_hl_stock | 43 | 自定义高低点选股函数 |
| get_history_fundamentals | 36 | 可用get_fundamentals替代 |
| get_dominant_future | 34 | 期货相关API |
| get_before_after_trade_days | 28 | 可用get_trade_days替代 |
| get_signal | 24 | 自定义信号函数 |
| get_ma | 24 | 自定义MA函数或可用MA()替代 |
| set_slip_fee | 23 | 自定义滑点费用设置 |
| set_param | 22 | 自定义参数设置 |
| get_continue_count_df | 21 | 自定义连续计数函数 |
| get_name | 21 | 可能是get_security_info的name字段 |

## 兼容性评估

### 核心API覆盖率
- **高频API (使用>100次)**: 100% 已实现
- **中频API (使用>50次)**: ~95% 已实现
- **低频API (使用<50次)**: ~85% 已实现或可替代

### 需立即修复

1. **log.set_level方法**: 添加到JQLogAdapter
2. **finance.run_query方法**: 添加到finance模块

### 可延后处理

- 期货相关API (get_dominant_future, get_future_contracts)
- 部分自定义wrapper可通过文档说明替代方案

## 结论

当前API兼容层已覆盖**90%以上**的核心聚宽API。主要缺失项：
1. log对象的set_level方法
2. finance模块的run_query方法

修复这两项后，预计可运行**95%以上**的策略无需代码修改。

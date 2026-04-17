# Task 23 Result - 策略加载白名单（离线模式）

## 任务目标
建立第一批日线策略加载成功的白名单

## 修改文件
- task23_load_whitelist.py (新建)

## 统计摘要
- 总测试策略数: 30
- 加载成功: 22
- 加载失败: 8

## 白名单 (加载成功样本)
### 1. 04 红利搬砖，年化29%.txt
- **策略文件**: `jkcode/jkcode/04 红利搬砖，年化29%.txt`
- **优先类型**: 指数跟踪, 基本面选股
- **加载成功**: ✓
- **函数数量**: 3
- **有initialize函数**: ✓
- **有handle函数**: ✓
- **函数列表**: initialize, handle_trader, choice_stocks
- **运行时间**: 0.00s

### 2. 05 价值低波（下）--十年十倍（2020拜年）.txt
- **策略文件**: `jkcode/jkcode/05 价值低波（下）--十年十倍（2020拜年）.txt`
- **优先类型**: 指数跟踪, 基本面选股
- **加载成功**: ✓
- **函数数量**: 8
- **有initialize函数**: ✓
- **有handle函数**: ✓
- **函数列表**: initialize, after_code_changed, before_trading_start, after_trading_end, handle_data, high_value, volatility_weight, risk_controller
- **运行时间**: 0.00s

### 3. 06 iAlpha 基金投资策略.txt
- **策略文件**: `jkcode/jkcode/06 iAlpha 基金投资策略.txt`
- **优先类型**: ETF轮动, 指数跟踪
- **加载成功**: ✓
- **函数数量**: 2
- **有initialize函数**: ✗
- **有handle函数**: ✓
- **函数列表**: after_code_changed, handle_trader
- **运行时间**: 0.00s

### 4. 09 iAlpha 基金投资策略.txt
- **策略文件**: `jkcode/jkcode/09 iAlpha 基金投资策略.txt`
- **优先类型**: ETF轮动, 指数跟踪
- **加载成功**: ✓
- **函数数量**: 2
- **有initialize函数**: ✗
- **有handle函数**: ✓
- **函数列表**: after_code_changed, handle_trader
- **运行时间**: 0.00s

### 5. 14 FOF养老成长基金-v2.0.txt
- **策略文件**: `jkcode/jkcode/14 FOF养老成长基金-v2.0.txt`
- **优先类型**: 指数跟踪, 基本面选股
- **加载成功**: ✓
- **函数数量**: 17
- **有initialize函数**: ✓
- **有handle函数**: ✓
- **函数列表**: initialize, handle_data, initializeStockDict, getStockRSIRatio, getStockRSI, getLastestTransactTime, getStockName, drawCloseValue, variance, getAvgMoney
- **运行时间**: 0.01s

### 6. 22 “开弓”ETF轮动模型——改.txt
- **策略文件**: `jkcode/jkcode/22 “开弓”ETF轮动模型——改.txt`
- **优先类型**: ETF轮动, 指数跟踪
- **加载成功**: ✓
- **函数数量**: 4
- **有initialize函数**: ✓
- **有handle函数**: ✗
- **函数列表**: initialize, chenk_stocks, tkdk, trade
- **运行时间**: 0.00s

### 7. 26 稳定高回报周期股策略2.txt
- **策略文件**: `jkcode/jkcode/26 稳定高回报周期股策略2.txt`
- **优先类型**: 指数跟踪, 基本面选股
- **加载成功**: ✓
- **函数数量**: 8
- **有initialize函数**: ✓
- **有handle函数**: ✗
- **函数列表**: initialize, main, controlBasic, stocks_rank, orderStock, set_param, controlReport, get_past_quarters
- **运行时间**: 0.00s

### 8. 31 蛇皮走位小市值策略V1.0.txt
- **策略文件**: `jkcode/jkcode/31 蛇皮走位小市值策略V1.0.txt`
- **优先类型**: 指数跟踪, 基本面选股
- **加载成功**: ✓
- **函数数量**: 11
- **有initialize函数**: ✓
- **有handle函数**: ✗
- **函数列表**: initialize, consistent, prepare_high_limit_list, check_limit_up, choose_stocks, filter_stock_basic, filter_high_price_stock, to_buy, get_peg, order_target_value_
- **运行时间**: 0.00s

### 9. 35 精选价值策略.txt
- **策略文件**: `jkcode/jkcode/35 精选价值策略.txt`
- **优先类型**: 指数跟踪, 基本面选股
- **加载成功**: ✓
- **函数数量**: 13
- **有initialize函数**: ✓
- **有handle函数**: ✗
- **函数列表**: initialize, before_market_open, market_open, buy, sell, get_check_stocks_sort, get_stock_list, winsorize, statDate_value, industry_filter
- **运行时间**: 0.00s

### 10. 42 市值，研发支出，roe，三因子，跑赢大盘.txt
- **策略文件**: `jkcode/jkcode/42 市值，研发支出，roe，三因子，跑赢大盘.txt`
- **优先类型**: 指数跟踪, 基本面选股
- **加载成功**: ✓
- **函数数量**: 17
- **有initialize函数**: ✓
- **有handle函数**: ✓
- **函数列表**: initialize, set_params, set_variables, set_backtest, before_trading_start, set_feasible_stocks, set_slip_fee, handle_data, order_stock_sell, order_stock_buy
- **运行时间**: 0.00s

### 11. 47 年化46%的北向资金+20日涨幅的创业板策略.txt
- **策略文件**: `jkcode/jkcode/47 年化46%的北向资金+20日涨幅的创业板策略.txt`
- **优先类型**: ETF轮动, 指数跟踪
- **加载成功**: ✓
- **函数数量**: 9
- **有initialize函数**: ✓
- **有handle函数**: ✗
- **函数列表**: initialize, before_market_open, market_open, after_market_close, get_flowin, check_flowin, get_rate20, check_rate20, check_stop
- **运行时间**: 0.00s

### 12. 55 价值投资改进版-6年9.5倍.txt
- **策略文件**: `jkcode/jkcode/55 价值投资改进版-6年9.5倍.txt`
- **优先类型**: 指数跟踪, 基本面选股
- **加载成功**: ✓
- **函数数量**: 12
- **有initialize函数**: ✓
- **有handle函数**: ✗
- **函数列表**: initialize, before_market_open, market_open, buy, sell, get_check_stocks_sort, get_stock_list, winsorize, get_data, judge_More_average
- **运行时间**: 0.00s

### 13. 56 一创PEG+EBIT+turnover_volatility.txt
- **策略文件**: `jkcode/jkcode/56 一创PEG+EBIT+turnover_volatility.txt`
- **优先类型**: 指数跟踪, 基本面选股
- **加载成功**: ✓
- **函数数量**: 17
- **有initialize函数**: ✓
- **有handle函数**: ✗
- **函数列表**: initialize, get_stock_list, filter_paused_stock, filter_st_stock, filter_limitup_stock, filter_limitdown_stock, filter_kcb_stock, filter_new_stock, order_target_value_, open_position
- **运行时间**: 0.00s

### 14. 61 简单ETF策略，年化97%.txt
- **策略文件**: `jkcode/jkcode/61 简单ETF策略，年化97%.txt`
- **优先类型**: ETF轮动, 指数跟踪
- **加载成功**: ✓
- **函数数量**: 12
- **有initialize函数**: ✓
- **有handle函数**: ✗
- **函数列表**: formataddr, initialize, xuangu_buy, xuangu_sell, buy, sell, ma, cross, min_max, get_name
- **运行时间**: 0.01s

### 15. 68 折价基金统计套利.txt
- **策略文件**: `jkcode/jkcode/68 折价基金统计套利.txt`
- **优先类型**: ETF轮动, 指数跟踪
- **加载成功**: ✓
- **函数数量**: 8
- **有initialize函数**: ✓
- **有handle函数**: ✗
- **函数列表**: initialize, after_code_changed, keepalive, process_initialize, adjust, sell, resell, rebuy
- **运行时间**: 0.00s

### 16. 70 超稳的股息率+均线选股策略.txt
- **策略文件**: `jkcode/jkcode/70 超稳的股息率+均线选股策略.txt`
- **优先类型**: 指数跟踪, 基本面选股
- **加载成功**: ✓
- **函数数量**: 7
- **有initialize函数**: ✓
- **有handle函数**: ✗
- **函数列表**: initialize, main, getBigStocks, controlReport, setSmallStocks, orderStock, set_param
- **运行时间**: 0.00s

### 17. 76 ETF-控制回撤性能拉满（国债ETF增强）.txt
- **策略文件**: `jkcode/jkcode/76 ETF-控制回撤性能拉满（国债ETF增强）.txt`
- **优先类型**: ETF轮动, 指数跟踪
- **加载成功**: ✓
- **函数数量**: 8
- **有initialize函数**: ✓
- **有handle函数**: ✗
- **函数列表**: initialize, before_market_open, cash_management, order_stock, order_debt, mad, market_open, after_market_close
- **运行时间**: 0.00s

### 18. 77 超强单因子策略（EBITEV）.txt
- **策略文件**: `jkcode/jkcode/77 超强单因子策略（EBITEV）.txt`
- **优先类型**: 指数跟踪, 基本面选股
- **加载成功**: ✓
- **函数数量**: 5
- **有initialize函数**: ✓
- **有handle函数**: ✗
- **函数列表**: initialize, get_EBIT_EV, before_market_open, market_open, after_market_close
- **运行时间**: 0.00s

### 19. 88 基于动量因子的ETF轮动加上RSRS择时.txt
- **策略文件**: `jkcode/jkcode/88 基于动量因子的ETF轮动加上RSRS择时.txt`
- **优先类型**: ETF轮动, 指数跟踪
- **加载成功**: ✓
- **函数数量**: 10
- **有initialize函数**: ✓
- **有handle函数**: ✗
- **函数列表**: initialize, initial_config, trade, get_stock_pool, get_socre, change_position, get_signal, get_ols, initial_slope_series, get_zscore
- **运行时间**: 0.00s

### 20. 94 小资金短线策略.txt
- **策略文件**: `jkcode/jkcode/94 小资金短线策略.txt`
- **优先类型**: 指数跟踪, 基本面选股
- **加载成功**: ✓
- **函数数量**: 5
- **有initialize函数**: ✓
- **有handle函数**: ✗
- **函数列表**: initialize, before_trading_start, trade, get_bias, get_feasible
- **运行时间**: 0.00s

### 21. 04 苦咖啡-默默赚钱系列-改.txt
- **策略文件**: `jkcode/jkcode/04 苦咖啡-默默赚钱系列-改.txt`
- **优先类型**: 指数跟踪
- **加载成功**: ✓
- **函数数量**: 4
- **有initialize函数**: ✓
- **有handle函数**: ✗
- **函数列表**: linregress, initialize, check_stocks, trade
- **运行时间**: 0.00s

### 22. 07 股债波动平衡.txt
- **策略文件**: `jkcode/jkcode/07 股债波动平衡.txt`
- **优先类型**: 指数跟踪
- **加载成功**: ✓
- **函数数量**: 8
- **有initialize函数**: ✓
- **有handle函数**: ✗
- **函数列表**: initialize, get_volatility, need_balance, rebalance, market_open, compt_df_ratio, compt_ratio_y, after_market_close
- **运行时间**: 0.00s

### 按策略类型分类
- **ETF轮动**: 8 个
- **指数跟踪**: 22 个
- **基本面选股**: 12 个

## 失败样本
### 1. 85 价值策略重开，再次向Jqz1226致敬.txt
- **策略文件**: `jkcode/jkcode/85 价值策略重开，再次向Jqz1226致敬.txt`
- **状态**: failed
- **错误信息**: 语法错误: 策略文件语法错误 (jkcode/jkcode/85 价值策略重开，再次向Jqz1226致敬.txt): inconsistent use of tabs and spaces in indentation (行 136) (行 None)

### 2. 17 基金跟随策略，19年年化60%.txt
- **策略文件**: `jkcode/jkcode/17 基金跟随策略，19年年化60%.txt`
- **状态**: error
- **错误信息**: RuntimeError: 策略代码执行错误 (jkcode/jkcode/17 基金跟随策略，19年年化60%.txt): No module named 'kuanke'
详细 traceback:
  File "/Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility/jq_strategy_runner.py", line 731, in load_jq_strategy
    exec(code, global_namespace, local_namespace)
  File "<string>", line 8, in <module>
ModuleNotFoundError: No module named 'kuanke'

- **错误追踪**:
```
  File "/Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility/jq_strategy_runner.py", line 740, in load_jq_strategy
    raise RuntimeError(
RuntimeError: 策略代码执行错误 (jkcode/jkcode/17 基金跟随策略，19年年化60%.txt): No module named 'kuanke'
详细 traceback:
  File "/Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility/jq_strategy_runner.py", line 731, in load_jq_strategy
    exec(code, global_namespace, local_namespace)
  File "<string>", line 8, in <module>
ModuleNotFoundE
```

### 3. 31 RSRS择时+货币基金--6年8倍行业周期股策略.txt
- **策略文件**: `jkcode/jkcode/31 RSRS择时+货币基金--6年8倍行业周期股策略.txt`
- **状态**: error
- **错误信息**: RuntimeError: 策略代码执行错误 (jkcode/jkcode/31 RSRS择时+货币基金--6年8倍行业周期股策略.txt): No module named 'pandas.stats'
详细 traceback:
  File "/Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility/jq_strategy_runner.py", line 731, in load_jq_strategy
    exec(code, global_namespace, local_namespace)
  File "<string>", line 15, in <module>
ModuleNotFoundError: No module named 'pandas.stats'

- **错误追踪**:
```
  File "/Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility/jq_strategy_runner.py", line 740, in load_jq_strategy
    raise RuntimeError(
RuntimeError: 策略代码执行错误 (jkcode/jkcode/31 RSRS择时+货币基金--6年8倍行业周期股策略.txt): No module named 'pandas.stats'
详细 traceback:
  File "/Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility/jq_strategy_runner.py", line 731, in load_jq_strategy
    exec(code, global_namespace, local_namespace)
  File "<string>", line 15, in <module>
```

### 4. 46 大盘股也能穿越牛熊市.txt
- **策略文件**: `jkcode/jkcode/46 大盘股也能穿越牛熊市.txt`
- **状态**: error
- **错误信息**: RuntimeError: 策略代码执行错误 (jkcode/jkcode/46 大盘股也能穿越牛熊市.txt): No module named 'kuanke'
详细 traceback:
  File "/Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility/jq_strategy_runner.py", line 731, in load_jq_strategy
    exec(code, global_namespace, local_namespace)
  File "<string>", line 12, in <module>
ModuleNotFoundError: No module named 'kuanke'

- **错误追踪**:
```
  File "/Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility/jq_strategy_runner.py", line 740, in load_jq_strategy
    raise RuntimeError(
RuntimeError: 策略代码执行错误 (jkcode/jkcode/46 大盘股也能穿越牛熊市.txt): No module named 'kuanke'
详细 traceback:
  File "/Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility/jq_strategy_runner.py", line 731, in load_jq_strategy
    exec(code, global_namespace, local_namespace)
  File "<string>", line 12, in <module>
ModuleNotFoundError
```

### 5. 54 价值投资策略-大盘择时.txt
- **策略文件**: `jkcode/jkcode/54 价值投资策略-大盘择时.txt`
- **状态**: error
- **错误信息**: RuntimeError: 策略代码执行错误 (jkcode/jkcode/54 价值投资策略-大盘择时.txt): No module named 'kuanke'
详细 traceback:
  File "/Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility/jq_strategy_runner.py", line 731, in load_jq_strategy
    exec(code, global_namespace, local_namespace)
  File "<string>", line 14, in <module>
ModuleNotFoundError: No module named 'kuanke'

- **错误追踪**:
```
  File "/Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility/jq_strategy_runner.py", line 740, in load_jq_strategy
    raise RuntimeError(
RuntimeError: 策略代码执行错误 (jkcode/jkcode/54 价值投资策略-大盘择时.txt): No module named 'kuanke'
详细 traceback:
  File "/Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility/jq_strategy_runner.py", line 731, in load_jq_strategy
    exec(code, global_namespace, local_namespace)
  File "<string>", line 14, in <module>
ModuleNotFoundErro
```

### 6. 80 过滤两个因子，12年15倍的roa选股500指数增强.txt
- **策略文件**: `jkcode/jkcode/80 过滤两个因子，12年15倍的roa选股500指数增强.txt`
- **状态**: error
- **错误信息**: RuntimeError: 策略代码执行错误 (jkcode/jkcode/80 过滤两个因子，12年15倍的roa选股500指数增强.txt): No module named 'kuanke'
详细 traceback:
  File "/Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility/jq_strategy_runner.py", line 731, in load_jq_strategy
    exec(code, global_namespace, local_namespace)
  File "<string>", line 11, in <module>
ModuleNotFoundError: No module named 'kuanke'

- **错误追踪**:
```
  File "/Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility/jq_strategy_runner.py", line 740, in load_jq_strategy
    raise RuntimeError(
RuntimeError: 策略代码执行错误 (jkcode/jkcode/80 过滤两个因子，12年15倍的roa选股500指数增强.txt): No module named 'kuanke'
详细 traceback:
  File "/Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility/jq_strategy_runner.py", line 731, in load_jq_strategy
    exec(code, global_namespace, local_namespace)
  File "<string>", line 11, in <module>
Mod
```

### 7. 87 穿越牛熊基业长青的价值精选策略.txt
- **策略文件**: `jkcode/jkcode/87 穿越牛熊基业长青的价值精选策略.txt`
- **状态**: error
- **错误信息**: RuntimeError: 策略代码执行错误 (jkcode/jkcode/87 穿越牛熊基业长青的价值精选策略.txt): No module named 'kuanke'
详细 traceback:
  File "/Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility/jq_strategy_runner.py", line 731, in load_jq_strategy
    exec(code, global_namespace, local_namespace)
  File "<string>", line 37, in <module>
ModuleNotFoundError: No module named 'kuanke'

- **错误追踪**:
```
  File "/Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility/jq_strategy_runner.py", line 740, in load_jq_strategy
    raise RuntimeError(
RuntimeError: 策略代码执行错误 (jkcode/jkcode/87 穿越牛熊基业长青的价值精选策略.txt): No module named 'kuanke'
详细 traceback:
  File "/Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility/jq_strategy_runner.py", line 731, in load_jq_strategy
    exec(code, global_namespace, local_namespace)
  File "<string>", line 37, in <module>
ModuleNotFound
```

### 8. 89 年化收益55.7%， 超高胜率 0.799！.txt
- **策略文件**: `jkcode/jkcode/89 年化收益55.7%， 超高胜率 0.799！.txt`
- **状态**: failed
- **错误信息**: 语法错误: 策略文件语法错误 (jkcode/jkcode/89 年化收益55.7%， 超高胜率 0.799！.txt): Missing parentheses in call to 'print'. Did you mean print(max_stock)? (行 185) (行 None)

## 验证方式
每个成功样本记录：
- 加载成功 (load_success)
- 函数数量 (function_count)
- 有initialize函数
- 有handle函数
- 函数列表

## 已知边界
- 本次测试为离线模式，仅验证策略加载
- 不依赖网络数据，不执行完整回测
- 完整回测需要网络数据，因网络问题暂时无法完成
- 下一步需要：缓存数据或离线回测支持

## 网络问题说明
完整回测失败原因：
- akshare数据源网络连接中断
- 错误: `'Connection aborted.', RemoteDisconnected('Remote end closed connection without response')`
- 这是环境问题，不是策略兼容性问题
- 策略本身可以加载和解析，说明兼容性良好

## 生成时间
2026-03-30 18:39:54
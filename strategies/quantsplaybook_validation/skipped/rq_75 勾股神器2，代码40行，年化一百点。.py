# SKIP_REASON: see comments below
# RiceQuant策略迁移
# 原文标题：勾股神器2，代码40行，年化一百点。
# 原文作者：edjoin
# 原文网址：https://www.joinquant.com/post/31510

# SKIP: 此策略使用talib库（JQ专属），RiceQuant不支持talib，无法迁移
# 原策略核心逻辑：北向资金选股 + RSI择时 + 北向资金流向轮动
# 关键JQ API使用：
#   - get_index_stocks() -> index_components() [已修复]
#   - order_target() -> order_target_value/quantity() [已修复]
#   - get_bars() -> history_bars() [已修复]
#   - finance.STK_HK_HOLD_INFO (北向资金数据) [RQ无直接替代]
#   - talib.RSI() [JQ专属，无RQ替代]

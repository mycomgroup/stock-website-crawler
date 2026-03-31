"""
极简验证策略 - 测试 RiceQuant API
只打印数据，不做交易
"""


def init(context):
    logger.info("=== 策略初始化 ===")
    context.test_days = 0
    scheduler.run_daily(test_api, time_rule=market_open(minute=10))


def test_api(context, bar_dict):
    today = context.now.date()
    context.test_days += 1

    if context.test_days > 5:
        return

    logger.info(f"=== 测试第 {context.test_days} 天: {today} ===")

    # 测试获取所有股票
    all_inst = all_instruments("CS")
    stock_list = all_inst["order_book_id"].tolist()
    logger.info(f"股票总数: {len(stock_list)}")

    # 测试前10只股票的涨停情况
    test_stocks = stock_list[:10]
    for s in test_stocks:
        try:
            bars = history_bars(s, 3, "1d", ["close", "limit_up"])
            if bars is not None and len(bars) >= 2:
                close = bars[-1]["close"]
                limit = bars[-1]["limit_up"]
                prev_close = bars[-2]["close"]
                prev_limit = bars[-2]["limit_up"]

                is_zt_today = close >= limit * 0.99
                is_zt_prev = prev_close >= prev_limit * 0.99

                if is_zt_today:
                    logger.info(
                        f"  {s}: 今日涨停 (close={close:.2f}, limit={limit:.2f})"
                    )
                if is_zt_prev and not is_zt_today:
                    logger.info(f"  {s}: 昨日涨停今日未涨停 (可能二板)")
        except Exception as e:
            pass

    logger.info(f"=== 第 {context.test_days} 天测试完成 ===")


def after_trading(context):
    pass


__all__ = ["init", "test_api", "after_trading"]

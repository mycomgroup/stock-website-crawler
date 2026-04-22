# Simple Test - Verify RiceQuant API works


def init(context):
    scheduler.run_monthly(test_api, monthday=1)


def test_api(context, bar_dict):
    logger.info("=== Testing RiceQuant API ===")

    # Test index_components
    hs300 = index_components("000300.XSHG")
    logger.info(f"hs300 count: {len(hs300) if hs300 else 0}")

    # Test bar_dict
    if hs300:
        for stock in hs300[:5]:
            if stock in bar_dict:
                bar = bar_dict[stock]
                logger.info(
                    f"bar_dict[{stock}]: close={bar.close}, is_trading={bar.is_trading}"
                )
            else:
                logger.info(f"bar_dict[{stock}]: NOT FOUND")

    # Test history_bars
    try:
        hist = history_bars("000300.XSHG", 5, "1d", "close")
        logger.info(f"history_bars: {hist}")
    except Exception as e:
        logger.warning(f"history_bars failed: {e}")

    # Test get_factor
    if hs300:
        test_stocks = hs300[:3]
        try:
            factors = get_factor(test_stocks, ["roa", "pb_ratio"])
            logger.info(f"get_factor result: {factors}")
        except Exception as e:
            logger.warning(f"get_factor failed: {e}")

    # Test all_instruments
    try:
        all_inst = all_instruments(type="CS")
        logger.info(f"all_instruments type: {type(all_inst)}, count: {len(all_inst)}")
    except Exception as e:
        logger.warning(f"all_instruments failed: {e}")

    # Test instruments
    if hs300:
        try:
            inst = instruments(hs300[0])
            logger.info(f"instruments({hs300[0]}): symbol={inst.symbol}")
        except Exception as e:
            logger.warning(f"instruments failed: {e}")

    logger.info("=== Test Complete ===")

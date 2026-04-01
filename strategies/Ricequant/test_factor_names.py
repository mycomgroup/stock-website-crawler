# Test Factor Names in RiceQuant


def init(context):
    scheduler.run_monthly(test_factors, monthday=1)


def test_factors(context, bar_dict):
    stocks = index_components("000300.XSHG")[:5]

    # Test different factor names
    factor_tests = [
        ["roa"],
        ["return_on_asset"],
        ["return_on_equity"],
        ["roe"],
        ["pb_ratio"],
        ["pe_ratio"],
        ["market_cap"],
    ]

    for factors in factor_tests:
        try:
            data = get_factor(stocks, factors)
            logger.info(f"get_factor({factors}): {data}")
        except Exception as e:
            logger.warning(f"get_factor({factors}) failed: {e}")

    # Test get_fundamentals with fundamentals table
    try:
        q = query(
            fundamentals.eod_derivative_indicator.roa,
            fundamentals.eod_derivative_indicator.pb_ratio,
        )
        data = get_fundamentals(q)
        logger.info(f"get_fundamentals (eod_derivative_indicator): {data}")
    except Exception as e:
        logger.warning(f"get_fundamentals (eod_derivative_indicator) failed: {e}")

    # Test get_fundamentals with valuation
    try:
        q = query(
            valuation.code, valuation.pb_ratio, valuation.pe_ratio, valuation.market_cap
        )
        data = get_fundamentals(q)
        logger.info(f"get_fundamentals (valuation): {data}")
    except Exception as e:
        logger.warning(f"get_fundamentals (valuation) failed: {e}")

# Test strategy to verify API calls
from mindgo_api import *


def initialize(context):
    set_benchmark("000300.SH")
    g.test_results = []
    run_daily(run_tests, time_rule="after_open", hours=0, minutes=0)


def run_tests(context):
    prev_date = context.previous_date.strftime("%Y-%m-%d")

    # Test 1: get_all_securities
    try:
        all_stocks = get_all_securities(ty="stock", date=prev_date)
        log.info("Test 1: get_all_securities - count=%d" % len(all_stocks))
        g.test_results.append({"test": "get_all_securities", "count": len(all_stocks)})
    except Exception as e:
        log.info("Test 1 ERROR: %s" % str(e))
        g.test_results.append({"test": "get_all_securities", "error": str(e)})

    # Test 2: Filter stocks
    try:
        all_stocks = all_stocks.index.tolist() if hasattr(all_stocks, "index") else []
        filtered = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]
        log.info(
            "Test 2: Filtered stocks - before=%d after=%d"
            % (len(all_stocks), len(filtered))
        )
        g.test_results.append(
            {"test": "filter", "before": len(all_stocks), "after": len(filtered)}
        )
    except Exception as e:
        log.info("Test 2 ERROR: %s" % str(e))

    # Test 3: get_security_info
    try:
        if filtered:
            s = filtered[0]
            info = get_security_info(s)
            log.info(
                "Test 3: get_security_info(%s) - listed_date=%s"
                % (s, str(info.listed_date))
            )
            g.test_results.append(
                {
                    "test": "get_security_info",
                    "stock": s,
                    "listed_date": str(info.listed_date),
                }
            )
    except Exception as e:
        log.info("Test 3 ERROR: %s" % str(e))

    # Test 4: history
    try:
        if filtered:
            df = history(
                filtered[:100],  # Use first 100 to speed up
                ["close", "high_limit"],
                1,
                "1d",
                is_panel=False,
                fq="pre",
            )
            log.info(
                "Test 4: history - df_shape=%s"
                % str(df.shape if hasattr(df, "shape") else "N/A")
            )
            g.test_results.append(
                {
                    "test": "history",
                    "shape": str(df.shape if hasattr(df, "shape") else "N/A"),
                }
            )
    except Exception as e:
        log.info("Test 4 ERROR: %s" % str(e))

    # Test 5: get_current
    try:
        bar_dict = get_current(filtered[:10])
        log.info("Test 5: get_current - keys=%d" % len(bar_dict))
        g.test_results.append({"test": "get_current", "keys": len(bar_dict)})
    except Exception as e:
        log.info("Test 5 ERROR: %s" % str(e))

    # Log all test results at end
    log.info("ALL TESTS: %s" % str(g.test_results))

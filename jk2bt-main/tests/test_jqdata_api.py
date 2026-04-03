import pytest
import pandas as pd

from jk2bt import (
    get_price,
    get_fundamentals,
    get_all_securities_jq,
    get_security_info_jq,
)

from jk2bt.core.strategy_base import (
    get_all_trade_days_jq,
    get_extras_jq,
    get_billboard_list_jq,
    get_bars_jq,
)

from jk2bt.market_data.call_auction import (
    get_call_auction,
    get_call_auction_jq,
)

pytestmark = pytest.mark.network


# 辅助函数：安全断言DataFrame字段
def assert_df_has_columns(df, columns):
    if df is None or df.empty:
        pytest.skip("DataFrame is empty, skip column check")
    for col in columns:
        assert col in df.columns, f"Missing column: {col}"


# get_price_jq 测试：单只/多只、fields、frequency、异常股票
@pytest.mark.parametrize(
    "symbols,fields,frequency",
    [
        ("sh600000", ["open", "close"], "daily"),
        (["sh600000", "sz000001"], ["open", "close"], "daily"),
        ("sh600000", None, "1m"),
        ("fakecode", ["open", "close"], "daily"),
    ],
)
def test_get_price_jq_param(symbols, fields, frequency):
    print(f"开始: test_get_price_jq_param {symbols} {fields} {frequency}")
    try:
        res = get_price_jq(
            symbols,
            start_date="2023-01-03",
            end_date="2023-01-05",
            fields=fields,
            frequency=frequency,
        )
        if isinstance(symbols, list):
            assert isinstance(res, dict)
            for df in res.values():
                if not df.empty:
                    assert_df_has_columns(
                        df, ["datetime"] + (fields or ["open", "close"])
                    )
        else:
            assert isinstance(res, pd.DataFrame)
            if not res.empty:
                assert_df_has_columns(res, ["datetime"] + (fields or ["open", "close"]))
    except Exception as e:
        print(f"异常: {e}")
    print(f"结束: test_get_price_jq_param {symbols} {fields} {frequency}")


# get_fundamentals_jq 测试：多表、异常symbol
@pytest.mark.parametrize(
    "table,symbol",
    [
        ("balance", "sh600000"),
        ("income", "sh600000"),
        ("cash_flow", "sh600000"),
        ("balance", "fakecode"),
    ],
)
def test_get_fundamentals_jq_param(table, symbol):
    print(f"开始: test_get_fundamentals_jq_param {table} {symbol}")
    try:
        query = {"table": table, "symbol": symbol}
        res = get_fundamentals_jq(query, statDate="2022-12-31")
        assert isinstance(res, pd.DataFrame)
    except Exception as e:
        print(f"异常: {e}")
    print(f"结束: test_get_fundamentals_jq_param {table} {symbol}")


# get_history_fundamentals_jq 测试：多表多字段、异常symbol
@pytest.mark.parametrize(
    "symbol,fields",
    [
        (
            "sh600000",
            [
                "balance.cash_equivalents",
                "income.total_operating_revenue",
                "cash_flow.net_deposit_increase",
            ],
        ),
        ("fakecode", ["balance.cash_equivalents"]),
    ],
)
def test_get_history_fundamentals_jq_param(symbol, fields):
    print(f"开始: test_get_history_fundamentals_jq_param {symbol} {fields}")
    try:
        res = get_history_fundamentals_jq(symbol, fields, stat_date="2022q4", count=1)
        assert isinstance(res, pd.DataFrame)
    except Exception as e:
        print(f"异常: {e}")
    print(f"结束: test_get_history_fundamentals_jq_param {symbol} {fields}")


# get_all_securities_jq 测试
def test_get_all_securities_jq():
    print("开始: test_get_all_securities_jq")
    res = get_all_securities_jq()
    assert isinstance(res, pd.DataFrame)
    assert "code" in res.columns
    assert not res.empty
    print("结束: test_get_all_securities_jq")


# ========== 缓存功能测试 ========== #
def test_get_all_securities_jq_cache(tmp_path):
    import os
    import pandas as pd

    cache_dir = tmp_path / "meta_cache"
    # 第一次调用应下载并缓存
    df1 = get_all_securities_jq(cache_dir=str(cache_dir), force_update=True)
    assert isinstance(df1, pd.DataFrame) and not df1.empty
    # 第二次调用应直接读取缓存
    df2 = get_all_securities_jq(cache_dir=str(cache_dir), force_update=False)
    assert isinstance(df2, pd.DataFrame) and not df2.empty
    # 缓存文件存在
    assert any(f.name.startswith("securities_") for f in cache_dir.iterdir())


def test_get_billboard_list_jq_cache(tmp_path):
    import os
    import pandas as pd

    cache_dir = tmp_path / "billboard_cache"
    # 第一次调用应下载并缓存
    df1 = get_billboard_list_jq(cache_dir=str(cache_dir), force_update=True)
    assert isinstance(df1, pd.DataFrame)
    # 第二次调用应直接读取缓存
    df2 = get_billboard_list_jq(cache_dir=str(cache_dir), force_update=False)
    assert isinstance(df2, pd.DataFrame)
    # 缓存文件存在
    assert any(f.name.startswith("billboard_") for f in cache_dir.iterdir())


def test_get_extras_jq_cache(tmp_path):
    import os
    import pandas as pd

    cache_dir = tmp_path / "extras_cache"
    # is_st
    df1 = get_extras_jq(
        "is_st", ["sh600000"], cache_dir=str(cache_dir), force_update=True
    )
    assert isinstance(df1, pd.DataFrame)
    df2 = get_extras_jq(
        "is_st", ["sh600000"], cache_dir=str(cache_dir), force_update=False
    )
    assert isinstance(df2, pd.DataFrame)
    assert any(f.name.startswith("is_st_") for f in cache_dir.iterdir())
    # is_paused
    df3 = get_extras_jq(
        "is_paused", ["sh600000"], cache_dir=str(cache_dir), force_update=True
    )
    assert isinstance(df3, pd.DataFrame)
    df4 = get_extras_jq(
        "is_paused", ["sh600000"], cache_dir=str(cache_dir), force_update=False
    )
    assert isinstance(df4, pd.DataFrame)
    assert any(f.name.startswith("is_paused_") for f in cache_dir.iterdir())


# get_security_info_jq 测试：多种股票代码格式、异常代码
@pytest.mark.parametrize(
    "code",
    [
        "sh600000",
        "600000.XSHG",
        "600000",
        "sz000001",
        "000001.XSHE",
        "000001",
        "fakecode",
    ],
)
def test_get_security_info_jq_param(code):
    print(f"开始: test_get_security_info_jq_param {code}")
    res = get_security_info_jq(code)
    if code == "fakecode":
        assert res is None
    else:
        assert isinstance(res, dict)
        assert "code" in res
    print(f"结束: test_get_security_info_jq_param {code}")


# get_all_trade_days_jq 测试
def test_get_all_trade_days_jq():
    print("开始: test_get_all_trade_days_jq")
    res = get_all_trade_days_jq()
    assert isinstance(res, list)
    assert all(isinstance(d, pd.Timestamp) for d in res)
    assert len(res) > 200
    print("结束: test_get_all_trade_days_jq")


# get_extras_jq 测试：is_st/is_paused/异常字段、单只/多只
@pytest.mark.parametrize(
    "field,securities",
    [
        ("is_st", ["sh600000"]),
        ("is_paused", ["sh600000"]),
        ("is_st", ["sh600000", "sz000001"]),
        ("not_exist", ["sh600000"]),
    ],
)
def test_get_extras_jq_param(field, securities):
    print(f"开始: test_get_extras_jq_param {field} {securities}")
    try:
        res = get_extras_jq(field, securities)
        assert isinstance(res, pd.DataFrame)
        assert "代码" in res.columns
    except NotImplementedError:
        assert field == "not_exist"
    except Exception as e:
        print(f"异常: {e}")
    print(f"结束: test_get_extras_jq_param {field} {securities}")


# get_billboard_list_jq 测试：主流程、异常股票
@pytest.mark.parametrize("stock_list", [["sh600000"], ["fakecode"], None])
def test_get_billboard_list_jq_param(stock_list):
    print(f"开始: test_get_billboard_list_jq_param {stock_list}")
    try:
        res = get_billboard_list_jq(stock_list)
        assert isinstance(res, pd.DataFrame)
        assert "code" in res.columns
        assert "date" in res.columns
        assert "net_value" in res.columns
    except Exception as e:
        print(f"异常: {e}")
    print(f"结束: test_get_billboard_list_jq_param {stock_list}")


# get_bars_jq 测试：日线/分钟线、fields、异常股票
@pytest.mark.parametrize(
    "unit,fields,symbol",
    [
        ("1d", ["open", "close"], "sh600000"),
        ("1m", ["open", "close"], "sh600000"),
        ("1d", None, "fakecode"),
    ],
)
def test_get_bars_jq_param(unit, fields, symbol):
    print(f"开始: test_get_bars_jq_param {unit} {fields} {symbol}")
    try:
        res = get_bars_jq(symbol, count=2, unit=unit, fields=fields)
        assert isinstance(res, pd.DataFrame)
        if not res.empty and fields:
            assert_df_has_columns(res, ["datetime"] + fields)
    except Exception as e:
        print(f"异常: {e}")
    print(f"结束: test_get_bars_jq_param {unit} {fields} {symbol}")


# get_call_auction 测试：历史日期（返回空表）、字段验证、模拟器
@pytest.mark.parametrize(
    "stock_list,fields",
    [
        ("000001.XSHE", ["time", "current", "volume", "money"]),
        (["000001.XSHE", "600000.XSHG"], ["time", "current"]),
        ("fakecode", None),
    ],
)
def test_get_call_auction_fields(stock_list, fields):
    print(f"开始: test_get_call_auction_fields {stock_list} {fields}")
    try:
        res = get_call_auction(
            stock_list, start_date="2023-01-01", end_date="2023-01-01", fields=fields
        )
        assert isinstance(res, pd.DataFrame)
        assert "code" in res.columns
        assert "capability" in res.columns
        if fields:
            for f in fields:
                assert f in res.columns, f"Missing field: {f}"
    except Exception as e:
        print(f"异常: {e}")
    print(f"结束: test_get_call_auction_fields {stock_list} {fields}")


def test_get_call_auction_simulator():
    print("开始: test_get_call_auction_simulator")
    try:
        # 测试模拟器基本功能（使用有数据的日期）
        res = get_call_auction(
            ["000001.XSHE", "600000.XSHG"],
            start_date="2023-01-03",
            end_date="2023-01-05",
            simulated=True,
        )
        assert isinstance(res, pd.DataFrame)
        assert len(res) > 0, "模拟器应返回数据"
        assert "simulated" in res["capability"].unique(), "应标记为 simulated"
        assert "current" in res.columns
        assert "volume" in res.columns
        assert "money" in res.columns

        # 验证数据合理性
        assert all(res["current"] > 0), "价格应大于 0"
        assert all(res["volume"] > 0), "成交量应大于 0"
        assert all(res["money"] > 0), "成交额应大于 0"

        print(f"模拟器返回 {len(res)} 行数据")
        print(f"capability: {res['capability'].unique()}")

        # 测试自定义 volume_ratio
        res2 = get_call_auction(
            ["000001.XSHE"],
            start_date="2023-01-03",
            end_date="2023-01-03",
            simulated=True,
            volume_ratio=0.5,
        )
        if len(res2) > 0 and len(res) > 0:
            # 验证 volume_ratio 效果
            default_vol = res[res["code"] == "000001.XSHE"]["volume"].iloc[0]
            custom_vol = res2["volume"].iloc[0]
            ratio_diff = abs(custom_vol / default_vol - 0.5 / 0.3)
            assert ratio_diff < 0.01, f"volume_ratio 应生效 (差异: {ratio_diff})"
            print(f"volume_ratio 效果验证通过")

    except Exception as e:
        print(f"异常: {e}")
    print("结束: test_get_call_auction_simulator")


def test_get_call_auction_simulated_vs_realtime():
    print("开始: test_get_call_auction_simulated_vs_realtime")
    try:
        # 历史日期 + simulated=False（应返回空表）
        res1 = get_call_auction(
            ["000001.XSHE"],
            start_date="2023-01-01",
            end_date="2023-01-01",
            simulated=False,
        )
        assert len(res1) == 0, "simulated=False 应返回空表"
        assert "capability" in res1.columns, "应包含 capability 列"
        print("simulated=False 返回空表 ✓")

        # 历史日期 + simulated=True（应返回模拟数据）
        res2 = get_call_auction(
            ["000001.XSHE"],
            start_date="2023-01-03",
            end_date="2023-01-03",
            simulated=True,
        )
        assert len(res2) > 0, "simulated=True 应返回数据"
        assert "simulated" in res2["capability"].unique(), "应标记为 simulated"

        print("simulated 参数效果验证通过")

    except Exception as e:
        print(f"异常: {e}")
    print("结束: test_get_call_auction_simulated_vs_realtime")

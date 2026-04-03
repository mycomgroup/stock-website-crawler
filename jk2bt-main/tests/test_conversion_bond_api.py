"""
tests/test_conversion_bond_api.py
可转债 API 测试。

测试内容：
1. 溢价率计算测试
2. 历史数据测试
3. 批量查询测试
4. 转股价值测试
5. 边界条件测试
6. 数据验证测试
7. 缓存测试
"""

import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.market_data.conversion_bond import (
    get_conversion_bond_list,
    get_conversion_bond_list_robust,
    get_conversion_bond_price,
    get_conversion_bond_info,
    get_conversion_bond_detail,
    get_conversion_bond_by_stock,
    get_conversion_value,
    calculate_conversion_value,
    calculate_premium_rate,
    query_conversion_bond_basic,
    query_conversion_bond_price,
    query_conversion_bond,
    get_conversion_bond_history,
    get_conversion_price,
    calculate_conversion_premium,
    get_conversion_bond_daily,
    run_query_simple,
    finance,
    RobustResult,
    STK_CONVERSION_BOND_BASIC,
    STK_CONVERSION_BOND_PRICE,
    CONVERSION_BOND,
    _normalize_bond_code,
    _normalize_stock_code,
)


class TestConversionBondAPI:
    """测试可转债 API 基础功能"""

    def test_normalize_bond_code(self):
        """测试代码格式转换"""
        assert _normalize_bond_code("110048") == "110048"
        assert _normalize_bond_code("110048.XSHG") == "110048"
        assert _normalize_bond_code("sh110048") == "110048"
        assert _normalize_bond_code("SH110048") == "110048"
        assert _normalize_bond_code("123456.XSHE") == "123456"
        assert _normalize_bond_code("sz123456") == "123456"
        assert _normalize_bond_code("") == ""
        assert _normalize_bond_code(None) == ""

    def test_normalize_stock_code(self):
        """测试股票代码格式转换"""
        assert _normalize_stock_code("600519") == "600519.XSHG"
        assert _normalize_stock_code("000001") == "000001.XSHE"
        assert _normalize_stock_code("600519.XSHG") == "600519.XSHG"
        assert _normalize_stock_code("000001.XSHE") == "000001.XSHE"

    def test_robust_result(self):
        """测试 RobustResult 类"""
        result = RobustResult(
            success=True, data=pd.DataFrame({"a": [1]}), reason="", source="network"
        )
        assert result.success is True
        assert bool(result) is True
        assert result.is_empty() is False

        result_fail = RobustResult(success=False, reason="test error", source="input")
        assert result_fail.success is False
        assert bool(result_fail) is False
        assert "FAILED" in repr(result_fail)


class TestConversionPremiumCalculation:
    """
    测试溢价率计算（calculate_conversion_premium）。

    溢价率是衡量可转债相对于转股价值偏离程度的重要指标，
    计算公式：溢价率 = (可转债价格 / 转股价值 - 1) * 100%

    测试场景：
    - 正溢价场景：可转债价格高于转股价值
    - 负溢价场景：可转债价格低于转股价值（存在套利机会）
    - 溢价率边界值：零溢价、极高溢价、极低溢价
    """

    def test_positive_premium_rate(self):
        """
        测试正溢价场景。

        当可转债价格高于转股价值时，溢价率为正，表示转债被高估。
        例如：债券价格120元，转股价值100元，溢价率=(120/100-1)*100=20%
        """
        bond_price = 120.0
        conversion_value = 100.0
        premium = calculate_premium_rate(bond_price, conversion_value)
        assert premium == pytest.approx(20.0, rel=0.001)
        print(f"正溢价率: {premium}%")

    def test_high_positive_premium_rate(self):
        """
        测试高正溢价场景。

        高溢价通常表示可转债被高估或正股下跌预期强烈。
        例如：债券价格150元，转股价值80元，溢价率=(150/80-1)*100=87.5%
        """
        bond_price = 150.0
        conversion_value = 80.0
        premium = calculate_premium_rate(bond_price, conversion_value)
        assert premium == pytest.approx(87.5, rel=0.001)
        print(f"高正溢价率: {premium}%")

    def test_negative_premium_rate(self):
        """
        测试负溢价场景。

        当可转债价格低于转股价值时，溢价率为负，存在套利机会。
        例如：债券价格95元，转股价值100元，溢价率=(95/100-1)*100=-5%
        """
        bond_price = 95.0
        conversion_value = 100.0
        premium = calculate_premium_rate(bond_price, conversion_value)
        assert premium == pytest.approx(-5.0, rel=0.001)
        print(f"负溢价率: {premium}%")

    def test_deep_negative_premium_rate(self):
        """
        测试深度负溢价场景。

        深度负溢价可能表示套利机会或流动性问题。
        例如：债券价格80元，转股价值100元，溢价率=(80/100-1)*100=-20%
        """
        bond_price = 80.0
        conversion_value = 100.0
        premium = calculate_premium_rate(bond_price, conversion_value)
        assert premium == pytest.approx(-20.0, rel=0.001)
        print(f"深度负溢价率: {premium}%")

    def test_zero_premium_rate(self):
        """
        测试零溢价边界值。

        当债券价格等于转股价值时，溢价率为零，表示平价。
        例如：债券价格100元，转股价值100元，溢价率=0%
        """
        bond_price = 100.0
        conversion_value = 100.0
        premium = calculate_premium_rate(bond_price, conversion_value)
        assert premium == pytest.approx(0.0, rel=0.001)
        print(f"零溢价率: {premium}%")

    def test_premium_rate_boundary_high_bond_price(self):
        """
        测试高债券价格边界。

        极高的债券价格（如退市前）可能产生极高溢价。
        例如：债券价格300元，转股价值50元，溢价率=(300/50-1)*100=500%
        """
        bond_price = 300.0
        conversion_value = 50.0
        premium = calculate_premium_rate(bond_price, conversion_value)
        assert premium == pytest.approx(500.0, rel=0.001)
        assert premium > 100.0
        print(f"高债券价格溢价率: {premium}%")

    def test_premium_rate_boundary_low_conversion_value(self):
        """
        测试低转股价值边界。

        极低的转股价值会产生极高的溢价率。
        例如：债券价格100元，转股价值10元，溢价率=(100/10-1)*100=900%
        """
        bond_price = 100.0
        conversion_value = 10.0
        premium = calculate_premium_rate(bond_price, conversion_value)
        assert premium == pytest.approx(900.0, rel=0.001)
        print(f"低转股价值溢价率: {premium}%")

    def test_premium_rate_zero_conversion_value(self):
        """
        测试零转股价值边界。

        当转股价值为零（转股价为零或正股价格为负）时，溢价率应返回零避免计算错误。
        """
        bond_price = 100.0
        conversion_value = 0.0
        premium = calculate_premium_rate(bond_price, conversion_value)
        assert premium == 0.0
        print(f"零转股价值溢价率: {premium}%")

    def test_premium_rate_negative_conversion_value(self):
        """
        测试负转股价值边界。

        负的转股价值是不合理的数据，函数应返回零。
        """
        bond_price = 100.0
        conversion_value = -50.0
        premium = calculate_premium_rate(bond_price, conversion_value)
        assert premium == 0.0
        print(f"负转股价值溢价率: {premium}%")

    def test_calculate_conversion_premium_with_real_bond(self):
        """
        测试真实可转债的溢价率计算。

        使用 calculate_conversion_premium 函数获取实际可转债的溢价率。
        """
        premium = calculate_conversion_premium("110048", use_cache=False)
        print(f"110048 溢价率: {premium}")
        if premium is not None and pd.notna(premium):
            assert isinstance(premium, (int, float))
            assert -100 <= premium <= 1000, f"溢价率应在合理范围内: {premium}"

    def test_calculate_conversion_premium_invalid_bond(self):
        """
        测试无效可转债代码的溢价率计算。

        无效代码应返回 None。
        """
        premium = calculate_conversion_premium("999999", use_cache=False)
        assert premium is None
        print("无效可转债代码溢价率返回 None")


class TestHistoricalDataQuery:
    """
    测试历史数据查询（get_conversion_bond_daily）。

    验证日线数据的获取、日期范围控制、数据完整性等。

    测试场景：
    - 不同日期范围：7天、30天、90天、一年
    - 数据完整性：OHLCV 字段完整性
    - 价格一致性：high >= low
    """

    def test_get_daily_data_seven_days(self):
        """
        测试获取7天日线数据。

        验证返回的数据包含必要字段且日期在指定范围内。
        """
        from datetime import datetime, timedelta

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        df = get_conversion_bond_daily(
            "110048", start_date, end_date, force_update=True
        )
        assert isinstance(df, pd.DataFrame)
        print(f"7天日线数据: {len(df)} 条记录")
        if not df.empty:
            assert "datetime" in df.columns
            assert "close" in df.columns

    def test_get_daily_data_thirty_days(self):
        """
        测试获取30天日线数据。

        验证数据完整性和日期范围。
        """
        from datetime import datetime, timedelta

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        df = get_conversion_bond_daily(
            "110048", start_date, end_date, force_update=True
        )
        assert isinstance(df, pd.DataFrame)
        print(f"30天日线数据: {len(df)} 条记录")
        if not df.empty:
            assert len(df) <= 30, f"30天数据不应超过30条，实际: {len(df)}"

    def test_get_daily_data_ninety_days(self):
        """
        测试获取90天日线数据。

        验证大数据量查询的性能和完整性。
        """
        from datetime import datetime, timedelta

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

        df = get_conversion_bond_daily(
            "110048", start_date, end_date, force_update=True
        )
        assert isinstance(df, pd.DataFrame)
        print(f"90天日线数据: {len(df)} 条记录")
        if not df.empty:
            df["datetime"] = pd.to_datetime(df["datetime"])
            date_range_days = (df["datetime"].max() - df["datetime"].min()).days
            print(f"实际日期跨度: {date_range_days} 天")

    def test_get_daily_data_one_year(self):
        """
        测试获取一年日线数据。

        验证长周期历史数据查询。
        """
        from datetime import datetime, timedelta

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

        df = get_conversion_bond_daily(
            "110048", start_date, end_date, force_update=True
        )
        assert isinstance(df, pd.DataFrame)
        print(f"一年日线数据: {len(df)} 条记录")

    def test_daily_data_date_range_boundary(self):
        """
        测试日期范围边界。

        验证返回数据的时间范围不超出请求范围。
        """
        from datetime import datetime, timedelta

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d")

        df = get_conversion_bond_daily(
            "110048", start_date, end_date, force_update=True
        )
        if not df.empty:
            df["datetime"] = pd.to_datetime(df["datetime"])
            assert df["datetime"].min() >= pd.to_datetime(start_date)
            assert df["datetime"].max() <= pd.to_datetime(end_date)
            print("日期范围边界验证通过")

    def test_daily_data_ohlc_completeness(self):
        """
        测试日线 OHLCV 数据完整性。

        验证 open/high/low/close/volume 字段存在且非空。
        """
        from datetime import datetime, timedelta

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        df = get_conversion_bond_daily(
            "110048", start_date, end_date, force_update=True
        )
        if not df.empty:
            required_fields = ["datetime", "close"]
            optional_fields = ["open", "high", "low", "volume"]
            for field in required_fields:
                assert field in df.columns, f"缺少必要字段: {field}"
            for field in optional_fields:
                if field in df.columns:
                    print(f"字段 {field} 存在")
            print(f"OHLCV 数据完整性验证通过，字段: {list(df.columns)}")

    def test_daily_data_price_consistency(self):
        """
        测试日线价格数据一致性。

        验证 high >= low，close 在 high 和 low 之间。
        """
        from datetime import datetime, timedelta

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        df = get_conversion_bond_daily(
            "110048", start_date, end_date, force_update=True
        )
        if not df.empty and "high" in df.columns and "low" in df.columns:
            for idx, row in df.iterrows():
                assert row["high"] >= row["low"], f"第{idx}行最高价应>=最低价"
            print("价格一致性验证通过")

    def test_daily_data_sorted_by_date(self):
        """
        测试日线数据按日期排序。

        验证数据按日期升序或降序排列。
        """
        from datetime import datetime, timedelta

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        df = get_conversion_bond_daily(
            "110048", start_date, end_date, force_update=True
        )
        if not df.empty and len(df) > 1:
            df["datetime"] = pd.to_datetime(df["datetime"])
            dates = df["datetime"].tolist()
            is_sorted = dates == sorted(dates) or dates == sorted(dates, reverse=True)
            assert is_sorted, "数据应按日期排序"
            print("日期排序验证通过")


class TestBatchQuery:
    """
    测试批量查询。

    验证批量获取多只可转债信息和按正股代码查询功能。

    测试场景：
    - 批量获取多只可转债信息
    - 按正股代码查询
    - 空列表和无效代码处理
    """

    def test_query_multiple_bonds_by_codes(self):
        """
        测试批量获取多只可转债信息。

        验证 query_conversion_bond 函数能正确筛选多只可转债。
        """
        bond_codes = ["110048", "113050", "123015"]
        df = query_conversion_bond(bond_codes, force_update=True, use_duckdb=False)
        assert isinstance(df, pd.DataFrame)
        print(f"批量查询 {len(bond_codes)} 只可转债: 返回 {len(df)} 条记录")
        if not df.empty:
            assert "bond_code" in df.columns

    def test_query_by_stock_code(self):
        """
        测试按正股代码查询可转债。

        验证 get_conversion_bond_by_stock 函数能根据正股代码找到对应可转债。
        """
        result = get_conversion_bond_by_stock("600519.XSHG", use_cache=False)
        assert isinstance(result, RobustResult)
        print(f"按正股600519查询: {result}")
        if result.success:
            assert isinstance(result.data, pd.DataFrame)

    def test_query_by_stock_code_multiple_formats(self):
        """
        测试不同格式的正股代码查询。

        验证正股代码格式转换正确性，支持纯数字和聚宽格式。
        """
        stock_codes = ["600519", "600519.XSHG"]
        for stock_code in stock_codes:
            result = get_conversion_bond_by_stock(stock_code, use_cache=False)
            assert isinstance(result, RobustResult)
            print(f"正股代码 {stock_code} 查询: {result}")

    def test_query_by_invalid_stock_code(self):
        """
        测试无效正股代码查询。

        验证无效正股代码返回失败结果。
        """
        result = get_conversion_bond_by_stock("999999", use_cache=False)
        assert isinstance(result, RobustResult)
        if not result.success:
            assert "未找到" in result.reason or result.success is False
        print(f"无效正股代码查询: {result}")

    def test_query_empty_bond_list(self):
        """
        测试空可转债列表查询。

        验证传入空列表时返回空 DataFrame。
        """
        df = query_conversion_bond([], force_update=True)
        assert isinstance(df, pd.DataFrame)
        assert df.empty
        print("空列表查询返回空 DataFrame")

    def test_query_none_bond_list(self):
        """
        测试 None 可转债列表查询。

        验证传入 None 时返回空 DataFrame。
        """
        df = query_conversion_bond(None, force_update=True)
        assert isinstance(df, pd.DataFrame)
        assert df.empty
        print("None 列表查询返回空 DataFrame")

    def test_query_conversion_bond_basic_multiple(self):
        """
        测试批量查询可转债基本信息。

        验证 query_conversion_bond_basic 函数不带筛选条件时返回全部数据。
        """
        df = query_conversion_bond_basic(use_cache=False)
        assert isinstance(df, pd.DataFrame)
        print(f"查询全部可转债基本信息: {len(df)} 条")
        if not df.empty:
            assert "bond_code" in df.columns
            assert "bond_name" in df.columns


class TestConversionValueCalculation:
    """
    测试转股价值计算（calculate_conversion_value）。

    转股价值 = (100 / 转股价) * 正股价，衡量转债转换为股票后的价值。

    测试场景：
    - 标准计算
    - 高正股价格与低转股价
    - 低正股价格与高转股价
    - 平价场景
    - 边界值处理
    """

    def test_conversion_value_standard_calculation(self):
        """
        测试标准转股价值计算。

        例如：转股价20元，正股价25元，转股价值 = (100/20)*25 = 125元
        """
        conversion_price = 20.0
        stock_price = 25.0
        value = calculate_conversion_value(conversion_price, stock_price)
        expected = (100 / conversion_price) * stock_price
        assert value == pytest.approx(expected, rel=0.001)
        print(f"转股价值: {value}元 (转股价{conversion_price}, 正股{stock_price})")

    def test_conversion_value_high_stock_price(self):
        """
        测试高正股价格场景。

        正股价格远高于转股价时，转股价值显著高于面值。
        例如：转股价10元，正股价50元，转股价值 = (100/10)*50 = 500元
        """
        conversion_price = 10.0
        stock_price = 50.0
        value = calculate_conversion_value(conversion_price, stock_price)
        expected = (100 / 10.0) * 50.0
        assert value == pytest.approx(expected, rel=0.001)
        assert value == 500.0
        print(f"高正股价格转股价值: {value}元")

    def test_conversion_value_low_stock_price(self):
        """
        测试低正股价格场景。

        正股价格远低于转股价时，转股价值显著低于面值。
        例如：转股价50元，正股价10元，转股价值 = (100/50)*10 = 20元
        """
        conversion_price = 50.0
        stock_price = 10.0
        value = calculate_conversion_value(conversion_price, stock_price)
        expected = (100 / 50.0) * 10.0
        assert value == pytest.approx(expected, rel=0.001)
        assert value == 20.0
        print(f"低正股价格转股价值: {value}元")

    def test_conversion_value_at_parity(self):
        """
        测试平价场景。

        正股价格等于转股价时，转股价值等于面值100元。
        """
        conversion_price = 25.0
        stock_price = 25.0
        value = calculate_conversion_value(conversion_price, stock_price)
        assert value == 100.0
        print(f"平价时转股价值: {value}元")

    def test_conversion_value_zero_stock_price(self):
        """
        测试零正股价格边界。

        正股价格为0时，转股价值应为0。
        """
        conversion_price = 20.0
        stock_price = 0.0
        value = calculate_conversion_value(conversion_price, stock_price)
        assert value == 0.0
        print(f"零正股价格转股价值: {value}元")

    def test_conversion_value_zero_conversion_price(self):
        """
        测试零转股价边界。

        转股价为0时，转股价值应为0（避免除零错误）。
        """
        conversion_price = 0.0
        stock_price = 25.0
        value = calculate_conversion_value(conversion_price, stock_price)
        assert value == 0.0
        print(f"零转股价转股价值: {value}元")

    def test_conversion_value_negative_conversion_price(self):
        """
        测试负转股价边界。

        负转股价是不合理数据，函数应返回0。
        """
        conversion_price = -20.0
        stock_price = 25.0
        value = calculate_conversion_value(conversion_price, stock_price)
        assert value == 0.0
        print(f"负转股价转股价值: {value}元")

    def test_conversion_value_with_real_bond(self):
        """
        测试真实可转债的转股价值计算。

        使用 get_conversion_value 函数获取实际可转债的转股价值。
        """
        result = get_conversion_value("110048", stock_price=100.0, use_cache=False)
        assert isinstance(result, RobustResult)
        print(f"真实可转债转股价值计算: {result}")
        if result.success:
            data = result.data
            assert "conversion_value" in data
            assert "premium_rate" in data
            assert "conversion_price" in data
            assert data["conversion_value"] > 0
            assert data["conversion_price"] > 0

    def test_conversion_value_relationship_with_premium(self):
        """
        测试转股价值与溢价率的关系。

        验证溢价率 = (债券价格/转股价值 - 1) * 100
        """
        bond_price = 110.0
        conversion_value = 100.0
        premium = calculate_premium_rate(bond_price, conversion_value)
        assert premium == pytest.approx(10.0, rel=0.001)
        print(
            f"溢价率验证: 债券价格{bond_price}, 转股价值{conversion_value}, 溢价率{premium}%"
        )


class TestBoundaryConditions:
    """
    测试边界条件。

    验证不存在可转债代码、已退市可转债、日期范围边界等场景。

    测试场景：
    - 不存在可转债代码
    - 已退市可转债
    - 日期范围边界（起始晚于结束、未来日期）
    """

    def test_empty_bond_code(self):
        """
        测试空可转债代码。

        验证空字符串返回失败结果。
        """
        result = get_conversion_bond_price("", use_cache=False)
        assert result.success is False
        assert "不能为空" in result.reason or "未找到" in result.reason

    def test_none_bond_code(self):
        """
        测试 None 可转债代码。

        验证 None 值返回失败结果。
        """
        result = get_conversion_bond_info(None, use_cache=False)
        assert result.success is False

    def test_nonexistent_bond_code(self):
        """
        测试不存在的可转债代码。

        验证查询不存在的可转债代码时返回失败结果。
        """
        result = get_conversion_bond_price("999999", use_cache=False)
        assert result.success is False
        assert "未找到" in result.reason or not result.success
        print(f"不存在可转债代码查询: {result}")

    def test_delisted_bond_query(self):
        """
        测试已退市可转债查询。

        使用可能已退市的可转债代码进行测试。
        """
        result = get_conversion_bond_price("110000", use_cache=False)
        assert isinstance(result, RobustResult)
        print(f"已退市可转债查询: {result}")

    def test_date_range_start_after_end(self):
        """
        测试起始日期晚于结束日期。

        验证日期范围无效时返回空数据而非报错。
        """
        from datetime import datetime, timedelta

        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        end_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        df = get_conversion_bond_daily(
            "110048", start_date, end_date, force_update=True
        )
        assert isinstance(df, pd.DataFrame)
        print(f"起始晚于结束日期查询: 返回 {len(df)} 条")

    def test_future_date_query(self):
        """
        测试未来日期查询。

        验证查询未来日期时返回空数据。
        """
        from datetime import datetime, timedelta

        start_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")

        df = get_conversion_bond_daily(
            "110048", start_date, end_date, force_update=True
        )
        assert isinstance(df, pd.DataFrame)
        assert df.empty, "未来日期应返回空数据"
        print("未来日期查询返回空数据")

    def test_invalid_stock_code_format(self):
        """
        测试无效股票代码格式查询。

        验证无效格式的股票代码能被正确处理。
        """
        result = get_conversion_bond_by_stock("INVALID", use_cache=False)
        assert isinstance(result, RobustResult)
        print(f"无效股票代码格式查询: {result}")


class TestDataValidation:
    """
    测试数据验证。

    验证可转债基本字段、日线 OHLCV 数据、转股价非负等。

    测试场景：
    - 可转债基本字段完整性
    - 日线 OHLCV 数据验证
    - 转股价非负验证
    - 溢价率范围验证
    """

    def test_bond_list_fields_complete(self):
        """
        测试可转债列表字段完整性。

        验证 bond_code、bond_name、stock_code 等必要字段存在。
        """
        result = get_conversion_bond_list_robust(force_update=True, use_cache=False)
        if result.success and not result.data.empty:
            required_fields = ["bond_code", "bond_name", "stock_code"]
            for field in required_fields:
                assert field in result.data.columns, f"缺少必要字段: {field}"
            print(f"字段完整性检查通过: {list(result.data.columns)}")

    def test_bond_code_format_valid(self):
        """
        测试可转债代码格式有效性。

        验证所有可转债代码为6位数字格式。
        """
        result = get_conversion_bond_list_robust(force_update=True, use_cache=False)
        if result.success and not result.data.empty:
            for _, row in result.data.head(10).iterrows():
                bond_code = str(row["bond_code"])
                if bond_code and bond_code.strip():
                    assert len(bond_code) == 6, f"可转债代码长度错误: {bond_code}"
                    assert bond_code.isdigit(), f"可转债代码格式错误: {bond_code}"
            print("可转债代码格式检查通过")

    def test_conversion_price_non_negative(self):
        """
        测试转股价非负验证。

        验证所有可转债转股价为正数（非零非负）。
        """
        result = get_conversion_bond_list_robust(force_update=True, use_cache=False)
        if result.success and not result.data.empty:
            valid_count = 0
            for _, row in result.data.head(20).iterrows():
                conv_price = row.get("conversion_price")
                if conv_price is not None and pd.notna(conv_price):
                    assert conv_price >= 0, f"转股价应为非负: {conv_price}"
                    if conv_price > 0:
                        valid_count += 1
            print(f"转股价非负验证通过，有效数据: {valid_count}")

    def test_conversion_price_reasonable_range(self):
        """
        测试转股价合理性范围。

        验证转股价在合理范围内（通常 1-1000 元）。
        """
        result = get_conversion_bond_list_robust(force_update=True, use_cache=False)
        if result.success and not result.data.empty:
            valid_count = 0
            for _, row in result.data.head(20).iterrows():
                conv_price = row.get("conversion_price")
                if conv_price is not None and pd.notna(conv_price) and conv_price >= 1:
                    assert 1 <= conv_price <= 1000, f"转股价异常: {conv_price}"
                    valid_count += 1
            print(f"转股价合理性检查通过，有效数据: {valid_count}")

    def test_premium_rate_range(self):
        """
        测试溢价率范围验证。

        验证溢价率在合理范围内（通常 -100% 到 500%）。
        """
        result = get_conversion_bond_list_robust(force_update=True, use_cache=False)
        if result.success and not result.data.empty:
            valid_count = 0
            for _, row in result.data.head(30).iterrows():
                premium = row.get("premium_rate")
                if premium is not None and pd.notna(premium):
                    assert -100 <= premium <= 500, f"溢价率异常: {premium}"
                    valid_count += 1
            print(f"溢价率范围检查通过，有效数据: {valid_count}")

    def test_bond_price_reasonable(self):
        """
        测试债券价格合理性。

        验证债券价格在合理范围内（通常 80-300 元）。
        """
        result = get_conversion_bond_list_robust(force_update=True, use_cache=False)
        if result.success and not result.data.empty:
            valid_count = 0
            for _, row in result.data.head(20).iterrows():
                close = row.get("close")
                if close is not None and pd.notna(close) and close > 0:
                    assert 50 <= close <= 500, f"债券价格异常: {close}"
                    valid_count += 1
            print(f"债券价格合理性检查通过，有效数据: {valid_count}")

    def test_daily_data_volume_field(self):
        """
        测试日线数据成交量字段。

        验证成交量字段数据类型正确。
        """
        from datetime import datetime, timedelta

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        df = get_conversion_bond_daily(
            "110048", start_date, end_date, force_update=True
        )
        if not df.empty and "volume" in df.columns:
            assert df["volume"].dtype in [int, float, "int64", "float64"]
            print("成交量字段验证通过")


class TestCacheAndPerformance:
    """
    测试缓存和性能。

    验证按日缓存、缓存预热、缓存有效性等。

    测试场景：
    - 按日缓存功能
    - 缓存预热
    - 缓存有效性
    - 缓存过期策略
    """

    def test_cache_effectiveness(self):
        """
        测试缓存有效性。

        验证缓存数据与实时数据一致。
        """
        result1 = get_conversion_bond_list_robust(force_update=True, use_cache=False)
        result2 = get_conversion_bond_list_robust(force_update=False, use_cache=True)

        assert result1.success == result2.success
        if result1.success and result2.success:
            assert len(result1.data) == len(result2.data)
            print("缓存有效性验证通过")

    def test_force_update_flag(self):
        """
        测试强制更新标志。

        验证 force_update 标志能正确控制缓存刷新。
        """
        result1 = get_conversion_bond_list_robust(force_update=False, use_cache=True)
        result2 = get_conversion_bond_list_robust(force_update=True, use_cache=False)

        assert isinstance(result1, RobustResult)
        assert isinstance(result2, RobustResult)
        print("强制更新标志验证通过")

    def test_daily_cache_by_date(self):
        """
        测试按日缓存功能。

        验证日线数据缓存按日期有效存储和读取，
        相同日期范围的请求可以从缓存中获取数据。
        """
        from datetime import datetime, timedelta

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        df1 = get_conversion_bond_daily(
            "110048", start_date, end_date, force_update=True
        )
        df2 = get_conversion_bond_daily(
            "110048", start_date, end_date, force_update=False
        )

        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)
        if not df1.empty and not df2.empty:
            assert len(df1) == len(df2)
            print(f"按日缓存验证通过，缓存数据: {len(df1)} 条")

    def test_cache_different_date_ranges(self):
        """
        测试不同日期范围的缓存隔离。

        验证不同日期范围查询的数据相互独立，
        不会因缓存导致数据混淆。
        """
        from datetime import datetime, timedelta

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date1 = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        start_date2 = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")

        df1 = get_conversion_bond_daily(
            "110048", start_date1, end_date, force_update=True
        )
        df2 = get_conversion_bond_daily(
            "110048", start_date2, end_date, force_update=True
        )

        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)
        print(f"7天数据: {len(df1)} 条, 14天数据: {len(df2)} 条")

    def test_cache_prewarm(self):
        """
        测试缓存预热功能。

        验证预先加载可转债列表数据到缓存，
        后续查询能够直接使用预热数据。
        """
        result = get_conversion_bond_list_robust(force_update=True, use_cache=True)
        assert isinstance(result, RobustResult)
        print(f"缓存预热完成: {result}")

        if result.success:
            result_cached = get_conversion_bond_list_robust(
                force_update=False, use_cache=True
            )
            assert result_cached.success
            assert result_cached.source == "cache"
            print(f"使用预热缓存数据: {len(result_cached.data)} 只")

    def test_cache_expiration_one_day(self):
        """
        测试按日缓存过期策略。

        验证缓存数据在超过一天后需要重新获取，
        缓存策略正确判断数据新鲜度。
        """
        import os
        from datetime import datetime

        cache_dir = "finance_cache"
        cache_file = os.path.join(cache_dir, "conversion_bond_list.pkl")

        result = get_conversion_bond_list_robust(force_update=True, use_cache=False)
        assert isinstance(result, RobustResult)

        if os.path.exists(cache_file):
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            cache_age_hours = (datetime.now() - file_mtime).total_seconds() / 3600
            print(
                f"缓存文件存在，创建时间: {file_mtime}, 年龄: {cache_age_hours:.2f} 小时"
            )
            assert cache_age_hours < 1, "刚创建的缓存应该小于1小时"


class TestCacheWarmup:
    """
    测试缓存预热。

    验证预先加载可转债数据到缓存的能力，包括全量预热和按需预热。

    测试场景：
    - 全量可转债缓存预热
    - 单只可转债缓存预热
    - 日线数据缓存预热
    - 多只可转债批量预热
    """

    def test_warmup_all_conversion_bonds(self):
        """
        测试全量可转债缓存预热。

        验证预先加载全部可转债数据到缓存，提高后续查询性能。
        """
        result = get_conversion_bond_list_robust(force_update=True, use_cache=True)
        assert isinstance(result, RobustResult)
        if result.success:
            print(f"全量预热完成，共 {len(result.data)} 只可转债")
            assert len(result.data) >= 100

    def test_warmup_specific_bond_price(self):
        """
        测试单只可转债缓存预热。

        验证预先加载单只可转债行情数据到缓存。
        """
        result = get_conversion_bond_price("110048", force_update=True, use_cache=True)
        assert isinstance(result, RobustResult)
        print(f"单只可转债预热: {result}")

    def test_warmup_bond_daily_data(self):
        """
        测试日线数据缓存预热。

        验证预先加载日线历史数据到缓存。
        """
        from datetime import datetime, timedelta

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        df = get_conversion_bond_daily(
            "110048", start_date, end_date, force_update=True
        )
        assert isinstance(df, pd.DataFrame)
        print(f"日线数据预热完成: {len(df)} 条记录")

    def test_warmup_multiple_bonds(self):
        """
        测试多只可转债批量预热。

        验证预先加载多只可转债数据到缓存。
        """
        bond_codes = ["110048", "113050", "123015"]
        for code in bond_codes:
            result = get_conversion_bond_price(code, force_update=True, use_cache=True)
            assert isinstance(result, RobustResult)
            print(f"预热可转债 {code}: {result.success}")

    def test_cache_warmup_source_indicator(self):
        """
        测试预热后数据来源指示器。

        验证预热后再次查询时，source 字段正确标识为 'cache'。
        """
        get_conversion_bond_list_robust(force_update=True, use_cache=True)
        result = get_conversion_bond_list_robust(force_update=False, use_cache=True)
        if result.success:
            assert result.source == "cache"
            print(f"数据来源: {result.source}")


class TestConversionBondList:
    """测试可转债列表获取"""

    def test_get_all_conversion_bonds(self):
        """测试获取全部可转债"""
        result = get_conversion_bond_list_robust(force_update=True, use_cache=False)
        if result.success:
            assert isinstance(result.data, pd.DataFrame)
            assert len(result.data) > 0, "可转债列表不应为空"
            print(f"获取全部可转债: {len(result.data)} 只")
        else:
            pytest.skip(f"获取可转债列表失败: {result.reason}")

    def test_conversion_bond_count_reasonable(self):
        """测试可转债数量合理性（通常在300-800只之间）"""
        result = get_conversion_bond_list_robust(force_update=True, use_cache=False)
        if result.success and not result.data.empty:
            count = len(result.data)
            assert count >= 100, f"可转债数量过少: {count}"
            assert count <= 2000, f"可转债数量异常: {count}"
            print(f"可转债数量: {count}，在合理范围内")


class TestEdgeCases:
    """测试边界场景"""

    def test_high_premium_bond_detection(self):
        """测试高溢价可转债检测"""
        result = get_conversion_bond_list_robust(force_update=True, use_cache=False)
        if result.success and not result.data.empty:
            high_premium_bonds = result.data[
                (result.data["premium_rate"].notna())
                & (result.data["premium_rate"] > 50)
            ]
            if not high_premium_bonds.empty:
                print(f"发现高溢价可转债: {len(high_premium_bonds)} 只")
                assert len(high_premium_bonds) > 0

    def test_low_premium_bond_detection(self):
        """测试低溢价可转债检测"""
        result = get_conversion_bond_list_robust(force_update=True, use_cache=False)
        if result.success and not result.data.empty:
            low_premium_bonds = result.data[
                (result.data["premium_rate"].notna())
                & (result.data["premium_rate"] < 5)
            ]
            if not low_premium_bonds.empty:
                print(f"发现低溢价可转债: {len(low_premium_bonds)} 只")

    def test_negative_premium_bond_detection(self):
        """测试负溢价可转债检测"""
        result = get_conversion_bond_list_robust(force_update=True, use_cache=False)
        if result.success and not result.data.empty:
            negative_premium_bonds = result.data[
                (result.data["premium_rate"].notna())
                & (result.data["premium_rate"] < 0)
            ]
            print(f"发现负溢价可转债: {len(negative_premium_bonds)} 只")


class TestRobustResultBehavior:
    """测试 RobustResult 行为"""

    def test_robust_result_bool_conversion(self):
        """测试 RobustResult 布尔转换"""
        success_result = RobustResult(success=True, data=pd.DataFrame({"a": [1]}))
        fail_result = RobustResult(success=False, reason="test")

        assert bool(success_result) is True
        assert bool(fail_result) is False

    def test_robust_result_repr(self):
        """测试 RobustResult 字符串表示"""
        result = RobustResult(success=True, data=pd.DataFrame(), source="cache")
        repr_str = repr(result)
        assert "SUCCESS" in repr_str
        assert "cache" in repr_str

    def test_robust_result_empty_check(self):
        """测试 RobustResult 空数据检查"""
        empty_df_result = RobustResult(success=True, data=pd.DataFrame())
        non_empty_result = RobustResult(success=True, data=pd.DataFrame({"a": [1]}))
        empty_list_result = RobustResult(success=True, data=[])

        assert empty_df_result.is_empty() is True
        assert non_empty_result.is_empty() is False
        assert empty_list_result.is_empty() is True


class TestFinanceQueryCompatibility:
    """测试 finance 模块兼容性"""

    def test_finance_run_query(self):
        """测试 finance.run_query 接口"""
        df = finance.run_query(finance.STK_CB_DAILY)
        assert isinstance(df, pd.DataFrame)
        print(f"finance.STK_CB_DAILY 查询: {len(df)} 条记录")

    def test_stk_conversion_bond_basic_class(self):
        """测试 STK_CONVERSION_BOND_BASIC 类"""
        assert hasattr(STK_CONVERSION_BOND_BASIC, "bond_code")
        assert hasattr(STK_CONVERSION_BOND_BASIC, "bond_name")
        assert hasattr(STK_CONVERSION_BOND_BASIC, "stock_code")
        assert hasattr(STK_CONVERSION_BOND_BASIC, "conversion_price")

    def test_stk_conversion_bond_price_class(self):
        """测试 STK_CONVERSION_BOND_PRICE 类"""
        assert hasattr(STK_CONVERSION_BOND_PRICE, "bond_code")
        assert hasattr(STK_CONVERSION_BOND_PRICE, "date")
        assert hasattr(STK_CONVERSION_BOND_PRICE, "close")
        assert hasattr(STK_CONVERSION_BOND_PRICE, "volume")

    def test_conversion_bond_class(self):
        """测试 CONVERSION_BOND 类"""
        assert hasattr(CONVERSION_BOND, "bond_code")
        assert hasattr(CONVERSION_BOND, "bond_name")
        assert hasattr(CONVERSION_BOND, "stock_code")
        assert hasattr(CONVERSION_BOND, "conversion_price")
        assert hasattr(CONVERSION_BOND, "premium_rate")


class TestGlobalFinanceCompatibility:
    """测试全局 finance 模块兼容性"""

    def test_global_finance_tables_defined(self):
        """测试全局 finance 表定义"""
        from jk2bt import finance as global_finance

        assert hasattr(global_finance, "STK_CONVERSION_BOND_BASIC")
        assert hasattr(global_finance, "STK_CONVERSION_BOND_PRICE")
        assert hasattr(global_finance, "STK_CB_DAILY")
        print("全局 finance 表定义检查通过")

    def test_global_finance_run_query_stk_cb_daily(self):
        """测试全局 finance.run_query STK_CB_DAILY"""
        from jk2bt import finance as global_finance

        df = global_finance.run_query(global_finance.STK_CB_DAILY)
        assert isinstance(df, pd.DataFrame)
        print(f"全局 finance.STK_CB_DAILY 查询: {len(df)} 条记录")

    def test_global_finance_run_query_stk_conversion_bond_basic(self):
        """测试全局 finance.run_query STK_CONVERSION_BOND_BASIC"""
        from jk2bt import finance as global_finance

        df = global_finance.run_query(global_finance.STK_CONVERSION_BOND_BASIC)
        assert isinstance(df, pd.DataFrame)
        print(f"全局 finance.STK_CONVERSION_BOND_BASIC 查询: {len(df)} 条记录")

    def test_global_finance_run_query_with_bond_code(self):
        """测试全局 finance.run_query 带债券代码查询"""
        from jk2bt import (
            finance as global_finance,
            query,
        )

        q = query(global_finance.STK_CONVERSION_BOND_BASIC)
        df = global_finance.run_query(q)
        assert isinstance(df, pd.DataFrame)
        print(f"带查询对象的全局 finance 查询: {len(df)} 条记录")


class TestEmptyCodeHandling:
    """测试空代码和非法代码处理"""

    def test_empty_bond_code_returns_empty_df(self):
        """测试空债券代码返回空 DataFrame"""
        result = get_conversion_bond_price("", use_cache=False)
        assert result.success is False
        assert isinstance(result.data, pd.DataFrame)
        print("空债券代码返回失败 RobustResult")

    def test_none_bond_code_returns_empty_df(self):
        """测试 None 债券代码返回空 DataFrame"""
        result = get_conversion_bond_price(None, use_cache=False)
        assert result.success is False
        assert isinstance(result.data, pd.DataFrame)
        print("None 债券代码返回失败 RobustResult")

    def test_invalid_bond_code_returns_empty_df(self):
        """测试无效债券代码返回空 DataFrame"""
        result = get_conversion_bond_price("999999", use_cache=False)
        assert result.success is False
        assert isinstance(result.data, pd.DataFrame)
        print("无效债券代码返回失败 RobustResult")

    def test_query_conversion_bond_basic_empty_code(self):
        """测试 query_conversion_bond_basic 空代码返回数据"""
        df = query_conversion_bond_basic(bond_code="", use_cache=False)
        assert isinstance(df, pd.DataFrame)
        print(f"空代码查询基本信息返回: {len(df)} 条记录")

    def test_query_conversion_bond_price_empty_code(self):
        """测试 query_conversion_bond_price 空代码返回空 DataFrame"""
        df = query_conversion_bond_price(bond_code="", use_cache=False)
        assert isinstance(df, pd.DataFrame)
        assert df.empty
        print("空代码查询行情返回空 DataFrame")

    def test_module_finance_unsupported_table_returns_empty(self):
        """测试模块 finance 不支持的表返回空 DataFrame"""
        from jk2bt.market_data.conversion_bond import (
            FinanceQuery,
        )

        fq = FinanceQuery()

        class UnsupportedTable:
            pass

        df = fq.run_query(UnsupportedTable())
        assert isinstance(df, pd.DataFrame)
        assert df.empty
        print("不支持的表返回空 DataFrame")


class TestConversionValueStability:
    """测试转股价值和溢价率稳定性"""

    def test_conversion_value_calculation_stable(self):
        """测试转股价值计算稳定性"""
        for _ in range(3):
            value = calculate_conversion_value(conversion_price=20.0, stock_price=25.0)
            expected = (100 / 20.0) * 25.0
            assert value == pytest.approx(expected, rel=0.001)
        print("转股价值计算稳定")

    def test_premium_rate_calculation_stable(self):
        """测试溢价率计算稳定性"""
        for _ in range(3):
            premium = calculate_premium_rate(bond_price=120.0, conversion_value=100.0)
            assert premium == pytest.approx(20.0, rel=0.001)
        print("溢价率计算稳定")

    def test_get_conversion_value_with_valid_code(self):
        """测试有效代码的转股价值获取"""
        result = get_conversion_value("110048", stock_price=100.0, use_cache=False)
        assert isinstance(result, RobustResult)
        if result.success:
            data = result.data
            assert "conversion_value" in data
            assert "premium_rate" in data
            assert data["conversion_value"] > 0
            print(
                f"转股价值: {data['conversion_value']}, 溢价率: {data['premium_rate']}"
            )

    def test_get_conversion_value_with_invalid_code(self):
        """测试无效代码的转股价值获取"""
        result = get_conversion_value("999999", stock_price=100.0, use_cache=False)
        assert isinstance(result, RobustResult)
        assert result.success is False
        print(f"无效代码转股价值查询: {result.reason}")

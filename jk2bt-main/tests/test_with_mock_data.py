"""
tests/test_with_mock_data.py
使用 Mock 数据的离线测试

优势：
1. 无需网络连接即可运行
2. 测试数据固定可重复
3. 测试速度快
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tests.mock_data import MOCK_PROVIDER


class TestMockCompanyInfo:
    """使用 Mock 数据测试公司信息 API"""

    def test_get_company_info_600519(self):
        """测试获取茅台公司信息"""
        df = MOCK_PROVIDER.get_company_info("600519")

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert df.iloc[0]["code"] == "600519.XSHG"
        assert "贵州茅台" in df.iloc[0]["company_name"]
        assert df.iloc[0]["industry"] == "饮料制造"

    def test_get_company_info_000001(self):
        """测试获取平安银行公司信息"""
        df = MOCK_PROVIDER.get_company_info("000001")

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert df.iloc[0]["code"] == "000001.XSHE"
        assert "平安银行" in df.iloc[0]["company_name"]

    def test_get_company_info_cache(self):
        """测试 Mock 数据缓存"""
        df1 = MOCK_PROVIDER.get_company_info("600036")
        df2 = MOCK_PROVIDER.get_company_info("600036")

        assert df1.equals(df2)


class TestMockSecurityStatus:
    """使用 Mock 数据测试证券状态 API"""

    def test_get_security_status_normal(self):
        """测试正常交易状态"""
        df = MOCK_PROVIDER.get_security_status("600519", "2025-01-15")

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "status_type" in df.columns
        assert df.iloc[0]["status_type"] == "正常交易"

    def test_get_security_status_with_date(self):
        """测试指定日期状态"""
        df = MOCK_PROVIDER.get_security_status("000001", "2025-03-20")

        assert isinstance(df, pd.DataFrame)
        assert "status_date" in df.columns
        assert df.iloc[0]["status_date"] == "2025-03-20"


class TestMockShareholder:
    """使用 Mock 数据测试股东信息 API"""

    def test_get_shareholder_data(self):
        """测试获取股东数据"""
        df = MOCK_PROVIDER.get_shareholder_data("600519")

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "shareholder_name" in df.columns
        assert "share_ratio" in df.columns
        assert len(df) == 5

    def test_shareholder_top1(self):
        """测试第一大股东"""
        df = MOCK_PROVIDER.get_shareholder_data("600519")

        assert "贵州茅台酒厂" in df.iloc[0]["shareholder_name"]
        assert df.iloc[0]["share_ratio"] > 50


class TestMockDividend:
    """使用 Mock 数据测试分红信息 API"""

    def test_get_dividend_data(self):
        """测试获取分红数据"""
        df = MOCK_PROVIDER.get_dividend_data("600519")

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "bonus_amount_rmb" in df.columns
        assert "ex_dividend_date" in df.columns

    def test_dividend_trend(self):
        """测试分红趋势"""
        df = MOCK_PROVIDER.get_dividend_data("600519")

        # 检查分红金额
        assert all(df["bonus_amount_rmb"] > 0)


class TestMockStockDaily:
    """使用 Mock 数据测试股票日线 API"""

    def test_get_stock_daily(self):
        """测试获取股票日线数据"""
        df = MOCK_PROVIDER.get_stock_daily("600519", "2025-01-01", "2025-01-31")

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "datetime" in df.columns
        assert "open" in df.columns
        assert "close" in df.columns
        assert "volume" in df.columns

    def test_stock_daily_columns(self):
        """测试日线数据列完整性"""
        df = MOCK_PROVIDER.get_stock_daily("600519", "2025-01-01", "2025-01-15")

        required_cols = ["datetime", "open", "high", "low", "close", "volume", "money"]
        for col in required_cols:
            assert col in df.columns


class TestMockUnlock:
    """使用 Mock 数据测试解禁数据 API"""

    def test_get_unlock_data(self):
        """测试获取解禁数据"""
        df = MOCK_PROVIDER.get_unlock_data("600519")

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "unlock_date" in df.columns
        assert "unlock_ratio" in df.columns


class TestOfflineIntegration:
    """离线集成测试"""

    def test_full_workflow(self):
        """测试完整工作流（离线）"""
        print("\n=== 离线集成测试 ===")

        # 1. 公司信息
        company = MOCK_PROVIDER.get_company_info("600519")
        print(f"1. 公司信息: {company.iloc[0]['company_name']}")

        # 2. 证券状态
        status = MOCK_PROVIDER.get_security_status("600519", "2025-01-15")
        print(f"2. 证券状态: {status.iloc[0]['status_type']}")

        # 3. 股东信息
        shareholders = MOCK_PROVIDER.get_shareholder_data("600519")
        print(f"3. 股东数量: {len(shareholders)}")

        # 4. 分红信息
        dividends = MOCK_PROVIDER.get_dividend_data("600519")
        print(f"4. 分红记录: {len(dividends)}")

        # 5. 日线数据
        daily = MOCK_PROVIDER.get_stock_daily("600519", "2025-01-01", "2025-01-31")
        print(f"5. 日线数据: {len(daily)} 条")

        print("=== 离线测试完成 ===\n")


def test_all_mock_functions():
    """快速验证所有 Mock 函数"""
    print("\n=== 验证所有 Mock 函数 ===")

    functions = [
        ("get_company_info", ["600519"]),
        ("get_security_status", ["600519", "2025-01-15"]),
        ("get_shareholder_data", ["600519"]),
        ("get_dividend_data", ["600519"]),
        ("get_stock_daily", ["600519", "2025-01-01", "2025-01-15"]),
        ("get_unlock_data", ["600519"]),
    ]

    for func_name, args in functions:
        func = getattr(MOCK_PROVIDER, func_name)
        df = func(*args)
        status = "✅" if not df.empty else "❌"
        print(f"{status} {func_name}: {len(df)} 条记录")


if __name__ == "__main__":
    test_all_mock_functions()
    pytest.main([__file__, "-v", "-s"])

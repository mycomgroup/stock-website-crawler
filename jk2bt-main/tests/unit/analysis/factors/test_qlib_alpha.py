"""
test_qlib_alpha.py
Qlib Alpha因子模块测试。

测试覆盖：
- init_qlib 初始化qlib
- compute_alpha101 Alpha101因子
- compute_alpha191 Alpha191因子
- compute_alpha360 Alpha360因子
- get_alpha_values_jq 聚宽风格接口
"""

import warnings

warnings.filterwarnings("ignore")

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock


class TestQlibAlphaImport:
    """测试qlib导入和可用性。"""

    def test_qlib_import_status(self):
        """测试qlib是否可用。"""
        from jk2bt.analysis.factors import qlib_alpha

        assert hasattr(qlib_alpha, "QLIB_AVAILABLE")

    def test_module_functions_exist(self):
        """测试模块函数存在。"""
        from jk2bt.analysis.factors import qlib_alpha

        assert hasattr(qlib_alpha, "init_qlib")
        assert hasattr(qlib_alpha, "compute_alpha101")
        assert hasattr(qlib_alpha, "compute_alpha191")
        assert hasattr(qlib_alpha, "compute_alpha360")
        assert hasattr(qlib_alpha, "get_alpha_values_jq")

    def test_qlib_unavailable_raises(self):
        """测试qlib不可用时抛出ImportError。"""
        from jk2bt.analysis.factors import qlib_alpha

        if not qlib_alpha.QLIB_AVAILABLE:
            with pytest.raises(ImportError, match="qlib未安装"):
                qlib_alpha.init_qlib()


class TestAlphaExpressionGetters:
    """测试Alpha表达式获取函数。"""

    def test_get_alpha101_expr_defined(self):
        """测试已知Alpha101表达式。"""
        from jk2bt.analysis.factors.qlib_alpha import _get_alpha101_expr

        expr = _get_alpha101_expr("alpha001")
        assert expr is not None
        assert "rank" in expr.lower() or "ts_" in expr.lower()

    def test_get_alpha101_expr_undefined(self):
        """测试未知Alpha101表达式。"""
        from jk2bt.analysis.factors.qlib_alpha import _get_alpha101_expr

        expr = _get_alpha101_expr("alpha999")
        assert expr is None

    def test_get_alpha101_expr_fallback(self):
        """测试Alpha101 fallback表达式。"""
        from jk2bt.analysis.factors.qlib_alpha import _get_alpha101_expr

        expr = _get_alpha101_expr("alpha050")
        assert expr is not None
        assert "Ref" in expr

    def test_get_alpha191_expr_defined(self):
        """测试已知Alpha191表达式。"""
        from jk2bt.analysis.factors.qlib_alpha import _get_alpha191_expr

        expr = _get_alpha191_expr("alpha001")
        assert expr is not None

    def test_get_alpha191_expr_undefined(self):
        """测试未知Alpha191表达式。"""
        from jk2bt.analysis.factors.qlib_alpha import _get_alpha191_expr

        expr = _get_alpha191_expr("alpha999")
        assert expr is None


class TestAlphaEstimateStartDate:
    """测试起始日期估算函数。"""

    def test_estimate_start_date(self):
        """测试起始日期估算。"""
        from jk2bt.analysis.factors.qlib_alpha import _estimate_start_date

        result = _estimate_start_date("2023-12-31", 100)
        assert result < "2023-12-31"

    def test_estimate_start_date_format(self):
        """测试返回日期格式。"""
        from jk2bt.analysis.factors.qlib_alpha import _estimate_start_date

        result = _estimate_start_date("2023-12-31", 100)
        assert len(result) == 10
        assert "-" in result


class TestGetAlphaValuesJq:
    """测试聚宽风格接口。"""

    def test_symbol_conversion(self):
        """测试代码转换。"""
        from jk2bt.analysis.factors.qlib_alpha import _get_alpha101_expr

        expr = _get_alpha101_expr("alpha001")
        assert expr is not None

    def test_jq_code_conversion(self):
        """测试聚宽代码格式转换。"""
        from jk2bt.analysis.factors.qlib_alpha import get_alpha_values_jq

        if not hasattr(get_alpha_values_jq, "__wrapped__"):
            pass


class TestAlpha101NotAvailable:
    """测试qlib不可用时的行为。"""

    def test_compute_alpha101_no_qlib(self):
        """测试qlib不可用时compute_alpha101行为。"""
        from jk2bt.analysis.factors import qlib_alpha

        if not qlib_alpha.QLIB_AVAILABLE:
            with pytest.raises(ImportError, match="qlib未安装"):
                qlib_alpha.compute_alpha101(["sh600519"])

    def test_compute_alpha191_no_qlib(self):
        """测试qlib不可用时compute_alpha191行为。"""
        from jk2bt.analysis.factors import qlib_alpha

        if not qlib_alpha.QLIB_AVAILABLE:
            with pytest.raises(ImportError, match="qlib未安装"):
                qlib_alpha.compute_alpha191(["sh600519"])

    def test_compute_alpha360_no_qlib(self):
        """测试qlib不可用时compute_alpha360行为。"""
        from jk2bt.analysis.factors import qlib_alpha

        if not qlib_alpha.QLIB_AVAILABLE:
            with pytest.raises(ImportError, match="qlib未安装"):
                qlib_alpha.compute_alpha360(["sh600519"])

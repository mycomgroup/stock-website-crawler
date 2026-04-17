"""Tests for qlib Alpha101/Alpha191 expression dictionaries and APIs."""


def test_alpha101_expr_count():
    from jk2bt.analysis.factors.qlib_alpha import ALPHA101_EXPR

    assert len(ALPHA101_EXPR) == 101
    for i in range(1, 102):
        key = f"alpha{i:03d}"
        assert key in ALPHA101_EXPR
        assert isinstance(ALPHA101_EXPR[key], str)
        assert len(ALPHA101_EXPR[key]) > 0


def test_alpha191_expr_count():
    from jk2bt.analysis.factors.qlib_alpha import ALPHA191_EXPR

    assert len(ALPHA191_EXPR) == 191
    for i in range(1, 192):
        key = f"alpha{i:03d}"
        assert key in ALPHA191_EXPR
        assert isinstance(ALPHA191_EXPR[key], str)
        assert len(ALPHA191_EXPR[key]) > 0


def test_get_alpha_expr_helpers():
    from jk2bt.analysis.factors.qlib_alpha import (
        _get_alpha101_expr,
        _get_alpha191_expr,
    )

    assert _get_alpha101_expr("alpha001") is not None
    assert _get_alpha101_expr("alpha101") is not None
    assert _get_alpha101_expr("alpha102") is None

    assert _get_alpha191_expr("alpha001") is not None
    assert _get_alpha191_expr("alpha191") is not None
    assert _get_alpha191_expr("alpha192") is None


def test_api_factor_alpha_interfaces():
    from jk2bt.api.factor import get_alpha101, get_alpha191

    assert callable(get_alpha101)
    assert callable(get_alpha191)

"""
test_constants.py
constants.py 单元测试

测试场景覆盖:
1. SECURITY_INDEXES 常量
2. INDEX_CODE_ALIAS_MAP 别名映射
3. INDEX_FALLBACK_MAP 回退映射
4. CONS_ONLY_INDICES 特殊指数集合
5. DATE_COLUMN_CANDIDATES 日期列候选
6. INDEX_DESCRIPTION 指数描述
"""

import pytest
from jk2bt.engine.constants import (
    SECURITY_INDEXES,
    INDEX_CODE_ALIAS_MAP,
    INDEX_FALLBACK_MAP,
    CONS_ONLY_INDICES,
    DATE_COLUMN_CANDIDATES,
    INDEX_DESCRIPTION,
)


class TestSecurityIndexes:
    """测试 SECURITY_INDEXES 常量"""

    def test_security_indexes_not_empty(self):
        """测试指数列表不为空"""
        assert len(SECURITY_INDEXES) > 0

    def test_hs300_exists(self):
        """测试沪深300指数存在"""
        assert "000300" in SECURITY_INDEXES
        assert SECURITY_INDEXES["000300"] == "沪深300"

    def test_common_indices_exist(self):
        """测试常见指数都存在"""
        common_indices = ["000300", "000016", "000905", "000852", "399006"]
        for idx in common_indices:
            assert idx in SECURITY_INDEXES

    def test_index_codes_are_six_digits(self):
        """测试所有指数代码都是6位数字"""
        for code in SECURITY_INDEXES.keys():
            assert len(code) == 6
            assert code.isdigit()


class TestIndexCodeAliasMap:
    """测试 INDEX_CODE_ALIAS_MAP 别名映射"""

    def test_alias_map_not_empty(self):
        """测试别名映射不为空"""
        assert len(INDEX_CODE_ALIAS_MAP) > 0

    def test_hs300_aliases(self):
        """测试沪深300别名"""
        assert "sh000300" in INDEX_CODE_ALIAS_MAP
        assert "hs300" in INDEX_CODE_ALIAS_MAP
        assert "沪深300" in INDEX_CODE_ALIAS_MAP
        assert INDEX_CODE_ALIAS_MAP["hs300"] == "000300"

    def test_cyb_alias(self):
        """测试创业板别名"""
        assert "cyb" in INDEX_CODE_ALIAS_MAP
        assert "创业板" in INDEX_CODE_ALIAS_MAP
        assert INDEX_CODE_ALIAS_MAP["cyb"] == "399006"

    def test_alias_resolve(self):
        """测试别名解析"""
        assert INDEX_CODE_ALIAS_MAP["000300.xshg"] == "000300"
        assert INDEX_CODE_ALIAS_MAP["399006.xshe"] == "399006"


class TestIndexFallbackMap:
    """测试 INDEX_FALLBACK_MAP 回退映射"""

    def test_fallback_map_not_empty(self):
        """测试回退映射不为空"""
        assert len(INDEX_FALLBACK_MAP) > 0

    def test_fallback_format(self):
        """测试回退格式"""
        for original, fallback in INDEX_FALLBACK_MAP.items():
            assert len(original) == 6
            assert len(fallback) == 6


class TestConsOnlyIndices:
    """测试 CONS_ONLY_INDICES 特殊指数集合"""

    def test_cons_only_indices_not_empty(self):
        """测试特殊指数集合不为空"""
        assert len(CONS_ONLY_INDICES) > 0

    def test_cons_only_contains_399_codes(self):
        """测试特殊指数包含深市代码"""
        for code in CONS_ONLY_INDICES:
            assert code.startswith("399")


class TestDateColumnCandidates:
    """测试 DATE_COLUMN_CANDIDATES 日期列候选"""

    def test_market_candidates_exist(self):
        """测试市场数据日期列候选"""
        assert "market" in DATE_COLUMN_CANDIDATES
        assert len(DATE_COLUMN_CANDIDATES["market"]) > 0

    def test_financial_candidates_exist(self):
        """测试财务数据日期列候选"""
        assert "financial" in DATE_COLUMN_CANDIDATES
        assert len(DATE_COLUMN_CANDIDATES["financial"]) > 0

    def test_common_candidates_exist(self):
        """测试通用日期列候选"""
        assert "common" in DATE_COLUMN_CANDIDATES
        assert len(DATE_COLUMN_CANDIDATES["common"]) > 0

    def test_date_in_common(self):
        """测试通用候选包含date"""
        assert "date" in DATE_COLUMN_CANDIDATES["common"]


class TestIndexDescription:
    """测试 INDEX_DESCRIPTION 指数描述"""

    def test_description_for_key_indices(self):
        """测试关键指数有描述"""
        key_indices = ["399101", "399303", "399006", "399001"]
        for idx in key_indices:
            assert idx in INDEX_DESCRIPTION
            assert len(INDEX_DESCRIPTION[idx]) > 0

    def test_description_format(self):
        """测试描述格式"""
        for code, desc in INDEX_DESCRIPTION.items():
            assert isinstance(desc, str)
            assert len(desc) > 0

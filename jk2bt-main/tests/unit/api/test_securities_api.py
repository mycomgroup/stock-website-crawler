"""
tests/unit/api/test_securities_api.py
证券信息 API 单元测试

测试覆盖:
1. get_all_securities - 获取全市场证券列表
2. get_security_info - 获取单只证券信息
3. get_all_securities_jq - 聚宽风格别名
4. get_security_info_jq - 聚宽风格别名
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock


class TestGetAllSecurities:
    """测试获取全市场证券列表"""

    @patch("jk2bt.api.securities.get_all_securities_jq")
    def test_get_all_securities(self, mock_get_all):
        mock_get_all.return_value = pd.DataFrame(
            {
                "display_name": ["贵州茅台", "平安银行"],
                "name": ["茅台", "平安"],
                "start_date": ["2001-08-27", "1991-04-03"],
                "type": ["stock", "stock"],
            },
            index=pd.Index(["600519.XSHG", "000001.XSHE"], name="JQ_Code"),
        )

        from jk2bt.api.securities import get_all_securities

        result = get_all_securities()

        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.api.securities.get_all_securities_jq")
    def test_get_all_securities_with_types(self, mock_get_all):
        mock_get_all.return_value = pd.DataFrame()

        from jk2bt.api.securities import get_all_securities

        result = get_all_securities(types=["stock"])

        mock_get_all.assert_called_once_with(types=["stock"], date=None)


class TestGetSecurityInfo:
    """测试获取单只证券信息"""

    @patch("jk2bt.api.securities.get_security_info_jq")
    def test_get_security_info_success(self, mock_get_info):
        mock_info = MagicMock()
        mock_info.display_name = "贵州茅台"
        mock_info.name = "茅台"
        mock_info.start_date = "2001-08-27"
        mock_info.type = "stock"
        mock_get_info.return_value = mock_info

        from jk2bt.api.securities import get_security_info

        result = get_security_info("600519.XSHG")

        assert result.display_name == "贵州茅台"

    def test_get_security_info_empty_code(self):
        from jk2bt.api.securities import get_security_info

        with pytest.raises(ValueError, match="code 参数不能为空"):
            get_security_info("")

    def test_get_security_info_none_code(self):
        from jk2bt.api.securities import get_security_info

        with pytest.raises(ValueError, match="code 参数不能为空"):
            get_security_info(None)


class TestSecuritiesAliases:
    """测试聚宽风格别名"""

    def test_get_all_securities_jq_is_get_all_securities(self):
        from jk2bt.api.securities import get_all_securities, get_all_securities_jq

        assert get_all_securities_jq is get_all_securities

    def test_get_security_info_jq_is_get_security_info(self):
        from jk2bt.api.securities import get_security_info, get_security_info_jq

        assert get_security_info_jq is get_security_info

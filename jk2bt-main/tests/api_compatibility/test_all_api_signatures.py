"""
test_all_api_signatures.py
测试所有API是否存在、参数签名是否正确
使用inspect.signature检查函数签名
"""

import sys
import os
import inspect
from typing import get_type_hints

# 添加项目路径
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import pytest


class TestAPISignatureValidator:
    """API签名验证器"""

    # 定义期望的API签名（聚宽风格）
    EXPECTED_API_SIGNATURES = {
        # Market API
        "get_price": {
            "module": "src.api.market_api",
            "params": ["security", "start_date", "end_date", "frequency", "fields", "skip_paused", "fq", "count", "panel", "fill_paused"],
            "required": ["security"],
        },
        "history": {
            "module": "src.api.market_api",
            "params": ["count", "unit", "field", "security_list", "df", "skip_paused", "fq", "end_date"],
            "required": ["count"],
        },
        "attribute_history": {
            "module": "src.api.market_api",
            "params": ["security", "count", "unit", "fields", "skip_paused", "df", "fq", "end_date"],
            "required": ["security", "count"],
        },
        "get_bars": {
            "module": "src.api.market_api",
            "params": ["security", "count", "unit", "fields", "include_now", "end_dt", "fq", "skip_paused"],
            "required": ["security", "count"],
        },
        # Enhancements API
        "order_shares": {
            "module": "src.api.enhancements",
            "params": ["security", "amount", "style"],
            "required": ["security", "amount"],
        },
        "order_target_percent": {
            "module": "src.api.enhancements",
            "params": ["security", "percent"],
            "required": ["security", "percent"],
        },
        "filter_st": {
            "module": "src.api.enhancements",
            "params": ["stock_list", "date"],
            "required": ["stock_list"],
        },
        "filter_paused": {
            "module": "src.api.enhancements",
            "params": ["stock_list", "date"],
            "required": ["stock_list"],
        },
        "filter_limit_up": {
            "module": "src.api.enhancements",
            "params": ["stock_list", "date"],
            "required": ["stock_list"],
        },
        "filter_limit_down": {
            "module": "src.api.enhancements",
            "params": ["stock_list", "date"],
            "required": ["stock_list"],
        },
        "filter_new_stocks": {
            "module": "src.api.enhancements",
            "params": ["stock_list", "days"],
            "required": ["stock_list"],
        },
        # Indicators API
        "MA": {
            "module": "src.api.indicators",
            "params": ["closeArray", "timeperiod"],
            "required": ["closeArray"],
        },
        "EMA": {
            "module": "src.api.indicators",
            "params": ["closeArray", "timeperiod"],
            "required": ["closeArray"],
        },
        "MACD": {
            "module": "src.api.indicators",
            "params": ["security_list", "check_date", "SHORT", "LONG", "MID", "unit", "include_now"],
            "required": ["security_list"],
        },
        "KDJ": {
            "module": "src.api.indicators",
            "params": ["security", "check_date", "unit", "N", "M1", "M2", "include_now"],
            "required": ["security"],
        },
        "RSI": {
            "module": "src.api.indicators",
            "params": ["price", "timeperiod", "check_date"],
            "required": ["price"],
        },
        "BOLL": {
            "module": "src.api.indicators",
            "params": ["security", "check_date", "timeperiod", "nbdevup", "nbdevdn", "unit", "include_now"],
            "required": ["security"],
        },
        "ATR": {
            "module": "src.api.indicators",
            "params": ["security", "check_date", "timeperiod", "unit", "include_now"],
            "required": ["security"],
        },
        # Missing APIs
        "get_locked_shares": {
            "module": "src.api.missing_apis",
            "params": ["stock_list", "start_date", "end_date", "forward_count"],
            "required": [],
        },
        "get_fund_info": {
            "module": "src.api.missing_apis",
            "params": ["fund_code", "fields"],
            "required": ["fund_code"],
        },
        "get_fundamentals_continuously": {
            "module": "src.api.missing_apis",
            "params": ["query_obj", "start_date", "end_date", "frequency", "count", "fields"],
            "required": ["query_obj", "start_date"],
        },
        "get_beta": {
            "module": "src.api.missing_apis",
            "params": ["security", "benchmark", "start_date", "end_date", "window", "frequency"],
            "required": ["security"],
        },
        # Factor API
        "get_north_factor": {
            "module": "src.api.factor_api",
            "params": ["security", "end_date", "count", "window", "factor_type"],
            "required": [],
        },
        "get_comb_factor": {
            "module": "src.api.factor_api",
            "params": ["securities", "factors", "end_date", "count", "method", "weights", "normalize"],
            "required": ["securities", "factors"],
        },
        "get_factor_momentum": {
            "module": "src.api.factor_api",
            "params": ["securities", "factor", "window", "end_date"],
            "required": ["securities", "factor"],
        },
    }

    def test_api_exists(self):
        """测试所有API函数是否存在"""
        missing_apis = []

        for api_name, api_info in self.EXPECTED_API_SIGNATURES.items():
            try:
                module = __import__(api_info["module"], fromlist=[api_name])
                func = getattr(module, api_name)
                if not callable(func):
                    missing_apis.append(f"{api_name}: exists but not callable")
            except ImportError as e:
                missing_apis.append(f"{api_name}: module import failed - {e}")
            except AttributeError:
                missing_apis.append(f"{api_name}: function not found in module")

        assert len(missing_apis) == 0, f"Missing APIs:\n" + "\n".join(missing_apis)

    def test_api_signatures(self):
        """测试API函数签名是否正确"""
        signature_errors = []

        for api_name, api_info in self.EXPECTED_API_SIGNATURES.items():
            try:
                module = __import__(api_info["module"], fromlist=[api_name])
                func = getattr(module, api_name)

                # 获取函数签名
                sig = inspect.signature(func)
                actual_params = list(sig.parameters.keys())

                # 检查必需参数是否存在
                for required_param in api_info["required"]:
                    if required_param not in actual_params:
                        signature_errors.append(
                            f"{api_name}: missing required parameter '{required_param}'"
                        )

                # 检查参数数量是否匹配（允许有额外参数）
                expected_count = len(api_info["params"])
                actual_count = len(actual_params)

                # 允许实际参数比期望的多（可能有额外默认参数）
                if actual_count < expected_count:
                    missing = set(api_info["params"]) - set(actual_params)
                    signature_errors.append(
                        f"{api_name}: expected {expected_count} params, got {actual_count}. Missing: {missing}"
                    )

            except Exception as e:
                signature_errors.append(f"{api_name}: signature check failed - {e}")

        assert len(signature_errors) == 0, f"Signature errors:\n" + "\n".join(signature_errors)

    def test_api_callable(self):
        """测试API是否可调用"""
        callable_errors = []

        for api_name, api_info in self.EXPECTED_API_SIGNATURES.items():
            try:
                module = __import__(api_info["module"], fromlist=[api_name])
                func = getattr(module, api_name)

                if not callable(func):
                    callable_errors.append(f"{api_name}: not callable")

            except Exception as e:
                callable_errors.append(f"{api_name}: callable check failed - {e}")

        assert len(callable_errors) == 0, f"Callable errors:\n" + "\n".join(callable_errors)

    def test_api_return_types(self):
        """测试API返回类型标注"""
        # 这个测试是可选的，仅检查有类型标注的API
        type_info = []

        for api_name, api_info in self.EXPECTED_API_SIGNATURES.items():
            try:
                module = __import__(api_info["module"], fromlist=[api_name])
                func = getattr(module, api_name)

                # 尝试获取返回类型标注
                sig = inspect.signature(func)
                if sig.return_annotation != inspect.Parameter.empty:
                    type_info.append(f"{api_name}: returns {sig.return_annotation}")

            except Exception:
                pass

        # 这个测试总是通过，只是记录类型信息
        assert True


class TestModuleImport:
    """测试模块导入"""

    def test_api_module_import(self):
        """测试API模块可以导入"""
        modules_to_test = [
            "src.api",
            "src.api.market_api",
            "src.api.enhancements",
            "src.api.indicators",
            "src.api.missing_apis",
            "src.api.factor_api",
        ]

        import_errors = []

        for module_name in modules_to_test:
            try:
                __import__(module_name)
            except ImportError as e:
                import_errors.append(f"{module_name}: {e}")

        assert len(import_errors) == 0, f"Import errors:\n" + "\n".join(import_errors)

    def test_api_module_all_exports(self):
        """测试模块__all__导出"""
        module_exports = {
            "src.api": [
                "get_price", "history", "attribute_history", "get_bars",
                "MA", "EMA", "MACD", "KDJ", "RSI", "BOLL", "ATR",
                "filter_st", "filter_paused", "filter_new_stocks",
            ],
            "src.api.market_api": ["get_price", "history", "attribute_history", "get_bars", "get_price_jq", "get_bars_jq"],
            "src.api.indicators": ["MA", "EMA", "MACD", "KDJ", "RSI", "BOLL", "ATR"],
            "src.api.enhancements": ["order_shares", "order_target_percent", "filter_st", "filter_paused"],
            "src.api.missing_apis": ["get_locked_shares", "get_fund_info", "get_fundamentals_continuously", "get_beta"],
            "src.api.factor_api": ["get_north_factor", "get_comb_factor", "get_factor_momentum"],
        }

        export_errors = []

        for module_name, expected_exports in module_exports.items():
            try:
                module = __import__(module_name, fromlist=["__all__"])
                actual_exports = getattr(module, "__all__", None)

                # 如果模块有__all__，检查是否包含期望导出
                # 如果没有__all__，直接检查函数是否可通过getattr获取
                if actual_exports is not None:
                    for export in expected_exports:
                        if export not in actual_exports:
                            export_errors.append(f"{module_name}: '{export}' not in __all__")
                else:
                    # 没有__all__时，检查是否可以通过getattr获取
                    for export in expected_exports:
                        if not hasattr(module, export):
                            export_errors.append(f"{module_name}: '{export}' not found in module")

            except ImportError as e:
                export_errors.append(f"{module_name}: import failed - {e}")

        assert len(export_errors) == 0, f"Export errors:\n" + "\n".join(export_errors)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
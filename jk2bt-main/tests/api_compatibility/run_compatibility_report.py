"""
run_compatibility_report.py
运行所有API兼容性测试并生成兼容性报告
输出每个API的状态: ✅实现 / ⚠️部分实现 / ❌未实现
"""

import sys
import os
import importlib
import inspect
from datetime import datetime

_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)


class APICompatibilityReporter:
    """API兼容性报告生成器"""

    # 定义需要检查的API列表
    API_CHECKLIST = {
        "Market API": {
            "get_price": {"module": "src.api.market_api", "critical": True},
            "history": {"module": "src.api.market_api", "critical": True},
            "attribute_history": {"module": "src.api.market_api", "critical": True},
            "get_bars": {"module": "src.api.market_api", "critical": True},
            "get_price_jq": {"module": "src.api.market_api", "critical": False},
            "get_bars_jq": {"module": "src.api.market_api", "critical": False},
        },
        "Enhancements API": {
            "order_shares": {"module": "src.api.enhancements", "critical": True},
            "order_target_percent": {"module": "src.api.enhancements", "critical": True},
            "filter_st": {"module": "src.api.enhancements", "critical": True},
            "filter_paused": {"module": "src.api.enhancements", "critical": True},
            "filter_limit_up": {"module": "src.api.enhancements", "critical": False},
            "filter_limit_down": {"module": "src.api.enhancements", "critical": False},
            "filter_new_stocks": {"module": "src.api.enhancements", "critical": True},
            "get_open_price": {"module": "src.api.enhancements", "critical": False},
            "get_close_price": {"module": "src.api.enhancements", "critical": False},
            "get_high_limit": {"module": "src.api.enhancements", "critical": False},
            "get_low_limit": {"module": "src.api.enhancements", "critical": False},
            "LimitOrderStyle": {"module": "src.api.enhancements", "critical": False},
            "MarketOrderStyle": {"module": "src.api.enhancements", "critical": False},
        },
        "Technical Indicators": {
            "MA": {"module": "src.api.indicators", "critical": True},
            "EMA": {"module": "src.api.indicators", "critical": True},
            "MACD": {"module": "src.api.indicators", "critical": True},
            "KDJ": {"module": "src.api.indicators", "critical": True},
            "RSI": {"module": "src.api.indicators", "critical": True},
            "BOLL": {"module": "src.api.indicators", "critical": True},
            "ATR": {"module": "src.api.indicators", "critical": False},
        },
        "Missing APIs": {
            "get_locked_shares": {"module": "src.api.missing_apis", "critical": False},
            "get_fund_info": {"module": "src.api.missing_apis", "critical": False},
            "get_fundamentals_continuously": {"module": "src.api.missing_apis", "critical": False},
            "get_beta": {"module": "src.api.missing_apis", "critical": False},
        },
        "Factor API": {
            "get_north_factor": {"module": "src.api.factor_api", "critical": False},
            "get_comb_factor": {"module": "src.api.factor_api", "critical": False},
            "get_factor_momentum": {"module": "src.api.factor_api", "critical": False},
        },
        "Optimizations": {
            "get_current_data_cached": {"module": "src.api.optimizations", "critical": False},
            "cached_get_security_info": {"module": "src.api.optimizations", "critical": False},
            "cached_get_index_stocks": {"module": "src.api.optimizations", "critical": False},
            "batch_get_fundamentals": {"module": "src.api.optimizations", "critical": False},
        },
    }

    # 期望的参数签名
    EXPECTED_SIGNATURES = {
        "get_price": ["security", "start_date", "end_date", "frequency", "fields", "fq", "count"],
        "history": ["count", "unit", "field", "security_list", "df", "fq", "end_date"],
        "attribute_history": ["security", "count", "unit", "fields", "df", "fq", "end_date"],
        "get_bars": ["security", "count", "unit", "fields", "fq", "skip_paused"],
        "filter_st": ["stock_list", "date"],
        "filter_paused": ["stock_list", "date"],
        "MA": ["closeArray", "timeperiod"],
        "EMA": ["closeArray", "timeperiod"],
        "MACD": ["security_list", "check_date", "SHORT", "LONG", "MID"],
        "KDJ": ["security", "check_date", "N", "M1", "M2"],
        "RSI": ["price", "timeperiod", "check_date"],
        "BOLL": ["security", "check_date", "timeperiod", "nbdevup", "nbdevdn"],
    }

    def __init__(self):
        self.results = {}
        self.summary = {
            "implemented": 0,
            "partial": 0,
            "missing": 0,
            "total": 0,
        }

    def check_api_exists(self, module_name, api_name):
        """检查API是否存在"""
        try:
            module = importlib.import_module(module_name)
            func = getattr(module, api_name)
            return True, func
        except ImportError:
            return False, None
        except AttributeError:
            return False, None

    def check_signature(self, func, expected_params):
        """检查参数签名"""
        if func is None:
            return False, []

        try:
            sig = inspect.signature(func)
            actual_params = list(sig.parameters.keys())

            # 检查关键参数是否存在
            missing_params = []
            for param in expected_params:
                if param not in actual_params:
                    missing_params.append(param)

            # 如果缺少关键参数，则标记为部分实现
            if len(missing_params) > 0:
                return False, missing_params

            return True, actual_params

        except Exception as e:
            return False, [str(e)]

    def check_callable(self, func):
        """检查是否可调用"""
        if func is None:
            return False
        return callable(func)

    def run_checks(self):
        """运行所有检查"""
        for category, apis in self.API_CHECKLIST.items():
            self.results[category] = {}

            for api_name, api_info in apis.items():
                self.summary["total"] += 1

                # 检查存在性
                exists, func = self.check_api_exists(api_info["module"], api_name)

                if not exists:
                    self.results[category][api_name] = {
                        "status": "missing",
                        "icon": "X",
                        "critical": api_info["critical"],
                        "details": "API not found in module",
                    }
                    self.summary["missing"] += 1
                    continue

                # 检查可调用性
                callable_ok = self.check_callable(func)

                if not callable_ok:
                    self.results[category][api_name] = {
                        "status": "partial",
                        "icon": "!",
                        "critical": api_info["critical"],
                        "details": "API exists but not callable",
                    }
                    self.summary["partial"] += 1
                    continue

                # 检查签名
                expected = self.EXPECTED_SIGNATURES.get(api_name, [])
                sig_ok, missing = self.check_signature(func, expected)

                if not sig_ok and len(expected) > 0:
                    self.results[category][api_name] = {
                        "status": "partial",
                        "icon": "!",
                        "critical": api_info["critical"],
                        "details": f"Missing params: {missing}",
                    }
                    self.summary["partial"] += 1
                else:
                    self.results[category][api_name] = {
                        "status": "implemented",
                        "icon": "OK",
                        "critical": api_info["critical"],
                        "details": "Fully implemented",
                    }
                    self.summary["implemented"] += 1

    def generate_report(self):
        """生成报告"""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("API Compatibility Report")
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("=" * 60)
        report_lines.append("")

        # 汇总统计
        report_lines.append("SUMMARY")
        report_lines.append("-" * 40)
        total = self.summary["total"]
        implemented_pct = (self.summary["implemented"] / total * 100) if total > 0 else 0
        partial_pct = (self.summary["partial"] / total * 100) if total > 0 else 0
        missing_pct = (self.summary["missing"] / total * 100) if total > 0 else 0

        report_lines.append(f"  Total APIs: {total}")
        report_lines.append(f"  Implemented: {self.summary['implemented']} ({implemented_pct:.1f}%)")
        report_lines.append(f"  Partial: {self.summary['partial']} ({partial_pct:.1f}%)")
        report_lines.append(f"  Missing: {self.summary['missing']} ({missing_pct:.1f}%)")
        report_lines.append("")

        # 详细报告
        report_lines.append("DETAILED STATUS")
        report_lines.append("-" * 40)

        for category, apis in self.results.items():
            report_lines.append(f"\n[{category}]")

            for api_name, result in apis.items():
                icon = result["icon"]
                status = result["status"]
                critical = result["critical"]
                details = result["details"]

                # 格式化输出
                critical_mark = "*" if critical else " "
                status_text = {
                    "implemented": "Implemented",
                    "partial": "Partial",
                    "missing": "Missing",
                }.get(status, status)

                report_lines.append(f"  {icon} {critical_mark} {api_name}: {status_text}")
                if details and status != "implemented":
                    report_lines.append(f"      -> {details}")

        # 图例说明
        report_lines.append("")
        report_lines.append("LEGEND")
        report_lines.append("-" * 40)
        report_lines.append("  OK = Fully implemented")
        report_lines.append("  !   = Partially implemented (missing params or not callable)")
        report_lines.append("  X   = Not implemented")
        report_lines.append("  *   = Critical API (essential for strategy execution)")
        report_lines.append("")

        # 关键缺失API警告
        critical_missing = []
        for category, apis in self.results.items():
            for api_name, result in apis.items():
                if result["critical"] and result["status"] != "implemented":
                    critical_missing.append(api_name)

        if critical_missing:
            report_lines.append("WARNING: Critical APIs with issues")
            report_lines.append("-" * 40)
            for api in critical_missing:
                report_lines.append(f"  - {api}")
        else:
            report_lines.append("All critical APIs are implemented!")
            report_lines.append("-" * 40)

        report_lines.append("")
        report_lines.append("=" * 60)
        report_lines.append("END OF REPORT")
        report_lines.append("=" * 60)

        return "\n".join(report_lines)

    def save_report(self, filename="api_compatibility_report.txt"):
        """保存报告到文件"""
        report = self.generate_report()
        output_path = os.path.join(_project_root, "tests", "api_compatibility", filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"Report saved to: {output_path}")
        return report

    def run_pytest_tests(self):
        """运行pytest测试"""
        import subprocess

        test_dir = os.path.join(_project_root, "tests", "api_compatibility")

        print("\nRunning pytest tests...")
        print("-" * 40)

        # 运行所有测试文件
        test_files = [
            "test_all_api_signatures.py",
            "test_market_api.py",
            "test_stats_api.py",
            "test_date_api.py",
            "test_filter_api.py",
        ]

        results = {}
        for test_file in test_files:
            test_path = os.path.join(test_dir, test_file)
            if os.path.exists(test_path):
                try:
                    result = subprocess.run(
                        ["python", "-m", "pytest", test_path, "-v", "--tb=short"],
                        capture_output=True,
                        text=True,
                        timeout=120,
                    )
                    results[test_file] = {
                        "passed": result.returncode == 0,
                        "output": result.stdout + result.stderr,
                    }
                except subprocess.TimeoutExpired:
                    results[test_file] = {
                        "passed": False,
                        "output": "Test timed out",
                    }
                except Exception as e:
                    results[test_file] = {
                        "passed": False,
                        "output": str(e),
                    }

        return results


def main():
    """主函数"""
    print("API Compatibility Test Suite")
    print("=" * 60)

    reporter = APICompatibilityReporter()

    # 运行检查
    reporter.run_checks()

    # 生成并保存报告
    report = reporter.save_report()

    # 打印报告
    print("\n")
    print(report)

    # 运行pytest测试
    pytest_results = reporter.run_pytest_tests()

    print("\nPytest Test Results:")
    print("-" * 40)
    for test_file, result in pytest_results.items():
        status = "PASS" if result["passed"] else "FAIL"
        print(f"  {test_file}: {status}")

    # 返回总体状态
    critical_issues = reporter.summary["missing"] + reporter.summary["partial"]
    if critical_issues == 0:
        print("\nAll APIs are fully implemented and compatible!")
        return 0
    else:
        print(f"\nFound {critical_issues} APIs with issues. Check the report for details.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
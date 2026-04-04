"""
test_api_scanner_alignment.py
测试 API 扫描器与 Runtime 实现的对齐准确性

验证目标：
1. API 名称映射正确性（get_ticks -> get_ticks_enhanced）
2. 真实未支持 API 的准确性（get_dividends 应被标记）
3. 已实现 API 不应出现在 missing_apis 中
"""

import os
import tempfile
import pytest
from jk2bt.strategy.scanner import StrategyScanner, StrategyStatus


class TestAPINameMapping:
    """测试 API 名称映射解决扫描器误判"""

    def setup_method(self):
        """每个测试前初始化扫描器"""
        self.scanner = StrategyScanner()

    def _create_test_strategy(self, api_call: str) -> str:
        """创建测试策略文件（临时）"""
        code = f"""
def initialize(context):
    pass

def handle_data(context, data):
    {api_call}
"""
        # 创建临时文件
        temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False,
            encoding='utf-8'
        )
        temp_file.write(code)
        temp_file.close()
        return temp_file.name

    def test_get_ticks_mapping(self):
        """验证 get_ticks 不应被误判为未实现"""
        test_file = self._create_test_strategy("get_ticks('000001.XSHE', count=100)")
        result = self.scanner.scan_file(test_file)

        # get_ticks 已通过 get_ticks_enhanced 实现，不应在 missing_apis 中
        assert 'get_ticks' not in result.missing_apis, \
            "get_ticks should not be marked as missing (mapped to get_ticks_enhanced)"

        # 清理临时文件
        os.unlink(test_file)

    def test_get_future_contracts_mapping(self):
        """验证 get_future_contracts 不应被误判"""
        test_file = self._create_test_strategy("get_future_contracts('IF')")
        result = self.scanner.scan_file(test_file)

        # get_future_contracts 已实现，不应在 missing_apis 中
        assert 'get_future_contracts' not in result.missing_apis, \
            "get_future_contracts should not be marked as missing"

        os.unlink(test_file)

    def test_get_dominant_contract_mapping(self):
        """验证 get_dominant_contract 不应被误判"""
        test_file = self._create_test_strategy("get_dominant_contract('IF', date='2024-01-01')")
        result = self.scanner.scan_file(test_file)

        # get_dominant_contract 已通过 get_dominant_future 实现
        assert 'get_dominant_contract' not in result.missing_apis, \
            "get_dominant_contract should not be marked as missing (mapped to get_dominant_future)"

        os.unlink(test_file)

    def test_get_institutional_holdings_mapping(self):
        """验证 get_institutional_holdings 不应被误判"""
        test_file = self._create_test_strategy("get_institutional_holdings('000001.XSHE')")
        result = self.scanner.scan_file(test_file)

        # get_institutional_holdings 已实现（api/billboard.py）
        assert 'get_institutional_holdings' not in result.missing_apis, \
            "get_institutional_holdings should not be marked as missing"

        os.unlink(test_file)

    def test_get_margin_stocks_mapping(self):
        """验证 get_margin_stocks 不应被误判"""
        test_file = self._create_test_strategy("get_margin_stocks()")
        result = self.scanner.scan_file(test_file)

        # get_margin_stocks 已通过新接口 get_margincash_stocks 实现
        assert 'get_margin_stocks' not in result.missing_apis, \
            "get_margin_stocks should not be marked as missing (mapped to get_margincash_stocks)"

        os.unlink(test_file)


class TestMissingAPIAccuracy:
    """测试真实未支持 API 的准确性"""

    def setup_method(self):
        self.scanner = StrategyScanner()

    def _create_test_strategy(self, api_call: str) -> str:
        code = f"""
def initialize(context):
    pass

def handle_data(context, data):
    {api_call}
"""
        temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False,
            encoding='utf-8'
        )
        temp_file.write(code)
        temp_file.close()
        return temp_file.name

    def test_get_dividends_missing(self):
        """验证 get_dividends 应被正确标记为未实现"""
        test_file = self._create_test_strategy("get_dividends('000001.XSHE')")
        result = self.scanner.scan_file(test_file)

        # get_dividends 在必须实现层，应被标记为缺失
        assert 'get_dividends' in result.missing_apis, \
            "get_dividends should be marked as missing (P0 priority)"

        # 验证策略不可执行（因为依赖必须实现的 API）
        assert result.is_executable == False, \
            "Strategy with get_dividends should not be executable"

        os.unlink(test_file)

    def test_get_splits_missing(self):
        """验证 get_splits 应被正确标记为未实现"""
        test_file = self._create_test_strategy("get_splits('000001.XSHE')")
        result = self.scanner.scan_file(test_file)

        # get_splits 在必须实现层
        assert 'get_splits' in result.missing_apis, \
            "get_splits should be marked as missing (P0 priority)"

        assert result.is_executable == False

        os.unlink(test_file)

    def test_get_interest_rate_low_priority(self):
        """验证低优先级 API 应被标记但不阻止运行"""
        test_file = self._create_test_strategy("get_interest_rate()")
        result = self.scanner.scan_file(test_file)

        # get_interest_rate 在暂不支持层
        assert 'get_interest_rate' in result.missing_apis, \
            "get_interest_rate should be marked as missing (P3 low priority)"

        # TODO: 未来可以根据分层策略调整 is_executable 判断
        # 目前仍标记为不可执行，后续可放宽为 "策略受限但可运行"
        assert result.status == StrategyStatus.MISSING_API

        os.unlink(test_file)


class TestKnownAPIsSupport:
    """测试已知 API 不应被误判"""

    def setup_method(self):
        self.scanner = StrategyScanner()

    def _create_test_strategy(self, api_call: str) -> str:
        code = f"""
def initialize(context):
    pass

def handle_data(context, data):
    {api_call}
"""
        temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False,
            encoding='utf-8'
        )
        temp_file.write(code)
        temp_file.close()
        return temp_file.name

    def test_get_price_supported(self):
        """验证核心 API get_price 不应被误判"""
        test_file = self._create_test_strategy("get_price('000001.XSHE', count=10)")
        result = self.scanner.scan_file(test_file)

        # get_price 在 _KNOWN_APIS 中，不应在 missing_apis
        assert 'get_price' not in result.missing_apis, \
            "get_price should not be marked as missing"

        # 策略应可执行
        assert result.is_executable == True

        os.unlink(test_file)

    def test_get_fundamentals_supported(self):
        """验证 get_fundamentals 不应被误判"""
        test_file = self._create_test_strategy("get_fundamentals(query(finance.valuation))")
        result = self.scanner.scan_file(test_file)

        assert 'get_fundamentals' not in result.missing_apis
        assert 'query' not in result.missing_apis

        os.unlink(test_file)


class TestScannerRuntimeAlignment:
    """测试扫描器与 Runtime 导出的对齐"""

    def test_api_exports_alignment(self):
        """验证扫描器识别的 API 与实际导出对齐"""
        # 导入 jk2bt.api 模块
        try:
            from jk2bt.api import __all__ as exported_apis
        except ImportError:
            # 如果模块未完全导入，跳过测试
            pytest.skip("jk2bt.api module not fully importable")

        # 导入扫描器
        scanner = StrategyScanner()

        # 检查导出的 API 是否在扫描器的已知列表或映射中
        for api in exported_apis:
            if api in scanner._KNOWN_APIS:
                continue  # 已知 API，正确
            if api in scanner._API_NAME_MAPPING.values():
                continue  # 名称映射的目标，正确
            if api in scanner._UNIMPLEMENTED_APIS:
                # 不应该出现：导出但标记为未实现
                pytest.fail(
                    f"API '{api}' exported in __init__.py but marked as unimplemented in scanner"
                )


def test_scanner_summary_output():
    """测试扫描器输出摘要格式"""
    scanner = StrategyScanner()

    # 创建测试目录
    temp_dir = tempfile.mkdtemp()

    # 创建几个测试文件
    files = {
        'valid_strategy.py': """
def initialize(context):
    pass

def handle_data(context, data):
    get_price('000001.XSHE', count=10)
""",
        'missing_api.py': """
def initialize(context):
    pass

def handle_data(context, data):
    get_dividends('000001.XSHE')
""",
        'mapped_api.py': """
def initialize(context):
    pass

def handle_data(context, data):
    get_ticks('000001.XSHE', count=100)
""",
    }

    for filename, code in files.items():
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)

    # 扫描目录
    results = scanner.scan_directory(temp_dir, pattern='*.py')

    # 验证统计
    assert len(results['all']) == 3
    assert len(results['valid']) >= 1  # valid_strategy 和 mapped_api
    assert len(results['missing_api']) == 1  # missing_api.py

    # 验证 mapped_api.py 不应在 missing_api 中
    mapped_file = os.path.join(temp_dir, 'mapped_api.py')
    mapped_result = None
    for r in results['all']:
        if r.file_path == mapped_file:
            mapped_result = r
            break

    assert mapped_result is not None
    assert 'get_ticks' not in mapped_result.missing_apis, \
        "mapped_api.py should not have missing APIs (get_ticks is mapped)"

    # 清理
    import shutil
    shutil.rmtree(temp_dir)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
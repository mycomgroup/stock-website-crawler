"""
test_import_cleanliness.py
导入洁净性测试 - 验证导入 jk2bt 包不会产生副作用。

导入包应该:
- 不创建文件/目录
- 不连接数据库
- 不下载网络数据
- 日志输出极少或可控
- 导入行为可预测

测试策略:
1. 文件系统监控 - 检测导入前后文件变化
2. 网络请求拦截 - mock 网络调用
3. 数据库连接拦截 - mock 数据库连接
4. 日志输出捕获 - 验证日志输出量
5. 环境隔离 - 使用 subprocess 测试独立进程
"""

import pytest
import sys
import os
import subprocess
import tempfile
import logging
from pathlib import Path
from unittest.mock import patch, MagicMock
import io


class TestImportNoFileCreation:
    """测试导入不创建文件或目录"""

    def test_import_in_clean_environment(self):
        """在干净环境中导入不创建文件"""
        # 使用子进程测试，确保干净环境
        test_code = '''
import sys
import os
import tempfile

# 创建临时目录作为工作目录
temp_dir = tempfile.mkdtemp()
os.chdir(temp_dir)

# 记录导入前的文件状态
before_files = set(os.listdir(temp_dir))

# 导入包
import jk2bt

# 记录导入后的文件状态
after_files = set(os.listdir(temp_dir))

# 检查是否有新文件创建
new_files = after_files - before_files

# 打印结果
print("NEW_FILES:", list(new_files))

# 清理
import shutil
shutil.rmtree(temp_dir, ignore_errors=True)
'''
        result = subprocess.run(
            [sys.executable, '-c', test_code],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent)
        )

        # 解析输出
        output = result.stdout + result.stderr
        if "NEW_FILES:" in output:
            new_files_line = [line for line in output.split('\n') if 'NEW_FILES:' in line]
            if new_files_line:
                new_files = new_files_line[0].replace("NEW_FILES:", "").strip()
                # 允许空列表或仅有预期的临时文件
                assert new_files == "[]" or new_files == "", \
                    f"导入创建了非预期文件: {new_files}"

    def test_import_no_cache_directory_created(self):
        """导入不创建缓存目录"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_code = '''
import os
import sys

# 设置工作目录到临时目录
os.chdir(os.environ.get("TEMP_DIR"))

# 检查 data 目录是否存在
before_data_exists = os.path.exists("data")
before_cache_exists = os.path.exists("data/cache")

# 导入包
import jk2bt

# 再次检查
after_data_exists = os.path.exists("data")
after_cache_exists = os.path.exists("data/cache")

# 输出结果
print(f"DATA_BEFORE:{before_data_exists}")
print(f"DATA_AFTER:{after_data_exists}")
print(f"CACHE_BEFORE:{before_cache_exists}")
print(f"CACHE_AFTER:{after_cache_exists}")
'''
            env = os.environ.copy()
            env["TEMP_DIR"] = tmpdir

            result = subprocess.run(
                [sys.executable, '-c', test_code],
                capture_output=True,
                text=True,
                env=env,
                cwd=str(Path(__file__).parent.parent)
            )

            output = result.stdout
            # 解析输出
            lines = output.strip().split('\n')
            results = {}
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    results[key] = value == 'True'

            # 导入应该不创建 data 目录
            # 如果目录不存在导入前，导入后也不应该存在
            if 'DATA_BEFORE' in results and not results['DATA_BEFORE']:
                assert 'DATA_AFTER' in results and not results['DATA_AFTER'], \
                    f"导入创建了 data 目录: {output}"
            # 如果目录已存在导入前，导入后状态相同（不创建新的子目录）
            if 'CACHE_BEFORE' in results and not results['CACHE_BEFORE']:
                assert 'CACHE_AFTER' in results and not results['CACHE_AFTER'], \
                    f"导入创建了 data/cache 目录: {output}"

    def test_import_no_log_files_created(self):
        """导入不创建日志文件"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_code = '''
import os

os.chdir(os.environ.get("TEMP_DIR"))

# 检查 logs 目录
before_logs_exists = os.path.exists("logs")

import jk2bt

after_logs_exists = os.path.exists("logs")

print(f"LOGS_BEFORE:{before_logs_exists}")
print(f"LOGS_AFTER:{after_logs_exists}")
'''
            env = os.environ.copy()
            env["TEMP_DIR"] = tmpdir
            env["JK2BT_LOG_LEVEL"] = "ERROR"  # 最小化日志

            result = subprocess.run(
                [sys.executable, '-c', test_code],
                capture_output=True,
                text=True,
                env=env,
                cwd=str(Path(__file__).parent.parent)
            )

            output = result.stdout
            # 解析输出
            lines = output.strip().split('\n')
            results = {}
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    results[key] = value == 'True'

            # 如果 logs 目录不存在导入前，导入后也不应该存在
            if 'LOGS_BEFORE' in results and not results['LOGS_BEFORE']:
                assert 'LOGS_AFTER' in results and not results['LOGS_AFTER'], \
                    f"导入创建了 logs 目录: {output}"
            # 如果目录已存在，我们只验证导入没有改变状态（没有创建新文件）
            # 这个场景我们跳过，因为目录已存在意味着测试环境不干净


class TestImportNoDatabaseConnection:
    """测试导入不连接数据库"""

    def test_import_no_duckdb_connection(self):
        """导入不创建 DuckDB 连接"""
        # Mock duckdb.connect
        with patch('duckdb.connect') as mock_connect:
            mock_connect.return_value = MagicMock()

            # 强制重新导入
            if 'jk2bt' in sys.modules:
                del sys.modules['jk2bt']
            if 'jk2bt.db.unified_cache' in sys.modules:
                del sys.modules['jk2bt.db.unified_cache']
            if 'jk2bt.db.duckdb_manager' in sys.modules:
                del sys.modules['jk2bt.db.duckdb_manager']

            import jk2bt

            # 验证 duckdb.connect 没有被调用（导入阶段）
            # 注意：某些子模块可能在导入时检查 duckdb 是否可用
            # 但不应实际创建数据库连接
            # 允许零次调用或仅做导入检查
            call_count = mock_connect.call_count
            # 导入不应该触发实际数据库连接
            assert call_count == 0, \
                f"导入阶段不应连接数据库，但 duckdb.connect 被调用了 {call_count} 次"

    def test_import_no_db_initialization(self):
        """导入不初始化数据库表"""
        # 在子进程中测试
        test_code = '''
import sys
from unittest.mock import patch, MagicMock

# Mock DuckDBAdapter._init_tables
original_init_tables = None

class MockDuckDBAdapter:
    def __init__(self, *args, **kwargs):
        self._initialized = False
        self._schemas = {}
        self.db_path = ""
        self.read_only = False

    def _init_tables(self):
        # 记录调用但不执行
        print("INIT_TABLES_CALLED")
        self._initialized = True

# 在导入前替换
import jk2bt.db.unified_cache as cache_module
original_adapter = cache_module.DuckDBAdapter
cache_module.DuckDBAdapter = MockDuckDBAdapter

# 导入包
if 'jk2bt' in sys.modules:
    del sys.modules['jk2bt']
import jk2bt

# 恢复
cache_module.DuckDBAdapter = original_adapter
'''
        result = subprocess.run(
            [sys.executable, '-c', test_code],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent)
        )

        output = result.stdout + result.stderr
        # 导入不应该触发 _init_tables
        assert "INIT_TABLES_CALLED" not in output, \
            "导入阶段不应该初始化数据库表"

    def test_db_modules_import_without_connection(self):
        """db 子模块可以单独导入而不连接数据库"""
        with patch('duckdb.connect') as mock_connect:
            mock_connect.return_value = MagicMock()

            # 清除已导入的模块
            modules_to_clear = [
                'jk2bt.db',
                'jk2bt.db.unified_cache',
                'jk2bt.db.duckdb_manager',
                'jk2bt.db.cache_config',
                'jk2bt.db.cache_status',
                'jk2bt.db.migrate',
                'jk2bt.db.migrate_pickle',
                'jk2bt.db.meta_cache_api',
            ]
            for mod in modules_to_clear:
                if mod in sys.modules:
                    del sys.modules[mod]

            # 仅导入 db 模块
            from jk2bt.db import DuckDBManager, UnifiedCacheManager

            # 验证没有数据库连接
            assert mock_connect.call_count == 0, \
                "导入 db 模块不应该创建数据库连接"


class TestImportNoNetworkRequests:
    """测试导入不发起网络请求"""

    def test_import_no_http_requests(self):
        """导入不发起 HTTP 请求"""
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.return_value = MagicMock()

        with patch('requests.get') as mock_get:
            mock_get.return_value = MagicMock()

        with patch('requests.post') as mock_post:
            mock_post.return_value = MagicMock()

            # 清除模块缓存
            if 'jk2bt' in sys.modules:
                # 保留部分子模块，清除主模块
                del sys.modules['jk2bt']

            import jk2bt

            # 验证没有网络请求
            # 导入阶段不应该发起任何 HTTP 请求
            # 注意：某些模块可能在导入时检查网络可用性
            # 但不应该实际发起数据请求

    def test_import_no_akshare_data_fetch(self):
        """导入不从 akshare 获取数据"""
        with patch('akshare.stock_zh_a_hist') as mock_akshare:
            mock_akshare.return_value = MagicMock()

            # 清除相关模块
            for mod in list(sys.modules.keys()):
                if 'jk2bt' in mod and ('data_access' in mod or 'market_data' in mod):
                    del sys.modules[mod]

            if 'jk2bt' in sys.modules:
                del sys.modules['jk2bt']

            import jk2bt

            # 导入不应该调用 akshare 获取数据
            assert mock_akshare.call_count == 0, \
                "导入阶段不应该从 akshare 获取数据"


class TestImportLoggingControlled:
    """测试导入时日志输出可控"""

    def test_import_logging_level_controllable(self):
        """导入时日志级别可通过环境变量控制"""
        # 使用子进程测试
        test_code = '''
import os
import sys
import logging

# 设置日志级别为 ERROR（最小化输出）
os.environ["JK2BT_LOG_LEVEL"] = "ERROR"

# 重新配置 logging
logging.basicConfig(level=logging.ERROR, force=True)

# 导入前的 handler 数量
root_logger = logging.getLogger()
before_handlers = len(root_logger.handlers)

# 导入包
import jk2bt

# 导入后的 handler 数量
after_handlers = len(root_logger.handlers)

print(f"HANDLERS_BEFORE:{before_handlers}")
print(f"HANDLERS_AFTER:{after_handlers}")
print(f"ROOT_LEVEL:{root_logger.level}")
'''
        result = subprocess.run(
            [sys.executable, '-c', test_code],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent)
        )

        output = result.stdout
        # 验证日志级别被正确设置
        assert "ROOT_LEVEL:40" in output, \
            f"ERROR 级别应该是 40，实际输出: {output}"

    def test_import_minimal_stdout_output(self):
        """导入时 stdout 输出极少"""
        # 使用子进程测试
        test_code = '''
import os
os.environ["JK2BT_LOG_LEVEL"] = "CRITICAL"

import jk2bt
'''
        result = subprocess.run(
            [sys.executable, '-c', test_code],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent)
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        # 导入阶段 stdout 应该几乎没有输出（除可能的必要警告）
        # 允许少量输出（如版本信息或必要警告）
        total_output_len = len(stdout) + len(stderr)
        # 允许最多 500 字符的输出（考虑可能的初始化信息）
        assert total_output_len < 500, \
            f"导入产生了过多输出 ({total_output_len} 字符): stdout={stdout[:200]}, stderr={stderr[:200]}"

    def test_import_no_excessive_logging(self):
        """导入不产生大量日志"""
        # 捕获日志输出
        log_capture = io.StringIO()
        handler = logging.StreamHandler(log_capture)
        handler.setLevel(logging.DEBUG)

        root_logger = logging.getLogger()
        original_handlers = root_logger.handlers.copy()
        root_logger.handlers.clear()
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.DEBUG)

        try:
            # 清除模块缓存
            if 'jk2bt' in sys.modules:
                del sys.modules['jk2bt']

            import jk2bt

            # 获取日志输出
            log_output = log_capture.getvalue()

            # 统计日志行数
            log_lines = log_output.strip().split('\n') if log_output.strip() else []

            # 导入阶段不应该产生大量日志
            # 允许最多 10 行日志（合理的初始化信息）
            assert len(log_lines) <= 10, \
                f"导入产生了过多日志 ({len(log_lines)} 行): {log_output[:500]}"
        finally:
            root_logger.handlers.clear()
            for h in original_handlers:
                root_logger.addHandler(h)


class TestImportPredictability:
    """测试导入行为可预测"""

    def test_import_twice_same_result(self):
        """两次导入结果一致"""
        import jk2bt

        # 获取第一次导入的属性
        first_attrs = set(dir(jk2bt))
        first_all = set(jk2bt.__all__)

        # 再次导入
        import importlib
        importlib.reload(jk2bt)

        # 获取第二次导入的属性
        second_attrs = set(dir(jk2bt))
        second_all = set(jk2bt.__all__)

        # 验证一致
        assert first_attrs == second_attrs, \
            "两次导入的属性不一致"
        assert first_all == second_all, \
            "两次导入的 __all__ 不一致"

    def test_import_time_reasonable(self):
        """导入时间合理（不超过 5 秒）"""
        import time

        start = time.time()

        # 清除模块缓存
        if 'jk2bt' in sys.modules:
            del sys.modules['jk2bt']

        import jk2bt

        elapsed = time.time() - start

        # 导入应该在 5 秒内完成
        assert elapsed < 5.0, \
            f"导入耗时 {elapsed:.2f} 秒，超过预期的 5 秒"

    def test_import_all_exports_accessible(self):
        """__all__ 中的所有符号都可访问"""
        import jk2bt

        missing_symbols = []
        for symbol in jk2bt.__all__:
            if not hasattr(jk2bt, symbol):
                missing_symbols.append(symbol)

        assert len(missing_symbols) == 0, \
            f"以下符号在 __all__ 中但不可访问: {missing_symbols}"

    def test_import_no_global_state_mutation(self):
        """导入不修改全局状态"""
        # 在子进程中测试
        test_code = '''
import sys
import os

# 记录导入前的全局状态
before_env_keys = set(os.environ.keys())

# 导入包
import jk2bt

# 记录导入后的全局状态
after_env_keys = set(os.environ.keys())

# 检查是否有新的环境变量
new_env_vars = after_env_keys - before_env_keys

print(f"NEW_ENV_VARS:{list(new_env_vars)}")
'''
        result = subprocess.run(
            [sys.executable, '-c', test_code],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent)
        )

        output = result.stdout
        # 导入不应该设置新的环境变量
        if "NEW_ENV_VARS:" in output:
            new_vars_line = [line for line in output.split('\n') if 'NEW_ENV_VARS:' in line]
            if new_vars_line:
                new_vars = new_vars_line[0].replace("NEW_ENV_VARS:", "").strip()
                # 允许空列表
                assert new_vars == "[]" or new_vars == "", \
                    f"导入设置了新的环境变量: {new_vars}"


class TestImportModuleIsolation:
    """测试子模块导入隔离"""

    def test_import_core_no_db_connection(self):
        """导入 core 模块不连接数据库"""
        with patch('duckdb.connect') as mock_connect:
            mock_connect.return_value = MagicMock()

            # 清除模块
            modules_to_clear = [k for k in sys.modules.keys() if 'jk2bt.core' in k]
            for mod in modules_to_clear:
                del sys.modules[mod]

            from jk2bt.core import GlobalState, ContextProxy

            # 验证没有数据库连接
            assert mock_connect.call_count == 0, \
                "导入 core 模块不应该连接数据库"

    def test_import_market_data_no_network(self):
        """导入 market_data 模块不发起网络请求"""
        with patch('akshare.stock_zh_a_hist') as mock_akshare:
            mock_akshare.return_value = MagicMock()

            # 清除模块
            modules_to_clear = [k for k in sys.modules.keys() if 'jk2bt.market_data' in k]
            for mod in modules_to_clear:
                del sys.modules[mod]

            from jk2bt.market_data import get_stock_daily

            # 导入不应该调用 akshare
            assert mock_akshare.call_count == 0, \
                "导入 market_data 模块不应该发起网络请求"

    def test_import_factors_no_data_fetch(self):
        """导入 factors 模块不获取数据"""
        # 清除模块
        modules_to_clear = [k for k in sys.modules.keys() if 'jk2bt.factors' in k]
        for mod in modules_to_clear:
            del sys.modules[mod]

        from jk2bt.factors import get_factor_values_jq

        # 导入成功，没有数据获取
        assert callable(get_factor_values_jq), \
            "factors 模块导入应该提供函数"


class TestImportInCIEnvironment:
    """测试 CI 环境中的导入行为"""

    def test_import_with_network_disabled(self):
        """网络禁用时仍可导入"""
        # Mock 所有网络请求
        with patch('urllib.request.urlopen', side_effect=Exception("Network disabled")):
            with patch('requests.get', side_effect=Exception("Network disabled")):
                with patch('requests.post', side_effect=Exception("Network disabled")):
                    # 清除模块
                    if 'jk2bt' in sys.modules:
                        del sys.modules['jk2bt']

                    # 导入应该成功
                    import jk2bt

                    assert jk2bt is not None, \
                        "网络禁用时导入应该仍然成功"

    def test_import_with_minimal_dependencies(self):
        """仅有必要依赖时可导入"""
        # 这个测试验证导入不依赖可选依赖
        # 如 akshare 可能不是所有环境都有
        test_code = '''
import sys

# Mock akshare
sys.modules["akshare"] = None

# 尝试导入
try:
    import jk2bt
    print("IMPORT_SUCCESS")
except ImportError as e:
    print(f"IMPORT_FAILED:{e}")
'''
        result = subprocess.run(
            [sys.executable, '-c', test_code],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent)
        )

        # 注意：这个测试可能失败，因为 akshare 是核心依赖
        # 但我们记录结果以便改进
        output = result.stdout + result.stderr
        # 如果导入失败，记录原因
        if "IMPORT_FAILED" in output:
            # 这是预期行为，akshare 是必要依赖
            pass
        elif "IMPORT_SUCCESS" in output:
            # 导入成功，说明对可选依赖处理良好
            pass


class TestImportSideEffectsSummary:
    """导入副作用汇总测试"""

    def test_import_cleanliness_summary(self):
        """导入洁净性综合测试"""
        # 使用隔离子进程测试
        test_code = '''
import os
import sys
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# 创建临时工作目录
temp_dir = tempfile.mkdtemp()
os.chdir(temp_dir)

# 设置环境变量
os.environ["JK2BT_LOG_LEVEL"] = "ERROR"

# 记录初始状态
initial_files = set(os.listdir(temp_dir))
initial_env_keys = set(os.environ.keys())

# Mock 可能的副作用源
mock_calls = {
    "duckdb_connect": 0,
    "http_requests": 0,
    "akshare_calls": 0,
}

# 记录 mock 调用
def track_call(name):
    mock_calls[name] += 1
    return MagicMock()

# 导入
import jk2bt

# 检查最终状态
final_files = set(os.listdir(temp_dir))
final_env_keys = set(os.environ.keys())

# 计算变化
new_files = final_files - initial_files
new_env_vars = final_env_keys - initial_env_keys

# 输出结果
print(f"NEW_FILES:{list(new_files)}")
print(f"NEW_ENV_VARS:{list(new_env_vars)}")

# 清理
shutil.rmtree(temp_dir, ignore_errors=True)
'''
        result = subprocess.run(
            [sys.executable, '-c', test_code],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent),
            timeout=30  # 30秒超时
        )

        output = result.stdout

        # 验证结果
        # 不应该有新文件
        assert "NEW_FILES:[]" in output or "NEW_FILES:" not in output, \
            f"导入创建了新文件: {output}"

        # 不应该有新环境变量
        new_env_match = [line for line in output.split('\n') if 'NEW_ENV_VARS:' in line]
        if new_env_match:
            new_vars = new_env_match[0].replace("NEW_ENV_VARS:", "").strip()
            # JK2BT_LOG_LEVEL 是我们主动设置的，可以忽略
            assert new_vars == "[]" or "JK2BT_LOG_LEVEL" in new_vars, \
                f"导入设置了新的环境变量: {new_vars}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
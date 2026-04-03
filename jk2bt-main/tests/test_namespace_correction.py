"""
测试 Runner 命名空间纠偏
验证:
1. 编码回退支持 (utf-8, gbk, gb2312, latin-1)
2. get_price 参数签名正确 (count, frequency, panel)
3. get_all_trade_days/get_extras/get_billboard_list 绑定正确
4. 导入预处理正确移除 jqdata/jqlib 等模块
5. 错误处理明确抛出异常
6. 策略命名空间完整性
"""

import tempfile
import pytest
import inspect


class TestEncodingFallback:
    """编码回退机制测试"""

    def test_utf8_encoding(self, tmp_path):
        utf8_strategy = """
def initialize(context):
    log.info('UTF-8 策略初始化')
    g.num = 10

def handle_data(context):
    pass
"""
        strategy_file = tmp_path / "strategy_utf8.txt"
        strategy_file.write_text(utf8_strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None
        assert "initialize" in funcs
        assert "handle_data" in funcs

    def test_gbk_encoding(self, tmp_path):
        gbk_strategy = """
def initialize(context):
    log.info('GBK 编码策略初始化')
    g.stocks = ['贵州茅台', '中国平安']

def handle_data(context):
    pass
"""
        strategy_file = tmp_path / "strategy_gbk.txt"
        strategy_file.write_text(gbk_strategy, encoding="gbk")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None
        assert "initialize" in funcs

    def test_gb2312_encoding(self, tmp_path):
        gb2312_strategy = """
def initialize(context):
    log.info('GB2312 策略')
    pass
"""
        strategy_file = tmp_path / "strategy_gb2312.txt"
        strategy_file.write_text(gb2312_strategy, encoding="gb2312")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_latin1_encoding(self, tmp_path):
        latin1_strategy = """
def initialize(context):
    log.info('Latin-1 strategy')
    pass
"""
        strategy_file = tmp_path / "strategy_latin1.txt"
        strategy_file.write_text(latin1_strategy, encoding="latin-1")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_file_not_found(self):
        from jk2bt import load_jq_strategy

        with pytest.raises(FileNotFoundError):
            load_jq_strategy("/nonexistent/path/strategy.txt")

    def test_syntax_error_reporting(self, tmp_path):
        bad_syntax = """
def initialize(context):
    log.info('test'
    # missing closing paren
"""
        strategy_file = tmp_path / "bad_syntax.txt"
        strategy_file.write_text(bad_syntax, encoding="utf-8")

        from jk2bt import load_jq_strategy

        with pytest.raises(SyntaxError):
            load_jq_strategy(str(strategy_file))

    def test_runtime_error_reporting(self, tmp_path):
        bad_runtime = """
x = 1 / 0

def initialize(context):
    pass
"""
        strategy_file = tmp_path / "bad_runtime.txt"
        strategy_file.write_text(bad_runtime, encoding="utf-8")

        from jk2bt import load_jq_strategy

        with pytest.raises(RuntimeError):
            load_jq_strategy(str(strategy_file))

    def test_empty_strategy_file(self, tmp_path):
        empty_strategy = ""
        strategy_file = tmp_path / "empty.txt"
        strategy_file.write_text(empty_strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None
        assert len(funcs) == 0

    def test_binary_like_content(self, tmp_path):
        content = """
def initialize(context):
    # Some special chars
    pass
"""
        strategy_file = tmp_path / "binary_like.txt"
        strategy_file.write_text(content, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None


class TestNamespaceBinding:
    """命名空间绑定测试 - 通过策略文件验证"""

    def test_get_price_signature(self):
        from jk2bt.core.strategy_base import (
            get_price_jq,
        )

        sig = inspect.signature(get_price_jq)
        params = list(sig.parameters.keys())

        assert "symbols" in params
        assert "start_date" in params
        assert "end_date" in params
        assert "frequency" in params
        assert "fields" in params
        assert "count" in params
        assert "panel" in params
        assert "adjust" in params

    def test_get_all_trade_days_signature(self):
        from jk2bt.core.strategy_base import (
            get_all_trade_days_jq,
        )

        sig = inspect.signature(get_all_trade_days_jq)
        params = list(sig.parameters.keys())

        assert "cache_dir" in params
        assert "force_update" in params

    def test_get_extras_signature(self):
        from jk2bt.core.strategy_base import (
            get_extras_jq,
        )

        sig = inspect.signature(get_extras_jq)
        params = list(sig.parameters.keys())

        assert "field" in params
        assert "securities" in params
        assert "start_date" in params
        assert "end_date" in params

    def test_get_billboard_list_signature(self):
        from jk2bt.core.strategy_base import (
            get_billboard_list_jq,
        )

        sig = inspect.signature(get_billboard_list_jq)
        params = list(sig.parameters.keys())

        assert "stock_list" in params
        assert "end_date" in params
        assert "count" in params

    def test_get_bars_signature(self):
        from jk2bt.core.strategy_base import (
            get_bars_jq,
        )

        sig = inspect.signature(get_bars_jq)
        params = list(sig.parameters.keys())

        assert "security" in params
        assert "count" in params
        assert "unit" in params
        assert "fields" in params

    def test_get_price_in_strategy_namespace(self, tmp_path):
        strategy = """
def test_func(context):
    df = get_price('600519.XSHG', end_date='2023-12-31', count=10, frequency='daily', panel=False)
    return df
"""
        strategy_file = tmp_path / "test_price.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert "test_func" in funcs

    def test_get_all_trade_days_in_strategy_namespace(self, tmp_path):
        strategy = """
def test_func(context):
    days = get_all_trade_days()
    return days
"""
        strategy_file = tmp_path / "test_days.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert "test_func" in funcs

    def test_get_extras_in_strategy_namespace(self, tmp_path):
        strategy = """
def test_func(context):
    st_info = get_extras('is_st', ['600519.XSHG'])
    return st_info
"""
        strategy_file = tmp_path / "test_extras.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert "test_func" in funcs

    def test_get_billboard_list_in_strategy_namespace(self, tmp_path):
        strategy = """
def test_func(context):
    df = get_billboard_list()
    return df
"""
        strategy_file = tmp_path / "test_billboard.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert "test_func" in funcs


class TestImportPreprocessing:
    """导入预处理测试"""

    def test_jqdata_import_removed(self, tmp_path):
        strategy = """
from jqdata import get_price, get_fundamentals

def initialize(context):
    log.info('初始化')
"""
        strategy_file = tmp_path / "jqdata_import.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None
        assert "initialize" in funcs

    def test_jqdata_import_multiline_removed(self, tmp_path):
        strategy = """
from jqdata import (
    get_price,
    get_fundamentals,
    get_all_securities
)

def initialize(context):
    pass
"""
        strategy_file = tmp_path / "jqdata_multiline.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_import_jqdata_removed(self, tmp_path):
        strategy = """
import jqdata

def initialize(context):
    pass
"""
        strategy_file = tmp_path / "import_jqdata.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_jqlib_import_removed(self, tmp_path):
        strategy = """
from jqlib.technical_analysis import *

def initialize(context):
    pass
"""
        strategy_file = tmp_path / "jqlib_import.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_from_jqlib_removed(self, tmp_path):
        strategy = """
from jqlib import something

def initialize(context):
    pass
"""
        strategy_file = tmp_path / "from_jqlib.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_kuanke_import_removed(self, tmp_path):
        strategy = """
from kuanke import *
import kuanke

def initialize(context):
    pass
"""
        strategy_file = tmp_path / "kuanke_import.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_jqfactor_import_removed(self, tmp_path):
        strategy = """
from jqfactor import get_factor_values
import jqfactor

def initialize(context):
    pass
"""
        strategy_file = tmp_path / "jqfactor_import.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_normal_imports_preserved(self, tmp_path):
        strategy = """
import pandas as pd
import numpy as np

def initialize(context):
    df = pd.DataFrame()
"""
        strategy_file = tmp_path / "normal_import.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None
        assert "initialize" in funcs

    def test_from_pandas_import_preserved(self, tmp_path):
        strategy = """
from pandas import DataFrame
from datetime import datetime

def initialize(context):
    df = DataFrame()
"""
        strategy_file = tmp_path / "pandas_import.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None
        assert "initialize" in funcs

    def test_mixed_imports(self, tmp_path):
        strategy = """
from jqdata import get_price
import pandas as pd
import numpy as np
from datetime import datetime

def initialize(context):
    df = pd.DataFrame()
"""
        strategy_file = tmp_path / "mixed_import.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None
        assert "initialize" in funcs


class TestGlobalNamespaceCompleteness:
    """策略全局命名空间完整性测试"""

    def test_basic_python_builtins(self, tmp_path):
        strategy = """
def initialize(context):
    x = list([1, 2, 3])
    y = dict({'a': 1})
    z = set([1, 2])
    s = sum([1, 2, 3])
    m = max([1, 2, 3])
    n = min([1, 2, 3])
    r = round(1.5)
    a = abs(-1)
    l = len([1, 2, 3])
"""
        strategy_file = tmp_path / "builtins.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None
        assert "initialize" in funcs

    def test_numpy_pandas_available(self, tmp_path):
        strategy = """
def initialize(context):
    arr = np.array([1, 2, 3])
    df = pd.DataFrame({'a': [1, 2]})
"""
        strategy_file = tmp_path / "np_pd.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_datetime_available(self, tmp_path):
        strategy = """
def initialize(context):
    dt = datetime.now()
    td = timedelta(days=1)
    d = date.today()
"""
        strategy_file = tmp_path / "datetime.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_jq_globals_g_and_log(self, tmp_path):
        strategy = """
def initialize(context):
    g.stocks = []
    g.num = 10
    log.info('初始化')
    log.warn('警告')
"""
        strategy_file = tmp_path / "globals.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_jq_api_get_fundamentals(self, tmp_path):
        strategy = """
def initialize(context):
    q = query(valuation.pe_ratio)
    df = get_fundamentals(q)
"""
        strategy_file = tmp_path / "fundamentals.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_jq_api_get_all_securities(self, tmp_path):
        strategy = """
def initialize(context):
    all_stocks = get_all_securities()
    info = get_security_info('600519.XSHG')
"""
        strategy_file = tmp_path / "securities.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_jq_api_index_functions(self, tmp_path):
        strategy = """
def initialize(context):
    weights = get_index_weights('000300.XSHG')
    stocks = get_index_stocks('000300.XSHG')
"""
        strategy_file = tmp_path / "index.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_jq_api_history(self, tmp_path):
        strategy = """
def initialize(context):
    h = history(10, unit='1d', field='close', security='600519.XSHG')
"""
        strategy_file = tmp_path / "history.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_jq_api_order_functions(self, tmp_path):
        strategy = """
def handle_data(context):
    order_target('600519.XSHG', 100)
    order_value('600519.XSHG', 10000)
    order_target_value('600519.XSHG', 10000)
    order('600519.XSHG', 100)
"""
        strategy_file = tmp_path / "order.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None
        assert "handle_data" in funcs

    def test_jq_api_timer_functions(self, tmp_path):
        strategy = """
def initialize(context):
    run_monthly(my_func, 1, 'open')
    run_daily(my_func, 'after_close')
    run_weekly(my_func, 1, 'open')
    unschedule_all()

def my_func(context):
    pass
"""
        strategy_file = tmp_path / "timer.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_jq_api_config_functions(self, tmp_path):
        strategy = """
def initialize(context):
    set_option('use_real_price', True)
    set_benchmark('000300.XSHG')
    set_slippage(FixedSlippage(0.01))
    set_order_cost(OrderCost(open_tax=0, close_tax=0.001, open_commission=0.0003))
"""
        strategy_file = tmp_path / "config.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_current_data_in_namespace(self, tmp_path):
        strategy = """
def handle_data(context):
    current = get_current_data()
    price = current['600519.XSHG'].last_price
"""
        strategy_file = tmp_path / "current.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None


class TestComplexStrategy:
    """复杂策略场景测试"""

    def test_multi_function_strategy(self, tmp_path):
        strategy = """
def initialize(context):
    g.stocks = []
    g.num = 5
    log.info('初始化')
    run_monthly(rebalance, 1, 'open')

def rebalance(context):
    stocks = get_index_stocks('000300.XSHG')[:g.num]
    g.stocks = stocks
    
    for stock in context.portfolio.positions:
        if stock not in g.stocks:
            order_target(stock, 0)
    
    for stock in g.stocks:
        order_target_value(stock, context.portfolio.total_value / len(g.stocks))

def after_trading(context):
    log.info('收盘后处理')
"""
        strategy_file = tmp_path / "complex.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None
        assert "initialize" in funcs
        assert "rebalance" in funcs
        assert "after_trading" in funcs

    def test_class_based_strategy(self, tmp_path):
        strategy = """
class MyStrategy:
    def __init__(self):
        self.stocks = []
    
    def run(self, context):
        pass

def initialize(context):
    g.strategy = MyStrategy()
"""
        strategy_file = tmp_path / "class_based.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None
        assert "initialize" in funcs

    def test_nested_functions(self, tmp_path):
        strategy = """
def initialize(context):
    def inner_func():
        return 10
    
    g.value = inner_func()

def handle_data(context):
    pass
"""
        strategy_file = tmp_path / "nested.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_lambda_and_comprehensions(self, tmp_path):
        strategy = """
def initialize(context):
    stocks = ['600519.XSHG', '000858.XSHE']
    filtered = [s for s in stocks if s.startswith('6')]
    mapped = list(map(lambda x: x[:6], stocks))
"""
        strategy_file = tmp_path / "lambda.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_strategy_with_comments(self, tmp_path):
        strategy = """
# 这是一个测试策略
# 作者: test
# 日期: 2023-01-01

def initialize(context):
    # 初始化函数
    g.stocks = []  # 股票列表
    log.info('初始化完成')

def handle_data(context):
    # 每日执行
    pass
"""
        strategy_file = tmp_path / "comments.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None


class TestEdgeCases:
    """边界情况测试"""

    def test_binary_file_raises_error(self, tmp_path):
        binary_data = b"\xff\xfe\x00\x00\x01\x02\x03"
        strategy_file = tmp_path / "binary.txt"
        strategy_file.write_bytes(binary_data)

        from jk2bt import load_jq_strategy

        with pytest.raises((UnicodeDecodeError, RuntimeError)):
            load_jq_strategy(str(strategy_file))

    def test_strategy_with_tabs(self, tmp_path):
        strategy = """
def initialize(context):
\tg.stocks = []
\tlog.info('初始化')
"""
        strategy_file = tmp_path / "tabs.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_strategy_file_with_py_extension(self, tmp_path):
        strategy = """
def initialize(context):
    pass
"""
        strategy_file = tmp_path / "strategy.py"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_large_strategy_file(self, tmp_path):
        lines = ["def initialize(context):", "    pass"]
        for i in range(100):
            lines.append(f"def func_{i}(context):")
            lines.append(f"    return {i}")
        strategy = "\n".join(lines)

        strategy_file = tmp_path / "large.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None
        assert len(funcs) >= 100

    def test_strategy_with_special_characters(self, tmp_path):
        strategy = """
def initialize(context):
    # 特殊字符: @#$%^&*()_+-=[]{}|;':",./<>?
    msg = "Hello 世界"
    log.info(msg)
"""
        strategy_file = tmp_path / "special.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None

    def test_strategy_with_decorators(self, tmp_path):
        strategy = """
def my_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def initialize(context):
    pass
"""
        strategy_file = tmp_path / "decorator.txt"
        strategy_file.write_text(strategy, encoding="utf-8")

        from jk2bt import load_jq_strategy

        funcs = load_jq_strategy(str(strategy_file))
        assert funcs is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

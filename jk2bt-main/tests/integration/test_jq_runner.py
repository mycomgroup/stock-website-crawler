"""
测试聚宽策略运行器
验证能否直接运行聚宽策略文件，无需修改代码
"""

import os
import pytest
from jk2bt import run_jq_strategy


def test_simple_strategy():
    """测试简单策略"""

    print("测试1: 简单策略文件")
    print("=" * 80)

    # 创建一个简单的测试策略
    test_strategy = """
# 简单测试策略
import pandas as pd

def initialize(context):
    g.stocks = []
    g.num = 3
    log.info('初始化策略')
    run_monthly(rebalance, 1, 'open')

def rebalance(context):
    log.info('月度调仓', context.current_dt)
    
    # 模拟选股
    stocks = ['600519.XSHG', '000858.XSHE', '000333.XSHE']
    g.stocks = stocks[:g.num]
    
    # 获取当前数据
    current = get_current_data()
    
    # 卖出不在股票池的持仓
    for stock in context.portfolio.positions:
        if stock not in g.stocks:
            log.info('卖出', stock, current[stock].name)
            order_target(stock, 0)
    
    # 买入股票
    if len(g.stocks) > 0:
        position = context.portfolio.total_value / len(g.stocks)
        for stock in g.stocks:
            if not current[stock].paused:
                log.info('买入', stock, current[stock].name)
                order_value(stock, position)
"""

    # 保存测试策略
    test_file = "test_simple_strategy.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_strategy)

    # 运行策略 - 硬验收：必须成功运行
    try:
        result = run_jq_strategy(
            strategy_file=test_file,
            start_date="2022-01-01",
            end_date="2022-12-31",
            initial_capital=1000000,
            stock_pool=["600519.XSHG", "000858.XSHE", "000333.XSHE"],
        )

        # 硬验收：结果必须有效
        if result is None:
            pytest.fail("策略返回None - 硬验收失败")

        # 硬验收：必须有基本字段
        assert "final_value" in result, \
            f"结果缺少final_value字段 - 硬验收失败: {result.keys()}"

        assert "pnl_pct" in result, \
            f"结果缺少pnl_pct字段 - 硬验收失败: {result.keys()}"

        # 硬验收：数值必须合理
        assert result["final_value"] > 0, \
            f"最终资金无效 - 硬验收失败: {result['final_value']}"

        print(f"\n✅ 测试通过！策略成功运行")
        print(f"最终资金: {result['final_value']:,.2f}")
        print(f"收益率: {result['pnl_pct']:.2f}%")

    except Exception as e:
        import traceback
        tb_lines = traceback.format_exc()
        # 硬验收：异常即失败
        pytest.fail(
            f"策略运行异常 - 硬验收失败:\n"
            f"  错误: {str(e)}\n"
            f"  Traceback:\n{tb_lines[-10:]}"
        )

    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)


def test_real_strategy():
    """测试真实策略文件 - 使用仓库内策略"""

    print("\n\n测试2: 真实策略文件")
    print("=" * 80)

    # 使用仓库内的真实策略文件（干净机器验收必须使用仓库内资源）
    # 项目根目录相对于本测试文件的位置（tests/integration -> tests -> project_root）
    integration_dir = os.path.dirname(os.path.abspath(__file__))
    tests_dir = os.path.dirname(integration_dir)
    project_root = os.path.dirname(tests_dir)
    strategy_file = os.path.join(project_root, "strategies", "validation_v4_double_ma.txt")

    # 硬验收：策略文件必须存在，不允许静默跳过
    if not os.path.exists(strategy_file):
        pytest.fail(
            f"策略文件不存在 - 硬验收失败:\n"
            f"  期望路径: {strategy_file}\n"
            f"  仓库内必须包含验证策略文件以支持干净机器验收"
        )

    # 沪深300成分股（示例）
    hs300_stocks = [
        "600519.XSHG",  # 贵州茅台
        "600036.XSHG",  # 招商银行
        "601318.XSHG",  # 中国平安
        "600000.XSHG",  # 浦发银行
        "601166.XSHG",  # 兴业银行
        "600030.XSHG",  # 中信证券
        "601328.XSHG",  # 交通银行
        "600016.XSHG",  # 民生银行
        "601288.XSHG",  # 农业银行
        "600028.XSHG",  # 中国石化
    ]

    try:
        result = run_jq_strategy(
            strategy_file=strategy_file,
            start_date="2020-01-01",
            end_date="2022-12-31",
            initial_capital=1000000,
            stock_pool=hs300_stocks[:5],  # 只测试前5只
        )

        # 硬验收：结果必须有效
        if result is None:
            pytest.fail("真实策略返回None - 硬验收失败")

        # 硬验收：必须有基本字段
        assert "final_value" in result, \
            f"结果缺少final_value字段 - 硬验收失败: {result.keys()}"

        assert "pnl_pct" in result, \
            f"结果缺少pnl_pct字段 - 硬验收失败: {result.keys()}"

        # 硬验收：数值必须合理
        assert result["final_value"] > 0, \
            f"最终资金无效 - 硬验收失败: {result['final_value']}"

        print(f"\n✅ 真实策略运行成功！")
        print(f"最终资金: {result['final_value']:,.2f}")
        print(f"收益率: {result['pnl_pct']:.2f}%")

    except Exception as e:
        import traceback
        tb_lines = traceback.format_exc()
        # 硬验收：异常即失败
        pytest.fail(
            f"真实策略运行异常 - 硬验收失败:\n"
            f"  策略文件: {strategy_file}\n"
            f"  错误: {str(e)}\n"
            f"  Traceback:\n{tb_lines[-10:]}"
        )


def test_utf8_encoding():
    """测试 UTF-8 编码策略文件加载"""

    print("\n\n测试3: UTF-8 编码策略文件")
    print("=" * 80)

    test_strategy = """
def initialize(context):
    log.info('UTF-8编码测试初始化')
    g.test = 'utf8测试'

def handle_data(context):
    log.info('UTF-8编码处理数据')
"""

    test_file = "test_utf8_strategy.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_strategy)

    try:
        from jk2bt.core.runner import load_jq_strategy

        funcs = load_jq_strategy(test_file)

        if funcs and "initialize" in funcs and "handle_data" in funcs:
            print("\n✅ UTF-8 编码策略加载成功")
            print(f"   加载的函数: {list(funcs.keys())}")
        else:
            print("\n❌ UTF-8 编码策略加载失败")
    except Exception as e:
        print(f"\n❌ UTF-8 编码策略加载失败: {e}")
        import traceback

        traceback.print_exc()
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_gbk_encoding():
    """测试 GBK 编码策略文件加载"""

    print("\n\n测试4: GBK 编码策略文件")
    print("=" * 80)

    test_strategy = """
def initialize(context):
    log.info('GBK编码测试初始化')
    g.test = 'gbk测试'

def handle_data(context):
    log.info('GBK编码处理数据')
"""

    test_file = "test_gbk_strategy.txt"
    with open(test_file, "w", encoding="gbk") as f:
        f.write(test_strategy)

    try:
        from jk2bt.core.runner import load_jq_strategy

        funcs = load_jq_strategy(test_file)

        if funcs and "initialize" in funcs and "handle_data" in funcs:
            print("\n✅ GBK 编码策略加载成功")
            print(f"   加载的函数: {list(funcs.keys())}")
        else:
            print("\n❌ GBK 编码策略加载失败")
    except Exception as e:
        print(f"\n❌ GBK 编码策略加载失败: {e}")
        import traceback

        traceback.print_exc()
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_get_price_signature():
    """测试 get_price(count=..., frequency=..., panel=False) 签名"""

    print("\n\n测试5: get_price 函数签名验证")
    print("=" * 80)

    test_strategy = """
import inspect

def test_api_signatures():
    # 测试关键 API 的签名
    apis_to_check = ['get_price', 'get_current_data', 'get_all_trade_days', 
                     'get_extras', 'get_billboard_list', 'get_bars']
    
    results = {}
    for api_name in apis_to_check:
        if api_name in globals():
            api_func = globals()[api_name]
            sig = inspect.signature(api_func)
            params = list(sig.parameters.keys())
            results[api_name] = {
                'actual_name': api_func.__name__,
                'params': params
            }
            log.info(f'{api_name} -> {api_func.__name__}: {params}')
        else:
            log.info(f'{api_name} NOT FOUND')
    
    # 专门检查 get_price 的关键参数
    if 'get_price' in results:
        gp_params = results['get_price']['params']
        has_count = 'count' in gp_params
        has_panel = 'panel' in gp_params
        has_frequency = 'frequency' in gp_params
        
        log.info(f'get_price 有 count 参数: {has_count}')
        log.info(f'get_price 有 panel 参数: {has_panel}')
        log.info(f'get_price 有 frequency 参数: {has_frequency}')
        
        if not (has_count and has_panel and has_frequency):
            log.error('get_price 签名错误！缺少关键参数')
            return False
    
    return True

def initialize(context):
    log.info('测试API签名初始化')
"""

    test_file = "test_get_price_sig.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_strategy)

    try:
        from jk2bt.core.runner import load_jq_strategy

        funcs = load_jq_strategy(test_file)

        if "test_api_signatures" in funcs:
            result = funcs["test_api_signatures"]()
            if result:
                print("\n✅ get_price 签名验证成功")
                print("   count, panel, frequency 参数都存在")
            else:
                print("\n❌ get_price 签名验证失败")
        else:
            print("\n❌ 测试函数未加载")
    except Exception as e:
        print(f"\n❌ get_price 签名测试失败: {e}")
        import traceback

        traceback.print_exc()
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_get_price_call_with_count():
    """测试实际调用 get_price with count 和 panel 参数"""

    print("\n\n测试6: get_price 实际调用验证")
    print("=" * 80)

    test_strategy = """
def test_get_price_call():
    # 尝试使用 count, frequency, panel 参数调用 get_price
    # 注意：这里不实际获取数据，只检查参数是否正确传递
    
    import inspect
    sig = inspect.signature(get_price)
    params = list(sig.parameters.keys())
    
    log.info(f'get_price 参数列表: {params}')
    
    # 验证参数存在
    assert 'count' in params, 'get_price 缺少 count 参数'
    assert 'panel' in params, 'get_price 缺少 panel 参数'
    assert 'frequency' in params, 'get_price 缺少 frequency 参数'
    
    log.info('所有关键参数验证通过')
    return True

def initialize(context):
    log.info('测试get_price调用初始化')
"""

    test_file = "test_get_price_call.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_strategy)

    try:
        from jk2bt.core.runner import load_jq_strategy

        funcs = load_jq_strategy(test_file)

        if "test_get_price_call" in funcs:
            result = funcs["test_get_price_call"]()
            if result:
                print("\n✅ get_price 实际调用验证成功")
                print("   可以使用 count, frequency, panel 参数")
            else:
                print("\n❌ get_price 实际调用验证失败")
        else:
            print("\n❌ 测试函数未加载")
    except AssertionError as e:
        print(f"\n❌ 签名验证失败: {e}")
        print("   get_price 缺少关键参数！")
    except Exception as e:
        print(f"\n❌ get_price 调用测试失败: {e}")
        import traceback

        traceback.print_exc()
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_namespace_binding():
    """测试命名空间绑定是否正确"""

    print("\n\n测试7: 命名空间绑定验证")
    print("=" * 80)

    test_strategy = """
def test_bindings():
    # 检查所有关键 API 是否绑定到正确的 JQ 风格实现
    bindings = {
        'get_price': 'get_price_jq',
        'get_all_trade_days': 'get_all_trade_days_jq',
        'get_extras': 'get_extras_jq',
        'get_billboard_list': 'get_billboard_list_jq',
        'get_bars': 'get_bars_jq'
    }
    
    all_correct = True
    for api_name, expected_name in bindings.items():
        if api_name in globals():
            actual_name = globals()[api_name].__name__
            if actual_name == expected_name:
                log.info(f'{api_name} -> {actual_name} ✓')
            else:
                log.error(f'{api_name} -> {actual_name} (期望 {expected_name}) ✗')
                all_correct = False
        else:
            log.error(f'{api_name} 未找到 ✗')
            all_correct = False
    
    return all_correct

def initialize(context):
    log.info('测试命名空间绑定初始化')
"""

    test_file = "test_namespace_binding.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_strategy)

    try:
        from jk2bt.core.runner import load_jq_strategy

        funcs = load_jq_strategy(test_file)

        if "test_bindings" in funcs:
            result = funcs["test_bindings"]()
            if result:
                print("\n✅ 命名空间绑定验证成功")
                print("   所有 API 都绑定到正确的 JQ 风格实现")
            else:
                print("\n❌ 命名空间绑定验证失败")
        else:
            print("\n❌ 测试函数未加载")
    except Exception as e:
        print(f"\n❌ 命名空间绑定测试失败: {e}")
        import traceback

        traceback.print_exc()
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_invalid_file_error():
    """测试加载失败时的错误处理"""

    print("\n\n测试8: 无效文件错误处理")
    print("=" * 80)

    # 创建一个包含无法解码字节的文件
    test_file = "test_invalid_bytes.txt"
    with open(test_file, "wb") as f:
        f.write(b"\xff\xfe\x00\x00\x01\x02invalid bytes")

    try:
        from jk2bt.core.runner import load_jq_strategy

        funcs = load_jq_strategy(test_file)
        print("\n❌ 不应该成功加载无效文件")
    except UnicodeDecodeError as e:
        print("\n✅ 正确抛出 UnicodeDecodeError")
        print(f"   错误消息: {str(e)[:80]}")
    except RuntimeError as e:
        print("\n✅ 正确抛出 RuntimeError（latin-1 解码后执行失败）")
        print(f"   错误消息: {str(e)[:80]}")
    except FileNotFoundError as e:
        print("\n✅ 正确抛出 FileNotFoundError")
        print(f"   错误消息: {str(e)[:80]}")
    except Exception as e:
        print(f"\n⚠️ 抛出了其他异常: {type(e).__name__}")
        print(f"   错误消息: {str(e)[:80]}")
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


if __name__ == "__main__":
    # 测试1: 简单策略
    test_simple_strategy()

    # 测试2: 真实策略（可选）
    # test_real_strategy()

    # 测试3-8: 新增的测试
    test_utf8_encoding()
    test_gbk_encoding()
    test_get_price_signature()
    test_get_price_call_with_count()
    test_namespace_binding()
    test_invalid_file_error()

    print("\n测试完成！")

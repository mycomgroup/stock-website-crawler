"""
Test script for stock pool discovery enhancement
"""

from jk2bt.core.runner import _static_analyze_stock_pool


def test_strategy_with_etf(context):
    """Test strategy that uses ETF codes"""
    g.etf = '510500.XSHG'
    g.etf2 = '512900.XSHG'


def handle_data(context, data):
    pass


if __name__ == "__main__":
    print("Testing stock pool discovery...")

    func_dict = {
        'initialize': test_strategy_with_etf,
        'handle_data': handle_data,
    }

    result = _static_analyze_stock_pool(func_dict)
    print(f"Discovered: {result}")

    # Check if ETF codes are found
    expected_etfs = {'510500.XSHG', '512900.XSHG'}
    found_etfs = result.intersection(expected_etfs)

    if found_etfs:
        print(f"✓ Found ETF codes: {found_etfs}")
    else:
        print("✗ ETF codes not found")

    print("\nTest completed!")
import os

try:
    from ..utils.cache import fetch_and_cache_data
except ImportError:
    from utils.cache import fetch_and_cache_data


def get_income(
    symbol, indicator="按报告期", cache_dir="finance_cache", force_update=False
):
    cache_file = os.path.join(cache_dir, f"{symbol}_income_{indicator}.pkl")
    from akshare import stock_financial_benefit_ths

    def download_func():
        return stock_financial_benefit_ths(symbol=symbol, indicator=indicator)

    df = fetch_and_cache_data(
        symbol=symbol,
        start=None,
        end=None,
        cache_file=cache_file,
        download_func=download_func,
        date_col=None,
        columns_map=None,
        select_cols=None,
        force_update=force_update,
    )
    return df

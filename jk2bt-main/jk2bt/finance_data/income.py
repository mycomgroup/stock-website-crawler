try:
    from ..utils.cache import fetch_and_cache_data
except ImportError:
    from utils.cache import fetch_and_cache_data


def get_income(symbol, indicator="按报告期", force_update=False):
    try:
        from jk2bt.data_access import get_adapter
    except ImportError:
        from data_access import get_adapter

    adapter = get_adapter()

    def download_func():
        return adapter.get_financial_benefit(symbol=symbol, indicator=indicator)

    df = fetch_and_cache_data(
        symbol=symbol,
        start=None,
        end=None,
        cache_file=None,
        download_func=download_func,
        date_col=None,
        columns_map=None,
        select_cols=None,
        force_update=force_update,
    )
    return df

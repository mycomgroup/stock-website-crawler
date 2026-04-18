def get_income(symbol, indicator="按报告期", force_update=False):
    try:
        from jk2bt.data.sources import get_adapter
    except ImportError:
        from data_access import get_adapter

    adapter = get_adapter()
    df = adapter.get_financial_benefit(symbol=symbol, indicator=indicator)

    # Align column names with JQData income statement schema
    if df is not None and not df.empty:
        column_mapping = {
            "报告日": "stat_date",
            "净利润": "net_profit",
            "归属于母公司股东的净利润": "net_profit_to_shareholders",
            "归母净利润": "net_profit_to_shareholders",
            "营业总收入": "total_operating_revenue",
            "营业收入": "operating_revenue",
            "营业总成本": "total_operating_cost",
            "营业成本": "operating_cost",
            "营业利润": "operating_profit",
            "利润总额": "total_profit",
            "基本每股收益": "basic_eps",
            "稀释每股收益": "diluted_eps",
            "毛利": "gross_profit",
        }
        rename_cols = {k: v for k, v in column_mapping.items() if k in df.columns}
        df = df.rename(columns=rename_cols)

    return df

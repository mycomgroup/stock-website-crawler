# V1 RFScore7 进攻版 - RiceQuant 策略编辑器格式
# 回测区间: 2022-01-01 ~ 2025-12-31


def init(context):
    """初始化"""
    # 基准指数
    context.benchmark = "000300.XSHG"

    # 策略参数
    context.stock_num = 20
    context.hold_list = []
    context.target_list = []

    # 月度调仓 - 每月第一个交易日
    scheduler.run_monthly(adjust_position, 1)


def select_rfscore7(context, n=20):
    """RFScore7 + PB低20%选股"""
    # 中证800股票池
    stocks_300 = index_components("000300")
    stocks_500 = index_components("000905")
    stocks = list(set(stocks_300 + stocks_500))

    # 获取基本面数据
    q = (
        query(
            fundamentals.eod_derivative_indicator.pe_ratio,
            fundamentals.eod_derivative_indicator.pb_ratio,
            fundamentals.profit_statement.roa,
            fundamentals.profit_statement.roe,
        )
        .filter(
            fundamentals.eod_derivative_indicator.code.in_(stocks),
            fundamentals.eod_derivative_indicator.pe_ratio > 0,
            fundamentals.eod_derivative_indicator.pb_ratio > 0,
            fundamentals.profit_statement.roa > 0,
        )
        .order_by(fundamentals.eod_derivative_indicator.pb_ratio.asc())
        .limit(int(len(stocks) * 0.2))
    )

    df = get_fundamentals(q)

    if df is None or len(df) == 0:
        return []

    # 按ROA排序
    df = df.sort_values("roa", ascending=False)

    # 返回股票代码
    return df["code"].tolist()[:n]


def adjust_position(context, bar_dict):
    """月度调仓"""
    # 选股
    context.target_list = select_rfscore7(context, context.stock_num)

    if len(context.target_list) == 0:
        return

    # 卖出不在目标列表的持仓
    for stock in list(context.portfolio.positions.keys()):
        if stock not in context.target_list:
            order_target(stock, 0)
            print(f"卖出: {stock}")

    # 计算每只股票的买入金额
    position_count = len(context.portfolio.positions)
    if context.stock_num > position_count:
        cash_per_stock = context.portfolio.cash / (context.stock_num - position_count)

        # 买入
        for stock in context.target_list:
            if stock not in context.portfolio.positions:
                if order_value(stock, cash_per_stock):
                    print(f"买入: {stock}")
                if len(context.portfolio.positions) >= context.stock_num:
                    break


def handle_bar(context, bar_dict):
    """每日处理"""
    pass

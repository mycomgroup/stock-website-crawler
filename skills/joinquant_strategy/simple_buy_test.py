from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    log.set_level("system", "error")
    g.count = 0


def handle_data(context, data):
    g.count += 1

    if g.count > 3:
        return

    date = context.current_dt.strftime("%Y-%m-%d")

    if g.count == 1:
        log.info(f"{date}: 策略启动")

        stocks = ["000001.XSHE", "600000.XSHG"]
        for s in stocks:
            order_value(s, 50000)

        log.info(f"买入 {stocks}")

    if g.count == 3:
        for s in list(context.portfolio.positions):
            order_target(s, 0)
        log.info(f"卖出所有持仓")

from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    g.count = 0


def handle_data(context, data):
    g.count += 1
    if g.count == 1:
        log.info("策略启动成功")

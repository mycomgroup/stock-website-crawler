def init(context):
    context.stock = "000001.XSHE"
    context.bought = False
    logger.info("Simple test strategy initialized")


def handle_bar(context, bar_dict):
    if not context.bought:
        order_target_value(context.stock, 10000)
        context.bought = True
        logger.info(f"Bought {context.stock}")

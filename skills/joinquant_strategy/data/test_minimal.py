# 最简单的测试策略


def initialize(context):
    g.count = 0


def handle_data(context, data):
    g.count += 1
    if g.count % 250 == 0:
        log.info(f"第 {g.count} 天")

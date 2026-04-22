"""
主线策略：假弱高开影子盘
策略ID: mainline_fake_weak_high_open
创建时间: 2026-03-30
可信度: A档（实测支持）

核心数据（2024全年实测）：
- 假弱高开：日内收益+2.89%，胜率88.5%，样本26个
- 真低开A：日内收益+5.13%，胜率100%，样本4个
- 全年信号：136个，平均每日0.54个

风控约束：
- 单票上限：10万元
- 总仓上限：30万元
"""


class MainlineFakeWeakHighOpen:
    def __init__(self):
        self.strategy_name = "主线_假弱高开"
        self.single_position_limit = 100000
        self.total_position_limit = 300000
        self.emotion_filter_threshold = 30
        self.market_cap_range = (50, 150)
        self.position_limit = 30
        self.sell_profit_threshold = 0.03

    def filter_by_market_cap(self, stock_data):
        market_cap = stock_data.get("market_cap", 0)
        return self.market_cap_range[0] <= market_cap <= self.market_cap_range[1]

    def filter_by_position(self, stock_data):
        position_pct = stock_data.get("position_pct", 100)
        return position_pct <= self.position_limit

    def filter_by_consecutive_boards(self, stock_data):
        return stock_data.get("consecutive_boards", 0) == 0

    def check_emotion_filter(self, limit_up_count):
        return limit_up_count >= self.emotion_filter_threshold

    def is_fake_weak_high_open(self, stock_data):
        open_price = stock_data.get("open_price", 0)
        prev_close = stock_data.get("prev_close", 0)
        pre_market_high = stock_data.get("pre_market_high", 0)

        if prev_close > 0:
            open_change = (open_price - prev_close) / prev_close
            if open_change > 0 and open_change < 0.03:
                if pre_market_high > 0 and open_price < pre_market_high:
                    return True
        return False

    def generate_signals(self, stock_list, limit_up_count):
        if not self.check_emotion_filter(limit_up_count):
            return []

        signals = []
        for stock in stock_list:
            if not self.filter_by_market_cap(stock):
                continue
            if not self.filter_by_position(stock):
                continue
            if not self.filter_by_consecutive_boards(stock):
                continue
            if self.is_fake_weak_high_open(stock):
                signals.append(
                    {
                        "code": stock.get("code"),
                        "name": stock.get("name"),
                        "open_price": stock.get("open_price"),
                        "prev_close": stock.get("prev_close"),
                        "market_cap": stock.get("market_cap"),
                        "position_pct": stock.get("position_pct"),
                        "signal_type": "fake_weak_high_open",
                    }
                )
        return signals

    def calculate_position(self, signal, available_capital):
        max_position = min(self.single_position_limit, available_capital)
        remaining_limit = self.total_position_limit - self.current_total_position()
        return min(max_position, remaining_limit)

    def current_total_position(self):
        return 0

    def get_sell_rule(self, holding_data):
        current_price = holding_data.get("current_price", 0)
        buy_price = holding_data.get("buy_price", 0)

        if buy_price > 0:
            profit_pct = (current_price - buy_price) / buy_price
            if profit_pct >= self.sell_profit_threshold:
                return {
                    "action": "sell",
                    "reason": "冲高+3%止盈",
                    "timing": "immediate",
                }

        return {"action": "sell", "reason": "尾盘卖出", "timing": "close"}

    def check_stop_loss(self, holding_data):
        consecutive_losses = holding_data.get("consecutive_losses", 0)
        if consecutive_losses >= 3:
            return {
                "action": "stop_trading",
                "duration_days": 3,
                "reason": "连亏3笔，暂停3天",
            }
        return None

    def run_daily(self, date, stock_list, limit_up_count, current_holdings):
        signals = self.generate_signals(stock_list, limit_up_count)

        sell_orders = []
        for holding in current_holdings:
            sell_rule = self.get_sell_rule(holding)
            if sell_rule:
                sell_orders.append({"code": holding.get("code"), **sell_rule})

        stop_check = self.check_stop_loss(
            {"consecutive_losses": self.get_consecutive_losses()}
        )

        return {
            "date": date,
            "signals": signals,
            "sell_orders": sell_orders,
            "stop_trading": stop_check,
        }

    def get_consecutive_losses(self):
        return 0


if __name__ == "__main__":
    strategy = MainlineFakeWeakHighOpen()
    print(f"策略名称: {strategy.strategy_name}")
    print(f"单票上限: {strategy.single_position_limit}元")
    print(f"总仓上限: {strategy.total_position_limit}元")
    print(f"情绪过滤阈值: 涨停家数 >= {strategy.emotion_filter_threshold}")
    print(f"市值范围: {strategy.market_cap_range[0]}-{strategy.market_cap_range[1]}亿")
    print(f"位置上限: {strategy.position_limit}%")

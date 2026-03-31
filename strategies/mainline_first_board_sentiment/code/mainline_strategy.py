"""
首板低开情绪择时策略 - JoinQuant版本
版本：v1.0 正式版
日期：2026-03-31
状态：参数已锁定
"""

from jqdata import *


class MainlineFirstBoardSentiment:
    """
    首板低开情绪择时策略

    核心逻辑：
    1. 昨日涨停股次日假弱高开（+0.5%~+1.5%）
    2. 情绪开关（涨停家数≥30）决定是否开仓
    3. 次日开盘卖出
    """

    def __init__(self, context):
        self.context = context

        # 参数配置（已锁定）
        self.params = {
            # 信号参数
            "open_pct_min": 0.5,  # 开盘涨幅下限（%）
            "open_pct_max": 1.5,  # 开盘涨幅上限（%）
            "cap_min": 50,  # 流通市值下限（亿）
            "cap_max": 150,  # 流通市值上限（亿）
            "position_max": 30,  # 相对位置上限（%）
            "prev_day_zt": 0,  # 近1日涨停次数上限
            # 情绪参数
            "zt_count_mid": 30,  # 中等情绪阈值
            "zt_count_high": 50,  # 高情绪阈值
            # 仓位参数
            "single_position_pct": 5,  # 单票仓位上限（%）
            "single_position_max": 50,  # 单票资金上限（万）
            "total_position_pct": 30,  # 总仓位上限（%）
            "max_stocks_per_day": 3,  # 每日最多买入数量
            # 风控参数
            "consecutive_loss_trigger": 3,  # 连亏触发阈值
            "pause_days": 3,  # 停手天数
            "daily_loss_stop": -3.0,  # 日内止损阈值（%）
            # 滑点参数
            "buy_slippage": 0.005,  # 买入滑点
            "sell_slippage": 0.005,  # 卖出滑点
        }

        # 状态变量
        self.trade_count = 0
        self.win_count = 0
        self.loss_count = 0
        self.consecutive_loss = 0
        self.pause_days = 0
        self.can_trade = True

        # 情绪数据
        self.zt_count = 0
        self.dt_count = 0
        self.zt_dt_ratio = 0
        self.max_lianban = 0

        # 目标股票
        self.target_stocks = []

    def get_sentiment_data(self, date):
        """
        获取情绪数据

        参数：
            date: 日期字符串

        返回：
            dict: 情绪数据
        """
        # 获取所有股票
        all_stocks = get_all_securities("stock", date).index.tolist()
        all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]

        # 获取价格数据
        df = get_price(
            all_stocks,
            end_date=date,
            frequency="daily",
            fields=["close", "high_limit", "low_limit"],
            count=1,
            panel=False,
            fill_paused=False,
        )
        df = df.dropna()

        # 计算涨停家数
        zt_df = df[df["close"] == df["high_limit"]]
        dt_df = df[df["close"] == df["low_limit"]]

        self.zt_count = len(zt_df)
        self.dt_count = len(dt_df)
        self.zt_dt_ratio = self.zt_count / max(self.dt_count, 1)

        # 计算最高连板
        max_lb = 0
        for stock in zt_df["code"].tolist()[:30]:
            d = get_price(
                stock,
                end_date=date,
                frequency="daily",
                fields=["close", "high_limit"],
                count=10,
                panel=False,
                fill_paused=False,
            )
            if len(d) == 0:
                continue
            c = 0
            for i in range(len(d) - 1, -1, -1):
                if d.iloc[i]["close"] == d.iloc[i]["high_limit"]:
                    c += 1
                else:
                    break
            max_lb = max(max_lb, c)

        self.max_lianban = max_lb

        return {
            "zt_count": self.zt_count,
            "dt_count": self.dt_count,
            "zt_dt_ratio": self.zt_dt_ratio,
            "max_lianban": self.max_lianban,
        }

    def check_sentiment_switch(self):
        """
        检查情绪开关

        返回：
            bool: 是否允许买入
            str: 决策理由
        """
        if self.zt_count >= self.params["zt_count_high"]:
            return True, "高情绪（涨停≥50），积极开仓"
        elif self.zt_count >= self.params["zt_count_mid"]:
            return True, "中等情绪（涨停≥30），正常开仓"
        else:
            return False, "低情绪（涨停<30），空仓观望"

    def check_pause_status(self):
        """
        检查停手状态

        返回：
            bool: 是否可交易
        """
        if self.pause_days > 0:
            self.can_trade = False
        else:
            self.can_trade = True

        return self.can_trade

    def get_yesterday_zt_stocks(self, date):
        """
        获取昨日涨停股票

        参数：
            date: 日期字符串

        返回：
            list: 涨停股票列表
        """
        all_stocks = get_all_securities("stock", date).index.tolist()
        all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]

        df = get_price(
            all_stocks,
            end_date=date,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
            fill_paused=False,
        )
        df = df.dropna()

        zt_df = df[df["close"] == df["high_limit"]]
        zt_stocks = zt_df["code"].tolist()

        return zt_stocks

    def filter_stocks(self, stocks, date):
        """
        筛选股票

        参数：
            stocks: 股票列表
            date: 日期字符串

        返回：
            list: 筛选后的股票列表
        """
        if len(stocks) == 0:
            return []

        # 获取基本面数据
        q = query(
            valuation.code, valuation.circulating_market_cap, valuation.turnover
        ).filter(
            valuation.code.in_(stocks),
            valuation.circulating_market_cap >= self.params["cap_min"],
            valuation.circulating_market_cap <= self.params["cap_max"],
        )

        df = get_fundamentals(q, date=date)
        if df is None or len(df) == 0:
            return []

        filtered_stocks = df["code"].tolist()

        # 检查相对位置和连板状态
        final_stocks = []
        for stock in filtered_stocks[:50]:
            # 获取历史价格
            prices = get_price(
                stock,
                end_date=date,
                frequency="daily",
                fields=["close", "high_limit"],
                count=15,
                panel=False,
                fill_paused=False,
            )

            if len(prices) < 15:
                continue

            # 检查相对位置
            high_15d = prices["close"].max()
            current_price = prices["close"].iloc[-1]
            position = (
                (current_price - prices["close"].min())
                / (high_15d - prices["close"].min())
                * 100
            )

            if position > self.params["position_max"]:
                continue

            # 检查连板状态（近1日无涨停）
            if len(prices) >= 2:
                if prices.iloc[-2]["close"] == prices.iloc[-2]["high_limit"]:
                    continue

            final_stocks.append(stock)

        return final_stocks

    def check_buy_signal(self, stock, current_data):
        """
        检查买入信号

        参数：
            stock: 股票代码
            current_data: 当前数据

        返回：
            bool: 是否符合买入条件
            str: 理由
        """
        cd = current_data[stock]

        # 计算开盘涨幅
        open_pct = (cd.day_open - cd.pre_close) / cd.pre_close * 100

        # 检查假弱高开
        if open_pct < self.params["open_pct_min"]:
            return False, f"开盘涨幅{open_pct:.2f}%低于下限"

        if open_pct > self.params["open_pct_max"]:
            return False, f"开盘涨幅{open_pct:.2f}%高于上限"

        # 检查是否涨停
        if cd.day_open >= cd.high_limit:
            return False, "开盘涨停，无法买入"

        return True, f"假弱高开{open_pct:.2f}%，符合买入条件"

    def execute_buy(self, context, stocks):
        """
        执行买入

        参数：
            context: 策略上下文
            stocks: 目标股票列表
        """
        if len(stocks) == 0:
            return

        current_data = get_current_data()

        # 筛选符合买入条件的股票
        buy_stocks = []
        for stock in stocks[: self.params["max_stocks_per_day"] * 2]:
            if stock not in current_data:
                continue

            cd = current_data[stock]
            if cd.paused:
                continue

            is_signal, reason = self.check_buy_signal(stock, current_data)
            if is_signal:
                buy_stocks.append((stock, cd.day_open, reason))
                log.info(f"{stock} {reason}")

        # 限制买入数量
        buy_stocks = buy_stocks[: self.params["max_stocks_per_day"]]

        if len(buy_stocks) == 0:
            log.info("无符合买入条件的股票")
            return

        # 计算买入金额
        total_value = context.portfolio.total_value
        single_value = min(
            total_value * self.params["single_position_pct"] / 100,
            self.params["single_position_max"] * 10000,
        )

        # 执行买入
        for stock, price, reason in buy_stocks:
            # 清空现有持仓
            if stock in context.portfolio.positions:
                order_target_value(stock, 0)

            # 买入
            order_value(stock, single_value)
            log.info(f"买入 {stock} 金额 {single_value:.0f} 元")

    def execute_sell(self, context):
        """
        执行卖出

        参数：
            context: 策略上下文
        """
        current_data = get_current_data()

        for stock in list(context.portfolio.positions):
            pos = context.portfolio.positions[stock]
            cd = current_data[stock]

            # 计算盈亏
            pnl = (cd.last_price - pos.avg_cost) / pos.avg_cost * 100

            # 涨停持有
            if cd.last_price >= cd.high_limit * 0.995:
                log.info(f"{stock} 涨停持有 盈亏 {pnl:.2f}%")
                continue

            # 次日开盘卖出
            order_target(stock, 0)
            log.info(f"卖出 {stock} 盈亏 {pnl:.2f}%")

            # 记录交易结果
            self.record_trade(pnl)

    def record_trade(self, pnl):
        """
        记录交易结果

        参数：
            pnl: 盈亏比例
        """
        self.trade_count += 1

        if pnl > 0:
            self.win_count += 1
            self.consecutive_loss = 0
        else:
            self.loss_count += 1
            self.consecutive_loss += 1

        # 检查是否触发停手
        if self.consecutive_loss >= self.params["consecutive_loss_trigger"]:
            self.pause_days = self.params["pause_days"]
            log.info(f"连亏{self.consecutive_loss}笔，触发停手{self.pause_days}天")

    def daily_update(self):
        """
        每日更新
        """
        if self.pause_days > 0:
            self.pause_days -= 1
            log.info(f"停手天数剩余 {self.pause_days} 天")


def initialize(context):
    """
    初始化函数
    """
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    # 创建策略实例
    g.strategy = MainlineFirstBoardSentiment(context)

    # 设置基准
    set_benchmark("000300.XSHG")

    # 定时任务
    run_daily(before_trading, "08:30")
    run_daily(select_stocks, "09:00")
    run_daily(buy_stocks, "09:35")
    run_daily(sell_stocks, "09:35")
    run_daily(after_trading, "15:10")


def before_trading(context):
    """
    盘前准备
    """
    date = context.previous_date.strftime("%Y-%m-%d")

    # 获取情绪数据
    sentiment = g.strategy.get_sentiment_data(date)
    log.info(f"涨停家数: {sentiment['zt_count']}")
    log.info(f"跌停家数: {sentiment['dt_count']}")
    log.info(f"涨跌停比: {sentiment['zt_dt_ratio']:.2f}")
    log.info(f"最高连板: {sentiment['max_lianban']}")

    # 检查情绪开关
    allow_buy, reason = g.strategy.check_sentiment_switch()
    log.info(f"情绪判断: {reason}")

    # 检查停手状态
    can_trade = g.strategy.check_pause_status()
    log.info(f"停手状态: {'可交易' if can_trade else '停手中'}")

    # 更新停手天数
    g.strategy.daily_update()


def select_stocks(context):
    """
    选股
    """
    if not g.strategy.can_trade:
        log.info("停手中，不选股")
        g.strategy.target_stocks = []
        return

    if g.strategy.zt_count < g.strategy.params["zt_count_mid"]:
        log.info("低情绪，不选股")
        g.strategy.target_stocks = []
        return

    date = context.previous_date.strftime("%Y-%m-%d")

    # 获取昨日涨停股票
    zt_stocks = g.strategy.get_yesterday_zt_stocks(date)
    log.info(f"昨日涨停: {len(zt_stocks)} 只")

    # 筛选股票
    filtered_stocks = g.strategy.filter_stocks(zt_stocks, date)
    log.info(f"筛选后: {len(filtered_stocks)} 只")

    g.strategy.target_stocks = filtered_stocks


def buy_stocks(context):
    """
    买入
    """
    if not g.strategy.can_trade:
        log.info("停手中，不买入")
        return

    if g.strategy.zt_count < g.strategy.params["zt_count_mid"]:
        log.info("低情绪，不买入")
        return

    if len(g.strategy.target_stocks) == 0:
        log.info("无目标股票，不买入")
        return

    g.strategy.execute_buy(context, g.strategy.target_stocks)


def sell_stocks(context):
    """
    卖出
    """
    g.strategy.execute_sell(context)


def after_trading(context):
    """
    收盘后
    """
    log.info(f"交易次数: {g.strategy.trade_count}")
    log.info(
        f"胜率: {g.strategy.win_count / max(g.strategy.trade_count, 1) * 100:.1f}%"
    )
    log.info(f"连亏次数: {g.strategy.consecutive_loss}")
    log.info(f"停手天数: {g.strategy.pause_days}")

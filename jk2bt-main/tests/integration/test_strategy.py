from jk2bt.core.strategy_base import (
    JQ2BTBaseStrategy,
    get_akshare_etf_data,
    get_akshare_stock_data,
    get_index_nav,
    analyze_performance,
)
import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt


class BuyAndHoldStrategy(JQ2BTBaseStrategy):
    def __init__(self):
        super().__init__()
        self.bought = set()

    def next(self):
        super().next()
        for data in self.datas:
            pos = self.getposition(data).size
            if data._name not in self.bought and pos == 0:
                self.order_target_percent(data, target=1.0 / len(self.datas))
                self.log(f"买入并持有 {data._name}", log_type="trade")
                self.bought.add(data._name)


def run_etf_test():
    ETF_POOL = {
        "518880": "黄金ETF",
        "513100": "纳指100",
        "159915": "创业板100",
        "510180": "上证180",
    }
    start_date = "2020-01-01"
    end_date = "2022-12-31"

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0.0002)
    cerebro.broker.set_slippage_perc(perc=0.000)

    datas = []
    for symbol in ETF_POOL.keys():
        data = get_akshare_etf_data(symbol, start_date, end_date)
        assert data is not None, f"ETF数据加载失败: {symbol}"
        cerebro.adddata(data, name=symbol)
        datas.append(data)
    assert len(datas) == len(ETF_POOL), "ETF数据源数量与ETF池不符"

    cerebro.addstrategy(BuyAndHoldStrategy)
    print("【ETF测试】Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())
    results = cerebro.run()
    strat = results[0]
    print("【ETF测试】Final Portfolio Value: %.2f" % cerebro.broker.getvalue())

    length = strat.datas[0].buflen()
    dates = [strat.datas[0].datetime.date(-i) for i in range(length)]
    dates.reverse()
    strategy_nav = pd.Series(strat.navs, index=dates)
    assert not strategy_nav.empty, "ETF策略净值序列为空"
    assert strategy_nav.isnull().sum() == 0, "ETF策略净值序列存在缺失值"

    benchmark_nav = get_index_nav("000300", start_date, end_date)
    assert not benchmark_nav.empty, "ETF基准净值序列为空"
    benchmark_nav = benchmark_nav.reindex(strategy_nav.index).ffill()
    assert benchmark_nav.isnull().sum() == 0, "ETF基准净值序列存在缺失值"

    analyze_performance(strategy_nav, benchmark_nav)

    plt.figure(figsize=(10, 5))
    (strategy_nav / strategy_nav.iloc[0]).plot(label="ETF策略净值")
    (benchmark_nav / benchmark_nav.iloc[0]).plot(label="沪深300", linestyle="--")
    plt.legend()
    plt.title("ETF Buy&Hold 策略 vs 沪深300净值对比")
    plt.grid(True)
    plt.show()


def run_stock_test():
    STOCK_POOL = {
        "sh600519": "贵州茅台",
    }
    start_date = "2020-01-01"
    end_date = "2022-12-31"

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0.0002)
    cerebro.broker.set_slippage_perc(perc=0.000)

    datas = []
    for symbol in STOCK_POOL.keys():
        data = get_akshare_stock_data(symbol, start_date, end_date)
        assert data is not None, f"个股数据加载失败: {symbol}"
        cerebro.adddata(data, name=symbol)
        datas.append(data)
    assert len(datas) == len(STOCK_POOL), "个股数据源数量与股票池不符"

    cerebro.addstrategy(BuyAndHoldStrategy)
    print("【个股测试】Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())
    results = cerebro.run()
    strat = results[0]
    print("【个股测试】Final Portfolio Value: %.2f" % cerebro.broker.getvalue())

    length = strat.datas[0].buflen()
    dates = [strat.datas[0].datetime.date(-i) for i in range(length)]
    dates.reverse()
    strategy_nav = pd.Series(strat.navs, index=dates)
    assert not strategy_nav.empty, "个股策略净值序列为空"
    assert strategy_nav.isnull().sum() == 0, "个股策略净值序列存在缺失值"

    benchmark_nav = get_index_nav("000300", start_date, end_date)
    assert not benchmark_nav.empty, "个股基准净值序列为空"
    benchmark_nav = benchmark_nav.reindex(strategy_nav.index).ffill()
    assert benchmark_nav.isnull().sum() == 0, "个股基准净值序列存在缺失值"

    analyze_performance(strategy_nav, benchmark_nav)

    plt.figure(figsize=(10, 5))
    (strategy_nav / strategy_nav.iloc[0]).plot(label="个股策略净值")
    (benchmark_nav / benchmark_nav.iloc[0]).plot(label="沪深300", linestyle="--")
    plt.legend()
    plt.title("个股 Buy&Hold 策略 vs 沪深300净值对比")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    run_etf_test()
    run_stock_test()

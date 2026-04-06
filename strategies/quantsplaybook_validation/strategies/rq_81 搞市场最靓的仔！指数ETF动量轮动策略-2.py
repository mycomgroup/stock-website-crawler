# 风险及免责提示：该策略由聚宽用户在聚宽社区分享，仅供学习交流使用。
# 原文一般包含策略说明，如有疑问请到原文和作者交流讨论。
# 原文网址：https://www.joinquant.com/post/46429
# 标题：搞市场最靓的仔！指数ETF动量轮动策略-2
# 作者：野蛮生涨
# 原回测条件：2020-01-01 到 2024-02-03, ￥100000, 每天

# 导入函数库
import random

# 初始化函数，设定基准等等
def init(context):
    # 设定沪深300作为基准
    # 开启动态复权模式(真实价格)
    # 输出内容到日志 print()
    print('初始函数开始运行且全局只运行一次')

    ### 股票相关设定 ###
    # 股票类每笔交易时的手续费是：千分之一印花税，买入时佣金万分之2.5，卖出时佣金万分之2.5， 每笔交易佣金最低扣5块钱
    # 基金类每笔交易时的手续费是：无印花税，买入时佣金万分之1，卖出时佣金万分之1， 每笔交易佣金最低扣5块钱
    #set_order_cost(OrderCost(close_tax=0.001, open_commission=0.00025, close_commission=0.00025, min_commission=5), type='stock')
    # 设置滑点,ETF单价较低滑点高了对影响较大
    # Note: PriceRelatedSlippage not available in RQ, using FixedSlippage(0) as approximation
    # 开盘前运行
    scheduler.run_daily(before_market_open, time_rule=market_open(minute=0))
    # 收盘后运行
    scheduler.run_daily(after_market_close, time_rule=market_close(minute=30))
    # 日线策略，指定时间运行，如果后期要分钟级这里需要改成分钟级handle_data
    scheduler.run_daily(my_trade, time_rule=market_close(minute=0))

    context.stocks = {
        '510500.XSHG',    # 中证500ETF
        '510300.XSHG',    # 沪深510300
        '510050.XSHG',    # 上证50
        '159949.XSHE',    # 创业板50
        '513100.XSHG',    # 纳指ETF
        '513500.XSHG',    # 标普500
        '159920.XSHE',    # 恒生ETF
        '513520.XSHG',    # 日经ETF
        '513030.XSHG',    # 德国30
        '162411.XSHE',    # 华宝油气
        '159985.XSHE'}    # 豆粕ETF

    # 持仓状态
    context.position = {'ETF_HOLD':'0', 'STATUS':0, 'HOLD_NUM':0}

## 开盘前运行函数

def handle_bar(context, bar_dict):
    pass

def before_market_open(context, bar_dict):
    print('函数运行时间(before_market_open)：' + str(context.now.time()))
    print("持仓情况:{0}".format(context.position))


## 开盘时运行函数
def log_market_open(context, bar_dict):
    print('函数运行时间(market_open)：' + str(context.now.time()))
    print("持仓情况:{0}".format(context.position))


def my_trade(context, bar_dict):

    N = 21

    SEC_LIST = []
    R_LIST = []

    for security in context.stocks:
        close_data1 = history_bars(security, 30, '1d', 'close')
        if close_data1 is None or len(close_data1) < 25:
            continue
        curr_price = close_data1[-1]
        his_n_price = sum(close_data1[-23:-20]) / 3

        if curr_price != curr_price or his_n_price != his_n_price or curr_price < 0.01 or his_n_price < 0.01:
            print("未取到[%s]分钟级数据,直接退出！！！" % (instruments(security).symbol))
            return

        R = (close_data1[-2]+close_data1[-1]+curr_price-sum(close_data1[-23:-20]))*100/sum(close_data1[-23:-20])

        base_price = close_data1[-N]                  # 特定的一个历史价

        # 回测偶尔有遇到到R结果一致的情况，导致排序出错，如果有重复的加一个随机数
        if R in R_LIST:
            R = R + random.random()/1000
        R_LIST.append(R)
        SEC_LIST.append((R, security, curr_price, base_price))

    # 将ETF进行排序
    SEC_LIST.sort(reverse=True)
    ETF_No1 = SEC_LIST[0][1]

    if context.position['STATUS'] == 0:
        # 大于历史价才买进
        if SEC_LIST[0][2] > SEC_LIST[0][3]*1.001:
            print("目前空仓买入:%s" % ETF_No1)
            order_target_value(ETF_No1, context.portfolio.cash)
            context.position['STATUS'] = 1
            context.position['ETF_HOLD'] = ETF_No1
    elif context.position['STATUS'] == 1:
        if context.position['ETF_HOLD'] == ETF_No1:
            # 跌破历史价卖出
            if SEC_LIST[0][2] < SEC_LIST[0][3]*0.999:
                print("持仓%s排名第一，但小于历史价需要卖出" % context.position['ETF_HOLD'])
                order_target_value(context.position['ETF_HOLD'], 0)
                context.position['STATUS'] = 0
                context.position['ETF_HOLD'] = ' '
            else:
                print("持仓%s排名第一，继续持仓" % context.position['ETF_HOLD'])
        else:
            if SEC_LIST[0][2] > SEC_LIST[0][3]*1.001:
                order_target_value(context.position['ETF_HOLD'], 0)
                order_target_value(ETF_No1, context.portfolio.cash)
                context.position['ETF_HOLD'] = ETF_No1


## 收盘后运行函数
def after_market_close(context, bar_dict):
    print(str('函数运行时间(after_market_close):' + str(context.now.time())))
    #得到当天所有成交记录
    trades = {}
    for _trade in trades.values():
        print('成交记录：'+str(_trade))

    print('一天结束')
    print('##############################################################\n\n')

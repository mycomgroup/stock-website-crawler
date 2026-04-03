# 差分进化算法组合优化策略 - RiceQuant版本
# 来源：《DE算法下的组合优化》
# 核心逻辑：用差分进化算法（DE）优化ETF组合权重，最大化夏普比率
#           DE算法是一种全局优化算法，适合非凸优化问题

import numpy as np


def differential_evolution_sharpe(returns_matrix, pop_size=20, max_iter=50,
                                   F=0.8, CR=0.9):
    """
    差分进化算法优化组合权重（最大化夏普比率）
    returns_matrix: shape (n_assets, n_days)
    """
    n_assets = returns_matrix.shape[0]

    def sharpe(weights):
        weights = np.abs(weights)
        weights /= weights.sum()
        port_returns = returns_matrix.T @ weights
        if np.std(port_returns) == 0:
            return -999
        return np.mean(port_returns) / np.std(port_returns) * np.sqrt(252)

    # 初始化种群（权重向量）
    population = np.random.dirichlet(np.ones(n_assets), size=pop_size)
    fitness = np.array([sharpe(ind) for ind in population])

    for _ in range(max_iter):
        for i in range(pop_size):
            # 随机选3个不同个体
            idxs = [j for j in range(pop_size) if j != i]
            a, b, c = population[np.random.choice(idxs, 3, replace=False)]

            # 变异
            mutant = a + F * (b - c)
            mutant = np.clip(mutant, 0, 1)

            # 交叉
            cross_points = np.random.rand(n_assets) < CR
            trial = np.where(cross_points, mutant, population[i])
            trial = np.abs(trial)
            if trial.sum() > 0:
                trial /= trial.sum()

            # 选择
            trial_fitness = sharpe(trial)
            if trial_fitness > fitness[i]:
                population[i] = trial
                fitness[i] = trial_fitness

    best_idx = np.argmax(fitness)
    best_weights = population[best_idx]
    best_weights /= best_weights.sum()
    return best_weights


# ETF组合
ETFS = [
    '510300.XSHG',  # 沪深300ETF
    '510500.XSHG',  # 中证500ETF
    '159915.XSHE',  # 创业板ETF
    '512010.XSHG',  # 军工ETF
    '515000.XSHG',  # 科技ETF
]


def init(context):
    context.etfs = ETFS
    context.lookback = 60
    context.quarter = -1
    context.weights = None


def handle_bar(context, bar_dict):
    current_quarter = (context.now.month - 1) // 3
    if current_quarter == context.quarter:
        # 按优化权重持仓
        if context.weights is not None:
            total_value = context.portfolio.total_value
            for etf, w in zip(context.etfs, context.weights):
                if etf in bar_dict:
                    order_target_value(etf, total_value * w * 0.95)
        return
    context.quarter = current_quarter

    # 收集收益率数据
    returns_list = []
    valid_etfs = []
    for etf in context.etfs:
        if etf not in bar_dict:
            continue
        try:
            prices = history_bars(etf, context.lookback + 1, '1d', 'close')
            if prices is None or len(prices) < context.lookback + 1:
                continue
            prices = np.array(prices, dtype=float)
            returns = np.diff(prices) / prices[:-1]
            returns_list.append(returns)
            valid_etfs.append(etf)
        except:
            continue

    if len(valid_etfs) < 2:
        return

    returns_matrix = np.array(returns_list)

    # DE算法优化权重
    try:
        weights = differential_evolution_sharpe(returns_matrix)
        context.weights = weights
    except:
        # 降级：等权
        context.weights = np.ones(len(valid_etfs)) / len(valid_etfs)

    # 卖出不在目标中的持仓
    for etf in list(context.portfolio.positions.keys()):
        if etf not in valid_etfs:
            order_to(etf, 0)

    total_value = context.portfolio.total_value
    for etf, w in zip(valid_etfs, context.weights):
        order_target_value(etf, total_value * w * 0.95)
    print(f"DE优化权重: {dict(zip(valid_etfs, context.weights.round(3)))}")

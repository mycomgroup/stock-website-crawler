# 实盘策略代码

## 一、逻辑回归选股策略（完整版）

### 1.1 策略参数配置

```python
# strategy_config.py
"""
策略配置文件
"""

CONFIG = {
    # 模型参数
    "model": {
        "name": "LogisticRegression",
        "params": {
            "C": 100,
            "max_iter": 200,
            "random_state": 42,
            "solver": "lbfgs"
        }
    },
    
    # 股票池
    "stock_pool": {
        "index": "000905.XSHG",  # 中证500
        "min_list_days": 180,     # 上市至少180天
        "exclude_st": True,       # 排除ST
        "exclude_suspended": True # 排除停牌
    },
    
    # 特征因子
    "features": [
        "pe_ratio",   # 市盈率
        "pb_ratio",   # 市净率
        "roe",        # 净资产收益率
        "roa"         # 总资产收益率
    ],
    
    # 调仓参数
    "rebalance": {
        "frequency": "quarterly",  # 季度调仓
        "hold_n": 10,              # 持仓10只
        "min_score": 0.5           # 最小预测概率
    },
    
    # 风控参数
    "risk_control": {
        "max_single_position": 0.15,    # 单票上限15%
        "max_industry_position": 0.30,  # 行业上限30%
        "stop_loss": 0.08,              # 个股止损8%
        "strategy_stop_loss": 0.15,     # 策略止损15%
        "min_cash_ratio": 0.20          # 最低现金比例20%
    },
    
    # 交易成本
    "cost": {
        "commission": 0.0003,  # 佣金
        "slippage": 0.001,     # 滑点
        "stamp_duty": 0.001    # 印花税
    }
}
```

### 1.2 选股核心代码

```python
# stock_selector.py
"""
逻辑回归选股核心模块
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score


class LogisticRegressionSelector:
    """逻辑回归选股器"""
    
    def __init__(self, config):
        """
        初始化
        
        Parameters:
        -----------
        config : dict
            策略配置
        """
        self.config = config
        self.model = LogisticRegression(**config["model"]["params"])
        self.scaler = StandardScaler()
        self.feature_cols = config["features"]
        
    def prepare_features(self, stocks, date, jq_api):
        """
        准备特征数据
        
        Parameters:
        -----------
        stocks : list
            股票列表
        date : str
            日期
        jq_api : module
            JoinQuant API
            
        Returns:
        --------
        features : DataFrame
            特征数据
        """
        # 查询财务数据
        q = jq_api.query(
            jq_api.valuation.code,
            jq_api.valuation.pe_ratio,
            jq_api.valuation.pb_ratio,
            jq_api.indicator.roe,
            jq_api.indicator.roa,
        ).filter(jq_api.valuation.code.in_(stocks))
        
        df = jq_api.get_fundamentals(q, date=date)
        df = df.set_index("code")
        
        # 数据清洗
        df = df.replace([np.inf, -np.inf], np.nan)
        
        # 去极值
        for col in self.feature_cols:
            if col in df.columns:
                q01 = df[col].quantile(0.01)
                q99 = df[col].quantile(0.99)
                df[col] = df[col].clip(q01, q99)
        
        df = df[self.feature_cols].dropna()
        
        return df
    
    def create_labels(self, returns, method="median"):
        """
        创建标签
        
        Parameters:
        -----------
        returns : Series
            收益率序列
        method : str
            标签创建方法，"median"或"quantile"
            
        Returns:
        --------
        labels : Series
            标签序列
        """
        if method == "median":
            median = returns.median()
            labels = (returns > median).astype(int)
        elif method == "quantile":
            q30 = returns.quantile(0.3)
            q70 = returns.quantile(0.7)
            labels = pd.Series(np.nan, index=returns.index)
            labels[returns >= q70] = 1
            labels[returns <= q30] = 0
            labels = labels.dropna()
        
        return labels
    
    def train(self, X_train, y_train):
        """
        训练模型
        
        Parameters:
        -----------
        X_train : DataFrame
            训练特征
        y_train : Series
            训练标签
            
        Returns:
        --------
        cv_score : float
            交叉验证得分
        """
        # 标准化
        X_scaled = self.scaler.fit_transform(X_train)
        
        # 训练
        self.model.fit(X_scaled, y_train)
        
        # 交叉验证
        cv_scores = cross_val_score(
            self.model, X_scaled, y_train, 
            cv=5, scoring="accuracy"
        )
        
        return cv_scores.mean()
    
    def predict(self, X_test):
        """
        预测
        
        Parameters:
        -----------
        X_test : DataFrame
            测试特征
            
        Returns:
        --------
        proba : Series
            预测概率
        """
        # 标准化
        X_scaled = self.scaler.transform(X_test)
        
        # 预测概率
        proba = self.model.predict_proba(X_scaled)[:, 1]
        
        return pd.Series(proba, index=X_test.index)
    
    def select_stocks(self, X_test, hold_n=10, min_score=0.5):
        """
        选股
        
        Parameters:
        -----------
        X_test : DataFrame
            测试特征
        hold_n : int
            持仓数量
        min_score : float
            最小得分
            
        Returns:
        --------
        selected : list
            选中的股票
        scores : Series
            得分序列
        """
        # 预测
        scores = self.predict(X_test)
        
        # 过滤低分
        scores = scores[scores >= min_score]
        
        # 选前N个
        selected = scores.nlargest(hold_n).index.tolist()
        
        return selected, scores
    
    def get_feature_importance(self):
        """
        获取特征重要性
        
        Returns:
        --------
        importance : DataFrame
            特征重要性
        """
        importance = pd.DataFrame({
            "feature": self.feature_cols,
            "coefficient": self.model.coef_[0],
            "abs_coefficient": np.abs(self.model.coef_[0])
        })
        
        importance = importance.sort_values(
            "abs_coefficient", ascending=False
        )
        
        return importance


# 使用示例
if __name__ == "__main__":
    from jqdata import *
    
    # 配置
    config = {
        "model": {
            "params": {
                "C": 100,
                "max_iter": 200,
                "random_state": 42
            }
        },
        "features": ["pe_ratio", "pb_ratio", "roe", "roa"]
    }
    
    # 初始化
    selector = LogisticRegressionSelector(config)
    
    # 获取股票池
    stocks = get_index_stocks("000905.XSHG")[:100]
    
    # 准备特征
    features = selector.prepare_features(stocks, "2024-01-01", jq)
    
    print(f"特征维度: {features.shape}")
    print(f"特征列: {features.columns.tolist()}")
```

### 1.3 回测框架

```python
# backtest.py
"""
回测框架
"""

import pandas as pd
import numpy as np
from datetime import datetime
from jqdata import *


class BacktestEngine:
    """回测引擎"""
    
    def __init__(self, selector, config):
        """
        初始化
        
        Parameters:
        -----------
        selector : LogisticRegressionSelector
            选股器
        config : dict
            配置
        """
        self.selector = selector
        self.config = config
        
    def get_rebalance_dates(self, start_date, end_date, freq="quarterly"):
        """
        获取调仓日期
        
        Parameters:
        -----------
        start_date : str
            开始日期
        end_date : str
            结束日期
        freq : str
            频率，"quarterly"或"monthly"
            
        Returns:
        --------
        dates : list
            调仓日期列表
        """
        trade_days = get_trade_days(start_date, end_date)
        
        if freq == "quarterly":
            dates = []
            last_q = None
            for d in trade_days:
                q = (d.month - 1) // 3
                if q != last_q:
                    dates.append(d)
                    last_q = q
        elif freq == "monthly":
            dates = []
            last_m = None
            for d in trade_days:
                if d.month != last_m:
                    dates.append(d)
                    last_m = d.m onth
        
        return dates
    
    def run(self, start_date, end_date, initial_capital=100000):
        """
        运行回测
        
        Parameters:
        -----------
        start_date : str
            开始日期
        end_date : str
            结束日期
        initial_capital : float
            初始资金
            
        Returns:
        --------
        results : dict
            回测结果
        """
        # 获取调仓日期
        rebalance_dates = self.get_rebalance_dates(
            start_date, end_date, 
            freq=self.config["rebalance"]["frequency"]
        )
        
        # 初始化
        capital = initial_capital
        positions = {}
        results = []
        
        # 滚动回测
        for i in range(len(rebalance_dates) - 1):
            date = rebalance_dates[i]
            next_date = rebalance_dates[i + 1]
            
            print(f"\n调仓: {date}")
            
            # 获取股票池
            stocks = get_index_stocks(self.config["stock_pool"]["index"])
            
            # 准备特征
            features = self.selector.prepare_features(stocks, str(date), jq)
            
            # 选股
            selected, scores = self.selector.select_stocks(
                features, 
                hold_n=self.config["rebalance"]["hold_n"],
                min_score=self.config["rebalance"]["min_score"]
            )
            
            # 计算权重
            weight = 1.0 / len(selected)
            
            # 计算收益
            # 获取价格
            p0 = get_price(selected, end_date=str(date), count=1, 
                          fields=["close"], panel=False)
            p1 = get_price(selected, end_date=str(next_date), count=1,
                          fields=["close"], panel=False)
            
            p0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
            p1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]
            
            # 计算收益
            returns = (p1 / p0 - 1).dropna()
            
            # 扣除成本
            cost = self.config["cost"]["commission"] * 2 + \
                   self.config["cost"]["slippage"] * 2
            
            net_returns = returns - cost
            
            # 组合收益
            port_return = net_returns.mean()
            
            # 更新资金
            capital *= (1 + port_return)
            
            # 记录结果
            results.append({
                "date": date,
                "next_date": next_date,
                "selected": selected,
                "port_return": port_return,
                "capital": capital,
                "n_stocks": len(selected)
            })
            
            print(f"  选股: {len(selected)}只")
            print(f"  收益: {port_return:.2%}")
            print(f"  资金: {capital:,.0f}")
        
        # 汇总结果
        df_results = pd.DataFrame(results)
        
        # 计算累计收益
        df_results["cum_return"] = (1 + df_results["port_return"]).cumprod() - 1
        
        # 计算回撤
        df_results["cum_capital"] = df_results["capital"]
        df_results["max_capital"] = df_results["cum_capital"].cummax()
        df_results["drawdown"] = (
            df_results["cum_capital"] / df_results["max_capital"] - 1
        )
        
        # 统计指标
        total_return = df_results["cum_return"].iloc[-1]
        annual_return = (1 + total_return) ** (4 / len(df_results)) - 1  # 季度
        max_drawdown = df_results["drawdown"].min()
        sharpe = (
            df_results["port_return"].mean() / 
            df_results["port_return"].std() * 2  # 年化
        )
        win_rate = (df_results["port_return"] > 0).mean()
        
        summary = {
            "total_return": total_return,
            "annual_return": annual_return,
            "max_drawdown": max_drawdown,
            "sharpe_ratio": sharpe,
            "win_rate": win_rate,
            "n_periods": len(df_results)
        }
        
        return {
            "summary": summary,
            "details": df_results
        }


# 使用示例
if __name__ == "__main__":
    from stock_selector import LogisticRegressionSelector
    from strategy_config import CONFIG
    
    # 初始化选股器
    selector = LogisticRegressionSelector(CONFIG)
    
    # 初始化回测引擎
    engine = BacktestEngine(selector, CONFIG)
    
    # 运行回测
    results = engine.run("2023-01-01", "2025-12-31", initial_capital=100000)
    
    # 打印结果
    print("\n" + "=" * 50)
    print("回测结果")
    print("=" * 50)
    print(f"累计收益: {results['summary']['total_return']:.2%}")
    print(f"年化收益: {results['summary']['annual_return']:.2%}")
    print(f"最大回撤: {results['summary']['max_drawdown']:.2%}")
    print(f"夏普比率: {results['summary']['sharpe_ratio']:.3f}")
    print(f"胜率: {results['summary']['win_rate']:.1%}")
```

---

## 二、使用说明

### 2.1 文件结构

```
scripts/
├── strategy_config.py      # 配置文件
├── stock_selector.py       # 选股核心
└── backtest.py            # 回测框架
```

### 2.2 运行步骤

```bash
# 1. 运行选股
python stock_selector.py

# 2. 运行回测
python backtest.py
```

### 2.3 参数调整

在 `strategy_config.py` 中修改参数：

```python
# 调整持仓数量
"hold_n": 20  # 从10只增加到20只

# 调整特征因子
"features": [
    "pe_ratio", "pb_ratio", 
    "roe", "roa",
    "inc_revenue_year_on_year"  # 新增成长因子
]

# 调整风控参数
"stop_loss": 0.05  # 止损从8%改为5%
```

---

**代码版本**: v1.0  
**最后更新**: 2026-04-01
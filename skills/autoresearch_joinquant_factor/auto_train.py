#!/usr/bin/env python
# coding: utf-8

# In[1]:


from jqdata import *
from jqlib.technical_analysis import *
from jqfactor import get_factor_values
from jqfactor import winsorize_med
from jqfactor import standardlize
from jqfactor import neutralize
import datetime
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels import regression
from six import StringIO
#导入pca
from sklearn.decomposition import PCA
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn import metrics
from tqdm import tqdm
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import seaborn as sns
#获取指定周期的日期列表 'W、M、Q'
def get_period_date(peroid,start_date, end_date):
    #设定转换周期period_type  转换为周是'W',月'M',季度线'Q',五分钟'5min',12天'12D'
    stock_data = get_price('000001.XSHE',start_date,end_date,'daily',fields=['close'])
    stock_data['date']=stock_data.index
    period_stock_data=stock_data.resample(peroid,how='last')
    period_stock_data = period_stock_data.set_index('date').dropna()
    date=period_stock_data.index
    pydate_array = date.to_pydatetime()
    date_only_array = np.vectorize(lambda s: s.strftime('%Y-%m-%d'))(pydate_array )
    date_only_series = pd.Series(date_only_array)
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    start_date=start_date-datetime.timedelta(days=1)
    start_date = start_date.strftime("%Y-%m-%d")
    date_list=date_only_series.values.tolist()
    date_list.insert(0,start_date)
    return date_list
peroid = 'W'
start_date = '2025-01-01'
end_date = '2024-04-15'
DAY = get_period_date(peroid,start_date, end_date)
print(len(DAY))


# In[2]:


11*12*4


# In[3]:


#去除上市距beginDate不足3个月的股票
def delect_stop(stocks,beginDate,n=30*3):
    stockList=[]
    beginDate = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    for stock in stocks:
        start_date=get_security_info(stock).start_date
        if start_date<(beginDate-datetime.timedelta(days=n)).date():
            stockList.append(stock)
    return stockList
#获取股票池
def get_stock(stockPool,begin_date):
    if stockPool=='HS300':
        stockList=get_index_stocks('000300.XSHG',begin_date)
    elif stockPool=='ZZ500':
        stockList=get_index_stocks('399905.XSHE',begin_date)
    elif stockPool=='ZZ800':
        stockList=get_index_stocks('399906.XSHE',begin_date)   
    elif stockPool=='CYBZ':
        stockList=get_index_stocks('399006.XSHE',begin_date)
    elif stockPool=='ZXBZ':
        stockList=get_index_stocks('399005.XSHE',begin_date)
    elif stockPool=='A':
        stockList=get_index_stocks('000002.XSHG',begin_date)+get_index_stocks('399107.XSHE',begin_date)
        stockList = [stock for stock in stockList if not stock.startswith(('68', '4', '8'))]
    elif stockPool=='AA':
        stockList=get_index_stocks('000985.XSHG',begin_date)
        stockList = [stock for stock in stockList if not stock.startswith(('3', '68', '4', '8'))]
    elif stockPool=='small':
        stockList=get_index_stocks('399101.XSHE',begin_date)
        stockList = [stock for stock in stockList if not stock.startswith(('68', '4', '8'))]
    elif stockPool=='small_25':
        initial_list=get_index_stocks('000002.XSHG',begin_date)+get_index_stocks('399107.XSHE',begin_date)
        stockList = list(get_fundamentals(
        query(valuation.code,valuation.market_cap).filter(
            valuation.code.in_(initial_list),
            valuation.market_cap < 25
        ).order_by(
            valuation.circulating_market_cap.asc()
        )).code)[:50]
    
    #剔除ST股
    st_data=get_extras('is_st',stockList, count = 1,end_date=begin_date)
    stockList = [stock for stock in stockList if not st_data[stock][0]]
    #剔除停牌、新股及退市股票
    stockList=delect_stop(stockList,begin_date)
    return stockList
#获取时间为date的全部因子数据
def get_factor_data(securities_list,date,jqfactors_list):
    factor_data = get_factor_values(securities=securities_list,                                     factors=jqfactors_list,                                     count=1,                                     end_date=date)
    df_jq_factor=pd.DataFrame(index=securities_list)
    for i in factor_data.keys():
        df_jq_factor[i]=factor_data[i].iloc[0,:]
    return df_jq_factor
dateList = get_period_date(peroid,start_date, end_date)
print(len(dateList))


# In[4]:


xx = []

xx.append(['inventory_turnover_rate', 'sales_to_price_ratio', 'share_turnover_monthly', 'natural_log_of_market_cap'])  # score = 2.5936
xx.append(['size', 'roe_ttm', 'TVSTD20', 'current_asset_turnover_rate'])  # score = 2.0640
xx.append(['TVMA6', 'financial_expense_ttm'])  # score = 2.0574
xx.append(['VOL10', 'circulating_market_cap', 'single_day_VPT_12'])  # score = 1.9164
xx.append(['money_flow_20', 'adjusted_profit_to_total_profit'])  # score = 1.8782
xx.append(['super_quick_ratio', 'cube_of_size', 'cfo_to_ev'])  # score = 1.3558
# xx.append(['cash_to_current_liability', 'TVSTD20', 'operating_tax_to_operating_revenue_ratio_ttm', 'Price3M'])  # score = 1.2482
# xx.append(['liquidity', 'value_change_profit_ttm', 'roa_ttm'])  # score = 1.2267
# xx.append(['VSTD10', 'ROC60'])  # score = 1.0209
# xx.append(['accounts_payable_turnover_rate', 'net_operating_cash_flow_coverage', 'TVSTD20', 'quick_ratio'])  # score = 0.9247
# xx.append(['net_operate_cash_flow_ttm', 'TVMA6', 'total_profit_ttm', 'Kurtosis60', 'relative_strength'])  # score = 0.9177
# xx.append(['sharpe_ratio_120', 'intangible_asset_ratio', 'Skewness60', 'ROC20', 'single_day_VPT_6'])  # score = 0.8259
# xx.append(['net_operating_cash_flow_coverage', 'accounts_payable_turnover_days', 'average_share_turnover_quarterly', 'non_linear_size', 'bull_power'])  # score = 0.7995
# xx.append(['non_current_asset_ratio', 'admin_expense_rate', 'ATR6', 'VOL20'])  # score = 0.7880
# xx.append(['ROC120', 'VOL5', 'arron_up_25', 'SGI'])  # score = 0.7880
# xx.append(['MAC120', 'total_asset_growth_rate', 'financing_cash_growth_rate', 'money_flow_20'])  # score = 0.7361
# xx.append(['average_share_turnover_annual', 'operating_cost_to_operating_revenue_ratio', 'DSRI', 'money_flow_20', 'MAC120'])  # score = 0.7286
# xx.append(['debt_to_assets', 'operating_cost_to_operating_revenue_ratio', 'DAVOL20', 'price_no_fq', 'sales_growth'])  # score = 0.7155
# xx.append(['VSTD10', 'TVMA20', 'net_asset_per_share'])  # score = 0.6892
# xx.append(['Price3M', 'residual_volatility', 'Volume1M', 'current_asset_turnover_rate', 'momentum'])  # score = 0.6205
# xx.append(['TVSTD6', 'cashflow_per_share_ttm', 'sharpe_ratio_120', 'non_operating_net_profit_ttm'])  # score = 0.5182
# xx.append(['financial_liability', 'VOL240', 'administration_expense_ttm'])  # score = 0.5044
# xx.append(['net_non_operating_income_to_total_profit', 'Skewness120', 'MAC60', 'VOL10'])  # score = 0.4616
# xx.append(['VROC12', 'gross_profit_ttm', 'VEMA12', 'Price3M', 'interest_carry_current_liability'])  # score = 0.4501
# xx.append(['total_operating_cost_ttm', 'total_operating_revenue_per_share_ttm', 'Kurtosis20', 'BIAS60', 'circulating_market_cap'])  # score = 0.4458
# xx.append(['non_current_asset_ratio', 'admin_expense_rate', 'VOL20'])  # score = 0.4324
# xx.append(['TVSTD6', 'market_leverage', 'Kurtosis20', 'BIAS60'])  # score = 0.4323
# xx.append(['single_day_VPT_6', 'EMAC120'])  # score = 0.4314
# xx.append(['TVMA6', 'BIAS60', 'intangible_asset_ratio'])  # score = 0.3978
# xx.append(['MAC120', 'operating_revenue_per_share_ttm', 'net_debt', 'earnings_to_price_ratio'])  # score = 0.3705
# xx.append(['TVSTD20', 'VOL5', 'growth', 'net_asset_growth_rate', 'EMA5'])  # score = 0.3208
# xx.append(['operating_profit_growth_rate', 'roe_ttm_8y', 'net_working_capital', 'VEMA26'])  # score = 0.3147
# xx.append(['operating_revenue_growth_rate', 'surplus_reserve_fund_per_share', 'VSTD20', 'net_operate_cash_flow_to_operate_income'])  # score = 0.2300
# xx.append(['MAC120', 'net_operate_cash_flow_to_total_liability', 'average_share_turnover_quarterly'])  # score = 0.1933
# xx.append(['Price1Y', 'total_profit_to_cost_ratio', 'VOL120'])  # score = 0.1903
# xx.append(['momentum', 'current_ratio', 'TVSTD6', 'Variance20', 'equity_to_asset_ratio'])  # score = 0.0960
# xx.append(['Volume1M', 'BIAS60', 'Price1M', 'cash_earnings_to_price_ratio'])  # score = 0.0524
# xx.append(['TVMA20', 'VEMA12', 'VSTD10', 'sharpe_ratio_20', 'single_day_VPT_6'])  # score = -0.0110
# xx.append(['roic_ttm', 'net_operate_cash_flow_per_share', 'EMAC120'])  # score = -0.0118
# xx.append(['MAC5', 'MLEV', 'EMAC120', 'fifty_two_week_close_rank'])  # score = -0.0313
# xx.append(['VSTD20', 'account_receivable_turnover_rate', 'long_term_debt_to_asset_ratio', 'OperatingCycle'])  # score = -0.0516
# xx.append(['MACDC', 'CCI20', 'EMAC20'])  # score = -0.0916
# xx.append(['price_no_fq', 'total_profit_to_cost_ratio', 'inventory_turnover_rate'])  # score = -0.0926
# xx.append(['Price1Y', 'MAC60', 'single_day_VPT_6', 'TVSTD20', 'cash_earnings_to_price_ratio'])  # score = -0.1420
# xx.append(['CCI15', 'EMAC120', 'roe_ttm', 'long_term_predicted_earnings_growth', 'net_working_capital'])  # score = -0.2337
# xx.append(['BIAS60', 'CR20', 'PLRC6', 'Variance120'])  # score = -0.3238
# xx.append(['net_profit_ratio', 'MAC60', 'Variance120', 'financial_expense_ttm', 'growth'])  # score = -0.3906
# xx.append(['turnover_volatility', 'maximum_margin', 'equity_turnover_rate', 'EMAC12'])  # score = -0.5861
# xx.append(['AR', 'MAWVAD', 'VEMA10', 'bull_power'])  # score = -0.6329
# xx.append(['VOL60', 'TVSTD20', 'BBIC', 'goods_service_cash_to_operating_revenue_ttm'])  # score = -0.6459
# xx.append(['Variance120', 'EMAC26', 'VOL120', 'bull_power', 'EMA5'])  # score = -0.6976
# xx.append(['ATR14', 'BIAS60', 'TRIX10', 'arron_down_25', 'sharpe_ratio_120'])  # score = -0.8104
# xx.append(['BBIC', 'MAC120', 'VROC12', 'Variance60'])  # score = -0.8322
# xx.append(['ARBR', 'SGAI', 'net_profit_to_total_operate_revenue_ttm', 'retained_profit_per_share'])  # score = -0.8467
# xx.append(['operating_revenue_growth_rate', 'total_profit_growth_rate', 'net_profit_growth_rate', 'earnings_growth', 'eps_ttm'])  # score = -1.0901
# xx.append(['MFI14', 'DEGM_8y', 'MAC10', 'EMAC26'])  # score = -1.1342
# xx.append(['BIAS5', 'np_parent_company_owners_growth_rate', 'ROC6', 'MAC60'])  # score = -1.2727
# xx.append(['debt_to_assets', 'BIAS10', 'ROC120', 'leverage'])  # score = -1.2893
# xx.append(['BIAS5', 'CR20', 'VDIFF', 'VEMA5', 'money_flow_20'])  # score = -1.4777
# xx.append(['ATR6', 'PLRC12', 'Price1Y', 'ROC60', 'VMACD'])  # score = -1.6884
# xx.append(['BIAS10', 'TRIX10', 'BIAS5'])  # score = -1.7511
# xx.append(['VROC6', 'equity_to_asset_ratio', 'Price1M', 'MAC120', 'boll_down'])  # score = -1.9603
# xx.append(['TVMA20', 'bear_power', 'MAC20', 'TRIX5'])  # score = -3.6090

# xx.append(['MAC120', 'EMAC20', 'EMA5', 'EMAC26'])  # score = -0.4767
# xx.append(['arron_down_25', 'book_to_price_ratio', 'earnings_yield', 'MAC5', 'MAC20'])  # score = -0.9538
# xx.append(['sales_to_price_ratio', 'fifty_two_week_close_rank', 'BBIC', 'Rank1M'])  # score = -0.9809
# xx.append(['EMAC120', 'boll_down', 'EMAC12', 'EMAC10', 'MAC60', 'MAC10'])  # score = -2.6940



xx_all = list(set([item for sublist in xx for item in sublist]))

print(xx_all)


# In[ ]:


jqfactors_list= xx_all

train_data=pd.DataFrame()
train_length = 11*12*4
for date in tqdm(dateList[:train_length]):
    try:
        stockList=get_stock('small',date)
        print(len(stockList))
        factor_solve_data = get_factor_data(stockList,date,jqfactors_list)
        data_close=get_price(stockList,date,dateList[dateList.index(date)+1],'1d','close')['close']
        factor_solve_data['pchg']=data_close.iloc[-1]/data_close.iloc[1]-1
        factor_solve_data['date']=date
        if train_data.empty:
            train_data=factor_solve_data
        else:
            train_data=train_data.append(factor_solve_data)
    except:
        pass
            
train_data.to_csv(r'train_baseline_2.0_1.csv')
print(len(train_data))  


# In[ ]:


train_data=pd.DataFrame()
for date in tqdm(dateList[train_length:-1]):
    try:
        stockList=get_stock('small',date)
        factor_solve_data = get_factor_data(stockList,date,jqfactors_list)
        data_close=get_price(stockList,date,dateList[dateList.index(date)+1],'1d','close')['close']
        factor_solve_data['pchg']=data_close.iloc[-1]/data_close.iloc[1]-1
        factor_solve_data['date']=date
        if train_data.empty:
            train_data=factor_solve_data
        else:
            train_data=train_data.append(factor_solve_data)
    except:
        pass
            
train_data.to_csv(r'test_baseline_2.0_1.csv')
print(len(train_data))


# In[ ]:


import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score
import pickle
from xgboost import XGBClassifier ,XGBRegressor
import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score
import pickle
from xgboost import XGBClassifier ,XGBRegressor
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score, confusion_matrix, recall_score, precision_score
from sklearn.metrics import precision_recall_curve, auc
import lightgbm as lgb 
import xgboost as xgb 
import joblib  
from sklearn.linear_model import Ridge,BayesianRidge
from sklearn.metrics import mean_squared_error, r2_score

jqfactors_list= xx_all

X_train = pd.read_csv('train_baseline_2.0_1.csv').fillna(0)
X_test = pd.read_csv('test_baseline_2.0_1.csv').fillna(0)
# X_train = pd.read_csv('train_baseline_2.0_1.csv')
# split_index = int(len(X_train) * (2/3))
# X_train =X_train[split_index:]
# X_test = pd.read_csv('test_baseline_2.0_1.csv')


columns_to_fill = [col for col in jqfactors_list if col in X_train.columns]
df_filled_train = X_train.copy()
for column in columns_to_fill:
    df_filled_train[column] = X_train.groupby('date')[column].transform(lambda x: x.fillna(x.median()))
X_train = df_filled_train.dropna()

df_filled_test = X_test.copy()
for column in columns_to_fill:
    df_filled_test[column] = X_test.groupby('date')[column].transform(lambda x: x.fillna(x.median()))
X_test = df_filled_test.dropna()



y_train = X_train['pchg']
y_test =X_test['pchg']


# In[ ]:



from sklearn.linear_model import BayesianRidge
from sklearn.metrics import mean_squared_error, r2_score

predictions = []
factor_list = []

for i in xx:
    jqfactors_list0 = i
    X_train0 = X_train[jqfactors_list0]
    X_test0 = X_test[jqfactors_list0]

    Bridge0 = BayesianRidge()
    Bridge0.fit(X_train0, y_train)

    bridge_manual_predictions0 = np.dot(X_test0, Bridge0.coef_)
    bridge_manual_mse = mean_squared_error(y_test, bridge_manual_predictions0)
    bridge_manual_r2 = r2_score(y_test, bridge_manual_predictions0)

    predictions.append(bridge_manual_predictions0)

    print("########################")
    print(i)
    result = ",".join([f"{x:.10f}" for x in Bridge0.coef_.tolist()])
    print(f"[{result}]")
    print("intercept:", Bridge0.intercept_)

    print("\nBayesian Ridge Regression (Manual Prediction):")
    print("Mean Squared Error:", bridge_manual_mse)
    print("R^2 Score:", bridge_manual_r2)

    # 生成 factor_list 中的一项
    factor_list.append(
        (jqfactors_list0, Bridge0.coef_.tolist(), Bridge0.intercept_)
    )

# 打印出符合格式的 factor_list
print("\n\nfactor_list = [")
for factors, coefs, intercept in factor_list:
    factors_str = "[" + ", ".join([f"'{f}'" for f in factors]) + "]"
    coefs_str = "[" + ", ".join([f"{c:.10f}" for c in coefs]) + "]"
    print(f"    ({factors_str}, {coefs_str}, {intercept:.2f}),")
print("]")


##########
print("clean factor_list:")

# 处理并打印符合格式的 factor_list，去除系数为 0 的因子
print("\n\nfactor_list = [")
for factors, coefs, intercept in factor_list:
    # 过滤掉系数为0的因子和对应系数
    filtered = [(f, c) for f, c in zip(factors, coefs) if abs(c) > 1e-10]
    if not filtered:
        continue  # 如果全是0，就跳过这一组
    filtered_factors, filtered_coefs = zip(*filtered)
    factors_str = "[" + ", ".join([f"'{f}'" for f in filtered_factors]) + "]"
    coefs_str = "[" + ", ".join([f"{c:.10f}" for c in filtered_coefs]) + "]"
    print(f"    ({factors_str}, {coefs_str}, {intercept:.10f}),")
print("]")


# In[ ]:


import matplotlib.pyplot as plt

def calculate_layered_returns(result_df, returns_df, num_layers=20):
    backtest_results = pd.DataFrame(columns=[f'Group_{i}' for i in range(1, num_layers + 1)])

    for date in result_df.index:
        # 获取当天的因子值和收益率
        factors = result_df.loc[date]
        returns = returns_df.loc[date]

        # 合并因子值和收益率到一个DataFrame中
        combined_data = pd.DataFrame({'Factor': factors, 'Returns': returns})

        # 按因子值排序
        combined_data = combined_data.sort_values(by='Factor', ascending=False)

        # 分成num_layers组，每组数量相等
        group_size = len(combined_data) // num_layers

        groups = []
        for i in range(num_layers):
            start_idx = i * group_size
            end_idx = (i + 1) * group_size
            group = combined_data.iloc[start_idx:end_idx]
            groups.append(group)

        # 计算每个组的累积收益率
        group_returns = []
        for group in groups:
            group_return = group['Returns'].sum()
            group_returns.append(group_return)

        # 将每个组的累积收益率添加到结果DataFrame中
        backtest_results.loc[date] = [i/group_size for i in group_returns]

    return backtest_results

# predictions = [bridge_manual_predictions0]
#predictions = [bridge_manual_predictions0,bridge_manual_predictions02,bridge_manual_predictions2,bridge_manual_predictions3,bridge_manual_predictions4,bridge_manual_predictions5]

X_test.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
for i in range(len(predictions)):
    y_pred_proba =predictions[i]
    X_test['factor'] = y_pred_proba
    factor = X_test.set_index(['id', 'date'])['factor']
    factor = factor.unstack(level='id')
    ret = X_test.set_index(['id', 'date'])['pchg']
    ret = ret.unstack(level='id')
    backtest_results = calculate_layered_returns(factor, ret, num_layers=5)
    
    plt.figure()
    backtest_results.cumsum().plot()
    plt.title(f'{xx[i]}')
    plt.show()


# In[ ]:


def calculate_layered_returns_withmac(result_df, returns_df, market_cap_df=None, num_layers=20):
    backtest_results = pd.DataFrame(columns=[f'Group_{i}' for i in range(1, num_layers + 1)])

    if market_cap_df is not None:
        backtest_results['TinyCapTopGroup'] = np.nan  # 新增分组

    for date in result_df.index:
        factors = result_df.loc[date]
        returns = returns_df.loc[date]

        combined_data = pd.DataFrame({
            'Factor': factors,
            'Returns': returns
        })

        if market_cap_df is not None:
            combined_data['MarketCap'] = market_cap_df.loc[date]

        # 删除NA
        combined_data = combined_data.dropna()

        # 按因子值降序排序
        combined_data = combined_data.sort_values(by='Factor', ascending=False)

        # 分组
        group_size = len(combined_data) // num_layers
        groups = []
        for i in range(num_layers):
            start_idx = i * group_size
            end_idx = (i + 1) * group_size if i < num_layers - 1 else len(combined_data)
            group = combined_data.iloc[start_idx:end_idx]
            groups.append(group)

        # 各组平均收益
        group_returns = [group['Returns'].mean() for group in groups]
        backtest_results.loc[date, [f'Group_{i}' for i in range(1, num_layers + 1)]] = group_returns

        # 构造 TinyCapTopGroup
        if market_cap_df is not None and len(groups) > 0:
            top_group = groups[0]  # Group_1：因子值最高的一组
            tiny_top10 = top_group.sort_values(by='MarketCap').head(1)
            if not tiny_top10.empty:
                tiny_cap_return = tiny_top10['Returns'].mean()
                backtest_results.loc[date, 'TinyCapTopGroup'] = tiny_cap_return

    return backtest_results



X_test.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
for i in range(len(predictions)):
    y_pred_proba =predictions[i]
    X_test['factor'] = y_pred_proba
    factor = X_test.set_index(['id', 'date'])['factor']
    factor = factor.unstack(level='id')
    ret = X_test.set_index(['id', 'date'])['pchg']
    ret = ret.unstack(level='id')
    
    # 假设 X_test 中包含 circulating_market_cap
    X_test.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
    X_test['market_cap'] = X_test['circulating_market_cap']

    # 转换为日期-股票结构
    factor = X_test.set_index(['id', 'date'])['factor'].unstack(level='id')
    ret = X_test.set_index(['id', 'date'])['pchg'].unstack(level='id')
    market_cap = X_test.set_index(['id', 'date'])['market_cap'].unstack(level='id')

    # 计算回测结果（含 TinyCapTopGroup）
    backtest_results = calculate_layered_returns_withmac(factor, ret, market_cap_df=market_cap, num_layers=5)
    
    plt.figure()
    backtest_results.cumsum().plot()
    plt.title(f'{xx[i]}')
    plt.show()
    


# In[ ]:


# predictions = [bridge_manual_predictions2,bridge_manual_predictions3,bridge_manual_predictions4]

X_test.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
y_pred_proba=0
for i in range(len(predictions)):
    y_pred_proba +=predictions[i]
    
X_test['factor'] = y_pred_proba
factor = X_test.set_index(['id', 'date'])['factor']
factor = factor.unstack(level='id')
ret = X_test.set_index(['id', 'date'])['pchg']
ret = ret.unstack(level='id')
backtest_results = calculate_layered_returns(factor, ret, num_layers=10)
backtest_results.cumsum().plot()


# In[ ]:


import pandas as pd

import matplotlib.pyplot as plt

def calculate_layered_scores(result_df, returns_df, num_layers=20):
    """
    计算分层收益率并返回得分，用于比较不同预测结果。
    """
    backtest_results = pd.DataFrame(columns=[f'Group_{i}' for i in range(1, num_layers + 1)])

    for date in result_df.index:
        # 获取当天的因子值和收益率
        factors = result_df.loc[date]
        returns = returns_df.loc[date]

        # 合并因子值和收益率到一个DataFrame中
        combined_data = pd.DataFrame({'Factor': factors, 'Returns': returns})

        # 按因子值排序
        combined_data = combined_data.sort_values(by='Factor', ascending=False)

        # 分成num_layers组，每组数量相等
        group_size = len(combined_data) // num_layers
        groups = [combined_data.iloc[i * group_size:(i + 1) * group_size] for i in range(num_layers)]

        # 计算每个组的累计收益率
        group_returns = [group['Returns'].sum() for group in groups]

        # 将每个组的累积收益率添加到结果DataFrame中
        backtest_results.loc[date] = group_returns

    # 计算多空策略收益率（即顶层减去底层）
    long_short_returns = backtest_results[f'Group_1'] - backtest_results[f'Group_{num_layers}']

    # 计算得分：可根据需求修改，例如取累计收益率、平均收益率等
    score = long_short_returns.sum()

    return score


def calculate_layered_scores2(result_df, returns_df, num_layers=20):
    """
    计算分层收益率并返回得分，用于比较不同预测结果。
    修改说明：确保正确分组并计算平均收益率，保证顶层收益最优。
    """
    backtest_results = pd.DataFrame(columns=[f'Group_{i}' for i in range(1, num_layers + 1)])

    for date in result_df.index:
        # 获取当天的因子值和收益率
        factors = result_df.loc[date]
        returns = returns_df.loc[date]

        # 合并因子值和收益率到一个DataFrame中
        combined_data = pd.DataFrame({'Factor': factors, 'Returns': returns})

        # 按因子值降序排序（假设因子值越高收益越高）
        combined_data = combined_data.sort_values(by='Factor', ascending=False)

        # 分成num_layers组，正确处理余数以确保所有股票被分组
        n = len(combined_data)
        group_size = n // num_layers
        remainder = n % num_layers
        groups = []
        start = 0
        for i in range(num_layers):
            # 前remainder组每组多分配一个股票
            end = start + group_size + (1 if i < remainder else 0)
            group = combined_data.iloc[start:end]
            groups.append(group)
            start = end

        # 计算每个组的平均收益率（确保组间可比性）
        group_returns = [group['Returns'].mean() for group in groups]

        # 记录各组的平均收益率
        backtest_results.loc[date] = group_returns

    # 计算多空策略收益率（顶层平均收益 - 底层平均收益）
    long_short_returns = backtest_results['Group_1'] - backtest_results[f'Group_{num_layers}']

    # 得分：多空策略累计收益
    score = long_short_returns.sum()

    return score

def calculate_layered_scores3(result_df, returns_df, num_layers=100, smooth_window=10):
    """
    计算稳定的顶层收益，确保顶层收益稳定，适用于层数很多（如100层）的情况。
    修改说明：
    1. 适应更多层数的分组处理。
    2. 对顶层收益进行平滑（移动平均），提高收益的稳定性。
    """
    backtest_results = pd.DataFrame(columns=[f'Group_{i}' for i in range(1, num_layers + 1)])

    for date in result_df.index:
        # 获取当天的因子值和收益率
        factors = result_df.loc[date]
        returns = returns_df.loc[date]

        # 合并因子值和收益率到一个DataFrame中
        combined_data = pd.DataFrame({'Factor': factors, 'Returns': returns})

        # 按因子值降序排序（假设因子值越高收益越高）
        combined_data = combined_data.sort_values(by='Factor', ascending=False)

        # 分成num_layers组，正确处理余数以确保所有股票被分组
        n = len(combined_data)
        group_size = n // num_layers
        remainder = n % num_layers
        groups = []
        start = 0
        for i in range(num_layers):
            # 前remainder组每组多分配一个股票
            end = start + group_size + (1 if i < remainder else 0)
            group = combined_data.iloc[start:end]
            groups.append(group)
            start = end

        # 计算每个组的平均收益率（确保组间可比性）
        group_returns = [group['Returns'].mean() for group in groups]

        # 记录各组的平均收益率
        backtest_results.loc[date] = group_returns

    # 获取顶层收益（Group_1）
    top_layer_returns = backtest_results['Group_1']

    # 对顶层收益进行平滑处理（使用滑动平均平滑波动）
    smoothed_top_layer_returns = top_layer_returns.rolling(window=smooth_window, min_periods=1).mean()

    # 计算最终得分：使用平滑后的顶层收益
    score = smoothed_top_layer_returns.sum()

    return score


def calculate_layered_scores4(result_df, returns_df, num_layers=100, smooth_window=10):
    """
    在层数很多时确保顶层收益表现好。通过调整分层方式、给顶层更高的权重等手段，减少噪声。
    """
    backtest_results = pd.DataFrame(columns=[f'Group_{i}' for i in range(1, num_layers + 1)])

    for date in result_df.index:
        # 获取当天的因子值和收益率
        factors = result_df.loc[date]
        returns = returns_df.loc[date]

        # 合并因子值和收益率到一个DataFrame中
        combined_data = pd.DataFrame({'Factor': factors, 'Returns': returns})

        # 排序，假设因子值越高收益越高
        combined_data = combined_data.sort_values(by='Factor', ascending=False)

        # 根据分布调整分层策略：避免过于均匀的分层，确保每层有足够的差异
        n = len(combined_data)
        group_size = n // num_layers
        remainder = n % num_layers
        groups = []
        start = 0
        for i in range(num_layers):
            end = start + group_size + (1 if i < remainder else 0)
            group = combined_data.iloc[start:end]
            groups.append(group)
            start = end

        # 计算每组的平均收益率
        group_returns = [group['Returns'].mean() for group in groups]

        # 记录各组的收益率
        backtest_results.loc[date] = group_returns

    # 获取顶层收益（Group_1）并平滑
    top_layer_returns = backtest_results['Group_1']
    smoothed_top_layer_returns = top_layer_returns.rolling(window=smooth_window, min_periods=1).mean()

    # 对顶层收益加权：确保顶层收益的贡献更大
    weighted_top_layer_returns = smoothed_top_layer_returns * 1.5  # 例如，给顶层更高的权重

    # 计算最终得分：平滑后顶层收益 + 给顶层加权的收益
    score = weighted_top_layer_returns.sum()

    return score

def calculate_score(y_pred_proba, X_test, calculate_layered_scores4):
    """
    Calculate the score based on the predicted probabilities (y_pred_proba).

    Args:
    - y_pred_proba (pd.Series): Predicted probabilities from the model.
    - X_test (pd.DataFrame): DataFrame containing the test data, including 'id', 'date', and 'pchg'.
    - calculate_layered_scores4 (function): Function to calculate the score from the factor and return series.

    Returns:
    - score (float): The calculated score based on the predicted probabilities.
    """
    # Add the predicted probabilities as a factor column
    X_test['factor'] = y_pred_proba
    
    # Create the factor and return (ret) dataframes
    factor = X_test.set_index(['id', 'date'])['factor'].unstack(level='id')
    ret = X_test.set_index(['id', 'date'])['pchg'].unstack(level='id')

    # Calculate the score using the provided function
    score = calculate_layered_scores4(factor, ret, num_layers=100)
    
    return score


# 计算各个 predictions 的得分
# scores = []

# for i in range(len(predictions)):
#     y_pred_proba = predictions[i]
#     X_test['factor'] = y_pred_proba
#     factor = X_test.set_index(['id', 'date'])['factor']
#     factor = factor.unstack(level='id')
#     ret = X_test.set_index(['id', 'date'])['pchg']
#     ret = ret.unstack(level='id')

#     # 计算当前预测结果的得分
#     score = calculate_layered_scores4(factor, ret, num_layers=100)
#     scores.append(score)

scores = []
for i in range(len(predictions)):
    y_pred_proba = predictions[i]
    
    # Calculate score for each set of predicted probabilities
    score = calculate_score(y_pred_proba, X_test, calculate_layered_scores4)
    scores.append(score)






sorted_scores = sorted(enumerate(scores, start=1), key=lambda x: x[1], reverse=True)

new_predictions =[]
max =5
i = 0
print("Models sorted by performance:")
for idx, score in sorted_scores:
    print(f"{xx[idx-1]}")
    print(f"Model {idx}: Score = {score}")
    if i < max:
        new_predictions.append(predictions[idx-1])
        i = i + 1
print("\n\n")        

print("Models sorted for use:")
max =5
i = 0
print("factor_list = [")
for idx, score in sorted_scores:
    if i < max:
        factors, coefs, intercept = factor_list[idx - 1]  # 注意 idx 是从 1 开始的
        factors_str = "[" + ", ".join([f"'{f}'" for f in factors]) + "]"
        coefs_str = "[" + ", ".join([f"{c:.10f}" for c in coefs]) + "]"
        print(f"    ({factors_str}, {coefs_str}, {intercept:.2f}),")
        i = i + 1
print("]")

print("\n\n")
print("clean factor_list:")
max =5
i = 0
# 处理并打印符合格式的 factor_list，去除系数为 0 的因子
print("\n\nfactor_list = [")
for idx, score in sorted_scores:
    if i < max:
        factors, coefs, intercept = factor_list[idx - 1]  # 还是要注意 idx 从 1 开始
        # 去除系数为 0 的因子
        filtered = [(f, c) for f, c in zip(factors, coefs) if abs(c) > 1e-10]
        if not filtered:
            continue  # 如果全部系数为 0，跳过

        filtered_factors, filtered_coefs = zip(*filtered)
        factors_str = "[" + ", ".join([f"'{f}'" for f in filtered_factors]) + "]"
        coefs_str = "[" + ", ".join([f"{c:.10f}" for c in filtered_coefs]) + "]"

        print(f"    ({factors_str}, {coefs_str}, {intercept:.10f}),  # score = {score:.4f}")
        i = i + 1
print("]")

print("\n\n")
print("not clean append:")
for idx, score in sorted_scores:
    print(f"xx.append({xx[idx-1]})  # score = {score:.4f}")


# # predictions = [bridge_manual_predictions2,bridge_manual_predictions3,bridge_manual_predictions4]
# 
# X_test.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
# y_pred_proba=0
# for i in range(len(new_predictions)):
#     y_pred_proba +=new_predictions[i]
#     
# X_test['factor'] = y_pred_proba
# factor = X_test.set_index(['id', 'date'])['factor']
# factor = factor.unstack(level='id')
# ret = X_test.set_index(['id', 'date'])['pchg']
# ret = ret.unstack(level='id')
# backtest_results = calculate_layered_returns(factor, ret, num_layers=100)
# backtest_results.cumsum().plot()

# In[ ]:


X_test.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
y_pred_proba=0
for i in range(len(new_predictions)):
    y_pred_proba +=new_predictions[i]
    
X_test['factor'] = y_pred_proba
factor = X_test.set_index(['id', 'date'])['factor']
factor = factor.unstack(level='id')
ret = X_test.set_index(['id', 'date'])['pchg']
ret = ret.unstack(level='id')
backtest_results = calculate_layered_returns(factor, ret, num_layers=30)
backtest_results.cumsum().plot()


# In[ ]:





# In[ ]:





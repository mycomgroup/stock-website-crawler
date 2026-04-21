#!/usr/bin/env python
# coding: utf-8

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

def get_period_date(peroid,start_date, end_date):
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

def delect_stop(stocks,beginDate,n=30*3):
    stockList=[]
    beginDate = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    for stock in stocks:
        start_date=get_security_info(stock).start_date
        if start_date<(beginDate-datetime.timedelta(days=n)).date():
            stockList.append(stock)
    return stockList

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

    st_data=get_extras('is_st',stockList, count = 1,end_date=begin_date)
    stockList = [stock for stock in stockList if not st_data[stock][0]]
    stockList=delect_stop(stockList,begin_date)
    return stockList

def get_factor_data(securities_list,date,jqfactors_list):
    factor_data = get_factor_values(securities=securities_list,
                                    factors=jqfactors_list,
                                    count=1,
                                    end_date=date)
    df_jq_factor=pd.DataFrame(index=securities_list)
    for i in factor_data.keys():
        df_jq_factor[i]=factor_data[i].iloc[0,:]
    return df_jq_factor

all_factors = get_all_factors()
jqfactors_list = all_factors['factor'].tolist()
print(f"Total factors: {len(jqfactors_list)}")
print(jqfactors_list)

peroid = 'W'
start_date = '2025-05-07'
end_date = '2025-06-15'
dateList = get_period_date(peroid,start_date, end_date)
print(f"Weekly dates: {dateList}")

train_data=pd.DataFrame()

for i in tqdm(range(len(dateList[:-1]))):
    date = dateList[i]
    stockList=get_stock('small',date)
    print(f"Date: {date}, Stocks: {len(stockList)}")

    factor_solve_data = get_factor_data(stockList,date,jqfactors_list)

    if i + 1 < len(dateList):
        future_date = dateList[i + 1]
        data_close=get_price(stockList,date,future_date,'daily',fields=['close'],fill_panel=False)['close']
        if data_close.shape[0] >= 2:
            factor_solve_data['pchg'] = data_close.iloc[-1] / data_close.iloc[0] - 1
        else:
            continue
    else:
        continue

    factor_solve_data['date'] = date
    train_data = pd.concat([train_data, factor_solve_data], ignore_index=False)

output_file = 'all_factors_weekly_data.csv'
train_data.to_csv(output_file)
print(f"Saved to {output_file}, total rows: {len(train_data)}")
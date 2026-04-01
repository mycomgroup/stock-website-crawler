# 样本外数据管理方案

## 一、数据需求清单

### 1.1 行情数据

#### 1.1.1 日线数据（核心）

| 数据字段 | 字段说明 | 用途 | 必要性 | 更新频率 |
|---------|---------|------|--------|---------|
| stock_code | 股票代码 | 标识 | 必需 | 固定 |
| trade_date | 交易日期 | 时间戳 | 必需 | 日频 |
| open | 开盘价 | OHLC基础 | 必需 | 日频 |
| high | 最高价 | OHLC基础 | 必需 | 日频 |
| low | 最低价 | OHLC基础 | 必需 | 日频 |
| close | 收盘价 | OHLC基础 | 必需 | 日频 |
| volume | 成交量 | 交易活跃度 | 必需 | 日频 |
| amount | 成交额 | 流动性评估 | 必需 | 日频 |
| turnover_rate |换手率 | 流动性评估 | 建议 | 日频 |
| pct_change |涨跌幅 | 策略收益计算 | 必需 | 日频 |

#### 1.1.2 分钟线数据（可选）

| 数据字段 | 字段说明 | 用途 | 必要性 | 更新频率 |
|---------|---------|------|--------|---------|
| minute_time | 分钟时间戳 | 精确入场时机分析 | 建议 | 日频 |
| minute_price | 分钟价格 | 滑点分析 | 建议 | 日频 |
| minute_volume | 分钟成交量 | 流动性分析 | 建议 | 日频 |

#### 1.1.3 竞价数据（可选）

| 数据字段 | 字段说明 | 用途 | 必要性 | 更新频率 |
|---------|---------|------|--------|---------|
| call_open | 竞价开盘价 | 竞价策略分析 | 建议 | 日频 |
| call_volume | 竞价成交量 | 竞价流动性 | 建议 | 日频 |

### 1.2 财务数据

#### 1.2.1 市值与估值数据

| 数据字段 | 字段说明 | 用途 | 必要性 | 更新频率 |
|---------|---------|------|--------|---------|
| market_cap | 总市值 | 股票池筛选 | 必需 | 日频 |
| circulating_cap | 流通市值 | 流动性评估 | 必需 | 日频 |
| pe_ratio | 市盈率PE | 估值评估 | 建议 | 日频 |
| pb_ratio | 市净率PB | 估值评估 | 建议 | 日频 |
| ps_ratio | 市销率PS | 估值评估 | 可选 | 日频 |

#### 1.2.2 财务质量数据

| 数据字段 | 字段说明 | 用途 | 必要性 | 更新频率 |
|---------|---------|------|--------|---------|
| roe | 净资产收益率 | 质量筛选 | 建议 | 季频 |
| roa | 总资产收益率 | 质量筛选 | 可选 | 季频 |
| debt_ratio | 资产负债率 | 风险评估 | 建议 | 季频 |
| current_ratio | 流动比率 | 风险评估 | 可选 | 季频 |
| net_profit_growth | 净利润增长率 | 成长性评估 | 建议 | 季频 |

### 1.3 情绪数据（核心）

#### 1.3.1 板块情绪指标

| 数据字段 | 字段说明 | 用途 | 必要性 | 更新频率 |
|---------|---------|------|--------|---------|
| limit_up_count | 涨停股数量 | 市场情绪温度计 | 必需 | 日频 |
| limit_down_count | 贩停股数量 | 市场恐慌指标 | 必需 | 日频 |
| limit_up_limit_down_ratio | 涨跌停比例 | 情绪方向 | 必需 | 日频 |
| max_consecutive_board | 最高连板数 | 接力情绪强度 | 必需 | 日频 |
| avg_board_count | 平均连板数 | 接力情绪广度 | 建议 | 日频 |

#### 1.3.2 板块分布数据

| 数据字段 | 字段说明 | 用途 | 必要性 | 更新频率 |
|---------|---------|------|--------|---------|
| board_distribution | 连板分布统计 | 接力结构分析 | 必需 | 日频 |
| sector_limit_up_count | 各板块涨停数 | 板块轮动分析 | 建议 | 日频 |
| consecutive_board_distribution | 连板股票分布 | 接力机会分析 | 必需 | 日频 |

### 1.4 广度数据（核心）

#### 1.4.1 指数广度指标

| 数据字段 | 字段说明 | 用途 | 必要性 | 更新频率 |
|---------|---------|------|--------|---------|
| hs300_above_20d_pct | 沪深300站上20日线比例 | 大盘广度 | 必需 | 日频 |
| zz1000_above_20d_pct | 中证1000站上20日线比例 | 小盘广度 | 必需 | 日频 |
| all_stock_above_20d_pct | 全市场站上20日线比例 | 整体广度 | 建议 | 日频 |

#### 1.4.2 风格因子数据（可选）

| 数据字段 | 字段说明 | 用途 | 必要性 | 更新频率 |
|---------|---------|------|--------|---------|
| small_cap_factor_return | 小市值因子收益 | 风格轮动分析 | 建议 | 日频 |
| value_factor_return | 价值因子收益 | 风格轮动分析 | 建议 | 日频 |
| momentum_factor_return | 动量因子收益 | 风格轮动分析 | 建议 | 日频 |

### 1.5 策略特定数据

#### 1.5.1 二板接力专用数据

| 数据字段 | 字段说明 | 用途 | 必要性 | 更新频率 |
|---------|---------|------|--------|---------|
| board_count | 连板数 | 策略信号核心 | 必需 | 日频 |
| is_limit_up | 是否涨停 | 策略信号核心 | 必需 | 日频 |
| is_limit_up_arrangement | 是否涨停排列 | 策略过滤 | 必需 | 日频 |
| consecutive_limit_up_days | 连续涨停天数 | 接力判断 | 必需 | 日频 |
| open_gap_pct | 开盘涨幅 | 入场时机 | 必需 | 日频 |
| intraday_high_pct | 日内最高涨幅 | 持仓管理 | 建议 | 日频 |

#### 1.5.2 交易记录数据

| 数据字段 | 字段说明 | 用途 | 必要性 | 更新频率 |
|---------|---------|------|--------|---------|
| signal_date | 信号日期 | 交易时间 | 必需 | 日频 |
| signal_stock_code | 信号股票代码 | 交易标的 | 必需 | 日频 |
| signal_price | 信号价格 | 入场价格 | 必需 | 日频 |
| execution_date | 执行日期 | 执行时间 | 必需 | 日频 |
| execution_price | 执行价格 | 实际入场价 | 必需 | 日频 |
| execution_volume | 执行数量 | 交易量 | 必需 | 日频 |
| sell_date | 卖出日期 | 退出时间 | 必需 | 日频 |
| sell_price | 卖出价格 | 退出价格 | 必需 | 日频 |
| sell_reason | 卖出原因 | 退出逻辑 | 必需 | 日频 |
| profit_loss_pct | 盈亏比例 | 收益统计 | 必需 | 日频 |

### 1.6 数据优先级矩阵

| 优先级 | 数据类别 | 具体数据 | 获取难度 | 替代方案 |
|--------|---------|---------|---------|---------|
| P0 | 行情日线 | OHLCV | 低 | 无替代 |
| P0 | 情绪数据 | 涨跌停统计 | 中 | 手动统计 |
| P0 | 广度数据 | 站上20日线比例 | 中 | 自行计算 |
| P1 | 财务数据 | 市值、PE、PB | 低 | 延迟更新 |
| P1 | 策略数据 | 连板数、涨停状态 | 中 | 自行识别 |
| P2 | 分钟线 | 分钟价格/量 | 高 | 仅用日线 |
| P2 | 风格因子 | 因子收益 | 高 | 延迟获取 |

## 二、数据来源方案

### 2.1 主数据源：JoinQuant平台

#### 2.1.1 可获取数据类型

| 数据类别 | 数据内容 | API接口 | 更新频率 | 数据质量 |
|---------|---------|---------|---------|---------|
| 行情数据 | 日线OHLCV、分钟线 | get_price() | T+0 | 高 |
| 财务数据 | 市值、PE、PB、ROE等 | get_fundamentals() | 季报后 | 高 |
| 指数数据 | 沪深300、中证1000 | get_price() | T+0 | 高 |
| 板块数据 | 行业分类、板块涨跌 | get_industry_stocks() | T+0 | 中 |

#### 2.1.2 JoinQuant使用方案

**历史回测**：
```python
# 获取历史日线数据
def fetch_historical_data(start_date, end_date, stock_list):
    """
    从JoinQuant获取历史数据
    
    参数:
    - start_date: 开始日期
    - end_date: 结束日期
    - stock_list: 股票列表
    
    返回:
    - DataFrame: 包含OHLCV等数据
    """
    data = jq.get_price(
        stock_list, 
        start_date=start_date, 
        end_date=end_date,
        frequency='daily',
        fields=['open', 'high', 'low', 'close', 'volume', 'money']
    )
    
    # 获取财务数据
    fundamentals = jq.get_fundamentals(
        jq.query(
            jq.valuation
        ).filter(
            jq.valuation.code.in_(stock_list)
        ),
        start_date
    )
    
    return data.merge(fundamentals, on='code')
```

**实时更新**（模拟）：
```python
# 每日收盘后更新数据
def daily_data_update(current_date):
    """
    每日数据更新流程
    
    参数:
    - current_date: 当前日期
    
    返回:
    - 更新状态
    """
    # 1. 获取当日行情数据
    daily_data = jq.get_price(
        jq.get_all_securities(),
        start_date=current_date,
        end_date=current_date,
        frequency='daily'
    )
    
    # 2. 计算情绪指标
    limit_up_count = count_limit_up_stocks(daily_data)
    limit_down_count = count_limit_down_stocks(daily_data)
    
    # 3. 计算广度指标
    hs300_stocks = jq.get_index_stocks('000300.XSHG')
    hs300_above_20d = calculate_above_ma_pct(hs300_stocks, 20)
    
    # 4. 存储到本地数据库
    save_to_local_db(daily_data, 'daily_price')
    save_to_local_db({'limit_up': limit_up_count}, 'sentiment')
    save_to_local_db({'hs300_above_20d': hs300_above_20d}, 'breadth')
    
    return "success"
```

#### 2.1.3 JoinQuant优势与局限

**优势**：
- 数据质量高，准确性可靠
- API接口稳定，更新及时
- 数据覆盖全市场，完整性好
- 支持回测框架，历史数据完整

**局限**：
- 实盘接口需要实盘账户
- 分钟线数据获取有延迟
- 情绪数据需自行计算
- 广度数据需自行计算

### 2.2 补充数据源

#### 2.2.1 东方财富网（情绪数据）

| 数据类别 | 数据内容 | 获取方式 | 更新频率 | 数据质量 |
|---------|---------|---------|---------|---------|
| 情绪数据 | 涨跌停统计、连板统计 | Web爬虫 | 日频 | 中 |
| 板块数据 | 板块涨跌、板块涨停数 | Web爬虫 | 日频 | 中 |

**爬虫方案**：
```python
# 东方财富涨跌停数据爬虫
def fetch_emotion_data_from_eastmoney(date):
    """
    从东方财富爬取情绪数据
    
    参数:
    - date: 日期
    
    返回:
    - dict: 涨跌停统计
    """
    import requests
    from bs4 import BeautifulSoup
    
    # 爬取涨跌停统计页面
    url = f"http://data.eastmoney.com/zdt/{date}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 提取涨跌停数量
    limit_up_count = extract_limit_up_count(soup)
    limit_down_count = extract_limit_down_count(soup)
    max_board = extract_max_consecutive_board(soup)
    
    return {
        'date': date,
        'limit_up_count': limit_up_count,
        'limit_down_count': limit_down_count,
        'max_consecutive_board': max_board
    }
```

#### 2.2.2 Wind金融终端（可选）

| 数据类别 | 数据内容 | 获取方式 | 更新频率 | 数据质量 |
|---------|---------|---------|---------|---------|
| 高频数据 | 分钟线、竞价数据 | API接口 | 日频 | 高 |
| 风格因子 | 因子收益数据 | API接口 | 日频 | 高 |
| 深度财务 | 详细财务数据 | API接口 | 季频 | 高 |

**Wind优势**：
- 数据质量最高
- 数据覆盖最全
- 更新速度最快

**Wind局限**：
- 需付费订阅
- 成本较高
- 适合专业机构

#### 2.2.3 自建计算方案

**情绪指标计算**：
```python
def calculate_emotion_metrics(date, stock_data):
    """
    自行计算情绪指标
    
    参数:
    - date: 日期
    - stock_data: 全市场股票数据
    
    返回:
    - dict: 情绪指标
    """
    # 涨停判断
    limit_up_stocks = []
    limit_down_stocks = []
    
    for stock in stock_data:
        pct_change = stock['pct_change']
        
        # 涨停判断（考虑精度）
        if pct_change >= 9.9:
            limit_up_stocks.append(stock)
        # 贩停判断
        elif pct_change <= -9.9:
            limit_down_stocks.append(stock)
    
    # 计算连板数
    board_count_distribution = calculate_board_distribution(limit_up_stocks)
    max_board = max(board_count_distribution.keys())
    
    return {
        'date': date,
        'limit_up_count': len(limit_up_stocks),
        'limit_down_count': len(limit_down_stocks),
        'limit_up_limit_down_ratio': len(limit_up_stocks) / (len(limit_down_stocks) + 1),
        'max_consecutive_board': max_board,
        'board_distribution': board_count_distribution
    }
```

**广度指标计算**：
```python
def calculate_breadth_metrics(date, index_stocks, price_data):
    """
    自行计算广度指标
    
    参数:
    - date: 日期
    - index_stocks: 指数成分股
    - price_data: 价格数据
    
    返回:
    - dict: 广度指标
    """
    above_count = 0
    total_count = len(index_stocks)
    
    for stock in index_stocks:
        # 获取近20日数据
        recent_prices = get_recent_prices(stock, 20)
        ma_20 = np.mean(recent_prices)
        current_price = price_data[stock]['close']
        
        if current_price >= ma_20:
            above_count += 1
    
    above_pct = above_count / total_count
    
    return {
        'date': date,
        'index_code': index_code,
        'above_ma_20_pct': above_pct,
        'total_count': total_count,
        'above_count': above_count
    }
```

### 2.3 数据源整合方案

#### 2.3.1 主备数据源架构

```
┌─────────────────────────────────────┐
│     数据源整合架构                    │
├─────────────────────────────────────┤
│                                     │
│  主数据源：JoinQuant                 │
│  ├─ 行情数据（日线）                 │
│  ├─ 财务数据（季报）                 │
│  └─ 指数数据（日线）                 │
│                                     │
│  补充数据源：                        │
│  ├─ 东方财富（情绪数据）             │
│  ├─ Wind终端（可选，高频数据）       │
│  └─ 自建计算（情绪、广度）           │
│                                     │
│  数据整合层：                        │
│  ├─ 数据清洗                        │
│  ├─ 数据验证                        │
│  ├─ 数据融合                        │
│  └─ 数据存储                        │
│                                     │
└─────────────────────────────────────┘
```

#### 2.3.2 数据源切换机制

```python
def fetch_data_with_fallback(data_type, date):
    """
    带容错的数据获取
    
    参数:
    - data_type: 数据类型
    - date: 日期
    
    返回:
    - data: 数据
    """
    # 主数据源尝试
    try:
        data = fetch_from_joinquant(data_type, date)
        if validate_data(data):
            return data
    except Exception as e:
        log_error(f"JoinQuant获取失败: {e}")
    
    # 补充数据源尝试
    try:
        if data_type == 'emotion':
            data = fetch_from_eastmoney(date)
        elif data_type == 'breadth':
            data = calculate_breadth_metrics(date)
        
        if validate_data(data):
            return data
    except Exception as e:
        log_error(f"补充数据源获取失败: {e}")
    
    # 最终容错：使用历史数据或标记缺失
    return get_fallback_data(data_type, date)
```

## 三、数据质量检查方案

### 3.1 完整性检查

#### 3.1.1 检查规则

| 检查项 | 检查方法 | 合格标准 | 异常处理 |
|--------|---------|---------|---------|
| 数据缺失率 | 缺失记录数/总记录数 | <1% | 标记缺失，触发补充获取 |
| 字段缺失率 | 缺失字段数/总字段数 | <5% | 标记缺失，使用历史数据 |
| 时间序列缺失 | 检查日期连续性 | 无断点 | 补充缺失日期数据 |

#### 3.1.2 完整性检查实现

```python
def check_data_completeness(data, expected_fields, expected_date_range):
    """
    数据完整性检查
    
    参数:
    - data: 待检查数据
    - expected_fields: 期望字段列表
    - expected_date_range: 期望日期范围
    
    返回:
    - completeness_report: 完整性报告
    """
    # 检查字段完整性
    missing_fields = []
    for field in expected_fields:
        if field not in data.columns:
            missing_fields.append(field)
    
    field_completeness = 1 - len(missing_fields) / len(expected_fields)
    
    # 检查记录完整性
    expected_dates = pd.date_range(*expected_date_range, freq='D')
    actual_dates = pd.to_datetime(data['date'])
    
    missing_dates = expected_dates.difference(actual_dates)
    record_completeness = 1 - len(missing_dates) / len(expected_dates)
    
    # 检查数据缺失值
    missing_values_ratio = data.isnull().sum().sum() / data.size
    
    # 判断合格性
    is_complete = (
        field_completeness >= 0.95 and
        record_completeness >= 0.99 and
        missing_values_ratio < 0.01
    )
    
    return {
        'is_complete': is_complete,
        'field_completeness': field_completeness,
        'record_completeness': record_completeness,
        'missing_values_ratio': missing_values_ratio,
        'missing_fields': missing_fields,
        'missing_dates': missing_dates
    }
```

### 3.2 准确性检查

#### 3.2.1 检查规则

| 检查项 | 检查方法 | 合格标准 | 异常处理 |
|--------|---------|---------|---------|
| 数值范围 | 检查数值是否在合理范围 | 在合理范围内 | 标记异常，人工复核 |
| 逻辑一致性 | 检查相关指标逻辑一致性 | 符合逻辑关系 | 标记异常，修正数据 |
| 异常值检测 | 统计方法检测异常值 | 无异常值或异常值<0.5% | 标记异常，复核确认 |

#### 3.2.2 数值范围检查

| 数据字段 | 合理范围 | 检查方法 |
|---------|---------|---------|
| 股价 | 0.01-1000元 | 范围检查 |
| 涨跌幅 | -20%-+20% | 范围检查（考虑涨跌停） |
| 成交量 | >0 | 正数检查 |
| 市值 | 1000万-5000亿 | 范围检查 |
| PE | -100-500 | 范围检查（负值允许） |
| PB | 0-20 | 范围检查 |

```python
def check_data_accuracy(data, field_ranges):
    """
    数据准确性检查
    
    参数:
    - data: 待检查数据
    - field_ranges: 字段合理范围字典
    
    返回:
    - accuracy_report: 准确性报告
    """
    anomalies = []
    
    for field, (min_val, max_val) in field_ranges.items():
        if field in data.columns:
            # 检查超出范围的数据
            out_of_range = data[
                (data[field] < min_val) | 
                (data[field] > max_val)
            ]
            
            if len(out_of_range) > 0:
                anomalies.append({
                    'field': field,
                    'anomaly_count': len(out_of_range),
                    'anomaly_records': out_of_range.index.tolist()
                })
    
    # 检查逻辑一致性
    logical_anomalies = check_logical_consistency(data)
    
    # 综合判断
    anomaly_ratio = sum([a['anomaly_count'] for a in anomalies]) / len(data)
    is_accurate = anomaly_ratio < 0.005 and len(logical_anomalies) == 0
    
    return {
        'is_accurate': is_accurate,
        'anomaly_ratio': anomaly_ratio,
        'anomalies': anomalies,
        'logical_anomalies': logical_anomalies
    }

def check_logical_consistency(data):
    """
    逻辑一致性检查
    """
    anomalies = []
    
    # 检查：high >= max(open, close)
    if 'high' in data.columns and 'open' in data.columns and 'close' in data.columns:
        invalid_high = data[data['high'] < data[['open', 'close']].max(axis=1)]
        if len(invalid_high) > 0:
            anomalies.append({
                'type': 'high_price_logic',
                'count': len(invalid_high)
            })
    
    # 检查：low <= min(open, close)
    if 'low' in data.columns and 'open' in data.columns and 'close' in data.columns:
        invalid_low = data[data['low'] > data[['open', 'close']].min(axis=1)]
        if len(invalid_low) > 0:
            anomalies.append({
                'type': 'low_price_logic',
                'count': len(invalid_low)
            })
    
    return anomalies
```

### 3.3 及时性检查

#### 3.3.1 检查规则

| 检查项 | 检查方法 | 合格标准 | 异常处理 |
|--------|---------|---------|---------|
| 更新时间 | 检查数据更新时间戳 | T+0（当日收盘后更新） | 标记延迟，触发提醒 |
| 更新延迟 | 检查数据更新延迟时长 | <30分钟 | 延迟预警 |
| 数据版本 | 检查数据版本号 | 最新版本 | 使用旧版本需标记 |

#### 3.3.2 及时性检查实现

```python
def check_data_timeliness(data_timestamp, current_time, expected_update_time):
    """
    数据及时性检查
    
    参数:
    - data_timestamp: 数据时间戳
    - current_time: 当前时间
    - expected_update_time: 期望更新时间
    
    返回:
    - timeliness_report: 及时性报告
    """
    # 计算更新延迟
    if data_timestamp:
        update_delay = (current_time - data_timestamp).total_seconds() / 60  # 分钟
    else:
        update_delay = None
    
    # 判断是否及时
    is_timely = False
    if update_delay is not None:
        if update_delay <= 30:  # 30分钟内
            is_timely = True
        elif update_delay <= 60:  # 30-60分钟
            timeliness_level = "slight_delay"
        else:  # >60分钟
            timeliness_level = "serious_delay"
    
    # 检查数据版本
    is_latest_version = check_data_version()
    
    return {
        'is_timely': is_timely,
        'update_delay': update_delay,
        'timeliness_level': timeliness_level,
        'is_latest_version': is_latest_version
    }
```

### 3.4 一致性检查

#### 3.4.1 检查规则

| 检查项 | 检查方法 | 合格标准 | 异常处理 |
|--------|---------|---------|---------|
| 多源对比 | 对比多个数据源同一指标 | 差异<1% | 使用主数据源，标记差异 |
| 时序一致性 | 对比前后日数据变化 | 连续性合理 | 检查跳变，复核确认 |
| 指标计算一致性 | 对比自行计算与外部数据 | 差异<0.5% | 使用自计算，标记差异 |

#### 3.4.2 一致性检查实现

```python
def check_data_consistency(primary_data, secondary_data):
    """
    数据一致性检查
    
    参数:
    - primary_data: 主数据源数据
    - secondary_data: 补充数据源数据
    
    返回:
    - consistency_report: 一致性报告
    """
    discrepancies = []
    
    # 对比关键指标
    for field in ['close', 'volume', 'market_cap']:
        if field in primary_data.columns and field in secondary_data.columns:
            # 计算差异比例
            diff_ratio = abs(
                primary_data[field] - secondary_data[field]
            ) / primary_data[field]
            
            # 记录超过阈值的差异
            large_diff = diff_ratio[diff_ratio > 0.01]
            if len(large_diff) > 0:
                discrepancies.append({
                    'field': field,
                    'discrepancy_count': len(large_diff),
                    'max_discrepancy': large_diff.max()
                })
    
    # 时序一致性检查
    temporal_anomalies = check_temporal_consistency(primary_data)
    
    # 综合判断
    is_consistent = len(discrepancies) == 0 and len(temporal_anomalies) == 0
    
    return {
        'is_consistent': is_consistent,
        'discrepancies': discrepancies,
        'temporal_anomalies': temporal_anomalies
    }

def check_temporal_consistency(data):
    """
    时序一致性检查
    """
    anomalies = []
    
    # 检查价格跳变（日间涨跌幅>20%，非涨跌停）
    if 'close' in data.columns:
        pct_change = data['close'].pct_change()
        
        # 找出跳变（排除涨跌停）
        jumps = pct_change[
            (abs(pct_change) > 0.2) & 
            (abs(pct_change) < 0.099)  # 非涨跌停
        ]
        
        if len(jumps) > 0:
            anomalies.append({
                'type': 'price_jump',
                'count': len(jumps),
                'dates': jumps.index.tolist()
            })
    
    return anomalies
```

### 3.5 数据质量综合评估

```python
def evaluate_data_quality(data, config):
    """
    数据质量综合评估
    
    参数:
    - data: 待评估数据
    - config: 评估配置
    
    返回:
    - quality_report: 质量报告
    """
    # 完整性检查
    completeness = check_data_completeness(
        data, 
        config['expected_fields'],
        config['expected_date_range']
    )
    
    # 准确性检查
    accuracy = check_data_accuracy(data, config['field_ranges'])
    
    # 及时性检查
    timeliness = check_data_timeliness(
        data.get('timestamp'),
        datetime.now(),
        config['expected_update_time']
    )
    
    # 一致性检查（如有补充数据）
    consistency = None
    if config.get('secondary_data'):
        consistency = check_data_consistency(data, config['secondary_data'])
    
    # 综合评分
    quality_score = (
        completeness['field_completeness'] * 0.3 +
        completeness['record_completeness'] * 0.2 +
        (1 - accuracy['anomaly_ratio']) * 0.3 +
        (1 if timeliness['is_timely'] else 0) * 0.2
    )
    
    # 判断质量等级
    if quality_score >= 0.95:
        quality_level = "A级（优秀）"
    elif quality_score >= 0.90:
        quality_level = "B级（良好）"
    elif quality_score >= 0.80:
        quality_level = "C级（合格）"
    else:
        quality_level = "D级（不合格）"
    
    return {
        'quality_score': quality_score,
        'quality_level': quality_level,
        'completeness': completeness,
        'accuracy': accuracy,
        'timeliness': timeliness,
        'consistency': consistency,
        'is_acceptable': quality_score >= 0.80
    }
```

## 四、数据更新频率与流程

### 4.1 数据更新频率矩阵

| 数据类别 | 具体数据 | 更新频率 | 更新时间 | 更新触发 |
|---------|---------|---------|---------|---------|
| 行情日线 | OHLCV | 日频 | 每日15:30后 | 自动定时 |
| 情绪指标 | 涨跌停统计 | 日频 | 每日15:30后 | 自动定时 |
| 广度指标 | 站上20日线比例 | 日频 | 每日15:30后 | 自动定时 |
| 财务数据 | 季报数据 | 季频 | 季报发布后 | 手动触发 |
| 风格因子 | 因子收益 | 日频 | 每日15:30后 | 可选获取 |
| 交易记录 | 策略交易数据 | 日频 | 每日16:00后 | 策略执行后 |

### 4.2 数据更新流程

#### 4.2.1 日频更新流程

```
每日15:30-16:30数据更新流程：

15:30  ├─ 触发数据更新任务
       │  ├─ 检查数据源状态
       │  └─ 确认交易日状态
       │
15:35  ├─ 获取行情数据
       │  ├─ JoinQuant获取日线数据
       │  ├─ 数据质量检查
       │  └─ 存储到本地数据库
       │
15:40  ├─ 计算情绪指标
       │  ├─ 统计涨停股数量
       │  ├─ 统计连板分布
       │  ├─ 数据质量检查
       │  └─ 存储情绪数据
       │
15:45  ├─ 计算广度指标
       │  ├─ 计算沪深300站上20日线比例
       │  ├─ 计算中证1000站上20日线比例
       │  ├─ 数据质量检查
       │  └─ 存储广度数据
       │
15:50  ├─ 数据质量综合检查
       │  ├─ 完整性检查
       │  ├─ 准确性检查
       │  ├─ 及时性检查
       │  └─ 一致性检查
       │
16:00  ├─ 生成数据质量报告
       │  ├─ 记录质量问题
       │  ├─ 发出异常通知（如有）
       │  └─ 数据质量归档
       │
16:05  ├─ 触发验证任务
       │  └─ 启动日频验证流程
       │
16:10  └─ 完成数据更新
```

#### 4.2.2 季频更新流程

```
季报发布后财务数据更新流程：

触发  ├─ 接收季报发布通知
      │
1h后  ├─ 获取季报数据
      │  ├─ JoinQuant获取季报数据
      │  ├─ 数据质量检查
      │  └─ 存储财务数据
      │
2h后  ├─ 更新相关指标
      │  ├─ 更新ROE、PE、PB等
      │  ├─ 更新股票池筛选条件
      │  └─ 更新策略参数（如需要）
      │
3h后  ├─ 回测验证
      │  ├─ 使用新财务数据回测
      │  ├─ 对比新旧数据表现
      │  └─ 评估数据变更影响
      │
4h后  └─ 完成季报数据更新
```

### 4.3 数据更新自动化实现

```python
class DataUpdateScheduler:
    def __init__(self):
        self.update_tasks = {
            'daily': {
                'time': '15:30',
                'tasks': ['price', 'emotion', 'breadth']
            },
            'quarterly': {
                'trigger': 'quarter_report_release',
                'tasks': ['fundamentals']
            }
        }
    
    def run_daily_update(self):
        """
        执行日频数据更新
        """
        # 1. 检查是否交易日
        if not is_trading_day(datetime.now()):
            log_info("非交易日，跳过更新")
            return
        
        # 2. 依次执行更新任务
        for task in self.update_tasks['daily']['tasks']:
            try:
                if task == 'price':
                    self.update_price_data()
                elif task == 'emotion':
                    self.update_emotion_data()
                elif task == 'breadth':
                    self.update_breadth_data()
                
                log_success(f"{task}数据更新成功")
                
            except Exception as e:
                log_error(f"{task}数据更新失败: {e}")
                send_alert(f"{task}数据更新失败")
        
        # 3. 数据质量检查
        quality_report = self.check_data_quality()
        
        # 4. 发送质量报告
        if not quality_report['is_acceptable']:
            send_alert("数据质量不合格", quality_report)
        
        # 5. 触发验证
        trigger_validation()
    
    def update_price_data(self):
        """
        更新行情数据
        """
        current_date = get_current_date()
        
        # 获取数据
        price_data = fetch_from_joinquant('price', current_date)
        
        # 质量检查
        quality = evaluate_data_quality(price_data)
        
        if quality['is_acceptable']:
            # 存储
            save_to_db(price_data, 'daily_price')
            return True
        else:
            raise DataQualityError(quality)
    
    def update_emotion_data(self):
        """
        更新情绪数据
        """
        current_date = get_current_date()
        
        # 自行计算情绪指标
        all_stocks = get_all_securities()
        price_data = get_price_data(all_stocks, current_date)
        
        emotion_data = calculate_emotion_metrics(current_date, price_data)
        
        # 存储
        save_to_db(emotion_data, 'emotion_metrics')
        
        return True
    
    def update_breadth_data(self):
        """
        更新广度数据
        """
        current_date = get_current_date()
        
        # 计算沪深300广度
        hs300_stocks = get_index_stocks('000300.XSHG')
        hs300_breadth = calculate_breadth_metrics(
            current_date, 
            hs300_stocks, 
            get_price_data(hs300_stocks, current_date, 20)
        )
        
        # 计算中证1000广度
        zz1000_stocks = get_index_stocks('000852.XSHG')
        zz1000_breadth = calculate_breadth_metrics(
            current_date, 
            zz1000_stocks, 
            get_price_data(zz1000_stocks, current_date, 20)
        )
        
        # 存储
        save_to_db(hs300_breadth, 'breadth_hs300')
        save_to_db(zz1000_breadth, 'breadth_zz1000')
        
        return True
```

## 五、数据存储方案

### 5.1 本地存储方案

#### 5.1.1 SQLite数据库设计

**数据库结构**：

```sql
-- 行情数据表
CREATE TABLE daily_price (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_code TEXT NOT NULL,
    trade_date DATE NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    amount REAL,
    pct_change REAL,
    turnover_rate REAL,
    update_time TIMESTAMP,
    UNIQUE(stock_code, trade_date)
);

-- 情绪数据表
CREATE TABLE emotion_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_date DATE NOT NULL UNIQUE,
    limit_up_count INTEGER,
    limit_down_count INTEGER,
    limit_up_limit_down_ratio REAL,
    max_consecutive_board INTEGER,
    board_distribution TEXT,  -- JSON格式
    update_time TIMESTAMP
);

-- 广度数据表
CREATE TABLE breadth_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_date DATE NOT NOT NULL,
    index_code TEXT NOT NULL,
    above_ma_20_pct REAL,
    above_count INTEGER,
    total_count INTEGER,
    update_time TIMESTAMP,
    UNIQUE(trade_date, index_code)
);

-- 交易记录表
CREATE TABLE trade_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    signal_date DATE,
    signal_stock_code TEXT,
    signal_price REAL,
    execution_date DATE,
    execution_price REAL,
    execution_volume INTEGER,
    sell_date DATE,
    sell_price REAL,
    sell_reason TEXT,
    profit_loss_pct REAL,
    update_time TIMESTAMP
);

-- 数据质量检查记录表
CREATE TABLE data_quality_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    check_date DATE NOT NULL,
    data_type TEXT NOT NULL,
    quality_score REAL,
    quality_level TEXT,
    completeness_score REAL,
    accuracy_score REAL,
    timeliness_score REAL,
    issues TEXT,  -- JSON格式
    update_time TIMESTAMP
);
```

#### 5.1.2 SQLite存储实现

```python
import sqlite3
import json
from datetime import datetime

class SQLiteDataManager:
    def __init__(self, db_path='strategy_data.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
    
    def save_price_data(self, data):
        """
        存储行情数据
        """
        for row in data.itertuples():
            self.cursor.execute(
                """
                INSERT OR REPLACE INTO daily_price
                (stock_code, trade_date, open, high, low, close, 
                 volume, amount, pct_change, turnover_rate, update_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row.code,
                    row.date,
                    row.open,
                    row.high,
                    row.low,
                    row.close,
                    row.volume,
                    row.amount,
                    row.pct_change,
                    row.turnover_rate,
                    datetime.now()
                )
            )
        
        self.conn.commit()
    
    def save_emotion_data(self, data):
        """
        存储情绪数据
        """
        self.cursor.execute(
            """
            INSERT OR REPLACE INTO emotion_metrics
            (trade_date, limit_up_count, limit_down_count, 
             limit_up_limit_down_ratio, max_consecutive_board,
             board_distribution, update_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data['date'],
                data['limit_up_count'],
                data['limit_down_count'],
                data['limit_up_limit_down_ratio'],
                data['max_consecutive_board'],
                json.dumps(data['board_distribution']),
                datetime.now()
            )
        )
        
        self.conn.commit()
    
    def save_breadth_data(self, data, index_code):
        """
        存储广度数据
        """
        self.cursor.execute(
            """
            INSERT OR REPLACE INTO breadth_metrics
            (trade_date, index_code, above_ma_20_pct, 
             above_count, total_count, update_time)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data['date'],
                index_code,
                data['above_ma_20_pct'],
                data['above_count'],
                data['total_count'],
                datetime.now()
            )
        )
        
        self.conn.commit()
    
    def query_price_data(self, start_date, end_date, stock_codes=None):
        """
        查询行情数据
        """
        if stock_codes:
            query = """
                SELECT * FROM daily_price
                WHERE trade_date BETWEEN ? AND ?
                AND stock_code IN (?)
            """
            stocks_str = ','.join(stock_codes)
            self.cursor.execute(query, (start_date, end_date, stocks_str))
        else:
            query = """
                SELECT * FROM daily_price
                WHERE trade_date BETWEEN ? AND ?
            """
            self.cursor.execute(query, (start_date, end_date))
        
        return self.cursor.fetchall()
    
    def close(self):
        self.conn.close()
```

#### 5.1.3 CSV备份方案

```python
class CSVBackupManager:
    def __init__(self, backup_dir='data_backup'):
        self.backup_dir = backup_dir
    
    def backup_to_csv(self, data_type, date):
        """
        CSV格式备份
        """
        # 从SQLite读取数据
        sqlite_manager = SQLiteDataManager()
        
        if data_type == 'price':
            data = sqlite_manager.query_price_data(date, date)
            filename = f"{self.backup_dir}/price_{date}.csv"
            pd.DataFrame(data).to_csv(filename, index=False)
        
        elif data_type == 'emotion':
            # ...类似处理
        
        sqlite_manager.close()
        
        return filename
    
    def restore_from_csv(self, data_type, date):
        """
        从CSV恢复数据
        """
        filename = f"{self.backup_dir}/{data_type}_{date}.csv"
        
        if os.path.exists(filename):
            data = pd.read_csv(filename)
            
            # 存回SQLite
            sqlite_manager = SQLiteDataManager()
            
            if data_type == 'price':
                sqlite_manager.save_price_data(data)
            
            # ...类似处理
            
            sqlite_manager.close()
            
            return True
        else:
            return False
```

### 5.2 云端存储方案（可选）

#### 5.2.1 云数据库选择

| 云服务商 | 数据库类型 | 适用场景 | 成本 |
|---------|-----------|---------|------|
| 阿里云 | RDS MySQL | 生产环境，高可用 | 中 |
| AWS | RDS PostgreSQL | 国际部署，可扩展 | 中-高 |
|腾讯云 | TDSQL | 国内部署，性价比好 | 低-中 |

#### 5.2.2 云端存储架构

```
┌─────────────────────────────────────┐
│     云端数据存储架构                  │
├─────────────────────────────────────┤
│                                     │
│  本地缓存层                          │
│  ├─ SQLite（日频数据）               │
│  └─ CSV备份（历史数据）              │
│                                     │
│  云端主库                            │
│  ├─ MySQL/PostgreSQL                │
│  ├─ 全量历史数据                     │
│  └─ 生产环境访问                     │
│                                     │
│  云端备份                            │
│  ├─ 对象存储（OSS/S3）               │
│  ├─ 定期备份文件                     │
│  └─ 长期历史归档                     │
│                                     │
│  数据同步机制                        │
│  ├─ 日频数据：本地→云端              │
│  ├─ 定期备份：云端→对象存储          │
│  └─ 异地容灾：多区域复制             │
│                                     │
└─────────────────────────────────────┘
```

### 5.3 数据备份方案

#### 5.3.1 备份策略

| 备份类型 | 备份频率 | 备份内容 | 存储位置 | 恢复时间 |
|---------|---------|---------|---------|---------|
| 日频备份 | 每日 | 当日新增数据 | 本地CSV | <5分钟 |
| 周频备份 | 每周 | 近7日数据 | 本地+云端 | <30分钟 |
| 月频备份 | 每月 | 近月数据 | 云端对象存储 | <1小时 |
| 全量备份 | 每季度 | 全量历史数据 | 云端+异地 | <4小时 |

#### 5.3.2 备份自动化

```python
class BackupScheduler:
    def __init__(self):
        self.backup_tasks = {
            'daily': {
                'time': '17:00',
                'backup_type': 'daily_incremental'
            },
            'weekly': {
                'day': 'Sunday',
                'time': '18:00',
                'backup_type': 'weekly_full'
            },
            'monthly': {
                'day': 'last_day',
                'time': '19:00',
                'backup_type': 'monthly_archive'
            }
        }
    
    def run_daily_backup(self):
        """
        执行日频备份
        """
        current_date = get_current_date()
        
        # 1. 备份SQLite数据库
        sqlite_backup_file = backup_sqlite_database()
        
        # 2. 备份当日数据到CSV
        csv_backup_files = []
        for data_type in ['price', 'emotion', 'breadth']:
            filename = backup_to_csv(data_type, current_date)
            csv_backup_files.append(filename)
        
        # 3. 同步到云端（可选）
        if self.config['cloud_sync_enabled']:
            sync_to_cloud(sqlite_backup_file, csv_backup_files)
        
        # 4. 记录备份日志
        log_backup('daily', current_date, backup_files)
        
        return True
    
    def backup_sqlite_database(self):
        """
        备份SQLite数据库文件
        """
        source_db = 'strategy_data.db'
        backup_file = f"backup/db_backup_{datetime.now().strftime('%Y%m%d')}.db"
        
        shutil.copy2(source_db, backup_file)
        
        return backup_file
```

## 六、数据安全与权限管理

### 6.1 数据安全措施

| 安全措施 | 实施方法 | 目的 |
|---------|---------|------|
| 数据加密 | SQLite加密、传输加密 | 防止数据泄露 |
| 访问控制 | 用户权限管理、API密钥管理 | 防止未授权访问 |
| 数据脱敏 |敏感字段脱敏处理 | 保护敏感信息 |
| 审计日志 | 记录所有数据访问操作 | 可追溯、可审计 |

### 6.2 权限管理

```python
class DataAccessManager:
    def __init__(self):
        self.user_roles = {
            'admin': ['read', 'write', 'delete', 'backup'],
            'analyst': ['read', 'write'],
            'viewer': ['read']
        }
    
    def check_permission(self, user, action):
        """
        检查用户权限
        """
        user_role = get_user_role(user)
        
        if action in self.user_roles[user_role]:
            return True
        else:
            log_unauthorized_access(user, action)
            return False
    
    def log_access(self, user, action, data_type):
        """
        记录访问日志
        """
        log_entry = {
            'timestamp': datetime.now(),
            'user': user,
            'action': action,
            'data_type': data_type,
            'ip_address': get_client_ip()
        }
        
        save_access_log(log_entry)
```

## 七、数据管理工具集成

### 7.1 数据管理工具集

| 工具 | 功能 | 使用场景 |
|------|------|---------|
| 数据获取工具 | 自动获取各类数据 | 日频数据更新 |
| 数据检查工具 | 数据质量检查 | 每次数据更新后 |
| 数据存储工具 | 数据存储与管理 | 数据写入数据库 |
| 数据查询工具 | 数据查询与提取 | 验证、回测、分析 |
| 数据备份工具 | 数据备份与恢复 | 定期备份、灾备恢复 |
| 数据可视化工具 | 数据可视化展示 | 监控仪表盘 |

### 7.2 数据管理API接口

```python
class DataManagementAPI:
    """
    数据管理统一API接口
    """
    
    def get_data(self, data_type, start_date, end_date, **kwargs):
        """
        统一数据获取接口
        
        参数:
        - data_type: 数据类型（price/emotion/breadth/fundamentals）
        - start_date: 开始日期
        - end_date: 结束日期
        - kwargs: 其他参数
        
        返回:
        - data: 数据DataFrame
        """
        # 权限检查
        if not self.check_permission(kwargs.get('user'), 'read'):
            raise PermissionError("无权限访问数据")
        
        # 数据获取
        if data_type == 'price':
            data = self.query_price_data(start_date, end_date, kwargs.get('stock_codes'))
        elif data_type == 'emotion':
            data = self.query_emotion_data(start_date, end_date)
        elif data_type == 'breadth':
            data = self.query_breadth_data(start_date, end_date, kwargs.get('index_code'))
        
        # 记录访问日志
        self.log_access(kwargs.get('user'), 'read', data_type)
        
        return data
    
    def update_data(self, data_type, date, **kwargs):
        """
        统一数据更新接口
        """
        # 权限检查
        if not self.check_permission(kwargs.get('user'), 'write'):
            raise PermissionError("无权限更新数据")
        
        # 数据更新
        if data_type == 'price':
            self.update_price_data(date)
        elif data_type == 'emotion':
            self.update_emotion_data(date)
        elif data_type == 'breadth':
            self.update_breadth_data(date)
        
        # 数据质量检查
        quality_report = self.check_data_quality(data_type)
        
        # 记录访问日志
        self.log_access(kwargs.get('user'), 'write', data_type)
        
        return quality_report
```

## 八、数据管理方案总结

### 8.1 方案特点

1. **数据全面**：涵盖行情、财务、情绪、广度等多维度数据
2. **来源可靠**：主数据源JoinQuant，补充数据源多样化
3. **质量可控**：完整性、准确性、及时性、一致性四维检查
4. **更新自动**：日频自动更新，季频触发更新，流程标准化
5. **存储安全**：本地SQLite+云端备份，双重保障
6. **权限清晰**：分级权限管理，访问可追溯

### 8.2 实施建议

**优先级排序**：
1. P0：建立本地SQLite数据库，实现日频数据更新
2. P1：实现数据质量检查机制，确保数据可靠性
3. P2：实现数据备份方案，防止数据丢失
4. P3：考虑云端存储，实现异地容灾（可选）

**渐进式实施**：
- Week 1：搭建SQLite数据库，实现行情数据存储与查询
- Week 2：实现情绪、广度数据计算与存储
- Week 3：实现数据质量检查机制
- Week 4：实现数据备份方案
- Week 5+：考虑云端存储与高级功能

该数据管理方案能够有效支撑OOS验证框架，确保数据质量可靠、更新及时、存储安全，为策略验证提供坚实基础。
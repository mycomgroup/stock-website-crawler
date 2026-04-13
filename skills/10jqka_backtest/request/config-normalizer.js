/**
 * 转换通用的策略配置，映射到 10jqka 公式引擎格式
 */
export function normalizeConfig(rawConfig) {
    const config = { ...rawConfig };
    const mapped = {};
    
    // 中英文混搭同义词映射
    const fieldMap = {
        'query': 'query',
        'formula': 'query',
        'conditions': 'query',
        
        'startDate': 'start_date',
        'start_date': 'start_date',
        
        'endDate': 'end_date',
        'end_date': 'end_date',
        
        'daysForSaleStrategy': 'period',
        'period': 'period',
        
        'stockHoldCount': 'stock_hold',
        'maxPositions': 'stock_hold',
        
        'dayBuyStockNum': 'day_buy_stock_num',
        'dailyBuyCount': 'day_buy_stock_num',
        
        'upperIncome': 'upper_income',
        'takeProfit': 'upper_income',
        
        'lowerIncome': 'lower_income',
        'stopLoss': 'lower_income',
        
        'fallIncome': 'fall_income',
        'trailingStopLoss': 'fall_income',
        
        'capital': 'capital',
        'initialCapital': 'capital',
        
        'engine': 'engine'
    };

    // 默认回测基准处理
    for (const [key, value] of Object.entries(config)) {
        if (fieldMap[key]) {
             mapped[fieldMap[key]] = value;
        } else {
             mapped[key] = value;
        }
    }
    
    // 如果是数组条件说明，自动转成问财需要的自然语言拼接（逗号分隔）
    if (Array.isArray(mapped.query)) {
        mapped.query = mapped.query.join('，');
    }
    
    // 若不存在，默认给予引擎要求的一些缺省值，防止接口500
    mapped.capital = mapped.capital || '10000000';
    mapped.engine = mapped.engine || 'undefined';
    
    return mapped;
}

"""
修复DuckDB中缺失的2月-3月数据
只下载缺失日期的数据
"""
import duckdb
import akshare as ak
from datetime import datetime, timedelta
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DUCKDB_PATH = "/Users/yuping/Downloads/git/timesfm-cn-forecast-clean/data/market.duckdb"

def get_missing_dates(conn):
    """找出2月9日到3月9日之间缺失数据的日期"""
    logger.info("查找缺失数据的日期...")
    
    # 获取这个时间段内所有有数据的日期
    result = conn.execute('''
        SELECT DISTINCT date
        FROM daily_data 
        WHERE date >= '2026-02-09' AND date <= '2026-03-09'
        ORDER BY date
    ''').fetchall()
    
    existing_dates = set(str(row[0]) for row in result)
    logger.info(f"现有日期: {sorted(existing_dates)}")
    
    # 生成完整的日期范围（工作日）
    start = datetime(2026, 2, 9)
    end = datetime(2026, 3, 9)
    all_dates = []
    current = start
    while current <= end:
        # 跳过周末
        if current.weekday() < 5:  # 0-4是周一到周五
            all_dates.append(current.strftime('%Y-%m-%d'))
        current += timedelta(days=1)
    
    logger.info(f"应有工作日: {all_dates}")
    
    # 找出缺失的日期
    missing_dates = [d for d in all_dates if d not in existing_dates]
    logger.info(f"缺失日期: {missing_dates}")
    
    return missing_dates


def download_data_for_date_range(conn, start_date, end_date, symbols):
    """为指定日期范围下载所有股票的数据（批量下载更快）"""
    logger.info(f"\n批量下载 {start_date} 到 {end_date} 的数据...")
    
    success_count = 0
    failed_count = 0
    no_data_count = 0
    
    for i, (symbol, name) in enumerate(symbols, 1):
        if i % 500 == 0:
            logger.info(f"  进度: {i}/{len(symbols)}, 成功={success_count}, 无数据={no_data_count}, 失败={failed_count}")
        
        try:
            # 批量下载这个时间段的数据
            df = ak.stock_zh_a_daily(
                symbol=symbol,
                start_date=start_date.replace('-', ''),
                end_date=end_date.replace('-', ''),
                adjust='qfq'
            )
            
            if df.empty:
                no_data_count += 1
                continue
            
            # 插入数据
            for _, row in df.iterrows():
                try:
                    conn.execute('''
                        INSERT INTO daily_data 
                        (date, open, high, low, close, volume, amount, outstanding_share, turnover, symbol, name, adjust)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', [
                        row['date'],
                        float(row.get('open', 0)),
                        float(row.get('high', 0)),
                        float(row.get('low', 0)),
                        float(row.get('close', 0)),
                        float(row.get('volume', 0)),
                        float(row.get('amount', 0)),
                        float(row.get('outstanding_share', 0)),
                        float(row.get('turnover', 0)),
                        symbol,
                        name,
                        'qfq'
                    ])
                    success_count += 1
                except Exception as e:
                    # 可能是重复数据，跳过
                    pass
            
            # 避免请求过快
            time.sleep(0.2)
            
        except Exception as e:
            failed_count += 1
            if failed_count <= 5:  # 只显示前5个错误
                logger.error(f"  {symbol} 失败: {e}")
    
    logger.info(f"批量下载完成: 成功={success_count}, 无数据={no_data_count}, 失败={failed_count}")
    return success_count


def main():
    logger.info("="*60)
    logger.info("修复DuckDB中缺失的2月-3月数据")
    logger.info("="*60)
    
    conn = duckdb.connect(DUCKDB_PATH)
    
    try:
        # 1. 找出缺失的日期
        missing_dates = get_missing_dates(conn)
        
        if not missing_dates:
            logger.info("\n没有发现缺失的日期")
            return
        
        logger.info(f"\n发现 {len(missing_dates)} 个缺失日期")
        
        # 2. 获取所有股票列表
        logger.info("\n获取股票列表...")
        symbols = conn.execute('''
            SELECT DISTINCT symbol, name 
            FROM daily_data 
            WHERE symbol LIKE 'sh%' OR symbol LIKE 'sz%'
            ORDER BY symbol
        ''').fetchall()
        
        logger.info(f"需要更新 {len(symbols)} 只股票")
        
        # 3. 批量下载所有缺失日期的数据（一次请求下载整个时间段）
        if missing_dates:
            start_date = min(missing_dates)
            end_date = max(missing_dates)
            total_success = download_data_for_date_range(conn, start_date, end_date, symbols)
        else:
            total_success = 0
        
        logger.info(f"\n修复完成! 总共新增 {total_success} 条记录")
        
        # 4. 验证修复结果
        logger.info("\n验证修复结果...")
        result = conn.execute('''
            SELECT 
                date,
                COUNT(*) as total,
                COUNT(CASE WHEN close > 0 THEN 1 END) as positive_count
            FROM daily_data 
            WHERE date >= '2026-02-09' AND date <= '2026-03-09'
            GROUP BY date
            ORDER BY date
        ''').fetchall()
        
        for row in result:
            logger.info(f"  {row[0]}: {row[1]}只股票, {row[2]}只价格>0")
        
    except Exception as e:
        logger.error(f"修复失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()


if __name__ == "__main__":
    main()

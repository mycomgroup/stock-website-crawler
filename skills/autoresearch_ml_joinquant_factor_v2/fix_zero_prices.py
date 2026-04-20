"""
修复DuckDB中价格为0的数据
删除价格全为0的记录，然后重新下载正确的数据
"""
import duckdb
import akshare as ak
from datetime import datetime, timedelta
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DUCKDB_PATH = "/Users/yuping/Downloads/git/timesfm-cn-forecast-clean/data/market.duckdb"

def find_zero_price_dates(conn):
    """找出价格全为0或大部分为0的日期"""
    logger.info("查找价格异常的日期...")
    
    result = conn.execute('''
        SELECT 
            date,
            COUNT(*) as total,
            COUNT(CASE WHEN close = 0 THEN 1 END) as zero_count,
            COUNT(CASE WHEN close > 0 THEN 1 END) as positive_count
        FROM daily_data 
        WHERE date >= '2026-02-01' AND date < '2026-04-01'
        GROUP BY date
        HAVING zero_count > positive_count  -- 0值数量超过正常值
        ORDER BY date
    ''').fetchall()
    
    problem_dates = []
    for row in result:
        date, total, zero_count, positive_count = row
        zero_ratio = zero_count / total * 100
        logger.info(f"  {date}: {zero_count}/{total} ({zero_ratio:.1f}%) 价格为0")
        problem_dates.append(str(date))
    
    return problem_dates


def delete_zero_price_data(conn, dates):
    """删除指定日期的价格为0的数据"""
    logger.info(f"\n删除 {len(dates)} 个日期的0值数据...")
    
    total_deleted = 0
    for date in dates:
        result = conn.execute(
            "DELETE FROM daily_data WHERE date = ? AND close = 0",
            [date]
        )
        deleted = result.fetchone()[0] if result else 0
        total_deleted += deleted
        logger.info(f"  {date}: 删除 {deleted} 条记录")
    
    logger.info(f"总共删除 {total_deleted} 条记录")
    return total_deleted


def redownload_data_for_dates(conn, dates):
    """重新下载指定日期的数据"""
    logger.info(f"\n重新下载 {len(dates)} 个日期的数据...")
    
    # 获取所有股票列表
    symbols = conn.execute('''
        SELECT DISTINCT symbol, name 
        FROM daily_data 
        WHERE symbol LIKE 'sh%' OR symbol LIKE 'sz%'
        ORDER BY symbol
    ''').fetchall()
    
    logger.info(f"需要更新 {len(symbols)} 只股票")
    
    success_count = 0
    failed_count = 0
    
    for i, (symbol, name) in enumerate(symbols, 1):
        if i % 100 == 0:
            logger.info(f"进度: {i}/{len(symbols)}")
        
        try:
            # 找出这个股票在问题日期范围内缺失的数据
            min_date = min(dates)
            max_date = max(dates)
            
            # 下载这个时间段的数据
            df = ak.stock_zh_a_daily(
                symbol=symbol,
                start_date=min_date.replace('-', ''),
                end_date=max_date.replace('-', ''),
                adjust='qfq'
            )
            
            if df.empty:
                continue
            
            # 只保留问题日期的数据
            df = df[df['date'].isin(dates)]
            
            if df.empty:
                continue
            
            # 插入数据
            for _, row in df.iterrows():
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
            
            # 避免请求过快
            time.sleep(0.5)
            
        except Exception as e:
            failed_count += 1
            if failed_count <= 10:  # 只显示前10个错误
                logger.error(f"  {symbol} 失败: {e}")
    
    logger.info(f"重新下载完成: 成功 {success_count}, 失败 {failed_count}")
    return success_count


def main():
    logger.info("="*60)
    logger.info("修复DuckDB中价格为0的数据")
    logger.info("="*60)
    
    conn = duckdb.connect(DUCKDB_PATH)
    
    try:
        # 1. 找出问题日期
        problem_dates = find_zero_price_dates(conn)
        
        if not problem_dates:
            logger.info("\n没有发现价格异常的日期")
            return
        
        logger.info(f"\n发现 {len(problem_dates)} 个问题日期")
        
        # 2. 删除0值数据
        deleted = delete_zero_price_data(conn, problem_dates)
        
        # 3. 重新下载数据
        if deleted > 0:
            logger.info("\n注意: 重新下载数据需要较长时间，建议使用原始的duckdb_update.py脚本")
            logger.info("运行命令:")
            logger.info("  cd /Users/yuping/Downloads/git/timesfm-cn-forecast-clean/code")
            logger.info("  python3 duckdb_update.py")
        
        logger.info("\n修复完成!")
        
    except Exception as e:
        logger.error(f"修复失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()


if __name__ == "__main__":
    main()

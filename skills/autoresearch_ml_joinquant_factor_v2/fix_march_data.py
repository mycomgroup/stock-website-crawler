"""
修复3月3-9日的数据
"""
import duckdb
import akshare as ak
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DUCKDB_PATH = "/Users/yuping/Downloads/git/timesfm-cn-forecast-clean/data/market.duckdb"

def main():
    logger.info('='*60)
    logger.info('修复3月3-9日的数据')
    logger.info('='*60)
    
    conn = duckdb.connect(DUCKDB_PATH)
    
    try:
        # 删除3月3-9日的旧数据
        logger.info('\n删除3月3-9日的旧数据...')
        conn.execute("DELETE FROM daily_data WHERE date >= '2026-03-03' AND date <= '2026-03-09'")
        
        # 获取股票列表
        logger.info('获取股票列表...')
        symbols = conn.execute('''
            SELECT DISTINCT symbol, name 
            FROM daily_data 
            WHERE symbol LIKE 'sh%' OR symbol LIKE 'sz%'
            ORDER BY symbol
        ''').fetchall()
        
        logger.info(f'需要更新 {len(symbols)} 只股票\n')
        
        # 批量下载3月3-9日的数据
        logger.info('批量下载3月3-9日的数据...')
        success_count = 0
        failed_count = 0
        no_data_count = 0
        
        for i, (symbol, name) in enumerate(symbols, 1):
            if i % 500 == 0:
                logger.info(f'  进度: {i}/{len(symbols)}, 成功={success_count}, 无数据={no_data_count}, 失败={failed_count}')
            
            try:
                df = ak.stock_zh_a_daily(
                    symbol=symbol,
                    start_date='20260303',
                    end_date='20260309',
                    adjust='qfq'
                )
                
                if df.empty:
                    no_data_count += 1
                    continue
                
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
                    except:
                        pass
                
                time.sleep(0.2)
                
            except Exception as e:
                failed_count += 1
                if failed_count <= 5:
                    logger.error(f'  {symbol} 失败: {e}')
        
        logger.info(f'\n下载完成: 成功={success_count}, 无数据={no_data_count}, 失败={failed_count}')
        
        # 验证
        logger.info('\n验证结果:')
        result = conn.execute('''
            SELECT 
                date,
                COUNT(*) as total,
                COUNT(CASE WHEN close > 0 THEN 1 END) as positive
            FROM daily_data 
            WHERE date >= '2026-03-03' AND date <= '2026-03-09'
            GROUP BY date
            ORDER BY date
        ''').fetchall()
        
        for row in result:
            logger.info(f'  {row[0]}: {row[1]}只股票, {row[2]}只价格>0')
        
        logger.info('\n完成!')
        
    except Exception as e:
        logger.error(f'修复失败: {e}')
        import traceback
        traceback.print_exc()
    finally:
        conn.close()


if __name__ == "__main__":
    main()

"""
从 OSS 下载因子文件并自动拼接当天的股票价格
简化版：下载哪天的因子，就补充哪天的价格
"""
import os
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional
import pandas as pd
import duckdb
import time
from download_oss import bucket, LOGGER, download_file


# DuckDB 配置
DUCKDB_PATH = "/Users/yuping/Downloads/git/timesfm-cn-forecast-clean/data/market.duckdb"


def convert_stock_code(jq_code: str) -> str:
    """
    将聚宽股票代码转换为 DuckDB 格式
    
    聚宽格式: 600000.XSHG, 000001.XSHE, 300001.XSHE
    DuckDB格式: sh600000, sz000001, sz300001
    
    Args:
        jq_code: 聚宽格式的股票代码
        
    Returns:
        DuckDB 格式的股票代码
    """
    if not jq_code or '.' not in jq_code:
        return jq_code
    
    code, exchange = jq_code.split('.')
    
    if exchange == 'XSHG':  # 上海
        return f'sh{code}'
    elif exchange == 'XSHE':  # 深圳
        return f'sz{code}'
    elif exchange == 'XBSE':  # 北京
        return f'bj{code}'
    else:
        return jq_code


def get_price_for_date(date: str, duckdb_path: str = DUCKDB_PATH, max_retries: int = 5) -> Dict[str, Dict]:
    """
    从 DuckDB 获取指定日期的股票数据（包含价格、名称等多个字段）
    
    Args:
        date: 日期，格式 'YYYY-MM-DD'
        duckdb_path: DuckDB 数据库路径
        max_retries: 最大重试次数
        
    Returns:
        股票代码到数据字典的映射 {stock_code: {name, open, high, low, close, volume, amount, ...}}
    """
    # 尝试连接并查询
    for attempt in range(max_retries):
        conn = None
        try:
            # 使用只读模式连接
            conn = duckdb.connect(duckdb_path, read_only=True)
            
            # 查询所有可用字段
            query = f"""
                SELECT 
                    symbol, name, open, high, low, close, volume, amount,
                    outstanding_share, turnover, adjust
                FROM daily_data 
                WHERE date = '{date}'
            """
            
            result = conn.execute(query).fetchall()
            
            # 转换为嵌套字典
            price_dict = {}
            for row in result:
                stock_code = str(row[0])
                price_dict[stock_code] = {
                    'name': str(row[1]) if row[1] else None,
                    'open': float(row[2]) if row[2] is not None else None,
                    'high': float(row[3]) if row[3] is not None else None,
                    'low': float(row[4]) if row[4] is not None else None,
                    'close': float(row[5]) if row[5] is not None else None,
                    'volume': float(row[6]) if row[6] is not None else None,
                    'amount': float(row[7]) if row[7] is not None else None,
                    'outstanding_share': float(row[8]) if row[8] is not None else None,
                    'turnover': float(row[9]) if row[9] is not None else None,
                    'adjust': str(row[10]) if row[10] else None,
                }
            
            LOGGER.info(f"  获取数据: {len(price_dict)} 只股票")
            return price_dict
            
        except Exception as e:
            if attempt < max_retries - 1:
                LOGGER.warning(f"  获取数据失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                time.sleep(2)  # 等待2秒后重试
            else:
                LOGGER.error(f"  获取数据失败，已达最大重试次数: {e}")
                return {}
        finally:
            if conn:
                conn.close()
    
    return {}


def download_and_add_price(
    start_date: str,
    end_date: str,
    oss_base_prefix: str = "uploads/",
    local_base_dir: str = "./data/factors_with_price/",
    file_pattern: str = "factors_{date}_all.csv",
    duckdb_path: str = DUCKDB_PATH,
    price_column_name: str = "close_price"
) -> int:
    """
    下载因子文件并拼接当天的价格
    
    Args:
        start_date: 开始日期，格式 'YYYY-MM-DD' 或 'YYYYMMDD'
        end_date: 结束日期，格式 'YYYY-MM-DD' 或 'YYYYMMDD'
        oss_base_prefix: OSS 基础路径前缀
        local_base_dir: 本地保存基础目录
        file_pattern: 文件名模式
        duckdb_path: DuckDB 数据库路径
        price_column_name: 价格列名
        
    Returns:
        成功处理的文件数量
    """
    # 解析日期
    start_dt = datetime.strptime(start_date.replace('-', ''), '%Y%m%d')
    end_dt = datetime.strptime(end_date.replace('-', ''), '%Y%m%d')
    
    LOGGER.info(f"\n{'='*60}")
    LOGGER.info(f"开始下载因子并拼接价格")
    LOGGER.info(f"日期范围: {start_dt.date()} 到 {end_dt.date()}")
    LOGGER.info(f"{'='*60}\n")
    
    success_count = 0
    failed_count = 0
    current_dt = start_dt
    
    # 创建临时目录
    temp_dir = Path(local_base_dir) / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        while current_dt <= end_dt:
            year = current_dt.strftime('%Y')
            date_str = current_dt.strftime('%Y%m%d')
            date_dash = current_dt.strftime('%Y-%m-%d')
            
            # 构建路径
            filename = file_pattern.format(date=date_str)
            oss_path = f"{oss_base_prefix}{year}/{filename}"
            temp_path = temp_dir / year / filename
            final_path = Path(local_base_dir) / year / filename
            
            LOGGER.info(f"[{date_dash}] {filename}")
            
            # 1. 下载因子文件
            if download_file(oss_path, str(temp_path)):
                try:
                    # 2. 读取因子文件
                    df = pd.read_csv(temp_path)
                    stock_col = df.columns[0]  # 第一列是股票代码
                    LOGGER.info(f"  因子数据: {len(df)} 行 × {len(df.columns)} 列")
                    
                    # 3. 获取当天的价格数据
                    price_dict = get_price_for_date(date_dash, duckdb_path)
                    
                    # 4. 拼接所有字段
                    if price_dict:
                        # 转换股票代码格式后匹配所有字段
                        df['stock_name'] = df[stock_col].apply(lambda x: price_dict.get(convert_stock_code(x), {}).get('name'))
                        df['open'] = df[stock_col].apply(lambda x: price_dict.get(convert_stock_code(x), {}).get('open'))
                        df['high'] = df[stock_col].apply(lambda x: price_dict.get(convert_stock_code(x), {}).get('high'))
                        df['low'] = df[stock_col].apply(lambda x: price_dict.get(convert_stock_code(x), {}).get('low'))
                        df['close'] = df[stock_col].apply(lambda x: price_dict.get(convert_stock_code(x), {}).get('close'))
                        df['volume'] = df[stock_col].apply(lambda x: price_dict.get(convert_stock_code(x), {}).get('volume'))
                        df['amount'] = df[stock_col].apply(lambda x: price_dict.get(convert_stock_code(x), {}).get('amount'))
                        df['outstanding_share'] = df[stock_col].apply(lambda x: price_dict.get(convert_stock_code(x), {}).get('outstanding_share'))
                        df['turnover'] = df[stock_col].apply(lambda x: price_dict.get(convert_stock_code(x), {}).get('turnover'))
                        df['adjust'] = df[stock_col].apply(lambda x: price_dict.get(convert_stock_code(x), {}).get('adjust'))
                        
                        # 统计匹配情况（使用 close 作为参考）
                        matched = df['close'].notna().sum()
                        total = len(df)
                        match_rate = matched / total * 100 if total > 0 else 0
                        LOGGER.info(f"  数据匹配: {matched}/{total} ({match_rate:.1f}%)")
                    else:
                        LOGGER.warning(f"  未获取到数据")
                        df['stock_name'] = None
                        df['open'] = None
                        df['high'] = None
                        df['low'] = None
                        df['close'] = None
                        df['volume'] = None
                        df['amount'] = None
                        df['outstanding_share'] = None
                        df['turnover'] = None
                        df['adjust'] = None
                    
                    # 5. 保存文件
                    final_path.parent.mkdir(parents=True, exist_ok=True)
                    df.to_csv(final_path, index=False)
                    LOGGER.info(f"  ✓ 已保存: {final_path.name}\n")
                    
                    # 删除临时文件
                    temp_path.unlink()
                    success_count += 1
                    
                except Exception as e:
                    LOGGER.error(f"  ✗ 处理失败: {e}\n")
                    failed_count += 1
            else:
                LOGGER.warning(f"  ✗ 下载失败\n")
                failed_count += 1
            
            # 移动到下一天
            current_dt += timedelta(days=1)
    
    finally:
        # 清理临时目录
        if temp_dir.exists():
            import shutil
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
    
    LOGGER.info(f"{'='*60}")
    LOGGER.info(f"处理完成: 成功 {success_count} 个, 失败 {failed_count} 个")
    LOGGER.info(f"保存位置: {local_base_dir}")
    LOGGER.info(f"{'='*60}\n")
    
    return success_count


def download_year_with_price(
    year: int,
    oss_base_prefix: str = "uploads/",
    local_base_dir: str = "./data/factors_with_price/",
    duckdb_path: str = DUCKDB_PATH
) -> int:
    """
    下载整年的因子文件并拼接价格
    
    Args:
        year: 年份
        oss_base_prefix: OSS 基础路径前缀
        local_base_dir: 本地保存基础目录
        duckdb_path: DuckDB 数据库路径
        
    Returns:
        成功处理的文件数量
    """
    return download_and_add_price(
        start_date=f"{year}-01-01",
        end_date=f"{year}-12-31",
        oss_base_prefix=oss_base_prefix,
        local_base_dir=local_base_dir,
        duckdb_path=duckdb_path
    )


def get_last_trading_day_of_week(start_date: str, duckdb_path: str = DUCKDB_PATH) -> Optional[str]:
    """
    获取自然周（周一到周日）的最后一个交易日
    
    Args:
        start_date: 周一的日期，格式 'YYYY-MM-DD'
        duckdb_path: DuckDB 数据库路径
        
    Returns:
        最后一个交易日的日期字符串，格式 'YYYY-MM-DD'，如果没有找到返回 None
    """
    from datetime import datetime, timedelta
    
    monday = datetime.strptime(start_date, '%Y-%m-%d')
    
    # 检查这一周的每一天（从周日往回找）
    for i in range(6, -1, -1):  # 6=周日, 5=周六, ..., 0=周一
        check_date = monday + timedelta(days=i)
        check_date_str = check_date.strftime('%Y-%m-%d')
        
        # 尝试获取这一天的价格数据
        prices = get_price_for_date(check_date_str, duckdb_path)
        if prices:  # 如果有价格数据，说明是交易日
            return check_date_str
    
    return None


def download_weekly_factors_with_return(
    start_date: str,
    end_date: str,
    oss_base_prefix: str = "uploads/",
    local_base_dir: str = "./data/weekly_factors/",
    file_pattern: str = "factors_{date}_all.csv",
    duckdb_path: str = DUCKDB_PATH
) -> int:
    """
    下载周级别因子数据并计算周收益率（pchg）
    
    每个自然周（周一到周日）：
    - 使用周一的因子数据
    - 计算本周最后一个交易日到下周最后一个交易日的收益率作为 pchg
    
    Args:
        start_date: 开始日期，格式 'YYYY-MM-DD' 或 'YYYYMMDD'
        end_date: 结束日期，格式 'YYYY-MM-DD' 或 'YYYYMMDD'
        oss_base_prefix: OSS 基础路径前缀
        local_base_dir: 本地保存基础目录
        file_pattern: 文件名模式
        duckdb_path: DuckDB 数据库路径
        
    Returns:
        成功处理的周数
    """
    from datetime import datetime, timedelta
    import pandas as pd
    
    # 解析日期
    start_dt = datetime.strptime(start_date.replace('-', ''), '%Y%m%d')
    end_dt = datetime.strptime(end_date.replace('-', ''), '%Y%m%d')
    
    # 找到第一个周一
    days_to_monday = (start_dt.weekday()) % 7
    if days_to_monday > 0:
        start_dt = start_dt + timedelta(days=(7 - days_to_monday))
    
    LOGGER.info(f"\n{'='*60}")
    LOGGER.info(f"下载周级别因子并计算周收益率")
    LOGGER.info(f"日期范围: {start_dt.date()} 到 {end_dt.date()}")
    LOGGER.info(f"{'='*60}\n")
    
    success_count = 0
    failed_count = 0
    current_monday = start_dt
    
    # 创建临时目录
    temp_dir = Path(local_base_dir) / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        while current_monday <= end_dt:
            # 下周一
            next_monday = current_monday + timedelta(days=7)
            
            monday_str = current_monday.strftime('%Y%m%d')
            monday_dash = current_monday.strftime('%Y-%m-%d')
            
            LOGGER.info(f"[{monday_dash}] 处理周数据")
            
            # 1. 下载周一的因子文件
            filename = file_pattern.format(date=monday_str)
            oss_path = f"{oss_base_prefix}{current_monday.year}/{filename}"
            temp_path = temp_dir / filename
            
            if download_file(oss_path, str(temp_path)):
                try:
                    # 2. 读取因子文件
                    df = pd.read_csv(temp_path)
                    stock_col = df.columns[0]  # 第一列是股票代码
                    LOGGER.info(f"  因子数据: {len(df)} 行 × {len(df.columns)} 列")
                    
                    # 3. 获取本周最后一个交易日
                    last_day_this_week = get_last_trading_day_of_week(monday_dash, duckdb_path)
                    if not last_day_this_week:
                        LOGGER.warning(f"  未找到本周的交易日\n")
                        failed_count += 1
                        temp_path.unlink()
                        current_monday = next_monday
                        continue
                    
                    LOGGER.info(f"  本周最后交易日: {last_day_this_week}")
                    
                    # 4. 获取下周最后一个交易日
                    next_monday_dash = next_monday.strftime('%Y-%m-%d')
                    last_day_next_week = get_last_trading_day_of_week(next_monday_dash, duckdb_path)
                    if not last_day_next_week:
                        LOGGER.warning(f"  未找到下周的交易日\n")
                        failed_count += 1
                        temp_path.unlink()
                        current_monday = next_monday
                        continue
                    
                    LOGGER.info(f"  下周最后交易日: {last_day_next_week}")
                    
                    # 5. 获取价格
                    price_this_week = get_price_for_date(last_day_this_week, duckdb_path)
                    price_next_week = get_price_for_date(last_day_next_week, duckdb_path)
                    
                    if price_this_week and price_next_week:
                        # 6. 计算周收益率 pchg = (下周收盘 / 本周收盘) - 1
                        # 转换股票代码格式后匹配价格
                        df['price_this_week'] = df[stock_col].apply(lambda x: price_this_week.get(convert_stock_code(x), {}).get('close'))
                        df['price_next_week'] = df[stock_col].apply(lambda x: price_next_week.get(convert_stock_code(x), {}).get('close'))
                        
                        # 计算 pchg，过滤掉价格为0或None的情况
                        def calc_pchg(row):
                            p1 = row['price_this_week']
                            p2 = row['price_next_week']
                            # 如果任一价格为None、0或负数，返回None
                            if p1 is None or p2 is None or p1 <= 0 or p2 <= 0:
                                return None
                            return (p2 / p1) - 1
                        
                        df['pchg'] = df.apply(calc_pchg, axis=1)
                        
                        # 添加其他字段（使用本周的数据）
                        df['stock_name'] = df[stock_col].apply(lambda x: price_this_week.get(convert_stock_code(x), {}).get('name'))
                        df['open'] = df[stock_col].apply(lambda x: price_this_week.get(convert_stock_code(x), {}).get('open'))
                        df['high'] = df[stock_col].apply(lambda x: price_this_week.get(convert_stock_code(x), {}).get('high'))
                        df['low'] = df[stock_col].apply(lambda x: price_this_week.get(convert_stock_code(x), {}).get('low'))
                        df['close'] = df[stock_col].apply(lambda x: price_this_week.get(convert_stock_code(x), {}).get('close'))
                        df['volume'] = df[stock_col].apply(lambda x: price_this_week.get(convert_stock_code(x), {}).get('volume'))
                        df['amount'] = df[stock_col].apply(lambda x: price_this_week.get(convert_stock_code(x), {}).get('amount'))
                        df['outstanding_share'] = df[stock_col].apply(lambda x: price_this_week.get(convert_stock_code(x), {}).get('outstanding_share'))
                        df['turnover'] = df[stock_col].apply(lambda x: price_this_week.get(convert_stock_code(x), {}).get('turnover'))
                        df['adjust'] = df[stock_col].apply(lambda x: price_this_week.get(convert_stock_code(x), {}).get('adjust'))
                        
                        # 删除中间列
                        df = df.drop(columns=['price_this_week', 'price_next_week'])
                        
                        # 添加 date 列（使用周一的日期）
                        df['date'] = monday_dash
                        
                        # 调整列顺序：stock_id, stock_name, date, pchg, open, high, low, close, volume, amount, outstanding_share, turnover, adjust, ...其他因子列
                        base_cols = [stock_col, 'stock_name', 'date', 'pchg', 'open', 'high', 'low', 'close', 
                                    'volume', 'amount', 'outstanding_share', 'turnover', 'adjust']
                        other_cols = [c for c in df.columns if c not in base_cols]
                        df = df[base_cols + other_cols]
                        
                        # 统计有效数据
                        valid_pchg = df['pchg'].notna().sum()
                        total = len(df)
                        valid_rate = valid_pchg / total * 100 if total > 0 else 0
                        
                        LOGGER.info(f"  周收益率: {valid_pchg}/{total} ({valid_rate:.1f}%)")
                        
                        # 7. 保存文件（文件名格式：factors_YYYYMMDD_all.csv）
                        output_filename = f"factors_{monday_str}_all.csv"
                        final_path = Path(local_base_dir) / output_filename
                        final_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        df.to_csv(final_path, index=False)
                        LOGGER.info(f"  ✓ 已保存: {output_filename}\n")
                        
                        success_count += 1
                    else:
                        LOGGER.warning(f"  未获取到价格数据\n")
                        failed_count += 1
                    
                    # 删除临时文件
                    temp_path.unlink()
                    
                except Exception as e:
                    LOGGER.error(f"  ✗ 处理失败: {e}\n")
                    import traceback
                    LOGGER.debug(traceback.format_exc())
                    failed_count += 1
            else:
                LOGGER.warning(f"  ✗ 下载失败\n")
                failed_count += 1
            
            # 移动到下一个周一
            current_monday = next_monday
    
    finally:
        # 清理临时目录
        if temp_dir.exists():
            import shutil
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
    
    LOGGER.info(f"{'='*60}")
    LOGGER.info(f"处理完成: 成功 {success_count} 周, 失败 {failed_count} 周")
    LOGGER.info(f"保存位置: {local_base_dir}")
    LOGGER.info(f"{'='*60}\n")
    
    return success_count


if __name__ == "__main__":
    import sys
    
    # 设置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("\n" + "=" * 60)
    print("OSS 因子下载 + 价格拼接工具")
    print("=" * 60)
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "year" and len(sys.argv) > 2:
            # 下载整年: python3 download_factors_with_price.py year 2024
            year = int(sys.argv[2])
            print(f"\n下载 {year} 年的数据...")
            count = download_year_with_price(year)
        elif sys.argv[1] == "weekly":
            # 下载周级别: python3 download_factors_with_price.py weekly 2024-01-01 2024-12-31
            start = sys.argv[2] if len(sys.argv) > 2 else "2024-01-01"
            end = sys.argv[3] if len(sys.argv) > 3 else "2024-12-31"
            print(f"\n下载周级别数据: {start} 到 {end}")
            count = download_weekly_factors_with_return(start, end)
        else:
            # 下载日期范围: python3 download_factors_with_price.py 2024-01-01 2024-01-31
            start = sys.argv[1]
            end = sys.argv[2] if len(sys.argv) > 2 else start
            print(f"\n下载 {start} 到 {end} 的数据...")
            count = download_and_add_price(start, end)
    else:
        # 默认示例：下载3天数据
        print("\n运行示例: 下载 2024-01-01 到 2024-01-03")
        print("(使用命令行参数可以指定其他日期)\n")
        count = download_and_add_price("2024-01-01", "2024-01-03")
    
    if count > 0:
        print(f"\n✓ 成功处理 {count} 个文件/周")
        print("\n查看结果:")
        print("  ls -lh data/factors_with_price/2024/")
        print("  ls -lh data/weekly_factors/2024/")
        print("\n使用方法:")
        print("  # 下载指定日期范围（每日）")
        print("  python3 download_factors_with_price.py 2024-01-01 2024-01-31")
        print("\n  # 下载整年（每日）")
        print("  python3 download_factors_with_price.py year 2024")
        print("\n  # 下载周级别数据（含周收益率 pchg）")
        print("  python3 download_factors_with_price.py weekly 2024-01-01 2024-12-31")
    else:
        print("\n✗ 处理失败")
        print("\n可能的原因:")
        print("  1. DuckDB 被其他程序锁定（请关闭 duckdb_update.py 等程序）")
        print("  2. OSS 文件不存在")
        print("  3. 网络连接问题")

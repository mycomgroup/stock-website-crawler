"""
create_offline_package.py
生成最小离线数据包

功能：
1. 基于验收策略集配置，计算数据需求
2. 预热所有必需的数据
3. 打包为单个压缩文件
4. 生成使用说明

使用方法：
    python create_offline_package.py --output-dir ./offline_packages --version v1.0
"""

import os
import sys
import json
import logging
import argparse
import tarfile
from datetime import datetime
from typing import List, Dict, Set
import time

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from tools.data.prewarm_data import (
    run_prewarm,
    print_summary,
    DEFAULT_SAMPLE_STOCKS,
    DEFAULT_SAMPLE_ETFS,
    DEFAULT_SAMPLE_INDEXES,
)


def load_validation_strategies(config_file: str) -> List[Dict]:
    """加载验收策略配置"""
    with open(config_file, 'r', encoding='utf-8') as f:
        strategies = json.load(f)
    return strategies


def extract_data_requirements(strategies: List[Dict]) -> Dict:
    """
    从验收策略配置中提取数据需求

    Returns:
        Dict: {
            'stocks': Set[str],
            'etfs': Set[str],
            'indexes': Set[str],
            'start_date': str,
            'end_date': str,
            'need_fundamentals': bool,
            'need_finance': bool,
        }
    """
    stocks = set()
    etfs = set()
    indexes = set()

    start_dates = []
    end_dates = []

    need_fundamentals = False
    need_finance = False
    need_index_weights = False
    need_index_stocks = False

    for strategy in strategies:
        # 提取时间范围
        time_range = strategy.get('time_range', {})
        start_dates.append(time_range.get('start', '2020-01-01'))
        end_dates.append(time_range.get('end', '2023-12-31'))

        # 提取股票池
        stock_pool = strategy.get('stock_pool', {})
        if stock_pool.get('type') == 'fixed':
            for symbol in stock_pool.get('symbols', []):
                # 转换为akshare格式
                if symbol.endswith('.XSHG'):
                    ak_symbol = 'sh' + symbol[:6]
                elif symbol.endswith('.XSHE'):
                    ak_symbol = 'sz' + symbol[:6]
                else:
                    ak_symbol = symbol
                stocks.add(ak_symbol)
        elif stock_pool.get('type') == 'dynamic':
            # 动态股票池，需要预热指数成分股
            source = stock_pool.get('source')
            if source == 'index_weights' or source == 'index_stocks':
                index = stock_pool.get('index')
                if isinstance(index, str):
                    indexes.add(index.zfill(6))
                elif isinstance(index, list):
                    for idx in index:
                        indexes.add(idx.zfill(6))
                need_index_weights = (source == 'index_weights')
                need_index_stocks = True

        # 提取ETF池
        etf_pool = strategy.get('etf_pool', {})
        if etf_pool.get('type') == 'fixed':
            for symbol in etf_pool.get('symbols', []):
                # ETF代码格式转换
                if symbol.endswith('.XSHG') or symbol.endswith('.XSHE'):
                    etf_symbol = symbol[:6]
                else:
                    etf_symbol = symbol
                etfs.add(etf_symbol)

        # 检查数据需求
        data_req = strategy.get('data_requirements', {})
        if 'fundamentals' in data_req:
            need_fundamentals = True
        if 'finance' in data_req:
            need_finance = True

    # 确定统一的时间范围（取最小和最大）
    min_start = min(start_dates)
    max_end = max(end_dates)

    # 如果股票池为空或太小，补充默认样本
    if len(stocks) < 10:
        logger.info(f"股票池较小（{len(stocks)}只），补充默认样本股票")
        for stock in DEFAULT_SAMPLE_STOCKS[:10]:
            if stock.endswith('.XSHG'):
                ak_symbol = 'sh' + stock[:6]
            elif stock.endswith('.XSHE'):
                ak_symbol = 'sz' + stock[:6]
            else:
                ak_symbol = stock
            stocks.add(ak_symbol)

    # 如果指数池为空，补充默认指数
    if len(indexes) == 0:
        logger.info("指数池为空，补充默认指数")
        indexes.update(['000300', '000905', '000016'])

    # 如果ETF池为空，补充默认ETF
    if len(etfs) < 3:
        logger.info(f"ETF池较小（{len(etfs)}只），补充默认样本ETF")
        etfs.update(DEFAULT_SAMPLE_ETFS)

    result = {
        'stocks': sorted(list(stocks)),
        'etfs': sorted(list(etfs)),
        'indexes': sorted(list(indexes)),
        'start_date': min_start,
        'end_date': max_end,
        'need_fundamentals': need_fundamentals,
        'need_finance': need_finance,
        'need_index_weights': need_index_weights,
        'need_index_stocks': need_index_stocks,
    }

    logger.info(f"数据需求统计:")
    logger.info(f"  股票: {len(result['stocks'])}只")
    logger.info(f"  ETF: {len(result['etfs'])}只")
    logger.info(f"  指数: {len(result['indexes'])}只")
    logger.info(f"  时间范围: {result['start_date']} ~ {result['end_date']}")
    logger.info(f"  需要基本面数据: {result['need_fundamentals']}")
    logger.info(f"  需要分红数据: {result['need_finance']}")
    logger.info(f"  需要指数权重: {result['need_index_weights']}")

    return result


def prewarm_data_for_validation(data_req: Dict) -> Dict:
    """
    预热验收策略集所需的所有数据
    """
    logger.info("=" * 80)
    logger.info("开始预热验收数据...")
    logger.info("=" * 80)

    # 转换股票代码格式（akshare -> jq格式，用于prewarm）
    jq_stocks = []
    for ak_symbol in data_req['stocks']:
        if ak_symbol.startswith('sh'):
            jq_stocks.append(ak_symbol[2:] + '.XSHG')
        elif ak_symbol.startswith('sz'):
            jq_stocks.append(ak_symbol[2:] + '.XSHE')
        else:
            jq_stocks.append(ak_symbol)

    summary = run_prewarm(
        stock_pool=jq_stocks,
        etf_pool=data_req['etfs'],
        index_pool=data_req['indexes'],
        start_date=data_req['start_date'],
        end_date=data_req['end_date'],
        adjust='qfq',
        skip_existing=True,
        force_update=False,
        include_meta=True,
        include_weights=data_req['need_index_weights'],
    )

    return summary


def create_offline_package(
    data_req: Dict,
    prewarm_summary: Dict,
    output_dir: str,
    version: str,
    strategies_config_file: str,
) -> str:
    """
    创建离线数据包

    Returns:
        str: 打包文件路径
    """
    logger.info("=" * 80)
    logger.info("开始创建离线数据包...")
    logger.info("=" * 80)

    os.makedirs(output_dir, exist_ok=True)

    # 创建临时打包目录
    package_name = f"jk2bt_offline_data_{version}"
    temp_dir = os.path.join(output_dir, package_name)
    os.makedirs(temp_dir, exist_ok=True)

    # 1. 复制数据文件
    data_dir = os.path.join(_project_root, 'data')
    cache_dir = os.path.join(_project_root, 'data', 'cache')

    # 复制DuckDB数据库
    db_file = os.path.join(data_dir, 'jk2bt.duckdb')
    if os.path.exists(db_file):
        import shutil
        shutil.copy2(db_file, os.path.join(temp_dir, 'jk2bt.duckdb'))
        logger.info(f"复制数据库文件: {db_file}")

    # 复制缓存目录
    if os.path.exists(cache_dir):
        import shutil
        shutil.copytree(cache_dir, os.path.join(temp_dir, 'cache'), dirs_exist_ok=True)
        logger.info(f"复制缓存目录: {cache_dir}")

    # 2. 复制验收策略配置
    shutil.copy2(strategies_config_file, os.path.join(temp_dir, 'validation_strategies.json'))

    # 3. 创建README
    readme_content = f"""# jk2bt 离线数据包 {version}

## 数据包信息

- **版本**: {version}
- **创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **数据范围**: {data_req['start_date']} ~ {data_req['end_date']}
- **覆盖股票**: {len(data_req['stocks'])}只
- **覆盖ETF**: {len(data_req['etfs'])}只
- **覆盖指数**: {len(data_req['indexes'])}只

## 包含文件

1. `jk2bt.duckdb` - DuckDB数据库（股票、ETF、指数日线数据）
2. `cache/meta_cache/` - 元数据缓存（交易日历、证券信息）
3. `cache/index_cache/` - 指数成分权重缓存
4. `validation_strategies.json` - 验收策略配置清单

## 数据预热结果

{json.dumps(prewarm_summary, indent=2, ensure_ascii=False)}

## 使用方法

### 1. 解压数据包

```bash
tar -xzf jk2bt_offline_data_{version}.tar.gz
cd jk2bt_offline_data_{version}
```

### 2. 复制到项目数据目录

```bash
# 将数据文件复制到项目的data目录
cp jk2bt.duckdb ../data/
cp -r cache ../data/
cp validation_strategies.json ../tools/validation/
```

### 3. 运行验收策略

```bash
cd ..
python tools/validation/run_validation_strategies.py --offline
```

### 4. 验证离线模式

```bash
pytest tests/validation/test_validation_strategies.py --offline
```

## 数据包用途

- ✅ 新用户安装验收（无需网络）
- ✅ CI/CD回归测试（稳定数据源）
- ✅ 策略开发调试（快速迭代）
- ✅ 离线环境部署

## 注意事项

1. 本数据包仅包含验收策略集所需数据，不包含全市场数据
2. 数据时间范围有限，如需更长历史请自行扩展
3. 数据更新频率建议：每季度更新一次
4. 数据来源：AkShare（免费开源金融数据库）

## 更新记录

- {version} ({datetime.now().strftime('%Y-%m-%d')}): 初始版本，包含7个验收策略数据

---
Generated by jk2bt tools/data/create_offline_package.py
"""

    readme_file = os.path.join(temp_dir, 'README.md')
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    logger.info(f"创建README: {readme_file}")

    # 4. 打包为tar.gz
    tar_file = os.path.join(output_dir, f"{package_name}.tar.gz")
    with tarfile.open(tar_file, 'w:gz') as tar:
        tar.add(temp_dir, arcname=package_name)

    logger.info(f"✅ 离线数据包已创建: {tar_file}")

    # 5. 清理临时目录
    import shutil
    shutil.rmtree(temp_dir)

    # 6. 计算文件大小
    file_size = os.path.getsize(tar_file)
    size_mb = file_size / (1024 * 1024)
    logger.info(f"文件大小: {size_mb:.2f} MB")

    return tar_file


def main():
    parser = argparse.ArgumentParser(description="生成离线数据包")
    parser.add_argument(
        "--config",
        default=os.path.join(_project_root, "tools/validation/validation_strategies.json"),
        help="验收策略配置文件路径",
    )
    parser.add_argument("--output-dir", default="./offline_packages", help="输出目录")
    parser.add_argument("--version", default="v1.0", help="数据包版本号")
    parser.add_argument("--skip-prewarm", action="store_true", help="跳过预热步骤（使用已有数据）")

    args = parser.parse_args()

    # 1. 加载验收策略配置
    logger.info("步骤1: 加载验收策略配置")
    strategies = load_validation_strategies(args.config)
    logger.info(f"加载了 {len(strategies)} 个验收策略")

    # 2. 提取数据需求
    logger.info("\n步骤2: 分析数据需求")
    data_req = extract_data_requirements(strategies)

    # 3. 预热数据
    if not args.skip_prewarm:
        logger.info("\n步骤3: 预热数据")
        prewarm_summary = prewarm_data_for_validation(data_req)
        print_summary(prewarm_summary)
    else:
        logger.info("\n步骤3: 跳过预热（使用已有数据）")
        prewarm_summary = {"skipped": True}

    # 4. 创建离线数据包
    logger.info("\n步骤4: 创建离线数据包")
    tar_file = create_offline_package(
        data_req,
        prewarm_summary,
        args.output_dir,
        args.version,
        args.config,
    )

    logger.info("\n" + "=" * 80)
    logger.info("✅ 完成！离线数据包已生成")
    logger.info(f"文件路径: {tar_file}")
    logger.info("=" * 80)

    return tar_file


if __name__ == "__main__":
    main()
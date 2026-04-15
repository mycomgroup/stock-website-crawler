#!/usr/bin/env python3
"""
一键计算 200 个 JoinQuant 因子（性能优化版）。

核心优化：
1) 子 agent 并行 + 自适应降载（失败 chunk 自动二分重试）
2) 因子分片（shard）运行，避免单次请求过大
3) 流式落盘（flush_every），避免全量堆内存
4) 日期级节流（sleep_sec），降低 JQ API 爆掉概率
"""

from __future__ import annotations

import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd


def _load_factor_pool() -> list[str]:
    """从现有因子分类定义中加载全量因子池。"""
    try:
        from skills.autoresearch_joinquant_factor.factor_categories import FACTOR_CATEGORIES
    except Exception:
        # 兼容直接在当前目录运行：python main.py
        import importlib.util
        import sys

        root = Path(__file__).resolve().parents[2]
        module_path = root / "skills" / "autoresearch_joinquant_factor" / "factor_categories.py"
        spec = importlib.util.spec_from_file_location("factor_categories", module_path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["factor_categories"] = mod
        assert spec and spec.loader
        spec.loader.exec_module(mod)
        FACTOR_CATEGORIES = mod.FACTOR_CATEGORIES

    factors = []
    for group in FACTOR_CATEGORIES.values():
        factors.extend(group)

    seen = set()
    dedup = []
    for f in factors:
        if f not in seen:
            dedup.append(f)
            seen.add(f)
    return dedup


def _chunked(items: list[str], chunk_size: int) -> list[list[str]]:
    return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]


def _to_period_dates(start_date: str, end_date: str, freq: str) -> list[str]:
    from jqdata import get_price

    period_map = {"daily": "D", "weekly": "W", "monthly": "M"}
    if freq not in period_map:
        raise ValueError(f"不支持的频率: {freq}")

    bench = get_price("000001.XSHE", start_date, end_date, "daily", fields=["close"])
    bench["date"] = bench.index
    rs = bench.resample(period_map[freq], how="last").dropna()
    return [d.strftime("%Y-%m-%d") for d in rs.index.to_pydatetime()]


def _get_pool_stocks(pool: str, date: str) -> list[str]:
    import datetime
    from jqdata import get_extras, get_index_stocks, get_security_info

    def filter_new(stocks: list[str], begin_date: str, n: int = 90) -> list[str]:
        begin_dt = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
        out = []
        for stock in stocks:
            if get_security_info(stock).start_date < (begin_dt - datetime.timedelta(days=n)).date():
                out.append(stock)
        return out

    if pool == "small":
        stocks = get_index_stocks("399101.XSHE", date)
        stocks = [s for s in stocks if not s.startswith(("68", "4", "8"))]
    elif pool == "HS300":
        stocks = get_index_stocks("000300.XSHG", date)
    elif pool == "ZZ500":
        stocks = get_index_stocks("399905.XSHE", date)
    elif pool == "all":
        stocks = get_index_stocks("000985.XSHG", date)
        stocks = [s for s in stocks if not s.startswith(("3", "68", "4", "8"))]
    else:
        raise ValueError(f"不支持的 pool: {pool}")

    st = get_extras("is_st", stocks, count=1, end_date=date)
    stocks = [s for s in stocks if not st[s][0]]
    return filter_new(stocks, date)


def _fetch_factor_chunk(stocks: list[str], date: str, factors_chunk: list[str]) -> pd.DataFrame:
    from jqfactor import get_factor_values

    vals = get_factor_values(securities=stocks, factors=factors_chunk, count=1, end_date=date)
    df = pd.DataFrame(index=stocks)
    for f in factors_chunk:
        df[f] = vals[f].iloc[0, :]
    return df


def _fetch_chunk_with_fallback(
    stocks: list[str],
    date: str,
    factors_chunk: list[str],
    max_retries: int,
) -> pd.DataFrame:
    """
    性能/稳定性关键：
    - 先按原 chunk 请求
    - 失败后重试；仍失败则二分 chunk 递归
    """
    retries = 0
    while True:
        try:
            return _fetch_factor_chunk(stocks, date, factors_chunk)
        except Exception as e:
            retries += 1
            if retries <= max_retries:
                time.sleep(0.2 * retries)
                continue

            if len(factors_chunk) == 1:
                print(f"[warn] date={date} factor={factors_chunk[0]} failed: {e}")
                return pd.DataFrame(index=stocks, columns=factors_chunk, dtype=float)

            mid = len(factors_chunk) // 2
            left = _fetch_chunk_with_fallback(stocks, date, factors_chunk[:mid], max_retries=max_retries)
            right = _fetch_chunk_with_fallback(stocks, date, factors_chunk[mid:], max_retries=max_retries)
            return pd.concat([left, right], axis=1)


def fetch_factors_for_date(
    date: str,
    pool: str,
    factors: list[str],
    workers: int,
    chunk_size: int,
    max_retries: int,
) -> pd.DataFrame:
    stocks = _get_pool_stocks(pool, date)
    if len(stocks) < 20:
        return pd.DataFrame()

    chunks = _chunked(factors, max(1, chunk_size))
    out_parts: list[pd.DataFrame] = []

    with ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        fut_map = {
            ex.submit(_fetch_chunk_with_fallback, stocks, date, chunk, max_retries): chunk
            for chunk in chunks
        }
        for fut in as_completed(fut_map):
            try:
                out_parts.append(fut.result())
            except Exception as e:
                chunk = fut_map[fut]
                print(f"[warn] date={date} chunk_failed={len(chunk)} err={e}")
                out_parts.append(pd.DataFrame(index=stocks, columns=chunk, dtype=float))

    if not out_parts:
        return pd.DataFrame()

    merged = pd.concat(out_parts, axis=1).reindex(columns=factors)
    merged["date"] = date
    merged.index.name = "stock"
    return merged


def _append_batch(batch_df: pd.DataFrame, output: Path, batch_id: int) -> Path:
    """流式落盘：csv 追加 / parquet 分片。"""
    output.parent.mkdir(parents=True, exist_ok=True)

    if output.suffix.lower() == ".csv":
        exists = output.exists()
        batch_df.to_csv(output, mode="a", header=not exists, index=False)
        return output

    # parquet 分片目录，避免内存中 concat 全量
    parts_dir = output.with_suffix(output.suffix + ".parts")
    parts_dir.mkdir(parents=True, exist_ok=True)
    part_path = parts_dir / f"part_{batch_id:05d}.parquet"
    batch_df.to_parquet(part_path, index=False)
    return parts_dir


def _apply_shard(factors: list[str], shard_index: int, shard_count: int) -> list[str]:
    if shard_count <= 1:
        return factors
    if not (0 <= shard_index < shard_count):
        raise ValueError("shard_index 必须在 [0, shard_count) 范围")
    return [f for i, f in enumerate(factors) if i % shard_count == shard_index]


def run_pipeline(
    start_date: str,
    end_date: str,
    pool: str,
    freq: str,
    n_factors: int,
    workers: int,
    chunk_size: int,
    max_retries: int,
    flush_every: int,
    sleep_sec: float,
    shard_index: int,
    shard_count: int,
    output: str,
) -> dict:
    all_factors = _load_factor_pool()
    if n_factors > len(all_factors):
        raise ValueError(f"请求因子数 {n_factors} 超过可用池 {len(all_factors)}")

    factors = _apply_shard(all_factors[:n_factors], shard_index=shard_index, shard_count=shard_count)
    dates = _to_period_dates(start_date, end_date, freq)

    output_path = Path(output)
    buffer: list[pd.DataFrame] = []
    written_target = None
    batch_id = 0

    total_rows = 0
    date_count = 0
    stock_set = set()
    nan_sum = 0.0
    nan_cnt = 0

    for i, dt in enumerate(dates, start=1):
        print(f"[run] {i}/{len(dates)} date={dt} factors={len(factors)} workers={workers} chunk={chunk_size}")
        one = fetch_factors_for_date(
            date=dt,
            pool=pool,
            factors=factors,
            workers=workers,
            chunk_size=chunk_size,
            max_retries=max_retries,
        )
        if one.empty:
            time.sleep(max(0.0, sleep_sec))
            continue

        df = one.reset_index()
        buffer.append(df)

        # 累积统计（不依赖全量 concat）
        total_rows += len(df)
        date_count += 1
        stock_set.update(df["stock"].unique().tolist())
        nan_sum += df[factors].isna().sum().sum()
        nan_cnt += len(df) * len(factors)

        if len(buffer) >= max(1, flush_every):
            batch = pd.concat(buffer, ignore_index=True)
            batch_id += 1
            written_target = _append_batch(batch, output_path, batch_id=batch_id)
            buffer = []

        time.sleep(max(0.0, sleep_sec))

    if buffer:
        batch = pd.concat(buffer, ignore_index=True)
        batch_id += 1
        written_target = _append_batch(batch, output_path, batch_id=batch_id)

    if date_count == 0:
        summary = {
            "success": False,
            "error": "no_data",
            "dates_total": len(dates),
            "dates_effective": 0,
            "factors": len(factors),
        }
        print(json.dumps(summary, ensure_ascii=False))
        return summary

    summary = {
        "success": True,
        "rows": int(total_rows),
        "dates_total": int(len(dates)),
        "dates_effective": int(date_count),
        "stocks": int(len(stock_set)),
        "factors": int(len(factors)),
        "output": str(written_target if written_target else output_path),
        "output_mode": "csv_append" if output_path.suffix.lower() == ".csv" else "parquet_parts",
        "batches": int(batch_id),
        "nan_ratio": float(nan_sum / max(1, nan_cnt)),
        "shard_index": int(shard_index),
        "shard_count": int(shard_count),
    }

    meta_path = output_path.with_suffix(output_path.suffix + ".meta.json")
    meta_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return summary


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="一键并行计算 JoinQuant 多因子（性能优化版）")
    p.add_argument("--start-date", required=True)
    p.add_argument("--end-date", required=True)
    p.add_argument("--pool", default="small", choices=["small", "HS300", "ZZ500", "all"])
    p.add_argument("--freq", default="weekly", choices=["daily", "weekly", "monthly"])
    p.add_argument("--n-factors", type=int, default=200)

    # 性能与稳定性参数
    p.add_argument("--workers", type=int, default=4, help="并发 worker 数（建议 2~6）")
    p.add_argument("--chunk-size", type=int, default=12, help="单次请求因子块大小（建议 8~20）")
    p.add_argument("--max-retries", type=int, default=2, help="chunk 失败重试次数")
    p.add_argument("--flush-every", type=int, default=8, help="累计多少日期后落盘")
    p.add_argument("--sleep-sec", type=float, default=0.15, help="日期间节流秒数")

    # 分片运行：200 因子可拆为多个 shard 分批跑
    p.add_argument("--shard-index", type=int, default=0)
    p.add_argument("--shard-count", type=int, default=1)

    p.add_argument("--output", default="./artifacts/jq_200_factors.parquet")
    return p


def main():
    args = build_parser().parse_args()
    run_pipeline(
        start_date=args.start_date,
        end_date=args.end_date,
        pool=args.pool,
        freq=args.freq,
        n_factors=args.n_factors,
        workers=args.workers,
        chunk_size=args.chunk_size,
        max_retries=args.max_retries,
        flush_every=args.flush_every,
        sleep_sec=args.sleep_sec,
        shard_index=args.shard_index,
        shard_count=args.shard_count,
        output=args.output,
    )


if __name__ == "__main__":
    main()

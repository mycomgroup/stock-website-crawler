"""离线验证脚本示例。

用法:
python -m entry_overlay.run_offline_validation \
  --bars data/minute_bars.csv --events data/events.csv --out result.csv
"""

from __future__ import annotations

import argparse

import pandas as pd

from entry_overlay.data_sources import PandasAdapter
from entry_overlay.engine import EntryMode
from entry_overlay.offline import grid_search_params


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bars", required=True, help="包含 code,time,open,high,low,close,volume 的CSV")
    ap.add_argument("--events", required=True, help="包含 code,signal_time[,must_buy] 的CSV")
    ap.add_argument("--mode", default="rank_filter", choices=["rank_filter", "timing_only"])
    ap.add_argument("--out", default="overlay_grid_result.csv")
    args = ap.parse_args()

    bars = pd.read_csv(args.bars)
    events = pd.read_csv(args.events)
    adapter = PandasAdapter(bars)
    res = grid_search_params(adapter, events, mode=EntryMode(args.mode))
    res.to_csv(args.out, index=False)
    print(f"saved: {args.out}")
    print(res.head(10).to_string(index=False))


if __name__ == "__main__":
    main()

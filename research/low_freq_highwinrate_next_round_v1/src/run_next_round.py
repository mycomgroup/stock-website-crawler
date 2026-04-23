from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

from common import Thresholds, ensure_dir
from task01_baseline_freeze import freeze_baseline_config, export_baseline
from task02_dynamic_router_v1 import route_dataframe
from task03_rsrs_filter import apply_rsrs_filter
from task04_rfscore_whitelist import build_rfscore_whitelist
from task05_etf_macro_mapping import build_account_mapping


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run low-freq high-winrate next-round pipeline")
    p.add_argument("--market-csv", required=True)
    p.add_argument("--factor-csv", required=True)
    p.add_argument("--prototype-csv", required=True)
    p.add_argument("--out-dir", required=True)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = ensure_dir(args.out_dir)

    thresholds = Thresholds()

    # Task 1
    baseline = freeze_baseline_config()
    export_baseline(baseline, out_dir / "task01_baseline_frozen.json")

    market_df = pd.read_csv(args.market_csv)

    # Task 2
    route_df = route_dataframe(market_df[["date", "breadth", "trend_off"]], thresholds)
    route_df.to_csv(out_dir / "task02_dynamic_router_v1.csv", index=False)

    # Task 3
    rsrs_input = market_df[["date", "signal", "rsrs", "breadth", "sentiment"]]
    rsrs_df = apply_rsrs_filter(rsrs_input, thresholds)
    rsrs_df.to_csv(out_dir / "task03_rsrs_filtered_signals.csv", index=False)

    # Task 4
    factor_df = pd.read_csv(args.factor_csv)
    wl, bl = build_rfscore_whitelist(factor_df)
    wl.to_csv(out_dir / "task04_rfscore_whitelist.csv", index=False)
    bl.to_csv(out_dir / "task04_rfscore_blacklist.csv", index=False)

    # Task 5
    proto_df = pd.read_csv(args.prototype_csv)
    mapping_df = build_account_mapping(proto_df)
    mapping_df.to_csv(out_dir / "task05_account_role_mapping.csv", index=False)

    print(f"Done. Outputs in: {Path(out_dir).resolve()}")


if __name__ == "__main__":
    main()

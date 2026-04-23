from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from project.pipeline import RF7Pipeline


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="RF7 formal pipeline runner")
    p.add_argument("--input", required=True, help="Input CSV with universe snapshot")
    p.add_argument("--selected-out", required=True, help="Output CSV for selected universe")
    p.add_argument("--allocation-out", required=True, help="Output CSV for target allocations")
    return p


def main() -> None:
    args = build_parser().parse_args()
    in_path = Path(args.input)
    selected_out = Path(args.selected_out)
    allocation_out = Path(args.allocation_out)

    df = pd.read_csv(in_path, parse_dates=["date"])
    pipeline = RF7Pipeline()
    selected, allocation = pipeline.run(df)

    selected.to_csv(selected_out, index=False)
    allocation.to_csv(allocation_out, index=False)


if __name__ == "__main__":
    main()

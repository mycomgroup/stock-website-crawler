#!/usr/bin/env python3
"""
迁移旧种子文件到 templates/ 目录。

用法：python upgrade_seeds.py --tree trees/A_value
"""

import argparse
import json
import shutil
from pathlib import Path

SKILL_ROOT = Path(__file__).parent


def main():
    parser = argparse.ArgumentParser(description="迁移旧种子文件到 templates/ 目录")
    parser.add_argument("--tree", required=True, help="树目录路径（如 trees/A_value）")
    parser.add_argument("--dry-run", action="store_true", help="只显示将要迁移的文件，不实际执行")
    args = parser.parse_args()

    tree_dir = Path(args.tree)
    if not tree_dir.is_absolute():
        tree_dir = SKILL_ROOT / tree_dir

    if not tree_dir.exists():
        print(f"错误：目录不存在：{tree_dir}")
        return

    templates_dir = tree_dir / "templates"

    json_files = sorted(tree_dir.glob("*.json"))
    seed_files = [f for f in json_files if f.name not in ("seed.json", "profile.json")]

    if not seed_files:
        print(f"没有需要迁移的种子文件：{tree_dir}")
        return

    print(f"\n=== 树目录：{tree_dir} ===")
    print(f"发现 {len(seed_files)} 个需要迁移的种子文件：")
    for f in seed_files:
        print(f"  {f.name}")

    if args.dry_run:
        print("\n[dry-run] 未实际执行迁移")
        return

    templates_dir.mkdir(exist_ok=True)
    migrated = 0

    for src in seed_files:
        dst = templates_dir / src.name
        if dst.exists():
            print(f"  跳过（已存在）：{dst.name}")
            continue
        shutil.move(str(src), str(dst))
        print(f"  已迁移：{src.name} -> templates/{src.name}")
        migrated += 1

    print(f"\n总计：{migrated} 个文件已迁移到 templates/")


if __name__ == "__main__":
    main()

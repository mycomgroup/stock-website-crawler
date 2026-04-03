"""
策略资产盘点与分层工具
对 txt 策略文件进行系统化盘点，输出按类型分层的可执行清单
"""

import os
import re
import json
import csv
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
from .scanner import StrategyScanner, ScanResult


@dataclass
class StrategyClassification:
    """策略分类结果"""

    file_path: str
    file_name: str
    strategy_type: List[str]
    is_real_strategy: bool
    is_executable: bool
    has_ml_dependency: bool
    has_file_dependency: bool
    time_frame: str
    market_type: str
    account_type: str
    scan_result: Optional[ScanResult] = None
    keywords: List[str] = None
    ml_libraries: List[str] = None
    file_dependencies: List[str] = None
    code_lines: int = 0

    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.ml_libraries is None:
            self.ml_libraries = []
        if self.file_dependencies is None:
            self.file_dependencies = []


class StrategyInventory:
    """策略盘点器"""

    _ML_LIBRARIES = {
        "talib",
        "sklearn",
        "xgboost",
        "lightgbm",
        "torch",
        "tensorflow",
        "keras",
        "catboost",
        "pytorch",
        "scipy",
        "numpy",
        "pandas",
        "statsmodels",
        "prophet",
        "pmdarima",
    }

    _FILE_DEPENDENCY_PATTERNS = [
        r"\.csv",
        r"\.xlsx",
        r"\.xls",
        r"\.pkl",
        r"\.pickle",
        r"\.h5",
        r"\.hdf5",
        r"open\s*\(",
        r"pd\.read_",
        r"read_csv",
        r"read_excel",
        r"load\(",
        r"joblib\.load",
        r"torch\.load",
        r"pickle\.load",
    ]

    _INTRADAY_KEYWORDS = [
        "分钟",
        "分钟线",
        "日内",
        "分钟级",
        "tick",
        "分时",
        "高频",
        "intraday",
        "minute",
        "min_bar",
        "m1",
        "m5",
        "m15",
        "m30",
        "日内交易",
        "盘中",
        "实时",
        "tick数据",
    ]

    _FUTURE_KEYWORDS = [
        "期货",
        "股指",
        "IC",
        "IF",
        "IH",
        "TS",
        "TF",
        "T",
        "主力合约",
        "期货合约",
        "保证金",
        "杠杆",
        "做空",
        "做空机制",
        "期指",
        "future",
        "futures",
        "期货策略",
        "商品期货",
        "金融期货",
        "收盘折溢价",
        "贴水",
        "升水",
    ]

    _ETF_KEYWORDS = [
        "ETF",
        "etf",
        "etf轮动",
        "指数基金",
        "指数etf",
        "场内基金",
        "宽基",
        "窄基",
        "行业etf",
        "跨境etf",
        "债券etf",
        "货币etf",
    ]

    _STOCK_KEYWORDS = [
        "股票",
        "选股",
        "因子",
        "市值",
        "动量",
        "反转",
        "红利",
        "股息",
        "价值",
        "成长",
        "质量",
        "小市值",
        "微盘",
        "北向",
        "涨停",
        "跌停",
        "连板",
        "首板",
        "龙虎榜",
        "融资融券",
    ]

    _MULTI_ACCOUNT_KEYWORDS = [
        "子账户",
        "多账户",
        "subportfolio",
        "sub_account",
        "分账户",
        "账户组",
        "组合管理",
        "资产配置",
        "fof",
        "FOF",
    ]

    _RESEARCH_KEYWORDS = [
        "研究",
        "说明",
        "笔记",
        "教程",
        "解析",
        "复盘",
        "回顾",
        "配套",
        "资料",
        "非策略",
        "文档",
        "readme",
        "学习",
        "笔记",
        "总结",
        "探讨",
        "分析",
    ]

    def __init__(self, strategy_dir: str):
        self.strategy_dir = strategy_dir
        self.scanner = StrategyScanner()
        self.classifications: List[StrategyClassification] = []

    def classify_strategy(self, file_path: str, content: str) -> StrategyClassification:
        """分类单个策略"""
        file_name = os.path.basename(file_path)
        scan_result = self.scanner.scan_file(file_path)

        strategy_types = []
        keywords = []
        ml_libraries = []
        file_dependencies = []

        content_lower = content.lower()
        code_lines = len(content.splitlines())

        for lib in self._ML_LIBRARIES:
            if lib in content_lower or f"import {lib}" in content_lower:
                ml_libraries.append(lib)

        for pattern in self._FILE_DEPENDENCY_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                matches = re.findall(pattern, content, re.IGNORECASE)
                file_dependencies.extend(matches[:3])

        for keyword in self._INTRADAY_KEYWORDS:
            if keyword in content:
                keywords.append(keyword)
        if any(kw in content for kw in self._INTRADAY_KEYWORDS[:5]):
            strategy_types.append("分钟级/日内策略")

        for keyword in self._FUTURE_KEYWORDS:
            if keyword in content:
                keywords.append(keyword)
        if any(kw in content for kw in self._FUTURE_KEYWORDS[:10]):
            strategy_types.append("期货/股指策略")

        etf_found = False
        for keyword in self._ETF_KEYWORDS:
            if keyword in content:
                keywords.append(keyword)
                etf_found = True
        if etf_found:
            strategy_types.append("ETF策略")

        stock_found = False
        for keyword in self._STOCK_KEYWORDS:
            if keyword in content:
                keywords.append(keyword)
                stock_found = True
        if (
            stock_found
            and "ETF策略" not in strategy_types
            and "期货/股指策略" not in strategy_types
        ):
            strategy_types.append("股票策略")

        for keyword in self._MULTI_ACCOUNT_KEYWORDS:
            if keyword in content:
                keywords.append(keyword)
        if any(kw in content for kw in self._MULTI_ACCOUNT_KEYWORDS):
            strategy_types.append("多账户/子账户策略")

        is_research = False
        for keyword in self._RESEARCH_KEYWORDS:
            if keyword in file_name:
                keywords.append(keyword)
                is_research = True
        if is_research or not scan_result.has_initialize:
            strategy_types.append("研究说明/非策略文档")

        if ml_libraries:
            strategy_types.append("依赖ML库策略")

        if file_dependencies:
            strategy_types.append("依赖文件资源策略")

        if not strategy_types:
            if scan_result.is_executable:
                strategy_types.append("股票策略")
            else:
                strategy_types.append("研究说明/非策略文档")

        time_frame = "日线"
        if "分钟级/日内策略" in strategy_types:
            time_frame = "分钟级"
        elif "tick" in content_lower:
            time_frame = "tick级"

        market_type = "股票"
        if "ETF策略" in strategy_types:
            market_type = "ETF"
        elif "期货/股指策略" in strategy_types:
            market_type = "期货/股指"

        account_type = "单账户"
        if "多账户/子账户策略" in strategy_types:
            account_type = "多账户"

        is_real_strategy = (
            "研究说明/非策略文档" not in strategy_types and scan_result.has_initialize
        )

        return StrategyClassification(
            file_path=file_path,
            file_name=file_name,
            strategy_type=list(set(strategy_types)),
            is_real_strategy=is_real_strategy,
            is_executable=scan_result.is_executable,
            has_ml_dependency=bool(ml_libraries),
            has_file_dependency=bool(file_dependencies),
            time_frame=time_frame,
            market_type=market_type,
            account_type=account_type,
            scan_result=scan_result,
            keywords=keywords[:20],
            ml_libraries=ml_libraries,
            file_dependencies=list(set(file_dependencies))[:10],
            code_lines=code_lines,
        )

    def scan_all_strategies(self) -> List[StrategyClassification]:
        """扫描所有策略"""
        import glob

        txt_files = glob.glob(os.path.join(self.strategy_dir, "*.txt"))
        print(f"扫描目录: {self.strategy_dir}")
        print(f"发现文件: {len(txt_files)} 个")

        self.classifications = []

        for i, file_path in enumerate(sorted(txt_files), 1):
            if i % 50 == 0:
                print(f"进度: {i}/{len(txt_files)}")

            encodings = ["utf-8", "gbk", "gb2312", "latin-1"]
            content = None
            for encoding in encodings:
                try:
                    with open(file_path, "r", encoding=encoding) as f:
                        content = f.read()
                    break
                except:
                    continue

            if content is None:
                continue

            classification = self.classify_strategy(file_path, content)
            self.classifications.append(classification)

        print(f"扫描完成: {len(self.classifications)} 个文件")
        return self.classifications

    def generate_report(self, output_dir: str) -> Tuple[str, str, str]:
        """生成报告"""
        os.makedirs(output_dir, exist_ok=True)

        md_file = os.path.join(output_dir, "task11_strategy_inventory_result.md")
        json_file = os.path.join(output_dir, "task11_strategy_inventory.json")
        csv_file = os.path.join(output_dir, "task11_strategy_inventory.csv")

        self._write_markdown_report(md_file)
        self._write_json_report(json_file)
        self._write_csv_report(csv_file)

        return md_file, json_file, csv_file

    def _write_markdown_report(self, md_file: str):
        """写入 Markdown 报告"""
        type_stats = defaultdict(list)
        for cls in self.classifications:
            for t in cls.strategy_type:
                type_stats[t].append(cls)

        total_files = len(self.classifications)
        real_strategies = [c for c in self.classifications if c.is_real_strategy]
        executable_strategies = [c for c in self.classifications if c.is_executable]

        ml_strategies = [c for c in self.classifications if c.has_ml_dependency]
        file_dep_strategies = [c for c in self.classifications if c.has_file_dependency]

        with open(md_file, "w", encoding="utf-8") as f:
            f.write("# Task 11 策略资产盘点与分层报告\n\n")
            f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**扫描目录**: `{self.strategy_dir}`\n\n")

            f.write("## 一、总体统计\n\n")
            f.write(f"- **总文件数**: {total_files}\n")
            f.write(f"- **真策略数**: {len(real_strategies)}\n")
            f.write(f"- **可执行策略数**: {len(executable_strategies)}\n")
            f.write(f"- **依赖 ML 库策略**: {len(ml_strategies)}\n")
            f.write(f"- **依赖文件资源策略**: {len(file_dep_strategies)}\n\n")

            f.write("## 二、按类型分层统计\n\n")
            f.write("| 类型 | 数量 | 占比 | 可执行 | 代表文件样本 |\n")
            f.write("|------|------|------|--------|-------------|\n")

            type_order = [
                "股票策略",
                "ETF策略",
                "期货/股指策略",
                "分钟级/日内策略",
                "多账户/子账户策略",
                "依赖ML库策略",
                "依赖文件资源策略",
                "研究说明/非策略文档",
            ]

            for t in type_order:
                if t in type_stats:
                    strategies = type_stats[t]
                    executable = [s for s in strategies if s.is_executable]
                    samples = [s.file_name for s in strategies[:3]]
                    f.write(
                        f"| {t} | {len(strategies)} | {len(strategies) / total_files * 100:.1f}% | {len(executable)} | {'; '.join(samples)} |\n"
                    )

            for t, strategies in sorted(type_stats.items()):
                if t not in type_order:
                    executable = [s for s in strategies if s.is_executable]
                    samples = [s.file_name for s in strategies[:3]]
                    f.write(
                        f"| {t} | {len(strategies)} | {len(strategies) / total_files * 100:.1f}% | {len(executable)} | {'; '.join(samples)} |\n"
                    )

            f.write("\n## 三、详细分类清单\n\n")

            for t in type_order:
                if t not in type_stats:
                    continue

                strategies = type_stats[t]
                f.write(
                    f"### 3.{type_order.index(t) + 1} {t} ({len(strategies)}个)\n\n"
                )

                executable = [s for s in strategies if s.is_executable]
                not_executable = [s for s in strategies if not s.is_executable]

                if executable:
                    f.write(f"**可执行策略** ({len(executable)}个):\n\n")
                    for s in executable[:20]:
                        ml_info = (
                            f" [ML: {', '.join(s.ml_libraries)}]"
                            if s.ml_libraries
                            else ""
                        )
                        file_info = (
                            f" [文件依赖: {len(s.file_dependencies)}]"
                            if s.file_dependencies
                            else ""
                        )
                        f.write(f"- `{s.file_name}`{ml_info}{file_info}\n")
                    if len(executable) > 20:
                        f.write(f"  - ... 还有 {len(executable) - 20} 个\n")

                if not_executable:
                    f.write(f"\n**待修复策略** ({len(not_executable)}个):\n\n")
                    for s in not_executable[:10]:
                        reason = (
                            s.scan_result.error_message if s.scan_result else "未知"
                        )
                        f.write(f"- `{s.file_name}` - {reason}\n")
                    if len(not_executable) > 10:
                        f.write(f"  - ... 还有 {len(not_executable) - 10} 个\n")

                f.write("\n")

            f.write("## 四、推进优先级清单\n\n")
            f.write("基于可执行性、复杂度、价值评估，建议按以下优先级推进：\n\n")

            f.write("### 优先级 1 - 高价值、低难度（建议首批打通）\n\n")
            priority1 = [
                s
                for s in type_stats.get("ETF策略", [])
                if s.is_executable
                and not s.has_ml_dependency
                and not s.has_file_dependency
            ]
            priority1 += [
                s
                for s in type_stats.get("股票策略", [])
                if s.is_executable
                and not s.has_ml_dependency
                and not s.has_file_dependency
            ][:30]
            for s in priority1[:15]:
                f.write(f"- `{s.file_name}` ({', '.join(s.strategy_type)})\n")
            f.write(f"\n**共 {len(priority1)} 个策略**\n\n")

            f.write("### 优先级 2 - 中等难度（需要额外依赖）\n\n")
            priority2 = [
                s
                for s in self.classifications
                if s.is_executable and (s.has_ml_dependency or s.has_file_dependency)
            ]
            for s in priority2[:15]:
                deps = []
                if s.ml_libraries:
                    deps.append(f"ML: {', '.join(s.ml_libraries)}")
                if s.file_dependencies:
                    deps.append(f"文件: {len(s.file_dependencies)}")
                f.write(f"- `{s.file_name}` ({'; '.join(deps)})\n")
            f.write(f"\n**共 {len(priority2)} 个策略**\n\n")

            f.write("### 优先级 3 - 待修复（需要调试）\n\n")
            priority3 = [
                s
                for s in self.classifications
                if s.is_real_strategy and not s.is_executable
            ]
            for s in priority3[:15]:
                reason = s.scan_result.error_message if s.scan_result else "未知"
                f.write(f"- `{s.file_name}` - {reason}\n")
            f.write(f"\n**共 {len(priority3)} 个策略**\n\n")

            f.write("### 优先级 4 - 研究文档（非策略）\n\n")
            priority4 = type_stats.get("研究说明/非策略文档", [])
            for s in priority4[:10]:
                f.write(f"- `{s.file_name}`\n")
            f.write(f"\n**共 {len(priority4)} 个文件**\n\n")

            f.write("## 五、ML库依赖统计\n\n")
            ml_lib_stats = defaultdict(int)
            for c in self.classifications:
                for lib in c.ml_libraries:
                    ml_lib_stats[lib] += 1

            f.write("| ML库 | 依赖策略数 |\n")
            f.write("|------|------------|\n")
            for lib, count in sorted(ml_lib_stats.items(), key=lambda x: -x[1]):
                f.write(f"| {lib} | {count} |\n")

            f.write("\n## 六、建议与下一步\n\n")
            f.write("1. **首批目标**: 先打通优先级1的策略，建立基础运行环境\n")
            f.write(
                "2. **环境准备**: 根据ML库统计，安装必要的Python库（talib, sklearn, xgboost等）\n"
            )
            f.write(
                "3. **文件依赖**: 处理依赖外部文件资源的策略，确保数据文件路径正确\n"
            )
            f.write("4. **逐类推进**: 按优先级顺序逐步验证和修复策略\n")
            f.write("5. **持续优化**: 对研究文档进行整理，提取有价值的策略思路\n")

    def _write_json_report(self, json_file: str):
        """写入 JSON 清单"""
        data = {
            "scan_time": datetime.now().isoformat(),
            "strategy_dir": self.strategy_dir,
            "total_files": len(self.classifications),
            "real_strategies": len(
                [c for c in self.classifications if c.is_real_strategy]
            ),
            "executable_strategies": len(
                [c for c in self.classifications if c.is_executable]
            ),
            "classifications": [],
        }

        for c in self.classifications:
            item = {
                "file_name": c.file_name,
                "file_path": c.file_path,
                "strategy_type": c.strategy_type,
                "is_real_strategy": c.is_real_strategy,
                "is_executable": c.is_executable,
                "has_ml_dependency": c.has_ml_dependency,
                "has_file_dependency": c.has_file_dependency,
                "time_frame": c.time_frame,
                "market_type": c.market_type,
                "account_type": c.account_type,
                "ml_libraries": c.ml_libraries,
                "code_lines": c.code_lines,
                "keywords": c.keywords[:10],
            }
            if c.scan_result:
                item["scan_status"] = c.scan_result.status.value
                item["scan_error"] = c.scan_result.error_message
            data["classifications"].append(item)

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _write_csv_report(self, csv_file: str):
        """写入 CSV 清单"""
        with open(csv_file, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "文件名",
                    "文件路径",
                    "策略类型",
                    "真策略",
                    "可执行",
                    "ML依赖",
                    "文件依赖",
                    "时间框架",
                    "市场类型",
                    "账户类型",
                    "ML库",
                    "代码行数",
                    "扫描状态",
                    "错误信息",
                ]
            )

            for c in self.classifications:
                row = [
                    c.file_name,
                    c.file_path,
                    "; ".join(c.strategy_type),
                    "是" if c.is_real_strategy else "否",
                    "是" if c.is_executable else "否",
                    "是" if c.has_ml_dependency else "否",
                    "是" if c.has_file_dependency else "否",
                    c.time_frame,
                    c.market_type,
                    c.account_type,
                    "; ".join(c.ml_libraries),
                    c.code_lines,
                    c.scan_result.status.value if c.scan_result else "",
                    c.scan_result.error_message if c.scan_result else "",
                ]
                writer.writerow(row)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="策略资产盘点与分层")
    parser.add_argument("--dir", default="jkcode/jkcode", help="策略目录")
    parser.add_argument("--output", default="docs/0330_result", help="输出目录")

    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    strategy_dir = os.path.join(base_dir, args.dir)
    output_dir = os.path.join(base_dir, args.output)

    inventory = StrategyInventory(strategy_dir)
    inventory.scan_all_strategies()

    md_file, json_file, csv_file = inventory.generate_report(output_dir)

    print(f"\n报告已生成:")
    print(f"  Markdown: {md_file}")
    print(f"  JSON: {json_file}")
    print(f"  CSV: {csv_file}")


if __name__ == "__main__":
    main()

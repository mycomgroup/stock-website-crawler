"""
策略资源依赖扫描脚本
扫描所有策略文件，识别 read_file/write_file/open 等资源依赖
"""

import os
import re
import ast
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent
JKCODE_DIR = PROJECT_ROOT / "jkcode" / "jkcode"
UTILITY_DIR = PROJECT_ROOT / "src"


class ResourceDependencyScanner:
    def __init__(self):
        self.dependencies: Dict[str, List[Dict]] = defaultdict(list)
        self.resource_patterns = {
            "read_file": r"read_file\s*\(\s*['\"]([^'\"]+)['\"]",
            "write_file": r"write_file\s*\(\s*['\"]([^'\"]+)['\"]",
            "pd_read_csv": r"pd\.read_csv\s*\(\s*['\"]([^'\"]+)['\"]",
            "pd_read_json": r"pd\.read_json\s*\(\s*['\"]([^'\"]+)['\"]",
            "pickle_load": r"pickle\.load\s*\(\s*open\s*\(\s*['\"]([^'\"]+)['\"]",
            "open_read": r"open\s*\(\s*['\"]([^'\"]+\.csv)['\"]",
            "open_json": r"open\s*\(\s*['\"]([^'\"]+\.json)['\"]",
            "open_pkl": r"open\s*\(\s*['\"]([^'\"]+\.pkl)['\"]",
            "open_h5": r"open\s*\(\s*['\"]([^'\"]+\.h5)['\"]",
            "open_pth": r"open\s*\(\s*['\"]([^'\"]+\.pth)['\"]",
            "relative_csv": r"['\"]([a-zA-Z0-9_/-]+\.csv)['\"]",
            "relative_json": r"['\"]([a-zA-Z0-9_/-]+\.json)['\"]",
            "relative_pkl": r"['\"]([a-zA-Z0-9_/-]+\.pkl)['\"]",
        }

    def scan_file(self, filepath: Path) -> Dict:
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            return {"error": str(e), "dependencies": []}

        found_deps = []
        lines = content.split("\n")

        for dep_type, pattern in self.resource_patterns.items():
            matches = re.finditer(pattern, content)
            for match in matches:
                resource_path = match.group(1)
                line_num = content[: match.start()].count("\n") + 1
                found_deps.append(
                    {
                        "type": dep_type,
                        "resource": resource_path,
                        "line": line_num,
                        "context": lines[line_num - 1][:100]
                        if line_num <= len(lines)
                        else "",
                    }
                )

        return {"file": str(filepath), "dependencies": found_deps}

    def scan_directory(self, directory: Path) -> Dict[str, List]:
        results = {}
        for py_file in directory.rglob("*.py"):
            scan_result = self.scan_file(py_file)
            if scan_result.get("dependencies"):
                relative_path = py_file.relative_to(PROJECT_ROOT)
                results[str(relative_path)] = scan_result["dependencies"]
        return results

    def scan_all(self) -> Dict:
        all_results = {}

        if JKCODE_DIR.exists():
            all_results["jkcode"] = self.scan_directory(JKCODE_DIR)

        if UTILITY_DIR.exists():
            all_results["utility"] = self.scan_directory(UTILITY_DIR)

        test_dir = PROJECT_ROOT / "tests"
        if test_dir.exists():
            all_results["tests"] = self.scan_directory(test_dir)

        scripts_dir = PROJECT_ROOT / "scripts"
        if scripts_dir.exists():
            all_results["scripts"] = self.scan_directory(scripts_dir)

        return all_results

    def categorize_dependencies(self, results: Dict) -> Dict:
        categorized = {
            "input_resources": defaultdict(list),
            "output_resources": defaultdict(list),
            "ambiguous": defaultdict(list),
            "file_specific": defaultdict(list),
        }

        input_extensions = [
            ".csv",
            ".json",
            ".pkl",
            ".h5",
            ".pth",
            ".pt",
            ".onnx",
            ".model",
            ".bin",
        ]
        input_keywords = ["train", "test", "model", "config", "param", "data", "base"]

        output_keywords = [
            "output",
            "result",
            "log",
            "trade",
            "signal",
            "nav",
            "record",
        ]

        for location, deps_dict in results.items():
            for filepath, deps in deps_dict.items():
                for dep in deps:
                    resource = dep["resource"]
                    ext = Path(resource).suffix.lower()

                    if ext in input_extensions:
                        if any(kw in resource.lower() for kw in output_keywords):
                            categorized["output_resources"][filepath].append(dep)
                        elif any(kw in resource.lower() for kw in input_keywords):
                            categorized["input_resources"][filepath].append(dep)
                        else:
                            categorized["ambiguous"][filepath].append(dep)
                    else:
                        categorized["file_specific"][filepath].append(dep)

        return categorized

    def generate_report(self, results: Dict, categorized: Dict) -> str:
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("策略资源依赖扫描报告")
        report_lines.append("=" * 80)
        report_lines.append("")

        total_deps = sum(
            len(deps) for loc_deps in results.values() for deps in loc_deps.values()
        )
        report_lines.append(f"扫描文件总数: {len(results)} 个区域")
        report_lines.append(f"资源依赖总数: {total_deps} 个")
        report_lines.append("")

        report_lines.append("=" * 80)
        report_lines.append("一、输入资源依赖 (需要提供)")
        report_lines.append("=" * 80)
        for filepath, deps in categorized["input_resources"].items():
            report_lines.append(f"\n{filepath}:")
            for dep in deps:
                report_lines.append(
                    f"  - [{dep['type']}] {dep['resource']} (行 {dep['line']})"
                )

        report_lines.append("")
        report_lines.append("=" * 80)
        report_lines.append("二、输出资源依赖 (策略产出)")
        report_lines.append("=" * 80)
        for filepath, deps in categorized["output_resources"].items():
            report_lines.append(f"\n{filepath}:")
            for dep in deps:
                report_lines.append(
                    f"  - [{dep['type']}] {dep['resource']} (行 {dep['line']})"
                )

        report_lines.append("")
        report_lines.append("=" * 80)
        report_lines.append("三、模糊资源依赖 (需人工确认)")
        report_lines.append("=" * 80)
        for filepath, deps in categorized["ambiguous"].items():
            report_lines.append(f"\n{filepath}:")
            for dep in deps:
                report_lines.append(
                    f"  - [{dep['type']}] {dep['resource']} (行 {dep['line']})"
                )

        report_lines.append("")
        report_lines.append("=" * 80)
        report_lines.append("四、按依赖类型统计")
        report_lines.append("=" * 80)
        type_counts = defaultdict(int)
        for loc_deps in results.values():
            for deps in loc_deps.values():
                for dep in deps:
                    type_counts[dep["type"]] += 1

        for dep_type, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            report_lines.append(f"  {dep_type}: {count} 次")

        return "\n".join(report_lines)


def main():
    scanner = ResourceDependencyScanner()
    print("正在扫描策略资源依赖...")
    results = scanner.scan_all()
    categorized = scanner.categorize_dependencies(results)
    report = scanner.generate_report(results, categorized)

    output_path = (
        PROJECT_ROOT / "docs" / "0330_result" / "resource_dependency_scan_report.txt"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(report)
    print(f"\n报告已保存到: {output_path}")

    return results, categorized


if __name__ == "__main__":
    main()

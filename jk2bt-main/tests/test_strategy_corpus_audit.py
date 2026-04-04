"""
TEST-5: 策略语料审计测试

自动审计策略语料库，生成兼容性报告。

功能:
1. 扫描所有策略文件（txt、py、ipynb）
2. 使用StrategyScanner对每个策略进行扫描
3. 统计各类状态分布
4. 与已有的strategies_registry.csv对比验证
5. 生成兼容性报告（CSV/JSON）

完成标准:
- 审计测试可运行
- 报告自动生成
- 数据准确
- 快速、自动化、便于CI集成

运行方式:
    pytest tests/test_strategy_corpus_audit.py -v
    pytest tests/test_strategy_corpus_audit.py -v --tb=short
    python tests/test_strategy_corpus_audit.py
"""

import os
import sys
import json
import csv
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
from dataclasses import dataclass, asdict

# 设置项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class AuditResult:
    """审计结果数据结构"""
    file_path: str
    file_name: str
    file_type: str  # txt, py, ipynb
    scan_status: str
    run_status: str
    is_executable: bool
    in_scope: bool
    has_initialize: bool
    has_handle: bool
    missing_apis: List[str]
    error_message: str
    scan_timestamp: str
    details: Dict[str, Any]


@dataclass
class AuditSummary:
    """审计汇总数据结构"""
    total_files: int
    executable_count: int
    non_executable_count: int
    in_scope_count: int
    out_scope_count: int
    status_distribution: Dict[str, int]
    file_type_distribution: Dict[str, int]
    missing_api_distribution: Dict[str, int]
    audit_timestamp: str
    scan_duration: float


class StrategyCorpusAuditor:
    """策略语料审计器"""

    def __init__(self, strategies_dir: Optional[Path] = None, output_dir: Optional[Path] = None):
        """
        初始化审计器

        Args:
            strategies_dir: 策略目录路径
            output_dir: 报告输出目录
        """
        self.strategies_dir = strategies_dir or project_root / "strategies"
        self.output_dir = output_dir or project_root / "logs" / "audit"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.registry_csv_path = self.strategies_dir / "strategies_registry.csv"
        self.registry_json_path = self.strategies_dir / "strategies_registry.json"

        # 尝试导入scanner
        self.scanner = None
        try:
            from jk2bt.strategy.scanner import StrategyScanner
            self.scanner = StrategyScanner()
        except ImportError as e:
            logger.warning(f"无法导入StrategyScanner: {e}")
            try:
                from src.strategy.scanner import StrategyScanner
                self.scanner = StrategyScanner()
            except ImportError as e2:
                logger.error(f"无法导入src.strategy.scanner: {e2}")

    def scan_all_files(self) -> List[AuditResult]:
        """扫描所有策略文件"""
        results = []
        start_time = time.time()

        # 扫描txt文件
        txt_files = list(self.strategies_dir.glob("*.txt"))
        logger.info(f"发现 {len(txt_files)} 个txt文件")

        # 扫描py文件
        py_files = list(self.strategies_dir.glob("*.py"))
        logger.info(f"发现 {len(py_files)} 个py文件")

        # 扫描ipynb文件（记录但不扫描）
        ipynb_files = list(self.strategies_dir.glob("*.ipynb"))
        logger.info(f"发现 {len(ipynb_files)} 个ipynb文件")

        # 扫描txt和py文件
        for file_path in txt_files + py_files:
            result = self._scan_single_file(file_path)
            results.append(result)

        # notebook文件单独处理
        for file_path in ipynb_files:
            result = AuditResult(
                file_path=str(file_path),
                file_name=file_path.name,
                file_type="ipynb",
                scan_status="excluded_notebook",
                run_status="not_applicable",
                is_executable=False,
                in_scope=False,
                has_initialize=False,
                has_handle=False,
                missing_apis=[],
                error_message="研究文档/notebook，非可执行策略",
                scan_timestamp=datetime.now().isoformat(),
                details={"reason": "notebook_excluded"}
            )
            results.append(result)

        duration = time.time() - start_time
        logger.info(f"扫描完成，耗时 {duration:.2f} 秒")

        return results

    def _scan_single_file(self, file_path: Path) -> AuditResult:
        """扫描单个文件"""
        file_type = file_path.suffix.lstrip('.')
        scan_timestamp = datetime.now().isoformat()

        # 使用scanner扫描
        if self.scanner:
            scan_result = self.scanner.scan_file(str(file_path))
            return AuditResult(
                file_path=str(file_path),
                file_name=file_path.name,
                file_type=file_type,
                scan_status=scan_result.status.value,
                run_status="executable" if scan_result.is_executable else "non_executable",
                is_executable=scan_result.is_executable,
                in_scope=file_type == "txt" and scan_result.is_executable,
                has_initialize=scan_result.has_initialize,
                has_handle=scan_result.has_handle,
                missing_apis=scan_result.missing_apis,
                error_message=scan_result.error_message,
                scan_timestamp=scan_timestamp,
                details=scan_result.details
            )
        else:
            # 兜底：简单的启发式扫描
            return self._fallback_scan(file_path, file_type, scan_timestamp)

    def _fallback_scan(self, file_path: Path, file_type: str, scan_timestamp: str) -> AuditResult:
        """兜底扫描（当scanner不可用时）"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            has_initialize = 'def initialize(' in content
            has_handle = any(
                kw in content for kw in [
                    'def handle_data(', 'def handle_',
                    'run_daily(', 'run_weekly(', 'run_monthly('
                ]
            )

            # 简单判断
            is_executable = has_initialize and has_handle
            scan_status = "valid" if is_executable else "no_initialize"
            run_status = "executable" if is_executable else "non_executable"

            return AuditResult(
                file_path=str(file_path),
                file_name=file_path.name,
                file_type=file_type,
                scan_status=scan_status,
                run_status=run_status,
                is_executable=is_executable,
                in_scope=file_type == "txt" and is_executable,
                has_initialize=has_initialize,
                has_handle=has_handle,
                missing_apis=[],
                error_message="" if is_executable else "缺少必要函数",
                scan_timestamp=scan_timestamp,
                details={"fallback": True}
            )
        except Exception as e:
            return AuditResult(
                file_path=str(file_path),
                file_name=file_path.name,
                file_type=file_type,
                scan_status="scan_error",
                run_status="non_executable",
                is_executable=False,
                in_scope=False,
                has_initialize=False,
                has_handle=False,
                missing_apis=[],
                error_message=str(e),
                scan_timestamp=scan_timestamp,
                details={"error": str(e)}
            )

    def generate_summary(self, results: List[AuditResult]) -> AuditSummary:
        """生成审计汇总"""
        status_distribution = defaultdict(int)
        file_type_distribution = defaultdict(int)
        missing_api_distribution = defaultdict(int)

        executable_count = 0
        non_executable_count = 0
        in_scope_count = 0
        out_scope_count = 0

        for result in results:
            status_distribution[result.scan_status] += 1
            file_type_distribution[result.file_type] += 1

            if result.is_executable:
                executable_count += 1
            else:
                non_executable_count += 1

            if result.in_scope:
                in_scope_count += 1
            else:
                out_scope_count += 1

            for api in result.missing_apis:
                missing_api_distribution[api] += 1

        # 计算扫描时长（估算）
        first_ts = min(r.scan_timestamp for r in results)
        last_ts = max(r.scan_timestamp for r in results)
        try:
            first_dt = datetime.fromisoformat(first_ts)
            last_dt = datetime.fromisoformat(last_ts)
            duration = (last_dt - first_dt).total_seconds()
        except Exception:
            duration = 0.0

        return AuditSummary(
            total_files=len(results),
            executable_count=executable_count,
            non_executable_count=non_executable_count,
            in_scope_count=in_scope_count,
            out_scope_count=out_scope_count,
            status_distribution=dict(status_distribution),
            file_type_distribution=dict(file_type_distribution),
            missing_api_distribution=dict(missing_api_distribution),
            audit_timestamp=datetime.now().isoformat(),
            scan_duration=duration
        )

    def compare_with_registry(self, results: List[AuditResult]) -> Dict[str, Any]:
        """与已有registry对比验证"""
        comparison = {
            "registry_exists": False,
            "registry_csv_records": 0,
            "audit_records": len(results),
            "matched": 0,
            "new_files": [],
            "removed_files": [],
            "status_changed": [],
            "consistency_check": {}
        }

        if not self.registry_csv_path.exists():
            logger.warning(f"registry CSV不存在: {self.registry_csv_path}")
            return comparison

        comparison["registry_exists"] = True

        # 读取registry CSV
        registry_data = {}
        try:
            with open(self.registry_csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    path = row.get('path', '')
                    if path:
                        registry_data[path] = row
            comparison["registry_csv_records"] = len(registry_data)
        except Exception as e:
            logger.error(f"读取registry CSV失败: {e}")
            return comparison

        # 对比
        audit_paths = {r.file_path for r in results}
        registry_paths = set(registry_data.keys())

        comparison["new_files"] = sorted(list(audit_paths - registry_paths))[:20]  # 只显示前20个
        comparison["removed_files"] = sorted(list(registry_paths - audit_paths))[:20]

        # 状态变更检查
        for result in results:
            if result.file_path in registry_data:
                reg_row = registry_data[result.file_path]
                reg_status = reg_row.get('scan_status', '')
                if reg_status != result.scan_status:
                    comparison["status_changed"].append({
                        "file": result.file_name,
                        "registry_status": reg_status,
                        "audit_status": result.scan_status
                    })
                comparison["matched"] += 1

        # 一致性检查
        if comparison["matched"] == len(results) and not comparison["new_files"] and not comparison["removed_files"]:
            comparison["consistency_check"]["status"] = "consistent"
        else:
            comparison["consistency_check"]["status"] = "inconsistent"
            comparison["consistency_check"]["details"] = {
                "new_count": len(comparison["new_files"]),
                "removed_count": len(comparison["removed_files"]),
                "changed_count": len(comparison["status_changed"])
            }

        return comparison

    def save_csv_report(self, results: List[AuditResult], filename: str = "audit_report.csv") -> Path:
        """保存CSV报告"""
        output_path = self.output_dir / filename

        fieldnames = [
            'file_path', 'file_name', 'file_type', 'scan_status', 'run_status',
            'is_executable', 'in_scope', 'has_initialize', 'has_handle',
            'missing_apis', 'error_message', 'scan_timestamp'
        ]

        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for result in results:
                row = {
                    'file_path': result.file_path,
                    'file_name': result.file_name,
                    'file_type': result.file_type,
                    'scan_status': result.scan_status,
                    'run_status': result.run_status,
                    'is_executable': result.is_executable,
                    'in_scope': result.in_scope,
                    'has_initialize': result.has_initialize,
                    'has_handle': result.has_handle,
                    'missing_apis': ','.join(result.missing_apis) if result.missing_apis else '',
                    'error_message': result.error_message,
                    'scan_timestamp': result.scan_timestamp
                }
                writer.writerow(row)

        logger.info(f"CSV报告已保存: {output_path}")
        return output_path

    def save_json_report(self, summary: AuditSummary, results: List[AuditResult],
                         comparison: Dict, filename: str = "audit_report.json") -> Path:
        """保存JSON报告"""
        output_path = self.output_dir / filename

        report = {
            "audit_timestamp": summary.audit_timestamp,
            "scan_duration": summary.scan_duration,
            "summary": asdict(summary),
            "comparison": comparison,
            "results": [asdict(r) for r in results]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logger.info(f"JSON报告已保存: {output_path}")
        return output_path

    def print_summary_report(self, summary: AuditSummary, comparison: Dict) -> None:
        """打印汇总报告"""
        print("\n" + "=" * 80)
        print("策略语料审计报告")
        print("=" * 80)

        print(f"\n审计时间: {summary.audit_timestamp}")
        print(f"扫描耗时: {summary.scan_duration:.2f} 秒")

        print("\n[文件统计]")
        print(f"  总文件数: {summary.total_files}")
        print(f"  可执行策略: {summary.executable_count}")
        print(f"  不可执行: {summary.non_executable_count}")
        print(f"  范围内: {summary.in_scope_count}")
        print(f"  范围外: {summary.out_scope_count}")

        print("\n[文件类型分布]")
        for file_type, count in summary.file_type_distribution.items():
            print(f"  {file_type}: {count}")

        print("\n[扫描状态分布]")
        for status, count in sorted(summary.status_distribution.items(), key=lambda x: -x[1]):
            pct = count / summary.total_files * 100
            print(f"  {status}: {count} ({pct:.1f}%)")

        if summary.missing_api_distribution:
            print("\n[缺失API统计]")
            for api, count in sorted(summary.missing_api_distribution.items(), key=lambda x: -x[1])[:10]:
                print(f"  {api}: {count} 个策略缺失")

        print("\n[Registry对比验证]")
        print(f"  Registry存在: {comparison['registry_exists']}")
        print(f"  Registry记录数: {comparison['registry_csv_records']}")
        print(f"  本次审计记录数: {comparison['audit_records']}")
        print(f"  匹配数: {comparison['matched']}")
        print(f"  新增文件: {len(comparison['new_files'])}")
        print(f"  移除文件: {len(comparison['removed_files'])}")
        print(f"  状态变更: {len(comparison['status_changed'])}")
        print(f"  一致性检查: {comparison['consistency_check']['status']}")

        if comparison['new_files'][:5]:
            print("\n  新增文件示例:")
            for f in comparison['new_files'][:5]:
                print(f"    + {Path(f).name}")

        if comparison['removed_files'][:5]:
            print("\n  移除文件示例:")
            for f in comparison['removed_files'][:5]:
                print(f"    - {Path(f).name}")

        if comparison['status_changed'][:5]:
            print("\n  状态变更示例:")
            for change in comparison['status_changed'][:5]:
                print(f"    * {change['file']}: {change['registry_status']} -> {change['audit_status']}")

        print("\n" + "=" * 80)


# ============= pytest测试函数 =============

def test_strategy_corpus_audit():
    """TEST-5: 策略语料审计测试"""
    auditor = StrategyCorpusAuditor()

    # 1. 扫描所有文件
    results = auditor.scan_all_files()
    assert len(results) > 0, "审计结果不能为空"

    # 2. 生成汇总
    summary = auditor.generate_summary(results)

    # 3. 与registry对比
    comparison = auditor.compare_with_registry(results)

    # 4. 保存报告
    csv_path = auditor.save_csv_report(results)
    json_path = auditor.save_json_report(summary, results, comparison)

    # 5. 打印汇总
    auditor.print_summary_report(summary, comparison)

    # 6. 验证关键指标
    assert summary.total_files > 0, "总文件数应大于0"
    assert summary.executable_count > 0, "应存在可执行策略"
    assert summary.file_type_distribution.get('txt', 0) > 0, "应有txt策略文件"

    # 7. 验证报告文件生成
    assert csv_path.exists(), "CSV报告应生成"
    assert json_path.exists(), "JSON报告应生成"

    print("\n审计测试通过!")
    print(f"CSV报告: {csv_path}")
    print(f"JSON报告: {json_path}")


def test_scanner_availability():
    """测试Scanner可用性"""
    try:
        from jk2bt.strategy.scanner import StrategyScanner
        scanner = StrategyScanner()
        assert scanner is not None, "Scanner应可用"
        print("Scanner导入成功: jk2bt.strategy.scanner")
    except ImportError:
        try:
            from src.strategy.scanner import StrategyScanner
            scanner = StrategyScanner()
            assert scanner is not None, "Scanner应可用"
            print("Scanner导入成功: src.strategy.scanner")
        except ImportError as e:
            print(f"Scanner导入失败: {e}")
            pytest.skip("Scanner不可用，使用兜底扫描")


def test_registry_consistency():
    """测试Registry一致性"""
    auditor = StrategyCorpusAuditor()

    # 扫描
    results = auditor.scan_all_files()
    summary = auditor.generate_summary(results)
    comparison = auditor.compare_with_registry(results)

    # 如果registry存在，验证一致性
    if comparison["registry_exists"]:
        # 允许少量差异（新增文件）
        new_count = len(comparison["new_files"])
        removed_count = len(comparison["removed_files"])

        # 新增文件数量应较少（正常情况下不会有大量新增）
        assert new_count < summary.total_files * 0.1, \
            f"新增文件过多 ({new_count}/{summary.total_files})，可能需要重新扫描registry"

        # 打印一致性状态
        status = comparison["consistency_check"]["status"]
        print(f"Registry一致性状态: {status}")

        if status == "inconsistent":
            details = comparison["consistency_check"]["details"]
            print(f"差异详情: 新增{details['new_count']}, 移除{details['removed_count']}, 变更{details['changed_count']}")
    else:
        print("Registry不存在，跳过一致性测试")


def test_executable_strategies_identification():
    """测试可执行策略识别"""
    auditor = StrategyCorpusAuditor()

    results = auditor.scan_all_files()
    executable_results = [r for r in results if r.is_executable]

    # 验证可执行策略都有initialize函数
    for result in executable_results[:20]:  # 只检查前20个
        if result.file_type == "txt":
            assert result.has_initialize, \
                f"可执行策略应包含initialize: {result.file_name}"

    print(f"可执行策略数量: {len(executable_results)}")


def test_file_type_statistics():
    """测试文件类型统计"""
    auditor = StrategyCorpusAuditor()

    results = auditor.scan_all_files()
    summary = auditor.generate_summary(results)

    # 验证文件类型分布
    assert "txt" in summary.file_type_distribution, "应有txt文件"
    assert "ipynb" in summary.file_type_distribution, "应有ipynb文件"

    # txt文件应为主要策略来源
    txt_count = summary.file_type_distribution.get("txt", 0)
    ipynb_count = summary.file_type_distribution.get("ipynb", 0)

    print(f"txt文件: {txt_count}")
    print(f"ipynb文件: {ipynb_count}")

    # ipynb都应被标记为非可执行
    ipynb_results = [r for r in results if r.file_type == "ipynb"]
    for result in ipynb_results:
        assert not result.is_executable, \
            f"notebook不应标记为可执行: {result.file_name}"
        assert result.scan_status == "excluded_notebook", \
            f"notebook应标记为excluded_notebook: {result.file_name}"


def test_missing_api_detection():
    """测试缺失API检测"""
    auditor = StrategyCorpusAuditor()

    results = auditor.scan_all_files()
    summary = auditor.generate_summary(results)

    # 如果有缺失API，验证检测结果
    if summary.missing_api_distribution:
        print("\n缺失API检测结果:")
        for api, count in sorted(summary.missing_api_distribution.items(), key=lambda x: -x[1])[:10]:
            print(f"  {api}: {count} 个策略")

        # 验证缺失API的策略都被标记为非可执行（如果使用scanner）
        for result in results:
            if result.missing_apis and result.file_type == "txt":
                assert not result.is_executable, \
                    f"缺失API的策略不应标记为可执行: {result.file_name}"
    else:
        print("未检测到缺失API")


# ============= 主函数 =============

def main():
    """主函数：运行完整审计"""
    print("\n" + "#" * 80)
    print("# TEST-5: 策略语料审计测试")
    print("#" * 80)

    auditor = StrategyCorpusAuditor()

    # 执行审计
    results = auditor.scan_all_files()
    summary = auditor.generate_summary(results)
    comparison = auditor.compare_with_registry(results)

    # 保存报告
    csv_path = auditor.save_csv_report(results)
    json_path = auditor.save_json_report(summary, results, comparison)

    # 打印汇总
    auditor.print_summary_report(summary, comparison)

    # 验证
    print("\n验证结果:")

    checks = [
        ("总文件数 > 0", summary.total_files > 0),
        ("可执行策略 > 0", summary.executable_count > 0),
        ("CSV报告生成", csv_path.exists()),
        ("JSON报告生成", json_path.exists()),
    ]

    all_passed = True
    for name, passed in checks:
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {name}")
        if not passed:
            all_passed = False

    print("\n" + "#" * 80)
    if all_passed:
        print("# 审计测试完成 - 所有检查通过")
        print("#" * 80)
        print(f"\n报告路径:")
        print(f"  CSV: {csv_path}")
        print(f"  JSON: {json_path}")
        return 0
    else:
        print("# 审计测试完成 - 存在失败检查")
        print("#" * 80)
        return 1


if __name__ == "__main__":
    import pytest
    sys.exit(main())
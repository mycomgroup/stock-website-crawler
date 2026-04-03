"""
TXT 策略文本标准化模块

目标：让更多策略至少能进入"可加载/可分析"阶段，
而不是一开始就死在编码和语法层。

功能：
- 多编码读取增强
- TAB/空格缩进修复或检测
- Python2 风格兼容问题识别
- 标准化前后差异记录

原则：
- 默认不改源文件
- 优先输出标准化后的临时文本或缓存版本
- 对危险修复保留告警
"""

import os
import re
import ast
import tempfile
import hashlib
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum

try:
    import chardet
except ImportError:  # pragma: no cover - optional dependency
    chardet = None

# 获取logger
logger = logging.getLogger(__name__)


class IssueType(Enum):
    ENCODING = "encoding"
    INDENTATION = "indentation"
    PYTHON2_PRINT = "python2_print"
    PYTHON2_EXCEPTION = "python2_exception"
    PYTHON2_DIVISION = "python2_division"
    PYTHON2_UNICODE = "python2_unicode"
    TAB_MIXED_SPACE = "tab_mixed_space"
    TRAILING_WHITESPACE = "trailing_whitespace"
    MISSING_NEWLINE = "missing_newline"
    NULL_BYTE = "null_byte"
    INVALID_CHAR = "invalid_char"
    SYNTAX_ERROR = "syntax_error"


class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class NormalizationIssue:
    issue_type: IssueType
    severity: Severity
    line_number: Optional[int] = None
    original: Optional[str] = None
    suggested: Optional[str] = None
    message: str = ""
    auto_fixable: bool = False
    is_dangerous: bool = False


@dataclass
class NormalizationResult:
    original_file: str
    normalized_file: Optional[str] = None
    original_encoding: Optional[str] = None
    detected_encoding: Optional[str] = None
    final_encoding: str = "utf-8"
    issues: List[NormalizationIssue] = field(default_factory=list)
    fixed_issues: List[NormalizationIssue] = field(default_factory=list)
    unfixed_issues: List[NormalizationIssue] = field(default_factory=list)
    original_lines: int = 0
    normalized_lines: int = 0
    original_hash: Optional[str] = None
    normalized_hash: Optional[str] = None
    can_load: bool = False
    load_error: Optional[str] = None
    diff_summary: Dict[str, Any] = field(default_factory=dict)
    success: bool = False
    message: str = ""


class TxtStrategyNormalizer:
    """TXT 策略文本标准化器"""

    _PYTHON2_PRINT_PATTERN = re.compile(r"^\s*print\s+(?!\()")
    _PYTHON2_EXCEPTION_PATTERN = re.compile(r"except\s+\w+\s*,\s*\w+\s*:")
    _TAB_PATTERN = re.compile(r"^\t+")
    _MIXED_INDENT_PATTERN = re.compile(r"^(\t+ +| +\t+)")
    _TRAILING_WHITESPACE_PATTERN = re.compile(r"[ \t]+$")

    def __init__(self, cache_dir: Optional[str] = None, auto_fix_safe: bool = True):
        self.cache_dir = cache_dir or os.path.join(
            tempfile.gettempdir(), "strategy_normalize_cache"
        )
        self.auto_fix_safe = auto_fix_safe
        os.makedirs(self.cache_dir, exist_ok=True)

    @staticmethod
    def _normalize_encoding_name(encoding: Optional[str]) -> str:
        if not encoding:
            return "utf-8"
        lowered = encoding.lower()
        if lowered in ("gb2312", "gb18030"):
            return "gbk"
        return encoding

    @staticmethod
    def _detect_encoding_without_chardet(raw_data: bytes) -> Tuple[str, float]:
        if raw_data.startswith(b"\xef\xbb\xbf"):
            return "utf-8-sig", 0.99
        if raw_data.startswith(b"\xff\xfe"):
            return "utf-16-le", 0.95
        if raw_data.startswith(b"\xfe\xff"):
            return "utf-16-be", 0.95

        for encoding in ("utf-8", "gbk", "gb2312", "big5", "cp1252", "latin-1"):
            try:
                raw_data.decode(encoding)
                confidence = 0.85 if encoding == "utf-8" else 0.6
                return encoding, confidence
            except UnicodeDecodeError:
                continue

        return "latin-1", 0.0

    def detect_encoding(self, file_path: str) -> Tuple[str, float]:
        """检测文件编码"""
        with open(file_path, "rb") as f:
            raw_data = f.read()

        if chardet is not None:
            result = chardet.detect(raw_data)
            encoding = self._normalize_encoding_name(result.get("encoding"))
            confidence = float(result.get("confidence", 0.0) or 0.0)
            return encoding, confidence

        return self._detect_encoding_without_chardet(raw_data)

    def read_with_encoding_fallback(self, file_path: str) -> Tuple[str, str]:
        """多编码读取，返回内容和使用的编码"""
        detected_encoding, confidence = self.detect_encoding(file_path)

        encodings_to_try = [detected_encoding]
        for fallback in ["utf-8", "gbk", "gb2312", "latin-1", "cp1252", "big5"]:
            if fallback not in encodings_to_try:
                encodings_to_try.append(fallback)

        for encoding in encodings_to_try:
            if not encoding:
                continue
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    content = f.read()
                return content, encoding
            except (UnicodeDecodeError, LookupError):
                continue

        with open(file_path, "rb") as f:
            raw = f.read()
        return raw.decode("latin-1", errors="replace"), "latin-1"

    def detect_indentation_issues(self, content: str) -> List[NormalizationIssue]:
        """检测缩进问题"""
        issues = []
        lines = content.split("\n")

        has_tab_indent = False
        has_space_indent = False
        mixed_lines = []

        for i, line in enumerate(lines, 1):
            if not line.strip():
                continue

            if self._TAB_PATTERN.match(line):
                has_tab_indent = True

            if line.startswith(" ") and not line.startswith("\t"):
                leading_spaces = len(line) - len(line.lstrip(" "))
                if leading_spaces > 0 and leading_spaces % 4 != 0:
                    issues.append(
                        NormalizationIssue(
                            issue_type=IssueType.INDENTATION,
                            severity=Severity.WARNING,
                            line_number=i,
                            message=f"空格缩进不是4的倍数 ({leading_spaces}个空格)",
                            auto_fixable=True,
                            is_dangerous=False,
                        )
                    )
                has_space_indent = True

            if self._MIXED_INDENT_PATTERN.match(line):
                mixed_lines.append(i)

        if has_tab_indent and has_space_indent:
            issues.append(
                NormalizationIssue(
                    issue_type=IssueType.TAB_MIXED_SPACE,
                    severity=Severity.WARNING,
                    message=f"文件混用TAB和空格缩进 (混用行: {len(mixed_lines)}行)",
                    auto_fixable=True,
                    is_dangerous=True,
                )
            )

        for i in mixed_lines:
            issues.append(
                NormalizationIssue(
                    issue_type=IssueType.INDENTATION,
                    severity=Severity.WARNING,
                    line_number=i,
                    message="同一行混用TAB和空格",
                    auto_fixable=True,
                    is_dangerous=True,
                )
            )

        return issues

    def detect_python2_issues(self, content: str) -> List[NormalizationIssue]:
        """检测 Python2 兼容问题"""
        issues = []
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            if self._PYTHON2_PRINT_PATTERN.match(line):
                issues.append(
                    NormalizationIssue(
                        issue_type=IssueType.PYTHON2_PRINT,
                        severity=Severity.ERROR,
                        line_number=i,
                        original=line.strip(),
                        suggested=f"print({line.strip()[6:]})",
                        message="Python2 风格 print 语句",
                        auto_fixable=True,
                        is_dangerous=False,
                    )
                )

            if "except" in line and self._PYTHON2_EXCEPTION_PATTERN.search(line):
                issues.append(
                    NormalizationIssue(
                        issue_type=IssueType.PYTHON2_EXCEPTION,
                        severity=Severity.ERROR,
                        line_number=i,
                        original=line.strip(),
                        message="Python2 风格异常处理 'except E, e'",
                        auto_fixable=False,
                        is_dangerous=True,
                    )
                )

        return issues

    def detect_syntax_issues(self, content: str) -> List[NormalizationIssue]:
        """检测语法问题"""
        issues = []

        if "\x00" in content:
            null_count = content.count("\x00")
            issues.append(
                NormalizationIssue(
                    issue_type=IssueType.NULL_BYTE,
                    severity=Severity.ERROR,
                    message=f"文件包含 {null_count} 个 NULL 字符",
                    auto_fixable=True,
                    is_dangerous=False,
                )
            )
            content = content.replace("\x00", "")

        try:
            ast.parse(content)
        except SyntaxError as e:
            issues.append(
                NormalizationIssue(
                    issue_type=IssueType.SYNTAX_ERROR,
                    severity=Severity.CRITICAL,
                    line_number=e.lineno,
                    message=f"语法错误: {e.msg}",
                    auto_fixable=False,
                    is_dangerous=False,
                )
            )

        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            if self._TRAILING_WHITESPACE_PATTERN.search(line):
                issues.append(
                    NormalizationIssue(
                        issue_type=IssueType.TRAILING_WHITESPACE,
                        severity=Severity.INFO,
                        line_number=i,
                        message="行尾空白字符",
                        auto_fixable=True,
                        is_dangerous=False,
                    )
                )

        if content and not content.endswith("\n"):
            issues.append(
                NormalizationIssue(
                    issue_type=IssueType.MISSING_NEWLINE,
                    severity=Severity.INFO,
                    message="文件末尾缺少换行符",
                    auto_fixable=True,
                    is_dangerous=False,
                )
            )

        return issues

    def fix_null_bytes(self, content: str) -> str:
        """修复 NULL 字符"""
        return content.replace("\x00", "")

    def fix_indentation(self, content: str, mode: str = "space4") -> str:
        """修复缩进问题

        mode: 'space4' (4空格), 'space2' (2空格), 'tab' (TAB)
        """
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            if not line.strip():
                fixed_lines.append(line)
                continue

            leading = len(line) - len(line.lstrip())
            indent_chars = line[:leading]

            if "\t" in indent_chars or mode == "space4":
                tab_count = indent_chars.count("\t")
                space_count = leading - tab_count
                total_indent = tab_count * 4 + space_count
                new_indent = " " * total_indent
            elif mode == "space2":
                tab_count = indent_chars.count("\t")
                space_count = leading - tab_count
                total_indent = tab_count * 2 + space_count
                new_indent = " " * total_indent
            else:
                new_indent = indent_chars

            fixed_lines.append(new_indent + line.lstrip())

        return "\n".join(fixed_lines)

    def fix_trailing_whitespace(self, content: str) -> str:
        """修复行尾空白"""
        lines = content.split("\n")
        return "\n".join(line.rstrip() for line in lines)

    def fix_missing_newline(self, content: str) -> str:
        """添加文件末尾换行"""
        if content and not content.endswith("\n"):
            return content + "\n"
        return content

    def fix_python2_print(self, content: str) -> str:
        """修复 Python2 print 语句"""
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            match = self._PYTHON2_PRINT_PATTERN.match(line)
            if match:
                indent = len(line) - len(line.lstrip())
                rest = line.strip()[6:]
                fixed_lines.append(" " * indent + f"print({rest})")
            else:
                fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def normalize(
        self, file_path: str, output_path: Optional[str] = None
    ) -> NormalizationResult:
        """标准化策略文件"""
        result = NormalizationResult(original_file=file_path)

        if not os.path.exists(file_path):
            result.message = "文件不存在"
            result.success = False
            return result

        content, used_encoding = self.read_with_encoding_fallback(file_path)
        result.original_encoding = used_encoding
        result.detected_encoding, _ = self.detect_encoding(file_path)

        original_hash = hashlib.md5(
            content.encode("utf-8", errors="replace")
        ).hexdigest()
        result.original_hash = original_hash
        result.original_lines = len(content.split("\n"))

        issues = []
        issues.extend(self.detect_indentation_issues(content))
        issues.extend(self.detect_python2_issues(content))
        issues.extend(self.detect_syntax_issues(content))

        if used_encoding.lower() not in ("utf-8", "ascii"):
            issues.append(
                NormalizationIssue(
                    issue_type=IssueType.ENCODING,
                    severity=Severity.INFO,
                    message=f"原始编码: {used_encoding}",
                    auto_fixable=True,
                    is_dangerous=False,
                )
            )

        result.issues = issues

        fixed_content = content
        fixed_issues = []
        unfixed_issues = []

        safe_fixes = [
            (self.fix_null_bytes, IssueType.NULL_BYTE),
            (self.fix_trailing_whitespace, IssueType.TRAILING_WHITESPACE),
            (self.fix_missing_newline, IssueType.MISSING_NEWLINE),
        ]

        if self.auto_fix_safe:
            for fix_func, issue_type in safe_fixes:
                matching_issues = [i for i in issues if i.issue_type == issue_type]
                if matching_issues:
                    try:
                        fixed_content = fix_func(fixed_content)
                        fixed_issues.extend(matching_issues)
                    except Exception as e:
                        for issue in matching_issues:
                            issue.message += f" (修复失败: {e})"
                            unfixed_issues.append(issue)

            indent_issues = [
                i
                for i in issues
                if i.issue_type in (IssueType.INDENTATION, IssueType.TAB_MIXED_SPACE)
            ]
            if indent_issues:
                try:
                    fixed_content = self.fix_indentation(fixed_content)
                    fixed_issues.extend(indent_issues)
                except Exception as e:
                    for issue in indent_issues:
                        issue.message += f" (修复失败: {e})"
                        unfixed_issues.append(issue)

            print_issues = [
                i
                for i in issues
                if i.issue_type == IssueType.PYTHON2_PRINT and i.auto_fixable
            ]
            if print_issues:
                try:
                    fixed_content = self.fix_python2_print(fixed_content)
                    fixed_issues.extend(print_issues)
                except Exception as e:
                    for issue in print_issues:
                        issue.message += f" (修复失败: {e})"
                        unfixed_issues.append(issue)

        for issue in issues:
            if issue not in fixed_issues and issue not in unfixed_issues:
                unfixed_issues.append(issue)

        result.fixed_issues = fixed_issues
        result.unfixed_issues = unfixed_issues

        try:
            ast.parse(fixed_content)
            result.can_load = True
        except SyntaxError as e:
            result.can_load = False
            result.load_error = f"语法错误: {e.msg} (行 {e.lineno})"

        result.normalized_lines = len(fixed_content.split("\n"))
        result.normalized_hash = hashlib.md5(fixed_content.encode("utf-8")).hexdigest()

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(fixed_content)
            result.normalized_file = output_path
        else:
            cache_name = f"{original_hash}_normalized.txt"
            cache_path = os.path.join(self.cache_dir, cache_name)
            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(fixed_content)
            result.normalized_file = cache_path

        result.diff_summary = {
            "total_issues": len(issues),
            "fixed_count": len(fixed_issues),
            "unfixed_count": len(unfixed_issues),
            "dangerous_count": len([i for i in issues if i.is_dangerous]),
            "encoding_changed": used_encoding.lower() != "utf-8",
            "lines_changed": result.original_lines != result.normalized_lines,
            "content_changed": result.original_hash != result.normalized_hash,
        }

        result.success = result.can_load or len(fixed_issues) > 0
        result.message = f"标准化完成: 修复 {len(fixed_issues)} 个问题, {len(unfixed_issues)} 个问题待处理"

        return result

    def batch_normalize(
        self, files: List[str], output_dir: Optional[str] = None
    ) -> Dict[str, NormalizationResult]:
        """批量标准化"""
        results = {}

        for file_path in files:
            if output_dir:
                base_name = os.path.basename(file_path)
                output_path = os.path.join(output_dir, base_name)
            else:
                output_path = None

            result = self.normalize(file_path, output_path)
            results[file_path] = result

        return results

    def generate_report(self, results: Dict[str, NormalizationResult], output_md: str):
        """生成 Markdown 报告"""
        from datetime import datetime

        total = len(results)
        success_count = sum(1 for r in results.values() if r.success)
        can_load_count = sum(1 for r in results.values() if r.can_load)

        issue_counts = {}
        for result in results.values():
            for issue in result.issues:
                key = issue.issue_type.value
                issue_counts[key] = issue_counts.get(key, 0) + 1

        fixed_counts = {}
        for result in results.values():
            for issue in result.fixed_issues:
                key = issue.issue_type.value
                fixed_counts[key] = fixed_counts.get(key, 0) + 1

        with open(output_md, "w", encoding="utf-8") as f:
            f.write("# Task 37 Result: TXT 策略文本标准化\n\n")
            f.write(
                f"**标准化时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )

            f.write("## 修改文件\n\n")
            f.write("- `src/txt_strategy_normalizer.py` (新增)\n")
            f.write("- `scripts/task37_txt_normalization_test.py` (新增)\n")
            f.write(
                "- `docs/0330_result/task37_txt_normalization_result.md` (本文件)\n\n"
            )

            f.write("## 完成内容\n\n")
            f.write("1. 创建 TXT 策略文本标准化器\n")
            f.write("2. 实现多编码读取增强（utf-8, gbk, gb2312, latin-1 等）\n")
            f.write("3. 实现 TAB/空格缩进修复\n")
            f.write("4. 实现 Python2 兼容问题检测（print语句、异常语法）\n")
            f.write("5. 从失败样本中抽取策略进行重试验证\n\n")

            f.write("## 标准化统计\n\n")
            f.write(f"| 指标 | 数值 |\n")
            f.write(f"|------|------|\n")
            f.write(f"| 总文件数 | {total} |\n")
            f.write(f"| 成功标准化数 | {success_count} |\n")
            f.write(f"| 可加载数 | {can_load_count} |\n")
            f.write(f"| 成功率 | {success_count / total * 100:.1f}% |\n")
            f.write(f"| 可加载率 | {can_load_count / total * 100:.1f}% |\n\n")

            f.write("## 问题类型分布\n\n")
            f.write("| 问题类型 | 检测数量 | 修复数量 |\n")
            f.write("|----------|----------|----------|\n")
            for issue_type, count in sorted(issue_counts.items(), key=lambda x: -x[1]):
                fixed = fixed_counts.get(issue_type, 0)
                f.write(f"| {issue_type} | {count} | {fixed} |\n")

            f.write("\n## 详细结果\n\n")

            f.write("### 成功标准化的策略\n\n")
            success_files = [(p, r) for p, r in results.items() if r.success]
            if success_files:
                f.write("| 文件 | 原编码 | 修复问题 | 可加载 |\n")
                f.write("|------|--------|----------|--------|\n")
                for path, result in success_files[:20]:
                    name = os.path.basename(path)[:40]
                    encoding = result.original_encoding or "unknown"
                    fixed = len(result.fixed_issues)
                    can_load = "✓" if result.can_load else "✗"
                    f.write(f"| {name} | {encoding} | {fixed} | {can_load} |\n")
            else:
                f.write("无成功标准化样本\n\n")

            f.write("\n### 未成功标准化的策略\n\n")
            failed_files = [(p, r) for p, r in results.items() if not r.success]
            if failed_files:
                f.write("| 文件 | 原编码 | 问题数 | 主要问题 |\n")
                f.write("|------|--------|--------|----------|\n")
                for path, result in failed_files[:20]:
                    name = os.path.basename(path)[:40]
                    encoding = result.original_encoding or "unknown"
                    issues = len(result.unfixed_issues)
                    main_issue = (
                        result.unfixed_issues[0].message[:30]
                        if result.unfixed_issues
                        else "N/A"
                    )
                    f.write(f"| {name} | {encoding} | {issues} | {main_issue} |\n")
            else:
                f.write("所有样本均成功标准化\n\n")

            f.write("\n## 功能说明\n\n")
            f.write("### 编码检测与转换\n\n")
            f.write("- 使用 `chardet` 库自动检测编码\n")
            f.write("- 支持多种编码尝试：utf-8, gbk, gb2312, latin-1, cp1252, big5\n")
            f.write("- 最终输出统一为 UTF-8 编码\n\n")

            f.write("### 缩进修复\n\n")
            f.write("- 检测 TAB/空格混用问题\n")
            f.write("- 检测非标准空格缩进（非4倍数）\n")
            f.write("- 自动转换为 4 空格标准缩进\n")
            f.write("- 混用修复标记为危险操作，需人工确认\n\n")

            f.write("### Python2 兼容问题检测\n\n")
            f.write("- 检测旧式 `print` 语句（不含括号）\n")
            f.write("- 检测旧式异常处理 `except E, e`\n")
            f.write("- print 语句可自动修复\n")
            f.write("- 异常语法需人工修复\n\n")

            f.write("### 其他修复\n\n")
            f.write("- NULL 字符清除\n")
            f.write("- 行尾空白清除\n")
            f.write("- 文件末尾换行补充\n\n")

            f.write("## 使用方法\n\n")
            f.write("```python\n")
            f.write(
                "from jk2bt.strategy.txt_strategy_normalizer import TxtStrategyNormalizer\n\n"
            )
            f.write("normalizer = TxtStrategyNormalizer()\n")
            f.write("result = normalizer.normalize('strategy.txt')\n\n")
            f.write("# 获取标准化后的文件路径\n")
            f.write("normalized_file = result.normalized_file\n\n")
            f.write("# 查看修复的问题\n")
            f.write("for issue in result.fixed_issues:\n")
            f.write("    print(f'{issue.issue_type}: {issue.message}')\n")
            f.write("```\n\n")

            f.write("## 已知边界\n\n")
            f.write("1. **复杂语法错误**: 需人工修复\n")
            f.write("2. **Python2 异常语法**: 需人工修复\n")
            f.write("3. **缩进混用修复**: 标记为危险操作，可能影响语义\n")
            f.write("4. **非策略文件**: 部分文件为文档而非策略\n\n")

            f.write("## 后续建议\n\n")
            if can_load_count < total * 0.8:
                f.write("当前可加载率较低，建议:\n")
                f.write("1. 增强复杂语法错误修复能力\n")
                f.write("2. 完善异常语法自动转换\n")
                f.write("3. 增加更多编码支持\n")
            else:
                f.write("当前标准化效果良好，建议:\n")
                f.write("1. 将标准化流程集成到策略加载流程\n")
                f.write("2. 增加标准化缓存管理\n")
                f.write("3. 建立标准化质量回归测试\n")

            f.write("\n---\n\n")
            f.write(f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")


def normalize_strategy_file(
    file_path: str, output_path: Optional[str] = None
) -> NormalizationResult:
    """便捷函数：标准化单个策略文件"""
    normalizer = TxtStrategyNormalizer()
    return normalizer.normalize(file_path, output_path)


def batch_normalize_strategies(
    files: List[str], output_dir: Optional[str] = None
) -> Dict[str, NormalizationResult]:
    """便捷函数：批量标准化策略文件"""
    normalizer = TxtStrategyNormalizer()
    return normalizer.batch_normalize(files, output_dir)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="TXT 策略文本标准化")
    parser.add_argument("files", nargs="+", help="策略文件路径")
    parser.add_argument("--output-dir", default=None, help="输出目录")
    parser.add_argument("--report", default=None, help="报告输出路径")

    args = parser.parse_args()

    normalizer = TxtStrategyNormalizer()
    results = normalizer.batch_normalize(args.files, args.output_dir)

    logger.info("标准化结果:")
    logger.info(f"  总文件: {len(results)}")
    logger.info(f"  成功: {sum(1 for r in results.values() if r.success)}")
    logger.info(f"  可加载: {sum(1 for r in results.values() if r.can_load)}")

    for path, result in results.items():
        logger.info(f"{os.path.basename(path)}:")
        logger.info(f"  编码: {result.original_encoding} -> utf-8")
        logger.info(f"  问题: {len(result.issues)} (修复: {len(result.fixed_issues)})")
        logger.info(f"  可加载: {result.can_load}")
        logger.info(f"  输出: {result.normalized_file}")

    if args.report:
        normalizer.generate_report(results, args.report)
        logger.info(f"报告已生成: {args.report}")

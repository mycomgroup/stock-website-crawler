"""
TXT策略文本标准化工具

处理常见文件层面失败问题:
1. 多编码读取增强 (UTF-8, GBK, GB2312, Latin-1)
2. TAB/空格缩进修复或检测
3. Python2 兼容性修复 (print, except, division等)
4. 标准化前后差异记录
"""

import os
import re
import tempfile
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum

# 获取logger
logger = logging.getLogger(__name__)


class NormalizationIssue(Enum):
    """标准化问题类型"""

    ENCODING = "encoding"
    TAB_INDENT = "tab_indent"
    PRINT_STMT = "print_statement"
    EXCEPT_SYNTAX = "except_syntax"
    DIVISION = "division"
    UNICODE_LITERAL = "unicode_literal"
    OTHER_PY2 = "other_python2"
    MIXED_INDENT = "mixed_indent"


@dataclass
class NormalizationResult:
    """标准化结果"""

    original_path: str
    normalized_path: Optional[str]
    detected_encoding: str
    original_size: int
    normalized_size: int
    issues_found: List[NormalizationIssue] = field(default_factory=list)
    issues_fixed: List[NormalizationIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    details: Dict = field(default_factory=dict)
    success: bool = False
    error_message: str = ""


class TxtNormalizer:
    """TXT策略文本标准化器"""

    _ENCODINGS = ["utf-8", "gbk", "gb2312", "latin-1"]

    _PRINT_PATTERN = re.compile(
        r'^(\s*)print\s+(?![\'"\(])'
        r"(.*?)"
        r"(?=\s*(?:#|$|\n))",
        re.MULTILINE,
    )

    _PRINT_SIMPLE_PATTERN = re.compile(r"^(\s*)print\s+([^\(\n].*?)$", re.MULTILINE)

    _EXCEPT_OLD_PATTERN = re.compile(
        r"^(\s*)except\s+(\w+)\s*,\s*(\w+)\s*:", re.MULTILINE
    )

    _TAB_PATTERN = re.compile(r"^\t+")

    _MIXED_INDENT_PATTERN = re.compile(r"^(\t+)( +)")

    _DIVISION_PATTERN = re.compile(r"^(\s*)from\s+__future__\s+import\s+division")

    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = output_dir or tempfile.gettempdir()
        self._cache: Dict[str, NormalizationResult] = {}

    def detect_encoding(self, file_path: str) -> Tuple[str, bool]:
        """检测文件编码"""
        for encoding in self._ENCODINGS:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    content = f.read()
                    if "\x00" in content:
                        continue
                return encoding, True
            except UnicodeDecodeError:
                continue
            except Exception:
                continue
        return "unknown", False

    def read_with_encoding(self, file_path: str) -> Tuple[Optional[str], str]:
        """多编码读取文件"""
        for encoding in self._ENCODINGS:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    content = f.read()
                if "\x00" in content:
                    content = content.replace("\x00", "")
                return content, encoding
            except UnicodeDecodeError:
                continue
            except Exception as e:
                continue
        return None, "unknown"

    def detect_tab_indent(self, content: str) -> Tuple[bool, int]:
        """检测TAB缩进"""
        has_tab = False
        tab_lines = 0
        for line in content.splitlines():
            if line.startswith("\t"):
                has_tab = True
                tab_lines += 1
        return has_tab, tab_lines

    def detect_mixed_indent(self, content: str) -> Tuple[bool, int]:
        """检测TAB/空格混用"""
        has_mixed = False
        mixed_lines = 0
        for i, line in enumerate(content.splitlines(), 1):
            if self._MIXED_INDENT_PATTERN.match(line):
                has_mixed = True
                mixed_lines += 1
        return has_mixed, mixed_lines

    def detect_python2_print(self, content: str) -> Tuple[bool, int, List[int]]:
        """检测Python2 print语句"""
        has_py2_print = False
        count = 0
        line_numbers = []

        for i, line in enumerate(content.splitlines(), 1):
            if self._PRINT_SIMPLE_PATTERN.match(line):
                if "print(" not in line:
                    has_py2_print = True
                    count += 1
                    line_numbers.append(i)

        return has_py2_print, count, line_numbers

    def detect_python2_except(self, content: str) -> Tuple[bool, int, List[int]]:
        """检测Python2 except语法"""
        has_py2_except = False
        count = 0
        line_numbers = []

        for i, line in enumerate(content.splitlines(), 1):
            if self._EXCEPT_OLD_PATTERN.match(line):
                has_py2_except = True
                count += 1
                line_numbers.append(i)

        return has_py2_except, count, line_numbers

    def fix_tab_indent(self, content: str, spaces_per_tab: int = 4) -> str:
        """修复TAB缩进为空格"""
        lines = content.splitlines()
        fixed_lines = []

        for line in lines:
            if line.startswith("\t"):
                tab_count = len(line) - len(line.lstrip("\t"))
                spaces = " " * (tab_count * spaces_per_tab)
                fixed_line = spaces + line.lstrip("\t")
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_python2_print(self, content: str) -> str:
        """修复Python2 print语句"""
        lines = content.splitlines()
        fixed_lines = []

        for line in lines:
            match = self._PRINT_SIMPLE_PATTERN.match(line)
            if match and "print(" not in line:
                indent = match.group(1)
                content_part = match.group(2).rstrip()

                if content_part:
                    if (
                        "," in content_part
                        and not content_part.startswith("'")
                        and not content_part.startswith('"')
                    ):
                        parts = [p.strip() for p in content_part.split(",")]
                        formatted_parts = []
                        for part in parts:
                            if part.startswith("'") or part.startswith('"'):
                                formatted_parts.append(part)
                            else:
                                formatted_parts.append(f"str({part})")
                        new_print = (
                            f"{indent}print(' '.join([{', '.join(formatted_parts)}]))"
                        )
                    else:
                        new_print = f"{indent}print({content_part})"
                else:
                    new_print = f"{indent}print()"

                fixed_lines.append(new_print)
            else:
                fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_python2_except(self, content: str) -> str:
        """修复Python2 except语法"""
        lines = content.splitlines()
        fixed_lines = []

        for line in lines:
            match = self._EXCEPT_OLD_PATTERN.match(line)
            if match:
                indent = match.group(1)
                exc_type = match.group(2)
                exc_var = match.group(3)
                new_except = f"{indent}except {exc_type} as {exc_var}:"
                fixed_lines.append(new_except)
            else:
                fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def normalize_file(
        self,
        file_path: str,
        fix_encoding: bool = True,
        fix_indent: bool = True,
        fix_py2_print: bool = True,
        fix_py2_except: bool = True,
        keep_original: bool = True,
    ) -> NormalizationResult:
        """标准化单个文件"""

        if file_path in self._cache:
            return self._cache[file_path]

        result = NormalizationResult(
            original_path=file_path,
            normalized_path=None,
            detected_encoding="unknown",
            original_size=0,
            normalized_size=0,
            success=False,
        )

        if not os.path.exists(file_path):
            result.error_message = "文件不存在"
            self._cache[file_path] = result
            return result

        content, encoding = self.read_with_encoding(file_path)
        if content is None:
            result.error_message = "无法解码文件"
            self._cache[file_path] = result
            return result

        result.detected_encoding = encoding
        result.original_size = len(content)

        original_content = content

        has_tab, tab_lines = self.detect_tab_indent(content)
        if has_tab:
            result.issues_found.append(NormalizationIssue.TAB_INDENT)
            result.details["tab_lines"] = tab_lines

        has_mixed, mixed_lines = self.detect_mixed_indent(content)
        if has_mixed:
            result.issues_found.append(NormalizationIssue.MIXED_INDENT)
            result.details["mixed_lines"] = mixed_lines

        has_py2_print, print_count, print_lines = self.detect_python2_print(content)
        if has_py2_print:
            result.issues_found.append(NormalizationIssue.PRINT_STMT)
            result.details["print_lines"] = print_lines
            result.details["print_count"] = print_count

        has_py2_except, except_count, except_lines = self.detect_python2_except(content)
        if has_py2_except:
            result.issues_found.append(NormalizationIssue.EXCEPT_SYNTAX)
            result.details["except_lines"] = except_lines
            result.details["except_count"] = except_count

        normalized_content = content

        if has_tab and fix_indent:
            normalized_content = self.fix_tab_indent(normalized_content)
            result.issues_fixed.append(NormalizationIssue.TAB_INDENT)

        if has_py2_print and fix_py2_print:
            normalized_content = self.fix_python2_print(normalized_content)
            result.issues_fixed.append(NormalizationIssue.PRINT_STMT)
            result.warnings.append("Python2 print语句已转换为Python3格式")

        if has_py2_except and fix_py2_except:
            normalized_content = self.fix_python2_except(normalized_content)
            result.issues_fixed.append(NormalizationIssue.EXCEPT_SYNTAX)

        if normalized_content != original_content:
            file_name = os.path.basename(file_path)
            safe_name = file_name.replace("/", "_").replace("\\", "_")
            normalized_path = os.path.join(self.output_dir, f"normalized_{safe_name}")

            try:
                with open(normalized_path, "w", encoding="utf-8") as f:
                    f.write(normalized_content)
                result.normalized_path = normalized_path
                result.normalized_size = len(normalized_content)
                result.success = True
            except Exception as e:
                result.error_message = f"写入标准化文件失败: {str(e)}"
                self._cache[file_path] = result
                return result
        else:
            result.normalized_path = file_path
            result.normalized_size = result.original_size
            result.success = True

        result.details["changes"] = len(normalized_content) != len(original_content)

        self._cache[file_path] = result
        return result

    def normalize_directory(
        self, directory: str, pattern: str = "*.txt", limit: Optional[int] = None
    ) -> Dict[str, List[NormalizationResult]]:
        """批量标准化目录下的文件"""

        import glob

        files = glob.glob(os.path.join(directory, pattern))
        if limit:
            files = files[:limit]

        results = {"success": [], "failed": [], "no_changes": [], "all": []}

        for file_path in sorted(files):
            result = self.normalize_file(file_path)
            results["all"].append(result)

            if result.success:
                if result.issues_fixed:
                    results["success"].append(result)
                else:
                    results["no_changes"].append(result)
            else:
                results["failed"].append(result)

        return results

    def print_summary(self, results: Dict[str, List[NormalizationResult]]) -> None:
        """打印标准化结果摘要"""

        total = len(results["all"])
        fixed = len(results["success"])
        no_change = len(results["no_changes"])
        failed = len(results["failed"])

        logger.info("=" * 80)
        logger.info("TXT策略文本标准化结果摘要")
        logger.info("=" * 80)
        logger.info(f"总文件数: {total}")
        logger.info(f"成功标准化: {fixed}")
        logger.info(f"无需修改: {no_change}")
        logger.info(f"失败: {failed}")
        logger.info("-" * 40)

        issue_stats = {}
        for r in results["all"]:
            for issue in r.issues_found:
                issue_stats[issue.value] = issue_stats.get(issue.value, 0) + 1

        if issue_stats:
            logger.info("发现的问题统计:")
            for issue_type, count in sorted(issue_stats.items()):
                logger.info(f"  {issue_type}: {count}")

        fix_stats = {}
        for r in results["success"]:
            for issue in r.issues_fixed:
                fix_stats[issue.value] = fix_stats.get(issue.value, 0) + 1

        if fix_stats:
            logger.info("已修复的问题统计:")
            for issue_type, count in sorted(fix_stats.items()):
                logger.info(f"  {issue_type}: {count}")

        if results["failed"]:
            logger.warning("失败文件详情:")
            for r in results["failed"][:5]:
                logger.warning(f"  - {os.path.basename(r.original_path)}: {r.error_message}")
            if len(results["failed"]) > 5:
                logger.warning(f"  ... 共 {len(results['failed'])} 个")

        logger.info("=" * 80)


def normalize_strategy_text(
    file_path: str, output_dir: Optional[str] = None
) -> Tuple[Optional[str], NormalizationResult]:
    """便捷函数: 标准化策略文本"""

    normalizer = TxtNormalizer(output_dir)
    result = normalizer.normalize_file(file_path)

    return result.normalized_path, result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="TXT策略文本标准化工具")
    parser.add_argument("--file", help="标准化单个文件")
    parser.add_argument("--dir", default="jkcode/jkcode", help="标准化目录")
    parser.add_argument("--pattern", default="*.txt", help="文件匹配模式")
    parser.add_argument("--limit", type=int, help="限制处理数量")
    parser.add_argument("--output", help="输出目录")
    parser.add_argument("--verbose", action="store_true", help="详细输出")

    args = parser.parse_args()

    normalizer = TxtNormalizer(args.output)

    if args.file:
        result = normalizer.normalize_file(args.file)
        logger.info(f"文件: {os.path.basename(result.original_path)}")
        logger.info(f"编码: {result.detected_encoding}")
        logger.info(f"发现问题: {[i.value for i in result.issues_found]}")
        logger.info(f"已修复: {[i.value for i in result.issues_fixed]}")
        logger.info(f"输出: {result.normalized_path}")
        if result.warnings:
            logger.warning(f"警告: {result.warnings}")
    else:
        results = normalizer.normalize_directory(args.dir, args.pattern, args.limit)
        normalizer.print_summary(results)

        if args.verbose:
            logger.info("标准化详情:")
            for r in results["success"][:10]:
                logger.info(f"{os.path.basename(r.original_path)}:")
                logger.info(f"  编码: {r.detected_encoding}")
                logger.info(f"  问题: {[i.value for i in r.issues_found]}")
                logger.info(f"  修复: {[i.value for i in r.issues_fixed]}")
                logger.info(f"  输出: {r.normalized_path}")

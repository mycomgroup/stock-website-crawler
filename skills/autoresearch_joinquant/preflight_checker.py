"""
Preflight Checker Module

本地轻量预检查模块，在提交平台回测前做本地检查。
参考设计文档: strategy_autoresearch_design.md 第 10.1 节

V1 预检查包括:
1. 文件存在
2. 编码正常 (UTF-8)
3. Python 语法可解析
4. 文件没有被写空
5. 不包含显然破坏性占位内容

注意: 预检查不参与评分，只负责挡住低级错误。

⚠️  此文件为基础设施文件，agent 不可修改。只改 strategy.py。
"""

import py_compile
import re
from pathlib import Path
from typing import Tuple, List


# 破坏性占位内容模式 (不区分大小写)
DESTRUCTIVE_PATTERNS: List[re.Pattern] = [
    re.compile(r'\bTODO\b', re.IGNORECASE),
    re.compile(r'\bFIXME\b', re.IGNORECASE),
    re.compile(r'\bplaceholder\b', re.IGNORECASE),
    re.compile(r'\bxxx\b', re.IGNORECASE),
    re.compile(r'\btbd\b', re.IGNORECASE),
    re.compile(r'\bhack\b', re.IGNORECASE),
    re.compile(r'\bnot implemented\b', re.IGNORECASE),
    re.compile(r'\bstub\b', re.IGNORECASE),
]


def check_file_exists(file_path: str) -> Tuple[bool, str]:
    """
    检查文件是否存在。

    Args:
        file_path: 待检查的文件路径

    Returns:
        Tuple[bool, str]: (是否通过, 失败原因或"OK")
    """
    path = Path(file_path)
    if path.exists() and path.is_file():
        return True, "OK"
    elif path.exists() and path.is_dir():
        return False, f"Path exists but is a directory, not a file: {file_path}"
    else:
        return False, f"File does not exist: {file_path}"


def check_encoding(file_path: str) -> Tuple[bool, str]:
    """
    检查文件是否为有效的 UTF-8 编码。

    Args:
        file_path: 待检查的文件路径

    Returns:
        Tuple[bool, str]: (是否通过, 失败原因或"OK")
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            f.read()
        return True, "OK"
    except UnicodeDecodeError as e:
        return False, f"File is not valid UTF-8 encoding: {e}"
    except OSError as e:
        return False, f"Failed to read file for encoding check: {e}"


def check_python_syntax(file_path: str) -> Tuple[bool, str]:
    """
    使用 py_compile 检查 Python 文件语法是否正确。

    Args:
        file_path: 待检查的 Python 文件路径

    Returns:
        Tuple[bool, str]: (是否通过, 失败原因或"OK")
    """
    try:
        py_compile.compile(file_path, doraise=True)
        return True, "OK"
    except py_compile.PyCompileError as e:
        return False, f"Python syntax error: {e}"
    except OSError as e:
        return False, f"Failed to compile file for syntax check: {e}"


def check_file_not_empty(file_path: str) -> Tuple[bool, str]:
    """
    检查文件是否为空（内容为空或只有空白字符）。

    Args:
        file_path: 待检查的文件路径

    Returns:
        Tuple[bool, str]: (是否通过, 失败原因或"OK")
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        stripped = content.strip()
        if not stripped:
            return False, "File is empty or contains only whitespace"
        return True, "OK"
    except UnicodeDecodeError as e:
        return False, f"File encoding issue when checking emptiness: {e}"
    except OSError as e:
        return False, f"Failed to read file for emptiness check: {e}"


def check_no_destructive_placeholders(content: str) -> Tuple[bool, str]:
    """
    检查内容是否包含显然破坏性的占位内容。

    检查以下模式（不区分大小写）:
    - TODO
    - FIXME
    - placeholder
    - xxx
    - tbd
    - hack
    - not implemented
    - stub

    Args:
        content: 文件内容字符串

    Returns:
        Tuple[bool, str]: (是否通过, 失败原因或"OK")
    """
    found_patterns = []
    for pattern in DESTRUCTIVE_PATTERNS:
        match = pattern.search(content)
        if match:
            found_patterns.append(match.group())

    if found_patterns:
        # 去重并保持顺序
        seen = set()
        unique_patterns = []
        for p in found_patterns:
            if p.lower() not in seen:
                seen.add(p.lower())
                unique_patterns.append(p)
        return False, f"Found destructive placeholder patterns: {', '.join(unique_patterns)}"
    return True, "OK"


def run_all_checks(file_path: str) -> Tuple[bool, List[str]]:
    """
    运行所有预检查。

    按顺序执行以下检查:
    1. 文件存在
    2. 编码正常 (UTF-8)
    3. Python 语法可解析
    4. 文件没有被写空
    5. 不包含显然破坏性占位内容

    Args:
        file_path: 待检查的文件路径

    Returns:
        Tuple[bool, List[str]]: (所有检查是否通过, 失败原因列表)
    """
    checks = [
        check_file_exists,
        check_encoding,
        check_python_syntax,
        check_file_not_empty,
    ]

    failure_reasons: List[str] = []

    # Run checks that operate on file_path
    for check in checks:
        passed, reason = check(file_path)
        if not passed:
            failure_reasons.append(reason)

    # For placeholder check, we need to read the file content first
    if not failure_reasons:  # Only check placeholders if previous checks passed
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            passed, reason = check_no_destructive_placeholders(content)
            if not passed:
                failure_reasons.append(reason)
        except (UnicodeDecodeError, OSError) as e:
            failure_reasons.append(f"Failed to read file for placeholder check: {e}")

    all_passed = len(failure_reasons) == 0
    return all_passed, failure_reasons


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python preflight_checker.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    print(f"Running preflight checks on: {file_path}")
    print("-" * 50)

    all_passed, reasons = run_all_checks(file_path)

    if all_passed:
        print("All checks PASSED")
    else:
        print("Checks FAILED:")
        for reason in reasons:
            print(f"  - {reason}")

    sys.exit(0 if all_passed else 1)

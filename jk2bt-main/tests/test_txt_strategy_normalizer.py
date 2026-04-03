"""
测试 TXT 策略文本标准化模块

覆盖功能:
- 编码检测与转换
- 缩进修复
- Python2兼容问题
- NULL字符清除
- 行尾空白清除
- 文件末尾换行
- 语法错误检测
- 批量标准化
"""

import os
import sys
import tempfile
import importlib.util
import unittest
from pathlib import Path

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
util_dir = os.path.join(base_dir, "src")

spec = importlib.util.spec_from_file_location(
    "txt_strategy_normalizer", os.path.join(util_dir, "txt_strategy_normalizer.py")
)
txt_norm_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(txt_norm_module)

TxtStrategyNormalizer = txt_norm_module.TxtStrategyNormalizer
NormalizationResult = txt_norm_module.NormalizationResult
NormalizationIssue = txt_norm_module.NormalizationIssue
IssueType = txt_norm_module.IssueType
Severity = txt_norm_module.Severity


class TestTxtStrategyNormalizer(unittest.TestCase):
    """测试 TxtStrategyNormalizer 类"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.normalizer = TxtStrategyNormalizer(cache_dir=self.temp_dir)

    def tearDown(self):
        import shutil

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def _create_test_file(
        self, content: str, encoding: str = "utf-8", filename: str = "test.txt"
    ) -> str:
        """创建测试文件"""
        file_path = os.path.join(self.temp_dir, filename)
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
        return file_path


class TestEncodingDetection(TestTxtStrategyNormalizer):
    """测试编码检测与转换"""

    def test_utf8_encoding_detection(self):
        content = "def initialize(context):\n    pass\n"
        file_path = self._create_test_file(content, "utf-8")

        result = self.normalizer.normalize(file_path)

        self.assertIsNotNone(result.original_encoding)
        self.assertTrue(result.can_load)
        self.assertEqual(result.final_encoding, "utf-8")

    def test_gbk_encoding_detection(self):
        content = "# 中文注释\ndef initialize(context):\n    pass\n"
        file_path = self._create_test_file(content, "gbk")

        detected, confidence = self.normalizer.detect_encoding(file_path)
        self.assertIsNotNone(detected)

    def test_latin1_encoding_fallback(self):
        content = "def initialize(context):\n    pass\n"
        file_path = self._create_test_file(content, "latin-1")

        result = self.normalizer.normalize(file_path)

        self.assertIsNotNone(result.original_encoding)
        self.assertTrue(result.success)

    def test_encoding_conversion_to_utf8(self):
        content = "# 测试\npass\n"
        file_path = self._create_test_file(content, "gbk")

        result = self.normalizer.normalize(file_path)

        if result.normalized_file:
            with open(result.normalized_file, "r", encoding="utf-8") as f:
                normalized_content = f.read()
            self.assertEqual(result.final_encoding, "utf-8")


class TestIndentationFix(TestTxtStrategyNormalizer):
    """测试缩进修复"""

    def test_tab_indentation_fix(self):
        content = "def initialize(context):\n\tpass\n\tg.x = 1\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        indent_issues = [
            i for i in result.issues if i.issue_type == IssueType.INDENTATION
        ]
        self.assertTrue(len(indent_issues) > 0 or result.can_load)

        self.assertTrue(result.success)
        self.assertIsNotNone(result.normalized_file)

    def test_mixed_tab_space_indentation(self):
        content = "def initialize(context):\n\t    pass\n    \tg.x = 1\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        mixed_issues = [
            i for i in result.issues if i.issue_type == IssueType.TAB_MIXED_SPACE
        ]
        self.assertTrue(len(mixed_issues) > 0)

    def test_non_standard_space_indentation(self):
        content = "def initialize(context):\n   pass\n      g.x = 1\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        indent_issues = [
            i for i in result.issues if i.issue_type == IssueType.INDENTATION
        ]
        self.assertTrue(len(indent_issues) > 0)

    def test_fix_indentation_to_space4(self):
        content = "def test():\n\tprint(1)\n\t\tprint(2)\n"

        fixed = self.normalizer.fix_indentation(content, mode="space4")

        self.assertIn("    print(1)", fixed)
        self.assertIn("        print(2)", fixed)

    def test_fix_indentation_preserves_empty_lines(self):
        content = "def test():\n\tpass\n\n\tpass\n"

        fixed = self.normalizer.fix_indentation(content)

        lines = fixed.split("\n")
        self.assertEqual(lines[2], "")


class TestPython2Compatibility(TestTxtStrategyNormalizer):
    """测试 Python2 兼容问题检测"""

    def test_python2_print_statement_detection(self):
        content = "print 'hello'\nprint 'world'\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        print_issues = [
            i for i in result.issues if i.issue_type == IssueType.PYTHON2_PRINT
        ]
        self.assertTrue(len(print_issues) >= 2)

    def test_python2_print_with_parenthesis_not_flagged(self):
        content = "print('hello')\nprint('world')\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        print_issues = [
            i for i in result.issues if i.issue_type == IssueType.PYTHON2_PRINT
        ]
        self.assertEqual(len(print_issues), 0)

    def test_python2_exception_syntax_detection(self):
        content = "try:\n    pass\nexcept Exception, e:\n    pass\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        exc_issues = [
            i for i in result.issues if i.issue_type == IssueType.PYTHON2_EXCEPTION
        ]
        self.assertTrue(len(exc_issues) > 0)

    def test_python3_exception_syntax_not_flagged(self):
        content = "try:\n    pass\nexcept Exception as e:\n    pass\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        exc_issues = [
            i for i in result.issues if i.issue_type == IssueType.PYTHON2_EXCEPTION
        ]
        self.assertEqual(len(exc_issues), 0)

    def test_fix_python2_print(self):
        content = "print 'hello world'\nprint 123\n"

        fixed = self.normalizer.fix_python2_print(content)

        self.assertIn("print('hello world')", fixed)
        self.assertIn("print(123)", fixed)

    def test_fix_python2_print_preserves_indentation(self):
        content = "def test():\n    print 'hello'\n\tprint 'tab'\n"

        fixed = self.normalizer.fix_python2_print(content)

        self.assertIn("    print('hello')", fixed)


class TestNullByteFix(TestTxtStrategyNormalizer):
    """测试 NULL 字符清除"""

    def test_null_byte_detection(self):
        content = "def test():\n\x00pass\n\x00\x00return 1\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        null_issues = [i for i in result.issues if i.issue_type == IssueType.NULL_BYTE]
        self.assertTrue(len(null_issues) > 0)

    def test_null_byte_fix(self):
        content = "hello\x00world\x00test"

        fixed = self.normalizer.fix_null_bytes(content)

        self.assertEqual(fixed, "helloworldtest")

    def test_null_byte_fix_preserves_content(self):
        content = "def initialize(context):\n\x00pass\n"

        fixed = self.normalizer.fix_null_bytes(content)

        self.assertIn("def initialize", fixed)
        self.assertIn("pass", fixed)


class TestTrailingWhitespace(TestTxtStrategyNormalizer):
    """测试行尾空白清除"""

    def test_trailing_whitespace_detection(self):
        content = "def test():    \n    pass   \n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        trailing_issues = [
            i for i in result.issues if i.issue_type == IssueType.TRAILING_WHITESPACE
        ]
        self.assertTrue(len(trailing_issues) >= 2)

    def test_trailing_whitespace_fix(self):
        content = "line1   \nline2\t\t\nline3    "

        fixed = self.normalizer.fix_trailing_whitespace(content)

        self.assertEqual(fixed, "line1\nline2\nline3")

    def test_trailing_whitespace_preserves_content(self):
        content = "def test():   \n    x = 1    \n"

        fixed = self.normalizer.fix_trailing_whitespace(content)

        self.assertIn("def test():", fixed)
        self.assertIn("x = 1", fixed)


class TestMissingNewline(TestTxtStrategyNormalizer):
    """测试文件末尾换行补充"""

    def test_missing_newline_detection(self):
        content = "def test():\n    pass"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        newline_issues = [
            i for i in result.issues if i.issue_type == IssueType.MISSING_NEWLINE
        ]
        self.assertTrue(len(newline_issues) > 0)

    def test_has_newline_not_flagged(self):
        content = "def test():\n    pass\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        newline_issues = [
            i for i in result.issues if i.issue_type == IssueType.MISSING_NEWLINE
        ]
        self.assertEqual(len(newline_issues), 0)

    def test_fix_missing_newline(self):
        content = "line1\nline2"

        fixed = self.normalizer.fix_missing_newline(content)

        self.assertTrue(fixed.endswith("\n"))

    def test_fix_missing_newline_no_double_newline(self):
        content = "line1\nline2\n"

        fixed = self.normalizer.fix_missing_newline(content)

        self.assertEqual(fixed, content)


class TestSyntaxErrorDetection(TestTxtStrategyNormalizer):
    """测试语法错误检测"""

    def test_valid_syntax_can_load(self):
        content = "def initialize(context):\n    pass\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        self.assertTrue(result.can_load)
        self.assertIsNone(result.load_error)

    def test_syntax_error_detection(self):
        content = "def test()\n    pass\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        self.assertFalse(result.can_load)
        self.assertIsNotNone(result.load_error)

    def test_syntax_error_with_invalid_indent(self):
        content = "def test():\npass\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        syntax_issues = [
            i for i in result.issues if i.issue_type == IssueType.SYNTAX_ERROR
        ]
        self.assertTrue(len(syntax_issues) > 0 or not result.can_load)

    def test_detect_syntax_issues_returns_list(self):
        content = "valid content\n"

        issues = self.normalizer.detect_syntax_issues(content)

        self.assertIsInstance(issues, list)

    def test_detect_syntax_issues_with_null_byte(self):
        content = "def test():\n\x00pass"

        issues = self.normalizer.detect_syntax_issues(content)

        null_issues = [i for i in issues if i.issue_type == IssueType.NULL_BYTE]
        self.assertTrue(len(null_issues) > 0)


class TestNormalizationResult(TestTxtStrategyNormalizer):
    """测试标准化结果"""

    def test_result_success_flag(self):
        content = "def initialize(context):\n    pass\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        self.assertTrue(result.success)

    def test_result_normalized_file_created(self):
        content = "def test():\n    pass\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        self.assertIsNotNone(result.normalized_file)
        self.assertTrue(os.path.exists(result.normalized_file))

    def test_result_hash_calculated(self):
        content = "def test():\n    pass\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        self.assertIsNotNone(result.original_hash)
        self.assertIsNotNone(result.normalized_hash)

    def test_result_lines_counted(self):
        content = "line1\nline2\nline3\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        self.assertEqual(result.original_lines, 4)

    def test_result_diff_summary(self):
        content = "def test():\n    pass\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        self.assertIn("total_issues", result.diff_summary)
        self.assertIn("fixed_count", result.diff_summary)


class TestBatchNormalize(TestTxtStrategyNormalizer):
    """测试批量标准化"""

    def test_batch_normalize_multiple_files(self):
        files = []
        for i in range(3):
            content = f"def test{i}():\n    pass\n"
            file_path = self._create_test_file(content, filename=f"test{i}.txt")
            files.append(file_path)

        results = self.normalizer.batch_normalize(files)

        self.assertEqual(len(results), 3)
        for file_path in files:
            self.assertIn(file_path, results)
            self.assertTrue(results[file_path].success)

    def test_batch_normalize_with_output_dir(self):
        output_dir = os.path.join(self.temp_dir, "output")
        os.makedirs(output_dir, exist_ok=True)

        files = []
        for i in range(2):
            content = f"def test{i}():\n    pass\n"
            file_path = self._create_test_file(content, filename=f"test{i}.txt")
            files.append(file_path)

        results = self.normalizer.batch_normalize(files, output_dir)

        for file_path, result in results.items():
            if result.normalized_file:
                self.assertTrue(os.path.exists(result.normalized_file))

    def test_batch_normalize_empty_list(self):
        results = self.normalizer.batch_normalize([])

        self.assertEqual(len(results), 0)


class TestIssueDetection(TestTxtStrategyNormalizer):
    """测试问题检测"""

    def test_detect_indentation_issues_returns_list(self):
        content = "def test():\n\tpass\n"

        issues = self.normalizer.detect_indentation_issues(content)

        self.assertIsInstance(issues, list)

    def test_detect_python2_issues_returns_list(self):
        content = "print 'hello'\n"

        issues = self.normalizer.detect_python2_issues(content)

        self.assertIsInstance(issues, list)
        self.assertTrue(len(issues) > 0)

    def test_issue_has_correct_type(self):
        content = "print 'hello'\n"

        issues = self.normalizer.detect_python2_issues(content)

        if issues:
            self.assertEqual(issues[0].issue_type, IssueType.PYTHON2_PRINT)

    def test_issue_has_correct_severity(self):
        content = "print 'hello'\n"

        issues = self.normalizer.detect_python2_issues(content)

        if issues:
            self.assertEqual(issues[0].severity, Severity.ERROR)

    def test_issue_auto_fixable_flag(self):
        content = "print 'hello'\n"

        issues = self.normalizer.detect_python2_issues(content)

        if issues:
            self.assertTrue(issues[0].auto_fixable)

    def test_issue_is_dangerous_flag(self):
        content = "try:\n    pass\nexcept E, e:\n    pass\n"

        issues = self.normalizer.detect_python2_issues(content)

        exc_issues = [i for i in issues if i.issue_type == IssueType.PYTHON2_EXCEPTION]
        if exc_issues:
            self.assertTrue(exc_issues[0].is_dangerous)


class TestReadWithEncodingFallback(TestTxtStrategyNormalizer):
    """测试多编码读取"""

    def test_read_utf8_file(self):
        content = "utf-8 content\n"
        file_path = self._create_test_file(content, "utf-8")

        read_content, encoding = self.normalizer.read_with_encoding_fallback(file_path)

        self.assertEqual(read_content, content)
        self.assertIsNotNone(encoding)

    def test_read_nonexistent_file_raises(self):
        file_path = os.path.join(self.temp_dir, "nonexistent.txt")

        try:
            self.normalizer.read_with_encoding_fallback(file_path)
        except FileNotFoundError:
            pass
        else:
            self.assertTrue(os.path.exists(file_path))


class TestFileNotExist(TestTxtStrategyNormalizer):
    """测试文件不存在情况"""

    def test_normalize_nonexistent_file(self):
        file_path = os.path.join(self.temp_dir, "nonexistent.txt")

        result = self.normalizer.normalize(file_path)

        self.assertFalse(result.success)
        self.assertEqual(result.message, "文件不存在")

    def test_normalize_nonexistent_file_no_normalized_file(self):
        file_path = os.path.join(self.temp_dir, "nonexistent.txt")

        result = self.normalizer.normalize(file_path)

        self.assertIsNone(result.normalized_file)


class TestAutoFixDisabled(TestTxtStrategyNormalizer):
    """测试禁用自动修复"""

    def test_auto_fix_disabled_preserves_content(self):
        normalizer = TxtStrategyNormalizer(cache_dir=self.temp_dir, auto_fix_safe=False)

        content = "def test():\n    pass   \n"
        file_path = self._create_test_file(content)

        result = normalizer.normalize(file_path)

        trailing_issues = [
            i
            for i in result.unfixed_issues
            if i.issue_type == IssueType.TRAILING_WHITESPACE
        ]
        self.assertTrue(len(trailing_issues) >= 1)


class TestConvenienceFunctions(TestTxtStrategyNormalizer):
    """测试便捷函数"""

    def test_normalize_strategy_file_function(self):
        normalize_strategy_file = txt_norm_module.normalize_strategy_file

        content = "def test():\n    pass\n"
        file_path = self._create_test_file(content)

        result = normalize_strategy_file(file_path)

        self.assertTrue(result.success)

    def test_batch_normalize_strategies_function(self):
        batch_normalize_strategies = txt_norm_module.batch_normalize_strategies

        files = []
        for i in range(2):
            content = f"def test{i}():\n    pass\n"
            file_path = self._create_test_file(content, filename=f"test{i}.txt")
            files.append(file_path)

        results = batch_normalize_strategies(files)

        self.assertEqual(len(results), 2)


class TestGenerateReport(TestTxtStrategyNormalizer):
    """测试报告生成"""

    def test_generate_report_creates_file(self):
        content = "def test():\n    pass\n"
        file_path = self._create_test_file(content)

        results = self.normalizer.batch_normalize([file_path])

        report_path = os.path.join(self.temp_dir, "report.md")
        self.normalizer.generate_report(results, report_path)

        self.assertTrue(os.path.exists(report_path))

    def test_generate_report_has_header(self):
        content = "def test():\n    pass\n"
        file_path = self._create_test_file(content)

        results = self.normalizer.batch_normalize([file_path])

        report_path = os.path.join(self.temp_dir, "report.md")
        self.normalizer.generate_report(results, report_path)

        with open(report_path, "r") as f:
            content = f.read()

        self.assertIn("# Task 37 Result", content)

    def test_generate_report_has_statistics(self):
        content = "def test():\n    pass\n"
        file_path = self._create_test_file(content)

        results = self.normalizer.batch_normalize([file_path])

        report_path = os.path.join(self.temp_dir, "report.md")
        self.normalizer.generate_report(results, report_path)

        with open(report_path, "r") as f:
            content = f.read()

        self.assertIn("标准化统计", content)


class TestEdgeCases(TestTxtStrategyNormalizer):
    """测试边缘情况"""

    def test_empty_file(self):
        file_path = self._create_test_file("")

        result = self.normalizer.normalize(file_path)

        self.assertIsNotNone(result)

    def test_whitespace_only_file(self):
        file_path = self._create_test_file("   \n\t\n   \n")

        result = self.normalizer.normalize(file_path)

        self.assertIsNotNone(result)

    def test_single_line_file(self):
        file_path = self._create_test_file("pass")

        result = self.normalizer.normalize(file_path)

        self.assertIsNotNone(result)

    def test_large_file(self):
        lines = ["    pass"] * 1000
        content = "def test():\n" + "\n".join(lines)
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        self.assertIsNotNone(result)
        self.assertEqual(result.original_lines, 1001)

    def test_unicode_content(self):
        content = "# 中文注释\ndef 测试():\n    pass\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        self.assertIsNotNone(result)

    def test_special_characters(self):
        content = "# Special: !@#$%^&*()\ndef test():\n    pass\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        self.assertTrue(result.success)


class TestIndentationEdgeCases(TestTxtStrategyNormalizer):
    """测试缩进边缘情况"""

    def test_no_indentation(self):
        content = "pass\npass\n"
        file_path = self._create_test_file(content)

        issues = self.normalizer.detect_indentation_issues(content)

        self.assertEqual(len(issues), 0)

    def test_deep_indentation(self):
        content = "def test():\n    if True:\n        if True:\n            if True:\n                pass\n"
        file_path = self._create_test_file(content)

        result = self.normalizer.normalize(file_path)

        self.assertTrue(result.can_load)

    def test_inconsistent_indentation_levels(self):
        content = "def test():\n  pass\n    pass\n  pass\n"
        file_path = self._create_test_file(content)

        issues = self.normalizer.detect_indentation_issues(content)

        self.assertTrue(len(issues) > 0)


class TestPython2EdgeCases(TestTxtStrategyNormalizer):
    """测试 Python2 兼容边缘情况"""

    def test_print_with_complex_expression(self):
        content = "print 'hello', 'world', 123\n"

        fixed = self.normalizer.fix_python2_print(content)

        self.assertIn("print(", fixed)

    def test_print_in_nested_function(self):
        content = "def outer():\n    def inner():\n        print 'hello'\n"

        fixed = self.normalizer.fix_python2_print(content)

        self.assertIn("print('hello')", fixed)

    def test_print_with_format_spec(self):
        content = "print '%s %d' % (name, age)\n"

        fixed = self.normalizer.fix_python2_print(content)

        self.assertIn("print(", fixed)


if __name__ == "__main__":
    unittest.main(verbosity=2)

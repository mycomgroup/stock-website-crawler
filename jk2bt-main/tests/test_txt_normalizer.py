"""
TXT策略文本标准化测试

测试覆盖范围:
1. 编码检测和多编码读取
2. TAB缩进检测和修复
3. TAB/空格混用检测
4. Python2 print语句检测和修复
5. Python2 except语法检测和修复
6. 单文件标准化流程
7. 批量标准化流程
8. 边界情况和错误处理
9. 缓存机制
10. 结果报告生成
"""

import os
import sys
import tempfile
import shutil
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.strategy.txt_normalizer import (
    TxtNormalizer,
    NormalizationResult,
    NormalizationIssue,
    normalize_strategy_text,
)


class TestEncodingDetection(unittest.TestCase):
    """编码检测测试"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="txt_norm_test_")
        self.normalizer = TxtNormalizer(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_utf8_detection(self):
        """UTF-8编码检测"""
        test_file = os.path.join(self.test_dir, "test_utf8.txt")
        content = "def initialize(context):\n    print('UTF-8测试')"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)

        encoding, success = self.normalizer.detect_encoding(test_file)
        self.assertEqual(encoding, "utf-8")
        self.assertTrue(success)

    def test_gbk_detection(self):
        """GBK编码检测"""
        test_file = os.path.join(self.test_dir, "test_gbk.txt")
        content = "def initialize(context):\n    print('GBK测试')"
        with open(test_file, "w", encoding="gbk") as f:
            f.write(content)

        encoding, success = self.normalizer.detect_encoding(test_file)
        self.assertEqual(encoding, "gbk")
        self.assertTrue(success)

    def test_gb2312_detection(self):
        """GB2312编码检测"""
        test_file = os.path.join(self.test_dir, "test_gb2312.txt")
        content = "def initialize(context):\n    # 中文注释"
        with open(test_file, "w", encoding="gb2312") as f:
            f.write(content)

        encoding, success = self.normalizer.detect_encoding(test_file)
        self.assertIn(encoding, ["gb2312", "gbk"])
        self.assertTrue(success)

    def test_latin1_detection(self):
        """Latin-1编码检测"""
        test_file = os.path.join(self.test_dir, "test_latin1.txt")
        content = "def initialize(context):\n    # Latin-1: \xe9\xe0\xe7"
        with open(test_file, "w", encoding="latin-1") as f:
            f.write(content)

        encoding, success = self.normalizer.detect_encoding(test_file)
        self.assertIn(encoding, ["latin-1", "utf-8"])
        self.assertTrue(success)

    def test_encoding_fallback(self):
        """编码自动回退"""
        test_file = os.path.join(self.test_dir, "test_fallback.txt")
        content = "中文内容\nprint('test')"
        with open(test_file, "w", encoding="gbk") as f:
            f.write(content)

        content_read, encoding = self.normalizer.read_with_encoding(test_file)
        self.assertIsNotNone(content_read)
        self.assertIn(encoding, ["gbk", "gb2312"])
        self.assertIn("中文内容", content_read)

    def test_null_byte_removal(self):
        """空字节清理"""
        test_file = os.path.join(self.test_dir, "test_null.txt")
        content = "def test():\n\x00print('test')\x00"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)

        content_read, encoding = self.normalizer.read_with_encoding(test_file)
        self.assertIsNotNone(content_read)
        self.assertNotIn("\x00", content_read)

    def test_unknown_encoding_file(self):
        """特殊编码文件处理"""
        test_file = os.path.join(self.test_dir, "test_binary.txt")
        with open(test_file, "wb") as f:
            f.write(b"\xff\xfe\xff\xff")

        content, encoding = self.normalizer.read_with_encoding(test_file)
        self.assertEqual(encoding, "latin-1")


class TestIndentationDetection(unittest.TestCase):
    """缩进检测测试"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="txt_norm_indent_")
        self.normalizer = TxtNormalizer(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_tab_indent_detection(self):
        """TAB缩进检测"""
        content = (
            "def initialize(context):\n\tprint('tab indent')\n\t\tlog.info('nested')"
        )
        has_tab, tab_lines = self.normalizer.detect_tab_indent(content)
        self.assertTrue(has_tab)
        self.assertEqual(tab_lines, 2)

    def test_space_indent_detection(self):
        """空格缩进检测"""
        content = "def initialize(context):\n    print('space indent')\n        log.info('nested')"
        has_tab, tab_lines = self.normalizer.detect_tab_indent(content)
        self.assertFalse(has_tab)
        self.assertEqual(tab_lines, 0)

    def test_mixed_indent_detection(self):
        """TAB/空格混用检测"""
        content = (
            "def initialize(context):\n\t    print('mixed')\n\t\t    log.info('nested')"
        )
        has_mixed, mixed_lines = self.normalizer.detect_mixed_indent(content)
        self.assertTrue(has_mixed)
        self.assertEqual(mixed_lines, 2)

    def test_tab_fix(self):
        """TAB缩进修复"""
        content = "def test():\n\tline1\n\t\tline2"
        fixed = self.normalizer.fix_tab_indent(content, spaces_per_tab=4)

        self.assertNotIn("\t", fixed)
        self.assertIn("    line1", fixed)
        self.assertIn("        line2", fixed)

    def test_tab_fix_preserves_content(self):
        """TAB修复保留内容"""
        content = "def initialize(context):\n\tg.stock = '000001'\n\tprint(g.stock)"
        fixed = self.normalizer.fix_tab_indent(content)

        self.assertIn("g.stock = '000001'", fixed)
        self.assertIn("print(g.stock)", fixed)

    def test_no_tab_content(self):
        """无TAB内容保持不变"""
        content = "def test():\n    line1\n        line2"
        fixed = self.normalizer.fix_tab_indent(content)
        self.assertEqual(content, fixed)


class TestPython2Compatibility(unittest.TestCase):
    """Python2兼容性测试"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="txt_norm_py2_")
        self.normalizer = TxtNormalizer(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_print_statement_detection(self):
        """Python2 print语句检测"""
        content = "def test():\n    print 'hello'\n    print 'world'"
        has_py2_print, count, lines = self.normalizer.detect_python2_print(content)

        self.assertTrue(has_py2_print)
        self.assertEqual(count, 2)
        self.assertEqual(lines, [2, 3])

    def test_print_function_not_detected(self):
        """Python3 print函数不被误检测"""
        content = "def test():\n    print('hello')\n    print('world')"
        has_py2_print, count, lines = self.normalizer.detect_python2_print(content)

        self.assertFalse(has_py2_print)
        self.assertEqual(count, 0)

    def test_print_simple_fix(self):
        """简单print语句修复"""
        content = "print 'hello world'"
        fixed = self.normalizer.fix_python2_print(content)

        self.assertIn("print('hello world')", fixed)

    def test_print_with_comma_fix(self):
        """多参数print语句修复"""
        content = "print 'count:', g.count"
        fixed = self.normalizer.fix_python2_print(content)

        self.assertIn("print(", fixed)
        self.assertIn("g.count", fixed)

    def test_print_empty_fix(self):
        """print语句修复"""
        content = "def test():\n    print\n    pass"
        fixed = self.normalizer.fix_python2_print(content)

        self.assertIn("def test():", fixed)

    def test_print_preserves_indent(self):
        """print修复保留缩进"""
        content = "def test():\n    print 'hello'"
        fixed = self.normalizer.fix_python2_print(content)

        self.assertIn("    print('hello')", fixed)

    def test_print_string_literal_preserved(self):
        """字符串字面print保留引号"""
        content = "print 'message'"
        fixed = self.normalizer.fix_python2_print(content)

        self.assertIn("print('message')", fixed)

    def test_except_syntax_detection(self):
        """Python2 except语法检测"""
        content = "try:\n    pass\nexcept Exception, e:\n    print e"
        has_py2_except, count, lines = self.normalizer.detect_python2_except(content)

        self.assertTrue(has_py2_except)
        self.assertEqual(count, 1)
        self.assertEqual(lines, [3])

    def test_except_syntax_fix(self):
        """except语法修复"""
        content = "except ValueError, e:\n    log.info(e)"
        fixed = self.normalizer.fix_python2_except(content)

        self.assertIn("except ValueError as e:", fixed)

    def test_except_preserves_indent(self):
        """except修复保留缩进"""
        content = "try:\n    pass\nexcept Exception, e:\n    pass"
        fixed = self.normalizer.fix_python2_except(content)

        self.assertIn("except Exception as e:", fixed)


class TestFileNormalization(unittest.TestCase):
    """文件标准化测试"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="txt_norm_file_")
        self.normalizer = TxtNormalizer(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_normalize_valid_file(self):
        """有效文件标准化"""
        test_file = os.path.join(self.test_dir, "valid_strategy.txt")
        content = "def initialize(context):\n    print('test')"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)

        result = self.normalizer.normalize_file(test_file)

        self.assertTrue(result.success)
        self.assertEqual(result.detected_encoding, "utf-8")
        self.assertEqual(len(result.issues_found), 0)

    def test_normalize_py2_print_file(self):
        """Python2 print文件标准化"""
        test_file = os.path.join(self.test_dir, "py2_print.txt")
        content = "def initialize(context):\n    print 'hello'"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)

        result = self.normalizer.normalize_file(test_file)

        self.assertTrue(result.success)
        self.assertIn(NormalizationIssue.PRINT_STMT, result.issues_found)
        self.assertIn(NormalizationIssue.PRINT_STMT, result.issues_fixed)
        self.assertIsNotNone(result.normalized_path)

    def test_normalize_tab_indent_file(self):
        """TAB缩进文件标准化"""
        test_file = os.path.join(self.test_dir, "tab_indent.txt")
        content = "def initialize(context):\n\tprint('tab')"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)

        result = self.normalizer.normalize_file(test_file)

        self.assertTrue(result.success)
        self.assertIn(NormalizationIssue.TAB_INDENT, result.issues_found)
        self.assertIn(NormalizationIssue.TAB_INDENT, result.issues_fixed)

    def test_normalize_multiple_issues(self):
        """多问题文件标准化"""
        test_file = os.path.join(self.test_dir, "multi_issues.txt")
        content = "def initialize(context):\n\tprint 'hello'\n\texcept Exception, e:\n\t\tprint e"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)

        result = self.normalizer.normalize_file(test_file)

        self.assertTrue(result.success)
        self.assertTrue(len(result.issues_found) >= 2)
        self.assertTrue(len(result.issues_fixed) >= 2)

    def test_normalize_nonexistent_file(self):
        """不存在文件处理"""
        test_file = os.path.join(self.test_dir, "nonexistent.txt")

        result = self.normalizer.normalize_file(test_file)

        self.assertFalse(result.success)
        self.assertEqual(result.error_message, "文件不存在")

    def test_normalize_output_file_created(self):
        """标准化文件输出创建"""
        test_file = os.path.join(self.test_dir, "source.txt")
        content = "def initialize(context):\n\tprint 'test'"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)

        result = self.normalizer.normalize_file(test_file)

        self.assertTrue(result.success)
        self.assertTrue(os.path.exists(result.normalized_path))

    def test_normalize_gbk_file(self):
        """GBK编码文件标准化"""
        test_file = os.path.join(self.test_dir, "gbk_file.txt")
        content = "def initialize(context):\n    # 中文注释"
        with open(test_file, "w", encoding="gbk") as f:
            f.write(content)

        result = self.normalizer.normalize_file(test_file)

        self.assertTrue(result.success)
        self.assertIn(result.detected_encoding, ["gbk", "gb2312"])

    def test_normalize_preserves_original(self):
        """标准化保留原文件"""
        test_file = os.path.join(self.test_dir, "original.txt")
        original_content = "def initialize(context):\n\tprint 'test'"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(original_content)

        result = self.normalizer.normalize_file(test_file, keep_original=True)

        with open(test_file, "r", encoding="utf-8") as f:
            content_after = f.read()

        self.assertEqual(original_content, content_after)

    def test_normalize_warnings_generated(self):
        """警告信息生成"""
        test_file = os.path.join(self.test_dir, "warning.txt")
        content = "def test():\n    print 'hello'"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)

        result = self.normalizer.normalize_file(test_file)

        self.assertTrue(len(result.warnings) > 0)


class TestBatchNormalization(unittest.TestCase):
    """批量标准化测试"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="txt_norm_batch_")
        self.source_dir = tempfile.mkdtemp(prefix="txt_batch_source_")
        self.normalizer = TxtNormalizer(self.test_dir)

        for i in range(5):
            test_file = os.path.join(self.source_dir, f"test_{i}.txt")
            content = f"def initialize(context):\n\tprint 'test{i}'"
            with open(test_file, "w", encoding="utf-8") as f:
                f.write(content)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists(self.source_dir):
            shutil.rmtree(self.source_dir)

    def test_batch_normalize(self):
        """批量标准化"""
        results = self.normalizer.normalize_directory(self.source_dir)

        self.assertEqual(len(results["all"]), 5)
        self.assertEqual(len(results["success"]), 5)
        self.assertEqual(len(results["failed"]), 0)

    def test_batch_normalize_limit(self):
        """批量标准化限制数量"""
        results = self.normalizer.normalize_directory(self.source_dir, limit=3)

        self.assertEqual(len(results["all"]), 3)

    def test_batch_normalize_pattern(self):
        """批量标准化匹配模式"""
        results = self.normalizer.normalize_directory(
            self.source_dir, pattern="test_*.txt"
        )

        self.assertEqual(len(results["all"]), 5)

    def test_batch_normalize_no_changes(self):
        """批量标准化无修改文件"""
        clean_file = os.path.join(self.source_dir, "clean.txt")
        content = "def initialize(context):\n    print('clean')"
        with open(clean_file, "w", encoding="utf-8") as f:
            f.write(content)

        results = self.normalizer.normalize_directory(self.source_dir)

        self.assertTrue(len(results["no_changes"]) > 0)

    def test_batch_print_summary(self):
        """批量标准化摘要输出"""
        results = self.normalizer.normalize_directory(self.source_dir)

        self.normalizer.print_summary(results)

        self.assertIn("success", results)
        self.assertIn("failed", results)


class TestNormalizationResult(unittest.TestCase):
    """标准化结果测试"""

    def test_result_dataclass(self):
        """结果数据结构"""
        result = NormalizationResult(
            original_path="/path/to/file.txt",
            normalized_path="/path/to/normalized.txt",
            detected_encoding="utf-8",
            original_size=100,
            normalized_size=120,
            success=True,
        )

        self.assertEqual(result.original_path, "/path/to/file.txt")
        self.assertEqual(result.detected_encoding, "utf-8")
        self.assertTrue(result.success)

    def test_result_default_values(self):
        """结果默认值"""
        result = NormalizationResult(
            original_path="/path/to/file.txt",
            normalized_path=None,
            detected_encoding="unknown",
            original_size=0,
            normalized_size=0,
            success=False,
        )

        self.assertEqual(len(result.issues_found), 0)
        self.assertEqual(len(result.issues_fixed), 0)
        self.assertEqual(len(result.warnings), 0)

    def test_result_issues_list(self):
        """问题列表"""
        result = NormalizationResult(
            original_path="/path",
            normalized_path=None,
            detected_encoding="utf-8",
            original_size=100,
            normalized_size=100,
            success=True,
        )

        result.issues_found.append(NormalizationIssue.TAB_INDENT)
        result.issues_fixed.append(NormalizationIssue.TAB_INDENT)

        self.assertIn(NormalizationIssue.TAB_INDENT, result.issues_found)


class TestCacheMechanism(unittest.TestCase):
    """缓存机制测试"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="txt_norm_cache_")
        self.normalizer = TxtNormalizer(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_cache_hit(self):
        """缓存命中"""
        test_file = os.path.join(self.test_dir, "cache_test.txt")
        content = "def test():\n    print('test')"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)

        result1 = self.normalizer.normalize_file(test_file)
        result2 = self.normalizer.normalize_file(test_file)

        self.assertEqual(result1.original_path, result2.original_path)
        self.assertEqual(result1.detected_encoding, result2.detected_encoding)

    def test_cache_different_files(self):
        """不同文件不同缓存"""
        test_file1 = os.path.join(self.test_dir, "test1.txt")
        test_file2 = os.path.join(self.test_dir, "test2.txt")

        with open(test_file1, "w") as f:
            f.write("content1")
        with open(test_file2, "w") as f:
            f.write("content2")

        result1 = self.normalizer.normalize_file(test_file1)
        result2 = self.normalizer.normalize_file(test_file2)

        self.assertNotEqual(result1.original_path, result2.original_path)


class TestNormalizationIssueEnum(unittest.TestCase):
    """问题类型枚举测试"""

    def test_issue_enum_values(self):
        """枚举值测试"""
        self.assertEqual(NormalizationIssue.ENCODING.value, "encoding")
        self.assertEqual(NormalizationIssue.TAB_INDENT.value, "tab_indent")
        self.assertEqual(NormalizationIssue.PRINT_STMT.value, "print_statement")
        self.assertEqual(NormalizationIssue.EXCEPT_SYNTAX.value, "except_syntax")

    def test_issue_enum_members(self):
        """枚举成员数量"""
        issues = list(NormalizationIssue)
        self.assertTrue(len(issues) >= 6)


class TestConvenienceFunction(unittest.TestCase):
    """便捷函数测试"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="txt_norm_func_")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_normalize_strategy_text_function(self):
        """便捷函数测试"""
        test_file = os.path.join(self.test_dir, "test.txt")
        content = "def initialize(context):\n\tprint 'test'"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)

        norm_path, result = normalize_strategy_text(test_file, self.test_dir)

        self.assertIsNotNone(norm_path)
        self.assertTrue(result.success)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="txt_norm_edge_")
        self.normalizer = TxtNormalizer(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_empty_file(self):
        """空文件处理"""
        test_file = os.path.join(self.test_dir, "empty.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("")

        content, encoding = self.normalizer.read_with_encoding(test_file)
        self.assertEqual(content, "")

    def test_only_comments_file(self):
        """纯注释文件"""
        test_file = os.path.join(self.test_dir, "comments.txt")
        content = "# 这只是注释\n# 没有代码"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)

        result = self.normalizer.normalize_file(test_file)
        self.assertTrue(result.success)

    def test_large_file(self):
        """大文件处理"""
        test_file = os.path.join(self.test_dir, "large.txt")
        lines = ["print 'line{}'".format(i) for i in range(1000)]
        content = "\n".join(lines)
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)

        result = self.normalizer.normalize_file(test_file)
        self.assertTrue(result.success)

    def test_unicode_special_chars(self):
        """特殊Unicode字符"""
        test_file = os.path.join(self.test_dir, "unicode.txt")
        content = "def test():\n    print('特殊字符：★●○')"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)

        content_read, encoding = self.normalizer.read_with_encoding(test_file)
        self.assertIn("★", content_read)

    def test_windows_line_endings(self):
        """Windows换行符"""
        test_file = os.path.join(self.test_dir, "windows.txt")
        content = "def test():\r\n    print('test')\r\n"
        with open(test_file, "w", encoding="utf-8", newline="") as f:
            f.write(content)

        content_read, encoding = self.normalizer.read_with_encoding(test_file)
        self.assertIsNotNone(content_read)

    def test_indentation_with_continuation(self):
        """续行缩进"""
        content = "def test():\n    result = very_long_line + \\\n        continuation"
        has_tab, tab_lines = self.normalizer.detect_tab_indent(content)
        self.assertFalse(has_tab)


class TestIntegration(unittest.TestCase):
    """集成测试"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="txt_norm_integration_")
        self.normalizer = TxtNormalizer(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_full_normalization_workflow(self):
        """完整标准化流程"""
        test_file = os.path.join(self.test_dir, "full_workflow.txt")
        original = """def initialize(context):
\tg.count = 0
\tprint '初始化'
\ttry:
\t\tpass
\texcept Exception, e:
\t\tprint e"""

        with open(test_file, "w", encoding="utf-8") as f:
            f.write(original)

        result = self.normalizer.normalize_file(test_file)

        self.assertTrue(result.success)
        self.assertIn(NormalizationIssue.TAB_INDENT, result.issues_fixed)
        self.assertIn(NormalizationIssue.PRINT_STMT, result.issues_fixed)
        self.assertIn(NormalizationIssue.EXCEPT_SYNTAX, result.issues_fixed)

        if result.normalized_path:
            with open(result.normalized_path, "r", encoding="utf-8") as f:
                normalized = f.read()

            self.assertIn("print(", normalized)
            self.assertIn("except Exception as e:", normalized)
            self.assertNotIn("\t", normalized)

    def test_real_strategy_sample(self):
        """真实策略样本"""
        test_file = os.path.join(self.test_dir, "real_strategy.txt")
        real_strategy = """def initialize(context):
\tset_benchmark('000300.XSHG')
\tg.stocks = ['000001.XSHE']
\tprint '策略初始化'

def handle_data(context, data):
\tfor stock in g.stocks:
\t\torder(stock, 100)
\t\tprint '买入:', stock"""

        with open(test_file, "w", encoding="utf-8") as f:
            f.write(real_strategy)

        result = self.normalizer.normalize_file(test_file)

        self.assertTrue(result.success)


if __name__ == "__main__":
    unittest.main(verbosity=2)

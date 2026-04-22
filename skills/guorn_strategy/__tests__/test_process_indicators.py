import json
import os
import tempfile
from unittest import mock

import pytest

from skills.guorn_strategy.process_indicators import process_meta, to_middle_name


class TestToMiddleName:
    """Test the to_middle_name helper function."""

    def test_standard_format(self):
        """Test standard '0.M.Category_Name.0' format."""
        assert to_middle_name("0.M.行情数据.0") == "行情数据"
        assert to_middle_name("0.M.财务指标.0") == "财务指标"
        assert to_middle_name("0.M.Category.0") == "Category"

    def test_not_starting_with_zero_dot(self):
        """Test ID not starting with '0.'."""
        assert to_middle_name("1.M.Category.0") == "1.M.Category.0"
        assert to_middle_name("Category") == "Category"

    def test_empty_string(self):
        """Test empty string input."""
        assert to_middle_name("") == ""

    def test_none_input(self):
        """Test None input handling."""
        assert to_middle_name(None) == ""

    def test_insufficient_parts(self):
        """Test ID with insufficient parts after split."""
        assert to_middle_name("0.") == "0."
        assert to_middle_name("0.M") == "0.M"
        assert to_middle_name("0.M.") == ""

    def test_exactly_three_parts(self):
        """Test ID with exactly three parts."""
        assert to_middle_name("0.M.Test") == "Test"

    def test_more_than_four_parts(self):
        """Test ID with more than four parts."""
        assert to_middle_name("0.M.Category.Name.0.Extra") == "Category"

    def test_with_dots_in_middle_name(self):
        """Test ID with dots in the middle name part."""
        assert to_middle_name("0.M.Category.SubCategory.0") == "Category"


class TestProcessMetaBasic:
    """Basic tests for process_meta function."""

    @pytest.fixture
    def sample_meta_data(self):
        """Create sample meta data for testing."""
        return {
            "status": "ok",
            "data": {
                "function": {
                    "measures": [
                        {
                            "name": "日期回溯函数",
                            "values": [
                                {
                                    "name": "Ref",
                                    "expr": "Ref(,)",
                                    "desc": "取得指标几个交易日前的值。<br/>例子说明。",
                                },
                                {
                                    "name": "BarRef",
                                    "expr": "BarRef(,)",
                                    "desc": "取得指标几根日K线前的值。\n换行测试。",
                                },
                            ],
                        },
                        {
                            "name": "统计函数",
                            "values": [
                                {"name": "MA", "expr": "MA(,)|extra", "desc": "计算平均值"}
                            ],
                        },
                    ]
                },
                "first_measures": [
                    {
                        "name": "行情指标",
                        "values": [
                            {
                                "name": "收盘价",
                                "id": "0.M.行情数据.0",
                                "desc": "每日收盘价",
                                "expr": "close",
                            },
                            {
                                "name": "成交量",
                                "id": "0.M.行情数据.0",
                                "desc": "每日成交量<br/>换行\n测试",
                                "expr": "volume",
                            },
                        ],
                    }
                ],
            }
        }

    def test_process_meta_with_custom_paths(self, sample_meta_data):
        """Test process_meta with custom input and output paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(sample_meta_data, f, ensure_ascii=False)

            result = process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            assert os.path.exists(output_md)
            assert os.path.exists(output_json)

            assert len(result["functions"]) == 3
            assert len(result["indicators"]) == 2

            assert result["functions"][0]["name"] == "Ref"
            assert result["functions"][1]["name"] == "BarRef"
            assert result["functions"][2]["name"] == "MA"

            assert result["indicators"][0]["name"] == "收盘价"
            assert result["indicators"][0]["middle_name"] == "行情数据"

    def test_process_meta_creates_valid_markdown(self, sample_meta_data):
        """Test that generated markdown has correct format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(sample_meta_data, f, ensure_ascii=False)

            process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            with open(output_md, "r", encoding="utf-8") as f:
                md_content = f.read()

            assert "# 果仁网指标与函数全量手册" in md_content
            assert "## 1. 系统函数 (Functions)" in md_content
            assert "## 2. 常用指标 (Standard Indicators)" in md_content
            assert "### 日期回溯函数" in md_content
            assert "### 行情指标" in md_content
            assert "| Ref | `Ref(,)` |" in md_content
            assert "| 收盘价 | `行情数据` |" in md_content

    def test_process_meta_escapes_pipe_characters(self, sample_meta_data):
        """Test that pipe characters in expressions are escaped."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(sample_meta_data, f, ensure_ascii=False)

            process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            with open(output_md, "r", encoding="utf-8") as f:
                md_content = f.read()

            assert "`MA(,)\\|extra`" in md_content

    def test_process_meta_cleans_html_tags(self, sample_meta_data):
        """Test that HTML <br/> tags are replaced with spaces."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(sample_meta_data, f, ensure_ascii=False)

            result = process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            assert "<br/>" not in result["functions"][0]["desc"]
            assert " " in result["functions"][0]["desc"]

    def test_process_meta_cleans_newlines(self, sample_meta_data):
        """Test that newlines in descriptions are replaced with spaces."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(sample_meta_data, f, ensure_ascii=False)

            result = process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            assert "\n" not in result["functions"][1]["desc"]
            assert " " in result["functions"][1]["desc"]


class TestProcessMetaEdgeCases:
    """Test edge cases for process_meta function."""

    def test_process_meta_empty_data(self):
        """Test processing with empty data."""
        empty_data = {"data": {}}

        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(empty_data, f)

            result = process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            assert result["functions"] == []
            assert result["indicators"] == []

    def test_process_meta_missing_function_data(self):
        """Test processing with missing function data."""
        data = {
            "data": {
                "first_measures": [
                    {
                        "name": "行情指标",
                        "values": [
                            {
                                "name": "收盘价",
                                "id": "0.M.行情数据.0",
                                "desc": "每日收盘价",
                            }
                        ],
                    }
                ]
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

            result = process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            assert result["functions"] == []
            assert len(result["indicators"]) == 1

    def test_process_meta_missing_first_measures(self):
        """Test processing with missing first_measures data."""
        data = {
            "data": {
                "function": {
                    "measures": [
                        {
                            "name": "测试函数",
                            "values": [{"name": "Test", "expr": "Test()", "desc": "测试"}],
                        }
                    ]
                }
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

            result = process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            assert len(result["functions"]) == 1
            assert result["indicators"] == []

    def test_process_meta_empty_values_list(self):
        """Test handling of empty values list."""
        data = {
            "data": {
                "function": {"measures": [{"name": "空分类", "values": []}]},
                "first_measures": [],
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(data, f)

            result = process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            assert result["functions"] == []

    def test_process_meta_missing_values_key(self):
        """Test handling of blocks without values key."""
        data = {
            "data": {
                "function": {"measures": [{"name": "无values分类"}]},
                "first_measures": [],
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(data, f)

            result = process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            assert result["functions"] == []

    def test_process_meta_missing_optional_fields(self):
        """Test handling of items with missing optional fields."""
        data = {
            "data": {
                "function": {
                    "measures": [
                        {
                            "name": "测试分类",
                            "values": [
                                {"name": "OnlyName"},
                                {"expr": "OnlyExpr()"},
                                {},
                            ],
                        }
                    ]
                },
                "first_measures": [
                    {
                        "name": "指标分类",
                        "values": [
                            {"name": "OnlyNameIndicator"},
                            {"id": "0.M.Test.0"},
                        ],
                    }
                ],
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

            result = process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            assert len(result["functions"]) == 3
            assert result["functions"][0]["name"] == "OnlyName"
            assert result["functions"][0]["expr"] == ""
            assert result["functions"][1]["name"] == ""

    def test_process_meta_missing_name_in_block(self):
        """Test handling of blocks without name key."""
        data = {
            "data": {
                "function": {
                    "measures": [
                        {"values": [{"name": "Test", "expr": "Test()", "desc": "测试"}]}
                    ]
                },
                "first_measures": [],
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

            result = process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            assert len(result["functions"]) == 1
            assert result["functions"][0]["category"] == "未分类"

    def test_process_meta_unicode_content(self):
        """Test proper handling of Chinese characters and unicode."""
        data = {
            "data": {
                "function": {
                    "measures": [
                        {
                            "name": "测试分类 🔬",
                            "values": [
                                {
                                    "name": "测试函数™",
                                    "expr": "测试()",
                                    "desc": "这是中文描述 © 2024",
                                }
                            ],
                        }
                    ]
                },
                "first_measures": [
                    {
                        "name": "指标分类 αβγ",
                        "values": [
                            {
                                "name": "测试指标 δ",
                                "id": "0.M.测试指标.0",
                                "desc": "指标描述 εζη",
                            }
                        ],
                    }
                ],
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

            result = process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            assert result["functions"][0]["name"] == "测试函数™"
            assert result["functions"][0]["category"] == "测试分类 🔬"
            assert result["indicators"][0]["middle_name"] == "测试指标"

            with open(output_md, "r", encoding="utf-8") as f:
                md_content = f.read()
            assert "测试函数™" in md_content
            assert "测试分类 🔬" in md_content


class TestProcessMetaErrorHandling:
    """Test error handling for process_meta function."""

    def test_file_not_found(self):
        """Test FileNotFoundError when input file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            non_existent = os.path.join(tmpdir, "non_existent.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with pytest.raises(FileNotFoundError):
                process_meta(
                    input_file=non_existent,
                    output_md=output_md,
                    output_json=output_json,
                )

    def test_invalid_json(self):
        """Test JSONDecodeError when input file has invalid JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "invalid.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                f.write("{ invalid json }")

            with pytest.raises(json.JSONDecodeError):
                process_meta(
                    input_file=input_file,
                    output_md=output_md,
                    output_json=output_json,
                )


class TestCatalogStructure:
    """Test the structure of generated catalog."""

    def test_functions_catalog_structure(self):
        """Test functions catalog has correct structure."""
        data = {
            "data": {
                "function": {
                    "measures": [
                        {
                            "name": "日期回溯函数",
                            "values": [
                                {
                                    "name": "Ref",
                                    "expr": "Ref(,)",
                                    "desc": "取得指标几个交易日前的值",
                                }
                            ],
                        }
                    ]
                },
                "first_measures": [],
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

            result = process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            assert "functions" in result
            assert "indicators" in result
            assert len(result["functions"]) == 1
            assert result["functions"][0]["name"] == "Ref"
            assert result["functions"][0]["expr"] == "Ref(,)"
            assert result["functions"][0]["desc"] == "取得指标几个交易日前的值"
            assert result["functions"][0]["category"] == "日期回溯函数"

    def test_indicators_catalog_structure(self):
        """Test indicators catalog has correct structure."""
        data = {
            "data": {
                "function": {"measures": []},
                "first_measures": [
                    {
                        "name": "行情指标",
                        "values": [
                            {
                                "name": "收盘价",
                                "id": "0.M.行情数据.0",
                                "desc": "每日收盘价",
                                "expr": "close",
                            }
                        ],
                    }
                ],
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

            result = process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            assert len(result["indicators"]) == 1
            assert result["indicators"][0]["name"] == "收盘价"
            assert result["indicators"][0]["middle_name"] == "行情数据"
            assert result["indicators"][0]["id"] == "0.M.行情数据.0"
            assert result["indicators"][0]["expr"] == "close"
            assert result["indicators"][0]["category"] == "行情指标"


class TestMarkdownOutput:
    """Test Markdown output format."""

    def test_markdown_table_format(self):
        """Test that Markdown tables are properly formatted."""
        data = {
            "data": {
                "function": {
                    "measures": [
                        {
                            "name": "日期回溯函数",
                            "values": [
                                {"name": "Ref", "expr": "Ref(,)", "desc": "取得指标值"}
                            ],
                        }
                    ]
                },
                "first_measures": [],
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

            process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            with open(output_md, "r", encoding="utf-8") as f:
                md_content = f.read()

            lines = md_content.split("\n")
            table_header_found = False
            table_separator_found = False

            for line in lines:
                if "| 函数名 | 表达式 | 说明 |" in line:
                    table_header_found = True
                if "| :--- | :--- | :--- |" in line:
                    table_separator_found = True

            assert table_header_found, "Table header not found"
            assert table_separator_found, "Table separator not found"

    def test_markdown_headers(self):
        """Test that Markdown headers are properly formatted."""
        data = {
            "data": {
                "function": {
                    "measures": [
                        {
                            "name": "日期回溯函数",
                            "values": [
                                {"name": "Ref", "expr": "Ref(,)", "desc": "取得指标值"}
                            ],
                        }
                    ]
                },
                "first_measures": [
                    {
                        "name": "行情指标",
                        "values": [
                            {
                                "name": "收盘价",
                                "id": "0.M.行情数据.0",
                                "desc": "每日收盘价",
                            }
                        ],
                    }
                ],
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

            process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            with open(output_md, "r", encoding="utf-8") as f:
                md_content = f.read()

            assert md_content.startswith("# 果仁网指标与函数全量手册")
            assert "## 1. 系统函数 (Functions)" in md_content
            assert "## 2. 常用指标 (Standard Indicators)" in md_content
            assert "### 日期回溯函数" in md_content
            assert "### 行情指标" in md_content

    def test_json_output_format(self):
        """Test that JSON output is properly formatted."""
        data = {
            "data": {
                "function": {
                    "measures": [
                        {
                            "name": "测试",
                            "values": [{"name": "Func", "expr": "F()", "desc": "测试"}],
                        }
                    ]
                },
                "first_measures": [
                    {
                        "name": "指标",
                        "values": [
                            {
                                "name": "指标名",
                                "id": "0.M.分类.0",
                                "desc": "描述",
                                "expr": "expr",
                            }
                        ],
                    }
                ],
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

            process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            with open(output_json, "r", encoding="utf-8") as f:
                loaded = json.load(f)

            assert "functions" in loaded
            assert "indicators" in loaded
            assert isinstance(loaded["functions"], list)
            assert isinstance(loaded["indicators"], list)

            with open(output_json, "r", encoding="utf-8") as f:
                content = f.read()
            assert content.startswith("{\n")
            assert "  " in content  # Check for indentation


class TestLongStrings:
    """Test handling of long strings."""

    def test_very_long_description(self):
        """Test handling of very long descriptions."""
        long_desc = "a" * 10000
        data = {
            "data": {
                "function": {
                    "measures": [
                        {
                            "name": "Long",
                            "values": [
                                {"name": "Test", "expr": "Test()", "desc": long_desc}
                            ],
                        }
                    ]
                },
                "first_measures": [],
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(data, f)

            result = process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            assert len(result["functions"][0]["desc"]) == 10000

    def test_special_characters_in_expr(self):
        """Test special characters in expression are handled."""
        data = {
            "data": {
                "function": {
                    "measures": [
                        {
                            "name": "Special",
                            "values": [
                                {
                                    "name": "Test",
                                    "expr": "a|b|c|d|e",
                                    "desc": "测试管道符",
                                }
                            ],
                        }
                    ]
                },
                "first_measures": [],
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

            process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            with open(output_md, "r", encoding="utf-8") as f:
                md_content = f.read()

            assert "`a\\|b\\|c\\|d\\|e`" in md_content


class TestIntegration:
    """Integration tests with real file structure."""

    def test_full_integration_with_all_fields(self):
        """Test full integration with all possible fields."""
        data = {
            "status": "ok",
            "data": {
                "function": {
                    "measures": [
                        {
                            "name": "分类1",
                            "values": [
                                {
                                    "name": "Func1",
                                    "expr": "F1()",
                                    "desc": "描述1<br/>换行\n测试",
                                },
                                {
                                    "name": "Func2",
                                    "expr": "F2|pipe",
                                    "desc": "描述2",
                                },
                            ],
                        },
                        {
                            "name": "分类2",
                            "values": [
                                {"name": "Func3", "expr": "F3()", "desc": "描述3"}
                            ],
                        },
                    ]
                },
                "first_measures": [
                    {
                        "name": "指标分类1",
                        "values": [
                            {
                                "name": "指标1",
                                "id": "0.M.分类A.0",
                                "desc": "指标描述1",
                                "expr": "expr1",
                            },
                        ],
                    },
                    {
                        "name": "指标分类2",
                        "values": [
                            {
                                "name": "指标2",
                                "id": "0.M.分类B.0",
                                "desc": "指标描述2<br/>换行",
                                "expr": "expr2",
                            },
                            {
                                "name": "指标3",
                                "id": "invalid_id",
                                "desc": "指标描述3",
                            },
                        ],
                    },
                ],
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test_meta.json")
            output_md = os.path.join(tmpdir, "output.md")
            output_json = os.path.join(tmpdir, "output.json")

            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

            result = process_meta(
                input_file=input_file, output_md=output_md, output_json=output_json
            )

            assert len(result["functions"]) == 3
            assert len(result["indicators"]) == 3

            assert result["functions"][0]["desc"] == "描述1 换行 测试"
            assert result["functions"][1]["expr"] == "F2\\|pipe"

            assert result["indicators"][0]["middle_name"] == "分类A"
            assert result["indicators"][2]["middle_name"] == "invalid_id"

            with open(output_md, "r", encoding="utf-8") as f:
                md_content = f.read()
            assert "### 分类1" in md_content
            assert "### 分类2" in md_content
            assert "### 指标分类1" in md_content
            assert "### 指标分类2" in md_content

            with open(output_json, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            assert loaded == result
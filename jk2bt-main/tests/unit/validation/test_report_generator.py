"""
Tests for jk2bt/validation/report_generator.py - ReportGenerator
"""

import pytest
import tempfile
import os
from datetime import datetime
from unittest.mock import MagicMock
from jk2bt.validation.report_generator import ReportGenerator
from jk2bt.validation.validator import ValidationReport
from jk2bt.validation.comparison_engine import (
    ComparisonSummary,
    StockComparisonResult,
    ComparisonResult,
)


def create_mock_report():
    """Create a mock ValidationReport for testing"""
    stock_result = StockComparisonResult(
        code="600519.XSHG",
        date="2024-01-01",
        data_type="valuation",
        is_match=True,
        match_rate=100.0,
        field_results=[
            ComparisonResult(
                field_name="pe",
                local_value=10.0,
                jq_value=10.0,
                tolerance=0.01,
                is_match=True,
            )
        ],
    )

    summary = ComparisonSummary(
        data_type="valuation",
        total_stocks=10,
        total_fields=5,
        matched_stocks=9,
        matched_fields=45,
        match_rate=90.0,
        stock_results=[stock_result],
        field_stats={
            "pe": {
                "total": 10,
                "matched": 9,
                "match_rate": 90.0,
                "avg_diff_pct": 0.5,
            }
        },
    )

    report = ValidationReport(
        config={
            "stocks": ["600519.XSHG"],
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "data_types": ["valuation"],
        },
        timestamp=datetime.now().isoformat(),
        summaries={"valuation": summary},
        overall_match_rate=90.0,
        total_comparisons=10,
        total_matched=9,
    )

    return report


class TestReportGenerator:
    """Test ReportGenerator class"""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.generator = ReportGenerator(output_dir=self.temp_dir)

    def teardown_method(self):
        import shutil

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_init_creates_output_dir(self):
        assert os.path.exists(self.temp_dir)

    def test_generate_markdown_report(self):
        report = create_mock_report()
        filepath = self.generator.generate_markdown_report(report)

        assert os.path.exists(filepath)
        with open(filepath, "r") as f:
            content = f.read()
            assert "jk2bt 数据验证报告" in content
            assert "600519.XSHG" in content

    def test_generate_markdown_custom_filename(self):
        report = create_mock_report()
        filepath = self.generator.generate_markdown_report(report, filename="custom.md")

        assert os.path.exists(filepath)
        assert "custom.md" in filepath

    def test_generate_diff_detail(self):
        report = create_mock_report()
        filepath = self.generator.generate_diff_detail(report)

        assert os.path.exists(filepath)
        assert filepath.endswith(".csv")

    def test_generate_diff_detail_no_differences(self):
        report = create_mock_report()
        for summary in report.summaries.values():
            for stock in summary.stock_results:
                stock.is_match = True
                for field in stock.field_results:
                    field.is_match = True

        filepath = self.generator.generate_diff_detail(report)
        assert os.path.exists(filepath)

    def test_generate_summary_table(self):
        report = create_mock_report()
        table = self.generator.generate_summary_table(report)

        assert "valuation" in table
        assert "90.00%" in table

    def test_print_console_summary(self, capsys):
        report = create_mock_report()
        self.generator.print_console_summary(report)

        captured = capsys.readouterr()
        assert "数据验证结果摘要" in captured.out


class TestReportGeneratorEdgeCases:
    """Test ReportGenerator edge cases"""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.generator = ReportGenerator(output_dir=self.temp_dir)

    def teardown_method(self):
        import shutil

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_report_with_no_stock_results(self):
        summary = ComparisonSummary(
            data_type="valuation",
            total_stocks=0,
            total_fields=0,
            matched_stocks=0,
            matched_fields=0,
            match_rate=0.0,
            stock_results=[],
            field_stats={},
        )

        report = ValidationReport(
            config={},
            timestamp=datetime.now().isoformat(),
            summaries={"valuation": summary},
            overall_match_rate=0.0,
            total_comparisons=0,
            total_matched=0,
        )

        filepath = self.generator.generate_markdown_report(report)
        assert os.path.exists(filepath)

    def test_report_with_high_match_rate(self):
        report = create_mock_report()
        report.overall_match_rate = 98.0

        filepath = self.generator.generate_markdown_report(report)
        with open(filepath, "r") as f:
            content = f.read()
            assert "一致性良好" in content

    def test_report_with_low_match_rate(self):
        report = create_mock_report()
        report.overall_match_rate = 70.0

        filepath = self.generator.generate_markdown_report(report)
        with open(filepath, "r") as f:
            content = f.read()
            assert "一致性较差" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

import time

import pandas as pd
import pytest

from .validator import (
    SchemaValidationError,
    SchemaValidator,
    deduplicate_by_key,
    normalize_date_columns,
)


class TestSchemaValidatorValidate:
    def test_validate_pass(self):
        schema = {"symbol": "string", "date": "date", "close": "float64"}
        validator = SchemaValidator("stock_daily", schema)
        df = pd.DataFrame(
            {
                "symbol": ["600519"],
                "date": pd.to_datetime(["2024-04-01"]).date,
                "close": [1800.0],
            }
        )
        errors = validator.validate(df)
        assert errors == []

    def test_validate_missing_column(self):
        schema = {"symbol": "string", "date": "date", "close": "float64"}
        validator = SchemaValidator("stock_daily", schema)
        df = pd.DataFrame(
            {
                "symbol": ["600519"],
                "close": [1800.0],
            }
        )
        errors = validator.validate(df)
        assert len(errors) == 1
        assert "Missing column" in errors[0]
        assert "date" in errors[0]

    def test_validate_type_incompatible(self):
        schema = {"symbol": "string", "close": "float64"}
        validator = SchemaValidator("stock_daily", schema)
        df = pd.DataFrame(
            {
                "symbol": ["600519"],
                "close": pd.to_datetime(["2024-04-01"]),
            }
        )
        errors = validator.validate(df)
        assert len(errors) >= 1


class TestSchemaValidatorPrimaryKey:
    def test_primary_key_has_null(self):
        schema = {"symbol": "string", "close": "float64"}
        validator = SchemaValidator("stock_daily", schema)
        df = pd.DataFrame(
            {
                "symbol": ["600519", "000001"],
                "close": [1800.0, None],
            }
        )
        with pytest.raises(SchemaValidationError):
            validator.validate_and_cast(df, primary_key=["close"])


class TestValidateAndCast:
    def test_validate_and_cast_type_conversion(self):
        schema = {"symbol": "string", "date": "date", "close": "float64"}
        validator = SchemaValidator("stock_daily", schema)
        df = pd.DataFrame(
            {
                "symbol": [600519],
                "date": ["2024-04-01"],
                "close": ["1800.5"],
            }
        )
        result = validator.validate_and_cast(df)
        assert result["symbol"].iloc[0] == "600519"
        assert isinstance(
            result["date"].iloc[0], type(pd.to_datetime("2024-04-01").date())
        )
        assert result["close"].iloc[0] == 1800.5


class TestDeduplicateByKey:
    def test_deduplicate_by_key(self):
        df = pd.DataFrame(
            {
                "symbol": ["600519", "600519", "600519"],
                "date": pd.to_datetime(["2024-04-01", "2024-04-01", "2024-04-01"]).date,
                "close": [1800.0, 1810.0, 1820.0],
            }
        )
        result = deduplicate_by_key(df, ["symbol", "date"])
        assert len(result) == 1
        assert result["close"].iloc[0] == 1820.0

    def test_deduplicate_by_key_no_duplicates(self):
        df = pd.DataFrame(
            {
                "symbol": ["600519", "000001"],
                "date": pd.to_datetime(["2024-04-01", "2024-04-01"]).date,
                "close": [1800.0, 15.5],
            }
        )
        result = deduplicate_by_key(df, ["symbol", "date"])
        assert len(result) == 2


class TestNormalizeDateColumns:
    def test_normalize_date_columns(self):
        df = pd.DataFrame(
            {
                "date": ["2024-04-01", "2024-04-02"],
                "symbol": ["600519", "000001"],
            }
        )
        result = normalize_date_columns(df, columns=["date"])
        assert isinstance(
            result["date"].iloc[0], type(pd.to_datetime("2024-04-01").date())
        )

    def test_normalize_date_columns_default_all(self):
        df = pd.DataFrame(
            {
                "date": ["2024-04-01"],
                "report_date": ["2024-03-31"],
            }
        )
        result = normalize_date_columns(df)
        assert isinstance(
            result["date"].iloc[0], type(pd.to_datetime("2024-04-01").date())
        )
        assert isinstance(
            result["report_date"].iloc[0], type(pd.to_datetime("2024-03-31").date())
        )

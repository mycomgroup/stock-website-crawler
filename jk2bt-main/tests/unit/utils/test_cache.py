"""
test_cache.py
缓存工具模块测试
"""

import pytest
import pandas as pd
import tempfile
import os
from jk2bt.utils.cache import fetch_and_cache_data


class TestFetchAndCacheData:
    """测试通用缓存工具"""

    @pytest.fixture
    def temp_cache_dir(self, tmp_path):
        """创建临时缓存目录"""
        return tmp_path / "cache"

    @pytest.fixture
    def sample_df(self):
        """创建示例数据"""
        return pd.DataFrame(
            {
                "date": pd.date_range("2023-01-01", periods=10),
                "open": [100.0 + i for i in range(10)],
                "close": [105.0 + i for i in range(10)],
            }
        )

    def test_cache_miss_triggers_download(self, temp_cache_dir, sample_df):
        """测试缓存未命中时触发下载"""
        cache_file = str(temp_cache_dir / "test.pkl")
        download_count = [0]

        def mock_download():
            download_count[0] += 1
            return sample_df.copy()

        result = fetch_and_cache_data(
            symbol="TEST",
            start="2023-01-01",
            end="2023-01-10",
            cache_file=cache_file,
            download_func=mock_download,
            date_col="date",
        )

        assert download_count[0] == 1
        assert len(result) == 10

    def test_cache_hit_returns_cached_data(self, temp_cache_dir, sample_df):
        """测试缓存命中时返回缓存数据"""
        cache_file = str(temp_cache_dir / "test.pkl")
        sample_df.to_pickle(cache_file)
        download_count = [0]

        def mock_download():
            download_count[0] += 1
            return sample_df.copy()

        result = fetch_and_cache_data(
            symbol="TEST",
            start="2023-01-01",
            end="2023-01-10",
            cache_file=cache_file,
            download_func=mock_download,
            date_col="date",
        )

        assert download_count[0] == 0
        assert len(result) == 10

    def test_force_update_bypasses_cache(self, temp_cache_dir, sample_df):
        """测试强制更新跳过缓存"""
        cache_file = str(temp_cache_dir / "test.pkl")
        sample_df.to_pickle(cache_file)
        download_count = [0]

        def mock_download():
            download_count[0] += 1
            return pd.DataFrame(
                {
                    "date": pd.date_range("2023-01-01", periods=5),
                    "open": [1, 2, 3, 4, 5],
                    "close": [1, 2, 3, 4, 5],
                }
            )

        result = fetch_and_cache_data(
            symbol="TEST",
            start="2023-01-01",
            end="2023-01-05",
            cache_file=cache_file,
            download_func=mock_download,
            date_col="date",
            force_update=True,
        )

        assert download_count[0] == 1
        assert len(result) == 5

    def test_date_range_filtering(self, temp_cache_dir, sample_df):
        """测试日期范围过滤"""
        cache_file = str(temp_cache_dir / "test.pkl")
        sample_df.to_pickle(cache_file)

        def mock_download():
            return sample_df.copy()

        result = fetch_and_cache_data(
            symbol="TEST",
            start="2023-01-03",
            end="2023-01-07",
            cache_file=cache_file,
            download_func=mock_download,
            date_col="date",
        )

        assert len(result) == 5
        assert result["date"].iloc[0] == pd.Timestamp("2023-01-03")

    def test_column_rename(self, temp_cache_dir, sample_df):
        """测试列重命名"""
        cache_file = str(temp_cache_dir / "test.pkl")
        sample_df.to_pickle(cache_file)

        def mock_download():
            return sample_df.copy()

        result = fetch_and_cache_data(
            symbol="TEST",
            start="2023-01-01",
            end="2023-01-10",
            cache_file=cache_file,
            download_func=mock_download,
            date_col="date",
            columns_map={"close": "closed"},
        )

        assert "closed" in result.columns
        assert "close" not in result.columns

    def test_column_selection(self, temp_cache_dir, sample_df):
        """测试列筛选"""
        cache_file = str(temp_cache_dir / "test.pkl")
        sample_df.to_pickle(cache_file)

        def mock_download():
            return sample_df.copy()

        result = fetch_and_cache_data(
            symbol="TEST",
            start="2023-01-01",
            end="2023-01-10",
            cache_file=cache_file,
            download_func=mock_download,
            date_col="date",
            select_cols=["date", "close"],
        )

        assert list(result.columns) == ["date", "close"]

    def test_download_returns_empty_raises(self, temp_cache_dir):
        """测试下载返回空数据时抛异常"""
        cache_file = str(temp_cache_dir / "test.pkl")

        def mock_download():
            return pd.DataFrame()

        with pytest.raises(ValueError, match="下载返回空数据"):
            fetch_and_cache_data(
                symbol="TEST",
                start="2023-01-01",
                end="2023-01-10",
                cache_file=cache_file,
                download_func=mock_download,
                date_col="date",
            )

    def test_no_date_col_no_filter(self, temp_cache_dir, sample_df):
        """测试无日期列时不进行范围过滤"""
        cache_file = str(temp_cache_dir / "test.pkl")
        sample_df.to_pickle(cache_file)

        def mock_download():
            return sample_df.copy()

        result = fetch_and_cache_data(
            symbol="TEST",
            start="2023-01-01",
            end="2023-01-10",
            cache_file=cache_file,
            download_func=mock_download,
            date_col=None,
        )

        assert len(result) == 10

    def test_corrupted_cache_triggers_redownload(self, temp_cache_dir):
        """测试损坏的缓存触发重新下载"""
        cache_file = str(temp_cache_dir / "test.pkl")
        with open(cache_file, "w") as f:
            f.write("corrupted data")
        download_count = [0]

        def mock_download():
            download_count[0] += 1
            return pd.DataFrame(
                {
                    "date": pd.date_range("2023-01-01", periods=5),
                    "value": [1, 2, 3, 4, 5],
                }
            )

        result = fetch_and_cache_data(
            symbol="TEST",
            start="2023-01-01",
            end="2023-01-05",
            cache_file=cache_file,
            download_func=mock_download,
            date_col="date",
        )

        assert download_count[0] == 1

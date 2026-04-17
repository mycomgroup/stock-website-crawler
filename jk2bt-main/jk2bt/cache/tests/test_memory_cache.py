import threading
import time

import pandas as pd
import pytest

from .memory import MemoryCache


class TestMemoryCacheBasic:
    def test_put_and_get(self):
        cache = MemoryCache(max_items=100, default_ttl_seconds=3600)
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        cache.put("key1", df)
        result = cache.get("key1")
        pd.testing.assert_frame_equal(result, df)

    def test_get_nonexistent_key(self):
        cache = MemoryCache()
        assert cache.get("nonexistent") is None

    def test_put_overwrites_existing(self):
        cache = MemoryCache(max_items=100, default_ttl_seconds=3600)
        df1 = pd.DataFrame({"a": [1]})
        df2 = pd.DataFrame({"a": [2]})
        cache.put("key1", df1)
        cache.put("key1", df2)
        result = cache.get("key1")
        pd.testing.assert_frame_equal(result, df2)


class TestMemoryCacheTTL:
    def test_ttl_expire(self):
        cache = MemoryCache(max_items=100, default_ttl_seconds=1)
        df = pd.DataFrame({"a": [1]})
        cache.put("key1", df, ttl_seconds=1)
        assert cache.get("key1") is not None
        time.sleep(1.1)
        assert cache.get("key1") is None

    def test_ttl_zero_never_expire(self):
        cache = MemoryCache(max_items=100, default_ttl_seconds=3600)
        df = pd.DataFrame({"a": [1]})
        cache.put("key1", df, ttl_seconds=0)
        assert cache.get("key1") is not None
        time.sleep(0.1)
        assert cache.get("key1") is not None


class TestMemoryCacheLRU:
    def test_lru_eviction(self):
        cache = MemoryCache(max_items=3, default_ttl_seconds=3600)
        cache.put("k1", pd.DataFrame({"a": [1]}))
        cache.put("k2", pd.DataFrame({"a": [2]}))
        cache.put("k3", pd.DataFrame({"a": [3]}))
        cache.get("k1")
        cache.put("k4", pd.DataFrame({"a": [4]}))
        assert cache.get("k1") is not None
        assert cache.get("k2") is None
        assert cache.get("k3") is not None
        assert cache.get("k4") is not None


class TestMemoryCacheStats:
    def test_hit_rate(self):
        cache = MemoryCache(max_items=100, default_ttl_seconds=3600)
        df = pd.DataFrame({"a": [1]})
        cache.put("key1", df)
        cache.get("key1")
        cache.get("key1")
        cache.get("nonexistent")
        assert cache.hit_rate == pytest.approx(2 / 3, abs=0.01)

    def test_hit_rate_empty(self):
        cache = MemoryCache()
        assert cache.hit_rate == 0.0


class TestMemoryCacheInvalidate:
    def test_invalidate_single_key(self):
        cache = MemoryCache(max_items=100, default_ttl_seconds=3600)
        cache.put("k1", pd.DataFrame({"a": [1]}))
        cache.put("k2", pd.DataFrame({"a": [2]}))
        count = cache.invalidate("k1")
        assert count == 1
        assert cache.get("k1") is None
        assert cache.get("k2") is not None

    def test_invalidate_all(self):
        cache = MemoryCache(max_items=100, default_ttl_seconds=3600)
        cache.put("k1", pd.DataFrame({"a": [1]}))
        cache.put("k2", pd.DataFrame({"a": [2]}))
        count = cache.invalidate()
        assert count == 2
        assert cache.get("k1") is None
        assert cache.get("k2") is None

    def test_invalidate_nonexistent_key(self):
        cache = MemoryCache()
        assert cache.invalidate("nonexistent") == 0


class TestMemoryCacheCleanup:
    def test_cleanup_expired(self):
        cache = MemoryCache(max_items=100, default_ttl_seconds=3600)
        cache.put("k1", pd.DataFrame({"a": [1]}), ttl_seconds=1)
        cache.put("k2", pd.DataFrame({"a": [2]}), ttl_seconds=0)
        time.sleep(1.1)
        cleaned = cache.cleanup_expired()
        assert cleaned == 1
        assert cache.size == 1


class TestMemoryCacheThreadSafety:
    def test_concurrent_put_get(self):
        cache = MemoryCache(max_items=1000, default_ttl_seconds=3600)
        errors = []

        def writer(start, count):
            try:
                for i in range(start, start + count):
                    cache.put(f"key_{i}", pd.DataFrame({"val": [i]}))
            except Exception as e:
                errors.append(e)

        def reader(start, count):
            try:
                for i in range(start, start + count):
                    cache.get(f"key_{i}")
            except Exception as e:
                errors.append(e)

        threads = []
        for t in range(4):
            threads.append(threading.Thread(target=writer, args=(t * 50, 50)))
            threads.append(threading.Thread(target=reader, args=(t * 50, 50)))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0
        assert cache.size <= 1000

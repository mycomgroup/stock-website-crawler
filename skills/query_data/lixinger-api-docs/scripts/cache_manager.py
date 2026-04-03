import os
import json
import sqlite3
import duckdb
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self, db_path=None):
        if db_path is None:
            # Default to a .cache directory in the skill folder
            base_dir = os.path.dirname(os.path.dirname(__file__))
            cache_dir = os.path.join(base_dir, ".cache")
            os.makedirs(cache_dir, exist_ok=True)
            db_path = os.path.join(cache_dir, "api_cache.db")
        
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with duckdb.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS api_cache (
                    key VARCHAR PRIMARY KEY,
                    suffix VARCHAR,
                    params VARCHAR,
                    response VARCHAR,
                    timestamp TIMESTAMP,
                    expiry_timestamp TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS session_lists (
                    name VARCHAR PRIMARY KEY,
                    stock_codes VARCHAR,
                    timestamp TIMESTAMP
                )
            """)

    def save_list(self, name, stock_codes):
        with duckdb.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO session_lists (name, stock_codes, timestamp)
                VALUES (?, ?, ?)
            """, [name, json.dumps(stock_codes), datetime.now()])

    def get_list(self, name):
        with duckdb.connect(self.db_path) as conn:
            res = conn.execute("SELECT stock_codes FROM session_lists WHERE name = ?", [name]).fetchone()
            if res:
                return json.loads(res[0])
        return None

    def _generate_key(self, suffix, params):
        # Sort params to ensure consistency
        params_str = json.dumps(params, sort_keys=True)
        return f"{suffix}:{params_str}"

    def get(self, suffix, params, max_age_days=1):
        key = self._generate_key(suffix, params)
        with duckdb.connect(self.db_path) as conn:
            res = conn.execute("SELECT response, timestamp FROM api_cache WHERE key = ?", [key]).fetchone()
            if res:
                response_str, timestamp = res
                if datetime.now() - timestamp < timedelta(days=max_age_days):
                    return json.loads(response_str)
        return None

    def set(self, suffix, params, response, expiry_days=1):
        key = self._generate_key(suffix, params)
        response_str = json.dumps(response)
        now = datetime.now()
        expiry = now + timedelta(days=expiry_days)
        
        with duckdb.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO api_cache (key, suffix, params, response, timestamp, expiry_timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, [key, suffix, json.dumps(params), response_str, now, expiry])

    def clear(self):
        with duckdb.connect(self.db_path) as conn:
            conn.execute("DELETE FROM api_cache")

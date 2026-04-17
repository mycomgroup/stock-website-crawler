import logging
import threading
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

logger = logging.getLogger(__name__)

from .partition_manager import PartitionManager


class QueryEngine:
    def __init__(
        self,
        base_dir: str | Path,
        threads: int = 4,
        memory_limit: str = "4GB",
    ):
        self.base_dir = Path(base_dir)
        self.threads = threads
        self.memory_limit = memory_limit
        self.partition_manager = PartitionManager(self.base_dir)
        self._local = threading.local()

    def query(
        self,
        table: str,
        storage_layer: str,
        partition_by: str | None = None,
        where: dict[str, Any] | None = None,
        columns: list[str] | None = None,
        order_by: list[str] | None = None,
        limit: int | None = None,
        prefer_aggregated: bool = True,
    ) -> pd.DataFrame | None:
        if prefer_aggregated:
            agg_glob = self.partition_manager.list_all_glob_paths(
                table, storage_layer, partition_by, layer="aggregated"
            )
            agg_paths = list(
                Path(self.base_dir).glob(agg_glob.replace(str(self.base_dir) + "/", ""))
            )
            if not agg_paths:
                agg_paths = (
                    list(Path(agg_glob).parent.glob("*.parquet"))
                    if Path(agg_glob).parent.exists()
                    else []
                )
            agg_paths = [p for p in agg_paths if p.suffix == ".parquet"]
            if agg_paths:
                result = self.query_by_paths(agg_paths, where, columns, order_by, limit)
                if result is not None and len(result) > 0:
                    return result

        raw_glob = self.partition_manager.list_all_glob_paths(
            table, storage_layer, partition_by, layer="raw"
        )
        raw_paths = list(
            Path(self.base_dir).glob(raw_glob.replace(str(self.base_dir) + "/", ""))
        )
        if not raw_paths:
            raw_paths = (
                list(Path(raw_glob).parent.glob("*.parquet"))
                if Path(raw_glob).parent.exists()
                else []
            )
        raw_paths = [p for p in raw_paths if p.suffix == ".parquet"]
        if raw_paths:
            return self.query_by_paths(raw_paths, where, columns, order_by, limit)

        return pd.DataFrame()

    def query_by_paths(
        self,
        paths: list[Path],
        where: dict[str, Any] | None = None,
        columns: list[str] | None = None,
        order_by: list[str] | None = None,
        limit: int | None = None,
    ) -> pd.DataFrame | None:
        if not paths:
            return pd.DataFrame()

        where_clause = self._build_where_clause(where) if where else ""
        sql = self._build_sql(
            str([str(p) for p in paths]),
            where_clause,
            columns,
            order_by,
            limit,
        )

        conn = self._get_connection()
        try:
            df = conn.execute(sql).fetchdf()
            return df
        except Exception as e:
            logger.error(f"Query failed for paths {paths}: {e}")
            df = pd.DataFrame()
            df["_query_error"] = True
            return df

    def exists(
        self,
        table: str,
        storage_layer: str,
        partition_by: str | None = None,
        where: dict[str, Any] | None = None,
        prefer_aggregated: bool = True,
    ) -> bool:
        if prefer_aggregated:
            agg_glob = self.partition_manager.list_all_glob_paths(
                table, storage_layer, partition_by, layer="aggregated"
            )
            agg_paths = list(
                Path(self.base_dir).glob(agg_glob.replace(str(self.base_dir) + "/", ""))
            )
            if not agg_paths:
                agg_paths = (
                    list(Path(agg_glob).parent.glob("*.parquet"))
                    if Path(agg_glob).parent.exists()
                    else []
                )
            agg_paths = [p for p in agg_paths if p.suffix == ".parquet"]
            if agg_paths:
                result = self.query_by_paths(agg_paths, where, columns=["1"], limit=1)
                if result is not None and len(result) > 0:
                    return True

        raw_glob = self.partition_manager.list_all_glob_paths(
            table, storage_layer, partition_by, layer="raw"
        )
        raw_paths = list(
            Path(self.base_dir).glob(raw_glob.replace(str(self.base_dir) + "/", ""))
        )
        if not raw_paths:
            raw_paths = (
                list(Path(raw_glob).parent.glob("*.parquet"))
                if Path(raw_glob).parent.exists()
                else []
            )
        raw_paths = [p for p in raw_paths if p.suffix == ".parquet"]
        if raw_paths:
            result = self.query_by_paths(raw_paths, where, columns=["1"], limit=1)
            return result is not None and len(result) > 0

        return False

    def count(
        self,
        table: str,
        storage_layer: str,
        partition_by: str | None = None,
        where: dict[str, Any] | None = None,
        prefer_aggregated: bool = True,
    ) -> int:
        total = 0

        if prefer_aggregated:
            agg_glob = self.partition_manager.list_all_glob_paths(
                table, storage_layer, partition_by, layer="aggregated"
            )
            agg_paths = list(
                Path(self.base_dir).glob(agg_glob.replace(str(self.base_dir) + "/", ""))
            )
            if not agg_paths:
                agg_paths = (
                    list(Path(agg_glob).parent.glob("*.parquet"))
                    if Path(agg_glob).parent.exists()
                    else []
                )
            agg_paths = [p for p in agg_paths if p.suffix == ".parquet"]
            if agg_paths:
                where_clause = self._build_where_clause(where) if where else ""
                paths_str = ", ".join(f"'{p}'" for p in agg_paths)
                sql = f"SELECT COUNT(*) FROM read_parquet([{paths_str}])"
                if where_clause:
                    sql += f" WHERE {where_clause}"
                conn = self._get_connection()
                try:
                    result = conn.execute(sql).fetchone()
                    if result:
                        total += result[0]
                except Exception:
                    pass

        raw_glob = self.partition_manager.list_all_glob_paths(
            table, storage_layer, partition_by, layer="raw"
        )
        raw_paths = list(
            Path(self.base_dir).glob(raw_glob.replace(str(self.base_dir) + "/", ""))
        )
        if not raw_paths:
            raw_paths = (
                list(Path(raw_glob).parent.glob("*.parquet"))
                if Path(raw_glob).parent.exists()
                else []
            )
        raw_paths = [p for p in raw_paths if p.suffix == ".parquet"]
        if raw_paths:
            where_clause = self._build_where_clause(where) if where else ""
            paths_str = ", ".join(f"'{p}'" for p in raw_paths)
            sql = f"SELECT COUNT(*) FROM read_parquet([{paths_str}])"
            if where_clause:
                sql += f" WHERE {where_clause}"
            conn = self._get_connection()
            try:
                result = conn.execute(sql).fetchone()
                if result:
                    total += result[0]
            except Exception:
                pass

        return total

    def _get_connection(self) -> duckdb.DuckDBPyConnection:
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = duckdb.connect(database=":memory:")
            self._local.conn.execute(f"SET threads={self.threads}")
            self._local.conn.execute(f"SET memory_limit='{self.memory_limit}'")
        return self._local.conn

    def _build_where_clause(self, where: dict[str, Any]) -> str:
        conditions = []
        for key, value in where.items():
            if (
                isinstance(value, (list, tuple))
                and len(value) == 2
                and not isinstance(value, str)
            ):
                if all(isinstance(v, (int, float)) for v in value):
                    conditions.append(
                        f"{key} >= {self._format_value(value[0])} AND {key} <= {self._format_value(value[1])}"
                    )
                elif all(hasattr(v, "strftime") for v in value):
                    conditions.append(
                        f"{key} >= {self._format_value(value[0])} AND {key} <= {self._format_value(value[1])}"
                    )
                else:
                    formatted_values = ", ".join(self._format_value(v) for v in value)
                    conditions.append(f"{key} IN ({formatted_values})")
            elif isinstance(value, list):
                formatted_values = ", ".join(self._format_value(v) for v in value)
                conditions.append(f"{key} IN ({formatted_values})")
            else:
                conditions.append(f"{key} = {self._format_value(value)}")
        return " AND ".join(conditions)

    def _build_sql(
        self,
        glob_pattern: str,
        where_clause: str,
        columns: list[str] | None,
        order_by: list[str] | None,
        limit: int | None,
    ) -> str:
        if glob_pattern.startswith("["):
            sql = f"SELECT {', '.join(columns) if columns else '*'} FROM read_parquet({glob_pattern})"
        else:
            sql = (
                f"SELECT {', '.join(columns) if columns else '*'} FROM '{glob_pattern}'"
            )

        if where_clause:
            sql += f" WHERE {where_clause}"

        if order_by:
            sql += f" ORDER BY {', '.join(order_by)}"

        if limit is not None:
            sql += f" LIMIT {limit}"

        return sql

    def _format_value(self, value: Any) -> str:
        if isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        if isinstance(value, str):
            escaped = value.replace("'", "''")
            return f"'{escaped}'"
        if isinstance(value, (int, float)):
            return str(value)
        if hasattr(value, "strftime"):
            return f"'{value.strftime('%Y-%m-%d')}'"
        return str(value)

    def _close(self):
        if hasattr(self._local, "conn") and self._local.conn is not None:
            self._local.conn.close()
            self._local.conn = None

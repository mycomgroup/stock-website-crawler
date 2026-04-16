import os
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from .partition_manager import PartitionManager
from .schema_validator import SchemaValidationError, SchemaValidator, deduplicate_by_key


class AtomicWriter:
    def __init__(
        self,
        base_dir: str | Path,
        compression: str = "snappy",
        row_group_size: int = 100_000,
    ):
        self.base_dir = Path(base_dir)
        self.compression = compression
        self.row_group_size = row_group_size
        self.partition_manager = PartitionManager(self.base_dir)

    def write(
        self,
        table: str,
        storage_layer: str,
        data: pd.DataFrame,
        partition_by: str | None = None,
        partition_value: str | None = None,
        schema: dict[str, str] | None = None,
        primary_key: list[str] | None = None,
    ) -> Path:
        partition_path = self.partition_manager.raw_partition_path(
            table, storage_layer, partition_by, partition_value
        )
        self.partition_manager.ensure_dir(partition_path)

        prepared_data = self._validate_and_prepare(data, schema, primary_key)

        filename = self.partition_manager.generate_filename(partition_value)
        target_path = partition_path / filename

        return self._write_atomic(prepared_data, target_path)

    def write_meta(
        self,
        table: str,
        data: pd.DataFrame,
        schema: dict[str, str] | None = None,
        primary_key: list[str] | None = None,
    ) -> Path:
        meta_path = self.partition_manager.raw_partition_path(table, "meta", None, None)
        self.partition_manager.ensure_dir(meta_path)

        prepared_data = self._validate_and_prepare(data, schema, primary_key)

        target_path = meta_path / f"{table}.parquet"
        return self._write_atomic(prepared_data, target_path)

    def _validate_and_prepare(
        self,
        data: pd.DataFrame,
        schema: dict[str, str] | None,
        primary_key: list[str] | None,
    ) -> pd.DataFrame:
        result = data
        if schema is not None:
            validator = SchemaValidator("unknown", schema)
            result = validator.validate_and_cast(result, primary_key)
        if primary_key is not None:
            result = deduplicate_by_key(result, primary_key)
        return result

    def _write_atomic(
        self,
        data: pd.DataFrame,
        target_path: Path,
    ) -> Path:
        tmp_path = target_path.with_suffix(target_path.suffix + ".tmp")
        try:
            table = pa.Table.from_pandas(data)
            pq.write_table(
                table,
                str(tmp_path),
                compression=self.compression,
                row_group_size=self.row_group_size,
            )
            os.replace(str(tmp_path), str(target_path))
        except OSError as e:
            if tmp_path.exists():
                tmp_path.unlink(missing_ok=True)
            raise IOError(f"Failed to write parquet file '{target_path}': {e}") from e
        return target_path

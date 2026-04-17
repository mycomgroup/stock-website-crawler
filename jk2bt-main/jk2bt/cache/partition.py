import os
import uuid
from pathlib import Path


class PartitionManager:
    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir)

    def raw_partition_path(
        self,
        table: str,
        storage_layer: str,
        partition_by: str | None,
        partition_value: str | None = None,
    ) -> Path:
        if partition_by and partition_value:
            return (
                self.base_dir
                / storage_layer
                / table
                / f"{partition_by}={partition_value}"
            )
        return self.base_dir / "meta" / table

    def aggregated_path(
        self,
        table: str,
        storage_layer: str,
        partition_by: str | None,
        partition_value: str | None = None,
    ) -> Path:
        if partition_by and partition_value:
            return (
                self.base_dir
                / "aggregated"
                / storage_layer
                / table
                / f"{partition_by}={partition_value}.parquet"
            )
        return self.base_dir / "aggregated" / "meta" / f"{table}.parquet"

    def generate_filename(self, partition_value: str | None = None) -> str:
        pid = os.getpid()
        uid = uuid.uuid4().hex[:8]
        return f"part_{pid}_{uid}.parquet"

    def list_partition_files(
        self,
        table: str,
        storage_layer: str,
        partition_by: str | None,
        partition_value: str | None = None,
    ) -> list[Path]:
        path = self.raw_partition_path(
            table, storage_layer, partition_by, partition_value
        )
        if not path.exists():
            return []
        return [f for f in path.glob("*.parquet") if not f.name.endswith(".tmp")]

    def list_all_partitions(
        self,
        table: str,
        storage_layer: str,
        partition_by: str | None,
    ) -> list[str]:
        if partition_by is None:
            return [""]
        path = self.base_dir / storage_layer / table
        if not path.exists():
            return []
        partitions = []
        for d in path.iterdir():
            if d.is_dir() and d.name.startswith(f"{partition_by}="):
                partitions.append(d.name.split("=", 1)[1])
        return sorted(partitions)

    def list_all_glob_paths(
        self,
        table: str,
        storage_layer: str,
        partition_by: str | None,
        layer: str = "raw",
    ) -> str:
        if layer == "raw":
            base = self.base_dir / storage_layer / table
        else:
            base = self.base_dir / "aggregated" / storage_layer / table

        if partition_by is None:
            return str(base / "*.parquet")

        if layer == "raw":
            return str(base / "**/*.parquet")
        return str(base / "*.parquet")

    def ensure_dir(self, path: Path) -> Path:
        path.mkdir(parents=True, exist_ok=True)
        return path

    def file_count(
        self,
        table: str,
        storage_layer: str,
        partition_by: str | None,
        partition_value: str | None = None,
    ) -> int:
        return len(
            self.list_partition_files(
                table, storage_layer, partition_by, partition_value
            )
        )

    def total_size_bytes(
        self,
        table: str,
        storage_layer: str,
        partition_by: str | None,
        partition_value: str | None = None,
    ) -> int:
        files = self.list_partition_files(
            table, storage_layer, partition_by, partition_value
        )
        return sum(f.stat().st_size for f in files)

    def lock_path(self, name: str) -> Path:
        return self.base_dir / "_locks" / f"{name}.lock"

    def remove_file(self, path: Path) -> bool:
        try:
            path.unlink()
            return True
        except FileNotFoundError:
            return False

    def remove_dir(self, path: Path) -> bool:
        try:
            import shutil

            shutil.rmtree(path)
            return True
        except FileNotFoundError:
            return False

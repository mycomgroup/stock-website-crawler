"""
运行时资源管理包
为策略提供统一的本地资源目录管理机制

资源类型分类：
- 输入资源：模型文件、参数文件、CSV/JSON 数据文件
- 输出资源：运行时输出文件、研究产物、交易记录

目录结构约定：
strategy_outputs/
  ├── strategy_name_1/
  │   ├── input/
  │   │   ├── config/     - 配置文件（JSON/YAML/TXT）
  │   │   ├── models/     - 模型文件（PKL/H5/PTH）
  │   │   ├── data/       - 数据文件（CSV/JSON/PKL）
  │   │   └── params/     - 参数文件
  │   └── output/
  │   │   ├── logs/       - 日志文件
  │   │   ├── trades/     - 交易记录
  │   │   ├── research/   - 研究产物
  │   │   └── signals/    - 信号记录
  ├── strategy_name_2/
  ├── ...

使用方法：
    from runtime_resource_pack import RuntimeResourcePack

    pack = RuntimeResourcePack(strategy_name="my_strategy")
    pack.setup_resource_dir()

    # 写入模型文件
    pack.write_input_resource("models/trained_model.pkl", model_bytes)

    # 读取配置文件
    config = pack.read_input_resource("config/params.json")

    # 输出交易记录
    pack.write_output_resource("trades/trade_log.csv", trade_data)
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime
import json
import threading


class RuntimeResourcePack:
    """运行时资源包管理器"""

    RESOURCE_TYPES = {
        "input": {
            "config": ["json", "yaml", "yml", "txt", "ini", "cfg"],
            "models": ["pkl", "h5", "pth", "pt", "onnx", "model", "bin"],
            "data": ["csv", "json", "pkl", "parquet", "xlsx", "txt"],
            "params": ["json", "txt", "csv", "pkl"],
        },
        "output": {
            "logs": ["log", "txt", "csv"],
            "trades": ["csv", "json", "txt"],
            "research": ["csv", "json", "pkl", "txt", "png", "pdf"],
            "signals": ["csv", "json", "log", "txt"],
        },
    }

    DEFAULT_RUNTIME_BASE = "strategy_outputs"

    _current_strategy_name: Optional[str] = None
    _lock = threading.Lock()

    def __init__(
        self,
        strategy_name: Optional[str] = None,
        runtime_base: Optional[Union[str, Path]] = None,
        auto_create: bool = True,
    ):
        self.strategy_name = (
            strategy_name or self._get_current_strategy_name() or "default"
        )
        self.runtime_base = Path(runtime_base or self._get_default_runtime_base())
        self.strategy_dir = self.runtime_base / self.strategy_name
        self.input_dir = self.strategy_dir / "input"
        self.output_dir = self.strategy_dir / "output"

        if auto_create:
            self.setup_resource_dir()

    @classmethod
    def _get_default_runtime_base(cls) -> Path:
        # 从 src/strategy/runtime_resource_pack.py 向上两级到项目根目录
        # Path(__file__) = src/strategy/runtime_resource_pack.py
        # parent = src/strategy/
        # parent.parent = src/
        # parent.parent.parent = 项目根目录
        base_dir = Path(__file__).parent.parent.parent / cls.DEFAULT_RUNTIME_BASE
        base_dir.mkdir(parents=True, exist_ok=True)
        return base_dir

    @classmethod
    def set_current_strategy_name(cls, name: str) -> None:
        with cls._lock:
            cls._current_strategy_name = name

    @classmethod
    def _get_current_strategy_name(cls) -> Optional[str]:
        with cls._lock:
            return cls._current_strategy_name

    def setup_resource_dir(self) -> Dict[str, Path]:
        for category, subdirs in self.RESOURCE_TYPES.items():
            category_dir = self.strategy_dir / category
            category_dir.mkdir(parents=True, exist_ok=True)

            for subdir in subdirs.keys():
                subdir_path = category_dir / subdir
                subdir_path.mkdir(parents=True, exist_ok=True)

        return {
            "strategy_dir": self.strategy_dir,
            "input_dir": self.input_dir,
            "output_dir": self.output_dir,
        }

    def get_input_dir(self, resource_type: Optional[str] = None) -> Path:
        if resource_type:
            return self.input_dir / resource_type
        return self.input_dir

    def get_output_dir(self, resource_type: Optional[str] = None) -> Path:
        if resource_type:
            return self.output_dir / resource_type
        return self.output_dir

    def _infer_resource_type(self, filepath: str) -> str:
        ext = Path(filepath).suffix.lower().lstrip(".")
        path_lower = filepath.lower()

        for subdir in ["model", "models", "train", "test"]:
            if subdir in path_lower:
                return "models"

        for subdir in ["config", "param", "parameter"]:
            if subdir in path_lower:
                return "config"

        for subdir in ["trade", "trades", "signal", "signals", "result", "nav"]:
            if subdir in path_lower:
                return "trades"

        for subdir in ["log"]:
            if subdir in path_lower:
                if "trade" not in path_lower and "signal" not in path_lower:
                    return "logs"

        for category, subdirs in self.RESOURCE_TYPES.items():
            for subdir, extensions in subdirs.items():
                if ext in extensions:
                    return subdir

        for category, subdirs in self.RESOURCE_TYPES.items():
            for subdir in subdirs.keys():
                if subdir in path_lower:
                    return subdir

        return "data"

    def _validate_path(self, filepath: str, is_input: bool) -> Path:
        base_dir = self.input_dir if is_input else self.output_dir

        if os.path.isabs(filepath):
            raise ValueError(f"不允许使用绝对路径: '{filepath}'。请使用相对路径。")

        if ".." in filepath:
            raise ValueError(f"不允许访问上级目录 ('..'): '{filepath}'")

        target_path = (base_dir / filepath).resolve()

        if not str(target_path).startswith(str(base_dir.resolve())):
            raise ValueError(
                f"路径越界: '{filepath}' 不在允许的目录范围内。允许目录: {base_dir}"
            )

        return target_path

    def write_input_resource(
        self,
        filepath: str,
        content: Union[str, bytes],
        resource_type: Optional[str] = None,
        mode: str = "w",
    ) -> Path:
        if resource_type is None:
            resource_type = self._infer_resource_type(filepath)

        target_dir = self.get_input_dir(resource_type)
        target_path = target_dir / filepath

        target_path.parent.mkdir(parents=True, exist_ok=True)

        is_binary_content = isinstance(content, bytes)
        actual_mode = mode if is_binary_content else mode

        if is_binary_content:
            if not actual_mode.endswith("b"):
                actual_mode = actual_mode + "b" if actual_mode in ("w", "a") else "wb"
            with open(target_path, actual_mode) as f:
                f.write(content)
        else:
            if actual_mode.endswith("b"):
                actual_mode = actual_mode[:-1]
            with open(target_path, actual_mode, encoding="utf-8") as f:
                f.write(content)

        return target_path

    def read_input_resource(
        self, filepath: str, resource_type: Optional[str] = None, mode: str = "r"
    ) -> Union[str, bytes]:
        if resource_type is None:
            resource_type = self._infer_resource_type(filepath)

        target_dir = self.get_input_dir(resource_type)
        target_path = target_dir / filepath

        if not target_path.exists():
            alt_path = self.input_dir / filepath
            if alt_path.exists():
                target_path = alt_path
            else:
                raise FileNotFoundError(f"文件不存在: {filepath}。路径: {target_path}")

        ext = Path(filepath).suffix.lower().lstrip(".")
        is_binary_file = ext in ["pkl", "h5", "pth", "pt", "onnx", "model", "bin"]

        actual_mode = mode
        if is_binary_file and not mode.endswith("b"):
            actual_mode = "rb"

        if actual_mode.endswith("b"):
            with open(target_path, "rb") as f:
                return f.read()
        else:
            with open(target_path, "r", encoding="utf-8") as f:
                return f.read()

    def write_output_resource(
        self,
        filepath: str,
        content: Union[str, bytes],
        resource_type: Optional[str] = None,
        mode: str = "w",
    ) -> Path:
        if resource_type is None:
            resource_type = self._infer_resource_type(filepath)

        target_dir = self.get_output_dir(resource_type)
        target_path = target_dir / filepath

        target_path.parent.mkdir(parents=True, exist_ok=True)

        is_binary_content = isinstance(content, bytes)
        actual_mode = mode

        if is_binary_content:
            if not actual_mode.endswith("b"):
                actual_mode = actual_mode + "b" if actual_mode in ("w", "a") else "wb"
            with open(target_path, actual_mode) as f:
                f.write(content)
        else:
            if actual_mode.endswith("b"):
                actual_mode = actual_mode[:-1]
            with open(target_path, actual_mode, encoding="utf-8") as f:
                f.write(content)

        return target_path

    def read_output_resource(
        self, filepath: str, resource_type: Optional[str] = None, mode: str = "r"
    ) -> Union[str, bytes]:
        if resource_type is None:
            resource_type = self._infer_resource_type(filepath)

        target_dir = self.get_output_dir(resource_type)
        target_path = target_dir / filepath

        if not target_path.exists():
            alt_path = self.output_dir / filepath
            if alt_path.exists():
                target_path = alt_path
            else:
                raise FileNotFoundError(f"文件不存在: {filepath}。路径: {target_path}")

        ext = Path(filepath).suffix.lower().lstrip(".")
        is_binary_file = ext in ["pkl", "h5", "pth", "pt", "onnx", "model", "bin"]

        actual_mode = mode
        if is_binary_file and not mode.endswith("b"):
            actual_mode = "rb"

        if actual_mode.endswith("b"):
            with open(target_path, "rb") as f:
                return f.read()
        else:
            with open(target_path, "r", encoding="utf-8") as f:
                return f.read()

    def list_input_resources(
        self, resource_type: Optional[str] = None
    ) -> List[Dict[str, str]]:
        return self._list_resources(self.input_dir, resource_type)

    def list_output_resources(
        self, resource_type: Optional[str] = None
    ) -> List[Dict[str, str]]:
        return self._list_resources(self.output_dir, resource_type)

    def _list_resources(
        self, base_dir: Path, resource_type: Optional[str] = None
    ) -> List[Dict[str, str]]:
        resources = []

        if resource_type:
            search_dir = base_dir / resource_type
            if search_dir.exists():
                for file_path in search_dir.rglob("*"):
                    if file_path.is_file():
                        rel_path = file_path.relative_to(search_dir)
                        resources.append(
                            {
                                "path": str(rel_path),
                                "full_path": str(file_path),
                                "type": resource_type,
                                "size": file_path.stat().st_size,
                            }
                        )
        else:
            for subdir in base_dir.iterdir():
                if subdir.is_dir():
                    for file_path in subdir.rglob("*"):
                        if file_path.is_file():
                            rel_path = file_path.relative_to(base_dir)
                            resources.append(
                                {
                                    "path": str(rel_path),
                                    "full_path": str(file_path),
                                    "type": subdir.name,
                                    "size": file_path.stat().st_size,
                                }
                            )

        return resources

    def clear_output_resources(self, resource_type: Optional[str] = None) -> None:
        if resource_type:
            target_dir = self.get_output_dir(resource_type)
            if target_dir.exists():
                shutil.rmtree(target_dir)
                target_dir.mkdir(parents=True, exist_ok=True)
        else:
            if self.output_dir.exists():
                shutil.rmtree(self.output_dir)
                self.setup_resource_dir()

    def clear_all_resources(self) -> None:
        if self.strategy_dir.exists():
            shutil.rmtree(self.strategy_dir)
            self.setup_resource_dir()

    def pack_resources(self, output_path: Optional[Union[str, Path]] = None) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        pack_name = f"{self.strategy_name}_resources_{timestamp}"
        pack_path = Path(output_path or self.runtime_base) / pack_name

        while pack_path.exists():
            import time

            time.sleep(0.001)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            pack_name = f"{self.strategy_name}_resources_{timestamp}"
            pack_path = Path(output_path or self.runtime_base) / pack_name

        shutil.copytree(self.strategy_dir, pack_path)

        manifest = {
            "strategy_name": self.strategy_name,
            "pack_time": timestamp,
            "input_resources": self.list_input_resources(),
            "output_resources": self.list_output_resources(),
        }

        with open(pack_path / "manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        return pack_path

    def get_resource_summary(self) -> Dict[str, any]:
        input_resources = self.list_input_resources()
        output_resources = self.list_output_resources()

        input_by_type = {}
        for rt in self.RESOURCE_TYPES["input"].keys():
            input_by_type[rt] = len([r for r in input_resources if r.get("type") == rt])

        output_by_type = {}
        for rt in self.RESOURCE_TYPES["output"].keys():
            output_by_type[rt] = len(
                [r for r in output_resources if r.get("type") == rt]
            )

        summary = {
            "strategy_name": self.strategy_name,
            "strategy_dir": str(self.strategy_dir),
            "input_dir": str(self.input_dir),
            "output_dir": str(self.output_dir),
            "input_resources": input_by_type,
            "output_resources": output_by_type,
            "total_input_files": len(input_resources),
            "total_output_files": len(output_resources),
        }
        return summary


def create_resource_pack(
    strategy_name: str,
    runtime_base: Optional[Union[str, Path]] = None,
) -> RuntimeResourcePack:
    pack = RuntimeResourcePack(
        strategy_name=strategy_name,
        runtime_base=runtime_base,
        auto_create=True,
    )
    RuntimeResourcePack.set_current_strategy_name(strategy_name)
    return pack


def get_current_resource_pack() -> Optional[RuntimeResourcePack]:
    strategy_name = RuntimeResourcePack._get_current_strategy_name()
    if strategy_name:
        return RuntimeResourcePack(strategy_name=strategy_name, auto_create=True)
    return None


def list_all_strategies(runtime_base: Optional[Union[str, Path]] = None) -> List[str]:
    base = Path(runtime_base or RuntimeResourcePack._get_default_runtime_base())
    if not base.exists():
        return []

    strategies = []
    for item in base.iterdir():
        if item.is_dir():
            if (item / "input").exists() or (item / "output").exists():
                strategies.append(item.name)

    return sorted(strategies)

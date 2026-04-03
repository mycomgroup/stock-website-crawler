"""
运行时 IO 与观测 API
实现聚宽平台的非交易型 API：
- record: 输出到结构化日志或 CSV
- send_message: 记录到日志（不实际发送消息）
- read_file: 从工作区安全目录读取文件
- write_file: 写入工作区安全目录

设计原则：
- 本地可运行且行为清楚
- 不允许随意越权访问工作区外路径
- 对不支持的参数明确报错
- 支持策略资源隔离，避免不同策略互相污染

资源管理增强：
- 支持策略级别的资源目录隔离
- 统一管理输入资源（模型、参数、数据）和输出资源（日志、交易记录）
- 通过 RuntimeResourcePack 提供更精细的资源管理能力
"""

import os
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Union
import threading

try:
    from ..strategy.runtime_resource_pack import RuntimeResourcePack
except ImportError:
    from jk2bt.strategy.runtime_resource_pack import RuntimeResourcePack

_RUNTIME_DIR = None
_RECORD_DATA = {}
_RECORD_LOCK = threading.Lock()
_MESSAGE_LOG = []
_CURRENT_STRATEGY_NAME = None
_RESOURCE_PACK = None


def _get_runtime_dir() -> Path:
    """获取运行时目录"""
    global _RUNTIME_DIR
    if _RUNTIME_DIR is None:
        # 使用 strategy_outputs 作为默认运行时目录
        # Path(__file__) = src/core/io.py
        # parent.parent.parent = 项目根目录
        base_dir = Path(__file__).parent.parent.parent / "strategy_outputs"
        base_dir.mkdir(parents=True, exist_ok=True)
        _RUNTIME_DIR = base_dir
    return _RUNTIME_DIR


def set_runtime_dir(path: Union[str, Path]) -> None:
    """设置运行时目录"""
    global _RUNTIME_DIR, _RESOURCE_PACK
    _RUNTIME_DIR = Path(path).resolve()
    _RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    _RESOURCE_PACK = None


def set_strategy_name(strategy_name: str) -> None:
    """
    设置当前策略名称，启用策略级别的资源隔离

    参数:
        strategy_name: 策略名称（用于创建独立的资源目录）

    效果:
        - 为策略创建独立的资源目录: strategy_outputs/<strategy_name>/
        - 所有 read_file/write_file 操作在该策略目录下进行
        - 避免不同策略互相污染资源

    示例:
        set_strategy_name("my_ml_strategy")
        # 后续 read_file/write_file 在 strategy_outputs/my_ml_strategy/ 下操作
    """
    global _CURRENT_STRATEGY_NAME, _RESOURCE_PACK, _RUNTIME_DIR
    _CURRENT_STRATEGY_NAME = strategy_name
    RuntimeResourcePack.set_current_strategy_name(strategy_name)

    # 直接使用 strategy_outputs 作为基础目录
    # RuntimeResourcePack._get_default_runtime_base() 返回 项目根目录/strategy_outputs
    base_runtime = RuntimeResourcePack._get_default_runtime_base()

    _RESOURCE_PACK = RuntimeResourcePack(
        strategy_name=strategy_name, runtime_base=base_runtime, auto_create=True
    )

    strategy_runtime_dir = _RESOURCE_PACK.strategy_dir
    _RUNTIME_DIR = strategy_runtime_dir


def get_current_strategy_name() -> Optional[str]:
    """获取当前策略名称"""
    global _CURRENT_STRATEGY_NAME
    return _CURRENT_STRATEGY_NAME


def get_resource_pack() -> Optional[RuntimeResourcePack]:
    """获取当前资源包实例"""
    global _RESOURCE_PACK
    return _RESOURCE_PACK


def _validate_path(filepath: str) -> Path:
    """验证文件路径安全性"""
    runtime_dir = _get_runtime_dir()
    target_path = (runtime_dir / filepath).resolve()

    if not str(target_path).startswith(str(runtime_dir.resolve())):
        raise ValueError(
            f"SecurityError: Access denied. Path '{filepath}' is outside the allowed runtime directory. "
            f"Allowed directory: {runtime_dir}"
        )

    return target_path


def record(
    *args, name: Optional[str] = None, date: Optional[datetime] = None, **kwargs
) -> None:
    """
    记录数据到结构化存储

    参数:
        *args: 要记录的值，按位置顺序记录
        name: 记录器名称（用于区分不同的记录流）
        date: 记录日期（默认使用当前日期）
        **kwargs: 要记录的键值对

    示例:
        record(price=100, volume=1000)
        record(100, 200, name="prices")
        record(high=105, low=95, close=100, date=datetime.now())

    实现:
        - 数据记录到内存字典
        - 同时写入 CSV 文件
        - 写入日志文件
    """
    global _RECORD_DATA, _RECORD_LOCK

    if date is None:
        date = datetime.now()
    elif isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d")

    record_name = name or "default"
    timestamp = date if isinstance(date, datetime) else datetime.now()

    with _RECORD_LOCK:
        if record_name not in _RECORD_DATA:
            _RECORD_DATA[record_name] = []

        record_entry = {
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "date": timestamp.strftime("%Y-%m-%d"),
        }

        for i, arg in enumerate(args):
            record_entry[f"arg_{i}"] = arg

        record_entry.update(kwargs)

        _RECORD_DATA[record_name].append(record_entry)

    csv_path = _get_runtime_dir() / f"record_{record_name}.csv"
    log_path = _get_runtime_dir() / f"record_{record_name}.log"

    file_exists = csv_path.exists()
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=record_entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(record_entry)

    log_entry = f"[{record_entry['timestamp']}] {kwargs}"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")


def send_message(
    title: str, content: Optional[str] = None, channel: str = "default", **kwargs
) -> None:
    """
    发送消息（本地运行时只记录到日志，不实际发送）

    参数:
        title: 消息标题
        content: 消息内容（可选）
        channel: 消息渠道（默认 default）
        **kwargs: 其他参数（不支持，会报错）

    示例:
        send_message("交易信号", "买入信号触发")
        send_message(title="警告", content="风险过高")

    注意:
        本地运行时不实际发送消息，仅记录到日志文件
    """
    if kwargs:
        unsupported = list(kwargs.keys())
        raise ValueError(
            f"send_message() does not support parameters: {unsupported}. "
            f"Supported parameters: title, content, channel"
        )

    global _MESSAGE_LOG

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_entry = {
        "timestamp": timestamp,
        "title": title,
        "content": content or "",
        "channel": channel,
    }

    _MESSAGE_LOG.append(message_entry)

    message_file = _get_runtime_dir() / "messages.log"
    with open(message_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [{channel}] {title}: {content or ''}\n")

    print(f"[SEND_MESSAGE] [{channel}] {title}: {content or ''}")


def read_file(filepath: str, mode: str = "rb", encoding: str = "utf-8") -> Union[str, bytes]:
    """
    从工作区安全目录读取文件

    参数:
        filepath: 相对于运行时目录的文件路径
        mode: 读取模式，只支持 'r' 和 'rb'（默认 'r')
        encoding: 文件编码（默认 'utf-8'，二进制模式忽略）

    返回:
        文件内容（字符串或字节）

    异常:
        ValueError: 路径越界或不支持的参数
        FileNotFoundError: 文件不存在

    示例:
        content = read_file("config.json")
        data = read_file("data.bin", mode="rb")

    安全限制:
        只能访问运行时目录下的文件，不允许访问上级目录或绝对路径

    资源隔离增强:
        - 如果设置了策略名称，文件路径在策略专属目录下
        - 支持智能路径映射，自动识别资源类型
    """
    if not filepath or filepath.strip() == "":
        raise ValueError(
            "read_file() filepath cannot be empty or whitespace. "
            "Please provide a valid relative file path."
        )

    if mode not in ("r", "rb"):
        raise ValueError(
            f"read_file() mode must be 'r' or 'rb', got '{mode}'. "
            f"Other modes are not supported for security reasons."
        )

    if encoding != "utf-8" and mode != "rb":
        raise ValueError(
            f"read_file() only supports 'utf-8' encoding, got '{encoding}'. "
            f"Use mode='rb' for binary files."
        )

    if os.path.isabs(filepath):
        raise ValueError(
            f"read_file() does not allow absolute paths. "
            f"Got: '{filepath}'. Use relative path under runtime directory."
        )

    if ".." in filepath:
        raise ValueError(
            f"read_file() does not allow parent directory references ('..'). "
            f"Got: '{filepath}'"
        )

    if _RESOURCE_PACK:
        return _read_file_with_resource_pack(filepath, mode)

    target_path = _validate_path(filepath)

    if not target_path.exists():
        raise FileNotFoundError(f"File not found: {filepath}. Full path: {target_path}")

    if mode == "rb":
        with open(target_path, "rb") as f:
            return f.read()
    else:
        with open(target_path, "r", encoding=encoding) as f:
            return f.read()


def _read_file_with_resource_pack(filepath: str, mode: str) -> Union[str, bytes]:
    """使用资源包读取文件，支持智能路径映射"""
    global _RESOURCE_PACK

    ext = Path(filepath).suffix.lower().lstrip(".")

    is_input_type = (
        ext in ["pkl", "h5", "pth", "pt", "onnx", "model", "bin"]
        or "model" in filepath.lower()
        or "train" in filepath.lower()
        or "test" in filepath.lower()
        or "config" in filepath.lower()
        or "param" in filepath.lower()
    )

    path_lower = filepath.lower()
    if any(
        kw in path_lower
        for kw in ["log", "trade", "signal", "output", "result", "record"]
    ):
        is_input_type = False

    try:
        if is_input_type:
            try:
                return _RESOURCE_PACK.read_input_resource(filepath, mode=mode)
            except FileNotFoundError:
                pass

        try:
            return _RESOURCE_PACK.read_output_resource(filepath, mode=mode)
        except FileNotFoundError:
            pass

        runtime_dir = _get_runtime_dir()
        direct_path = runtime_dir / filepath

        if direct_path.exists():
            if mode == "rb":
                with open(direct_path, "rb") as f:
                    return f.read()
            else:
                with open(direct_path, "r", encoding="utf-8") as f:
                    return f.read()

        raise FileNotFoundError(
            f"File not found in any resource location: {filepath}. "
            f"Checked: input/, output/, runtime_dir/"
        )
    except Exception as e:
        raise
    else:
        with open(target_path, "r", encoding=encoding) as f:
            return f.read()


def write_file(
    filepath: str, content: Union[str, bytes], mode: str = "w", encoding: str = "utf-8"
) -> None:
    """
    写入文件到工作区安全目录

    参数:
        filepath: 相对于运行时目录的文件路径
        content: 要写入的内容（字符串或字节）
        mode: 写入模式
            - 'w': 覆盖写入（默认）
            - 'a': 追加写入
            - 'wb': 二进制覆盖写入
            - 'ab': 二进制追加写入
        encoding: 文件编码（默认 'utf-8'，二进制模式忽略）

    异常:
        ValueError: 路径越界或不支持的参数

    示例:
        write_file("output.txt", "Hello World")
        write_file("log.txt", "\\nNew line", mode="a")
        write_file("data.bin", b"\\x00\\01", mode="wb")

    安全限制:
        只能访问运行时目录下的文件，不允许访问上级目录或绝对路径

    资源隔离增强:
        - 如果设置了策略名称，文件写入策略专属目录
        - 支持智能路径映射，自动识别资源类型
        - 默认写入 output 目录，除非文件名明确暗示是输入资源
    """
    if not filepath or filepath.strip() == "":
        raise ValueError(
            "write_file() filepath cannot be empty or whitespace. "
            "Please provide a valid relative file path."
        )

    if mode not in ("w", "a", "wb", "ab"):
        raise ValueError(
            f"write_file() mode must be 'w', 'a', 'wb', or 'ab', got '{mode}'. "
            f"Other modes are not supported for security reasons."
        )

    if encoding != "utf-8" and not mode.endswith("b"):
        raise ValueError(
            f"write_file() only supports 'utf-8' encoding, got '{encoding}'. "
            f"Use binary mode ('wb'/'ab') for binary data."
        )

    if os.path.isabs(filepath):
        raise ValueError(
            f"write_file() does not allow absolute paths. "
            f"Got: '{filepath}'. Use relative path under runtime directory."
        )

    if ".." in filepath:
        raise ValueError(
            f"write_file() does not allow parent directory references ('..'). "
            f"Got: '{filepath}'"
        )

    if _RESOURCE_PACK:
        _write_file_with_resource_pack(filepath, content, mode)
        return

    target_path = _validate_path(filepath)

    target_path.parent.mkdir(parents=True, exist_ok=True)

    is_binary = mode.endswith("b")
    actual_mode = mode if is_binary else mode

    if is_binary:
        if not isinstance(content, bytes):
            raise ValueError(
                f"write_file() with binary mode requires bytes content, "
                f"got {type(content).__name__}"
            )
        with open(target_path, actual_mode) as f:
            f.write(content)
    else:
        if not isinstance(content, str):
            raise ValueError(
                f"write_file() with text mode requires str content, "
                f"got {type(content).__name__}"
            )
        with open(target_path, actual_mode, encoding=encoding) as f:
            f.write(content)


def _write_file_with_resource_pack(
    filepath: str, content: Union[str, bytes], mode: str
) -> None:
    """使用资源包写入文件，支持智能路径映射"""
    global _RESOURCE_PACK

    ext = Path(filepath).suffix.lower().lstrip(".")
    path_lower = filepath.lower()

    is_output_type = any(
        kw in path_lower
        for kw in [
            "log",
            "trade",
            "signal",
            "output",
            "result",
            "record",
            "nav",
            "message",
        ]
    )

    is_input_type = not is_output_type and (
        ext in ["pkl", "h5", "pth", "pt", "onnx", "model", "bin"]
        or "model" in path_lower
        or "config" in path_lower
        or "param" in path_lower
        or "train" in path_lower
        or "test" in path_lower
    )

    if is_output_type:
        _RESOURCE_PACK.write_output_resource(filepath, content, mode=mode)
    elif is_input_type:
        _RESOURCE_PACK.write_input_resource(filepath, content, mode=mode)
    else:
        runtime_dir = _get_runtime_dir()
        target_path = runtime_dir / filepath
        target_path.parent.mkdir(parents=True, exist_ok=True)

        is_binary = mode.endswith("b")
        if is_binary:
            with open(target_path, mode) as f:
                f.write(content)
        else:
            with open(target_path, mode, encoding="utf-8") as f:
                f.write(content)


def get_record_data(name: Optional[str] = None) -> dict:
    """
    获取已记录的数据

    参数:
        name: 记录器名称（None 返回全部）

    返回:
        记录的数据字典
    """
    with _RECORD_LOCK:
        if name:
            return _RECORD_DATA.get(name, [])
        return dict(_RECORD_DATA)


def get_messages() -> list:
    """
    获取所有发送的消息

    返回:
        消息列表
    """
    return list(_MESSAGE_LOG)


def clear_runtime_data() -> None:
    """清空运行时数据（用于测试）"""
    global _RECORD_DATA, _MESSAGE_LOG
    with _RECORD_LOCK:
        _RECORD_DATA = {}
        _MESSAGE_LOG = []


def export_records_to_csv(output_dir: Optional[str] = None) -> dict:
    """
    导出所有记录到 CSV 文件

    参数:
        output_dir: 输出目录（默认使用运行时目录）

    返回:
        导出的文件路径字典
    """
    output_path = Path(output_dir) if output_dir else _get_runtime_dir()
    output_path.mkdir(parents=True, exist_ok=True)

    exported_files = {}

    with _RECORD_LOCK:
        for name, records in _RECORD_DATA.items():
            if not records:
                continue

            csv_path = output_path / f"export_{name}.csv"

            all_keys = set()
            for record in records:
                all_keys.update(record.keys())

            fieldnames = sorted(all_keys)

            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(records)

            exported_files[name] = str(csv_path)

    return exported_files

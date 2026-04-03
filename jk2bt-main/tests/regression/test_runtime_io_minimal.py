"""
最小策略验证 runtime IO API
"""

from jk2bt.core.io import (
    record,
    send_message,
    read_file,
    write_file,
    set_runtime_dir,
    clear_runtime_data,
    get_record_data,
    get_messages,
)
import tempfile
import os
from datetime import datetime


def validate_runtime_io_api():
    """
    验证 runtime IO API 的最小策略

    测试:
    - record 产生日志
    - send_message 被记录
    - write_file 写出文件
    - read_file 能读回
    """
    temp_dir = tempfile.mkdtemp()
    set_runtime_dir(temp_dir)
    clear_runtime_data()

    print("=" * 60)
    print("验证 Runtime IO API")
    print("=" * 60)

    # 1. 测试 record
    print("\n[1] 测试 record API...")
    record(name="strategy_metrics", date=datetime(2023, 1, 1), nav=1.0, return_rate=0.0)
    record(
        name="strategy_metrics", date=datetime(2023, 1, 2), nav=1.05, return_rate=0.05
    )
    record(
        name="strategy_metrics", date=datetime(2023, 1, 3), nav=1.02, return_rate=0.02
    )

    data = get_record_data("strategy_metrics")
    assert len(data) == 3, f"Expected 3 records, got {len(data)}"
    assert data[0]["nav"] == 1.0
    assert data[1]["return_rate"] == 0.05
    print(f"    ✓ record 成功记录 3 条数据")

    csv_path = os.path.join(temp_dir, "record_strategy_metrics.csv")
    assert os.path.exists(csv_path), "CSV file should exist"
    print(f"    ✓ CSV 文件已生成: {csv_path}")

    # 2. 测试 send_message
    print("\n[2] 测试 send_message API...")
    send_message("交易信号", "买入信号触发", channel="trading")
    send_message("风控警告", "仓位超过 80%", channel="risk")

    messages = get_messages()
    assert len(messages) == 2, f"Expected 2 messages, got {len(messages)}"
    assert messages[0]["title"] == "交易信号"
    assert messages[1]["channel"] == "risk"
    print(f"    ✓ send_message 成功记录 2 条消息")

    msg_log_path = os.path.join(temp_dir, "messages.log")
    assert os.path.exists(msg_log_path), "Messages log should exist"
    print(f"    ✓ 消息日志已生成: {msg_log_path}")

    # 3. 测试 write_file
    print("\n[3] 测试 write_file API...")
    config_content = """{
    "strategy_name": "test_strategy",
    "max_position": 0.8,
    "stop_loss": 0.05
}"""
    write_file("config/strategy_config.json", config_content)

    config_path = os.path.join(temp_dir, "config", "strategy_config.json")
    assert os.path.exists(config_path), "Config file should exist"
    print(f"    ✓ 配置文件已写入: {config_path}")

    # 测试追加模式
    write_file("logs/trade_log.txt", "2023-01-01: BUY 600519.XSHG 100@100.5\n")
    write_file(
        "logs/trade_log.txt", "2023-01-02: SELL 600519.XSHG 100@102.0\n", mode="a"
    )

    trade_log_path = os.path.join(temp_dir, "logs", "trade_log.txt")
    assert os.path.exists(trade_log_path), "Trade log should exist"
    print(f"    ✓ 交易日志已写入（追加模式）: {trade_log_path}")

    # 4. 测试 read_file
    print("\n[4] 测试 read_file API...")
    read_config = read_file("config/strategy_config.json")
    assert "strategy_name" in read_config, "Should contain strategy_name"
    assert read_config == config_content, "Content should match"
    print(f"    ✓ 成功读取配置文件")

    read_trade_log = read_file("logs/trade_log.txt")
    assert "BUY 600519.XSHG" in read_trade_log, "Should contain buy record"
    assert "SELL 600519.XSHG" in read_trade_log, "Should contain sell record"
    print(f"    ✓ 成功读取交易日志")

    # 5. 测试二进制文件
    print("\n[5] 测试二进制文件读写...")
    binary_data = bytes([0x00, 0x01, 0x02, 0xFF, 0xFE])
    write_file("data/binary.bin", binary_data, mode="wb")
    read_binary = read_file("data/binary.bin", mode="rb")
    assert read_binary == binary_data, "Binary content should match"
    print(f"    ✓ 二进制文件读写成功")

    # 6. 验证安全边界
    print("\n[6] 验证安全边界...")
    try:
        read_file("/etc/passwd")
        assert False, "Should have raised ValueError for absolute path"
    except ValueError as e:
        assert "absolute paths" in str(e)
        print(f"    ✓ 正确拒绝绝对路径访问")

    try:
        read_file("../../secrets.txt")
        assert False, "Should have raised ValueError for parent dir"
    except ValueError as e:
        assert "parent directory" in str(e)
        print(f"    ✓ 正确拒绝上级目录访问")

    print("\n" + "=" * 60)
    print("所有 Runtime IO API 验证通过!")
    print("=" * 60)

    print("\n生成的文件:")
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, temp_dir)
            print(f"  - {rel_path}")

    return True


if __name__ == "__main__":
    validate_runtime_io_api()

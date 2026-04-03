"""
Runtime IO API 使用示例
演示如何在策略中使用 record, send_message, read_file, write_file
"""

from datetime import datetime
import tempfile
import os

from jk2bt.runtime_io import (
    record,
    send_message,
    read_file,
    write_file,
    set_runtime_dir,
    get_record_data,
    get_messages,
)


def demo_runtime_io():
    temp_dir = tempfile.mkdtemp()
    set_runtime_dir(temp_dir)

    print("=" * 60)
    print("Runtime IO API 使用示例")
    print("=" * 60)

    print("\n[示例 1] 使用 record 记录策略指标")
    print("-" * 60)
    record(
        name="nav_metrics",
        date=datetime(2023, 1, 1),
        nav=1.0,
        returns=0.0,
        drawdown=0.0,
    )
    record(
        name="nav_metrics",
        date=datetime(2023, 1, 2),
        nav=1.02,
        returns=0.02,
        drawdown=-0.01,
    )
    record(
        name="nav_metrics",
        date=datetime(2023, 1, 3),
        nav=1.01,
        returns=0.01,
        drawdown=-0.02,
    )

    csv_path = os.path.join(temp_dir, "record_nav_metrics.csv")
    with open(csv_path, "r") as f:
        print(f.read())

    print("\n[示例 2] 使用 send_message 发送通知")
    print("-" * 60)
    send_message("策略启动", "策略开始运行，初始资金 100万", channel="system")
    send_message("风险警告", "仓位超过 80%，建议减仓", channel="risk_management")
    send_message("交易完成", "买入 600519.XSHG 100股@100.5", channel="trading")

    msg_log = os.path.join(temp_dir, "messages.log")
    with open(msg_log, "r") as f:
        print(f.read())

    print("\n[示例 3] 使用 write_file 写入配置")
    print("-" * 60)
    config = """{
    "strategy_name": "demo_strategy",
    "max_position": 0.8,
    "stop_loss": 0.05,
    "take_profit": 0.15
}"""
    write_file("config/strategy_config.json", config)
    print(f"配置已写入: {os.path.join(temp_dir, 'config', 'strategy_config.json')}")

    print("\n[示例 4] 使用 read_file 读取配置")
    print("-" * 60)
    read_config = read_file("config/strategy_config.json")
    print(read_config)

    print("\n[示例 5] 记录交易日志（追加模式）")
    print("-" * 60)
    write_file(
        "trades/trade_log.txt", "2023-01-01 09:30:00 | BUY 600519.XSHG 100股@100.5\n"
    )
    write_file(
        "trades/trade_log.txt",
        "2023-01-01 10:15:00 | SELL 600519.XSHG 50股@102.0\n",
        mode="a",
    )
    write_file(
        "trades/trade_log.txt",
        "2023-01-02 09:30:00 | BUY 000858.XSHE 200股@50.0\n",
        mode="a",
    )

    trade_log = read_file("trades/trade_log.txt")
    print(trade_log)

    print("\n[示例 6] 查询记录数据")
    print("-" * 60)
    nav_data = get_record_data("nav_metrics")
    print(f"记录了 {len(nav_data)} 条 NAV 数据")
    for entry in nav_data:
        print(f"  {entry['date']}: NAV={entry['nav']}, Returns={entry['returns']}")

    print("\n[示例 7] 查询发送的消息")
    print("-" * 60)
    messages = get_messages()
    print(f"发送了 {len(messages)} 条消息")
    for msg in messages:
        print(f"  [{msg['channel']}] {msg['title']}: {msg['content']}")

    print("\n" + "=" * 60)
    print("所有文件列表:")
    print("=" * 60)
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, temp_dir)
            print(f"  {rel_path}")

    print("\n运行时目录:", temp_dir)


if __name__ == "__main__":
    demo_runtime_io()

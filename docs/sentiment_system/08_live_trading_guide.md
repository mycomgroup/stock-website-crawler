# 实盘接口指南

本文档说明如何在实盘环境中使用情绪监控系统。

---

## 一、数据源选择

### 1.1 免费数据源

| 数据源 | 涨停数据 | 延迟 | 稳定性 | 推荐度 |
|--------|----------|------|--------|--------|
| 东方财富 | ✅ 有 | 低 | 高 | ⭐⭐⭐⭐⭐ |
| 新浪财经 | ✅ 有 | 低 | 中 | ⭐⭐⭐⭐ |
| 腾讯财经 | ⚠️ 有限 | 中 | 中 | ⭐⭐⭐ |
| Wind | ✅ 完整 | 低 | 高 | ⭐⭐⭐⭐⭐（付费） |

### 1.2 推荐配置

```python
# 生产环境推荐
data_source = EastMoneyDataSource()  # 免费，稳定

# 高要求场景
data_source = TushareDataSource(token=os.environ['TUSHARE_TOKEN'])  # 需要付费
```

---

## 二、东方财富API详解

### 2.1 涨停板接口

```python
import requests

def get_zt_count_eastmoney(date=None):
    """
    从东方财富获取涨停家数
    
    接口: http://push2.eastmoney.com/api/qt/clist/get
    """
    url = "http://push2.eastmoney.com/api/qt/clist/get"
    
    params = {
        'fid': 'f3',          # 按涨幅排序
        'po': '1',            # 降序
        'pz': '500',          # 每页500条
        'pn': '1',            # 第1页
        'np': '1',
        'fltt': '2',
        'invt': '2',
        # 筛选条件：沪深A股
        'fs': 'm:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23',
        'fields': 'f12,f14,f2,f3,f62,f184',  # 代码,名称,现价,涨幅,...
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, params=params, headers=headers, timeout=10)
    data = response.json()
    
    if data.get('data') and data['data'].get('diff'):
        # 筛选涨幅>=9.8%（涨停）
        zt_stocks = [
            s for s in data['data']['diff']
            if float(s.get('f3', 0)) >= 9.8
        ]
        return len(zt_stocks)
    
    return 0
```

### 2.2 完整数据源类

```python
class EastMoneyDataSource:
    """
    东方财富数据源
    
    优点:
    - 免费
    - 数据完整
    - 稳定性好
    
    缺点:
    - 无历史数据
    - 仅限当日
    """
    
    def __init__(self):
        self.base_url = "http://push2.eastmoney.com/api/qt/clist/get"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def _request(self, params):
        """发送请求"""
        response = requests.get(
            self.base_url, 
            params=params, 
            headers=self.headers, 
            timeout=10
        )
        return response.json()
    
    def get_zt_count(self, date=None):
        """获取涨停家数"""
        params = {
            'fid': 'f3',
            'po': '1',
            'pz': '500',
            'pn': '1',
            'np': '1',
            'fltt': '2',
            'invt': '2',
            'fs': 'm:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23',
            'fields': 'f12,f14,f2,f3',
        }
        
        data = self._request(params)
        
        if data.get('data') and data['data'].get('diff'):
            zt_stocks = [
                s for s in data['data']['diff']
                if float(s.get('f3', 0)) >= 9.8
            ]
            return len(zt_stocks)
        
        return 0
    
    def get_dt_count(self, date=None):
        """获取跌停家数"""
        params = {
            'fid': 'f3',
            'po': '1',
            'pz': '500',
            'pn': '1',
            'np': '1',
            'fltt': '2',
            'invt': '2',
            'fs': 'm:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23',
            'fields': 'f12,f14,f2,f3',
        }
        
        data = self._request(params)
        
        if data.get('data') and data['data'].get('diff'):
            dt_stocks = [
                s for s in data['data']['diff']
                if float(s.get('f3', 0)) <= -9.8
            ]
            return len(dt_stocks)
        
        return 0
```

---

## 三、定时任务配置

### 3.1 每日执行时间

| 时间点 | 任务 | 说明 |
|--------|------|------|
| 09:00 | 盘前检查 | 计算情绪，决定是否开仓 |
| 09:20 | 竞价确认 | 确认开盘前情绪 |
| 13:00 | 盘中监控 | 检查炸板等情况 |
| 14:30 | 收盘前检查 | 决定是否持有到收盘 |
| 15:30 | 收盘复盘 | 记录今日数据 |

### 3.2 schedule模块使用

```python
import schedule
import time

def job_morning():
    """盘前任务"""
    from live_sentiment_monitor import SentimentMonitor, EastMoneyDataSource
    
    monitor = SentimentMonitor(
        data_source=EastMoneyDataSource(),
        threshold=30
    )
    
    result = monitor.check()
    print(f"涨停: {result['zt_count']}, 建议: {result['action']}")
    
    # 发送通知
    monitor.alert(result)

def job_noon():
    """盘中监控"""
    # 检查炸板情况
    pass

def job_evening():
    """收盘复盘"""
    # 记录数据
    pass

# 定时任务设置
schedule.every().day.at("09:00").do(job_morning)
schedule.every().day.at("13:00").do(job_noon)
schedule.every().day.at("15:30").do(job_evening)

# 主循环
while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 四、告警通知配置

### 4.1 Server酱（微信）

```python
import os

# 1. 注册: https://sct.ftqq.com/
# 2. 获取SendKey
# 3. 设置环境变量
SERVERCHAN_KEY = os.environ.get('SERVERCHAN_KEY', 'your_key_here')

def send_wechat(title, content):
    """发送微信通知"""
    import requests
    
    url = f"https://sctapi.ftqq.com/{SERVERCHAN_KEY}.send"
    
    data = {
        'title': title,
        'desp': content
    }
    
    response = requests.post(url, data=data)
    return response.json().get('code') == 0
```

### 4.2 钉钉机器人

```python
import os

# 1. 创建钉钉群
# 2. 添加自定义机器人
# 3. 获取Webhook URL
DINGTALK_WEBHOOK = os.environ.get('DINGTALK_WEBHOOK', 'your_webhook_here')

def send_dingtalk(title, content):
    """发送钉钉通知"""
    import requests
    
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": f"## {title}\n\n{content}"
        }
    }
    
    response = requests.post(
        DINGTALK_WEBHOOK,
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    
    return response.json().get('errcode') == 0
```

### 4.3 邮件通知

```python
import smtplib
from email.mime.text import MIMEText

def send_email(title, content, 
               smtp_server='smtp.gmail.com',
               smtp_port=587,
               sender='your_email@gmail.com',
               password='your_password',
               receiver='receiver@example.com'):
    """发送邮件"""
    
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = title
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()
```

---

## 五、完整实盘监控示例

```python
#!/usr/bin/env python3
"""
实盘情绪监控完整示例

功能:
1. 每日09:00自动检查情绪
2. 根据阈值发送告警
3. 记录历史数据

使用方法:
    python live_monitor.py --threshold 30 --notify wechat
"""

import argparse
import json
import os
from datetime import datetime

# 导入监控模块
import sys
sys.path.append('/path/to/sentiment_system/code/live')
from live_sentiment_monitor import (
    EastMoneyDataSource,
    SentimentMonitor,
    WeChatNotifier,
    DingTalkNotifier
)


def load_config():
    """加载配置"""
    config_file = os.path.expanduser('~/.sentiment_config.json')
    
    if os.path.exists(config_file):
        with open(config_file) as f:
            return json.load(f)
    
    return {}


def save_config(config):
    """保存配置"""
    config_file = os.path.expanduser('~/.sentiment_config.json')
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='实盘情绪监控')
    parser.add_argument('--threshold', type=int, default=30,
                       help='涨停阈值，默认30')
    parser.add_argument('--notify', choices=['wechat', 'dingtalk', 'none'],
                       default='none', help='通知方式')
    parser.add_argument('--once', action='store_true',
                       help='只执行一次，不持续监控')
    args = parser.parse_args()
    
    # 加载配置
    config = load_config()
    
    # 创建数据源
    data_source = EastMoneyDataSource()
    
    # 创建通知器
    notifier = None
    if args.notify == 'wechat':
        key = os.environ.get('SERVERCHAN_KEY', config.get('serverchan_key'))
        if key:
            notifier = WeChatNotifier(key)
    elif args.notify == 'dingtalk':
        webhook = os.environ.get('DINGTALK_WEBHOOK', config.get('dingtalk_webhook'))
        if webhook:
            notifier = DingTalkNotifier(webhook)
    
    # 创建监控器
    monitor = SentimentMonitor(
        data_source=data_source,
        notifier=notifier,
        threshold=args.threshold
    )
    
    # 执行检查
    result = monitor.check()
    
    # 输出结果
    print("\n" + "=" * 50)
    print(f"  实盘情绪监控 - {result['time']}")
    print("=" * 50)
    print(f"  涨停家数: {result['zt_count']}")
    print(f"  跌停家数: {result['dt_count']}")
    print(f"  涨跌停比: {result['zt_dt_ratio']}")
    print(f"  状态: {result['status']}")
    print(f"  建议: {result['action']}")
    print(f"  阈值: {result['threshold']}")
    print("=" * 50)
    
    # 发送告警
    if result['status'] == 'bad' and notifier:
        monitor.alert(result)
        print("\n[已发送告警]")
    
    # 保存历史
    history_file = os.path.expanduser('~/.sentiment_history.json')
    history = []
    if os.path.exists(history_file):
        with open(history_file) as f:
            history = json.load(f)
    
    history.append(result)
    
    # 只保留最近100条
    history = history[-100:]
    
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)
    
    print(f"\n历史记录已保存到: {history_file}")


if __name__ == '__main__':
    main()
```

---

## 六、Docker部署（可选）

### 6.1 Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "live_monitor.py", "--threshold", "30", "--notify", "wechat"]
```

### 6.2 requirements.txt

```
requests>=2.28.0
schedule>=1.1.0
pandas>=1.4.0
```

### 6.3 使用方法

```bash
# 构建镜像
docker build -t sentiment-monitor .

# 运行容器
docker run -d \
  -e SERVERCHAN_KEY=your_key \
  sentiment-monitor:latest \
  python live_monitor.py --threshold 30 --notify wechat
```

---

## 七、故障排查

### 7.1 常见问题

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 请求超时 | 网络问题 | 增加timeout |
| 数据为空 | 接口变更 | 检查接口参数 |
| 通知失败 | SendKey错误 | 检查KEY |
| 进程退出 | 异常未捕获 | 添加异常处理 |

### 7.2 日志记录

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='/var/log/sentiment_monitor.log'
)

logger = logging.getLogger(__name__)

try:
    result = monitor.check()
    logger.info(f"检查完成: {result}")
except Exception as e:
    logger.error(f"检查失败: {e}")
```
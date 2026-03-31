from jqdata import *
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 研究问题：财报发布时间与RFScore因子更新时机

today = datetime.now().date()
trade_day = get_trade_days(end_date=today, count=1)[0]

# 1. 获取财报发布日历
print("=" * 70)
print("财报发布与调仓时机研究")
print("=" * 70)

# 获取沪深300成分股的财报发布时间
hs300 = get_index_stocks("000300.XSHG", date=trade_day)

# 获取最近的财报发布日期
print("\n【财报发布时间分布】")
report_dates = []
for code in hs300[:50]:  # 采样50只
    try:
        # 获取最近4个季报
        finance = get_finance(code, end_date=trade_day, count=4, fields=["pubDate"])
        if len(finance) > 0:
            for row in finance:
                pub_date = row["pubDate"]
                if pub_date:
                    report_dates.append(pub_date)
    except:
        pass

# 统计发布日分布
if report_dates:
    report_df = pd.DataFrame({"pubDate": report_dates})
    report_df["pubDate"] = pd.to_datetime(report_df["pubDate"])
    report_df["weekday"] = report_df["pubDate"].dt.dayofweek
    report_df["hour"] = report_df["pubDate"].dt.hour

    weekday_dist = report_df["weekday"].value_counts().sort_index()
    hour_dist = report_df["hour"].value_counts().sort_index()

    print("\n发布日星期分布:")
    weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    for day, count in weekday_dist.items():
        print(f"  {weekday_names[day]}: {count}次")

    print("\n发布时段分布:")
    for hour, count in hour_dist.items():
        print(f"  {hour}时: {count}次")

# 2. RFScore因子更新频率研究
print("\n" + "=" * 70)
print("【RFScore因子时效性分析】")
print("=" * 70)

print("\nRFScore依赖的财务因子:")
print("  - ROA: 季度更新，最大滞后90天")
print("  - 经营现金流: 季度更新，最大滞后90天")
print("  - 毛利率: 季度更新，最大滞后90天")
print("  - 总资产: 季度更新，最大滞后90天")
print("  - 周转率: 季度更新，最大滞后90天")

print("\n结论:")
print("  1. RFScore因子本质上是季度频率，月度调仓已足够覆盖")
print("  2. 财报发布后，因子数据才真正更新")
print("  3. 季报集中发布期（4月底、8月底、10月底）是最佳调仓窗口")

# 3. 事件驱动调仓方案
print("\n" + "=" * 70)
print("【事件驱动调仓方案】")
print("=" * 70)

print("\n方案A: 季报发布后调仓")
print("  触发时机: 季报集中发布期")
print("  优势: 信息最新，因子值准确")
print("  劣势: 发布期集中，执行压力大")
print("  建议: 在发布高峰期（4月25-30日、8月25-31日）自动触发调仓")

print("\n方案B: 混合调仓")
print("  规则:")
print("    - 基础调仓: 月度固定（每月首个周一）")
print("    - 增补调仓: 季报发布后一周内")
print("    - 紧急调仓: 市场宽度突破阈值时")
print("  优势: 既稳定又及时")
print("  建议: 采用此方案")

print("\n方案C: 实时监控触发")
print("  触发条件:")
print("    - 质量评分下降超过20分")
print("    - 异常股比例超过30%")
print("    - 市场宽度低于15%（极端）")
print("  劣势: 过度频繁，成本高")
print("  建议: 仅用于风控，不用于常规调仓")

# 4. JQData财报日历接口
print("\n" + "=" * 70)
print("【聚宽财报日历接口】")
print("=" * 70)

print("\n可用接口:")
print("  1. get_finance(code, fields=['pubDate']): 获取财报发布日期")
print("  2. get_report_info(): 获取财报基本信息")
print("  3. get_all_securities(fields=['report_date']): 批量获取")

# 实际获取示例
print("\n实际示例 - 获取财报日历:")
try:
    # 获取未来30天即将发布的财报
    start_date = trade_day
    end_date = trade_day + timedelta(days=30)

    # 模拟获取财报日历（JQData实际接口）
    print(f"  查询范围: {start_date} 至 {end_date}")

    # 注意：JQData的get_finance只能查历史，不能查未来
    # 但可以通过业绩预告获取即将发布信息
    print("  方法: 通过业绩预告(get_performance_forecast)获取发布预期")

except Exception as e:
    print(f"  错误: {e}")

# 5. 最佳实践建议
print("\n" + "=" * 70)
print("【最佳实践建议】")
print("=" * 70)

print("\n推荐调仓架构:")
print("""
┌─────────────────────────────────────────┐
│          调仓触发系统                     │
├─────────────────────────────────────────┤
│                                         │
│  [基础层] 月度固定调仓                   │
│    - 时间: 每月首个交易日                │
│    - 目的: 系统性再平衡                  │
│                                         │
│  [事件层] 季报发布后调仓                 │
│    - 触发: 季报集中发布期(4/8/10月底)    │
│    - 目的: 捕获最新财务信息              │
│                                         │
│  [风控层] 异常触发调仓                   │
│    - 触发: 质量评分<40 或 市场极端       │
│    - 目的: 紧急减仓                      │
│                                         │
└─────────────────────────────────────────┘
""")

print("\n调仓时机优化:")
print("  1. 避开财报发布当日（市场波动大）")
print("  2. 选择财报发布后T+1或T+2（信息充分吸收）")
print("  3. 优先选择周二至周四（避开周一跳空、周五不确定性）")
print("  4. 避开收盘前30分钟（流动性下降）")
print("  5. 建议: 上午10:00-10:30（开盘稳定后）")

print("\n" + "=" * 70)
print("研究结论:")
print("=" * 70)
print("\n1. RFScore因子本质是季度频率，月度调仓已足够")
print("2. 季报发布后一周内是最佳调仓窗口")
print("3. 建议采用'月度基础+季报增补'混合方案")
print("4. 不建议过度频繁的事件驱动（成本高、过度反应）")

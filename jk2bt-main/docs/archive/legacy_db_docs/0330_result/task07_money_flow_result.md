# Task 07 Result

## 修改文件
- `jqdata_akshare_backtrader_utility/market_data/money_flow.py` - 改进稳定 schema 支持
- `tests/test_money_flow.py` - 新建正式 pytest 测试文件

## 完成内容

### 1. `get_money_flow` 接口功能
- 支持常见参数：
  - `security_list`（标的，支持单标的或多标的）
  - `start_date` / `end_date`（日期区间）
  - `count`（最近 N 天数据）
  - `fields`（字段过滤）
- 返回 `DataFrame`

### 2. 支持字段
- `sec_code` - 标准化股票代码
- `date` - 日期
- `close` - 收盘价
- `change_pct` - 涨跌幅
- `net_amount_main` - 主力净流入金额
- `net_pct_main` - 主力净流入占比
- `net_amount_xl` / `net_pct_xl` - 超大单
- `net_amount_l` / `net_pct_l` - 大单
- `net_amount_m` / `net_pct_m` - 中单
- `net_amount_s` / `net_pct_s` - 小单

### 3. 字段名标准化
- 自动处理 AkShare 原始字段名映射
- `COLUMN_MAP` 实现中文名 -> 英文名转换

### 4. 稳定 Schema 支持
- 新增 `DEFAULT_SCHEMA` 常量
- 新增 `_get_empty_dataframe()` 函数
- 离线或失败时返回带稳定列名的空 DataFrame
- 空表仍保持完整字段列表，便于后续操作

### 5. 股票代码格式兼容
- 聚宽格式：`600519.XSHG` / `000001.XSHE`
- 前缀格式：`sh600519` / `sz000001` / `bj430001`
- 纯数字格式：`600519` / `000001`

## 验证命令
```bash
python3 -m pytest tests/test_money_flow.py -v
```

## 验证结果
```
======================== 24 passed, 3 warnings in 7.59s =========================
```

测试覆盖：
- 基础查询（单标的、多标的）
- 字段过滤（单字段、多字段）
- 日期区间和 count 参数
- 股票代码格式兼容
- 稳定 schema（空列表、无效代码、离线模式）
- DataFrame 操作（筛选、分组、pivot）
- 位置参数兼容
- 策略集成测试

## 已知边界
1. 数据依赖 AkShare，网络不可用时会返回空表
2. 历史数据受 AkShare 数据源限制
3. 不覆盖北向资金和龙虎榜（已明确排除）
4. 新股/次新股可能无历史资金流数据
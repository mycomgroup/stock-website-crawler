# OSS 因子文件下载工具使用说明

## 功能概述

这个工具用于从阿里云 OSS 下载按年份组织的因子文件，支持：
- 按日期范围下载（每天一个文件）
- 按年份下载（下载整年的所有文件）
- 检查文件是否存在
- 列出指定目录下的所有文件

## OSS 文件结构

```
uploads/factors/
├── 2024/
│   ├── factors_20240101.parquet
│   ├── factors_20240102.parquet
│   ├── factors_20240103.parquet
│   └── ...
├── 2025/
│   ├── factors_20250101.parquet
│   ├── factors_20250102.parquet
│   └── ...
└── ...
```

## 配置

确保 `.env` 文件包含以下配置：

```bash
# OSS配置
OSS_ACCESS_KEY_ID=your_access_key_id
OSS_ACCESS_KEY_SECRET=your_access_key_secret
OSS_ENDPOINT=https://oss-cn-hangzhou.aliyuncs.com
OSS_BUCKET_NAME=your_bucket_name
```

## 安装依赖

```bash
pip install oss2 python-dotenv
```

## 使用示例

### 1. 下载指定日期范围的因子文件

```python
from download_oss import download_daily_factors

# 下载 2024年1月1日 到 2024年1月7日 的因子文件
count = download_daily_factors(
    start_date="2024-01-01",      # 开始日期
    end_date="2024-01-07",        # 结束日期
    oss_base_prefix="uploads/factors/",  # OSS 基础路径
    local_base_dir="./data/factors/",    # 本地保存目录
    file_pattern="factors_{date}.parquet"  # 文件名模式
)
print(f"成功下载 {count} 个文件")
```

**下载结果：**
```
./data/factors/
├── 2024/
│   ├── factors_20240101.parquet
│   ├── factors_20240102.parquet
│   ├── factors_20240103.parquet
│   ├── factors_20240104.parquet
│   ├── factors_20240105.parquet
│   ├── factors_20240106.parquet
│   └── factors_20240107.parquet
```

### 2. 下载整年的因子文件

```python
from download_oss import download_year_factors

# 下载 2024 年的所有因子文件
count = download_year_factors(
    year=2024,
    oss_base_prefix="uploads/factors/",
    local_base_dir="./data/factors/"
)
print(f"成功下载 {count} 个文件")
```

### 3. 检查文件是否存在

```python
from download_oss import check_file_exists

# 检查文件是否存在
oss_path = "uploads/factors/2024/factors_20240101.parquet"
exists = check_file_exists(oss_path)
print(f"文件 {oss_path} {'存在' if exists else '不存在'}")
```

### 4. 列出目录下的所有文件

```python
from download_oss import list_oss_files

# 列出 2024 年的所有因子文件
files = list_oss_files(prefix="uploads/factors/2024/", max_keys=100)
print(f"找到 {len(files)} 个文件:")
for f in files[:10]:  # 只显示前10个
    print(f"  - {f}")
```

## 快速测试

运行测试脚本：

```bash
# 运行完整的示例（在 download_oss.py 中）
python download_oss.py

# 运行测试脚本
python test_download_oss.py
```

## 函数参数说明

### `download_daily_factors()`

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `start_date` | str | 开始日期，格式 'YYYY-MM-DD' 或 'YYYYMMDD' | 必填 |
| `end_date` | str | 结束日期，格式 'YYYY-MM-DD' 或 'YYYYMMDD' | 必填 |
| `oss_base_prefix` | str | OSS 基础路径前缀 | "uploads/factors/" |
| `local_base_dir` | str | 本地保存基础目录 | "./data/factors/" |
| `file_pattern` | str | 文件名模式，{date} 会被替换为日期 | "factors_{date}.parquet" |

**返回值：** 成功下载的文件数量

### `download_year_factors()`

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `year` | int | 年份 | 必填 |
| `oss_base_prefix` | str | OSS 基础路径前缀 | "uploads/factors/" |
| `local_base_dir` | str | 本地保存基础目录 | "./data/factors/" |

**返回值：** 成功下载的文件数量

### `check_file_exists()`

| 参数 | 类型 | 说明 |
|------|------|------|
| `oss_path` | str | OSS 文件路径 |

**返回值：** 文件是否存在（bool）

### `list_oss_files()`

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `prefix` | str | OSS 文件前缀 | "uploads/" |
| `max_keys` | int | 每次请求返回的最大文件数 | 100 |

**返回值：** 文件路径列表

## 注意事项

1. **日期格式**：支持 'YYYY-MM-DD' 和 'YYYYMMDD' 两种格式
2. **文件覆盖**：如果本地文件已存在，会被覆盖
3. **目录创建**：本地目录会自动创建
4. **错误处理**：下载失败的文件会记录日志，但不会中断整个下载过程
5. **大批量下载**：下载整年数据时可能需要较长时间，请耐心等待

## 日志输出

工具会输出详细的日志信息：

```
2024-01-01 10:00:00 - download_oss - INFO - 已从 .env 文件加载配置: /path/to/.env
2024-01-01 10:00:00 - download_oss - INFO - OSS 已初始化: endpoint=https://oss-cn-hangzhou.aliyuncs.com, bucket=test123432
2024-01-01 10:00:01 - download_oss - INFO - 开始下载因子文件: 2024-01-01 到 2024-01-07
2024-01-01 10:00:02 - download_oss - INFO - 已下载: uploads/factors/2024/factors_20240101.parquet -> ./data/factors/2024/factors_20240101.parquet
2024-01-01 10:00:03 - download_oss - INFO - 已下载: uploads/factors/2024/factors_20240102.parquet -> ./data/factors/2024/factors_20240102.parquet
...
2024-01-01 10:00:10 - download_oss - INFO - 下载完成: 成功 7 个文件
```

## 故障排查

### 问题 1: "OSS 访问凭证未配置"

**原因：** `.env` 文件不存在或配置不正确

**解决方法：**
1. 确保 `.env` 文件存在于正确的位置
2. 检查 `OSS_ACCESS_KEY_ID` 和 `OSS_ACCESS_KEY_SECRET` 是否正确配置

### 问题 2: "下载失败"

**可能原因：**
- OSS 文件不存在
- 网络连接问题
- 权限不足

**解决方法：**
1. 使用 `check_file_exists()` 检查文件是否存在
2. 使用 `list_oss_files()` 查看实际的文件列表
3. 检查 OSS 访问权限

### 问题 3: "未安装 python-dotenv"

**解决方法：**
```bash
pip install python-dotenv
```

## 高级用法

### 自定义文件名模式

如果你的文件名格式不同，可以自定义 `file_pattern`：

```python
# 例如：factor_data_20240101.csv
count = download_daily_factors(
    start_date="2024-01-01",
    end_date="2024-01-07",
    file_pattern="factor_data_{date}.csv"
)

# 例如：2024-01-01_factors.parquet
count = download_daily_factors(
    start_date="2024-01-01",
    end_date="2024-01-07",
    file_pattern="{date}_factors.parquet"
)
```

### 跨年下载

```python
# 下载 2024年12月25日 到 2025年1月5日
count = download_daily_factors(
    start_date="2024-12-25",
    end_date="2025-01-05"
)
# 文件会自动保存到对应年份的目录下
```

## 性能优化建议

1. **批量下载**：使用 `download_year_factors()` 比多次调用 `download_daily_factors()` 更高效
2. **并行下载**：如果需要下载多个年份，可以使用多线程/多进程
3. **断点续传**：在下载前检查本地文件是否已存在，避免重复下载

## 联系方式

如有问题，请联系开发团队。

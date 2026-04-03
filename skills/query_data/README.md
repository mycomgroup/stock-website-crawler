# Query Data Plugins

多数据源查询插件集合，支持各类金融数据API的快速测试和验证。

## 快速开始

### 1. 设置环境变量

创建 `.env` 文件或导出以下环境变量：

```bash
# 美股数据
export FINNHUB_API_KEY="your_finnhub_key"
export FMP_API_KEY="your_fmp_key"
export ALPHAVANTAGE_API_KEY="your_alphavantage_key"
export TIINGO_API_KEY="your_tiingo_key"

# 搜索API
export BRAVE_SEARCH_API_KEY="your_brave_key"
export TAVILY_API_KEY="your_tavily_key"
export SERP_API_KEY="your_serpapi_key"

# 其他数据
export EULERPOOL_API_KEY="your_eulerpool_key"
export MASSIVE_API_KEY="your_massive_key"
export ALLTICK_API_KEY="your_alltick_key"
export EODHD_API_KEY="your_eodhd_key"
export FINANCIALDATASETS_API_KEY="your_financialdatasets_key"

# 理杏仁（A股数据）
export LIXINGER_TOKEN="your_lixinger_token"
```

### 2. 运行测试

#### 测试所有数据源
```bash
python3 test_datasource.py
```

#### 测试单个数据源
```bash
python3 test_datasource.py --source finnhub --symbol AAPL
python3 test_datasource.py --source lixinger
```

## 支持的数据源

### 国际数据源（美股等）

| 数据源 | 类型 | 环境变量 | 说明 |
|--------|------|----------|------|
| **Finnhub** | 美股实时数据 | `FINNHUB_API_KEY` | 免费版有限额 |
| **Financial Modeling Prep** | 美股财务数据 | `FMP_API_KEY` | 稳定可靠 |
| **Alpha Vantage** | 美股历史数据 | `ALPHAVANTAGE_API_KEY` | 免费版有限额 |
| **Tiingo** | 美股历史数据 | `TIINGO_API_KEY` | 数据质量高 |
| **EODHD** | 全球股票数据 | `EODHD_API_KEY` | 覆盖范围广 |
| **Eulerpool** | 投资数据 | `EULERPOOL_API_KEY` | 超级投资者数据 |
| **Massive** | 金融数据 | `MASSIVE_API_KEY` | 综合金融数据 |
| **AllTick** | 实时行情 | `ALLTICK_API_KEY` | WebSocket实时数据 |
| **Financial Datasets** | 财务数据 | `FINANCIALDATASETS_API_KEY` | AI金融数据 |

### 搜索与信息

| 数据源 | 类型 | 环境变量 | 说明 |
|--------|------|----------|------|
| **Brave Search** | 网络搜索 | `BRAVE_SEARCH_API_KEY` | 隐私搜索引擎 |
| **Tavily** | AI搜索 | `TAVILY_API_KEY` | 专为AI设计 |
| **SerpAPI** | 搜索引擎 | `SERP_API_KEY` | Google搜索结果 |

### 中国A股数据源

| 数据源 | 类型 | 环境变量 | 说明 |
|--------|------|----------|------|
| **理杏仁 (Lixinger)** | A股/港股/美股 | `LIXINGER_TOKEN` | 最全面的中文金融数据 |

## 数据源详细说明

### 理杏仁 (Lixinger) - 推荐用于A股

理杏仁是专业的中文金融数据平台，提供最全面的A股、港股、美股数据。

**优势：**
- 覆盖A股、港股、美股、基金、指数、宏观数据
- 162+ API接口
- 基本面数据完整（PE、PB、ROE等）
- 财务数据详细
- 实时和历史数据

**获取Token：**
1. 访问 https://www.lixinger.com
2. 注册账号
3. 在个人中心获取 API Token

**使用方式：**
```bash
# 使用 query_tool.py 查询（推荐）
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "stockCode,name,pe_ttm,pb"

# 或使用本测试脚本
python3 test_datasource.py --source lixinger
```

**文档：** [lixinger-api-docs/README.md](./lixinger-api-docs/README.md)

### Finnhub - 美股实时数据

提供实时股票报价、基本面数据、新闻等。

**使用：**
```bash
python3 test_datasource.py --source finnhub --symbol AAPL
```

### Financial Modeling Prep - 美股财务数据

提供详细的财务报表数据、比率分析等。

**使用：**
```bash
python3 test_datasource.py --source financialmodelingprep --symbol MSFT
```

### Alpha Vantage - 美股历史数据

提供历史股价、技术指标等。

**使用：**
```bash
python3 test_datasource.py --source alphavantage --symbol TSLA
```

### Tiingo - 美股历史数据

数据质量高，适合量化分析。

**使用：**
```bash
python3 test_datasource.py --source tiingo --symbol NVDA
```

## 目录结构

```
query_data/
├── README.md                          # 本文件
├── test_datasource.py                 # 统一测试脚本
├── lixinger-api-docs/                 # 理杏仁API文档
│   └── README.md
├── finnhub-api-docs/                  # Finnhub文档
├── financial-modeling-prep-api-docs/  # FMP文档
├── alphavantage-api-docs/             # Alpha Vantage文档
├── tiingo-api-docs/                   # Tiingo文档
├── eodhd-api-docs/                    # EODHD文档
├── eulerpool-api-docs/                # Eulerpool文档
├── massive-api-docs/                  # Massive文档
├── alltick-api-docs/                  # AllTick文档
├── financial-datasets-api-docs/       # Financial Datasets文档
├── brave-search-api-docs/             # Brave Search文档
├── tavily-api-docs/                   # Tavily文档
└── serpapi-ai-overview/               # SerpAPI文档
```

## 添加新的数据源

1. 创建 `{provider}-api-docs/` 目录
2. 添加 `README.md` 文档说明
3. 在 `test_datasource.py` 中添加测试函数：

```python
def test_newprovider(symbol: str) -> Tuple[str, Any]:
    """Test NewProvider API."""
    api_key = _require_env("NEWPROVIDER_API_KEY")
    # 实现API调用逻辑
    return ("newprovider", data)
```

4. 更新 `tests` 列表和 `choices` 列表

## 故障排除

### 测试失败

检查环境变量是否正确设置：
```bash
echo $FINNHUB_API_KEY
echo $LIXINGER_TOKEN
```

### API限制

- Finnhub 免费版：60 calls/minute
- Alpha Vantage 免费版：5 calls/minute
- 理杏仁：根据账号等级有不同的日限额

### 网络问题

确保可以访问外部API：
```bash
curl https://finnhub.io/api/v1/quote?symbol=AAPL&token=YOUR_KEY
```

## 更多信息

- 理杏仁完整文档：`.claude/plugins/query_data/lixinger-api-docs/README.md`
- 理杏仁 API 文档：`.claude/plugins/query_data/lixinger-api-docs/docs/`
- 网页补充抓取说明：`.claude/plugins/stock-crawler/README.md`

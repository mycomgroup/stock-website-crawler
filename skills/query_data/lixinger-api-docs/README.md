# Lixinger (理杏仁) OpenAPI

理杏仁开放平台提供A股、港股、美股的金融数据API接口。

## 文档链接
- OpenAPI 文档: https://www.lixinger.com/open/api
- 接口列表: https://www.lixinger.com/open/api/doc

## API Key 获取
1. 注册理杏仁账号: https://www.lixinger.com
2. 在个人中心获取 API Token
3. 将 Token 保存到项目根目录的 `token.cfg` 文件中

## 接口分类

### A股公司
- `cn/company` - 股票详细信息
- `cn/company/fundamental/non_financial` - 基本面数据（PE、PB等）
- `cn/company/fs/non_financial` - 财务数据
- `cn/company/candlestick` - K线数据

### A股指数
- `cn/index` - 指数详细信息
- `cn/index/constituents` - 指数成分股
- `cn/index/fundamental` - 指数基本面数据

### 港股公司
- `hk/company` - 港股公司详情
- `hk/company/fundamental/non_financial` - 港股基本面数据

### 美股
- `us/index` - 美股指数数据

### 宏观数据
- `macro/gdp` - GDP数据
- `macro/cpi` - CPI数据
- `macro/interest-rates` - 利率数据

## 请求格式

### 基础URL
```
https://open.lixinger.com/api/
```

### 请求头
```
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN
```

### POST 请求示例
```bash
curl -X POST https://open.lixinger.com/api/cn/company \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "stockCodes": ["600519"],
    "metrics": ["pe_ttm", "pb"]
  }'
```

## 响应格式

### 成功响应
```json
{
  "code": 1,
  "msg": "success",
  "data": [...]
}
```

### 错误响应
```json
{
  "code": 0,
  "msg": "error message"
}
```

## 使用示例

### 查询贵州茅台的基本面数据
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "stockCode,name,pe_ttm,pb"
```

### 查询沪深300指数成分股
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/constituents" \
  --params '{"stockCodes": ["000300"], "date": "2024-01-01"}' \
  --flatten "constituents"
```

## 环境变量
- `LIXINGER_TOKEN` - 理杏仁API Token

# 快速开始

## 1. 生成 API 文档

```bash
cd web-api-generator
npm install
node generate-docs.js
```

这会在 `web-api-docs/` 目录生成 106 个 API 文档，格式类似 `api-docs/cn_company_allotment.md`。

## 2. 查看生成的文档

```bash
ls web-api-docs/
cat web-api-docs/detail-sh.md
```

每个文档包含：
- 简要描述
- 请求 URL
- URL 模式
- 参数说明
- 使用示例
- 返回数据说明

## 3. 配置登录信息

```bash
cd ..
cp .env.example .env
# 编辑 .env，填入理杏仁账号密码
```

## 4. 使用 Web API 客户端

### 列出所有 API

```bash
node web-api-client.js list
```

输出：
```
可用的 Web APIs:

analytics:
  - analytics-chart-maker: 图表制作工具 - 用于创建和管理自定义数据图表
  - detail-sz: 深圳证券交易所公司详情页
  - detail-sh: 上海证券交易所公司详情页
  ...

总计: 106 个 API
```

### 搜索 API

```bash
node web-api-client.js search 公司详情
```

输出：
```
找到 8 个匹配的 API:

- detail-sh: 上海证券交易所公司详情页
  示例: https://www.lixinger.com/analytics/company/detail/sh/605056/605056

- detail-sz: 深圳证券交易所公司详情页
  示例: https://www.lixinger.com/analytics/company/detail/sz/000002/2
...
```

### 调用 API

#### 示例 1: 获取贵州茅台详情

```bash
node web-api-client.js detail-sh --param4=600519 --param5=600519
```

返回：
```json
{
  "success": true,
  "api": "detail-sh",
  "url": "https://www.lixinger.com/analytics/company/detail/sh/600519/600519",
  "data": {
    "type": "generic",
    "title": "贵州茅台(600519)",
    "tables": [
      {
        "headers": ["指标", "2023", "2022", "2021"],
        "rowCount": 20,
        "rows": [
          ["营业收入", "1234.56", "1123.45", "1012.34"],
          ...
        ]
      }
    ],
    "charts": 5,
    "images": 3
  }
}
```

#### 示例 2: 获取 API 文档页

```bash
node web-api-client.js api-doc --api-key=cn/company
```

#### 示例 3: 获取指数成分股

```bash
node web-api-client.js constituents-list --param4=000300 --param5=300
```

## 5. 批量调用

创建脚本 `batch-fetch.sh`:

```bash
#!/bin/bash

# 批量获取多只股票的数据
for code in 600519 000858 000333 600036; do
  echo "Fetching $code..."
  node web-api-client.js detail-sh --param4=$code --param5=$code
  sleep 2
done
```

运行：
```bash
chmod +x batch-fetch.sh
./batch-fetch.sh
```

## 6. 在 Node.js 程序中使用

创建 `my-app.js`:

```javascript
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

async function fetchCompanyData(stockCode) {
  const cmd = `node web-api-client.js detail-sh --param4=${stockCode} --param5=${stockCode}`;
  const { stdout } = await execAsync(cmd, {
    cwd: './web-api-generator'
  });
  
  // 解析输出中的 JSON
  const match = stdout.match(/\{[\s\S]*\}/);
  if (match) {
    return JSON.parse(match[0]);
  }
  throw new Error('Failed to parse response');
}

// 使用
const data = await fetchCompanyData('600519');
console.log('公司名称:', data.data.title);
console.log('表格数量:', data.data.tables.length);
```

## 7. 与 MCP Server 集成

可以基于这个客户端创建 MCP Server，让大模型直接调用：

```javascript
// 在 MCP Server 中
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  // 调用 web-api-client
  const cmd = `node web-api-client.js ${name} ${buildParams(args)}`;
  const { stdout } = await execAsync(cmd);
  
  return {
    content: [{ type: 'text', text: stdout }]
  };
});
```

## 常见问题

### Q: 如何知道需要传哪些参数？

A: 查看生成的 API 文档：
```bash
cat web-api-docs/detail-sh.md
```

### Q: 返回的数据太多怎么办？

A: 客户端默认只返回前 10 行数据作为示例。如需完整数据，修改 `simplifyData()` 方法。

### Q: 如何加快抓取速度？

A: 
1. 使用 headless 模式（默认已启用）
2. 减少等待时间
3. 并行抓取多个页面

### Q: 抓取失败怎么办？

A: 
1. 检查登录信息是否正确
2. 检查 URL 参数是否正确
3. 查看错误日志

## 下一步

1. 查看所有生成的 API 文档
2. 尝试调用不同的 API
3. 集成到你的项目中
4. 创建 MCP Server（可选）

# 使用示例

## 1. 生成文档和配置

```bash
cd skills/web-api-generator

# 生成所有 API 文档和配置
node main.js generate-docs

# 查看生成的文件
ls output/web-api-docs/
# - README.md
# - api-configs.json      (配置文件 - JSON 格式)
# - api-configs.jsonl     (配置文件 - JSONL 格式)
# - detail-sh.md          (用户文档)
# - constituents-list.md  (用户文档)
# - ...
```

## 2. 查看配置

```bash
# 查看所有配置
cat output/web-api-docs/api-configs.json | jq '.[0:3]'

# 查看特定 API 的配置
cat output/web-api-docs/api-configs.json | jq '.[] | select(.api=="constituents-list")'
```

输出示例：
```json
{
  "api": "constituents-list",
  "description": "申万2021行业行业详情页 - 成分股数据",
  "outputFormat": "csv",
  "parameters": [
    {
      "name": "param4",
      "required": true,
      "type": "String",
      "description": "路径参数 param4"
    }
  ]
}
```

## 3. 调用 API（CSV 格式）

```bash
# 获取成分股列表（自动输出 CSV）
node main.js call \
  --api=constituents-list \
  --param4=480301 \
  --param5=480301
```

输出：
```
调用 API: constituents-list
参数: { param4: '480301', param5: '480301' }

抓取: https://www.lixinger.com/analytics/industry/detail/sw_2021/480301/480301/constituents/list

结果:

CSV 格式输出:

表格 1:
股票代码,股票名称,权重,行业
600519,贵州茅台,10.5%,白酒
000858,五粮液,8.2%,白酒
...

已保存到: output-constituents-list-1234567890.csv
```

## 4. 调用 API（MD 格式）

```bash
# 获取公司详情（自动输出 MD）
node main.js call \
  --api=detail-sh \
  --param4=600519 \
  --param5=600519
```

输出：
```json
{
  "success": true,
  "api": "detail-sh",
  "url": "https://www.lixinger.com/analytics/company/detail/sh/600519/600519",
  "outputFormat": "md",
  "data": {
    "type": "md",
    "title": "贵州茅台(600519)",
    "tables": [
      {
        "headers": ["指标", "2023", "2022", "2021"],
        "rowCount": 20,
        "rows": [...]
      }
    ],
    "charts": 5,
    "images": 3
  }
}

已保存到: output-detail-sh-1234567890.json
```

## 5. 指定输出文件

```bash
# 保存为指定的 CSV 文件
node main.js call \
  --api=constituents-list \
  --param4=480301 \
  --param5=480301 \
  --output=./data/sw_480301_constituents.csv

# 保存为指定的 JSON 文件
node main.js call \
  --api=detail-sh \
  --param4=600519 \
  --param5=600519 \
  --output=./data/600519_detail.json
```

## 6. 批量调用

创建脚本 `batch-fetch.sh`:

```bash
#!/bin/bash

# 批量获取多个行业的成分股
for code in 480301 480401 480501; do
  echo "Fetching industry $code..."
  node main.js call \
    --api=constituents-list \
    --param4=$code \
    --param5=$code \
    --output=./data/industry_${code}.csv
  sleep 2
done

echo "Done!"
```

运行：
```bash
chmod +x batch-fetch.sh
./batch-fetch.sh
```

## 7. 在 Node.js 中使用

```javascript
import { WebApiClient } from './lib/api-client.js';
import fs from 'fs';

const client = new WebApiClient({
  patternsPath: '../../stock-crawler/output/lixinger-crawler/url-patterns.json',
  configPath: './output/web-api-docs/api-configs.json',
  username: process.env.LIXINGER_USERNAME,
  password: process.env.LIXINGER_PASSWORD
});

await client.initialize();

// 调用 CSV 格式的 API
const csvResult = await client.callApi('constituents-list', {
  param4: '480301',
  param5: '480301'
});

if (csvResult.outputFormat === 'csv') {
  // 保存 CSV
  fs.writeFileSync('constituents.csv', csvResult.data.tables[0].csv);
  console.log('CSV saved!');
}

// 调用 MD 格式的 API
const mdResult = await client.callApi('detail-sh', {
  param4: '600519',
  param5: '600519'
});

console.log('Title:', mdResult.data.title);
console.log('Tables:', mdResult.data.tables.length);

await client.close();
```

## 8. 自定义配置

编辑 `output/web-api-docs/api-configs.json`:

```json
{
  "api": "my-custom-api",
  "outputFormat": "csv",  // 改为 csv
  "dataExtraction": {
    "tables": "primary",  // 只提取主表格
    "charts": false,
    "images": false,
    "mainContent": false
  }
}
```

然后使用自定义配置：

```bash
node main.js call \
  --api=my-custom-api \
  --config=./output/web-api-docs/api-configs.json \
  --param4=value
```

## 9. 数据处理

### 处理 CSV 数据

```bash
# 使用 csvkit 处理
pip install csvkit

# 查看 CSV
csvlook output-constituents-list-*.csv

# 转换为 JSON
csvjson output-constituents-list-*.csv > data.json

# 筛选数据
csvgrep -c 权重 -r "^[0-9]+" output-constituents-list-*.csv
```

### 处理 JSON 数据

```bash
# 使用 jq 处理
cat output-detail-sh-*.json | jq '.data.tables[0].rows'

# 提取特定字段
cat output-detail-sh-*.json | jq '.data.title'

# 转换为 CSV
cat output-detail-sh-*.json | jq -r '.data.tables[0].rows[] | @csv'
```

## 10. 完整工作流

```bash
# 1. 生成文档和配置
node main.js generate-docs

# 2. 查看可用 API
node main.js list

# 3. 搜索需要的 API
node main.js search --keyword=成分股

# 4. 查看 API 配置
cat output/web-api-docs/api-configs.json | jq '.[] | select(.api=="constituents-list")'

# 5. 调用 API
node main.js call \
  --api=constituents-list \
  --param4=480301 \
  --param5=480301 \
  --output=./data/constituents.csv

# 6. 处理数据
csvlook ./data/constituents.csv
```

## 常见问题

### Q: 如何知道某个 API 输出什么格式？

A: 查看配置文件：
```bash
cat output/web-api-docs/api-configs.json | jq '.[] | select(.api=="your-api") | .outputFormat'
```

### Q: 如何修改输出格式？

A: 编辑 `api-configs.json`，将 `outputFormat` 改为 `csv` 或 `md`。

### Q: CSV 和 MD 格式有什么区别？

A:
- **CSV**: 纯表格数据，适合导入 Excel、数据库
- **MD**: 完整页面内容，包含表格、图表、文本等

### Q: 如何批量处理多个 API？

A: 创建 shell 脚本循环调用，参考示例 6。

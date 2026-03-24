# lixinger-screener

理杏仁筛选工具现在统一放在这个目录下，分成两套可独立运行的实现：

- `browser/`: 浏览器自动化版本，适合自然语言 + Playwright 操作页面
- `request/`: 纯请求版本，适合直接读取筛选器配置、拼请求体并返回结果
- 两套实现现在共用同一份输入 schema：既支持 `--query` 自然语言，也支持 `--input-file` 参数文件

常用命令：

```bash
cd /Users/fengzhi/Downloads/git/testlixingren/skills/lixinger-screener

# 浏览器版：自然语言
node run-skill.js --query "PE-TTM(扣非)统计值10年分位点小于30%，股息率大于2%"

# 浏览器版：统一参数文件
node run-skill.js --input-file unified-input.example.json --headless false

# 浏览器版：指定 screener 页面和 profile
node run-skill.js \
  --url "https://www.lixinger.com/analytics/screener/company-fundamental/cn?screener-id=587c4d21d6e94ed9d447b29d" \
  --profile-dir /path/to/chrome-profile

# request 版：自然语言
node request/fetch-lixinger-screener.js --query "PE-TTM(扣非)统计值10年分位点小于30%，股息率大于2%" --output markdown

# request 版：统一参数文件
node request/fetch-lixinger-screener.js --input-file unified-input.example.json --output csv
```

所有理杏仁相关入口现在都只保留在这个目录下，不再保留 `stock-crawler/scripts` 里的兼容包装。

浏览器版登录优先级：

- 已保存的 `storageState`
- `--profile-dir` 或 `LIXINGER_BROWSER_PROFILE_DIR`
- 登录接口写 cookie
- 浏览器表单自动登录

统一参数文件示例见：

- `unified-input.example.json`

参数文件里可以手写 `conditions`，也可以带一个 `query` 字段；当前两套入口都会把它们合并处理。推荐的 condition 结构是：

```json
{
  "metric": "PE-TTM统计值",
  "selectors": ["10年", "分位点%"],
  "min": 0,
  "max": 30
}
```

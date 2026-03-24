# lixinger-screener

理杏仁筛选工具现在统一放在这个目录下，分成两套可独立运行的实现：

- `browser/`: 浏览器自动化版本，适合自然语言 + Playwright 操作页面
- `request/`: 纯请求版本，适合直接读取筛选器配置、拼请求体并返回结果

常用命令：

```bash
cd /Users/fengzhi/Downloads/git/testlixingren/skills/lixinger-screener

# 浏览器版
node run-skill.js --query "PE小于20，ROE大于15%"

# request 版
node request/fetch-lixinger-screener.js --url "https://www.lixinger.com/analytics/screener/company-fundamental/cn?screener-id=587c4d21d6e94ed9d447b29d"
```

所有理杏仁相关入口现在都只保留在这个目录下，不再保留 `stock-crawler/scripts` 里的兼容包装。

# 目录结构说明

## 新的项目目录结构

从现在开始，爬虫会为每个项目创建独立的目录结构：

```
output/
└── <project-name>/              # 项目名称文件夹（来自配置文件的 name 字段）
    ├── links.txt                # 链接文件（包含所有URL及其状态）
    ├── logs/                    # 日志文件夹
    │   └── crawler-*.log        # 带时间戳的日志文件
    └── pages/                   # 抓取的网页文件夹
        ├── page1.md             # 网页1的Markdown文件
        ├── page2.md             # 网页2的Markdown文件
        └── ...
```

## 示例

如果你的配置文件是：

```json
{
  "name": "lixinger-crawler",
  "output": {
    "directory": "./output"
  }
}
```

那么目录结构将是：

```
output/
└── lixinger-crawler/
    ├── links.txt
    ├── logs/
    │   └── crawler-2026-02-24T08-11-30-896Z.log
    └── pages/
        ├── 国债_-_中债_(股债收益率模型).md
        ├── 公司基本面数据.md
        └── ...
```

## 优点

1. **项目隔离**：每个爬取项目有自己独立的目录
2. **易于管理**：所有相关文件（链接、日志、页面）都在一个文件夹下
3. **支持多项目**：可以同时运行多个不同的爬取项目
4. **清晰组织**：页面文件、日志文件、链接文件分别存放

## 文件说明

### links.txt
- 格式：每行一个JSON对象
- 内容：URL、状态（pending/crawled/failed）、时间戳、重试次数等
- 用途：记录所有发现的链接及其爬取状态，支持断点续爬

### logs/
- 包含带时间戳的日志文件
- 记录爬取过程中的所有信息、警告和错误
- 便于调试和追踪问题

### pages/
- 包含所有抓取的网页的Markdown文件
- 文件名基于页面标题自动生成
- 包含表格、代码块等结构化内容

## 迁移说明

如果你有旧的爬取数据，可以手动移动到新的目录结构：

```bash
# 创建项目目录
mkdir -p output/lixinger-crawler/pages
mkdir -p output/lixinger-crawler/logs

# 移动链接文件
mv links.txt output/lixinger-crawler/

# 移动页面文件
mv output/*.md output/lixinger-crawler/pages/

# 移动日志文件
mv logs/*.log output/lixinger-crawler/logs/
```

# Requirements Document

## Introduction

本文档定义了一个通用的网站爬虫系统的需求，该系统主要用于爬取股票数据网站（如东方财富、雪球、腾讯、akshare、理杏仁等）的内容。系统支持配置化爬取、自动登录、链接发现、页面解析和数据提取等功能。

## Glossary

- **Crawler_System**: 网站爬虫系统，负责自动化访问网页、提取数据和管理链接
- **Link_Manager**: 链接管理器，负责读取、存储和去重URL链接
- **Page_Parser**: 页面解析器，负责从HTML页面中提取表格、tab内容等结构化数据
- **Login_Handler**: 登录处理器，负责处理需要身份验证的网站
- **Config_File**: 配置文件，包含爬取规则、起始URL、登录信息等
- **Links_File**: 链接文件（links.txt），存储待爬取和已发现的URL列表
- **Output_File**: 输出文件，存储解析后的页面内容（Markdown格式）

## Requirements

### Requirement 1: 配置化爬取管理

**User Story:** 作为用户，我希望通过配置文件定义爬取规则，以便灵活地爬取不同的网站而无需修改代码

#### Acceptance Criteria

1. THE Crawler_System SHALL 读取配置文件并解析爬取规则
2. WHERE 配置文件包含URL规则，THE Crawler_System SHALL 使用该规则过滤和匹配链接
3. WHERE 配置文件包含起始种子链接，THE Crawler_System SHALL 从这些链接开始爬取
4. WHERE 配置文件包含登录信息，THE Crawler_System SHALL 使用该信息进行网站登录
5. WHEN 配置文件格式错误或缺少必需字段，THE Crawler_System SHALL 返回描述性错误信息

### Requirement 2: 链接管理和持久化

**User Story:** 作为用户，我希望系统能够管理所有待爬取的链接，以便支持断点续爬和避免重复爬取

#### Acceptance Criteria

1. THE Link_Manager SHALL 从links.txt文件读取URL列表
2. WHEN 发现新的URL，THE Link_Manager SHALL 将其追加到links.txt文件
3. THE Link_Manager SHALL 对URL列表进行去重处理
4. THE Link_Manager SHALL 对URL列表进行排序以保持一致性
5. WHEN links.txt文件不存在，THE Link_Manager SHALL 使用配置文件中的起始种子链接创建该文件
6. THE Link_Manager SHALL 记录每个URL的爬取状态（待爬取、已爬取、失败）

### Requirement 3: 自动登录处理

**User Story:** 作为用户，我希望系统能够自动登录需要身份验证的网站，以便访问受保护的内容

#### Acceptance Criteria

1. WHEN 页面包含登录表单，THE Login_Handler SHALL 检测并识别登录页面
2. WHEN 检测到登录页面，THE Login_Handler SHALL 使用配置文件中的账号和密码填写表单
3. THE Login_Handler SHALL 支持多种登录表单格式（手机号、邮箱、用户名等）
4. WHEN 登录成功，THE Login_Handler SHALL 保存会话状态以供后续请求使用
5. WHEN 登录失败，THE Login_Handler SHALL 返回错误信息并记录失败原因
6. WHERE 网站不需要登录，THE Login_Handler SHALL 跳过登录步骤

### Requirement 4: 链接发现和提取

**User Story:** 作为用户，我希望系统能够自动发现页面中的新链接，以便实现递归爬取

#### Acceptance Criteria

1. THE Crawler_System SHALL 从当前页面提取所有符合URL规则的链接
2. THE Crawler_System SHALL 展开页面中的折叠内容以发现隐藏的链接
3. WHEN 页面包含动态加载的内容，THE Crawler_System SHALL 等待内容加载完成后再提取链接
4. THE Crawler_System SHALL 将相对URL转换为绝对URL
5. THE Crawler_System SHALL 过滤掉不符合配置规则的链接
6. WHEN 发现新链接，THE Crawler_System SHALL 通过Link_Manager将其添加到links.txt

### Requirement 5: 页面内容解析

**User Story:** 作为用户，我希望系统能够解析页面中的表格和结构化内容，以便提取有价值的数据

#### Acceptance Criteria

1. THE Page_Parser SHALL 提取页面中的所有表格数据
2. THE Page_Parser SHALL 识别并提取表格的标题行和数据行
3. WHEN 页面包含多个tab，THE Page_Parser SHALL 逐个点击tab并提取每个tab的内容
4. THE Page_Parser SHALL 提取页面标题、描述和主要文本内容
5. THE Page_Parser SHALL 识别并提取代码块（如JSON、XML等）
6. THE Page_Parser SHALL 处理表格中的特殊字符和换行符
7. WHEN 页面包含折叠内容，THE Page_Parser SHALL 展开所有折叠项后再解析

### Requirement 6: 输出格式化

**User Story:** 作为用户，我希望系统将解析的内容保存为Markdown格式，以便于阅读和后续处理

#### Acceptance Criteria

1. THE Crawler_System SHALL 将解析的页面内容转换为Markdown格式
2. THE Crawler_System SHALL 将表格转换为Markdown表格格式
3. THE Crawler_System SHALL 将代码块使用Markdown代码块格式包裹
4. THE Crawler_System SHALL 为每个页面生成独立的Markdown文件
5. THE Crawler_System SHALL 使用安全的文件名（移除特殊字符）
6. THE Crawler_System SHALL 在Markdown文件中保留原始URL作为参考

### Requirement 7: 错误处理和重试

**User Story:** 作为用户，我希望系统能够优雅地处理错误，以便在遇到问题时不会中断整个爬取过程

#### Acceptance Criteria

1. WHEN 页面加载超时，THE Crawler_System SHALL 记录错误并继续处理下一个URL
2. WHEN 页面返回404或其他错误状态码，THE Crawler_System SHALL 记录错误并标记该URL为失败
3. WHEN 网络连接失败，THE Crawler_System SHALL 记录错误并将URL标记为待重试
4. THE Crawler_System SHALL 为每个URL设置合理的超时时间
5. THE Crawler_System SHALL 在请求之间添加延迟以避免被封禁
6. THE Crawler_System SHALL 记录所有错误信息到日志文件

### Requirement 8: 进度跟踪和日志

**User Story:** 作为用户，我希望能够查看爬取进度和详细日志，以便了解系统运行状态

#### Acceptance Criteria

1. THE Crawler_System SHALL 在控制台输出当前爬取进度（已完成/总数）
2. THE Crawler_System SHALL 输出每个URL的处理状态（成功、失败、跳过）
3. THE Crawler_System SHALL 记录发现的新链接数量
4. THE Crawler_System SHALL 记录每个页面的解析结果摘要
5. THE Crawler_System SHALL 在爬取完成后输出统计信息（总数、成功数、失败数）
6. THE Crawler_System SHALL 将详细日志写入日志文件

### Requirement 9: 代码组织和可维护性

**User Story:** 作为开发者，我希望代码结构清晰、模块化，以便于维护和扩展

#### Acceptance Criteria

1. THE Crawler_System SHALL 将不同功能模块分离到独立的文件中
2. THE Crawler_System SHALL 使用清晰的目录结构组织代码
3. THE Crawler_System SHALL 为每个模块提供清晰的接口定义
4. THE Crawler_System SHALL 使用一致的命名约定
5. THE Crawler_System SHALL 包含必要的代码注释和文档
6. THE Crawler_System SHALL 将配置、代码和输出分离到不同的目录

### Requirement 10: 浏览器自动化

**User Story:** 作为用户，我希望系统能够处理动态网页和JavaScript渲染的内容，以便爬取现代Web应用

#### Acceptance Criteria

1. THE Crawler_System SHALL 使用Playwright进行浏览器自动化
2. THE Crawler_System SHALL 支持等待页面加载完成（networkidle状态）
3. THE Crawler_System SHALL 支持执行JavaScript代码以操作页面
4. THE Crawler_System SHALL 支持点击按钮、展开菜单等交互操作
5. WHERE 配置指定，THE Crawler_System SHALL 支持headless和有头模式
6. THE Crawler_System SHALL 在爬取完成后正确关闭浏览器资源

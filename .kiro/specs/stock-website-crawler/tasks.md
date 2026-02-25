# Implementation Plan: Stock Website Crawler

## Overview

本实现计划将通用网站爬虫系统分解为一系列增量式的编码任务。系统使用Node.js和Playwright构建，采用模块化设计，支持配置化爬取、自动登录、链接发现和页面解析等功能。

实现策略：
1. 先建立核心数据结构和工具模块
2. 逐步实现各功能模块，每个模块完成后立即测试
3. 最后集成所有模块并实现主控制器
4. 重构现有代码到新的目录结构

## Tasks

- [x] 1. 项目初始化和目录结构设置
  - 创建新的项目目录 `stock-crawler/`
  - 设置目录结构：`src/`, `config/`, `output/`, `test/`, `logs/`
  - 初始化package.json并安装依赖（playwright, fast-check, jest）
  - 创建.gitignore文件
  - _Requirements: 9.6_

- [ ] 2. 实现Config Manager模块
  - [x] 2.1 创建config-manager.js并实现配置加载功能
    - 实现loadConfig()方法读取JSON配置文件
    - 实现validateConfig()方法验证必需字段
    - 处理文件不存在和JSON解析错误
    - _Requirements: 1.1, 1.5_
  
  - [x] 2.2 编写Property 1测试：配置文件解析完整性
    - **Property 1: 配置文件解析完整性**
    - **Validates: Requirements 1.1**
    - 使用fast-check生成随机有效配置，验证解析结果包含所有必需字段
  
  - [x] 2.3 编写Property 4测试：无效配置错误处理
    - **Property 4: 无效配置错误处理**
    - **Validates: Requirements 1.5**
    - 生成缺少必需字段的配置，验证返回描述性错误
  
  - [x] 2.4 编写单元测试
    - 测试有效配置示例
    - 测试无效JSON格式
    - 测试文件不存在情况

- [ ] 3. 实现Link Manager模块
  - [x] 3.1 创建link-manager.js并实现链接管理功能
    - 实现loadLinks()方法从文件读取链接
    - 实现saveLinks()方法保存链接到文件
    - 实现addLink()方法添加新链接
    - 实现updateLinkStatus()方法更新链接状态
    - 实现getPendingLinks()方法获取待爬取链接
    - 实现deduplicateAndSort()方法去重和排序
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.6_
  
  - [x] 3.2 编写Property 5测试：链接文件读写一致性
    - **Property 5: 链接文件读写一致性**
    - **Validates: Requirements 2.1, 2.2**
    - 生成随机链接列表，验证保存后读取的结果一致（round-trip）
  
  - [x] 3.3 编写Property 6测试：URL去重不变性
    - **Property 6: URL去重不变性**
    - **Validates: Requirements 2.3**
    - 生成包含重复URL的列表，验证去重后无重复且保留所有唯一URL
  
  - [x] 3.4 编写Property 7测试：URL排序不变性
    - **Property 7: URL排序不变性**
    - **Validates: Requirements 2.4**
    - 生成随机URL列表，验证排序后按字典序排列
  
  - [x] 3.5 编写Property 8测试：链接状态更新正确性
    - **Property 8: 链接状态更新正确性**
    - **Validates: Requirements 2.6**
    - 生成随机链接和状态，验证更新后查询返回新状态
  
  - [x] 3.6 编写单元测试
    - 测试空文件处理
    - 测试文件不存在时使用种子链接初始化
    - 测试状态转换（pending -> crawled -> failed）

- [ ] 4. 实现URL工具函数
  - [x] 4.1 创建url-utils.js实现URL处理功能
    - 实现toAbsoluteUrl()函数转换相对URL为绝对URL
    - 实现filterLinks()函数根据规则过滤URL
    - 实现matchesPattern()函数匹配URL模式（支持正则）
    - _Requirements: 1.2, 4.4, 4.5_
  
  - [x] 4.2 编写Property 2测试：URL规则过滤正确性
    - **Property 2: URL规则过滤正确性**
    - **Validates: Requirements 1.2, 4.5**
    - 生成随机URL列表和过滤规则，验证结果符合include且不符合exclude
  
  - [x] 4.3 编写Property 12测试：相对URL转换正确性
    - **Property 12: 相对URL转换正确性**
    - **Validates: Requirements 4.4**
    - 生成随机相对URL和基础URL，验证转换结果正确
  
  - [x] 4.4 编写单元测试
    - 测试各种相对URL格式（./、../、/、无前缀）
    - 测试URL规则边缘情况（空规则、通配符）

- [x] 5. Checkpoint - 确保核心工具模块测试通过
  - 运行所有测试确保Config Manager、Link Manager和URL工具正常工作
  - 如有问题请询问用户

- [ ] 6. 实现Browser Manager模块
  - [x] 6.1 创建browser-manager.js实现浏览器管理
    - 实现launch()方法启动Playwright浏览器
    - 实现newPage()方法创建新页面
    - 实现goto()方法导航到URL（带超时和错误处理）
    - 实现waitForLoad()方法等待页面加载完成
    - 实现close()方法关闭浏览器
    - _Requirements: 10.1, 10.2, 10.5, 10.6_
  
  - [x] 6.2 编写单元测试
    - 测试浏览器启动和关闭
    - 测试headless和有头模式配置
    - 测试超时处理（使用mock）

- [ ] 7. 实现Login Handler模块
  - [x] 7.1 创建login-handler.js实现登录检测和处理
    - 实现needsLogin()方法检测是否在登录页面
    - 实现login()方法执行自动登录
    - 实现fillUsername()方法填写用户名（支持多种输入框类型）
    - 实现fillPassword()方法填写密码
    - 实现clickLoginButton()方法点击登录按钮
    - _Requirements: 3.1, 3.2, 3.3, 3.6_
  
  - [x] 7.2 编写Property 9测试：登录表单检测准确性
    - **Property 9: 登录表单检测准确性**
    - **Validates: Requirements 3.1**
    - 生成包含登录表单的HTML，验证正确识别为登录页面
  
  - [x] 7.3 编写Property 10测试：多格式登录表单识别
    - **Property 10: 多格式登录表单识别**
    - **Validates: Requirements 3.3**
    - 生成不同类型的用户名输入框，验证都能正确识别
  
  - [x] 7.4 编写单元测试
    - 测试常见登录表单示例
    - 测试不需要登录的页面
    - 测试登录失败情况

- [ ] 8. 实现Link Finder模块
  - [x] 8.1 创建link-finder.js实现链接发现功能
    - 实现expandCollapsibles()方法展开折叠内容
    - 实现extractLinks()方法提取页面链接
    - 集成url-utils的过滤和转换功能
    - _Requirements: 4.1, 4.2, 4.6_
  
  - [x] 8.2 编写Property 11测试：链接提取完整性
    - **Property 11: 链接提取完整性**
    - **Validates: Requirements 4.1**
    - 生成包含各种链接的HTML，验证提取的链接都是有效绝对URL且符合规则
  
  - [x] 8.3 编写单元测试
    - 测试空页面
    - 测试无链接页面
    - 测试混合相对和绝对链接

- [x] 9. 实现Page Parser模块
  - [x] 9.1 创建page-parser.js实现页面解析功能
    - 实现parsePage()主方法协调所有解析功能
    - 实现extractTitle()方法提取标题
    - 实现extractDescription()方法提取描述
    - 实现extractTables()方法提取所有表格
    - 实现extractTabContents()方法提取tab内容
    - 实现extractCodeBlocks()方法提取代码块
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.7_
  
  - [x] 9.2 编写Property 13测试：表格解析完整性
    - **Property 13: 表格解析完整性**
    - **Validates: Requirements 5.1, 5.2**
    - 生成随机HTML表格，验证解析结果包含所有标题和数据行
  
  - [x] 9.3 编写Property 14测试：文本内容提取正确性
    - **Property 14: 文本内容提取正确性**
    - **Validates: Requirements 5.4**
    - 生成包含标题和描述的HTML，验证提取内容正确
  
  - [x] 9.4 编写Property 15测试：代码块识别准确性
    - **Property 15: 代码块识别准确性**
    - **Validates: Requirements 5.5**
    - 生成包含各种代码块的HTML，验证都能正确识别和提取
  
  - [x] 9.5 编写单元测试
    - 测试空表格
    - 测试单行表格
    - 测试表格中的特殊字符和换行符
    - 测试嵌套表格

- [x] 10. Checkpoint - 确保解析模块测试通过
  - 运行所有测试确保Browser Manager、Login Handler、Link Finder和Page Parser正常工作
  - 如有问题请询问用户

- [x] 11. 实现Markdown Generator模块
  - [x] 11.1 创建markdown-generator.js实现Markdown生成功能
    - 实现generate()方法生成完整Markdown
    - 实现tableToMarkdown()方法转换表格
    - 实现codeBlockToMarkdown()方法转换代码块
    - 实现safeFilename()方法生成安全文件名
    - 实现saveToFile()方法保存文件
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_
  
  - [x] 11.2 编写Property 16测试：Markdown生成格式正确性
    - **Property 16: Markdown生成格式正确性**
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.6**
    - 生成随机PageData，验证Markdown包含标题、表格、代码块和URL
  
  - [x] 11.3 编写Property 17测试：Markdown文件生成唯一性
    - **Property 17: Markdown文件生成唯一性**
    - **Validates: Requirements 6.4**
    - 验证每个PageData生成唯一的文件
  
  - [x] 11.4 编写Property 18测试：文件名安全性
    - **Property 18: 文件名安全性**
    - **Validates: Requirements 6.5**
    - 生成包含特殊字符的文件名，验证转换后安全
  
  - [x] 11.5 编写单元测试
    - 测试空内容
    - 测试单个表格
    - 测试单个代码块
    - 测试Markdown特殊字符转义

- [x] 12. 实现日志和统计模块
  - [x] 12.1 创建logger.js实现日志功能
    - 实现控制台日志输出（带颜色和格式）
    - 实现文件日志写入
    - 实现不同日志级别（info, warn, error）
    - _Requirements: 7.6, 8.1, 8.2, 8.4, 8.6_
  
  - [x] 12.2 创建stats-tracker.js实现统计功能
    - 实现统计数据收集（总数、成功数、失败数、新链接数）
    - 实现generateStats()方法生成统计报告
    - _Requirements: 8.3, 8.5_
  
  - [x] 12.3 编写Property 19测试：错误日志记录完整性
    - **Property 19: 错误日志记录完整性**
    - **Validates: Requirements 7.6, 8.6**
    - 生成随机错误，验证日志包含URL、错误信息和时间戳
  
  - [x] 12.4 编写Property 20测试：统计信息准确性
    - **Property 20: 统计信息准确性**
    - **Validates: Requirements 8.3, 8.5**
    - 模拟爬取会话，验证统计数据准确
  
  - [x] 12.5 编写单元测试
    - 测试日志格式
    - 测试日志文件写入
    - 测试统计数据累加

- [ ] 13. 实现Main Controller
  - [x] 13.1 创建crawler-main.js实现主控制器
    - 实现initialize()方法初始化所有模块
    - 实现start()方法启动爬取流程
    - 实现processUrl()方法处理单个URL
    - 集成所有模块：Config Manager、Link Manager、Browser Manager、Login Handler、Link Finder、Page Parser、Markdown Generator
    - 实现错误处理和重试逻辑
    - 实现请求间延迟
    - _Requirements: 1.3, 2.5, 4.6, 7.1, 7.2, 7.3, 7.4, 7.5_
  
  - [x] 13.2 编写集成测试
    - 测试完整爬取流程（使用本地测试HTML文件）
    - 测试登录流程（使用模拟登录页面）
    - 测试链接发现和递归爬取
    - 测试错误恢复

- [ ] 14. 创建CLI入口和配置示例
  - [x] 14.1 创建index.js作为CLI入口
    - 解析命令行参数（配置文件路径）
    - 调用Main Controller启动爬取
    - 处理未捕获的异常
    - _Requirements: 9.1, 9.2_
  
  - [x] 14.2 创建配置文件示例
    - 创建config/lixinger.json（理杏仁网站配置）
    - 创建config/example.json（通用示例配置）
    - 添加配置说明文档
    - _Requirements: 1.1, 1.2, 1.3, 1.4_
  
  - [x] 14.3 创建README.md文档
    - 项目介绍和功能说明
    - 安装和使用说明
    - 配置文件格式说明
    - 示例用法
    - _Requirements: 9.5_

- [ ] 15. 迁移和重构现有代码
  - [x] 15.1 分析现有代码功能
    - 识别debug-find-all-links.js中可复用的逻辑
    - 识别crawl-doc-to-md.js中可复用的逻辑
    - _Requirements: 9.1_
  
  - [x] 15.2 将现有代码逻辑整合到新模块
    - 将登录逻辑迁移到Login Handler
    - 将链接发现逻辑迁移到Link Finder
    - 将页面解析逻辑迁移到Page Parser
    - 将Markdown生成逻辑迁移到Markdown Generator
    - _Requirements: 9.1, 9.3_
  
  - [x] 15.3 创建迁移脚本
    - 创建脚本将旧的links.txt迁移到新格式
    - 创建脚本将旧的输出文件移动到新目录
    - _Requirements: 2.1_

- [x] 16. Final Checkpoint - 完整测试和验证
  - 运行所有单元测试和属性测试
  - 使用理杏仁配置进行端到端测试
  - 验证生成的Markdown文件格式正确
  - 验证links.txt正确更新
  - 验证日志文件正确生成
  - 如有问题请询问用户

## Notes

- 任务标记`*`的为可选测试任务，可以跳过以加快MVP开发
- 每个任务都标注了对应的需求编号，便于追溯
- Checkpoint任务确保增量验证，及早发现问题
- 属性测试使用fast-check库，每个测试至少100次迭代
- 单元测试使用Jest框架
- 所有代码使用ES6+语法，采用模块化设计
- 配置文件使用JSON格式，便于编辑和验证

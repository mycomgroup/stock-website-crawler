# 更新日志

## 2026-02-24

### 主要更新

#### 1. 状态字段重命名
- `pending` → `unfetched` (未抓取)
- 新增 `fetching` 状态 (正在抓取)
- `crawled` → `fetched` (抓取完成)
- `crawledAt` → `fetchedAt`

#### 2. 重试逻辑改进
- 失败后如果未达到 `maxRetries`，状态改回 `unfetched`
- 只有达到 `maxRetries` 后才标记为 `failed`
- 每次失败增加 `retryCount`

#### 3. 登录功能增强
- 在爬取开始时主动尝试登录
- 实现三种登录策略：
  1. 访问配置的 loginUrl
  2. 在主页查找登录链接
  3. 尝试常见登录 URL 路径
- 使用浏览器上下文（Browser Context）共享登录状态
- 从旧的 `page.$()` API 迁移到现代的 `page.locator()` API

#### 4. Markdown 生成改进
- 始终在生成的文件中包含源 URL
- 文件名冲突时自动添加 URL hash 避免覆盖

#### 5. 批量处理
- 添加 `batchSize` 配置参数
- 每次运行只处理指定数量的链接
- 支持断点续爬

#### 6. 新增脚本和文档
- `npm run crawl` - 推荐的运行方式
- `npm run test:login` - 测试登录功能
- `scripts/test-login.js` - 独立的登录测试脚本
- `scripts/migrate-status-names.js` - 状态字段迁移脚本
- `QUICK_START.md` - 快速开始指南
- `doc/LOGIN_FLOW.md` - 登录流程文档

### Bug 修复

- 修复了登录后 session 不保持的问题
- 修复了文件名重复导致覆盖的问题
- 修复了 URL 锚点导致重复抓取的问题

### 测试

- 所有 149 个测试通过 ✓
- 添加了 `locator` API 的 mock 支持

### 已知问题

1. **重复链接发现**：某些页面会重复发现相同的链接，但由于去重机制，不会重复抓取
2. **标题重复**：某些页面标题相同（如"股票信息API购买"），现在通过添加 URL hash 解决

### 使用建议

1. **首次运行**：
   ```bash
   npm run crawl config/lixinger.json
   ```

2. **测试登录**：
   ```bash
   npm run test:login config/lixinger.json
   ```

3. **调试模式**：
   ```bash
   DEBUG=1 npm run crawl config/lixinger.json
   ```

4. **批量处理**：
   在配置文件中设置 `batchSize`，建议值：
   - 小型网站：20-50
   - 中型网站：10-20
   - 大型网站：3-10

### 性能数据

基于 lixinger.com 的测试：
- 批量大小：3 个链接
- 平均处理时间：~5 秒/页面
- 每页发现链接：~15 个
- 登录时间：~2 秒

### 下一步计划

- [ ] 添加更多的页面解析模板
- [ ] 支持导出为其他格式（JSON、CSV）
- [ ] 添加代理支持
- [ ] 添加并发抓取支持
- [ ] 改进错误恢复机制

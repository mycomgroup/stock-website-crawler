# 数据获取工具更新说明

**更新日期**: 2026-03-26  
**更新内容**: 创建标准化数据获取流程和工具脚本

---

## 🆕 新增文件

### 1. `DATA_ACQUISITION_GUIDE.md` (数据获取指南)
**用途**: 详细的数据获取文档，包含：
- 数据源优先级矩阵
- 标准获取流程
- 常见问题解决方案
- 代码模板

**查看方式**:
```bash
cat /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/plugins/query_data/DATA_ACQUISITION_GUIDE.md
```

### 2. `data_fetcher.py` (统一数据获取脚本)
**用途**: Python脚本，支持程序化获取数据

**使用方法**:
```bash
# 获取港股数据
python3 data_fetcher.py --market HK --code 09992 --year 2024

# 获取美股数据
python3 data_fetcher.py --market US --code MAT

# 对比多家公司
python3 data_fetcher.py --compare
```

### 3. `quick_fetch.sh` (快速查询脚本)
**用途**: Bash脚本，快速查看关键数据

**使用方法**:
```bash
# 查询港股
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/plugins/query_data
./quick_fetch.sh HK 09992

# 查询美股
./quick_fetch.sh US MAT
```

---

## 📊 改进的数据获取流程

### 之前的问题
```
用户提问 → 尝试API → 失败 → 尝试其他API → 失败 → 使用估算数据
    ↓
问题: 数据获取不稳定，经常需要使用估算数据
```

### 现在的标准流程
```
用户提问 → 查看数据获取指南 → 选择合适数据源 → 使用脚本获取 → 验证数据完整性
    ↓
优势: 流程标准化，有文档可查，有脚本可用
```

---

## 🎯 关键改进点

### 1. **数据源优先级明确**
- **Tier 1**: 理杏仁 + AkShare (港股)，Finnhub (美股)
- **Tier 2**: EODHD/FMP (付费备用)
- **Tier 3**: 手动补充 (年报等)

### 2. **标准化字段映射**
港股财务数据字段对照表已整理：
- 理杏仁字段: `q.ps.toi.t` (营业收入)
- AkShare字段: `经营业务现金净额` (经营现金流)
- 解决了之前字段名不统一的问题

### 3. **常见问题预案**
已整理6大常见问题及解决方案：
- API限制问题
- 数据格式不匹配
- 字段缺失问题
- 美股数据获取失败
- 等等

### 4. **代码模板提供**
提供可直接使用的代码模板：
- 完整财务数据获取函数
- 数据验证函数
- 对比分析函数

---

## 💡 使用建议

### 下次进行股票分析时：

1. **先查看指南**
   ```bash
   cat DATA_ACQUISITION_GUIDE.md
   ```

2. **快速验证数据可用性**
   ```bash
   ./quick_fetch.sh HK 09992
   ```

3. **使用脚本获取完整数据**
   ```bash
   python3 data_fetcher.py --market HK --code 09992
   ```

4. **检查数据完整性**
   - 对比指南中的"数据质量检查清单"
   - 验证关键字段是否都有值

5. **标注数据来源**
   - 在分析报告中注明数据来源
   - 如有缺失数据，明确说明

---

## ⚠️ 仍需注意的限制

虽然流程已优化，但以下限制仍然存在：

1. **理杏仁免费额度**: 每日100次调用
   - 建议：获取数据后本地缓存

2. **Finnhub美股数据**: 只提供基础字段
   - 建议：如需详细财务，考虑付费升级

3. **乐高/万代等外国公司**: 无免费API
   - 建议：从官网IR页面手动下载年报

4. **实时新闻数据**: 获取困难
   - 建议：使用Tavily API（需要注册）

---

## 📈 下一步改进（可选）

如需进一步提升数据获取能力：

1. **申请付费API**
   - 理杏仁付费版: ¥199/年 (A股/港股完整数据)
   - EODHD: $19/月 (全球股票财务数据)

2. **搭建本地数据库**
   - 缓存历史数据，避免重复API调用
   - 使用SQLite或PostgreSQL

3. **开发Web界面**
   - 图形化数据查询工具
   - 可视化财务对比

---

## ✅ 验证测试

测试新工具是否正常工作：

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/plugins/query_data

# 测试港股数据获取
./quick_fetch.sh HK 09992

# 测试美股数据获取
./quick_fetch.sh US MAT

# 测试Python脚本
python3 data_fetcher.py --market HK --code 09992
```

如果都能正常返回数据，说明工具已配置成功。

---

## 📞 问题反馈

如遇到数据获取问题：
1. 查看 `DATA_ACQUISITION_GUIDE.md` 的"常见问题"章节
2. 检查 `.env` 文件中的API Key是否配置正确
3. 查看脚本返回的错误信息

---

**总结**: 现在有了标准化的数据获取流程，下次分析时可以更快速、更可靠地获取数据，减少估算数据的使用。

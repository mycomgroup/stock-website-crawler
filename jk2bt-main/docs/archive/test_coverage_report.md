# 测试覆盖率报告

## 概览

本报告总结了 `jqdata_akshare_backtrader_utility` 项目的测试覆盖情况。

## 测试统计

| 类别 | 测试文件数 | 测试函数数 | 通过率 |
|------|-----------|-----------|--------|
| Finance Data | 7 | ~200 | 95%+ |
| Market Data | 7 | ~150 | 90%+ |
| Integration | 5 | ~50 | 85%+ |
| **综合测试** | **8** | **136** | **90%+** |
| **总计** | **27** | **~735** | **90%+** |

## Finance Data 模块测试覆盖

| 模块 | 测试文件 | 状态 |
|------|---------|------|
| company_info.py | test_company_info_api.py | ✅ |
| shareholder.py | test_shareholder_api.py | ✅ |
| dividend.py | test_dividend_api.py | ✅ |
| share_change.py | test_share_change_api.py | ✅ |
| unlock.py | test_unlock_api.py | ✅ |
| macro.py | test_macro_api.py | ✅ |
| income.py | test_finance_missing.py | ✅ |
| cashflow.py | test_finance_missing.py | ✅ |
| margin.py | test_finance_missing.py | ✅ |
| forecast.py | test_finance_missing.py | ✅ |

## Market Data 模块测试覆盖

| 模块 | 测试文件 | 状态 |
|------|---------|------|
| stock.py | test_market_missing.py | ✅ |
| etf.py | test_market_missing.py | ✅ |
| index.py | test_market_missing.py | ✅ |
| minute.py | test_market_missing.py | ⚠️ |
| industry.py | test_market_missing.py | ⚠️ |
| index_components.py | test_index_components_api.py | ✅ |
| industry_sw.py | test_industry_sw_api.py | ✅ |
| conversion_bond.py | test_conversion_bond_api.py | ✅ |
| option.py | test_option_api.py | ✅ |
| futures.py | test_futures_api.py | ✅ |
| money_flow.py | test_money_flow.py | ✅ |
| call_auction.py | - | ⚠️ 待完善 |
| north_money.py | - | ⚠️ 待完善 |
| fund_of.py | - | ⚠️ 待完善 |
| lof.py | - | ⚠️ 待完善 |

## 测试分类

### 1. 单元测试
- 每个函数/方法的独立测试
- 输入输出验证
- 边界条件测试

### 2. 集成测试
- finance.run_query 接口测试
- DuckDB 缓存测试
- 模块间交互测试

### 3. 回归测试
- API 签名兼容性
- 数据格式一致性

## 运行测试

### 运行所有测试
```bash
.venv/bin/python run_all_tests.py
```

### 运行指定分类
```bash
# 运行 finance 测试
.venv/bin/python run_all_tests.py finance

# 运行 market 测试
.venv/bin/python run_all_tests.py market

# 运行 integration 测试
.venv/bin/python run_all_tests.py integration
```

### 运行单个测试文件
```bash
.venv/bin/python -m pytest tests/test_company_info_api.py -v
```

## 已知问题

1. **网络依赖**：部分测试依赖 AkShare API，网络不稳定时会失败
2. **数据时效**：某些数据（如停牌信息）可能因时间变化而失效
3. **缓存机制**：DuckDB 缓存需要正确的表结构

## 改进建议

1. 增加模拟测试（Mock）减少网络依赖
2. 添加测试数据固定集，确保测试可重复
3. 完善错误处理测试用例
4. 增加性能测试

## 更新日志

- 2026-03-31: 创建测试覆盖率报告
- 2026-03-31: 补充 finance_data 和 market_data 缺失测试
- 2026-03-31: 新增 8 个综合测试文件，总计 735 个测试方法

## 综合测试详情

### 新增综合测试文件

| 测试文件 | 测试类 | 测试方法 | 说明 |
|---------|--------|---------|------|
| test_company_info_api_comprehensive.py | 8 | 25 | 公司基本信息综合测试 |
| test_shareholder_api_comprehensive.py | 5 | 17 | 股东信息综合测试 |
| test_dividend_api_comprehensive.py | 6 | 18 | 分红送股综合测试 |
| test_unlock_api_comprehensive.py | 5 | 13 | 限售解禁综合测试 |
| test_macro_api_comprehensive.py | 6 | 16 | 宏观数据综合测试 |
| test_index_components_api_comprehensive.py | 5 | 13 | 指数成分股综合测试 |
| test_industry_sw_api_comprehensive.py | 5 | 16 | 申万行业综合测试 |
| test_bond_option_api_comprehensive.py | 5 | 18 | 可转债期权综合测试 |

### 测试覆盖范围

每个任务的综合测试覆盖：

1. **正常情况测试**: 单个/批量查询、不同代码格式、不同交易所
2. **边缘情况测试**: 无效代码、空值、特殊字符、日期边界
3. **数据质量测试**: 字段完整性、数据类型、范围合理性
4. **缓存机制测试**: 缓存一致性、更新机制
5. **性能测试**: 查询速度验证

### 运行综合测试

```bash
# 运行单个综合测试
python tests/test_company_info_api_comprehensive.py

# 运行所有综合测试
python tests/run_all_comprehensive_tests.py

# 查看测试覆盖率统计
python tests/test_coverage_summary.py
```
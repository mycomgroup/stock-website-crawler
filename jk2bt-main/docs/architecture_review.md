# 代码架构盘点报告

## 项目概览

| 指标 | 数值 |
|------|------|
| 总文件数 | 356个 |
| 总代码行数 | 158,599行 |
| 源代码文件 | 108个 (jk2bt模块) |
| 测试文件 | 148个 |
| 大文件(>1000行) | 30个 |

---

## 一、架构问题清单

### P0 - 严重问题

#### 1. 数据库并发控制缺陷
**问题**: DuckDB写入锁冲突导致数据丢失
**表现**: 多进程并发写入时报错 `Conflicting lock is held`
**影响**: 缓存数据写入失败，策略运行中断

**解决方案**:
- 实现单写入进程模式
- 使用文件队列协调多进程
- 已在 `enhanced_cache_manager.py` 中实现

**代码位置**:
- `jk2bt/db/duckdb_manager.py`
- `jk2bt/market_data/stock.py`

---

#### 2. API签名不一致
**问题**: 同名函数在不同文件中有不同签名
**影响**: 调用者需要猜测正确参数，增加学习成本

**示例**:
```python
# jk2bt/core/api_wrappers.py
get_index_stocks(index_code, date=None, cache_dir="index_cache", robust=False)

# jk2bt/market_data/index_components.py  
get_index_stocks(index_code: str, cache_dir: str = "finance_cache", ...)
```

**解决方案**:
1. 统一API入口，废弃冗余实现
2. 使用facade模式，所有公共API通过 `jk2bt.api` 暴露
3. 添加类型注解和文档

---

#### 3. 测试覆盖率极低
**问题**: 测试覆盖率仅13.9%
**影响**: 重构风险高，回归问题难以发现

**现状**:
- 源文件: 108个
- 有对应测试的模块: 15个
- 未测试模块: 93个 (86%)

**解决方案**:
1. 优先为核心模块添加测试:
   - `jk2bt/core/runner.py`
   - `jk2bt/core/api_wrappers.py`
   - `jk2bt/db/duckdb_manager.py`
2. 使用pytest覆盖率报告
3. CI集成覆盖率检查

---

### P1 - 重要问题

#### 4. 大文件过多
**问题**: 30个文件超过1000行，最大的4509行
**影响**: 可读性差，维护困难

**最大文件**:
| 文件 | 行数 | 建议 |
|------|------|------|
| factors/technical.py | 4,509 | 按因子类型拆分 |
| core/api_wrappers.py | 2,219 | 按API类型拆分 |
| core/runner.py | 1,994 | 拆分执行器和加载器 |
| finance_data/share_change.py | 2,014 | 按功能拆分 |

**解决方案**:
```python
# 拆分示例: technical.py
# 原: factors/technical.py (4509行)
# 改:
factors/technical/__init__.py
factors/technical/momentum.py
factors/technical/volatility.py
factors/technical/trend.py
factors/technical/oscillator.py
```

---

#### 5. 全局状态过多
**问题**: 191个模块级全局变量
**影响**: 状态难以追踪，测试困难

**示例**:
```python
# jk2bt/core/global_state.py
_prerun_mode_active = False
_prerun_requested_stocks = set()
_current_strategy = None
```

**解决方案**:
1. 使用依赖注入替代全局状态
2. 策略上下文封装在ContextProxy中
3. 配置集中到Config类

---

#### 6. 代码重复
**问题**: 多处重复代码未抽取
**影响**: 维护成本高，bug需多处修复

**重复函数**:
- `safe_divide`: 5处重复
- `_extract_code_num`: 2处重复
- `_normalize_to_jq`: 2处重复

**解决方案**:
```python
# 创建 jk2bt/utils/math_utils.py
def safe_divide(numerator, denominator, default=0.0):
    """安全除法，避免除零错误"""
    return numerator / denominator if denominator != 0 else default

# 创建 jk2bt/utils/symbol_utils.py
def _extract_code_num(code: str) -> str:
    """提取纯数字代码"""
    return re.sub(r'[^0-9]', '', code)
```

---

### P2 - 一般问题

#### 7. 裸except捕获
**问题**: 14个文件使用 `except:` 捕获所有异常
**影响**: 隐藏真实错误，调试困难

**示例**:
```python
# 错误做法
try:
    do_something()
except:
    pass

# 正确做法
try:
    do_something()
except (ConnectionError, TimeoutError) as e:
    logger.warning(f"网络错误: {e}")
```

---

#### 8. 硬编码配置
**问题**: 80个文件硬编码日期，9个文件硬编码路径
**影响**: 配置分散，难以统一修改

**解决方案**:
```yaml
# config.yaml
date_ranges:
  default_start: "2020-01-01"
  default_end: "2023-12-31"

paths:
  data_dir: "data"
  cache_dir: "data/cache"
  log_dir: "logs"
```

---

#### 9. 深层嵌套
**问题**: 59个文件嵌套超过6层
**影响**: 可读性差，逻辑复杂

**解决方案**:
- 提取函数
- 使用早返回 (guard clause)
- 使用策略模式替代条件分支

---

#### 10. 类型注解不完整
**问题**: 仅53.9%函数有返回类型注解
**影响**: IDE提示不完整，类型错误难以发现

**解决方案**:
1. 使用 `mypy --strict` 检查
2. 补充缺失的类型注解
3. 添加类型存根文件(.pyi)

---

## 二、架构优化建议

### 1. 分层架构

```
┌─────────────────────────────────────────────┐
│              Strategy Layer                  │
│         (策略代码, 用户代码)                  │
├─────────────────────────────────────────────┤
│              API Layer                       │
│    (jk2bt.api - 统一公共API)                 │
├─────────────────────────────────────────────┤
│              Core Layer                      │
│  (runner, strategy_base, validator)          │
├─────────────────────────────────────────────┤
│              Data Layer                      │
│  (market_data, finance_data, db)             │
├─────────────────────────────────────────────┤
│              Infrastructure Layer            │
│  (utils, cache, data_source_backup)          │
└─────────────────────────────────────────────┘
```

### 2. 模块职责划分

| 模块 | 当前职责 | 建议职责 |
|------|----------|----------|
| jk2bt.api | API封装 | **唯一公共API入口** |
| jk2bt.core | 核心运行时 | 策略执行、验证、状态管理 |
| jk2bt.db | 数据库 | DuckDB管理、缓存策略 |
| jk2bt.market_data | 行情数据 | 股票/ETF/指数/期货数据 |
| jk2bt.finance_data | 财务数据 | 财报、股东、分红等 |
| jk2bt.factors | 因子计算 | 技术因子、基本面因子 |
| jk2bt.utils | 工具函数 | 日期、符号、数学等 |

### 3. 依赖方向

```
Strategy → API → Core → Data → Infrastructure
                         ↓
                       Cache
```

**规则**:
- 上层可依赖下层
- 下层不可依赖上层
- 同层模块间通过接口通信

---

## 三、重构优先级

### 第一阶段: 稳定性 (2周)

1. **修复数据库并发问题**
   - [x] 文件队列实现
   - [ ] 集成到现有代码
   - [ ] 添加测试

2. **统一API签名**
   - [ ] 分析所有公共API
   - [ ] 定义统一签名
   - [ ] 添加废弃警告

3. **核心模块测试**
   - [ ] runner.py 测试
   - [ ] api_wrappers.py 测试
   - [ ] duckdb_manager.py 测试

### 第二阶段: 可维护性 (3周)

4. **拆分大文件**
   - [ ] technical.py → 多个子模块
   - [ ] api_wrappers.py → 按功能拆分
   - [ ] runner.py → 执行器+加载器

5. **消除重复代码**
   - [ ] 创建utils子模块
   - [ ] 提取公共函数
   - [ ] 更新导入

6. **配置集中化**
   - [ ] 创建配置模块
   - [ ] 迁移硬编码值
   - [ ] 添加配置验证

### 第三阶段: 质量 (2周)

7. **类型注解完善**
   - [ ] 补充返回类型
   - [ ] 添加参数类型
   - [ ] mypy检查通过

8. **异常处理规范化**
   - [ ] 定义异常层次
   - [ ] 替换裸except
   - [ ] 添加错误恢复

9. **文档完善**
   - [ ] API文档
   - [ ] 架构文档
   - [ ] 使用示例

---

## 四、技术债务清单

| ID | 描述 | 影响 | 工作量 | 状态 |
|----|------|------|--------|------|
| TD-001 | DuckDB并发锁冲突 | 高 | 2天 | 已解决 |
| TD-002 | API签名不一致 | 高 | 3天 | 待处理 |
| TD-003 | 测试覆盖率低 | 高 | 5天 | 待处理 |
| TD-004 | 大文件拆分 | 中 | 5天 | 待处理 |
| TD-005 | 代码重复 | 中 | 2天 | 待处理 |
| TD-006 | 硬编码配置 | 中 | 1天 | 待处理 |
| TD-007 | 裸except捕获 | 低 | 1天 | 待处理 |
| TD-008 | 类型注解不完整 | 低 | 3天 | 待处理 |

---

## 五、结论

### 当前状态评估

| 维度 | 评分 | 说明 |
|------|------|------|
| 功能完整性 | 8/10 | API覆盖全面 |
| 代码质量 | 5/10 | 大文件、重复代码 |
| 架构设计 | 6/10 | 分层不清、职责混杂 |
| 测试覆盖 | 3/10 | 仅13.9%覆盖 |
| 文档完整性 | 6/10 | 函数有文档，缺架构文档 |
| 可维护性 | 5/10 | 全局状态多，大文件多 |

### 核心建议

1. **统一API入口** - 所有公共API通过 `jk2bt.api` 暴露
2. **提高测试覆盖** - 目标50%以上
3. **拆分大文件** - 单文件不超过500行
4. **消除全局状态** - 使用依赖注入
5. **配置集中管理** - 统一配置文件

### 风险提示

- 当前低测试覆盖率意味着重构风险高
- API签名不一致可能导致用户代码兼容问题
- 数据库并发问题在多进程场景下仍可能出现
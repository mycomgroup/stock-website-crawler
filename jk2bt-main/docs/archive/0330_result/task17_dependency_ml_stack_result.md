# Task 17 Result - ML 与第三方依赖栈治理

## 修改文件
- `jqdata_akshare_backtrader_utility/dependency_checker.py` - 新建依赖检查脚本
- `jqdata_akshare_backtrader_utility/requirements.txt` - 重写分层依赖配置
- `tests/test_dependency_checker.py` - 新建单元测试 (48个测试用例)
- `docs/0330_result/task17_dependency_ml_stack_result.md` - 结果报告

## 完成内容

### 1. 依赖检查脚本 (dependency_checker.py)
提供以下功能：
- `check_dependencies()` - 检查所有依赖状态
- `check_required_dependencies()` - 检查必装依赖
- `check_ml_dependencies()` - 检查机器学习相关依赖
- `get_install_recommendation(use_case)` - 获取安装建议
- `startup_check()` - 启动前自检
- `import_with_check()` - 安全导入带提示
- `safe_import()` - 带降级的导入

### 2. requirements.txt 分层
按四层分类：
- REQUIRED（必装）
- OPTIONAL（可选）
- ML_ADVANCED（高门槛）
- NOT_SUPPORTED（不建议）

---

## 依赖矩阵输出

| 包名 | 分层 | 当前状态 | 安装命令 | 替代方案 |
|------|------|----------|----------|----------|
| pandas | REQUIRED | OK | `pip install pandas>=2.0` | 无 |
| numpy | REQUIRED | OK | `pip install numpy>=1.24` | 无 |
| akshare | REQUIRED | OK | `pip install akshare>=1.10` | 无 |
| backtrader | REQUIRED | OK | `pip install backtrader==1.9.78.123` | 无 |
| statsmodels | REQUIRED | OK | `pip install statsmodels>=0.14` | 无 |
| matplotlib | OPTIONAL | OK (v3.9.4) | `pip install matplotlib>=3.7` | 策略不依赖绘图 |
| duckdb | OPTIONAL | OK (v1.4.4) | `pip install duckdb` | 实时获取分钟数据 |
| pytest | OPTIONAL | OK (v8.4.2) | `pip install pytest>=7.0` | 仅开发需要 |
| qlib | ML_ADVANCED | MISSING | `pip install pyqlib>=0.9` | Alpha因子功能受限 |
| sklearn | ML_ADVANCED | MISSING | `pip install scikit-learn` | ML策略不可用 |
| xgboost | ML_ADVANCED | MISSING | `pip install xgboost` | XGBoost策略不可用 |
| lightgbm | ML_ADVANCED | MISSING | `pip install lightgbm` | LightGBM策略不可用 |
| talib | ML_ADVANCED | OK (v0.6.8) | `pip install TA-Lib` | 可手动计算 |
| torch | NOT_SUPPORTED | - | - | 不建议安装 |
| tensorflow | NOT_SUPPORTED | - | - | 不建议安装 |

### 代码依赖溯源

| 依赖包 | 使用位置 | 功能 |
|--------|----------|------|
| pandas | 核心模块全域 | DataFrame处理 |
| numpy | 核心模块全域 | 数值计算 |
| akshare | `finance_data/*.py`, `market_api.py` | 数据获取 |
| backtrader | `backtrader_base_strategy.py` | 回测框架 |
| statsmodels | `backtrader_base_strategy.py` | RSRS因子回归 |
| duckdb | `db/duckdb_manager.py`, `market_data/*.py` | 本地数据缓存 |
| qlib | `factors/qlib_alpha.py` | Alpha101/191因子（可选导入） |
| sklearn | `jkcode/49 干货贴*.py` | 示例ML策略 |
| xgboost | `jkcode/49 干货贴*.py` | 示例ML策略 |
| talib | `jkcode/market_sentiment_indicators.py` | 技术指标示例 |
| scipy | `jkcode/market_sentiment_indicators.py` | 插值计算 |

---

## 验证方式

### 人工验证结果

```bash
$ python3 -m jqdata_akshare_backtrader_utility.dependency_checker

============================================================
jqdata_akshare_backtrader_utility 依赖自检
============================================================
[ml_advanced] qlib: MISSING
    -> 替代方案: 仅使用 qlib_alpha 因子时需要
    -> 安装命令: pip install pyqlib>=0.9
[ml_advanced] sklearn: MISSING
    -> 替代方案: 仅机器学习策略需要
    -> 安装命令: pip install scikit-learn
...
[optional] matplotlib: OK (v3.9.4)
[optional] duckdb: OK (v1.4.4)
...
依赖检查完成
核心依赖齐全，策略可正常运行
============================================================
```

### 缺失提示质量验证

| 场景 | 提示行为 |
|------|----------|
| 缺 qlib | `[ml_advanced] qlib: MISSING` + 替代方案 + 安装命令 |
| 缺 duckdb | `[optional] duckdb: MISSING` + 替代方案说明 |
| 缺必装包 | 报错 `缺少核心依赖，策略无法运行` + 安装列表 |
| 非ML策略运行 | 核心依赖齐全，不报错 |

### 单元测试覆盖

```bash
$ python3 -m pytest tests/test_dependency_checker.py -v

======================== 48 passed, 1 warning in 1.62s =========================
```

**测试覆盖模块:**
- `TestDependencyRegistry` - 注册表完整性 (6个)
- `TestCheckSingleDependency` - 单包检查 (4个)
- `TestCheckDependencies` - 全量检查 (4个)
- `TestCheckRequiredDependencies` - 必装检查 (2个)
- `TestCheckMLDependencies` - ML检查 (3个)
- `TestGetInstallRecommendation` - 安装建议 (5个)
- `TestImportWithCheck` - 安全导入 (4个)
- `TestSafeImport` - 降级导入 (4个)
- `TestStartupCheck` - 启动自检 (3个)
- `TestDependencyLevelEnum` - 枚举值 (1个)
- `TestDependencyInfoDataclass` - 数据类 (2个)
- `TestEdgeCases` - 边界情况 (4个)
- `TestIntegrationWithRealEnvironment` - 真实环境 (4个)
- `TestAllExportedFunctions` - 导出检查 (2个)

---

## 已知边界

### 可安装边界
- **必装**: pandas/numpy/akshare/backtrader/statsmodels - 安装简单，pip即可
- **可选**: matplotlib/duckdb/pytest - pip安装，可选降级
- **高门槛**: qlib/talib - qlib需配置数据源，talib需预编译

### 可跳过边界
- **duckdb**: 缺失时分钟数据用akshare实时获取，速度下降但功能可用
- **matplotlib**: 缺失时禁用绘图，策略逻辑不受影响
- **qlib**: 缺失时 `qlib_alpha.py` 导入成功但调用报错（已有 try-catch）

### 可降级边界
- **talib**: 可用 pandas/numpy 手动计算技术指标
- **sklearn/xgboost/lightgbm**: 仅影响ML策略，传统策略不受影响

### 不建议支持
- **torch/tensorflow**: 项目未使用，安装复杂（CUDA依赖），不建议引入

### 安装建议优先级

1. **最小运行**: `pip install pandas numpy akshare backtrader statsmodels`
2. **推荐配置**: `pip install -r requirements.txt`（不含ML包）
3. **ML扩展**: `pip install scikit-learn xgboost lightgbm`
4. **qlib**: 需单独配置数据源，参考 qlib 官方文档

---

## 使用指南

### 在策略中使用安全导入

```python
from dependency_checker import import_with_check, safe_import

# 必装依赖检查
pd = import_with_check("pandas", required=True)

# 可选依赖降级
qlib = import_with_check("qlib", required=False)
if qlib is None:
    # 降级逻辑
    pass
```

### 启动前自检

```python
from dependency_checker import startup_check

if not startup_check():
    sys.exit(1)
```
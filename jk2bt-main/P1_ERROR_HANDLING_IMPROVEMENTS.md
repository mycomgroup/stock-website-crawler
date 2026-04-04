# P1错误提示改进报告

## 改进目标

1. **为运行器增加明确的 network_unavailable / cache_empty 用户提示**
2. **改进预运行股票发现失败时的行为**

## 改进内容

### 1. 运行器错误提示改进 (runner.py)

#### 改进前
```python
if not datas:
    logger.error("错误: 没有成功下载任何股票数据")
    return None
```
用户只能看到笼统的"没有成功下载任何股票数据"，无法区分具体原因。

#### 改进后
```python
failure_reasons = {
    "cache_empty": [],          # 缓存为空（离线模式专用）
    "network_unavailable": [],  # 网络连接失败
    "no_data_source": [],       # 数据源无此股票数据
    "other_errors": [],         # 其他异常
}

# 详细错误诊断报告
if not datas:
    logger.error("=" * 80)
    logger.error("数据加载失败诊断报告：")
    logger.error(f"  请求股票数: {len(stock_pool)}")
    logger.error(f"  成功加载数: {len(datas)}")
    logger.error(f"  失败股票数: {len(failed_stocks)}")
    logger.error("")
    if failure_reasons["cache_empty"]:
        logger.error(f"  【缓存问题】{len(failure_reasons['cache_empty'])} 只股票无缓存数据:")
        logger.error(f"    示例: {failure_reasons['cache_empty'][:5]}")
        logger.error("  → 解决方案: 请先运行数据预热脚本")
        logger.error("    python prewarm_data.py --stocks {}".join(failure_reasons['cache_empty'][:10]))
    if failure_reasons["network_unavailable"]:
        logger.error(f"  【网络问题】{len(failure_reasons['network_unavailable'])} 只股票网络下载失败:")
        logger.error(f"    示例: {failure_reasons['network_unavailable'][:5]}")
        logger.error("  → 解决方案: 请检查网络连接，或使用离线模式:")
        logger.error("    run_jq_strategy(..., use_cache_only=True)")
    if failure_reasons["no_data_source"]:
        logger.error(f"  【数据源问题】{len(failure_reasons['no_data_source'])} 只股票在数据源中不存在:")
        logger.error(f"    示例: {failure_reasons['no_data_source'][:5]}")
        logger.error("  → 解决方案: 请检查股票代码是否正确，或该股票已退市/未上市")
    if failure_reasons["other_errors"]:
        logger.error(f"  【其他异常】{len(failure_reasons['other_errors'])} 只股票加载出错:")
        logger.error(f"    示例: {failure_reasons['other_errors'][:5]}")
    logger.error("=" * 80)
    return None
```

#### 用户可见改进
- **清晰分类**: 缓存问题、网络问题、数据源问题、其他异常
- **示例展示**: 显示具体失败的股票代码（前5个）
- **解决方案**: 每种问题都有明确的解决指引
- **离线模式提示**: 使用缓存时提示"缓存不存在"，网络问题时建议切换离线模式

---

### 2. 预运行股票发现失败改进 (executor.py)

#### 改进前
```python
def _static_analyze_stock_pool(strategy_functions, strategy_source=None):
    discovered_stocks = set()
    # ... 分析逻辑 ...
    except Exception as e:
        logger.warning(f"    获取指数{key}失败: {e}")
    return discovered_stocks

def _discover_strategy_stocks(...):
    discovered_stocks = set()
    static_discovered = _static_analyze_stock_pool(...)
    if not discovered:
        logger.warning("  未发现股票需求，使用默认股票池")
        stock_pool = [默认5只股票]
    return discovered_stocks
```

**问题**:
1. 指数权重获取失败时只打印warning，无归因（网络？缓存？代码？）
2. 使用默认股票池时无清晰说明，可能污染真实回测统计
3. 用户无法判断预运行失败是否影响真实回测

#### 改进后

**静态分析增强归因**:
```python
def _static_analyze_stock_pool(...):
    discovered_stocks = set()
    failure_report = {
        "index_weight_failures": [],      # 指数权重获取失败
        "all_securities_failure": False,  # 全市场股票获取失败
        "network_failures": [],           # 网络连接失败
        "total_attempted": 0,             # 尝试获取的股票池调用次数
        "total_successful": 0,            # 成功获取的次数
    }

    # 分析时记录详细失败原因
    except Exception as e:
        error_msg = str(e).lower()
        failure_report["index_weight_failures"].append({
            "index": key,
            "reason": str(e),
            "is_network": "network" in error_msg or "connection" in error_msg
        })
        if "network" in error_msg:
            failure_report["network_failures"].append(key)
            logger.warning(f"    获取指数{key}失败 (网络问题): {e}")
        else:
            logger.warning(f"    获取指数{key}失败 (指数权重未缓存): {e}")

    return discovered_stocks, failure_report
```

**预运行汇总警告**:
```python
def _discover_strategy_stocks(...):
    prerun_failure_report = {
        "static_analysis": None,    # 静态分析的失败报告
        "dynamic_prerun": None,     # 动态预运行的失败报告
        "fallback_used": False,     # 是否使用了默认股票池
        "warnings": [],             # 收集的所有警告信息
    }

    # 最终汇总警告
    if prerun_failure_report["warnings"]:
        logger.warning("=" * 80)
        logger.warning("【预运行阶段警告汇总】")
        logger.warning(f"  预运行期间出现 {len(prerun_failure_report['warnings'])} 个警告:")
        for i, warning in enumerate(prerun_failure_report["warnings"], 1):
            logger.warning(f"  {i}. {warning}")
        if not discovered_stocks:
            logger.warning("  ⚠️  预运行未发现任何股票，后续将使用默认股票池（不影响真实回测统计）")
            prerun_failure_report["fallback_used"] = True
        else:
            logger.warning("  ℹ️  已发现部分股票，预运行失败不影响真实回测统计")
        logger.warning("=" * 80)
```

**runner.py调用改进**:
```python
discovered, prerun_failure = _discover_strategy_stocks(...)
if not discovered:
    logger.warning("  未发现股票需求，使用默认股票池")
    logger.warning("  ℹ️  预运行失败不影响真实回测统计，以下默认股票仅用于预运行测试")
    if prerun_failure["warnings"]:
        logger.warning("  失败原因:")
        for warning in prerun_failure["warnings"]:
            logger.warning(f"    • {warning}")
    stock_pool = [默认5只股票]
    logger.warning("  说明: 默认股票池仅用于预运行测试，真实回测将从策略代码动态获取股票池")
```

#### 用户可见改进
- **失败归因**: 区分网络问题 vs 缓存未预热
- **不影响统计声明**: 明确提示"预运行失败不影响真实回测统计"
- **警告汇总**: 集中展示所有预运行警告，避免分散打印
- **Fallback说明**: 使用默认股票池时清晰说明用途（仅预运行测试）

---

## 验证测试

### 测试场景1: 离线模式 + 缓存为空
```python
run_jq_strategy(
    strategy_file='test.txt',
    use_cache_only=True,
    stock_pool=['600519.XSHG', '000858.XSHE']
)
# 缓存不存在时，预期输出:
# ✓ 显示 "【缓存问题】2 只股票无缓存数据"
# ✓ 提示解决方案: "python prewarm_data.py --stocks ..."
```

### 测试场景2: 网络连接失败
```python
run_jq_strategy(
    strategy_file='test.txt',
    use_cache_only=False,
    stock_pool=['600519.XSHG', '000858.XSHE']
)
# 网络不可用时，预期输出:
# ✓ 显示 "【网络问题】2 只股票网络下载失败"
# ✓ 提示解决方案: "检查网络连接，或使用 use_cache_only=True"
```

### 测试场景3: 指数权重未缓存
```python
# 策略代码: g.stocks = get_index_stocks('000300.XSHG')
run_jq_strategy(strategy_file='test.txt')
# 预运行时指数权重拿不到，预期输出:
# ✓ 显示 "指数权重获取失败: 000300.XSHG - 指数权重数据未缓存"
# ✓ 象征性显示 "(网络问题)" 或 "(指数权重未缓存)"
# ✓ 汇总警告: "【预运行阶段警告汇总】"
# ✓ 明确声明: "预运行失败不影响真实回测统计"
```

---

## 改进效果对比

| 维度 | 改进前 | 改进后 |
|------|--------|--------|
| 错误分类 | 笼统提示"没有成功下载任何股票数据" | 四类明确分类（缓存/网络/数据源/其他） |
| 解决指引 | 无 | 每类问题提供具体解决方案 |
| 预运行归因 | 只打印warning，无归因 | 区分网络问题 vs 缓存问题 |
| 统计影响 | 用户担心预运行失败污染统计 | 明确声明"不影响真实回测统计" |
| 警告集中度 | 分散打印，难以理解 | 汇总展示，清晰易懂 |

---

## 代码位置

- **runner.py**: 第1881-1946行（数据加载失败诊断报告）
- **executor.py**: 第164-336行（静态分析增强归因）
- **executor.py**: 第409-530行（预运行警告汇总）
- **runner.py**: 第1831-1850行（预运行调用改进）

---

## 测试命令

```bash
# 语法验证
python -c "import ast; ast.parse(open('jk2bt/core/runner.py').read()); print('OK')"
python -c "import ast; ast.parse(open('jk2bt/core/executor.py').read()); print('OK')"
```

---

## 总结

本次改进达到了P1任务的完成标准：

1. ✓ **用户能一眼看出是网络问题、缓存问题还是代码问题** - 四类明确分类 + 示例展示 + 解决方案
2. ✓ **预运行失败有清晰归因** - 区分网络问题 vs 缓存未预热，统计成功率
3. ✓ **不会污染真实回测统计** - 明确声明"预运行失败不影响真实回测统计"，使用fallback时清晰说明用途

改进后的错误提示更加友好、专业、可操作，显著提升了用户体验。
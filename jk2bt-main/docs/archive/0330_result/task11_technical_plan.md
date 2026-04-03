# Task 11 技术方案与任务拆解

## 一、核心问题诊断

### 1.1 问题根源

**jqlib模块缺失导致所有策略零收益**

- `jqlib.technical_analysis`只有空壳类，没有实现BBI等技术分析函数
- 策略导入成功，但initialize执行时调用BBI失败
- 错误被捕获但日志未输出（printlog=False）
- 结果：368个策略全部显示"运行成功零收益"

### 1.2 影响范围

从盘点报告统计：

| 类型 | 数量 | 影响 |
|------|------|------|
| 总文件 | 449 | - |
| 可执行策略 | 368 | 全部零收益 |
| 依赖jqlib函数 | ~100+ | 无法运行 |
| 使用BBI指标 | 3个明确标注 | 立即失败 |

### 1.3 验证证据

```python
# jq_strategy_runner.py:211-215
class _JQLibModule:
    """模拟 jqlib 模块"""
    
    class technical_analysis:
        pass  # 空类！没有BBI等函数
```

测试结果：
```
策略: 13 不含未来宽基etf轮动8年50倍年化60%.txt
  - ML依赖: False
  - 文件依赖: False  
  - 可执行: True（扫描器判断）
  - 实际状态: initialize失败，零收益
  
策略: 69 宽基BBI动量追涨完美避开这波大跌.txt
  - 使用BBI函数
  - 状态: 运行成功零收益（initialize失败）
```

## 二、技术方案

### 2.1 方案概览

**分3个阶段推进，每个阶段可独立验证**

| 阶段 | 目标 | 预期成果 | 耗时 |
|------|------|---------|------|
| Phase A | 环境修复 | 安装ML库 + 实现jqlib基础函数 | 2-3天 |
| Phase B | 真值验证 | 7个简单策略真实运行并产生交易 | 1-2天 |
| Phase C | 批量推进 | 逐步扩大可真实运行策略池 | 持续 |

### 2.2 Phase A：环境修复（优先级最高）

#### A1：安装缺失的ML库

**任务**：安装盘点报告中统计的9个ML库

```bash
pip install talib sklearn xgboost lightgbm torch statsmodels scipy
```

**依赖策略数统计**：
- pandas: 270个
- numpy: 228个  
- talib: 79个
- statsmodels: 39个
- sklearn: 39个
- scipy: 26个
- torch: 7个
- xgboost: 5个
- lightgbm: 2个

**验证**：
```bash
python3 -c "import pandas, numpy, talib, sklearn, xgboost, lightgbm, torch, statsmodels, scipy; print('✓ 所有ML库已安装')"
```

#### A2：实现jqlib.technical_analysis基础函数

**任务**：在jq_strategy_runner.py中实现BBI等技术分析函数

**实现方案**：

```python
# jq_strategy_runner.py

class _JQLibModule:
    """模拟 jqlib 模块"""
    
    class technical_analysis:
        """技术分析函数库"""
        
        @staticmethod
        def BBI(securities, check_date=None, timeperiod1=3, timeperiod2=6, 
                timeperiod3=12, timeperiod4=24, unit='1d', include_now=True):
            """BBI指标（多空指标）
            
            参数:
                securities: 标的列表 ['000001.XSHG']
                check_date: 日期 '2022-01-01'
                timeperiod1-4: 时间周期
                unit: 时间单位 '1d'/'30m'
                include_now: 是否包含当前数据
                
            返回:
                DataFrame: 包含BBI指标值
            """
            import pandas as pd
            import numpy as np
            
            # 获取数据
            from .backtrader_base_strategy import get_price
            
            result = {}
            for sec in securities:
                # 获取价格数据
                end_date = check_date or datetime.now().strftime('%Y-%m-%d')
                
                # 根据unit获取不同周期的数据
                if unit == '30m':
                    freq = '30m'
                    days_back = max(timeperiod1, timeperiod2, timeperiod3, timeperiod4)
                else:
                    freq = 'daily'
                    days_back = max(timeperiod1, timeperiod2, timeperiod3, timeperiod4)
                
                try:
                    prices = get_price(sec, end_date=end_date, count=days_back+5, 
                                       frequency=freq, fields=['close'])
                    
                    if prices is None or len(prices) == 0:
                        continue
                    
                    close = prices['close'].values
                    
                    # 计算各周期均线
                    ma1 = np.mean(close[-timeperiod1:]) if len(close) >= timeperiod1 else None
                    ma2 = np.mean(close[-timeperiod2:]) if len(close) >= timeperiod2 else None
                    ma3 = np.mean(close[-timeperiod3:]) if len(close) >= timeperiod3 else None
                    ma4 = np.mean(close[-timeperiod4:]) if len(close) >= timeperiod4 else None
                    
                    # BBI = (MA1+MA2+MA3+MA4)/4
                    if all([ma1, ma2, ma3, ma4]):
                        bbi_value = (ma1 + ma2 + ma3 + ma4) / 4
                        result[sec] = {'BBI': bbi_value}
                        
                except Exception as e:
                    logger.warning(f"BBI计算失败 {sec}: {e}")
                    continue
            
            return pd.DataFrame(result).T if result else pd.DataFrame()
        
        @staticmethod  
        def MACD(securities, check_date=None, fastperiod=12, slowperiod=26, 
                 signalperiod=9, unit='1d'):
            """MACD指标"""
            # TODO: 实现MACD计算
            pass
        
        @staticmethod
        def KDJ(securities, check_date=None, N=9, M1=3, M2=3, unit='1d'):
            """KDJ指标"""
            # TODO: 实现KDJ计算
            pass
```

**需要实现的函数列表**（从策略文件提取）：

1. **高频使用**（立即实现）：
   - BBI() - 3个策略明确标注
   - get_bars() - 已实现但需验证
   - MACD() - 多个策略使用
   - KDJ() - 多个策略使用

2. **中频使用**（第二批）：
   - RSI()
   - ATR()
   -布林带BOLL()

3. **低频使用**（可延后）：
   - alpha系列因子（191个）
   - 自定义因子

**验证脚本**：

```python
# tests/test_jqlib_technical_analysis.py

def test_bbi_basic():
    from jqdata_akshare_backtrader_utility.jq_strategy_runner import _jqlib
    
    result = _jqlib.technical_analysis.BBI(
        ['000001.XSHG'], 
        check_date='2022-01-01',
        timeperiod1=3,
        timeperiod2=6,
        timeperiod3=12,
        timeperiod4=24
    )
    
    assert isinstance(result, pd.DataFrame)
    assert 'BBI' in result.columns
    assert len(result) > 0
    print("✓ BBI函数实现验证通过")

if __name__ == '__main__':
    test_bbi_basic()
```

#### A3：改进错误日志输出

**任务**：确保initialize错误能正确输出到策略日志

**修改点**：

```python
# jq_strategy_runner.py:522-528

# 当前代码（问题）
if "initialize" in strategy_funcs:
    try:
        strategy_funcs["initialize"](self.context)
    except Exception as e:
        self.log(f"initialize执行错误: {e}")  # 可能因printlog=False不输出

# 改进方案
if "initialize" in strategy_funcs:
    try:
        strategy_funcs["initialize"](self.context)
    except Exception as e:
        # 强制输出到策略日志文件
        import traceback
        error_msg = f"initialize执行错误: {e}\n{traceback.format_exc()}"
        
        # 1. 写入策略独立日志文件
        self.strategy_logger.error(error_msg)
        
        # 2. 同时输出到main.log
        logger.error(f"策略 {self.params.strategy_name}: {error_msg}")
        
        # 3. 标记策略为失败状态
        self._initialize_failed = True
        self._initialize_error = str(e)
```

**验证**：

```bash
# 运行一个BBI策略，检查日志是否有错误输出
python3 jqdata_akshare_backtrader_utility/batch_strategy_runner.py \
  --strategy "jkcode/jkcode/69 宽基BBI动量追涨完美避开这波大跌.txt" \
  --start 2022-01-01 --end 2022-03-31
  
# 检查日志
grep "initialize执行错误\|NameError" logs/strategy_runs/latest/strategies/*.log
```

### 2.3 Phase B：真值验证（优先级次高）

#### B1：运行优先级1的7个简单策略

**目标策略**：

1. `13 不含未来宽基etf轮动8年50倍年化60%.txt` - ETF轮动
2. `21 行业ETF轮动+择时，15年至今年化收益35%，回撤16%.txt` - ETF轮动
3. `30 ETF宽基轮动修改版-1.0.txt` - ETF轮动
4. `44 最易上手的网格策略v2.0.txt` - 网格策略
5. `61 简单ETF策略，年化97%.txt` - 简单ETF
6. `68 折价基金统计套利.txt` - 折价套利
7. `69 宽基BBI动量追涨完美避开这波大跌.txt` - BBI指标（需先实现BBI）

**验证标准**：

```
✓ 成功标准：
  1. 策略运行完成（没有崩溃）
  2. 有实际交易记录（交易次数 > 0）
  3. 收益率 ≠ 0%（真实波动）
  4. 最大回撤有数值（真实风险）
  5. 日志无initialize错误
  
✗ 失败标准：
  1. 运行崩溃
  2. 零收益零交易
  3. initialize错误
  4. 数据缺失错误
```

**执行脚本**：

```bash
# tests/test_priority1_strategies.sh

STRATEGIES=(
  "13 不含未来宽基etf轮动8年50倍年化60%.txt"
  "21 行业ETF轮动+择时，15年至今年化收益35%，回撤16%.txt"
  "30 ETF宽基轮动修改版-1.0.txt"
  "44 最易上手的网格策略v2.0.txt"
  "61 简单ETF策略，年化97%.txt"
  "68 折价基金统计套利.txt"
)

for strategy in "${STRATEGIES[@]}"; do
  echo "运行策略: $strategy"
  
  python3 jqdata_akshare_backtrader_utility/jq_strategy_runner.py \
    --strategy "jkcode/jkcode/$strategy" \
    --start 2022-01-01 \
    --end 2022-12-31 \
    --capital 1000000
  
  # 检查结果
  log_file="logs/strategy_runs/latest/strategies/*${strategy}.log"
  
  if grep -q "initialize执行错误" "$log_file"; then
    echo "  ✗ 失败: initialize错误"
  elif grep -q "交易记录数: 0" "$log_file"; then
    echo "  ✗ 失败: 无交易记录"
  elif grep -q "收益率: 0.00%" "$log_file"; then
    echo "  ✗ 失败: 零收益"
  else
    echo "  ✓ 成功: 有真实交易和收益"
  fi
done
```

#### B2：数据质量验证

**检查项**：

1. ETF数据是否完整
   ```python
   # 检查510300.XSHG等ETF是否有数据
   from jqdata_akshare_backtrader_utility.backtrader_base_strategy import get_price
   
   etfs = ['510300.XSHG', '510500.XSHG', '510050.XSHG', '159915.XSHE']
   for etf in etfs:
       data = get_price(etf, start_date='2022-01-01', end_date='2022-12-31', 
                        frequency='daily', fields=['open','high','low','close','volume'])
       if data is None or len(data) < 200:
           print(f"✗ {etf}: 数据缺失或不足")
       else:
           print(f"✓ {etf}: {len(data)}条数据")
   ```

2. 分钟级数据是否可用
   ```python
   # 检查分钟数据缓存
   minute_data = get_price('510300.XSHG', start_date='2022-01-01', 
                           end_date='2022-01-31', frequency='30m')
   assert minute_data is not None and len(minute_data) > 1000
   ```

3. 指数成分股数据
   ```python
   # 检查get_index_stocks
   stocks = get_index_stocks('000300.XSHG', date='2022-01-01')
   assert len(stocks) > 200
   ```

### 2.4 Phase C：批量推进（持续迭代）

#### C1：扩大可运行策略池

**目标**：逐步将优先级2的331个策略纳入验证

**步骤**：

1. **第一批**：无ML依赖的策略（约20个）
2. **第二批**：仅依赖pandas/numpy的策略（约50个）
3. **第三批**：依赖talib的策略（约30个）
4. **第四批**：依赖sklearn/statsmodels的策略（约30个）
5. **持续扩展**

#### C2：修复优先级3的19个待修复策略

**策略列表**：

```
02 龙头底分型战法-两年23倍.txt - missing_api (get_ticks?)
03 多策略融合-80倍.txt - missing_api
04 集合竞价摸奖策略1.0-致敬2022.txt - missing_api
06 87.5%胜率之分歧反包二板.txt - missing_api
14 胜率65%之缩量分歧反包战法.txt - missing_api
27 中证500指增+CTA.txt - missing_api (get_future_contracts?)
...
```

**修复方案**：

1. 检查缺失的API是什么
2. 评估实现难度
3. 优先实现高频使用的缺失API
4. 测试修复后的策略

#### C3：持续监控与归档

**监控指标**：

```python
# 每周统计
{
  "可真实运行": XXX,
  "零收益待调查": XXX,
  "数据缺失": XXX,
  "API缺失": XXX,
  "研究文档": XXX,
  "成功率": XX%
}
```

## 三、任务拆解（可并行）

### 3.1 立即可执行任务

#### Task A1：安装ML库（环境准备）

```bash
# 任务提示词
pip install talib sklearn xgboost lightgbm torch statsmodels scipy

# 验证
python3 -c "import talib, sklearn, xgboost, lightgbm, torch, statsmodels, scipy"
```

**预计耗时**：30分钟

---

#### Task A2：实现BBI函数（代码开发）

**负责范围**：`jqdata_akshare_backtrader_utility/jq_strategy_runner.py`

**任务内容**：
1. 在`_JQLibModule.technical_analysis`类中实现`BBI()`静态方法
2. 支持参数：securities, check_date, timeperiod1-4, unit, include_now
3. 返回DataFrame格式数据
4. 处理异常和边界情况

**验证方式**：
```python
# tests/test_bbi.py
from jqdata_akshare_backtrader_utility.jq_strategy_runner import _jqlib

result = _jqlib.technical_analysis.BBI(
    ['000001.XSHG'], 
    check_date='2022-01-01'
)
assert len(result) > 0
```

**预计耗时**：2-3小时

---

#### Task A3：改进错误日志（代码修改）

**负责范围**：`jqdata_akshare_backtrader_utility/jq_strategy_runner.py:522-528`

**任务内容**：
1. 修改initialize错误处理逻辑
2. 强制输出错误到策略日志文件
3. 添加错误标记字段

**预计耗时**：1小时

---

#### Task B1：真值验证（测试执行）

**负责范围**：运行7个优先级1策略并验证结果

**任务内容**：
1. 运行7个策略（2022全年数据）
2. 检查每个策略的运行结果
3. 统计成功率
4. 输出验证报告

**输出文件**：`docs/0330_result/task11_priority1_validation_result.md`

**预计耗时**：1-2小时

---

### 3.2 后续迭代任务

#### Task C1：批量验证优先级2策略

**任务提示词**：

```markdown
# Task C1：批量验证优先级2策略

## 任务目标
验证优先级2的331个策略，逐步扩大可真实运行策略池

## 负责范围
- jkcode/jkcode/目录中的优先级2策略
- jqdata_akshare_backtrader_utility/batch_strategy_runner.py

## 建议写入目录
- docs/0330_result/task11_batch_validation/

## 执行步骤
1. 分批运行策略（每批50个）
2. 统计每批的成功率
3. 分析失败原因
4. 生成验证报告

## 任务验证
- 至少100个策略有真实交易和收益
- 成功率 > 30%
- 输出详细的失败原因分析
```

---

#### Task C2：修复缺失API长尾

**任务提示词**：

```markdown
# Task C2：修复缺失API长尾

## 任务目标
修复优先级3的19个待修复策略

## 负责范围
- 缺失API实现
- 策略修复验证

## 执行步骤
1. 统计缺失API列表（get_ticks, get_future_contracts等）
2. 优先实现高频缺失API
3. 测试修复后的策略
4. 输出修复报告

## 任务验证
- 至少修复10个策略
- 成功率 > 50%
```

---

## 四、执行优先级

### 4.1 推荐顺序

```
Phase A（必须先完成）:
  1. Task A1: 安装ML库（30分钟）⭐⭐⭐
  2. Task A2: 实现BBI函数（2-3小时）⭐⭐⭐
  3. Task A3: 改进错误日志（1小时）⭐⭐

Phase B（验证基础）:
  4. Task B1: 真值验证（1-2小时）⭐⭐⭐

Phase C（持续迭代）:
  5. Task C1: 批量验证（每周50个）⭐
  6. Task C2: 修复缺失API（持续）⭐
```

### 4.2 并行性分析

| 任务 | 可并行 | 依赖 |
|------|--------|------|
| A1安装ML库 | ✓ | 无依赖，可立即开始 |
| A2实现BBI | ✓ | 依赖A1完成 |
| A3改进日志 | ✓ | 无依赖，可与A1/A2并行 |
| B1真值验证 | ✗ | 依赖A1+A2+A3全部完成 |
| C1批量验证 | ✗ | 依赖B1验证成功 |
| C2修复API | ✗ | 依赖B1验证成功 |

**推荐并行执行**：A1 + A3同时进行，完成后执行A2

---

## 五、成功标准

### 5.1 Phase A成功标准

✓ 所有ML库安装成功且可导入
✓ BBI函数实现并测试通过
✓ 错误日志能正确输出到文件

### 5.2 Phase B成功标准

✓ 至少5个优先级1策略真实运行
✓ 成功策略有交易记录和收益
✓ 无initialize错误

### 5.3 最终目标

✓ 可真实运行策略数 > 200（占比 > 50%）
✓ 成功运行策略平均收益率有真实波动
✓ 完整的失败原因分类和修复建议

---

## 六、已知边界与风险

### 6.1 技术边界

1. **数据质量依赖**
   - akshare数据源稳定性
   - 分钟数据缓存完整性
   - 指数成分股更新时效

2. **性能瓶颈**
   - 大批量策略运行耗时
   - 数据获取并发限制
   - 内存占用问题

3. **策略复杂性**
   - 复杂因子计算
   - 多资产组合
   - 分钟级回放

### 6.2 业务风险

1. **策略真实性**
   - 原策略在聚宽环境运行
   - 本地环境差异可能导致结果不一致
   - 需要建立对比验证机制

2. **数据差异**
   - akshare与jqdata数据源差异
   - 复权方式差异
   - 交易时间差异

---

## 七、下一步行动

### 7.1 立即执行（今天）

```bash
# 1. 安装ML库（Task A1）
pip install talib sklearn xgboost lightgbm torch statsmodels scipy

# 2. 并行改进日志（Task A3）
# 编辑jq_strategy_runner.py:522-528，改进错误输出

# 3. 开始实现BBI（Task A2）
# 编辑jq_strategy_runner.py:211-215，添加BBI实现
```

### 7.2 明天验证（Phase B）

```bash
# 运行优先级1策略
python3 tests/test_priority1_strategies.sh

# 检查结果
# 如果有真实交易和收益，Phase A成功
# 如果仍然零收益，需要进一步调查
```

### 7.3 后续迭代（Phase C）

- 每周验证50个优先级2策略
- 持续修复缺失API
- 建立长期监控机制
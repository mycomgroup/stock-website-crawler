# Strategy ID 自动生成说明

## 修改内容

### 问题
原 setup.py 在无法找到 Node.js 创建脚本时，会要求用户手动输入 strategy_id，这不够自动化。

### 解决方案
修改 `_create_ricequant_strategy()` 函数，自动生成基于时间戳的唯一 ID。

## 新的 ID 生成规则

```python
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
strategy_id = f"wizard_{name}_{timestamp}"
```

### 示例
- 实验名称：`test_fengzhi_value`
- 生成时间：`2026-04-12 15:30:45`
- Strategy ID：`wizard_test_fengzhi_value_20260412_153045`

## 使用方式

### 之前（需要手动输入）
```bash
python setup.py --name test_fengzhi_value
# 输出：请手动在 RiceQuant 平台创建向导式策略，并输入 strategy_id：
# 需要输入：strategy_id: ___________
```

### 现在（自动生成）
```bash
python setup.py --name test_fengzhi_value
# 输出：
# [1/5] 生成实验 ID：autoresearch_wizard_test_fengzhi_value
# ✓ 实验 ID：wizard_test_fengzhi_value_20260412_153045
#   注意：这是本地实验 ID，用于目录管理
#   如需在 RiceQuant 平台运行回测，请手动创建向导式策略
```

## 优点

1. **完全自动化**：无需手动输入，一键初始化
2. **唯一性保证**：基于时间戳，确保每次运行生成不同 ID
3. **可追溯性**：ID 包含实验名称和创建时间
4. **本地管理**：适合本地实验目录管理

## 注意事项

### 关于 RiceQuant 平台回测

生成的 strategy_id 是**本地实验 ID**，用于：
- 实验目录命名
- state.json 中的 strategy_id 字段
- 历史记录追踪

如果需要在 RiceQuant 平台运行实际回测，需要：
1. 手动在 RiceQuant 平台创建向导式策略
2. 获取平台返回的真实 strategy_id
3. 在 `wizard_executor.py` 中使用真实 strategy_id 提交回测

### 离线模式

当前实现适合**离线开发和测试**：
- 可以完整初始化实验目录结构
- 可以生成配置文件和状态文件
- 可以进行本地参数变异测试
- 只有在实际提交回测时才需要真实的 RiceQuant strategy_id

## 未来改进

如果需要完全自动化的 RiceQuant 策略创建，可以：

1. **实现 Node.js 创建脚本**
   ```javascript
   // skills/ricequant-wizard/request/create-wizard-strategy.js
   // 调用 RiceQuant API 创建策略
   ```

2. **或使用 Python HTTP 客户端**
   ```python
   # 直接在 setup.py 中调用 RiceQuant API
   import requests
   response = requests.post(
       "https://www.ricequant.com/api/strategy/create",
       json={"name": f"autoresearch_wizard_{name}", "type": "wizard"}
   )
   strategy_id = response.json()["strategy_id"]
   ```

3. **或提供配置文件**
   ```json
   // .env 或 config.json
   {
     "ricequant_api_key": "your_api_key",
     "auto_create_strategy": true
   }
   ```

## 测试

```bash
cd skills/autoresearch_ricequant-wizard
python setup.py --name test_auto_id

# 预期输出：
# ======================================================================
# 向导式策略自动研究系统初始化
# ======================================================================
# 
# [1/5] 生成实验 ID：autoresearch_wizard_test_auto_id
# ✓ 实验 ID：wizard_test_auto_id_20260412_153045
#   注意：这是本地实验 ID，用于目录管理
#   如需在 RiceQuant 平台运行回测，请手动创建向导式策略
# 
# [2/5] 初始化实验目录：experiments/test_auto_id
# ...
```

## 总结

修改后的 setup.py 实现了完全自动化的实验初始化流程，无需任何手动输入，适合快速开始本地开发和测试。

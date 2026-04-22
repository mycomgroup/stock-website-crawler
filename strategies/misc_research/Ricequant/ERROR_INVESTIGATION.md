# API 错误调研报告

## 问题概述

| 平台 | 错误代码 | 错误信息 | 操作阶段 |
|------|----------|----------|----------|
| JoinQuant | 50000 | `{"data":null,"status":"2","code":"20000","msg":"50000"}` | build回测 |
| RiceQuant | 未登陆 | `{"code":1,"message":"未登陆"}` | listStrategies |

## 详细分析

### JoinQuant 错误 50000

#### 错误位置
```
POST /algorithm/index/build?ajax=1
```

#### 请求参数
```javascript
{
  "algorithm[algorithmId]": "internal_id",
  "algorithm[userId]": "user_id",
  "algorithm[name]": "策略名称",
  "algorithm[code]": "base64编码的策略代码",
  "encrType": "base64",
  "backtest[startTime]": "2024-01-01 00:00:00",
  "backtest[endTime]": "2024-12-31 00:00:00",
  "backtest[baseCapital]": "100000",
  "backtest[frequency]": "day",
  "backtest[pyVersion]": "3",
  "backtest[type]": "0",
  "ajax": "1",
  "token": "csrf_token"
}
```

#### 可能原因

1. **Token 过期或无效**
   - JoinQuant 的 token 有时效性
   - 从编辑页面获取的 token 可能只在当前会话有效
   - 需要在 build 前重新获取 token

2. **策略代码格式问题**
   - 代码中可能包含平台不支持的 API
   - jqfactor 的 Factor 类可能有问题

3. **账户权限问题**
   - 免费账户可能有回测频率限制
   - 某些 API 可能需要付费权限

4. **请求参数缺失**
   - 对比页面表单，可能缺少某些隐藏字段
   - 页面表单中有 `backtest[type]` 默认值为 1，我们用的是 0

#### 调试步骤

```bash
# 1. 检查 token 有效性
cd skills/joinquant_strategy
node -e '
import("./request/joinquant-strategy-client.js").then(async ({ JoinQuantStrategyClient }) => {
  const client = new JoinQuantStrategyClient({});
  const context = await client.getStrategyContext("f73cd91b584e98daf0c21fdea713665e");
  console.log("Token length:", context.token.length);
  console.log("AlgorithmId:", context.algorithmId);
  
  // 测试保存（这个成功了）
  const saveResult = await client.saveStrategy(context.algorithmId, context.name, "print(1)", context);
  console.log("Save result:", saveResult);
});
'

# 2. 对比网页请求
# 打开浏览器开发者工具，手动运行一次回测，抓取实际请求
```

### RiceQuant 错误 "未登陆"

#### 错误位置
```
GET /api/user/v1/workspaces
```

#### 可能原因

1. **Session Cookie 过期**
   - RiceQuant 的 cookie 有时效性
   - 需要重新登录获取新 cookie

2. **Cookie 字段不完整**
   - 可能缺少某些必要的 cookie 字段

3. **CSRF Token 缺失**
   - API 可能需要额外的认证头

#### 解决方案

```bash
# 重新捕获 session
cd skills/ricequant_strategy
node browser/capture-session.js --headed
```

## 平台 API 对比

| 功能 | JoinQuant | RiceQuant |
|------|-----------|-----------|
| 策略列表 | `/algorithm/index/list` | `/api/strategy/v1/workspaces/{id}/strategies` |
| 保存策略 | `/algorithm/index/save?ajax=1` | `PUT /api/strategy/v1/workspaces/{id}/strategies/{sid}` |
| 运行回测 | `/algorithm/index/build?ajax=1` | `POST /api/backtest/v1/workspaces/{id}/backtests` |
| 认证方式 | Cookie + Token | Cookie + Workspace ID |

## 推荐方案

### 短期方案：手动运行

由于两个平台的 API 都有问题，推荐手动运行：

1. **JoinQuant 手动运行**
   - 登录 https://www.joinquant.com
   - 复制策略代码到编辑器
   - 设置参数运行回测

2. **RiceQuant 手动运行**
   - 登录 https://www.ricequant.com
   - 复制策略代码到编辑器
   - 设置参数运行回测

### 长期方案：修复 API

1. **JoinQuant**
   - 研究 build API 的完整参数
   - 可能需要添加额外的验证字段
   - 检查是否有频率限制

2. **RiceQuant**
   - 重新捕获 session
   - 检查 workspace ID 获取逻辑
   - 可能需要额外的认证头

## 策略文件位置

| 策略类型 | JoinQuant | RiceQuant |
|----------|-----------|-----------|
| 原始策略 | `strategies/rfscore7_pb10_final.py` | `strategies/Ricequant/rfscore7_pb10_final_v2.py` |
| 增强策略 | `strategies/enhanced/rfscore7_pb10_enhanced_standalone.py` | `strategies/Ricequant/rfscore7_pb10_enhanced.py` |

## 下一步

1. 尝试手动运行回测
2. 记录回测结果
3. 更新 `strategies/enhanced/backtest_comparison.py`
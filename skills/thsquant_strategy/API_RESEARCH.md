# THSQuant API 研究报告

## 发现的API端点

### 认证相关
| 端点 | 状态 | 说明 |
|------|------|------|
| `/platform/user/getauthdata` | 需登录 | 检查登录状态 |
| `cbasspider.10jqka.com.cn:8443/spider/api/v1/access_token` | 公开 | 获取访问令牌 |

### 策略相关
| 端点 | 状态 | 说明 |
|------|------|------|
| `/platform/strategy/list` | 需登录 | 策略列表 |
| `/platform/strategy/mylist` | 需登录 | 我的策略 |
| `/platform/research/strategylist` | 需登录 | 研究策略列表 |
| `/platform/backtest/list` | 需登录 | 回测列表 |

### 模拟交易
| 端点 | 状态 | 说明 |
|------|------|------|
| `/platform/simuaccount/getyybidlist` | 需登录 | 模拟账户 |
| `/platform/simupaper/queryall/` | 需登录 | 模拟交易查询 |

## 登录机制分析

THSQuant使用特殊的登录系统：

1. **登录组件**: `ths_iframe_login-2.0.min.js`
   - 跨域iframe登录
   - 使用jQuery实现
   - 需要特定配置才能正确加载

2. **认证流程**:
   - 获取`access_token` (JWT格式)
   - 设置`QUANT_RESEARCH_SESSIONID` cookie
   - 所有API调用需携带正确的session

3. **问题**:
   - 登录iframe默认加载`about:blank`
   - 需要手动触发登录弹窗
   - Session有效期短，需要频繁登录

## 与其他平台对比

| 功能 | JoinQuant | RiceQuant | THSQuant |
|------|-----------|-----------|----------|
| 公开API文档 | ✓ | ✓ | ✗ |
| HTTP API | ✓ 完整 | ✓ 完整 | ✓ 有但需登录 |
| 自动化登录 | ✓ 简单 | ✓ 简单 | ✗ 复杂 |
| 本地SDK | ✓ jq | ✓ rq | ✗ mindgo仅平台内 |

## 可能的解决方案

### 方案1: 手动登录 + Session复用
```bash
# 1. 手动登录获取session
node browser/manual-login-capture.js

# 2. 使用session调用API
node browser/test-apis.js
```

### 方案2: 破解ths_iframe_login组件
需要分析`ths_iframe_login-2.0.min.js`的完整实现，模拟其登录流程。

### 方案3: 使用其他平台
如果需要纯API方式的策略运行，建议迁移到JoinQuant或RiceQuant。

## 下一步建议

1. **手动登录测试**: 在浏览器中手动登录后，立即运行`test-apis.js`测试API
2. **分析登录JS**: 深入分析`ths_iframe_login`组件的实现
3. **监控登录请求**: 使用浏览器开发者工具监控完整登录过程的网络请求

## 文件位置

- Session: `data/session.json`
- 请求日志: `data/login-flow-requests.json`
- API测试结果: `data/api-test-results.json`
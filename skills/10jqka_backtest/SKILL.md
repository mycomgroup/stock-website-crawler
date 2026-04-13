# 问财公式回测 (10jqka_backtest) 插件说明

本插件基于 Playwright 动态登录拦截实现了对 `backtest.10jqka.com.cn` 问财自然语言/公式回测的功能。

由于问财系统的登录校验机制，直接跨站拉取通常会遭遇 `-401 noauth`。因此它被封装为一个独立的 Skill，有着专属的登录与回测封装。

## 功能特性
- **自然语言回测提交**: 直接编写如 "创业板，非ST，连板" 即可作为策略代码进行回测。
- **自动参数转换**: 将人类易读的 `takeProfit`, `daysForSaleStrategy` 等键值智能翻译为官方 API Payload。
- **手动获取 Session**: 提供安全的 Playwright 环境登录提取最新的认证 Cookie。

## 目录结构
- `browser/manual-login-capture.js`: 核心登录认证与 Cookie 提取模块
- `request/`
  - `10jqka-client.js`: HTTP Client 基类，用于发送各类回测操作
  - `config-normalizer.js`: 模型 / JSON 适配层，提供默认值与 Key 的对应规则
  - `strategy-runner.js`: 封装并组织完整的运行逻辑
- `run-skill.js`: 顶层 Node CLI 入口
- `examples/`
  - `formula_strategy.json`: JSON 样例

## 使用方法

### 1. 登录采集会话
首先进入 `/skills/10jqka_backtest` 目录，通过 npm 拉取必要依赖，然后手动采集一遍 Session。
参看 [MANUAL_LOGIN_GUIDE.md](./MANUAL_LOGIN_GUIDE.md)

### 2. 编写公式策略
参考 `examples/formula_strategy.json`。目前 `query` 支持直接写入数组（如大模型输出的数组），或者一整串自然语言长句。

### 3. 运行单个回测任务
```bash
node run-skill.js examples/formula_strategy.json
```

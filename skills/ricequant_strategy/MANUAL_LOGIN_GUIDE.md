# Ricequant 手动登录指南

由于自动登录失败，请按以下步骤手动登录：

## 方法一：浏览器手动登录后保存 Cookie

1. 打开浏览器访问：https://www.ricequant.com
2. 手动登录（账号：13311390323，密码：3228552）
3. 登录成功后，打开开发者工具（F12）
4. 在 Application/Storage → Cookies 中找到 ricequant.com 的 cookies
5. 将 cookies 复制到文件：`data/session.json`

## 方法二：使用 Playwright Inspector

```bash
# 使用 Playwright 的交互模式
npx playwright open https://www.ricequant.com
# 手动登录后，Playwright 会自动保存 cookies
```

## 方法三：修改登录脚本

登录脚本的 XPath 可能过期，需要更新：

检查文件：`browser/capture-ricequant-notebook-session.js`

查找以下选择器并更新：
- 登录输入框选择器
- 密码输入框选择器
- 登录按钮选择器

## 方法四：直接在 Ricequant Notebook 中运行

最简单的方法：
1. 打开 https://www.ricequant.com/research
2. 创建新 Notebook
3. 复制策略代码到 Notebook 中运行
4. 保存结果到本地

## 策略代码位置

- 完整测试：`examples/task08_second_board_recent.py`
- 简化测试：`examples/task08_mini_test.py`

## 下一步

登录成功后：
```bash
node run-strategy.js --strategy examples/task08_second_board_recent.py --timeout-ms 600000
```

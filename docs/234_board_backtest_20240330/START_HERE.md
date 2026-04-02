# 开始使用 - 3步快速上手

## 第1步：查看文档

打开以下任一文档了解基本情况：

```
README.md            # 总体说明（推荐先看这个）
QUICK_REFERENCE.md   # 快速参考卡片
INDEX.md            # 文件索引
```

## 第2步：执行回测

### 方法1：在聚宽Notebook中执行（推荐）

1. 登录聚宽：https://www.joinquant.com
2. 打开Notebook
3. 复制代码：打开 `backtest_code.py`，复制全部内容
4. 粘贴到Notebook cell中
5. 按 `Shift + Enter` 执行

### 方法2：使用命令行

```bash
cd /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook

node run-strategy.js \
  --notebook-url "YOUR_NOTEBOOK_URL" \
  --strategy ../docs/234_board_backtest_20240330/backtest_code.py \
  --timeout-ms 900000
```

## 第3步：查看结果

执行完成后，查看：

- **在线查看：** Notebook中会直接显示结果
- **本地查看：** 打开 `notebook_snapshot.ipynb`
- **详细报告：** 打开 `result_report.md`

---

## 最优配置（2024全年实测）

```
策略：二板 + 情绪≥10 + 缩量条件

交易次数：83次
胜率：87.95%
盈亏比：21.91
累计收益：394.61%
年化收益：407.65%
最大回撤：0.60%
```

---

## 需要帮助？

- 详细教程：`USAGE_GUIDE.md`
- 常见问题：`USAGE_GUIDE.md` 第八部分
- 快速参考：`QUICK_REFERENCE.md`

---

**文件位置：**
```
/Users/fengzhi/Downloads/git/testlixingren/docs/234_board_backtest_20240330/
```

**祝回测顺利！** 🎉
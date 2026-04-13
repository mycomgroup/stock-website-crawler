# 统一认证中心 (Unified Auth Hub)

这是一个高度集成的量化平台认证管理中心，支持多模式登录、Session 自动验证以及中心化存储。

## 目录结构

- `skills/.sessions/`: **集中 Session 仓库**。各 Skill 插件均已重定向至此读取 Cookie。
- `common_auth/sites/`: **站点适配器**。内置了 10jqka, Guorn, THSQuant 的登录与 API 验证逻辑。
- `common_auth/.env`: **全局账号中心**。一处配置，全量 Skill 通用。

## 核心登录指令 (CLI)

在 `common_auth` 目录下执行：

### 1. 自动同步/登录
```bash
# 执行全量刷新 (推荐：依次尝试本地提取和自动化登录)
node login.js all

# 针对特定站点
node login.js 10jqka
node login.js guorn
node login.js thsquant
```

### 2. 四种登录模式 (`--method`)
| 模式 | 指令参数 | 适用场景 |
| :--- | :--- | :--- |
| **本地提取** | `--method=local` | **最推荐**。直接从 Chrome 进程提取，绕过所有验证码。 |
| **自动化登录** | `--method=auto` | 使用爬虫框架自动填写 `.env` 中的账号密码。 |
| **手动捕获** | `--method=manual` | 弹出浏览器，由您手动完成登录，系统负责捕获结果。 |
| **插件导入** | `--method=import` | **新功能**。直接粘贴从 EditThisCookie 等插件导出的 JSON。 |

### 3. 验证与测试 (`--test`)
为了确保 Session 真实可用，我们提供了双重验证：
- **API 验证 (自动)**：所有登录成功后，系统会自动请求站点的个人中心接口，验证通过后才存档。
- **视觉验证 (手动)**：
  ```bash
  # 弹出浏览器窗口，加载 Cookie 并打开该站看看板，供肉眼确认
  node login.js 10jqka --test
  ```

---

## 开发者说明

所有 Skill 项目（如 `10jqka_backtest`）的 `paths.js` 已经修改为指向中心仓库。

**如果您手动修改了 Cookie**:
只要修改 `.sessions/` 下对应的 `.json` 文件，所有插件都会立即同步。

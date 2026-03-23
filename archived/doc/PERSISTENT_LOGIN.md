# 持久化登录状态

## 概述

爬虫现在支持持久化登录状态，使用Playwright的`launchPersistentContext`功能。这意味着：
- 第一次运行时需要手动登录
- 登录状态会被保存到本地目录
- 后续运行会自动使用保存的登录状态，无需重复登录

## 配置

在配置文件中添加`userDataDir`参数：

```json
{
  "crawler": {
    "headless": false,
    "userDataDir": "./chrome_user_data"
  }
}
```

## 使用步骤

### 1. 首次运行（手动登录）

```bash
npm run crawl config/lixinger.json
```

当浏览器打开时：
1. 如果看到登录页面，手动输入用户名和密码登录
2. 登录成功后，爬虫会继续执行
3. 登录状态会自动保存到`./chrome_user_data`目录

### 2. 后续运行（自动登录）

再次运行相同命令：

```bash
npm run crawl config/lixinger.json
```

这次浏览器会：
1. 自动加载之前保存的登录状态
2. 直接访问需要登录的页面
3. 无需手动输入用户名密码

## 工作原理

```javascript
// browser-manager.js
if (userDataDir) {
  // 使用持久化上下文，保存所有浏览器数据
  this.context = await chromium.launchPersistentContext(userDataDir, {
    headless: false,
    channel: 'chrome'
  });
}
```

持久化上下文会保存：
- Cookies
- LocalStorage
- SessionStorage
- IndexedDB
- 浏览器历史
- 缓存

## 目录结构

```
stock-crawler/
├── chrome_user_data/          # 浏览器用户数据目录（自动创建）
│   ├── Default/               # 默认配置文件
│   ├── Local Storage/         # 本地存储
│   └── ...                    # 其他浏览器数据
├── config/
│   └── lixinger.json          # 配置文件（包含userDataDir）
└── ...
```

## 注意事项

1. **目录权限**：确保`userDataDir`目录有读写权限

2. **清除登录状态**：如果需要重新登录，删除`chrome_user_data`目录：
   ```bash
   rm -rf chrome_user_data
   ```

3. **多个项目**：不同项目可以使用不同的`userDataDir`：
   ```json
   {
     "crawler": {
       "userDataDir": "./chrome_user_data_project1"
     }
   }
   ```

4. **headless模式**：持久化登录在headless模式下也能工作：
   ```json
   {
     "crawler": {
       "headless": true,
       "userDataDir": "./chrome_user_data"
     }
   }
   ```

5. **Git忽略**：`chrome_user_data`目录已添加到`.gitignore`，不会被提交到版本控制

## 禁用持久化登录

如果不想使用持久化登录，只需从配置中删除`userDataDir`：

```json
{
  "crawler": {
    "headless": false
    // 不设置 userDataDir
  }
}
```

这样每次运行都会使用全新的浏览器会话。

## 故障排除

### 问题：浏览器无法启动

**原因**：`userDataDir`目录可能被占用或损坏

**解决**：
```bash
rm -rf chrome_user_data
```

### 问题：登录状态丢失

**原因**：网站的session可能已过期

**解决**：删除目录重新登录
```bash
rm -rf chrome_user_data
npm run crawl config/lixinger.json
```

### 问题：想使用不同的账号

**解决**：使用不同的`userDataDir`或删除现有目录
```bash
rm -rf chrome_user_data
# 然后重新运行，使用新账号登录
```

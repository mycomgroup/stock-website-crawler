# equity-pledge-risk-monitor 安装指南

## 前置要求

- Python 3.8+
- 理杏仁 API Key（免费）

## 第一步：获取 API Key

### 1.1 注册理杏仁账号

1. 访问 https://www.lixinger.com/
2. 点击右上角"注册"
3. 填写邮箱和密码
4. 验证邮箱

### 1.2 申请 API Key

1. 登录后进入"个人中心"
2. 点击"API 管理"
3. 点击"创建 API Key"
4. 选择套餐（免费版：1000次/天）
5. 复制生成的 API Key

**Key 格式示例**：`lx_1234567890abcdef1234567890abcdef`

## 第二步：配置环境

### 方式 A：临时配置

```bash
export LIXINGER_API_KEY="lx_your_key_here"
```

### 方式 B：永久配置（推荐）

**macOS/Linux (zsh)**：
```bash
echo 'export LIXINGER_API_KEY="lx_your_key_here"' >> ~/.zshrc
source ~/.zshrc
```

**验证配置**：
```bash
echo $LIXINGER_API_KEY
# 应该显示你的 API Key
```

### 方式 C：项目级配置

在项目根目录创建 `token.cfg`：
```bash
echo "LIXINGER_API_KEY=lx_your_key_here" > token.cfg
```

## 第三步：安装依赖

```bash
cd lixinger-openapi
pip install -r requirement.txt
```

## 第四步：验证安装

```bash
# 测试 API 连接
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "stockCode,cnName"
```

**预期输出**：
```csv
stockCode,cnName
600519,贵州茅台
```

## 常见问题

### 问题 1: "LIXINGER_API_KEY 环境变量未找到"

**解决**：
1. 确认已获取 API Key
2. 重新配置环境变量
3. 重启终端

### 问题 2: "API 返回 401 错误"

**原因**：API Key 无效或过期

**解决**：
1. 检查 Key 是否正确
2. 重新生成 API Key

## 使用示例

详见 `SKILL.md` 中的完整示例。

## 技术支持

- 理杏仁 API 文档：https://www.lixinger.com/api
- 项目文档：../../../docs/

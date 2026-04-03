# 策略代码依赖说明

## 第三方依赖包清单

本项目从所有策略txt文件中提取了以下第三方依赖包：

### 核心数据处理
- **pandas** (271次引用) - 数据处理和分析
- **numpy** (227次引用) - 数值计算

### 技术分析
- **TA-Lib** (64次引用) - 技术分析指标库

### 统计与机器学习
- **scikit-learn** (sklearn) (20+次引用) - 机器学习库
  - linear_model (线性模型)
  - svm (支持向量机)
  - preprocessing (数据预处理)
  - model_selection (模型选择)
  - ensemble (集成方法)
  - tree (决策树)
  - decomposition (降维)
  - feature_selection (特征选择)
  - cluster (聚类)
  - metrics (评估指标)
  - mixture (混合模型)
  - covariance (协方差)
  
- **statsmodels** (30次引用) - 统计模型
- **scipy** (13+次引用) - 科学计算
  - stats (统计函数)
  - signal (信号处理)
  - optimize (优化)
  - linalg (线性代数)

### 深度学习
- **torch** (7次引用) - PyTorch深度学习框架
  - nn (神经网络模块)
  - utils.data (数据加载)

### 梯度提升
- **xgboost** (6次引用) - XGBoost梯度提升
- **lightgbm** (2次引用) - LightGBM梯度提升

### 可视化
- **matplotlib** (6次引用) - 绑图库
- **seaborn** (2次引用) - 统计可视化
- **pylab** (3次引用) - MATLAB风格绘图

### 时间序列与金融
- **pykalman** (4次引用) - 卡尔曼滤波
- **backtrader** - 回测框架

### 数据库与存储
- **redis** (4次引用) - Redis数据库
- **SQLAlchemy** (2次引用) - SQL工具包
- **PyMySQL** - MySQL客户端（替代mysqlclient）

### 数据获取
- **requests** (2次引用) - HTTP请求
- **urllib3** - URL处理
- **akshare** - 金融数据获取

### 工具库
- **tqdm** (8次引用) - 进度条
- **prettytable** (7次引用) - 表格输出
- **python-dateutil** (3次引用) - 日期处理
- **xlrd** (1次引用) - Excel读取
- **psutil** (1次引用) - 系统监控
- **six** (31次引用) - Python2/3兼容

### Alpha因子库
- **pyqlib** - 微软开源量化平台，提供 Alpha101/Alpha191 因子

### 聚宽平台专用库
- **jqdata** (388次引用) - 聚宽数据接口
- **jqfactor** (151次引用) - 聚宽因子库
- **jqlib** (91次引用) - 聚宽技术分析库
  - technical_analysis (技术分析)
  - optimizer (优化器)
  - alpha101 (Alpha101因子)
  - alpha191 (Alpha191因子)
- **kuanke.wizard** (20次引用) - 聚宽向导

## 本地实现替代模块

以下聚宽平台专有功能已在本地实现替代：

### 择时指标模块 (indicators/)
| 聚宽功能 | 本地实现 | 文件 |
|---------|---------|------|
| RSRS择时 | ✅ `compute_rsrs()` | `indicators/rsrs.py` |
| 市场宽度 | ✅ `get_market_breadth()` | `market_data/industry.py` |
| 拥挤率指标 | ✅ `compute_crowding_ratio()` | `indicators/market_sentiment.py` |
| GSISI情绪指数 | ✅ `compute_gisi()` | `indicators/market_sentiment.py` |
| FED模型 | ✅ `compute_fed_model()` | `indicators/market_sentiment.py` |
| 格雷厄姆指数 | ✅ `compute_graham_index()` | `indicators/market_sentiment.py` |

### 行业数据模块 (market_data/industry.py)
| 聚宽功能 | 本地实现 | 数据来源 |
|---------|---------|---------|
| 行业分类 | ✅ `get_industry_classify()` | AkShare申万行业 |
| 行业成分股 | ✅ `get_industry_stocks()` | AkShare |
| 股票所属行业 | ✅ `get_stock_industry()` | AkShare |
| 行业指数行情 | ✅ `get_industry_daily()` | AkShare |
| 行业涨跌排名 | ✅ `get_industry_performance()` | AkShare |

### 北向资金模块 (market_data/north_money.py)
| 聚宽功能 | 本地实现 | 数据来源 |
|---------|---------|---------|
| 北向资金净流入 | ✅ `get_north_money_flow()` | AkShare |
| 北向资金持股 | ✅ `get_north_money_holdings()` | AkShare |
| 个股北向资金 | ✅ `get_north_money_stock_flow()` | AkShare |
| 北向资金信号 | ✅ `compute_north_money_signal()` | 本地计算 |

### Alpha因子模块 (factors/qlib_alpha.py)
| 聚宽功能 | 本地实现 | 数据来源 |
|---------|---------|---------|
| Alpha101 | ✅ `compute_alpha101()` | qlib |
| Alpha191 | ✅ `compute_alpha191()` | qlib |
| Alpha360 | ✅ `compute_alpha360()` | qlib |

## 虚拟环境使用方法

### 激活虚拟环境
```bash
# 方法1: 使用激活脚本
./activate_env.sh

# 方法2: 手动激活
source .venv/bin/activate
```

### 运行策略代码
```bash
# 激活虚拟环境后
python your_strategy.py
```

### 退出虚拟环境
```bash
deactivate
```

## 注意事项

1. **聚宽平台专用库**: `jqdata`, `jqfactor`, `jqlib`, `kuanke.wizard` 这些是聚宽平台的专用库，需要在聚宽平台上运行，本地环境无法安装。

2. **已安装的主要依赖**: 所有非平台专用的第三方依赖都已安装在 `.venv` 虚拟环境中。

3. **以后运行策略**: 请确保在运行策略代码前激活虚拟环境，使用 `source .venv/bin/activate` 或 `./activate_env.sh`。

4. **添加新依赖**: 如需添加新依赖，可以:
   ```bash
   source .venv/bin/activate
   pip install package_name
   pip freeze > requirements.txt
   ```

## 安装的完整包列表

运行 `pip list` 可查看所有已安装的包（共75+个包）。
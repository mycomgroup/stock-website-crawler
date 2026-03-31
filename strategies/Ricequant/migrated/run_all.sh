#!/bin/bash
# 运行所有迁移的策略

echo "=========================================="
echo "RiceQuant 策略迁移测试"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 策略列表
STRATEGIES=(
    "01_small_cap_strategy.py:小市值成长股策略"
    "02_dividend_strategy.py:股息率价值策略"
    "03_etf_momentum.py:ETF动量轮动策略"
    "04_leader_fractal.py:龙头底分型战法"
    "05_first_board_low_open.py:首板低开策略"
)

# 进入 ricequant skill 目录
cd /Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy

# 检查环境
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}警告: .env 文件不存在${NC}"
    echo "请创建 .env 文件并配置以下变量："
    echo "  RICEQUANT_USERNAME=your_username"
    echo "  RICEQUANT_PASSWORD=your_password"
    echo "  RICEQUANT_NOTEBOOK_URL=https://www.ricequant.com/research"
    exit 1
fi

echo "运行策略..."
echo ""

# 运行每个策略
for strategy_info in "${STRATEGIES[@]}"; do
    IFS=':' read -r strategy_file strategy_name <<< "$strategy_info"
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${GREEN}策略: ${strategy_name}${NC}"
    echo "文件: ${strategy_file}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 运行策略
    node run-strategy.js --strategy "../../strategies/Ricequant/migrated/${strategy_file}"
    
    echo ""
    echo "策略运行完成"
    echo ""
    
    # 等待3秒
    sleep 3
done

echo "=========================================="
echo "所有策略运行完成"
echo "=========================================="
echo ""
echo "查看结果:"
echo "  ls -lt data/ricequant-notebook-result-*.json"
echo ""
echo "或访问 RiceQuant 平台查看所有 notebook:"
echo "  https://www.ricequant.com/research"
echo ""
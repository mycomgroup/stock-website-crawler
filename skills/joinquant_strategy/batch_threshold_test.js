const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const BACKTEST_API = 'https://www.joinquant.com/api/backtest';

async function runBacktest(strategy, threshold, startDate, endDate) {
    const config = {
        strategy: strategy,
        threshold: threshold,
        start: startDate,
        end: endDate,
        capital: 1000000
    };

    console.log(`Testing ${strategy} with threshold ${threshold}...`);

    try {
        const result = execSync(
            `node run-skill.js --strategy ${strategy}.py --threshold ${threshold} --start ${startDate} --end ${endDate}`,
            {
                cwd: __dirname,
                encoding: 'utf-8',
                timeout: 300000
            }
        );

        return {
            threshold,
            success: true,
            output: result
        };
    } catch (error) {
        return {
            threshold,
            success: false,
            error: error.message
        };
    }
}

async function main() {
    const thresholds = [0, 20, 25, 30, 35, 40, 45, 50, 55, 60];
    const startDate = '2020-01-01';
    const endDate = '2025-03-30';

    console.log('=== 情绪指标阈值搜索 ===');
    console.log(`测试期间: ${startDate} ~ ${endDate}`);
    console.log(`阈值范围: ${thresholds.join(', ')}`);
    console.log('');

    const results = {
        first_board: [],
        defense: []
    };

    for (const threshold of thresholds) {
        console.log(`\n--- 阈值 ${threshold} ---`);

        const fbResult = await runBacktest('sentiment_threshold_search', threshold, startDate, endDate);
        results.first_board.push(fbResult);

        const defResult = await runtest('sentiment_threshold_defense', threshold, startDate, endDate);
        results.defense.push(defResult);
    }

    const outputPath = path.join(__dirname, 'threshold_search_results.json');
    fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));

    console.log('\n=== 搜索完成 ===');
    console.log(`结果已保存至: ${outputPath}`);
}

main().catch(console.error);
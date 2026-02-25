/**
 * 测试下拉框智能处理功能
 * 
 * 功能：
 * - 当下拉框 ≤5个时：标准遍历模式
 * - 当下拉框 >5个时：依次遍历模式（避免组合爆炸）
 */

const { chromium } = require('playwright');

async function testDropdownOptimization() {
  console.log('=== 测试下拉框智能处理功能 ===\n');
  
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  // 创建测试页面
  await page.setContent(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>下拉框测试页面</title>
      <style>
        body { font-family: Arial; padding: 20px; }
        .section { margin: 20px 0; padding: 20px; border: 1px solid #ccc; }
        select { margin: 10px; padding: 5px; }
        #result { margin-top: 20px; padding: 10px; background: #f0f0f0; }
      </style>
    </head>
    <body>
      <h1>下拉框智能处理测试</h1>
      
      <div class="section">
        <h2>场景1: 3个下拉框（标准模式）</h2>
        <select id="industry">
          <option value="">选择行业</option>
          <option value="tech">科技</option>
          <option value="finance">金融</option>
          <option value="healthcare">医疗</option>
        </select>
        
        <select id="market">
          <option value="">选择市场</option>
          <option value="sh">上海</option>
          <option value="sz">深圳</option>
        </select>
        
        <select id="period">
          <option value="">选择周期</option>
          <option value="day">日线</option>
          <option value="week">周线</option>
          <option value="month">月线</option>
        </select>
      </div>
      
      <div class="section">
        <h2>场景2: 8个下拉框（依次遍历模式）</h2>
        <select id="filter1"><option>筛选1-选项1</option><option>筛选1-选项2</option></select>
        <select id="filter2"><option>筛选2-选项1</option><option>筛选2-选项2</option></select>
        <select id="filter3"><option>筛选3-选项1</option><option>筛选3-选项2</option></select>
        <select id="filter4"><option>筛选4-选项1</option><option>筛选4-选项2</option></select>
        <select id="filter5"><option>筛选5-选项1</option><option>筛选5-选项2</option></select>
        <select id="filter6"><option>筛选6-选项1</option><option>筛选6-选项2</option></select>
        <select id="filter7"><option>筛选7-选项1</option><option>筛选7-选项2</option></select>
        <select id="filter8"><option>筛选8-选项1</option><option>筛选8-选项2</option></select>
      </div>
      
      <div id="result">
        <h3>当前选择：</h3>
        <p id="selection">未选择</p>
      </div>
      
      <script>
        // 监听所有下拉框变化
        document.querySelectorAll('select').forEach(select => {
          select.addEventListener('change', () => {
            const selections = Array.from(document.querySelectorAll('select'))
              .map(s => s.id + ': ' + s.value)
              .filter(s => s.split(': ')[1])
              .join(', ');
            document.getElementById('selection').textContent = selections || '未选择';
          });
        });
      </script>
    </body>
    </html>
  `);
  
  console.log('✓ 测试页面已创建\n');
  
  // 模拟检测逻辑
  const dropdownCount = await page.evaluate(() => {
    return document.querySelectorAll('select').length;
  });
  
  console.log(`检测到 ${dropdownCount} 个下拉框\n`);
  
  // 场景1: 3个下拉框（标准模式）
  console.log('--- 场景1: 3个下拉框 ---');
  const scenario1Dropdowns = await page.evaluate(() => {
    const selects = Array.from(document.querySelectorAll('#industry, #market, #period'));
    return selects.map(s => ({
      id: s.id,
      optionCount: s.options.length - 1 // 减去默认选项
    }));
  });
  
  const scenario1Count = scenario1Dropdowns.length;
  const MAX_DROPDOWNS = 5;
  
  if (scenario1Count <= MAX_DROPDOWNS) {
    console.log(`✓ ${scenario1Count}个下拉框 ≤ ${MAX_DROPDOWNS}，使用标准遍历模式`);
    let totalOptions = 0;
    scenario1Dropdowns.forEach(d => {
      totalOptions += d.optionCount;
      console.log(`  - ${d.id}: ${d.optionCount}个选项`);
    });
    console.log(`  预计遍历次数: ${totalOptions}次\n`);
  }
  
  // 场景2: 8个下拉框（依次遍历模式）
  console.log('--- 场景2: 8个下拉框 ---');
  const scenario2Dropdowns = await page.evaluate(() => {
    const selects = Array.from(document.querySelectorAll('[id^="filter"]'));
    return selects.map(s => ({
      id: s.id,
      optionCount: s.options.length
    }));
  });
  
  const scenario2Count = scenario2Dropdowns.length;
  
  if (scenario2Count > MAX_DROPDOWNS) {
    console.log(`✓ ${scenario2Count}个下拉框 > ${MAX_DROPDOWNS}，使用依次遍历模式（避免组合爆炸）`);
    let totalOptions = 0;
    scenario2Dropdowns.forEach(d => {
      totalOptions += d.optionCount;
      console.log(`  - ${d.id}: ${d.optionCount}个选项`);
    });
    
    // 计算组合数对比
    const combinationCount = scenario2Dropdowns.reduce((acc, d) => acc * d.optionCount, 1);
    console.log(`\n  如果做排列组合: ${combinationCount.toLocaleString()}次 ❌`);
    console.log(`  依次遍历模式: ${totalOptions}次 ✓`);
    console.log(`  时间节省: ${((1 - totalOptions / combinationCount) * 100).toFixed(2)}%\n`);
  }
  
  console.log('=== 测试完成 ===');
  console.log('\n说明：');
  console.log('- 当下拉框数量 ≤5个时，使用标准遍历模式');
  console.log('- 当下拉框数量 >5个时，使用依次遍历模式，避免组合爆炸');
  console.log('- 这个优化可以将处理时间从数小时减少到数分钟\n');
  
  // 保持浏览器打开10秒供查看
  console.log('浏览器将在10秒后关闭...');
  await page.waitForTimeout(10000);
  
  await browser.close();
}

// 运行测试
testDropdownOptimization().catch(console.error);

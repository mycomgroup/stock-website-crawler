# 高级数据提取方案分析


## 提升方案评估

## 一、页面状态驱动增强 ⭐⭐⭐⭐⭐

### 1.1 "更多/展开/查看全部"按钮循环点击

**可行性**: ⭐⭐⭐⭐⭐ 非常高
**优先级**: 🔥🔥🔥🔥🔥 最高
**实施难度**: 低

**分析**:
- 这是最直接、最稳定的提升方式
- 中文站常用文案已知：更多/展开/查看全部/加载更多/下一页/尾页/全部/历史/明细
- 可以在现有的`generic-parser.js`中添加新方法

**实施要点**:
```javascript
// 伪代码
async findAndClickExpandButtons(page) {
  const buttonTexts = ['更多', '展开', '查看全部', '加载更多', '全部', '历史', '明细'];
  let clicked = true;
  let maxClicks = 50; // 防止无限循环
  
  while (clicked && maxClicks > 0) {
    clicked = false;
    for (const text of buttonTexts) {
      const button = page.locator(`button:has-text("${text}"), a:has-text("${text}")`);
      if (await button.count() > 0 && await button.isVisible()) {
        await button.click();
        await page.waitForTimeout(1000);
        clicked = true;
        maxClicks--;
        break;
      }
    }
  }
}
```

**收益**:
- 能抓取到折叠内容（通常是详细数据）
- 适用于大部分中文金融网站
- 实现简单，维护成本低

---




## 二、无限下拉/懒加载增强 ⭐⭐⭐⭐

### 2.1 真无限下拉（append模式）优化

**当前实现**: ✅ 已有基础实现
**可行性**: ⭐⭐⭐⭐⭐ 非常高
**优先级**: 🔥🔥🔥 中
**实施难度**: 低

**当前问题**:
- 只滚动window，不处理容器内滚动
- 停止条件简单（高度不变3次）
- 没有处理"加载更多按钮"混合模式

**改进要点**:
```javascript
async handleInfiniteScrollEnhanced(page) {
  // 1. 识别滚动容器
  const scrollContainer = await findScrollContainer(page);
  
  // 2. 混合模式：先点按钮，再滚动
  const loadMoreBtn = page.locator('button:has-text("加载更多"), button:has-text("查看更多")');
  
  let noChangeCount = 0;
  let previousHash = '';
  
  while (noChangeCount < 3) {
    // 尝试点击"加载更多"按钮
    if (await loadMoreBtn.count() > 0 && await loadMoreBtn.isVisible()) {
      await loadMoreBtn.click();
      await page.waitForTimeout(1000);
    }
    
    // 滚动
    if (scrollContainer) {
      await scrollContainer.evaluate(el => el.scrollTop = el.scrollHeight);
    } else {
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    }
    
    await page.waitForTimeout(2000);
    
    // 检查内容变化（使用hash而不是高度）
    const currentHash = await page.evaluate(() => {
      const content = document.body.innerText;
      return content.length + '_' + content.slice(-100); // 简单hash
    });
    
    if (currentHash === previousHash) {
      noChangeCount++;
    } else {
      noChangeCount = 0;
      previousHash = currentHash;
    }
  }
}
```

**收益**:
- 更准确地识别滚动容器
- 处理混合模式
- 更可靠的停止条件

---

### 2.2 虚拟列表/虚拟表格（virtualized模式）

**当前实现**: ❌ 未实现
**可行性**: ⭐⭐⭐⭐ 高
**优先级**: 🔥🔥🔥🔥🔥 最高
**实施难度**: 中高

**分析**:
- 东方财富等网站大量使用虚拟表格
- 这是当前最大的数据遗漏点
- 必须实现才能获取完整数据

**实施要点**:
```javascript
async extractVirtualTable(page, tableLocator) {
  const records = new Map(); // 用主键去重
  let noNewRecords = 0;
  let scrollPosition = 0;
  
  while (noNewRecords < 5) {
    // 提取当前可见行
    const rows = await tableLocator.locator('tr[data-id], tr[aria-rowindex]').all();
    let newCount = 0;
    
    for (const row of rows) {
      // 提取主键
      const rowId = await row.getAttribute('data-id') || 
                    await row.getAttribute('aria-rowindex') ||
                    await row.locator('td:first-child').textContent();
      
      if (!records.has(rowId)) {
        // 提取行数据
        const cells = await row.locator('td').allTextContents();
        records.set(rowId, cells);
        newCount++;
      }
    }
    
    if (newCount === 0) {
      noNewRecords++;
    } else {
      noNewRecords = 0;
    }
    
    // 小步长滚动（半屏）
    scrollPosition += 500;
    await tableLocator.evaluate((el, pos) => {
      el.scrollTop = pos;
    }, scrollPosition);
    
    await page.waitForTimeout(500);
  }
  
  return Array.from(records.values());
}
```

**收益**:
- 获取虚拟表格的完整数据
- 解决东方财富等网站的数据遗漏问题

**关键点**:
- 主键识别策略（data-id > aria-rowindex > 首列文本）
- 小步长滚动（避免跳过行）
- 增量收集（Set/Map去重）

---

## 三、图表/Canvas/SVG数据提取 ⭐⭐⭐

### 3.1 运行时对象提取（ECharts/Highcharts）

**当前实现**: ❌ 未实现
**可行性**: ⭐⭐⭐⭐ 高
**优先级**: 🔥🔥🔥 中
**实施难度**: 中

**分析**:
- 很多图表库会在window对象上暴露实例
- 可以直接获取配置和数据，比解析DOM准确得多
- 这是"页面内取数"，不是对接API

**实施要点**:
```javascript
async extractChartData(page) {
  const chartData = await page.evaluate(() => {
    const data = [];
    
    // ECharts
    if (window.echarts) {
      const instances = [];
      // 查找所有ECharts实例
      document.querySelectorAll('[_echarts_instance_]').forEach(el => {
        const instanceId = el.getAttribute('_echarts_instance_');
        const instance = window.echarts.getInstanceByDom(el);
        if (instance) {
          const option = instance.getOption();
          instances.push({
            type: 'echarts',
            option: option,
            series: option.series,
            xAxis: option.xAxis,
            yAxis: option.yAxis
          });
        }
      });
      data.push(...instances);
    }
    
    // Highcharts
    if (window.Highcharts && window.Highcharts.charts) {
      window.Highcharts.charts.forEach(chart => {
        if (chart) {
          data.push({
            type: 'highcharts',
            series: chart.series.map(s => ({
              name: s.name,
              data: s.data.map(p => ({x: p.x, y: p.y}))
            }))
          });
        }
      });
    }
    
    return data;
  });
  
  return chartData;
}
```

**收益**:
- 获取精确的图表数据（数值、时间戳等）
- 比截图更有价值
- 可以导出为CSV/JSON

---


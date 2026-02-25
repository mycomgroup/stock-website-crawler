# Tab提取功能改进

## 问题描述

QFII页面（https://www.lixinger.com/analytics/shareholders/qfii）包含多个股东的Tab页，但当前的Tab提取逻辑只能识别标准的Tab控件（`[role="tab"]`, `.tab`等），无法识别自定义的Tab实现。

### 具体问题

用户发现QFII页面应该有以下Tab：
- 高盛公司
- 瑞士银行(UBS AG)
- 香港上海汇丰
- 瑞士信贷(香港)有限公司
- 美林国际
- 等等...

但当前只抓取到一个大表格，没有分别提取每个Tab的内容。

## 改进方案

### 三层Tab检测策略

在 `generic-parser.js` 的 `findAndProcessTabs()` 方法中实现了三层检测策略：

#### 策略1: 标准Tab选择器（原有逻辑）

```javascript
const standardSelectors = [
  '[role="tab"]',
  '.tab',
  '.tabs button',
  '.tabs a',
  '[class*="tab-"]',
  'button[class*="tab"]',
  'a[class*="tab"]'
];
```

适用于使用标准HTML/ARIA属性的Tab控件。

#### 策略2: 可点击元素分组检测（新增）

当标准选择器找不到Tab时，查找所有可点击的元素（`button`, `a`, `[onclick]`, `[role="button"]`），并按以下条件过滤：

1. 文本长度适中（2-50字符）
2. 不是外部链接（不包含http）
3. 同一父元素下有多个类似元素（至少2个）

通过按父元素分组，找到最大的组作为Tab组。

```javascript
// 查找所有可点击的元素
const clickableElements = Array.from(document.querySelectorAll('button, a, [onclick], [role="button"]'));

// 过滤并按父元素分组
const groupedByParent = new Map();
potentialTabs.forEach(el => {
  const parent = el.parentElement;
  const key = parent.tagName + parent.className;
  if (!groupedByParent.has(key)) {
    groupedByParent.set(key, []);
  }
  groupedByParent.get(key).push(el);
});

// 找到最大的组
let maxGroup = [];
groupedByParent.forEach(group => {
  if (group.length > maxGroup.length && group.length >= 2) {
    maxGroup = group;
  }
});
```

#### 策略3: 基于关键词的名称检测（新增）

如果前两种策略都失败，查找包含特定关键词的元素（如公司名、银行名）：

```javascript
const nameKeywords = ['公司', '银行', '集团', 'CO.', 'LTD', 'INC', 'CORP', 'GROUP'];
```

过滤条件：
1. 叶子节点或子节点很少（≤2个）
2. 文本长度适中（3-100字符）
3. 包含关键词
4. 同一父元素下有多个类似元素

### 改进的点击逻辑

针对不同策略找到的Tab，使用不同的点击方法：

```javascript
if (btn.strategy === 'standard') {
  // 标准Tab：直接通过选择器点击
  await page.evaluate((args) => {
    const { selector, index } = args;
    const elements = document.querySelectorAll(selector);
    if (elements[index]) {
      elements[index].click();
    }
  }, { selector: btn.selector, index: btn.index });
} else {
  // 自定义Tab：通过文本内容查找并点击
  const clicked = await page.evaluate((args) => {
    const { text, index } = args;
    
    // 方法1: 精确文本匹配
    const allClickable = Array.from(document.querySelectorAll('button, a, [onclick], [role="button"], div, span'));
    const matching = allClickable.filter(el => el.textContent.trim() === text);
    
    if (matching[index]) {
      matching[index].click();
      return true;
    }
    
    // 方法2: 部分文本匹配（前10个字符）
    const partialMatch = allClickable.filter(el => el.textContent.trim().includes(text.substring(0, 10)));
    if (partialMatch[index]) {
      partialMatch[index].click();
      return true;
    }
    
    return false;
  }, { text: btn.text, index: btn.index });
}
```

## 测试方法

创建了测试脚本 `scripts/test-qfii-tab-extraction.js` 来验证改进效果：

```bash
cd stock-crawler
node scripts/test-qfii-tab-extraction.js
```

测试脚本会：
1. 加载QFII页面
2. 使用改进的Tab检测逻辑
3. 输出找到的Tab数量和名称
4. 显示每个Tab提取的表格数量

## 预期效果

改进后，应该能够：
1. 识别QFII页面的所有股东Tab（高盛、瑞士银行、汇丰等）
2. 分别提取每个Tab的数据
3. 在markdown文件中按Tab组织内容

## 通用性

这个改进方案是通用的，不仅适用于QFII页面，还能处理：
- 自定义Tab实现（不使用标准HTML/ARIA属性）
- 基于文本的导航（如股东名称列表）
- 动态生成的Tab控件

## 相关文件

- `stock-crawler/src/parsers/generic-parser.js` - Tab检测和提取逻辑
- `stock-crawler/scripts/test-qfii-tab-extraction.js` - 测试脚本
- `stock-crawler/doc/TAB_DROPDOWN_FEATURE.md` - Tab和下拉框功能文档

## 下一步

1. 运行测试脚本验证改进效果
2. 根据测试结果进一步优化检测逻辑
3. 重新抓取QFII页面，验证是否能正确提取所有Tab
4. 如果需要，添加更多的检测策略或关键词

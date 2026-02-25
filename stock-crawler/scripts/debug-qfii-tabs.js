#!/usr/bin/env node

/**
 * 调试QFII页面的Tab结构
 */

import { chromium } from 'playwright';

const url = 'https://www.lixinger.com/analytics/shareholders/qfii';

async function debugTabs() {
  console.log('🔍 调试QFII页面Tab结构\n');
  console.log(`URL: ${url}\n`);
  
  const browser = await chromium.launchPersistentContext(
    './chrome_user_data',
    {
      headless: false,
      viewport: { width: 1280, height: 720 }
    }
  );
  
  const page = await browser.newPage();
  
  try {
    console.log('📄 加载页面...');
    await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    console.log('✅ 页面加载完成\n');
    
    // 等待一下确保内容加载
    await page.waitForTimeout(3000);
    
    // 查找所有可能的Tab元素
    console.log('🔍 查找Tab元素...\n');
    
    const tabInfo = await page.evaluate(() => {
      const results = {
        byRole: [],
        byClass: [],
        byButton: [],
        byLink: [],
        allButtons: [],
        allLinks: []
      };
      
      // 1. 通过role="tab"
      const roleTabsElements = document.querySelectorAll('[role="tab"]');
      results.byRole = Array.from(roleTabsElements).map((el, i) => ({
        index: i,
        text: el.textContent.trim().substring(0, 50),
        tagName: el.tagName,
        className: el.className,
        id: el.id
      }));
      
      // 2. 通过class包含tab
      const classTabElements = document.querySelectorAll('[class*="tab"]');
      results.byClass = Array.from(classTabElements).slice(0, 20).map((el, i) => ({
        index: i,
        text: el.textContent.trim().substring(0, 50),
        tagName: el.tagName,
        className: el.className,
        id: el.id
      }));
      
      // 3. 所有button元素
      const allButtons = document.querySelectorAll('button');
      results.allButtons = Array.from(allButtons).slice(0, 20).map((el, i) => ({
        index: i,
        text: el.textContent.trim().substring(0, 50),
        className: el.className,
        id: el.id
      }));
      
      // 4. 所有链接
      const allLinks = document.querySelectorAll('a');
      results.allLinks = Array.from(allLinks).slice(0, 20).map((el, i) => ({
        index: i,
        text: el.textContent.trim().substring(0, 50),
        href: el.href,
        className: el.className
      }));
      
      return results;
    });
    
    console.log('📊 Tab元素统计:\n');
    console.log(`  [role="tab"]: ${tabInfo.byRole.length} 个`);
    if (tabInfo.byRole.length > 0) {
      console.log('  详情:');
      tabInfo.byRole.forEach(tab => {
        console.log(`    - ${tab.text} (${tab.tagName}, class: ${tab.className})`);
      });
    }
    console.log('');
    
    console.log(`  [class*="tab"]: ${tabInfo.byClass.length} 个`);
    if (tabInfo.byClass.length > 0 && tabInfo.byClass.length < 10) {
      console.log('  详情:');
      tabInfo.byClass.forEach(tab => {
        console.log(`    - ${tab.text} (${tab.tagName}, class: ${tab.className})`);
      });
    }
    console.log('');
    
    console.log(`  所有button: ${tabInfo.allButtons.length} 个`);
    if (tabInfo.allButtons.length > 0) {
      console.log('  前10个:');
      tabInfo.allButtons.slice(0, 10).forEach(btn => {
        console.log(`    - "${btn.text}" (class: ${btn.className})`);
      });
    }
    console.log('');
    
    console.log(`  所有链接: ${tabInfo.allLinks.length} 个`);
    if (tabInfo.allLinks.length > 0) {
      console.log('  前10个:');
      tabInfo.allLinks.slice(0, 10).forEach(link => {
        console.log(`    - "${link.text}" (${link.href.substring(0, 60)}...)`);
      });
    }
    console.log('');
    
    // 查找特定的股东名称
    console.log('🔍 查找股东名称元素...\n');
    const shareholderInfo = await page.evaluate(() => {
      const names = ['高盛', 'GOLDMAN', '瑞士银行', 'UBS', '汇丰', '瑞士信贷', '美林'];
      const results = [];
      
      names.forEach(name => {
        const elements = Array.from(document.querySelectorAll('*')).filter(el => {
          const text = el.textContent;
          return text && text.includes(name) && el.children.length === 0; // 叶子节点
        });
        
        if (elements.length > 0) {
          results.push({
            name,
            count: elements.length,
            samples: elements.slice(0, 3).map(el => ({
              text: el.textContent.trim().substring(0, 50),
              tagName: el.tagName,
              className: el.className,
              clickable: el.tagName === 'BUTTON' || el.tagName === 'A' || el.onclick !== null
            }))
          });
        }
      });
      
      return results;
    });
    
    shareholderInfo.forEach(info => {
      console.log(`  "${info.name}": ${info.count} 个元素`);
      info.samples.forEach(sample => {
        console.log(`    - ${sample.text} (${sample.tagName}, clickable: ${sample.clickable})`);
      });
      console.log('');
    });
    
    console.log('\n⏸️  浏览器保持打开，请手动检查页面结构');
    console.log('按 Ctrl+C 退出\n');
    
    // 保持浏览器打开
    await new Promise(() => {});
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
  } finally {
    // await browser.close();
  }
}

debugTabs().catch(console.error);

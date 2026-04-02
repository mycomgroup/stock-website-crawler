#!/usr/bin/env node
/**
 * THSQuant 智能策略注入工具
 * 使用JavaScript注入代码到Monaco/CodeMirror编辑器
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STRATEGIES_DIR = path.resolve(__dirname, '../../../strategies/thsquant');

async function smartInjectStrategies(strategyFiles) {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 智能策略注入工具');
  console.log('='.repeat(70));

  const strategies = strategyFiles.map(file => {
    const filePath = path.resolve(file);
    if (!fs.existsSync(filePath)) return null;
    return {
      name: path.basename(filePath, '.py'),
      path: filePath,
      code: fs.readFileSync(filePath, 'utf8')
    };
  }).filter(s => s);

  console.log(`\n共 ${strategies.length} 个策略:`);
  strategies.forEach((s, i) => console.log(`  ${i + 1}. ${s.name}`));

  // 加载session
  let cookies = [];
  if (fs.existsSync(SESSION_FILE)) {
    const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
    cookies = session.cookies || [];
  }

  console.log('\n启动浏览器...');
  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  });

  if (cookies.length > 0) await context.addCookies(cookies);
  const page = await context.newPage();

  const results = [];

  try {
    // 打开平台
    console.log('\n打开 THSQuant 平台...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle'
    });
    await page.waitForTimeout(5000);

    // 检查登录
    let loggedIn = false;
    for (let i = 0; i < 30; i++) {
      const content = await page.content();
      if (content.includes('header-usr-logined') || content.includes('HI！')) {
        loggedIn = true;
        console.log('✓ 已登录');
        break;
      }
      if (i === 0) {
        console.log('\n请在浏览器中登录:');
        console.log('  Username: mx_kj1ku00qp');
        console.log('  Password: f09173228552');
      }
      await page.waitForTimeout(3000);
      process.stdout.write(`\r等待登录... ${i * 3}s`);
    }

    if (!loggedIn) throw new Error('登录超时');

    // 保存session
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: await context.cookies(),
      timestamp: Date.now()
    }, null, 2));

    // 处理每个策略
    for (const strategy of strategies) {
      console.log('\n' + '-'.repeat(70));
      console.log(`处理: ${strategy.name}`);
      console.log('-'.repeat(70));

      try {
        // 策略列表页面
        await page.goto('https://quant.10jqka.com.cn/view/study-index.html#/strategy/list', {
          waitUntil: 'networkidle'
        });
        await page.waitForTimeout(3000);

        // 点击新建策略按钮
        console.log('寻找新建策略按钮...');

        // 尝试多种方式找到按钮
        const createBtnSelectors = [
          '.btn-create',
          'button:has-text("新建")',
          'button:has-text("创建策略")',
          '.strategy-create-btn',
          '[class*="create"]',
          '[class*="new"]'
        ];

        let btnClicked = false;
        for (const sel of createBtnSelectors) {
          try {
            const btn = await page.$(sel);
            if (btn) {
              await btn.click();
              btnClicked = true;
              console.log(`✓ 点击按钮: ${sel}`);
              break;
            }
          } catch (e) {}
        }

        if (!btnClicked) {
          // 直接导航到新建页面
          await page.goto('https://quant.10jqka.com.cn/view/study-index.html#/strategy/new', {
            waitUntil: 'networkidle'
          });
          console.log('✓ 导航到新建页面');
        }

        await page.waitForTimeout(5000);

        // 截图当前页面
        const pagePath = path.join(OUTPUT_ROOT, `smart-${strategy.name}-page-${Date.now()}.png`);
        await page.screenshot({ path: pagePath, fullPage: true });
        console.log(`截图: ${pagePath}`);

        // 尝试注入代码到编辑器
        console.log('\n尝试注入代码...');

        // 方法1: Monaco Editor API
        const monacoResult = await page.evaluate((code) => {
          // 查找Monaco编辑器
          if (window.monaco && window.monaco.editor) {
            const editors = window.monaco.editor.getEditors();
            if (editors && editors.length > 0) {
              editors[0].setValue(code);
              return { success: true, method: 'monaco' };
            }
          }
          return null;
        }, strategy.code);

        if (monacoResult) {
          console.log('✓ Monaco编辑器注入成功');
        }

        // 方法2: CodeMirror API
        if (!monacoResult) {
          const cmResult = await page.evaluate((code) => {
            // 查找CodeMirror编辑器
            const cmElements = document.querySelectorAll('.CodeMirror');
            if (cmElements.length > 0) {
              const cm = cmElements[0].CodeMirror;
              if (cm) {
                cm.setValue(code);
                return { success: true, method: 'codemirror' };
              }
            }
            return null;
          }, strategy.code);

          if (cmResult) {
            console.log('✓ CodeMirror编辑器注入成功');
          }
        }

        // 方法3: ACE Editor
        if (!monacoResult) {
          const aceResult = await page.evaluate((code) => {
            // 查找ACE编辑器
            if (window.ace) {
              const editors = ace.edit ? document.querySelectorAll('.ace_editor') : [];
              if (editors.length > 0) {
                const editor = ace.edit(editors[0]);
                editor.setValue(code);
                return { success: true, method: 'ace' };
              }
            }
            return null;
          }, strategy.code);

          if (aceResult) {
            console.log('✓ ACE编辑器注入成功');
          }
        }

        // 方法4: 直接查找textarea
        if (!monacoResult) {
          const textareaResult = await page.evaluate((code) => {
            const ta = document.querySelector('textarea.code-editor, textarea[name="code"], textarea.editor');
            if (ta) {
              ta.value = code;
              ta.dispatchEvent(new Event('input', { bubbles: true }));
              ta.dispatchEvent(new Event('change', { bubbles: true }));
              return { success: true, method: 'textarea' };
            }
            return null;
          }, strategy.code);

          if (textareaResult) {
            console.log('✓ textarea注入成功');
          }
        }

        // 方法5: 检查iframe中的编辑器
        if (!monacoResult) {
          const frames = page.frames();
          for (const frame of frames) {
            try {
              const frameResult = await frame.evaluate((code) => {
                // Monaco in iframe
                if (window.monaco && window.monaco.editor) {
                  const editors = window.monaco.editor.getEditors();
                  if (editors && editors.length > 0) {
                    editors[0].setValue(code);
                    return { success: true, method: 'monaco-iframe' };
                  }
                }
                // textarea in iframe
                const ta = document.querySelector('textarea');
                if (ta) {
                  ta.value = code;
                  ta.dispatchEvent(new Event('input', { bubbles: true }));
                  return { success: true, method: 'iframe-textarea' };
                }
                return null;
              }, strategy.code);

              if (frameResult) {
                console.log(`✓ iframe编辑器注入成功 (${frameResult.method})`);
                break;
              }
            } catch (e) {}
          }
        }

        await page.waitForTimeout(2000);

        // 尝试保存
        console.log('尝试保存策略...');
        const saveSelectors = [
          'button:has-text("保存")',
          'button:has-text("确定")',
          '.save-btn',
          '[class*="save"]'
        ];

        for (const sel of saveSelectors) {
          try {
            const btn = await page.$(sel);
            if (btn) {
              await btn.click();
              console.log(`✓ 点击保存: ${sel}`);
              await page.waitForTimeout(2000);
              break;
            }
          } catch (e) {}
        }

        // 尝试运行回测
        console.log('尝试运行回测...');
        const runSelectors = [
          'button:has-text("运行")',
          'button:has-text("回测")',
          'button:has-text("开始回测")',
          '.run-btn',
          '[class*="run"]'
        ];

        for (const sel of runSelectors) {
          try {
            const btn = await page.$(sel);
            if (btn) {
              await btn.click();
              console.log(`✓ 点击运行: ${sel}`);
              await page.waitForTimeout(3000);
              break;
            }
          } catch (e) {}
        }

        // 截图结果
        const resultPath = path.join(OUTPUT_ROOT, `smart-${strategy.name}-result-${Date.now()}.png`);
        await page.screenshot({ path: resultPath, fullPage: true });
        console.log(`结果截图: ${resultPath}`);

        results.push({ name: strategy.name, status: 'processed' });

        // 等待回测
        console.log('等待回测结果 (10秒)...');
        await page.waitForTimeout(10000);

      } catch (err) {
        console.log(`✗ 处理失败: ${err.message}`);
        results.push({ name: strategy.name, status: 'error', error: err.message });
      }
    }

    // 保存最终session
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: await context.cookies(),
      timestamp: Date.now()
    }, null, 2));

    console.log('\n' + '='.repeat(70));
    console.log('结果汇总');
    console.log('='.repeat(70));
    results.forEach((r, i) => console.log(`${i + 1}. ${r.name}: ${r.status}`));

    console.log('\n浏览器保持打开60秒...');
    await page.waitForTimeout(60000);
    await browser.close();

    return results;

  } catch (error) {
    console.error('\n错误:', error.message);
    try {
      fs.writeFileSync(SESSION_FILE, JSON.stringify({
        cookies: await context.cookies(),
        timestamp: Date.now()
      }, null, 2));
    } catch (e) {}
    await browser.close();
    throw error;
  }
}

// 运行
const args = process.argv.slice(2);
let files = args.length > 0 ? args :
  fs.readdirSync(STRATEGIES_DIR)
    .filter(f => f.endsWith('.py') && !f.includes('test'))
    .map(f => path.join(STRATEGIES_DIR, f));

smartInjectStrategies(files).then(results => {
  console.log(`\n✓ 完成 ${results.filter(r => r.status === 'processed').length}/${results.length}`);
}).catch(err => {
  console.error('\n✗ 失败:', err.message);
  process.exit(1);
});
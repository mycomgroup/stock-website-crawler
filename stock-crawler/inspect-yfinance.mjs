// Quick test to inspect yfinance page structure
import { chromium } from 'playwright';

async function inspectPage() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  try {
    console.log('Loading page...');
    await page.goto('https://www.aidoczh.com/yfinance/reference/index.html', {
      waitUntil: 'domcontentloaded'
    });

    await page.waitForTimeout(3000);

    // Get all links in various selectors
    const linkStats = await page.evaluate(() => {
      const stats = {
        allLinks: [],
        selectorCounts: {},
        sidebarLinks: []
      };

      // Count all links on page
      const allLinks = document.querySelectorAll('a[href]');
      stats.allLinks = Array.from(allLinks).map(a => ({
        href: a.getAttribute('href'),
        text: a.textContent.trim().substring(0, 50)
      }));

      // Check various sidebar selectors
      const selectors = [
        '.wy-menu-vertical',
        '.wy-side-scroll',
        '.sidebar',
        'nav',
        '.bd-sidebar',
        '.toctree-wrapper',
        '.local-toc',
        '.wy-menu',
        '.nav.bd-links',
        '#bd-docs-nav'
      ];

      for (const selector of selectors) {
        const elements = document.querySelectorAll(selector);
        if (elements.length > 0) {
          const links = elements[0].querySelectorAll('a[href]');
          stats.selectorCounts[selector] = {
            elementCount: elements.length,
            linkCount: links.length,
            sampleHrefs: Array.from(links).slice(0, 5).map(a => a.getAttribute('href'))
          };
        }
      }

      // Get the actual HTML structure of the main nav
      const wyMenu = document.querySelector('.wy-menu-vertical');
      if (wyMenu) {
        stats.sidebarHTML = wyMenu.innerHTML.substring(0, 5000);
      }

      return stats;
    });

    console.log('\n=== Page Statistics ===');
    console.log(`Total links on page: ${linkStats.allLinks.length}`);

    // Show links containing yfinance (absolute or relative)
    console.log(`\nAll unique link hrefs (first 50):`);
    const uniqueHrefs = [...new Set(linkStats.allLinks.map(l => l.href).filter(h => h && !h.startsWith('#') && !h.startsWith('javascript:')))];
    uniqueHrefs.slice(0, 50).forEach(h => console.log(`  - ${h}`));
    console.log(`\nTotal unique external/relative links: ${uniqueHrefs.length}`);

    console.log('\n=== Selector Counts ===');
    for (const [selector, data] of Object.entries(linkStats.selectorCounts)) {
      console.log(`${selector}: ${data.elementCount} elements, ${data.linkCount} links`);
      if (data.sampleHrefs.length > 0) {
        console.log(`  Samples: ${data.sampleHrefs.slice(0, 3).join(', ')}`);
      }
    }

    if (linkStats.sidebarHTML) {
      console.log('\n=== Sidebar HTML Sample (first 2000 chars) ===');
      console.log(linkStats.sidebarHTML.substring(0, 2000));
    }

    // Check for nested lists in sidebar
    const nestedStructure = await page.evaluate(() => {
      const result = {
        listStructure: '',
        nestedListCount: 0,
        collapsedItems: []
      };

      // Check for nested ul/ol
      const nestedUls = document.querySelectorAll('ul ul, ol ol');
      result.nestedListCount = nestedUls.length;

      // Check for collapsed/hidden items
      const hiddenItems = document.querySelectorAll('[style*="display: none"], .hidden, .collapsed');
      result.collapsedItems = Array.from(hiddenItems).map(item =>
        item.tagName + (item.className ? '.' + item.className.split(' ').join('.') : '')
      ).slice(0, 20);

      // Get the toctree structure
      const toctree = document.querySelector('.toctree-wrapper, .wy-menu-vertical');
      if (toctree) {
        // Count list items at each level
        const levels = {};
        for (let i = 1; i <= 5; i++) {
          const items = toctree.querySelectorAll(`li.toctree-l${i}, .wy-menu-vertical li.current li`);
          if (items.length > 0) {
            levels[i] = items.length;
          }
        }
        result.listStructure = JSON.stringify(levels);
      }

      return result;
    });

    console.log('\n=== Nested Structure ===');
    console.log(`Nested lists found: ${nestedStructure.nestedListCount}`);
    console.log(`List levels: ${nestedStructure.listStructure}`);
    console.log(`Collapsed/hidden items: ${nestedStructure.collapsedItems.length}`);
    if (nestedStructure.collapsedItems.length > 0) {
      console.log('Sample hidden items:', nestedStructure.collapsedItems.slice(0, 10));
    }

  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    await browser.close();
  }
}

inspectPage();
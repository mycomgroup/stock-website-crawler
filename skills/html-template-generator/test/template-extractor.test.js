import { describe, it } from 'node:test';
import assert from 'node:assert';
import { TemplateExtractor } from '../lib/template-extractor.js';

describe('TemplateExtractor', () => {
  const html = `
    <html>
      <body>
        <main>
          <h1>Company A</h1>
          <section>
            <h2>Overview</h2>
            <p>Company A is a technology company with strong fundamentals.</p>
          </section>
          <section>
            <h2>Financials</h2>
            <table>
              <thead><tr><th>Year</th><th>Revenue</th></tr></thead>
              <tbody><tr><td>2024</td><td>100</td></tr></tbody>
            </table>
          </section>
          <ul><li>Listed</li><li>Profitable</li></ul>
        </main>
      </body>
    </html>
  `;

  const template = {
    templateName: 'company-detail',
    xpaths: {
      title: '//h1/text()',
      sections: {
        xpath: '//main/section',
        extract: {
          heading: './/h2/text()',
          description: './/p/text()',
          table: {
            xpath: './/table',
            headers: './/thead/tr/th',
            rows: './/tbody/tr'
          },
          list: {
            xpath: './/ul',
            items: './/li/text()'
          }
        }
      },
      mainContent: '//main'
    }
  };

  it('extracts useful content and confidence', () => {
    const extractor = new TemplateExtractor();
    const result = extractor.extract(html, template, { url: 'https://example.com/company-a' });

    assert.equal(result.title, 'Company A');
    assert.equal(result.sections.length, 2);
    assert.ok(result.paragraphs.length >= 1);
    assert.equal(result.tables.length, 1);
    assert.equal(result.needsHumanReview, false);
    assert.ok(result.confidence.score >= 0.7);
  });

  it('supports manual override', () => {
    const extractor = new TemplateExtractor();
    const result = extractor.extract(html, {
      ...template,
      xpaths: { ...template.xpaths, title: '//h1[@class="missing"]/text()' },
      manualOverrides: { title: '//h1/text()' }
    });

    assert.equal(result.title, 'Company A');
  });
});

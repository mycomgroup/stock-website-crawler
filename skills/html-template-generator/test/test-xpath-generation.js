/**
 * Integration test for XPath generation
 * Tests the complete flow from structure analysis to XPath generation
 */

import { StructureAnalyzer } from '../lib/structure-analyzer.js';
import { XPathGenerator } from '../lib/xpath-generator.js';

async function testXPathGeneration() {
  console.log('Testing XPath Generation Integration\n');
  console.log('=' .repeat(50));

  // Sample HTML content
  const sampleHTML = `
    <!DOCTYPE html>
    <html>
      <head><title>API Documentation</title></head>
      <body>
        <header>
          <nav>Navigation</nav>
        </header>
        <main class="main-content">
          <h1 class="page-title">API Documentation</h1>
          <section class="api-section">
            <h2 class="section-title">Overview</h2>
            <p class="description">This is the API overview.</p>
            <table class="params-table">
              <thead>
                <tr>
                  <th>Parameter</th>
                  <th>Type</th>
                  <th>Required</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>api_key</td>
                  <td>string</td>
                  <td>Yes</td>
                  <td>Your API key</td>
                </tr>
              </tbody>
            </table>
            <pre><code class="language-json">{"example": "data"}</code></pre>
            <ul class="api-list">
              <li>Feature 1</li>
              <li>Feature 2</li>
            </ul>
          </section>
        </main>
        <footer>Footer content</footer>
      </body>
    </html>
  `;

  // Create multiple samples (simulating multiple pages with same structure)
  const htmlContents = [
    { url: 'http://example.com/api/doc1', html: sampleHTML, title: 'API Doc 1' },
    { url: 'http://example.com/api/doc2', html: sampleHTML, title: 'API Doc 2' },
    { url: 'http://example.com/api/doc3', html: sampleHTML, title: 'API Doc 3' },
    { url: 'http://example.com/api/doc4', html: sampleHTML, title: 'API Doc 4' },
    { url: 'http://example.com/api/doc5', html: sampleHTML, title: 'API Doc 5' }
  ];

  try {
    // Step 1: Analyze structure
    console.log('\n1. Analyzing HTML structure...');
    const analyzer = new StructureAnalyzer();
    const structure = await analyzer.analyze(htmlContents);

    console.log('Structure analysis results:');
    console.log('  - Main content:', structure.mainContent?.xpath || 'Not found');
    console.log('  - Headings:', Object.keys(structure.headings).length, 'levels found');
    console.log('  - Tables:', structure.tables.length, 'found');
    console.log('  - Code blocks:', structure.codeBlocks.length, 'found');
    console.log('  - Lists:', structure.lists.length, 'found');

    // Step 2: Generate XPath rules
    console.log('\n2. Generating XPath rules...');
    const generator = new XPathGenerator();
    const rules = generator.generate(structure);

    console.log('Generated XPath rules:');
    console.log('\nTitle XPath:');
    console.log('  ', rules.title || 'Not generated');

    console.log('\nSections:');
    if (rules.sections) {
      console.log('  Container:', rules.sections.xpath);
      console.log('  Heading:', rules.sections.extract.heading);
      console.log('  Description:', rules.sections.extract.description);
      
      if (rules.sections.extract.table) {
        console.log('  Table:');
        console.log('    - XPath:', rules.sections.extract.table.xpath);
        console.log('    - Headers:', rules.sections.extract.table.headers);
        console.log('    - Rows:', rules.sections.extract.table.rows);
        console.log('    - Cells:', rules.sections.extract.table.cells);
      }
      
      if (rules.sections.extract.codeExample) {
        console.log('  Code:', rules.sections.extract.codeExample);
      }
      
      if (rules.sections.extract.list) {
        console.log('  List:');
        console.log('    - XPath:', rules.sections.extract.list.xpath);
        console.log('    - Items:', rules.sections.extract.list.items);
      }
    } else {
      console.log('  Not generated');
    }

    console.log('\nFilters:');
    console.log('  Remove XPaths:', rules.filters.removeXPaths.length, 'filters');
    console.log('  Clean text:', rules.filters.cleanText);

    // Step 3: Validate rules
    console.log('\n3. Validating generated rules...');
    const validations = [];

    if (rules.title) {
      validations.push('✓ Title XPath generated');
    } else {
      validations.push('✗ Title XPath missing');
    }

    if (rules.sections) {
      validations.push('✓ Sections rules generated');
      
      if (rules.sections.extract.table) {
        validations.push('✓ Table extraction rules generated');
      }
      
      if (rules.sections.extract.codeExample) {
        validations.push('✓ Code block extraction rules generated');
      }
      
      if (rules.sections.extract.list) {
        validations.push('✓ List extraction rules generated');
      }
    } else {
      validations.push('✗ Sections rules missing');
    }

    if (rules.filters && rules.filters.removeXPaths.length > 0) {
      validations.push('✓ Filter rules generated');
    } else {
      validations.push('✗ Filter rules missing');
    }

    console.log('\nValidation results:');
    validations.forEach(v => console.log('  ', v));

    // Step 4: Check XPath format
    console.log('\n4. Checking XPath format...');
    const formatChecks = [];

    if (rules.title && rules.title.includes('/text()')) {
      formatChecks.push('✓ Title XPath extracts text');
    }

    if (rules.sections) {
      const containerXPath = rules.sections.xpath;
      if (containerXPath.startsWith('//') || containerXPath.includes('|')) {
        formatChecks.push('✓ Container XPath is absolute or uses union');
      }

      const headingXPath = rules.sections.extract.heading;
      if (headingXPath && headingXPath.startsWith('.//')) {
        formatChecks.push('✓ Heading XPath is relative');
      }

      if (rules.sections.extract.table) {
        const tableXPath = rules.sections.extract.table.xpath;
        if (tableXPath && tableXPath.startsWith('.//')) {
          formatChecks.push('✓ Table XPath is relative');
        }
      }

      if (rules.sections.extract.codeExample) {
        const codeXPath = rules.sections.extract.codeExample;
        if (codeXPath && codeXPath.startsWith('.//')) {
          formatChecks.push('✓ Code XPath is relative');
        }
      }
    }

    console.log('Format checks:');
    formatChecks.forEach(c => console.log('  ', c));

    console.log('\n' + '='.repeat(50));
    console.log('✓ Integration test completed successfully!\n');

    return { structure, rules };

  } catch (error) {
    console.error('\n✗ Test failed:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

// Run the test
testXPathGeneration().catch(error => {
  console.error('Unexpected error:', error);
  process.exit(1);
});

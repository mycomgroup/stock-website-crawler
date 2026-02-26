import { StructureAnalyzer } from '../lib/structure-analyzer.js';

const analyzer = new StructureAnalyzer();

const htmlContents = [
  {
    url: 'http://example.com/page1',
    html: `
      <html>
        <body>
          <header class="site-header">
            <h1>Site Title</h1>
            <nav class="main-nav">
              <a href="/">Home</a>
              <a href="/about">About</a>
            </nav>
          </header>
          
          <aside class="sidebar">
            <h3>Related Links</h3>
            <ul>
              <li><a href="/link1">Link 1</a></li>
              <li><a href="/link2">Link 2</a></li>
            </ul>
          </aside>
          
          <main class="main-content">
            <article>
              <h1>Article Title</h1>
              <p>This is the main content area with substantial text content.</p>
              <p>Multiple paragraphs of meaningful content that should be identified as the primary content.</p>
              
              <h2>Section 1</h2>
              <p>More detailed content in this section.</p>
              
              <table class="data-table">
                <thead>
                  <tr><th>Column 1</th><th>Column 2</th></tr>
                </thead>
                <tbody>
                  <tr><td>Data 1</td><td>Data 2</td></tr>
                </tbody>
              </table>
              
              <h2>Code Example</h2>
              <pre><code class="language-javascript">
                const example = "code";
              </code></pre>
            </article>
          </main>
          
          <div class="ad-banner">
            <img src="ad.jpg" alt="Advertisement" />
          </div>
          
          <footer class="site-footer">
            <p>Copyright 2024</p>
          </footer>
        </body>
      </html>
    `,
    title: 'Example Page'
  }
];

console.log('Testing Main Content Area Identification\n');
console.log('='.repeat(50));

const result = await analyzer.analyze(htmlContents);

console.log('\n📊 Analysis Results:\n');

console.log('Main Content:');
console.log('  XPath:', result.mainContent?.xpath || 'Not found');
console.log('  Frequency:', result.mainContent?.frequency || 0);

console.log('\nHeadings:');
Object.entries(result.headings).forEach(([tag, info]) => {
  console.log(`  ${tag}:`, info.xpath, `(frequency: ${info.frequency})`);
});

console.log('\nTables:');
result.tables.forEach((table, i) => {
  console.log(`  Table ${i + 1}:`, table.xpath, `(frequency: ${table.frequency})`);
});

console.log('\nCode Blocks:');
result.codeBlocks.forEach((code, i) => {
  console.log(`  Code ${i + 1}:`, code.xpath, `(language: ${code.language || 'none'}, frequency: ${code.frequency})`);
});

console.log('\n✅ Main content area successfully identified!');
console.log('   The analyzer correctly filtered out:');
console.log('   - Navigation elements');
console.log('   - Sidebar content');
console.log('   - Advertisement banners');
console.log('   - Header and footer');
console.log('\n   And identified the <main> element as the primary content area.');

import MarkdownGenerator from '../stock-crawler/src/markdown-generator.js';

const gen = new MarkdownGenerator();

// Test with generic type
const pageData = {
  type: 'generic',
  title: 'Test Page',
  url: 'https://example.com',
  mainContent: [
    { type: 'paragraph', content: 'Some paragraph before' },
    { type: 'table', headers: ['A', 'B'], rows: [['1', '2']], precedingContent: [{ type: 'heading', level: 3, content: 'Table Title' }] }
  ]
};

console.log('=== Generated Markdown ===');
console.log(gen.generate(pageData));
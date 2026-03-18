import MarkdownGenerator from './src/parsers/markdown-generator.js';

const generator = new MarkdownGenerator();
const sampleData = {
  id: 'test-id',
  type: 'api',
  title: 'Test Title',
  url: 'http://test.com',
  description: 'Test description',
  source: 'test',
  tags: ['t1', 't2'],
  crawl_time: '2023-01-01',
  html: '<p>ignore</p>',
  content: 'ignore content',
  markdown: 'ignore markdown',
  api: {
    endpoint: '/test',
    method: 'GET'
  },
  nested: {
    arr: [{a: 1}, {b: 2}],
    obj: { c: 3 }
  }
};

const output = generator.generate(sampleData);
console.log(output);

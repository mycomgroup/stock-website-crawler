import { classifyPattern } from '../src/template-crawl-pipeline.js';

describe('TemplateCrawlPipeline helpers', () => {
  test('classifies api-like pattern', () => {
    const category = classifyPattern({
      name: 'open-api-doc',
      pathTemplate: '/open/api/doc/{id}',
      description: 'API 文档'
    });

    expect(category).toBe('api');
  });

  test('falls back to general category', () => {
    const category = classifyPattern({
      name: 'unknown-pattern',
      pathTemplate: '/x/y/z',
      description: 'misc'
    });

    expect(category).toBe('general');
  });
});

import PageClassifier from '../src/parsers/page-classifier.js';

describe('PageClassifier', () => {
  test('should classify api doc by url pattern', async () => {
    const classifier = new PageClassifier();

    const result = await classifier.classify({ evaluate: async () => ({}) }, 'https://example.com/api/doc/stock');

    expect(result.type).toBe('api_doc_page');
    expect(result.confidence).toBeGreaterThan(0.9);
  });

  test('should classify article by content signals', () => {
    const classifier = new PageClassifier();

    const result = classifier.classifyByRules({
      paragraphCount: 8,
      avgParagraphLength: 120,
      linkDensity: 0.12,
      tableCount: 0,
      maxTableRows: 0,
      repeatedListBlocks: 2,
      listItems: 6,
      paginationDetected: false,
      navLinks: 2,
      hasTreeStyle: false,
      detailHint: true
    });

    expect(result.type).toBe('article_page');
  });

  test('should classify table content page by table dominance', () => {
    const classifier = new PageClassifier();

    const result = classifier.classifyByRules({
      paragraphCount: 2,
      avgParagraphLength: 20,
      linkDensity: 0.05,
      tableCount: 1,
      maxTableRows: 18,
      repeatedListBlocks: 0,
      listItems: 0,
      paginationDetected: false,
      navLinks: 1,
      hasTreeStyle: false,
      detailHint: false
    });

    expect(result.type).toBe('table_content_page');
  });
});

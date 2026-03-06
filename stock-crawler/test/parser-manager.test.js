import ParserManager from '../src/parsers/parser-manager.js';

describe('ParserManager', () => {
  test('should use GenericParser when parserMode is core-content but no precise classification', () => {
    const manager = new ParserManager();

    const parser = manager.selectParser('https://example.com/article/1', {
      parserMode: 'core-content'
    });

    expect(parser.constructor.name).toBe('GenericParser');
  });

  test('should use GenericParser when url matches api doc but no precise classification', () => {
    const manager = new ParserManager();

    const parser = manager.selectParser('https://example.com/api/doc/test', {});

    expect(parser.constructor.name).toBe('GenericParser');
  });

  test('should select list parser based on high-confidence classification', () => {
    const manager = new ParserManager();

    const parser = manager.selectParser('https://example.com/unknown', {
      classification: { type: 'list_page', confidence: 0.88 }
    });

    expect(parser.constructor.name).toBe('ListParser');
  });

  test('should select directory parser based on high-confidence classification', () => {
    const manager = new ParserManager();

    const parser = manager.selectParser('https://example.com/unknown', {
      classification: { type: 'directory_page', confidence: 0.92 }
    });

    expect(parser.constructor.name).toBe('DirectoryParser');
  });

  test('should use parser override when url matches configured pattern', () => {
    const manager = new ParserManager();

    const parser = manager.selectParser('https://example.com/special/endpoint', {
      classification: { type: 'list_page', confidence: 0.95 },
      parserUrlPatternOverrides: [
        { pattern: '.*/special/.*', parser: 'DirectoryParser' }
      ]
    });

    expect(parser.constructor.name).toBe('DirectoryParser');
  });

  test('should fallback to GenericParser when classification confidence is low', () => {
    const manager = new ParserManager();

    const parser = manager.selectParser('https://example.com/list/page=1', {
      classification: { type: 'list_page', confidence: 0.3 }
    });

    expect(parser.constructor.name).toBe('GenericParser');
  });

  test('parse should skip classification when parser override matches', async () => {
    const manager = new ParserManager();
    let classifyCallCount = 0;
    manager.classifier.classify = async () => {
      classifyCallCount += 1;
      return { type: 'api_doc_page', confidence: 0.99, reasons: ['mock'], features: {} };
    };

    manager.parsers = [{
      constructor: { name: 'ApiDocParser' },
      matches: () => false,
      parse: async () => ({ type: 'api-doc', title: 'forced' }),
      getPriority: () => 100
    }, {
      constructor: { name: 'GenericParser' },
      matches: () => true,
      parse: async () => ({ type: 'generic', title: 'fallback' }),
      getPriority: () => 0
    }];

    const result = await manager.parse({}, 'https://example.com/open/api/doc/1', {
      parserUrlPatternOverrides: [{ pattern: '.*/open/api/doc/.*', parser: 'ApiDocParser' }]
    });

    expect(classifyCallCount).toBe(0);
    expect(result.type).toBe('api-doc');
    expect(result.classification).toBeNull();
  });

  test('parse should attach classification metadata to output', async () => {
    const manager = new ParserManager();
    manager.classifier.classify = async () => ({
      type: 'generic_page',
      confidence: 0.4,
      reasons: ['test'],
      features: {}
    });

    manager.parsers = [{
      constructor: { name: 'GenericParser' },
      matches: () => true,
      parse: async () => ({ type: 'generic', title: 'mock' }),
      getPriority: () => 0
    }];

    const data = await manager.parse({}, 'https://example.com/test', {});

    expect(data.type).toBe('generic');
    expect(data.classification).toEqual({
      type: 'generic_page',
      confidence: 0.4,
      reasons: ['test'],
      features: {}
    });
  });
});

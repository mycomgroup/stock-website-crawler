import ParserManager from '../src/parsers/parser-manager.js';

describe('ParserManager', () => {
  test('should select core content parser when parserMode is core-content', () => {
    const manager = new ParserManager();

    const parser = manager.selectParser('https://example.com/article/1', {
      parserMode: 'core-content'
    });

    expect(parser.constructor.name).toBe('CoreContentParser');
  });

  test('should still use api doc parser when url matches api doc and no core-content mode', () => {
    const manager = new ParserManager();

    const parser = manager.selectParser('https://example.com/api/doc/test', {});

    expect(parser.constructor.name).toBe('ApiDocParser');
  });

  test('should select list parser based on classification', () => {
    const manager = new ParserManager();

    const parser = manager.selectParser('https://example.com/unknown', {
      classification: { type: 'list_page' }
    });

    expect(parser.constructor.name).toBe('ListParser');
  });

  test('should select directory parser based on classification', () => {
    const manager = new ParserManager();

    const parser = manager.selectParser('https://example.com/unknown', {
      classification: { type: 'directory_page' }
    });

    expect(parser.constructor.name).toBe('DirectoryParser');
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

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
});

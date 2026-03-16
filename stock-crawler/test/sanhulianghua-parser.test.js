import SanhulianghuaParser from '../src/parsers/sanhulianghua-parser.js';

describe('SanhulianghuaParser', () => {
  let parser;

  beforeEach(() => {
    parser = new SanhulianghuaParser();
  });

  test('matches should only match sanhulianghua index.php docs urls', () => {
    expect(parser.matches('http://www.sanhulianghua.com/index.php?do=page_base_hsa_gupiao')).toBe(true);
    expect(parser.matches('https://www.sanhulianghua.com/index.php?do=page_real_hsa_gegumin')).toBe(true);
    expect(parser.matches('https://example.com/index.php?do=page_base_hsa_gupiao')).toBe(false);
  });

  test('generateFilename should strip page_ prefix from do param', () => {
    expect(parser.generateFilename('http://www.sanhulianghua.com/index.php?do=page_base_hsa_gupiao')).toBe('base_hsa_gupiao');
    expect(parser.generateFilename('http://www.sanhulianghua.com/index.php?do=page_real_hsa_gegumin')).toBe('real_hsa_gegumin');
  });

  test('parse should return fallback result when evaluate throws', async () => {
    const mockPage = {
      waitForLoadState: async () => {},
      waitForSelector: async () => {},
      waitForTimeout: async () => {},
      evaluate: async () => {
        throw new Error('eval boom');
      }
    };

    const result = await parser.parse(mockPage, 'http://www.sanhulianghua.com/index.php?do=page_base_hsa_gupiao');

    expect(result.type).toBe('sanhulianghua-api');
    expect(result.parameters).toEqual([]);
    expect(result.responses).toEqual([]);
    expect(result.suggestedFilename).toBe('base_hsa_gupiao');
  });
});

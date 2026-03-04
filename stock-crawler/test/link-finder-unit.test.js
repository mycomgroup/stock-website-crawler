import { jest } from '@jest/globals';
import LinkFinder from '../src/link-finder.js';

describe('LinkFinder unit', () => {
  let finder;

  beforeEach(() => {
    finder = new LinkFinder();
  });

  test('getDefaultPrioritizedPatterns returns api-key rule', () => {
    const patterns = finder.getDefaultPrioritizedPatterns();
    expect(patterns).toEqual([
      expect.objectContaining({
        selector: 'a[href*="api-key="]',
        requiredQueryParams: ['api-key'],
        pathIncludes: ['/open/api/doc']
      })
    ]);
  });

  test('extractLinks normalizes and filters links returned by page', async () => {
    const page = {
      url: () => 'https://example.com/docs/index.html',
      evaluate: jest.fn(async () => [
        '/open/api/doc?api-key=abc',
        'https://example.com/ignore?api-key=abc',
        '/open/api/doc?api-key=abc',
        'https://example.com/open/api/doc?api-key=undefined'
      ])
    };

    const links = await finder.extractLinks(page, {
      include: ['open/api/doc'],
      exclude: ['ignore']
    });

    expect(links).toEqual(['https://example.com/open/api/doc?api-key=abc']);
    expect(page.evaluate).toHaveBeenCalledTimes(1);
  });

  test('extractLinks returns empty array when evaluate fails', async () => {
    const page = {
      url: () => 'https://example.com',
      evaluate: async () => {
        throw new Error('evaluate failed');
      }
    };

    await expect(finder.extractLinks(page, { include: [] })).resolves.toEqual([]);
  });

  test('expandCollapsibles continues when evaluate fails', async () => {
    const page = {
      evaluate: jest.fn()
        .mockRejectedValueOnce(new Error('cannot click')),
      waitForTimeout: jest.fn()
    };

    const warnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {});

    await finder.expandCollapsibles(page);

    expect(warnSpy).toHaveBeenCalled();
    expect(page.waitForTimeout).not.toHaveBeenCalled();

    warnSpy.mockRestore();
  });
});

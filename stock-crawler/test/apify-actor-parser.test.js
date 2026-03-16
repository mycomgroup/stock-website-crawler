import ApifyActorParser from '../src/parsers/apify-actor-parser.js';

describe('ApifyActorParser', () => {
  test('should match apify and docs.apify domains', () => {
    const parser = new ApifyActorParser();
    expect(parser.matches('https://apify.com/scrapapi/google-finance-scraper')).toBe(true);
    expect(parser.matches('https://docs.apify.com/api/v2')).toBe(true);
    expect(parser.matches('https://example.com/docs')).toBe(false);
  });

  test('should provide stable filename and priority', () => {
    const parser = new ApifyActorParser();
    expect(parser.generateFilename('https://apify.com/scrapapi/google-finance-scraper')).toBe(
      'apify_com_scrapapi_google-finance-scraper'
    );
    expect(parser.getPriority()).toBe(95);
  });
});

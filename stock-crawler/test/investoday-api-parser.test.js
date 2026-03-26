import InvestodayApiParser from '../src/parsers/investoday-api-parser.js';

describe('InvestodayApiParser', () => {
  let parser;

  beforeEach(() => {
    parser = new InvestodayApiParser();
  });

  test('should match std and data-api investoday hosts', () => {
    expect(parser.matches('https://std.investoday.net/apidocs/ai-native-financial-data')).toBe(true);
    expect(parser.matches('https://data-api.investoday.net/docs')).toBe(true);
    expect(parser.matches('https://example.com/apidocs')).toBe(false);
  });

  test('should have higher priority than GenericParser', () => {
    expect(parser.getPriority()).toBeGreaterThan(0);
  });
});

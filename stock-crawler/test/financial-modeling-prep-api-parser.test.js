import { jest } from '@jest/globals';
import FinancialModelingPrepApiParser from '../src/parsers/financial-modeling-prep-api-parser.js';

describe('FinancialModelingPrepApiParser', () => {
  let parser;

  beforeEach(() => {
    parser = new FinancialModelingPrepApiParser();
  });

  test('matches FMP docs URLs', () => {
    expect(parser.matches('https://site.financialmodelingprep.com/developer/docs')).toBe(true);
    expect(parser.matches('https://site.financialmodelingprep.com/developer/docs/stable/profile-symbol')).toBe(true);
    expect(parser.matches('https://financialmodelingprep.com/developer/docs')).toBe(false);
  });

  test('convertToMarkdown should keep key fields and output valid table/code blocks', () => {
    const markdown = parser.convertToMarkdown({
      title: 'Company Profile API',
      description: 'Get a company profile by ticker.',
      responseExample: '{"symbol":"AAPL"}',
      sections: [
        {
          type: 'subpage-section',
          title: 'Endpoint',
          content: 'Returns profile data.',
          method: 'GET',
          endpoint: 'https://financialmodelingprep.com/stable/profile?symbol=AAPL',
          tables: [
            {
              headers: ['Parameter', 'Type', 'Required'],
              rows: [['symbol', 'string', 'Yes']]
            }
          ],
          codeBlocks: ['curl "https://financialmodelingprep.com/stable/profile?symbol=AAPL"']
        }
      ]
    });

    expect(markdown).toContain('# Company Profile API');
    expect(markdown).toContain('```json');
    expect(markdown).toContain('GET https://financialmodelingprep.com/stable/profile?symbol=AAPL');
    expect(markdown).toContain('| Parameter | Type | Required |');
    expect(markdown).toContain('| symbol | string | Yes |');
    expect(markdown).toContain('curl "https://financialmodelingprep.com/stable/profile?symbol=AAPL"');
  });

  test('parse should run wait and expand before extracting data', async () => {
    const page = {
      waitForLoadState: jest.fn().mockResolvedValue(undefined),
      waitForSelector: jest.fn().mockResolvedValue(undefined),
      waitForTimeout: jest.fn().mockResolvedValue(undefined),
      evaluate: jest
        .fn()
        .mockResolvedValueOnce(2)
        .mockResolvedValueOnce({
          title: 'Test API',
          description: 'Desc',
          sections: [],
          responseExample: '',
          isSubPage: true
        })
    };

    const result = await parser.parse(page, 'https://site.financialmodelingprep.com/developer/docs/test');

    expect(result.type).toBe('financial-modeling-prep-api');
    expect(page.waitForSelector).toHaveBeenCalled();
    expect(page.evaluate).toHaveBeenCalledTimes(2);
  });
});

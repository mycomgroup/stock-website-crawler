import { jest } from '@jest/globals';
import CoreContentParser from '../src/parsers/core-content-parser.js';
import GenericParser from '../src/parsers/generic-parser.js';

describe('CoreContentParser', () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('should keep core-content result for article-like pages', async () => {
    const parser = new CoreContentParser();

    jest.spyOn(parser, 'extractTitle').mockResolvedValue('Article Title');
    jest.spyOn(parser, 'extractCoreContent').mockResolvedValue({
      blocks: [
        { type: 'heading', level: 2, content: '标题' },
        { type: 'paragraph', content: '这是一段很长的正文内容。'.repeat(30) }
      ],
      meta: {
        paragraphCount: 4,
        headingCount: 2,
        listItemCount: 2,
        tableCount: 0,
        formCount: 0,
        totalParagraphChars: 1200,
        averageParagraphChars: 300,
        totalTextChars: 1500,
        linkDensity: 0.05,
        bestScore: 300
      }
    });

    const genericSpy = jest.spyOn(GenericParser.prototype, 'parse');

    const result = await parser.parse({}, 'https://example.com/article', {
      parserMode: 'core-content'
    });

    expect(result.type).toBe('core-content');
    expect(result.mainContent.length).toBe(2);
    expect(genericSpy).not.toHaveBeenCalled();
  });

  test('should fallback to generic parser for non-article pages', async () => {
    const parser = new CoreContentParser();

    jest.spyOn(parser, 'extractTitle').mockResolvedValue('List Page');
    jest.spyOn(parser, 'extractCoreContent').mockResolvedValue({
      blocks: [{ type: 'paragraph', content: '短内容' }],
      meta: {
        paragraphCount: 1,
        headingCount: 8,
        listItemCount: 40,
        tableCount: 3,
        formCount: 1,
        totalParagraphChars: 40,
        averageParagraphChars: 40,
        totalTextChars: 900,
        linkDensity: 0.7,
        bestScore: -50
      }
    });

    jest.spyOn(GenericParser.prototype, 'parse').mockResolvedValue({
      type: 'generic',
      title: 'List Page',
      url: 'https://example.com/list'
    });

    const result = await parser.parse({}, 'https://example.com/list', {
      parserMode: 'core-content'
    });

    expect(result.type).toBe('generic');
    expect(result.parserFallback).toBe('core-content->generic');
    expect(result.coreContentRejectedReason).toBe('paragraphs-too-few');
  });
});

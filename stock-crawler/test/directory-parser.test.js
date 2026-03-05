import { jest } from '@jest/globals';
import DirectoryParser from '../src/parsers/directory-parser.js';

describe('DirectoryParser', () => {
  let parser;

  beforeEach(() => {
    parser = new DirectoryParser();
  });

  test('matches 支持分类命中与URL规则命中', () => {
    expect(parser.matches('https://example.com/xxx', { classification: { type: 'directory_page' } })).toBe(true);
    expect(parser.matches('https://example.com/directory')).toBe(true);
    expect(parser.matches('https://example.com/index')).toBe(true);
    expect(parser.matches('https://example.com/guide/getting-started')).toBe(true);
    expect(parser.matches('https://example.com/catalog/list')).toBe(true);
  });

  test('matches 在非目录URL时返回 false', () => {
    expect(parser.matches('https://example.com/article/1')).toBe(false);
  });

  test('getPriority 返回 80', () => {
    expect(parser.getPriority()).toBe(80);
  });

  test('countNodes 应递归统计节点数', () => {
    const tree = [
      {
        name: 'A',
        url: '/a',
        children: [
          { name: 'A-1', url: '/a-1', children: [] },
          {
            name: 'A-2',
            url: '/a-2',
            children: [{ name: 'A-2-1', url: '/a-2-1', children: [] }]
          }
        ]
      },
      { name: 'B', url: '/b', children: [] }
    ];

    expect(parser.countNodes(tree)).toBe(5);
    expect(parser.countNodes()).toBe(0);
  });

  test('parse 应返回目录结构与 nodeCount', async () => {
    parser.extractTitle = jest.fn(async () => '目录页标题');

    const tree = [
      {
        name: '文档中心',
        url: '/docs',
        children: [{ name: 'API', url: '/docs/api', children: [] }]
      }
    ];

    const page = {
      evaluate: async () => tree
    };

    const result = await parser.parse(page, 'https://example.com/directory');

    expect(result).toEqual({
      type: 'directory-page',
      url: 'https://example.com/directory',
      title: '目录页标题',
      tree,
      directoryMeta: {
        nodeCount: 2
      }
    });
  });
});

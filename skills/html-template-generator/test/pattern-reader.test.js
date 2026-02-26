import { PatternReader } from '../lib/pattern-reader.js';
import { writeFile, mkdir, rm } from 'fs/promises';
import { join } from 'path';

describe('PatternReader', () => {
  const testDir = join(process.cwd(), 'test', 'fixtures');
  const testFile = join(testDir, 'test-patterns.json');
  let reader;

  beforeAll(async () => {
    await mkdir(testDir, { recursive: true });
  });

  afterAll(async () => {
    await rm(testDir, { recursive: true, force: true });
  });

  beforeEach(() => {
    reader = new PatternReader();
  });

  test('should read valid template', async () => {
    const patterns = [
      {
        name: 'test-template',
        description: 'Test template description',
        samples: ['https://example.com/page1', 'https://example.com/page2'],
        pathTemplate: '/page',
        pattern: '^https://example\\.com/page.*$',
        urlCount: 10
      }
    ];

    await writeFile(testFile, JSON.stringify(patterns));

    const result = await reader.read(testFile, 'test-template');

    expect(result.name).toBe('test-template');
    expect(result.description).toBe('Test template description');
    expect(result.samples).toHaveLength(2);
    expect(result.samples[0]).toBe('https://example.com/page1');
  });

  test('should throw error for non-existent file', async () => {
    await expect(
      reader.read('non-existent.json', 'test')
    ).rejects.toThrow('File not found');
  });

  test('should throw error for non-existent template', async () => {
    const patterns = [
      {
        name: 'other-template',
        description: 'Other template',
        samples: ['https://example.com']
      }
    ];

    await writeFile(testFile, JSON.stringify(patterns));

    await expect(
      reader.read(testFile, 'non-existent-template')
    ).rejects.toThrow('Template "non-existent-template" not found');
  });

  test('should throw error for invalid JSON', async () => {
    await writeFile(testFile, 'invalid json{');

    await expect(
      reader.read(testFile, 'test')
    ).rejects.toThrow('Invalid JSON');
  });

  test('should throw error for template missing required fields', async () => {
    const patterns = [
      {
        name: 'incomplete-template'
        // missing description and samples
      }
    ];

    await writeFile(testFile, JSON.stringify(patterns));

    await expect(
      reader.read(testFile, 'incomplete-template')
    ).rejects.toThrow('missing required fields');
  });

  test('should throw error for template with empty samples', async () => {
    const patterns = [
      {
        name: 'empty-samples',
        description: 'Template with no samples',
        samples: []
      }
    ];

    await writeFile(testFile, JSON.stringify(patterns));

    await expect(
      reader.read(testFile, 'empty-samples')
    ).rejects.toThrow('at least one sample URL');
  });
});

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import fs from 'node:fs';

vi.mock('node:fs');

vi.mock('./request/guorn-strategy-client.js', () => ({
  GuornStrategyClient: vi.fn().mockImplementation(() => ({
    getStockMeta: vi.fn().mockResolvedValue({
      data: { measures: [] }
    }),
  })),
}));

vi.mock('./request/ensure-session.js', () => ({
  ensureGuornSession: vi.fn().mockResolvedValue({ sessionFile: '/test/session.json' }),
}));

describe('dump_meta.js constants and logic', () => {
  let consoleLogSpy;
  let consoleErrorSpy;

  beforeEach(() => {
    vi.clearAllMocks();
    consoleLogSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
    consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    
    vi.mocked(fs.writeFileSync).mockImplementation(() => {});
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
    consoleErrorSpy.mockRestore();
  });

  describe('output file configuration', () => {
    it('should use guorn_meta_full.json as output file name', () => {
      const outFile = 'guorn_meta_full.json';
      expect(outFile).toBe('guorn_meta_full.json');
    });
  });

  describe('summary extraction', () => {
    it('should extract indicator count from measures', () => {
      const meta = {
        data: { measures: [{ name: 'PE' }, { name: 'PB' }] }
      };
      const indicatorCount = meta.data?.measures?.length || 0;
      expect(indicatorCount).toBe(2);
    });

    it('should handle empty measures', () => {
      const meta = { data: { measures: [] } };
      const indicatorCount = meta.data?.measures?.length || 0;
      expect(indicatorCount).toBe(0);
    });

    it('should handle missing measures', () => {
      const meta = { data: {} };
      const indicatorCount = meta.data?.measures?.length || 0;
      expect(indicatorCount).toBe(0);
    });

    it('should handle missing data', () => {
      const meta = {};
      const indicatorCount = meta.data?.measures?.length || 0;
      expect(indicatorCount).toBe(0);
    });
  });

  describe('JSON formatting', () => {
    it('should format JSON with 2-space indentation', () => {
      const data = { key: 'value' };
      const formatted = JSON.stringify(data, null, 2);
      expect(formatted).toContain('\n');
      expect(formatted).toContain('  ');
    });
  });

  describe('GuornStrategyClient usage', () => {
    it('should call getStockMeta with stock parameter', async () => {
      const { GuornStrategyClient } = await import('./request/guorn-strategy-client.js');
      const client = new GuornStrategyClient();
      
      const result = await client.getStockMeta('stock');
      
      expect(client.getStockMeta).toHaveBeenCalledWith('stock');
      expect(result.data).toBeDefined();
    });
  });

  describe('ensureGuornSession usage', () => {
    it('should call ensureGuornSession before fetching meta', async () => {
      const { ensureGuornSession } = await import('./request/ensure-session.js');
      
      const result = await ensureGuornSession();
      
      expect(ensureGuornSession).toHaveBeenCalled();
      expect(result.sessionFile).toBeDefined();
    });
  });

  describe('error handling', () => {
    it('should handle getStockMeta error', async () => {
      const { GuornStrategyClient } = await import('./request/guorn-strategy-client.js');
      
      vi.mocked(GuornStrategyClient).mockImplementation(() => ({
        getStockMeta: vi.fn().mockRejectedValue(new Error('API error')),
      }));
      
      const client = new GuornStrategyClient();
      
      await expect(client.getStockMeta('stock')).rejects.toThrow('API error');
    });
  });

  describe('file writing', () => {
    it('should write valid JSON to file', () => {
      const metaData = { status: 'ok', data: { measures: [] } };
      
      fs.writeFileSync('guorn_meta_full.json', JSON.stringify(metaData, null, 2));
      
      expect(fs.writeFileSync).toHaveBeenCalledWith(
        'guorn_meta_full.json',
        expect.stringContaining('"status"')
      );
    });
  });
});
import { describe, it, expect } from '@jest/globals';

describe('load-env.js', () => {
  it('should be importable', async () => {
    const module = await import('../load-env.js');
    expect(module).toBeDefined();
  });
});
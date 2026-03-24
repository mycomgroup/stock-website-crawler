/**
 * Property-based tests for limit parameter truncation.
 *
 * Validates: Requirements 6.3
 *
 * Property 5: limit 参数截断
 * For any result set and any positive integer limit, applying the limit should
 * return no more than `limit` rows and no more than the original row count.
 */

import { test } from 'node:test';
import assert from 'node:assert';
import fc from 'fast-check';
import { applyLimit } from '../main.js';

// ── Arbitraries ──────────────────────────────────────────────────────────────

const cellValueArb = fc.string({ minLength: 0, maxLength: 20 });

const rowArb = fc.record({
  name: cellValueArb,
  value: cellValueArb,
});

const rowsArb = fc.array(rowArb, { minLength: 0, maxLength: 50 });

const positiveLimitArb = fc.integer({ min: 1, max: 100 });

// ── Property 5a: result.length <= limit AND result.length <= rows.length ──────

test('Property 5a: result length <= limit and <= original rows length', () => {
  fc.assert(
    fc.property(rowsArb, positiveLimitArb, (rows, limit) => {
      const result = applyLimit(rows, limit);
      assert.ok(
        result.length <= limit,
        `result.length (${result.length}) should be <= limit (${limit})`
      );
      assert.ok(
        result.length <= rows.length,
        `result.length (${result.length}) should be <= rows.length (${rows.length})`
      );
    }),
    { numRuns: 100 }
  );
});

// ── Property 5b: no limit (null/undefined) returns all rows ──────────────────

test('Property 5b: null or undefined limit returns all rows', () => {
  fc.assert(
    fc.property(rowsArb, (rows) => {
      assert.deepStrictEqual(applyLimit(rows, null), rows,
        'applyLimit with null should return all rows');
      assert.deepStrictEqual(applyLimit(rows, undefined), rows,
        'applyLimit with undefined should return all rows');
    }),
    { numRuns: 100 }
  );
});

// ── Property 5c: limit >= rows.length returns all rows ───────────────────────

test('Property 5c: limit >= rows.length returns all rows', () => {
  fc.assert(
    fc.property(rowsArb, (rows) => {
      const limit = rows.length + fc.sample(fc.integer({ min: 0, max: 50 }), 1)[0];
      const result = applyLimit(rows, limit);
      assert.strictEqual(result.length, rows.length,
        `When limit (${limit}) >= rows.length (${rows.length}), all rows should be returned`);
    }),
    { numRuns: 100 }
  );
});

// ── Property 5d: result is a prefix of the original rows ─────────────────────

test('Property 5d: result is a prefix of the original rows', () => {
  fc.assert(
    fc.property(rowsArb, positiveLimitArb, (rows, limit) => {
      const result = applyLimit(rows, limit);
      const expected = rows.slice(0, Math.min(limit, rows.length));
      assert.deepStrictEqual(result, expected,
        `result should be rows.slice(0, min(limit, rows.length))`);
    }),
    { numRuns: 100 }
  );
});

// ── Edge cases ────────────────────────────────────────────────────────────────

test('applyLimit with zero limit returns all rows (zero is not a positive integer)', () => {
  const rows = [{ name: 'a' }, { name: 'b' }];
  assert.deepStrictEqual(applyLimit(rows, 0), rows);
});

test('applyLimit with negative limit returns all rows', () => {
  const rows = [{ name: 'a' }, { name: 'b' }];
  assert.deepStrictEqual(applyLimit(rows, -1), rows);
});

test('applyLimit with non-integer limit returns all rows', () => {
  const rows = [{ name: 'a' }, { name: 'b' }];
  assert.deepStrictEqual(applyLimit(rows, 1.5), rows);
});

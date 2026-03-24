/**
 * Property-based tests for pagination data merge integrity.
 *
 * Validates: Requirements 4.4
 *
 * Property 3: 分页数据合并完整性
 * For any multi-page result table, the merged row count should equal the sum
 * of all page row counts, and no duplicate rows should be introduced by the merge.
 */

import { test } from 'node:test';
import assert from 'node:assert';
import fc from 'fast-check';
import { mergePages } from '../main.js';

// ── Arbitraries ──────────────────────────────────────────────────────────────

/** Non-empty string for cell values */
const cellValueArb = fc.string({ minLength: 1, maxLength: 20 });

/** Generates a single table row object with string values */
const rowArb = fc.record({
  name: cellValueArb,
  value: cellValueArb,
  extra: cellValueArb,
});

/** Generates a single page (array of rows) */
const pageArb = fc.array(rowArb, { minLength: 0, maxLength: 20 });

/** Generates multiple pages */
const pagesArb = fc.array(pageArb, { minLength: 0, maxLength: 10 });

/** Generates a row with a unique numeric id field */
const rowWithIdArb = (id) =>
  fc.record({
    id: fc.constant(String(id)),
    name: cellValueArb,
    value: cellValueArb,
  });

// ── Property 3a: Row count equals sum of all page row counts ─────────────────

test('Property 3a: merged row count equals sum of all page row counts', () => {
  fc.assert(
    fc.property(pagesArb, (pages) => {
      const merged = mergePages(pages);
      const expectedCount = pages.reduce((sum, page) => sum + page.length, 0);
      assert.strictEqual(
        merged.length,
        expectedCount,
        `Expected merged length ${expectedCount} but got ${merged.length} for ${pages.length} pages`
      );
    }),
    { numRuns: 100 }
  );
});

// ── Property 3b: Empty pages array returns empty result ──────────────────────

test('Property 3b: empty pages array returns empty result', () => {
  const result = mergePages([]);
  assert.deepStrictEqual(result, [], 'mergePages([]) should return []');
});

// ── Property 3c: Single page returns same rows ───────────────────────────────

test('Property 3c: single page returns same rows', () => {
  fc.assert(
    fc.property(pageArb, (page) => {
      const result = mergePages([page]);
      assert.deepStrictEqual(
        result,
        page,
        `mergePages([page]) should equal page for page of length ${page.length}`
      );
    }),
    { numRuns: 100 }
  );
});

// ── Property 3d: No duplicate rows when input pages have unique rows ──────────

test('Property 3d: no duplicate ids when input pages have unique id rows', () => {
  fc.assert(
    fc.property(
      // Generate pages where each row has a globally unique id
      fc.array(fc.integer({ min: 1, max: 5 }), { minLength: 0, maxLength: 8 }),
      (pageSizes) => {
        // Build pages with globally unique ids across all pages
        let idCounter = 0;
        const pages = pageSizes.map(size => {
          const page = [];
          for (let i = 0; i < size; i++) {
            page.push({ id: String(idCounter++), name: `row-${idCounter}`, value: `val-${idCounter}` });
          }
          return page;
        });

        const merged = mergePages(pages);
        const ids = merged.map(row => row.id);
        const uniqueIds = new Set(ids);

        assert.strictEqual(
          uniqueIds.size,
          ids.length,
          `Expected no duplicate ids after merge, but found duplicates. Total rows: ${ids.length}, unique: ${uniqueIds.size}`
        );
      }
    ),
    { numRuns: 100 }
  );
});

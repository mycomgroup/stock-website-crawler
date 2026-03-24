/**
 * Property-based tests for LLM-converted ScreenerQuery field validity.
 *
 * Validates: Requirements 2.1, 2.2
 *
 * Property 2: LLM 转换字段合法性
 * For any ScreenerQuery, every filter's `field` value must be found in the
 * catalog's `displayName` list. validateScreenerQuery should correctly
 * identify valid and invalid queries.
 */

import { test } from 'node:test';
import assert from 'node:assert';
import fc from 'fast-check';
import { validateScreenerQuery } from '../main.js';

// ── Arbitraries ──────────────────────────────────────────────────────────────

/** Non-empty string with at least one visible character */
const nonEmptyString = fc.string({ minLength: 1, maxLength: 30 }).filter(s => s.trim().length > 0);

/** Generates a random catalog entry with a displayName */
const catalogEntryArb = fc.record({
  name: nonEmptyString,
  displayName: nonEmptyString,
  category: nonEmptyString,
  unit: nonEmptyString,
  operators: fc.array(nonEmptyString, { minLength: 1, maxLength: 3 }),
});

/** Generates a non-empty catalog array */
const catalogArb = fc.array(catalogEntryArb, { minLength: 1, maxLength: 10 });

/** Generates a valid operator string */
const operatorArb = fc.constantFrom('大于', '小于', '介于');

/** Generates a filter whose field is picked from the catalog's displayNames */
const validFilterArb = (catalog) =>
  fc.record({
    field: fc.constantFrom(...catalog.map(e => e.displayName)),
    operator: operatorArb,
    value: fc.oneof(fc.float({ noNaN: true }), fc.tuple(fc.float({ noNaN: true }), fc.float({ noNaN: true }))),
  });

/** Generates a ScreenerQuery where all fields are valid catalog displayNames */
const validQueryArb = (catalog) =>
  fc.array(validFilterArb(catalog), { minLength: 0, maxLength: 5 }).map(filters => ({ filters }));

/** Generates a string that is NOT in the given set */
const fieldNotInCatalog = (displayNames) =>
  nonEmptyString.filter(s => !displayNames.has(s));

/** Generates a filter whose field is NOT in the catalog */
const invalidFilterArb = (catalog) => {
  const displayNames = new Set(catalog.map(e => e.displayName));
  return fc.record({
    field: fieldNotInCatalog(displayNames),
    operator: operatorArb,
    value: fc.float({ noNaN: true }),
  });
};

// ── Property 2a: valid fields → valid: true, errors: [] ──────────────────────

test('Property 2a: all filter fields from catalog displayNames → valid: true, errors empty', () => {
  fc.assert(
    fc.property(
      catalogArb.chain(catalog =>
        fc.tuple(fc.constant(catalog), validQueryArb(catalog))
      ),
      ([catalog, query]) => {
        const result = validateScreenerQuery(query, catalog);
        assert.strictEqual(result.valid, true,
          `Expected valid:true for query ${JSON.stringify(query)} with catalog displayNames [${catalog.map(e => e.displayName).join(', ')}]`);
        assert.deepStrictEqual(result.errors, [],
          `Expected empty errors for valid query`);
      }
    ),
    { numRuns: 100 }
  );
});

// ── Property 2b: invalid field → valid: false, errors non-empty ──────────────

test('Property 2b: at least one filter field NOT in catalog → valid: false, errors non-empty', () => {
  fc.assert(
    fc.property(
      catalogArb.chain(catalog => {
        const displayNames = new Set(catalog.map(e => e.displayName));
        // Build a query with at least one invalid filter
        return fc.tuple(
          fc.constant(catalog),
          fc.array(validFilterArb(catalog), { minLength: 0, maxLength: 4 }),
          invalidFilterArb(catalog)
        ).map(([cat, validFilters, badFilter]) => {
          // Insert the bad filter at a random position
          const filters = [...validFilters, badFilter];
          return [cat, { filters }];
        });
      }),
      ([catalog, query]) => {
        const result = validateScreenerQuery(query, catalog);
        assert.strictEqual(result.valid, false,
          `Expected valid:false when query has invalid field. Query: ${JSON.stringify(query)}`);
        assert.ok(result.errors.length > 0,
          `Expected non-empty errors when query has invalid field`);
      }
    ),
    { numRuns: 100 }
  );
});

// ── Property 2c: empty filters → always valid ────────────────────────────────

test('Property 2c: empty filters array always returns valid: true', () => {
  fc.assert(
    fc.property(catalogArb, (catalog) => {
      const result = validateScreenerQuery({ filters: [] }, catalog);
      assert.strictEqual(result.valid, true,
        `Expected valid:true for empty filters with any catalog`);
      assert.deepStrictEqual(result.errors, [],
        `Expected empty errors for empty filters`);
    }),
    { numRuns: 100 }
  );
});

/**
 * Property-based tests for metrics-catalog structural integrity.
 *
 * Validates: Requirements 1.2
 *
 * Property 1: metrics-catalog 结构完整性
 * For any catalog entry, it should contain all 5 required fields
 * (name, displayName, category, unit, operators) and operators must be a non-empty array.
 */

import { test } from 'node:test';
import assert from 'node:assert';
import fc from 'fast-check';
import { createRequire } from 'node:module';
import { validateCatalogEntry } from '../lib/catalog-validator.js';

const require = createRequire(import.meta.url);

// ── Arbitraries ──────────────────────────────────────────────────────────────

// Strings with at least one non-whitespace character
const nonEmptyString = fc.string({ minLength: 1, maxLength: 20 }).filter(s => s.trim().length > 0);

/** Generates a structurally valid catalog entry */
const validEntryArb = fc.record({
  name: nonEmptyString,
  displayName: nonEmptyString,
  category: nonEmptyString,
  unit: nonEmptyString,
  operators: fc.array(nonEmptyString, { minLength: 1, maxLength: 5 }),
});

/** Generates an entry missing one or more required fields */
const missingFieldEntryArb = fc.record({
  name: fc.option(nonEmptyString, { nil: undefined }),
  displayName: fc.option(nonEmptyString, { nil: undefined }),
  category: fc.option(nonEmptyString, { nil: undefined }),
  unit: fc.option(nonEmptyString, { nil: undefined }),
  operators: fc.option(
    fc.array(nonEmptyString, { minLength: 1, maxLength: 5 }),
    { nil: undefined }
  ),
}).filter(entry => {
  // Keep only entries that are actually missing at least one field
  const required = ['name', 'displayName', 'category', 'unit', 'operators'];
  return required.some(f => entry[f] === undefined);
});

/** Generates an entry with an empty operators array */
const emptyOperatorsEntryArb = fc.record({
  name: nonEmptyString,
  displayName: nonEmptyString,
  category: nonEmptyString,
  unit: nonEmptyString,
  operators: fc.constant([]),
});

// ── Property tests ────────────────────────────────────────────────────────────

test('Property 1a: valid entries are accepted by validateCatalogEntry', () => {
  fc.assert(
    fc.property(validEntryArb, (entry) => {
      assert.strictEqual(validateCatalogEntry(entry), true,
        `Expected valid entry to pass: ${JSON.stringify(entry)}`);
    }),
    { numRuns: 100 }
  );
});

test('Property 1b: entries missing required fields are rejected', () => {
  fc.assert(
    fc.property(missingFieldEntryArb, (entry) => {
      // Remove undefined keys so the object truly lacks those fields
      const cleaned = Object.fromEntries(
        Object.entries(entry).filter(([, v]) => v !== undefined)
      );
      assert.strictEqual(validateCatalogEntry(cleaned), false,
        `Expected entry with missing fields to fail: ${JSON.stringify(cleaned)}`);
    }),
    { numRuns: 100 }
  );
});

test('Property 1c: entries with empty operators array are rejected', () => {
  fc.assert(
    fc.property(emptyOperatorsEntryArb, (entry) => {
      assert.strictEqual(validateCatalogEntry(entry), false,
        `Expected entry with empty operators to fail: ${JSON.stringify(entry)}`);
    }),
    { numRuns: 100 }
  );
});

test('Property 1d: non-object values are rejected', () => {
  fc.assert(
    fc.property(
      fc.oneof(
        fc.string(),
        fc.integer(),
        fc.boolean(),
        fc.constant(null),
        fc.array(fc.string())
      ),
      (value) => {
        assert.strictEqual(validateCatalogEntry(value), false,
          `Expected non-object to fail: ${JSON.stringify(value)}`);
      }
    ),
    { numRuns: 100 }
  );
});

// ── Concrete test: actual metrics-catalog.json ────────────────────────────────

test('All entries in metrics-catalog.json pass validateCatalogEntry', () => {
  const catalog = require('../metrics-catalog.json', { assert: { type: 'json' } });

  assert.ok(Array.isArray(catalog), 'metrics-catalog.json should be an array');
  assert.ok(catalog.length > 0, 'metrics-catalog.json should not be empty');

  for (const entry of catalog) {
    assert.strictEqual(
      validateCatalogEntry(entry),
      true,
      `Catalog entry failed validation: ${JSON.stringify(entry)}`
    );
  }
});

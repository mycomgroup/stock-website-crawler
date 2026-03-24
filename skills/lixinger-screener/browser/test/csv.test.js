/**
 * Property-based tests for CSV format correctness.
 *
 * Validates: Requirements 5.1
 *
 * Property 4: CSV 格式正确性
 * For any non-empty table data, the generated CSV first line should be the
 * column headers, and every subsequent line should have the same field count
 * as the header line.
 */

import { test } from 'node:test';
import assert from 'node:assert';
import fc from 'fast-check';
import { formatCsv } from '../main.js';

// ── Helpers ───────────────────────────────────────────────────────────────────

/**
 * Counts the number of RFC 4180 fields in a single CSV line.
 * Handles quoted fields (which may contain commas).
 * @param {string} line
 * @returns {number}
 */
function countCsvFields(line) {
  let count = 1;
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    if (inQuotes) {
      if (line[i] === '"') {
        if (line[i + 1] === '"') {
          i++; // escaped quote
        } else {
          inQuotes = false;
        }
      }
    } else {
      if (line[i] === '"') {
        inQuotes = true;
      } else if (line[i] === ',') {
        count++;
      }
    }
  }
  return count;
}

/**
 * Parses a single RFC 4180 CSV field from a line starting at position i.
 * Returns { value, nextIndex }.
 */
function parseCsvField(line, i) {
  if (i < line.length && line[i] === '"') {
    // Quoted field
    let value = '';
    i++; // skip opening quote
    while (i < line.length) {
      if (line[i] === '"') {
        if (i + 1 < line.length && line[i + 1] === '"') {
          value += '"';
          i += 2;
        } else {
          i++; // skip closing quote
          break;
        }
      } else {
        value += line[i++];
      }
    }
    // skip comma after closing quote
    if (i < line.length && line[i] === ',') i++;
    return { value, nextIndex: i };
  } else {
    // Unquoted field
    const end = line.indexOf(',', i);
    if (end === -1) {
      return { value: line.slice(i), nextIndex: line.length };
    }
    return { value: line.slice(i, end), nextIndex: end + 1 };
  }
}

/**
 * Parses a CSV string into an array of arrays, respecting RFC 4180 quoting.
 * Note: does NOT handle multi-line quoted fields (newlines in values split the CSV).
 * @param {string} csv
 * @returns {string[][]}
 */
function parseCsvLine(line) {
  if (line.length === 0) return [''];
  const fields = [];
  let i = 0;
  while (true) {
    const { value, nextIndex } = parseCsvField(line, i);
    fields.push(value);
    if (nextIndex >= line.length) break;
    i = nextIndex;
  }
  // If line ends with a comma, there's a trailing empty field
  if (line[line.length - 1] === ',') {
    fields.push('');
  }
  return fields;
}

// ── Arbitraries ──────────────────────────────────────────────────────────────

/** Safe cell value: no newlines (to keep CSV lines simple for parsing) */
const safeCellArb = fc.string({ minLength: 0, maxLength: 20 }).filter(s => !s.includes('\n') && !s.includes('\r'));

/** Cell value that may contain commas or quotes (but not newlines) */
const specialCellArb = fc.oneof(
  fc.constant('hello,world'),
  fc.constant('say "hi"'),
  fc.constant('a,b,"c"'),
  fc.constant(''),
  safeCellArb
);

/** Generates a non-empty list of unique column header names (no newlines) */
const headersArb = fc
  .array(
    fc.string({ minLength: 1, maxLength: 10 }).filter(s => s.trim().length > 0 && !s.includes('\n') && !s.includes('\r')),
    { minLength: 1, maxLength: 6 }
  )
  .map(arr => [...new Set(arr)])
  .filter(arr => arr.length >= 1);

/** Generates rows with consistent keys; headers derived from Object.keys(rows[0]) */
const rowsArb = headersArb.chain(headers =>
  fc.array(
    fc.tuple(...headers.map(() => safeCellArb)).map(values =>
      // Build object with keys in headers order
      headers.reduce((obj, h, i) => { obj[h] = values[i]; return obj; }, Object.create(null))
    ),
    { minLength: 1, maxLength: 10 }
  ).map(rows => ({ headers: Object.keys(rows[0]), rows }))
);

// ── Property 4a: first line is headers ───────────────────────────────────────

test('Property 4a: first CSV line contains all header keys in order', () => {
  fc.assert(
    fc.property(rowsArb, ({ headers, rows }) => {
      const csv = formatCsv(rows);
      assert.ok(csv.length > 0, 'CSV should not be empty for non-empty rows');

      const firstLine = csv.split('\n')[0];
      const parsedHeaders = parseCsvLine(firstLine);

      assert.deepStrictEqual(
        parsedHeaders,
        headers,
        `First CSV line should be headers. Expected: ${JSON.stringify(headers)}, got: ${JSON.stringify(parsedHeaders)}`
      );
    }),
    { numRuns: 100 }
  );
});

// ── Property 4b: every data line has same field count as header ───────────────

test('Property 4b: every data line has same field count as header line', () => {
  fc.assert(
    fc.property(rowsArb, ({ rows }) => {
      const csv = formatCsv(rows);
      const lines = csv.split('\n');

      assert.ok(lines.length >= 2,
        `CSV should have header + at least one data line, got ${lines.length} lines`);

      const headerCount = countCsvFields(lines[0]);
      for (let i = 1; i < lines.length; i++) {
        const fieldCount = countCsvFields(lines[i]);
        assert.strictEqual(
          fieldCount,
          headerCount,
          `Line ${i + 1} has ${fieldCount} fields but header has ${headerCount}. Line: ${JSON.stringify(lines[i])}`
        );
      }
    }),
    { numRuns: 100 }
  );
});

// ── Property 4c: empty rows returns empty string ──────────────────────────────

test('Property 4c: empty rows array returns empty string', () => {
  assert.strictEqual(formatCsv([]), '');
  assert.strictEqual(formatCsv(null), '');
  assert.strictEqual(formatCsv(undefined), '');
});

// ── Concrete tests: RFC 4180 escaping ────────────────────────────────────────

test('RFC 4180: value with comma is wrapped in double quotes', () => {
  const rows = [{ col: 'hello,world' }];
  const csv = formatCsv(rows);
  const lines = csv.split('\n');
  assert.strictEqual(lines[1], '"hello,world"');
});

test('RFC 4180: value with double quote escapes internal quotes', () => {
  const rows = [{ col: 'say "hi"' }];
  const csv = formatCsv(rows);
  const lines = csv.split('\n');
  assert.strictEqual(lines[1], '"say ""hi"""');
});

test('RFC 4180: value with newline is wrapped in double quotes', () => {
  const rows = [{ col: 'line1\nline2' }];
  const csv = formatCsv(rows);
  assert.ok(csv.includes('"line1\nline2"'), 'Newline in value should be quoted');
});

test('RFC 4180: plain value without special chars is not quoted', () => {
  const rows = [{ col: 'hello' }];
  const csv = formatCsv(rows);
  const lines = csv.split('\n');
  assert.strictEqual(lines[1], 'hello');
});

// ── Property 4d: values with special chars round-trip correctly ───────────────

test('Property 4d: values with special chars (no newlines) round-trip correctly', () => {
  fc.assert(
    fc.property(
      headersArb.chain(headers =>
        fc.tuple(...headers.map(() => specialCellArb)).map(values => {
          const row = headers.reduce((obj, h, i) => { obj[h] = values[i]; return obj; }, Object.create(null));
          return { headers: Object.keys(row), rows: [row] };
        })
      ),
      ({ headers, rows }) => {
        const csv = formatCsv(rows);
        const lines = csv.split('\n');

        // lines[0] = header line, lines[1] = data line
        assert.ok(lines.length >= 2, 'Should have header and data line');

        const parsedData = parseCsvLine(lines[1]);

        for (let i = 0; i < headers.length; i++) {
          const original = String(rows[0][headers[i]] ?? '');
          const roundTripped = parsedData[i];
          assert.strictEqual(
            roundTripped,
            original,
            `Value for column "${headers[i]}" should round-trip. Original: ${JSON.stringify(original)}, got: ${JSON.stringify(roundTripped)}`
          );
        }
      }
    ),
    { numRuns: 100 }
  );
});

import { describe, it } from 'node:test';
import assert from 'node:assert';
import { StructureComparator } from '../lib/structure-comparator.js';

describe('StructureComparator', () => {
  it('finds common section headings and table headers', () => {
    const comparator = new StructureComparator();
    const result = comparator.compare([
      {
        url: 'a',
        title: 'A',
        sections: [{ heading: 'Overview' }, { heading: 'Financials' }],
        tables: [{ headers: ['Year', 'Revenue'] }],
        lists: [['x', 'y']]
      },
      {
        url: 'b',
        title: 'B',
        sections: [{ heading: 'Overview' }, { heading: 'Risks' }],
        tables: [{ headers: ['Year', 'Revenue', 'Profit'] }],
        lists: [['z']]
      }
    ]);

    assert.deepEqual(result.commonSectionHeadings, ['Overview']);
    assert.deepEqual(result.commonTableHeaders, ['Revenue', 'Year']);
    assert.equal(result.signatures.length, 2);
  });
});

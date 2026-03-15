/**
 * StructureComparator - compares extracted pages of the same type
 * to find stable/common structure for human-assisted template refinement.
 */
export class StructureComparator {
  compare(records = []) {
    if (!Array.isArray(records) || records.length === 0) {
      return {
        total: 0,
        commonSectionHeadings: [],
        commonTableHeaders: [],
        signatures: []
      };
    }

    const sectionSets = records.map(r => new Set((r.sections || []).map(s => s.heading).filter(Boolean)));
    const tableHeaderSets = records.map(r => {
      const headers = [];
      for (const table of (r.tables || [])) {
        for (const h of (table.headers || [])) {
          if (h) headers.push(h);
        }
      }
      return new Set(headers);
    });

    const commonSectionHeadings = this._intersection(sectionSets);
    const commonTableHeaders = this._intersection(tableHeaderSets);

    const signatures = records.map((r) => ({
      url: r.url,
      signature: this._buildSignature(r)
    }));

    return {
      total: records.length,
      commonSectionHeadings,
      commonTableHeaders,
      signatures
    };
  }

  _buildSignature(record) {
    const sectionHeadings = (record.sections || []).map(s => s.heading).filter(Boolean).sort();
    const tableShapes = (record.tables || []).map(t => (t.headers || []).filter(Boolean).join('|')).sort();
    const listSizes = (record.lists || []).map(list => list.length).sort((a, b) => a - b);

    return {
      sectionHeadings,
      tableShapes,
      listSizes,
      hasTitle: Boolean(record.title)
    };
  }

  _intersection(sets) {
    if (sets.length === 0) return [];
    const [first, ...rest] = sets;
    return [...first].filter(item => rest.every(s => s.has(item))).sort();
  }
}

export default StructureComparator;

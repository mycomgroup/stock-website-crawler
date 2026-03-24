/**
 * Validates a single metrics-catalog entry.
 * A valid entry must have all 5 required fields:
 *   name, displayName, category, unit, operators
 * and operators must be a non-empty array.
 *
 * @param {unknown} entry
 * @returns {boolean}
 */
export function validateCatalogEntry(entry) {
  if (entry === null || typeof entry !== 'object' || Array.isArray(entry)) {
    return false;
  }

  const required = ['name', 'displayName', 'category', 'unit', 'operators'];
  for (const field of required) {
    if (!(field in entry)) return false;
    if (entry[field] === undefined || entry[field] === null) return false;
  }

  // name, displayName, category, unit must be non-empty strings
  for (const field of ['name', 'displayName', 'category', 'unit']) {
    if (typeof entry[field] !== 'string' || entry[field].trim() === '') return false;
  }

  // operators must be a non-empty array
  if (!Array.isArray(entry.operators) || entry.operators.length === 0) return false;

  return true;
}

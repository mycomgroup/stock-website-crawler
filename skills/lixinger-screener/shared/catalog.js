import fs from 'node:fs';
import path from 'node:path';
import { BROWSER_ROOT, LIXINGER_OUTPUT_DIR } from '../paths.js';

export const DEFAULT_CONDITION_CATALOG_PATH = path.join(
  LIXINGER_OUTPUT_DIR,
  'condition-catalog.cn.json'
);
export const DEFAULT_BROWSER_METRICS_CATALOG_PATH = path.join(
  BROWSER_ROOT,
  'metrics-catalog.json'
);

export function loadJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

export function saveJson(filePath, data) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

export function loadConditionCatalog(filePath = DEFAULT_CONDITION_CATALOG_PATH) {
  return loadJson(filePath);
}

export function loadConditionMetrics(filePath = DEFAULT_CONDITION_CATALOG_PATH) {
  const catalog = loadConditionCatalog(filePath);
  if (!Array.isArray(catalog?.metrics)) {
    throw new Error(`Invalid condition catalog: ${filePath}`);
  }
  return catalog.metrics;
}

export function loadBrowserMetricsCatalog(filePath = DEFAULT_BROWSER_METRICS_CATALOG_PATH) {
  const catalog = loadJson(filePath);
  if (!Array.isArray(catalog)) {
    throw new Error(`Invalid browser metrics catalog: ${filePath}`);
  }
  return catalog;
}

export function resolveCatalogPath(catalogPath, cwd = process.cwd()) {
  if (!catalogPath) return DEFAULT_CONDITION_CATALOG_PATH;
  return path.resolve(cwd, catalogPath);
}

export function conditionCatalogExists(filePath = DEFAULT_CONDITION_CATALOG_PATH) {
  return fs.existsSync(filePath);
}

export function getConditionDisplayLabel(entry) {
  return entry?.displayLabelExample || entry?.metric || null;
}

export function isConditionMetricEntry(entry) {
  return Boolean(entry?.metric && Object.prototype.hasOwnProperty.call(entry, 'displayLabelExample'));
}

export function isBrowserMetricEntry(entry) {
  return Boolean(entry?.displayName && Array.isArray(entry?.operators));
}

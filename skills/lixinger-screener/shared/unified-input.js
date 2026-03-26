import { loadBrowserMetricsCatalog } from './catalog.js';

const DEFAULT_RANGES = {
  market: 'a',
  stockBourseTypes: [],
  mutualMarkets: { selectedMutualMarkets: [], selectType: 'include' },
  multiMarketListedType: { selectedMultiMarketListedTypes: [], selectType: 'include' },
  excludeBlacklist: false,
  excludeDelisted: false,
  excludeBourseType: false,
  excludeSpecialTreatment: false,
  constituentsPerspectiveType: 'history',
  specialTreatmentOnly: false
};

const SPECIAL_METRIC_ALIASES = {
  '上市日期': {
    requestId: 'pm.ipoDate',
    resultFieldKey: 'ipoDate',
    supportedSubConditionLabels: ['上市时间'],
    notes: '当前脚本只支持“上市时间”这一种子条件。'
  },
  '市值/自由现金流': {
    browserField: '市值',
    browserCategory: '估值',
    browserFallbackLabels: ['PCF-TTM', '市值/自由现金流']
  }
};

export function normalizeOperatorValueCondition(condition) {
  const next = { ...condition };

  if (next.field && !next.displayLabel) {
    next.displayLabel = next.field;
  }

  if ((next.min == null && next.max == null) && next.operator) {
    if (next.operator === '介于') {
      if (!Array.isArray(next.value) || next.value.length !== 2) {
        throw new Error(`Condition ${JSON.stringify(condition)} requires a [min, max] array`);
      }
      [next.min, next.max] = next.value;
    } else if (next.operator === '大于') {
      next.min = next.value;
    } else if (next.operator === '小于') {
      next.max = next.value;
    } else {
      throw new Error(`Unsupported operator "${next.operator}" in condition ${JSON.stringify(condition)}`);
    }
  }

  return next;
}

export function normalizeUnifiedInput(input = {}) {
  const rawConditions = input.conditions || input.filters || [];
  return {
    ...input,
    conditions: rawConditions.map(normalizeOperatorValueCondition)
  };
}

export function mergeUnifiedInputs(baseInput = {}, extraInput = {}) {
  const base = normalizeUnifiedInput(baseInput);
  const extra = normalizeUnifiedInput(extraInput);

  return {
    ...base,
    ...extra,
    conditions: [...(base.conditions || []), ...(extra.conditions || [])]
  };
}

function stripLatestSuffix(formulaId) {
  return formulaId.endsWith('.latest')
    ? formulaId.slice(0, -('.latest'.length))
    : formulaId;
}

const SCREENER_DATE_ALIASES = {
  latest_fs: 'latest',
  latest_time: 'latest'
};

const Q_SUBCONDITION_TOKEN_MAP = {
  '累积': 'y',
  '累积同比': 'y_yoy',
  '累积环比': 'y_qoq',
  '累积年比': 'y_y2y',
  '当期': 'y',
  '当期同比': 'y_yoy',
  '当期环比': 'y_qoq',
  '当期年比': 'y_y2y',
  '单季': 'q',
  '单季同比': 'q_yoy',
  '单季环比': 'q_qoq',
  '单季年比': 'q_y2y',
  'TTM': 'ttm',
  'TTM同比': 'ttm_yoy',
  'TTM环比': 'ttm_qoq'
};

function getRequestIdPrefix(requestId) {
  return String(requestId || '').split('.')[0] || '';
}

function normalizeScreenerDateMode(dateModeApi, requestId) {
  if (/Date$/.test(requestId)) {
    return null;
  }

  const normalized = SCREENER_DATE_ALIASES[dateModeApi] || dateModeApi || null;
  if (normalized) {
    return normalized;
  }

  const prefix = getRequestIdPrefix(requestId);
  if (prefix === 'pm' || prefix === 'hm' || prefix === 'q') {
    return 'latest';
  }

  return null;
}

function resolveQSubConditionToken(rawToken, subCondition) {
  if (subCondition && Q_SUBCONDITION_TOKEN_MAP[subCondition]) {
    return Q_SUBCONDITION_TOKEN_MAP[subCondition];
  }
  if (rawToken) {
    return rawToken;
  }
  return 'y';
}

function normalizeQMetricRequestId(requestId, options = {}) {
  if (!String(requestId || '').startsWith('q.')) {
    return requestId;
  }

  const normalizedRequestId = stripLatestSuffix(requestId);
  const rawPattern = /^(q\..+)\.[^.]+\.dynamic~lq~([^~]+)~0$/;
  const match = normalizedRequestId.match(rawPattern);
  if (!match) {
    return normalizedRequestId;
  }

  const [, baseId, rawToken] = match;
  const token = resolveQSubConditionToken(rawToken, options.subCondition);
  return `${baseId}.${token}`;
}

function normalizeScreenerRequestId(requestId, options = {}) {
  const prefix = getRequestIdPrefix(requestId);
  if (prefix === 'q') {
    return normalizeQMetricRequestId(requestId, options);
  }
  return stripLatestSuffix(requestId);
}

function requestIdToSortName(requestId) {
  const prefix = getRequestIdPrefix(requestId);
  if (prefix === 'pm') {
    return `pm.latest.${requestId.replace(/^pm\./, '')}`;
  }
  if (prefix === 'q') {
    return `fsm.latest.${requestId}`;
  }
  return requestId;
}

function requestIdToResultFieldKey(requestId) {
  const prefix = getRequestIdPrefix(requestId);
  if (prefix === 'pm') {
    return requestId.replace(/^pm\./, '');
  }
  if (prefix === 'q') {
    return `fsm.latest.${requestId}`;
  }
  return requestId;
}

function mapScaleByUnit(unit) {
  if (unit === '%') return 0.01;
  if (unit === '亿') return 100000000;
  return 1;
}

function guessThresholdKind(unit, inputType) {
  if (inputType === 'date') return 'date';
  if (unit === '%') return 'percentage';
  if (unit === '亿') return 'yi';
  return 'number';
}

function defaultRanges(overrides = {}, baseRanges = {}) {
  return {
    ...DEFAULT_RANGES,
    ...baseRanges,
    ...overrides,
    mutualMarkets: overrides.mutualMarkets
      || baseRanges.mutualMarkets
      || DEFAULT_RANGES.mutualMarkets,
    multiMarketListedType: overrides.multiMarketListedType
      || baseRanges.multiMarketListedType
      || DEFAULT_RANGES.multiMarketListedType
  };
}

export function normalizeFilterList(filterList = []) {
  return filterList.map(item => {
    const next = { ...item };
    next.id = normalizeScreenerRequestId(next.id);
    if (!Object.prototype.hasOwnProperty.call(next, 'value')) {
      next.value = 'all';
    }
    const normalizedDate = normalizeScreenerDateMode(next.date, next.id);
    if (normalizedDate) {
      next.date = normalizedDate;
    }
    return next;
  });
}

export function normalizeSortName(sortName) {
  if (!sortName) return 'pm.latest.d_pe_ttm.y10.cvpos';
  if (sortName.startsWith('priceMetrics.latest.pm.')) {
    return sortName.replace(/^priceMetrics\.latest\.pm\./, 'pm.latest.');
  }
  if (sortName.startsWith('priceMetrics.latest.')) {
    return sortName.replace(/^priceMetrics\.latest\./, '');
  }
  return sortName;
}

function getCatalogMetrics(catalog) {
  if (Array.isArray(catalog)) return catalog;
  if (Array.isArray(catalog?.metrics)) return catalog.metrics;
  return [];
}

function findBrowserCatalogEntry(condition) {
  const browserCatalog = loadBrowserMetricsCatalog();
  const labels = new Set([
    condition.displayLabel,
    condition.field,
    condition.metric,
    ...(SPECIAL_METRIC_ALIASES[condition.metric || condition.displayLabel || condition.field || '']?.browserFallbackLabels || [])
  ].filter(Boolean));

  return browserCatalog.find(entry => labels.has(entry.displayName) || labels.has(entry.metric)) || null;
}

export function lookupCatalogEntry(catalog, rawCondition) {
  const condition = normalizeOperatorValueCondition(rawCondition);
  const metrics = getCatalogMetrics(catalog);
  if (!metrics.length) return null;

  if (condition.metric) {
    let candidates = metrics.filter(item => item.metric === condition.metric);
    if (condition.category) {
      candidates = candidates.filter(item => item.category === condition.category);
    }
    const preferred = candidates.find(item => item.category === '基本指标');
    return preferred || candidates[0] || null;
  }

  if (condition.displayLabel) {
    let candidates = metrics.filter(item => item.displayLabelExample === condition.displayLabel);
    if (condition.category) {
      candidates = candidates.filter(item => item.category === condition.category);
    }
    return candidates[0] || null;
  }

  if (condition.formulaId) {
    const requestId = stripLatestSuffix(condition.formulaId);
    return metrics.find(item =>
      item.formulaIdExample === condition.formulaId ||
      item.requestIdExample === requestId ||
      item.specialRequestId === requestId
    ) || null;
  }

  return null;
}

function resolveSelectorChoice(selector, desiredLabel, metricName) {
  const option = selector.options.find(item => item.label === desiredLabel);
  if (!option) {
    throw new Error(
      `Unknown selector label "${desiredLabel}" for metric "${metricName}". ` +
      `Available options: ${selector.options.map(item => item.label).join(', ')}`
    );
  }
  return option;
}

export function buildFormulaIdFromCondition(entry, rawCondition) {
  const condition = normalizeOperatorValueCondition(rawCondition);

  if (condition.formulaId) {
    return condition.formulaId;
  }

  if (entry?.formulaIdTemplate) {
    let formulaId = entry.formulaIdTemplate;
    const selectors = condition.selectors || [];
    for (let index = 0; index < (entry.selectors || []).length; index += 1) {
      const selector = entry.selectors[index];
      const desiredLabel = selectors[index] || selector.defaultLabel;
      const option = resolveSelectorChoice(selector, desiredLabel, entry.metric);
      formulaId = formulaId.replace(`{selector${index + 1}}`, option.value);
    }
    return formulaId;
  }

  return entry?.formulaIdExample || null;
}

export function buildDisplayLabel(entry, rawCondition) {
  const condition = normalizeOperatorValueCondition(rawCondition);

  if (condition.displayLabel) {
    return condition.displayLabel;
  }

  let label = entry.displayLabelExample || entry.displayName || entry.metric;
  const selectors = condition.selectors || [];

  for (let index = 0; index < (entry.selectors || []).length; index += 1) {
    const selector = entry.selectors[index];
    const desiredLabel = selectors[index] || selector.defaultLabel;
    resolveSelectorChoice(selector, desiredLabel, entry.metric);
    if (selector.defaultLabel && desiredLabel && selector.defaultLabel !== desiredLabel) {
      label = label.replace(selector.defaultLabel, desiredLabel);
    }
  }

  return label;
}

function resolveDateMode(entry, condition) {
  const desiredLabel = condition.dateModeLabel || condition.dateMode || null;
  const desiredValue = condition.dateModeApi || null;
  const options = entry?.dateModes || [];

  if (!desiredLabel && !desiredValue) {
    return null;
  }

  if (!options.length) {
    return {
      label: desiredLabel || desiredValue,
      value: desiredValue || desiredLabel
    };
  }

  const option = options.find(item =>
    (desiredLabel && item.label === desiredLabel) ||
    (desiredValue && item.value === desiredValue) ||
    (desiredValue && item.label === desiredValue) ||
    (desiredLabel && item.value === desiredLabel)
  );

  if (!option) {
    throw new Error(
      `Unknown date mode for metric "${entry.metric}". ` +
      `Available options: ${options.map(item => item.label).join(', ')}`
    );
  }

  return {
    label: option.label,
    value: option.value
  };
}

function resolveSubCondition(entry, condition) {
  const desired = condition.subCondition || null;
  const options = entry?.subConditionOptions || [];

  if (!desired) {
    return null;
  }

  if (options.length && !options.includes(desired)) {
    throw new Error(
      `Unknown subCondition "${desired}" for metric "${entry.metric}". ` +
      `Available options: ${options.join(', ')}`
    );
  }

  return desired;
}

export function resolveUnifiedCondition(entry, rawCondition) {
  const condition = normalizeOperatorValueCondition(rawCondition);
  const aliasName = condition.metric || condition.displayLabel || condition.field || null;
  const alias = aliasName ? SPECIAL_METRIC_ALIASES[aliasName] : null;

  if (alias) {
    const subCondition = condition.subCondition || alias.supportedSubConditionLabels?.[0] || null;
    if (subCondition && alias.supportedSubConditionLabels && !alias.supportedSubConditionLabels.includes(subCondition)) {
      throw new Error(
        `Metric "${aliasName}" currently supports only: ${alias.supportedSubConditionLabels.join(', ')}`
      );
    }

    return {
      filter: {
        id: alias.requestId,
        value: 'all',
        min: condition.min,
        max: condition.max
      },
      columnSpec: {
        metric: aliasName,
        displayLabel: condition.displayLabel || condition.field || aliasName,
        requestId: alias.requestId,
        resultFieldKey: alias.resultFieldKey,
        format: 'date',
        unit: null
      }
    };
  }

  if (!entry) {
    throw new Error(`Unable to resolve condition: ${JSON.stringify(rawCondition)}`);
  }

  const formulaId = buildFormulaIdFromCondition(entry, condition);
  if (!formulaId) {
    throw new Error(`Metric "${entry.metric}" does not expose a formula ID.`);
  }

  const dateMode = resolveDateMode(entry, condition);
  const subCondition = resolveSubCondition(entry, condition);
  const rawRequestId = stripLatestSuffix(formulaId);
  const requestId = normalizeScreenerRequestId(rawRequestId, {
    subCondition,
    dateModeApi: dateMode?.value || null
  });
  const primaryThreshold = entry.thresholds?.min || entry.thresholds?.max || {};
  const scale = mapScaleByUnit(primaryThreshold.unit);
  const kind = guessThresholdKind(primaryThreshold.unit, primaryThreshold.inputType);

  const filter = {
    id: requestId,
    value: 'all'
  };

  const filterDate = normalizeScreenerDateMode(dateMode?.value || condition.dateModeApi, requestId);
  if (filterDate) {
    filter.date = filterDate;
  }

  if (condition.min != null) {
    filter.min = kind === 'date' ? condition.min : Number(condition.min) * scale;
  }
  if (condition.max != null) {
    filter.max = kind === 'date' ? condition.max : Number(condition.max) * scale;
  }

  return {
    filter,
    columnSpec: {
      metric: entry.metric,
      displayLabel: buildDisplayLabel(entry, condition),
      requestId,
      resultFieldKey: requestIdToResultFieldKey(requestId),
      format: kind,
      unit: primaryThreshold.unit || null
    }
  };
}

export function buildRequestPlanFromUnifiedInput(rawInput, catalog, options = {}) {
  const input = normalizeUnifiedInput(rawInput);
  const filters = [];
  const columnSpecs = [];

  for (const condition of input.conditions || []) {
    const entry = lookupCatalogEntry(catalog, condition);
    const resolved = resolveUnifiedCondition(entry, condition);
    filters.push(resolved.filter);
    columnSpecs.push(resolved.columnSpec);
  }

  const sortCondition = input.sort || input.conditions?.[0] || null;
  const sortEntry = sortCondition ? lookupCatalogEntry(catalog, sortCondition) : null;
  const resolvedSort = sortCondition ? resolveUnifiedCondition(sortEntry, sortCondition) : null;

  const body = {
    areaCode: input.areaCode || options.areaCode || 'cn',
    ranges: defaultRanges(input.ranges, options.defaultRanges),
    filterList: filters,
    customFilterList: input.customFilterList || [],
    industrySource: input.industrySource ?? options.industrySource ?? 'sw_2021',
    industryLevel: input.industryLevel ?? options.industryLevel ?? 'three',
    sortName: normalizeSortName(
      input.sortName
      || (resolvedSort ? requestIdToSortName(resolvedSort.filter.id) : null)
      || options.defaultSortName
    ),
    sortOrder: input.sortOrder || input.sort?.order || options.defaultSortOrder || 'desc',
    pageIndex: Number(input.pageIndex ?? options.pageIndex ?? 0),
    pageSize: Number(input.pageSize ?? options.pageSize ?? 100)
  };

  return {
    body,
    columnSpecs,
    summary: {
      screenerName: input.name || null
    }
  };
}

export function buildRequestPlanFromScreener(config, options = {}) {
  const body = {
    areaCode: config.areaCode || options.areaCode || 'cn',
    ranges: defaultRanges(config.ranges, options.defaultRanges),
    filterList: normalizeFilterList(config.filterList),
    customFilterList: config.customFilterList || [],
    industrySource: config.industrySource ?? options.industrySource ?? 'sw_2021',
    industryLevel: config.industryLevel ?? options.industryLevel ?? 'three',
    sortName: normalizeSortName(config.sortName || options.defaultSortName),
    sortOrder: config.sortOrder || options.defaultSortOrder || 'desc',
    pageIndex: Number(options.pageIndex ?? config.pageIndex ?? 0),
    pageSize: Number(options.pageSize ?? config.pageSize ?? 100)
  };

  const columnSpecs = body.filterList.map(item => ({
    metric: item.id,
    displayLabel: item.id,
    requestId: item.id,
    resultFieldKey: requestIdToResultFieldKey(item.id),
    format: item.id.endsWith('Date') ? 'date' : 'number',
    unit: null
  }));

  return {
    body,
    columnSpecs,
    summary: {
      screenerName: config.name || null
    }
  };
}

export function conditionToBrowserFilter(rawCondition, catalog = null) {
  const condition = normalizeOperatorValueCondition(rawCondition);
  let entry = null;
  let displayLabel = condition.displayLabel || condition.field || null;

  if (!displayLabel) {
    if (!catalog) {
      entry = findBrowserCatalogEntry(condition);
      if (!entry) {
        throw new Error(
          `Condition ${JSON.stringify(rawCondition)} requires a condition catalog to resolve browser field name`
        );
      }
      displayLabel = buildDisplayLabel(entry, condition);
    } else {
      entry = lookupCatalogEntry(catalog, condition);
      if (!entry) {
        entry = findBrowserCatalogEntry(condition);
      }
      if (!entry) {
        throw new Error(`Unable to resolve browser field for condition: ${JSON.stringify(rawCondition)}`);
      }
      displayLabel = buildDisplayLabel(entry, condition);
    }
  } else if (catalog) {
    entry = lookupCatalogEntry(catalog, condition);
    if (!entry) {
      entry = findBrowserCatalogEntry(condition);
    }
  }

  const alias = SPECIAL_METRIC_ALIASES[condition.metric || condition.displayLabel || condition.field || ''] || null;
  if (alias?.browserField) {
    displayLabel = alias.browserField;
  }

  const category = alias?.browserCategory || condition.category || entry?.category || null;
  const dateMode = resolveDateMode(entry, condition);
  const subCondition = resolveSubCondition(entry, condition);
  const sharedFields = {
    field: displayLabel,
    category,
    ...(dateMode?.label ? { dateModeLabel: dateMode.label } : {}),
    ...(dateMode?.value ? { dateModeApi: dateMode.value } : {}),
    ...(subCondition ? { subCondition } : {})
  };

  if (condition.min != null && condition.max != null) {
    return { ...sharedFields, operator: '介于', value: [condition.min, condition.max] };
  }
  if (condition.min != null) {
    return { ...sharedFields, operator: '大于', value: condition.min };
  }
  if (condition.max != null) {
    return { ...sharedFields, operator: '小于', value: condition.max };
  }

  throw new Error(`Condition ${JSON.stringify(rawCondition)} is missing min/max or operator/value`);
}

export function buildBrowserFiltersFromUnifiedInput(rawInput, catalog = null) {
  const input = normalizeUnifiedInput(rawInput);
  return (input.conditions || []).map(condition => conditionToBrowserFilter(condition, catalog));
}

export function inputNeedsConditionCatalog(rawInput) {
  const input = normalizeUnifiedInput(rawInput);
  return (input.conditions || []).some(condition =>
    condition.metric ||
    condition.category ||
    condition.formulaId ||
    (Array.isArray(condition.selectors) && condition.selectors.length > 0) ||
    condition.subCondition
  );
}

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

function requestIdToResultFieldKey(requestId) {
  return requestId.replace(/^pm\./, '');
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

function defaultRanges(overrides = {}) {
  return {
    ...DEFAULT_RANGES,
    ...overrides,
    mutualMarkets: overrides.mutualMarkets || DEFAULT_RANGES.mutualMarkets,
    multiMarketListedType: overrides.multiMarketListedType || DEFAULT_RANGES.multiMarketListedType
  };
}

export function normalizeFilterList(filterList = []) {
  return filterList.map(item => {
    const next = { ...item };
    if (!Object.prototype.hasOwnProperty.call(next, 'value')) {
      next.value = 'all';
    }
    if (!next.date && next.id?.startsWith('pm.') && !/Date$/.test(next.id)) {
      next.date = 'latest';
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

  let label = entry.displayLabelExample || entry.metric;
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

  const requestId = stripLatestSuffix(formulaId);
  const primaryThreshold = entry.thresholds?.min || entry.thresholds?.max || {};
  const scale = mapScaleByUnit(primaryThreshold.unit);
  const kind = guessThresholdKind(primaryThreshold.unit, primaryThreshold.inputType);

  const filter = {
    id: requestId,
    value: 'all'
  };

  if (!/Date$/.test(requestId)) {
    filter.date = condition.dateModeApi || 'latest';
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
    ranges: defaultRanges(input.ranges),
    filterList: filters,
    customFilterList: input.customFilterList || [],
    industrySource: input.industrySource || 'sw_2021',
    industryLevel: input.industryLevel || 'three',
    sortName: normalizeSortName(input.sortName ||
      (resolvedSort ? `pm.latest.${requestIdToResultFieldKey(resolvedSort.filter.id)}` : null)),
    sortOrder: input.sortOrder || input.sort?.order || 'desc',
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
    ranges: defaultRanges(config.ranges),
    filterList: normalizeFilterList(config.filterList),
    customFilterList: config.customFilterList || [],
    industrySource: config.industrySource || 'sw_2021',
    industryLevel: config.industryLevel || 'three',
    sortName: normalizeSortName(config.sortName),
    sortOrder: config.sortOrder || 'desc',
    pageIndex: Number(options.pageIndex || 0),
    pageSize: Number(options.pageSize || 100)
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
      throw new Error(
        `Condition ${JSON.stringify(rawCondition)} requires a condition catalog to resolve browser field name`
      );
    }
    entry = lookupCatalogEntry(catalog, condition);
    if (!entry) {
      throw new Error(`Unable to resolve browser field for condition: ${JSON.stringify(rawCondition)}`);
    }
    displayLabel = buildDisplayLabel(entry, condition);
  } else if (catalog) {
    entry = lookupCatalogEntry(catalog, condition);
  }

  const category = condition.category || entry?.category || null;

  if (condition.min != null && condition.max != null) {
    return { field: displayLabel, category, operator: '介于', value: [condition.min, condition.max] };
  }
  if (condition.min != null) {
    return { field: displayLabel, category, operator: '大于', value: condition.min };
  }
  if (condition.max != null) {
    return { field: displayLabel, category, operator: '小于', value: condition.max };
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

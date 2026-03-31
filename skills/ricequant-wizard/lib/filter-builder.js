import { OPERATORS } from './factor-definitions.js';

export class FilterBuilder {
  constructor() {
    this.filters = [];
  }

  add(factor, operator, value) {
    this.filters.push({
      operator,
      lhs: factor,
      rhs: value
    });
    return this;
  }

  peLessThan(value) {
    return this.add({ type: 'fundamental', name: 'pe_ratio' }, 'less_than', value);
  }

  pbLessThan(value) {
    return this.add({ type: 'fundamental', name: 'pb_ratio' }, 'less_than', value);
  }

  peBetween(min, max) {
    return this.add({ type: 'fundamental', name: 'pe_ratio' }, 'in_range', [min, max]);
  }

  pbBetween(min, max) {
    return this.add({ type: 'fundamental', name: 'pb_ratio' }, 'in_range', [min, max]);
  }

  roeGreaterThan(value) {
    return this.add({ type: 'fundamental', name: 'roe' }, 'greater_than', value);
  }

  debtRatioLessThan(value) {
    return this.add({ type: 'fundamental', name: 'debt_ratio' }, 'less_than', value);
  }

  dividendYieldGreaterThan(value) {
    return this.add({ type: 'fundamental', name: 'dividend_yield' }, 'greater_than', value);
  }

  marketCapBetween(min, max) {
    return this.add({ type: 'fundamental', name: 'market_cap' }, 'in_range', [min, max]);
  }

  listedDaysGreaterThan(days) {
    return this.add({ type: 'extra', name: 'listed_days' }, 'greater_than', days);
  }

  rankInRange(factor, minPercent, maxPercent) {
    return this.add(factor, 'rank_in_range', [minPercent, maxPercent]);
  }

  build() {
    return this.filters;
  }

  static fromConfig(config) {
    const builder = new FilterBuilder();
    for (const filter of config) {
      builder.add(
        filter.factor || { type: filter.type || 'fundamental', name: filter.name },
        filter.operator,
        filter.rhs || filter.value
      );
    }
    return builder.build();
  }
}

export function validateFilter(filter) {
  const errors = [];
  
  if (!filter.operator) {
    errors.push('缺少 operator');
  } else if (!OPERATORS.find(o => o.name === filter.operator)) {
    errors.push(`不支持的 operator: ${filter.operator}`);
  }
  
  if (!filter.lhs) {
    errors.push('缺少 lhs (因子引用)');
  } else {
    if (!filter.lhs.type) {
      errors.push('lhs 缺少 type');
    }
    if (!filter.lhs.name) {
      errors.push('lhs 缺少 name');
    }
  }
  
  if (filter.rhs === undefined && filter.value === undefined) {
    errors.push('缺少 rhs 或 value');
  }
  
  const op = OPERATORS.find(o => o.name === filter.operator);
  if (op?.requiresArray && !Array.isArray(filter.rhs || filter.value)) {
    errors.push(`${filter.operator} 需要 rhs 为数组 [min, max]`);
  }
  
  return { valid: errors.length === 0, errors };
}
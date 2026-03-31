export class SortingBuilder {
  constructor() {
    this.rules = [];
  }

  add(factor, ascending = true, weight = 1) {
    this.rules.push({
      factor,
      ascending,
      weight
    });
    return this;
  }

  sortByMarketCap(desc = true) {
    return this.add({ type: 'fundamental', name: 'market_cap' }, !desc, 1);
  }

  sortByPE(ascending = true) {
    return this.add({ type: 'fundamental', name: 'pe_ratio' }, ascending, 1);
  }

  sortByPB(ascending = true) {
    return this.add({ type: 'fundamental', name: 'pb_ratio' }, ascending, 1);
  }

  sortByROE(desc = true) {
    return this.add({ type: 'fundamental', name: 'roe' }, !desc, 1);
  }

  sortByDividendYield(desc = true) {
    return this.add({ type: 'fundamental', name: 'dividend_yield' }, !desc, 1);
  }

  sortByTurnoverRate(desc = true) {
    return this.add({ type: 'pricing', name: 'turnover_rate' }, !desc, 1);
  }

  build() {
    const totalWeight = this.rules.reduce((sum, r) => sum + r.weight, 0);
    if (totalWeight > 0 && totalWeight !== 1) {
      console.log(`Warning: Sorting weights sum to ${totalWeight}, normalizing to 1`);
      this.rules = this.rules.map(r => ({
        ...r,
        weight: r.weight / totalWeight
      }));
    }
    return this.rules;
  }

  static fromConfig(config) {
    const builder = new SortingBuilder();
    for (const rule of config) {
      builder.add(
        rule.factor || { type: rule.type || 'fundamental', name: rule.name },
        rule.ascending !== false,
        rule.weight || 1
      );
    }
    return builder.build();
  }
}

export function validateSortingRule(rule) {
  const errors = [];
  
  if (!rule.factor) {
    errors.push('缺少 factor');
  } else {
    if (!rule.factor.type) {
      errors.push('factor 缺少 type');
    }
    if (!rule.factor.name) {
      errors.push('factor 缺少 name');
    }
  }
  
  if (rule.weight !== undefined && (rule.weight < 0 || rule.weight > 1)) {
    errors.push('weight 应在 0-1 之间');
  }
  
  return { valid: errors.length === 0, errors };
}
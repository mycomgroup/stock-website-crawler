import fs from 'fs';

/**
 * Pattern 匹配器
 */
export class PatternMatcher {
  constructor(patternsPath) {
    const content = fs.readFileSync(patternsPath, 'utf-8');
    const data = JSON.parse(content);
    this.patterns = data.patterns || [];
  }

  /**
   * 搜索 patterns
   */
  searchPatterns(keywords) {
    const results = [];
    const keywordLower = keywords.toLowerCase();

    for (const pattern of this.patterns) {
      const score = this.calculateMatchScore(pattern, keywordLower);
      if (score > 0) {
        results.push({ ...pattern, matchScore: score });
      }
    }

    results.sort((a, b) => b.matchScore - a.matchScore);
    return results;
  }

  /**
   * 计算匹配分数
   */
  calculateMatchScore(pattern, keywords) {
    let score = 0;
    const name = pattern.name.toLowerCase();
    const desc = pattern.description.toLowerCase();

    if (name === keywords) score += 100;
    else if (name.includes(keywords)) score += 50;
    if (desc.includes(keywords)) score += 30;

    return score;
  }

  /**
   * 构建 URL
   */
  buildUrl(pattern, params = {}) {
    let url = pattern.samples[0];

    if (Object.keys(params).length > 0) {
      let path = pattern.pathTemplate;

      for (const [key, value] of Object.entries(params)) {
        path = path.replace(`{${key}}`, value);
      }

      url = `https://www.lixinger.com${path}`;

      const queryParams = [];
      for (const [key, value] of Object.entries(params)) {
        if (!key.startsWith('param')) {
          queryParams.push(`${key}=${encodeURIComponent(value)}`);
        }
      }

      if (queryParams.length > 0) {
        url += '?' + queryParams.join('&');
      }
    }

    return url;
  }

  /**
   * 获取摘要
   */
  getSummary() {
    const categories = {};

    for (const pattern of this.patterns) {
      const pathParts = pattern.pathTemplate.split('/').filter(p => p && !p.startsWith('{'));
      const category = pathParts[0] || 'other';

      if (!categories[category]) {
        categories[category] = [];
      }

      categories[category].push({
        name: pattern.name,
        description: pattern.description,
        urlCount: pattern.urlCount
      });
    }

    return categories;
  }
}

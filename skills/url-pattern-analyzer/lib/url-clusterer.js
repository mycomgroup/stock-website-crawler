/**
 * URL Pattern Analyzer - URL Clusterer
 * 
 * 负责URL聚类和模式识别
 */

class URLPatternAnalyzer {
  constructor() {
    // 缓存：特征提取结果
    this.featureCache = new Map();
    // 缓存：相似度计算结果
    this.similarityCache = new Map();
  }
  
  /**
   * 清除缓存
   */
  clearCache() {
    this.featureCache.clear();
    this.similarityCache.clear();
  }
  
  /**
   * 提取URL特征（带缓存）
   * @param {string|URL} url - URL字符串或URL对象
   * @returns {Object} URL特征对象
   */
  extractFeatures(url) {
    const urlString = typeof url === 'string' ? url : url.href;
    
    // 检查缓存
    if (this.featureCache.has(urlString)) {
      return this.featureCache.get(urlString);
    }
    
    // 计算特征
    const features = this._extractFeaturesImpl(urlString);
    
    // 存入缓存
    this.featureCache.set(urlString, features);
    
    return features;
  }
  
  /**
   * 提取URL特征的实际实现
   * @private
   * @param {string} urlString - URL字符串
   * @returns {Object} URL特征对象
   */
  _extractFeaturesImpl(urlString) {
    // 如果是字符串，转换为URL对象
    const urlObj = new URL(urlString);
    
    // 提取路径段（过滤空字符串）
    const pathSegments = urlObj.pathname.split('/').filter(seg => seg.length > 0);
    
    // 提取查询参数键
    const queryParams = Array.from(urlObj.searchParams.keys());
    
    // 计算路径深度
    const pathDepth = pathSegments.length;
    
    return {
      protocol: urlObj.protocol.replace(':', ''), // 移除冒号
      host: urlObj.host,
      pathSegments,
      queryParams,
      pathDepth
    };
  }
  
  /**
   * 计算URL相似度（不使用固定阈值，带缓存）
   * @param {string|URL} url1 - 第一个URL
   * @param {string|URL} url2 - 第二个URL
   * @returns {number} 相似度分数
   */
  calculateSimilarity(url1, url2) {
    const url1String = typeof url1 === 'string' ? url1 : url1.href;
    const url2String = typeof url2 === 'string' ? url2 : url2.href;
    
    // 生成缓存键（确保顺序一致）
    const cacheKey = url1String < url2String 
      ? `${url1String}|${url2String}` 
      : `${url2String}|${url1String}`;
    
    // 检查缓存
    if (this.similarityCache.has(cacheKey)) {
      return this.similarityCache.get(cacheKey);
    }
    
    // 计算相似度
    const f1 = this.extractFeatures(url1String);
    const f2 = this.extractFeatures(url2String);
    
    let score = 0;
    
    // 协议和主机必须相同，否则相似度为0
    if (f1.protocol !== f2.protocol || f1.host !== f2.host) {
      this.similarityCache.set(cacheKey, 0);
      return 0;
    }
    
    // 路径深度相同 +20分
    if (f1.pathDepth === f2.pathDepth) {
      score += 20;
    }
    
    // 路径段匹配 +10分/段
    const minPathLength = Math.min(f1.pathSegments.length, f2.pathSegments.length);
    for (let i = 0; i < minPathLength; i++) {
      if (f1.pathSegments[i] === f2.pathSegments[i]) {
        score += 10;
      }
    }
    
    // 查询参数匹配 +5分/参数
    const commonParams = f1.queryParams.filter(p => f2.queryParams.includes(p));
    score += commonParams.length * 5;
    
    // 存入缓存
    this.similarityCache.set(cacheKey, score);
    
    return score;
  }
  
  /**
   * URL聚类（基于URL正则匹配和后端渲染判断）
   * 使用优化的聚类算法，基于相似度分数进行分组
   * @param {string[]} urls - URL列表
   * @param {Object} options - 选项
   * @returns {Array} 聚类结果，每个簇包含相似的URL
   */
  clusterURLs(urls, options = {}) {
    if (!urls || urls.length === 0) {
      return [];
    }
    
    // 使用优化的单次聚类算法
    return this._clusterOptimized(urls);
  }
  
  /**
   * 优化的聚类算法
   * 使用贪心策略，避免O(n^2)的复杂度
   * @private
   * @param {string[]} urls - URL列表
   * @returns {Array} 聚类结果
   */
  _clusterOptimized(urls) {
    const clusters = [];
    const processed = new Set();
    
    // 按URL长度排序，短的URL通常更通用
    const sortedUrls = [...urls].sort((a, b) => a.length - b.length);
    
    for (const url of sortedUrls) {
      if (processed.has(url)) {
        continue;
      }
      
      // 尝试将URL加入现有簇
      let added = false;
      
      for (const cluster of clusters) {
        // 使用簇的代表URL计算相似度
        const similarity = this.calculateSimilarity(url, cluster.representative);
        
        // 动态阈值：至少要有路径深度匹配(20分) + 部分路径匹配(至少10分)
        if (similarity >= 30) {
          cluster.urls.push(url);
          processed.add(url);
          added = true;
          break;
        }
      }
      
      // 如果没有加入任何簇，创建新簇
      if (!added) {
        clusters.push({
          urls: [url],
          representative: url
        });
        processed.add(url);
      }
    }
    
    // 返回聚类结果，按簇大小降序排序
    return clusters
      .map(cluster => cluster.urls)
      .sort((a, b) => b.length - a.length);
  }
  
  /**
   * 从URL列表中选择代表URL
   * 选择路径最短且最通用的URL作为代表
   * @private
   * @param {string[]} urls - URL列表
   * @returns {string} 代表URL
   */
  _selectRepresentative(urls) {
    if (urls.length === 1) {
      return urls[0];
    }
    
    // 选择路径最短的URL（通常更通用）
    return urls.reduce((shortest, current) => {
      const shortestFeatures = this.extractFeatures(shortest);
      const currentFeatures = this.extractFeatures(current);
      
      // 优先选择路径深度较小的
      if (currentFeatures.pathDepth < shortestFeatures.pathDepth) {
        return current;
      } else if (currentFeatures.pathDepth === shortestFeatures.pathDepth) {
        // 路径深度相同，选择查询参数较少的
        if (currentFeatures.queryParams.length < shortestFeatures.queryParams.length) {
          return current;
        }
      }
      
      return shortest;
    });
  }
  
  /**
   * 生成正则表达式
   * 分析URL组，识别固定部分和变化部分，生成匹配所有URL的正则表达式
   * @param {string[]} urlGroup - URL组
   * @returns {Object} 包含正则表达式和模板信息的对象
   */
  generatePattern(urlGroup) {
    if (!urlGroup || urlGroup.length === 0) {
      throw new Error('URL group cannot be empty');
    }
    
    // 如果只有一个URL，直接转义并返回
    if (urlGroup.length === 1) {
      const url = new URL(urlGroup[0]);
      return {
        pattern: this._escapeRegex(urlGroup[0]),
        pathTemplate: url.pathname,
        queryParams: Array.from(url.searchParams.keys())
      };
    }
    
    // 解析所有URL
    const parsedUrls = urlGroup.map(url => new URL(url));
    
    // 提取公共的协议和主机
    const protocol = parsedUrls[0].protocol;
    const host = parsedUrls[0].host;
    
    // 验证所有URL具有相同的协议和主机
    const allSameOrigin = parsedUrls.every(url => 
      url.protocol === protocol && url.host === host
    );
    
    if (!allSameOrigin) {
      throw new Error('All URLs in the group must have the same protocol and host');
    }
    
    // 分析路径模式
    const pathPattern = this._generatePathPattern(parsedUrls);
    
    // 分析查询参数模式
    const queryPattern = this._generateQueryPattern(parsedUrls);
    
    // 组合完整的正则表达式
    const fullPattern = `^${this._escapeRegex(protocol)}//${this._escapeRegex(host)}${pathPattern}${queryPattern}$`;
    
    // 生成路径模板（用于显示）
    const pathTemplate = this._generatePathTemplate(parsedUrls);
    
    // 提取所有查询参数键
    const allQueryParams = new Set();
    parsedUrls.forEach(url => {
      url.searchParams.forEach((value, key) => {
        allQueryParams.add(key);
      });
    });
    
    return {
      pattern: fullPattern,
      pathTemplate: pathTemplate,
      queryParams: Array.from(allQueryParams)
    };
  }
  
  /**
   * 生成路径部分的正则表达式
   * @private
   * @param {URL[]} urls - 解析后的URL对象数组
   * @returns {string} 路径正则表达式
   */
  _generatePathPattern(urls) {
    // 提取所有路径段
    const pathSegmentsList = urls.map(url => 
      url.pathname.split('/').filter(seg => seg.length > 0)
    );
    
    // 确保所有路径具有相同的段数
    const segmentCount = pathSegmentsList[0].length;
    const allSameLength = pathSegmentsList.every(segments => segments.length === segmentCount);
    
    if (!allSameLength) {
      // 如果路径长度不同，使用更宽松的匹配
      return '/.*';
    }
    
    // 逐段分析，识别固定段和变化段
    const patternSegments = [];
    for (let i = 0; i < segmentCount; i++) {
      const segmentValues = pathSegmentsList.map(segments => segments[i]);
      const uniqueValues = new Set(segmentValues);
      
      if (uniqueValues.size === 1) {
        // 固定段：所有URL在此位置的值相同
        patternSegments.push(this._escapeRegex(segmentValues[0]));
      } else {
        // 变化段：使用捕获组匹配任意非斜杠字符
        patternSegments.push('([^/]+)');
      }
    }
    
    return '/' + patternSegments.join('/');
  }
  
  /**
   * 生成查询参数部分的正则表达式
   * @private
   * @param {URL[]} urls - 解析后的URL对象数组
   * @returns {string} 查询参数正则表达式
   */
  _generateQueryPattern(urls) {
    // 收集所有查询参数键
    const allParamKeys = new Set();
    urls.forEach(url => {
      url.searchParams.forEach((value, key) => {
        allParamKeys.add(key);
      });
    });
    
    if (allParamKeys.size === 0) {
      // 没有查询参数
      return '';
    }
    
    // 检查是否所有URL都有相同的参数键
    const firstParamKeys = Array.from(urls[0].searchParams.keys()).sort();
    const allSameParams = urls.every(url => {
      const paramKeys = Array.from(url.searchParams.keys()).sort();
      return JSON.stringify(paramKeys) === JSON.stringify(firstParamKeys);
    });
    
    if (allSameParams && firstParamKeys.length > 0) {
      // 所有URL具有相同的参数键，生成精确的参数模式
      const paramPatterns = firstParamKeys.map(key => 
        `${this._escapeRegex(key)}=([^&]+)`
      );
      return '\\?' + paramPatterns.join('&');
    } else {
      // 参数键不同，使用宽松匹配
      return '(\\?.*)?';
    }
  }
  
  /**
   * 生成路径模板（用于显示）
   * @private
   * @param {URL[]} urls - 解析后的URL对象数组
   * @returns {string} 路径模板
   */
  _generatePathTemplate(urls) {
    const pathSegmentsList = urls.map(url => 
      url.pathname.split('/').filter(seg => seg.length > 0)
    );
    
    const segmentCount = pathSegmentsList[0].length;
    const allSameLength = pathSegmentsList.every(segments => segments.length === segmentCount);
    
    if (!allSameLength) {
      return urls[0].pathname;
    }
    
    // 逐段分析，固定段保留，变化段用{param}表示
    const templateSegments = [];
    for (let i = 0; i < segmentCount; i++) {
      const segmentValues = pathSegmentsList.map(segments => segments[i]);
      const uniqueValues = new Set(segmentValues);
      
      if (uniqueValues.size === 1) {
        // 固定段
        templateSegments.push(segmentValues[0]);
      } else {
        // 变化段
        templateSegments.push(`{param${i}}`);
      }
    }
    
    return '/' + templateSegments.join('/');
  }
  
  /**
   * 转义正则表达式特殊字符
   * @private
   * @param {string} str - 要转义的字符串
   * @returns {string} 转义后的字符串
   */
  _escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }
}

module.exports = URLPatternAnalyzer;

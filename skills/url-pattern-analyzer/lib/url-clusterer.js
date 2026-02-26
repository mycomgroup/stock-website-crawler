/**
 * URL Pattern Analyzer - URL Clusterer
 * 
 * 负责URL聚类和模式识别
 */

class URLPatternAnalyzer {
  constructor(options = {}) {
    // 缓存：特征提取结果
    this.featureCache = new Map();
    // 缓存：相似度计算结果
    this.similarityCache = new Map();
    
    // 细分控制参数
    this.refineMaxValues = options.refineMaxValues || 8;
    this.refineMinCount = options.refineMinCount || 10;
    this.refineMinGroups = options.refineMinGroups || 2;
    
    // 严格模式参数
    this.strictTopN = options.strictTopN || 0;  // 默认不启用
    this.strictMatchRatio = options.strictMatchRatio || 0.8;
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
    
    // 路径深度必须相同，否则相似度为0
    if (f1.pathDepth !== f2.pathDepth) {
      this.similarityCache.set(cacheKey, 0);
      return 0;
    }
    
    // 路径深度相同 +20分
    score += 20;
    
    // 路径段匹配分析：需要识别固定段和变化段
    // 策略：如果某个位置的段完全相同，认为是固定段；否则是变化段
    // 只有当所有固定段都匹配时，才认为是同一模式
    let matchedSegments = 0;
    let totalSegments = f1.pathSegments.length;
    
    for (let i = 0; i < totalSegments; i++) {
      if (f1.pathSegments[i] === f2.pathSegments[i]) {
        matchedSegments++;
        score += 15; // 每个匹配的段 +15分
      }
    }
    
    // 如果匹配的段数太少（少于50%），认为不是同一模式
    if (matchedSegments < totalSegments * 0.5) {
      this.similarityCache.set(cacheKey, 0);
      return 0;
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
        
        // 新的阈值策略：
        // - 相似度必须 > 0（说明路径深度相同且至少50%的段匹配）
        // - 基础分20分（路径深度） + 至少50%段匹配（至少15分/段）
        // 例如：6层路径需要至少3层匹配 = 20 + 3*15 = 65分
        if (similarity > 0) {
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
    
    // 后处理：细分包含"半固定段"的簇
    const refinedClusters = [];
    for (const cluster of clusters) {
      const subClusters = this._refineClusterBySemiFixedSegments(cluster);
      refinedClusters.push(...subClusters);
    }
    
    // 严格模式：对最大的N个簇应用更严格的细分规则
    let finalClusters = refinedClusters;
    if (this.strictTopN > 0) {
      finalClusters = this._applyStrictRefinement(refinedClusters);
    }
    
    // 返回聚类结果，按簇大小降序排序
    return finalClusters
      .map(cluster => cluster.urls)
      .sort((a, b) => b.length - a.length);
  }
  
  /**
   * 对最大的N个簇应用严格细分规则
   * @private
   * @param {Array} clusters - 簇对象数组
   * @returns {Array} 细分后的簇对象数组
   */
  _applyStrictRefinement(clusters) {
    // 按大小排序
    const sortedClusters = [...clusters].sort((a, b) => b.urls.length - a.urls.length);
    
    // 对前N个最大的簇应用严格规则
    const strictClusters = sortedClusters.slice(0, this.strictTopN);
    const normalClusters = sortedClusters.slice(this.strictTopN);
    
    const refinedStrictClusters = [];
    for (const cluster of strictClusters) {
      const subClusters = this._strictRefineCluster(cluster);
      refinedStrictClusters.push(...subClusters);
    }
    
    return [...refinedStrictClusters, ...normalClusters];
  }
  
  /**
   * 严格细分单个簇
   * 要求每个路径段要么全部固定，要么只有一个变量
   * @private
   * @param {Object} cluster - 簇对象
   * @returns {Array} 细分后的簇对象数组
   */
  _strictRefineCluster(cluster) {
    const urls = cluster.urls;
    
    if (urls.length <= 1) {
      return [cluster];
    }
    
    // 解析所有URL
    const parsedUrls = urls.map(url => new URL(url));
    const pathSegmentsList = parsedUrls.map(url => 
      url.pathname.split('/').filter(seg => seg.length > 0)
    );
    
    const segmentCount = pathSegmentsList[0].length;
    
    // 计算每个段的固定比例
    const segmentFixedRatios = [];
    for (let i = 0; i < segmentCount; i++) {
      const segmentValues = pathSegmentsList.map(segments => segments[i]);
      const uniqueValues = new Set(segmentValues);
      const fixedRatio = 1 - (uniqueValues.size - 1) / urls.length;
      segmentFixedRatios.push({
        position: i,
        fixedRatio: fixedRatio,
        uniqueCount: uniqueValues.size
      });
    }
    
    // 计算整体固定比例
    const avgFixedRatio = segmentFixedRatios.reduce((sum, s) => sum + s.fixedRatio, 0) / segmentCount;
    
    // 如果整体固定比例 >= strictMatchRatio，不需要细分
    if (avgFixedRatio >= this.strictMatchRatio) {
      return [cluster];
    }
    
    // 找出变化最大的段（固定比例最低的段）
    const mostVariableSegment = segmentFixedRatios
      .filter(s => s.uniqueCount > 1 && s.uniqueCount <= 10) // 只考虑有限变化的段
      .sort((a, b) => a.fixedRatio - b.fixedRatio)[0];
    
    if (!mostVariableSegment) {
      return [cluster];
    }
    
    // 按该段的值分组
    const subClusters = new Map();
    for (let i = 0; i < urls.length; i++) {
      const url = urls[i];
      const segments = pathSegmentsList[i];
      const segmentValue = segments[mostVariableSegment.position];
      
      if (!subClusters.has(segmentValue)) {
        subClusters.set(segmentValue, []);
      }
      subClusters.get(segmentValue).push(url);
    }
    
    // 只保留大小 >= 10 的子簇
    const validSubClusters = Array.from(subClusters.values())
      .filter(urlList => urlList.length >= 10)
      .map(urlList => ({
        urls: urlList,
        representative: urlList[0]
      }));
    
    // 如果没有有效的子簇，返回原簇
    if (validSubClusters.length === 0) {
      return [cluster];
    }
    
    return validSubClusters;
  }
  
  /**
   * 根据"半固定段"细分簇
   * 如果某个变化段只有少数几个值（≤5个），按这些值进一步分组
   * @private
   * @param {Object} cluster - URL簇对象 {urls: [], representative: ''}
   * @returns {Array} 细分后的簇对象数组
   */
  _refineClusterBySemiFixedSegments(cluster) {
    const urls = cluster.urls;
    
    if (urls.length <= 1) {
      return [cluster];
    }
    
    // 解析所有URL
    const parsedUrls = urls.map(url => new URL(url));
    const pathSegmentsList = parsedUrls.map(url => 
      url.pathname.split('/').filter(seg => seg.length > 0)
    );
    
    const segmentCount = pathSegmentsList[0].length;
    
    // 找出所有"半固定段"（唯一值数量 > 1 且 ≤ 5）
    const semiFixedSegments = [];
    for (let i = 0; i < segmentCount; i++) {
      const segmentValues = pathSegmentsList.map(segments => segments[i]);
      const uniqueValues = new Set(segmentValues);
      
      // 统计每个值的数量
      const valueCounts = new Map();
      segmentValues.forEach(val => {
        valueCounts.set(val, (valueCounts.get(val) || 0) + 1);
      });
      
      // 条件：
      // 1. 唯一值数量 > 1 且 ≤ refineMaxValues（可配置）
      // 2. 至少有refineMinGroups个值的出现次数 ≥ refineMinCount（可配置）
      const countsArray = Array.from(valueCounts.values());
      const largeGroups = countsArray.filter(count => count >= this.refineMinCount);
      
      if (uniqueValues.size > 1 && uniqueValues.size <= this.refineMaxValues && largeGroups.length >= this.refineMinGroups) {
        semiFixedSegments.push({
          position: i,
          values: Array.from(uniqueValues),
          valueCounts: valueCounts,
          largeGroupCount: largeGroups.length
        });
      }
    }
    
    // 如果没有半固定段，返回原簇
    if (semiFixedSegments.length === 0) {
      return [cluster];
    }
    
    // 选择有最多大组的半固定段进行分组
    const targetSegment = semiFixedSegments.sort((a, b) => b.largeGroupCount - a.largeGroupCount)[0];
    const subClusters = new Map();
    
    for (let i = 0; i < urls.length; i++) {
      const url = urls[i];
      const segments = pathSegmentsList[i];
      const segmentValue = segments[targetSegment.position];
      
      if (!subClusters.has(segmentValue)) {
        subClusters.set(segmentValue, []);
      }
      subClusters.get(segmentValue).push(url);
    }
    
    // 返回所有子簇对象
    return Array.from(subClusters.values()).map(urlList => ({
      urls: urlList,
      representative: urlList[0]
    }));
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

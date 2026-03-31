/**
 * HAR Parser - 解析 HAR 文件提取 API 信息
 */

import fs from 'fs';

export class HARParser {
  constructor(harPath) {
    this.harPath = harPath;
    this.har = null;
    this.entries = [];
  }

  /**
   * 加载 HAR 文件
   */
  load() {
    try {
      const content = fs.readFileSync(this.harPath, 'utf8');
      this.har = JSON.parse(content);
      this.entries = this.har.log?.entries || [];
      return true;
    } catch (error) {
      console.error(`加载 HAR 文件失败: ${error.message}`);
      return false;
    }
  }

  /**
   * 提取所有数据接口
   */
  extractDataAPIs() {
    return this.entries.filter(entry => {
      const url = entry.request.url;
      const mimeType = entry.response?.content?.mimeType || '';
      
      return this.isDataAPI(url, mimeType, entry);
    });
  }

  /**
   * 判断是否为数据接口
   */
  isDataAPI(url, mimeType, entry) {
    // JSON 响应
    if (mimeType.includes('json')) return true;
    
    // API 路径特征
    const apiPatterns = [
      '/api/', '/data/', '/v1/', '/v2/', '/v3/',
      '/rest/', '/service/', '/query/'
    ];
    if (apiPatterns.some(pattern => url.includes(pattern))) return true;
    
    // GraphQL
    if (this.isGraphQL(entry)) return true;
    
    // 排除静态资源
    const staticExtensions = [
      '.js', '.css', '.png', '.jpg', '.jpeg', '.gif', 
      '.svg', '.woff', '.woff2', '.ttf', '.ico'
    ];
    if (staticExtensions.some(ext => url.toLowerCase().endsWith(ext))) {
      return false;
    }
    
    return false;
  }

  /**
   * 识别 GraphQL 请求
   */
  isGraphQL(entry) {
    const url = entry.request.url;
    const postData = entry.request.postData?.text || '';
    
    return url.includes('graphql') || 
           postData.includes('"query"') ||
           postData.includes('"mutation"');
  }

  /**
   * 提取请求详情
   */
  extractRequestDetails(entry) {
    const req = entry.request;
    const res = entry.response;
    
    return {
      method: req.method,
      url: req.url,
      headers: this.cleanHeaders(req.headers),
      queryParams: this.extractQueryParams(req),
      postData: req.postData?.text,
      status: res.status,
      responseHeaders: this.cleanHeaders(res.headers),
      responseBody: res.content.text,
      mimeType: res.content.mimeType,
      time: entry.time,
      timestamp: entry.startedDateTime
    };
  }

  /**
   * 清理 headers（移除不必要的）
   */
  cleanHeaders(headers) {
    const exclude = [
      'content-length', 'connection', 'accept-encoding',
      'content-encoding', 'transfer-encoding'
    ];
    
    const cleaned = {};
    headers.forEach(h => {
      const name = h.name.toLowerCase();
      if (!exclude.includes(name)) {
        cleaned[h.name] = h.value;
      }
    });
    
    return cleaned;
  }

  /**
   * 提取查询参数
   */
  extractQueryParams(request) {
    return request.queryString.reduce((obj, param) => {
      obj[param.name] = param.value;
      return obj;
    }, {});
  }

  /**
   * 分类接口
   */
  categorizeAPIs() {
    const apis = this.extractDataAPIs();
    
    const rest = [];
    const graphql = [];
    
    apis.forEach(entry => {
      if (this.isGraphQL(entry)) {
        graphql.push(entry);
      } else {
        rest.push(entry);
      }
    });
    
    return {
      rest,
      graphql,
      total: apis.length,
      restCount: rest.length,
      graphqlCount: graphql.length
    };
  }

  /**
   * 按域名分组
   */
  groupByDomain() {
    const apis = this.extractDataAPIs();
    const groups = {};
    
    apis.forEach(entry => {
      const url = new URL(entry.request.url);
      const domain = url.hostname;
      
      if (!groups[domain]) {
        groups[domain] = [];
      }
      groups[domain].push(entry);
    });
    
    return groups;
  }

  /**
   * 按路径模式分组
   */
  groupByPathPattern() {
    const apis = this.extractDataAPIs();
    const groups = {};
    
    apis.forEach(entry => {
      const url = new URL(entry.request.url);
      const pattern = this.extractPathPattern(url.pathname);
      
      if (!groups[pattern]) {
        groups[pattern] = [];
      }
      groups[pattern].push(entry);
    });
    
    return groups;
  }

  /**
   * 提取路径模式（将数字替换为占位符）
   */
  extractPathPattern(pathname) {
    return pathname.replace(/\/\d+/g, '/:id')
                   .replace(/\/[a-f0-9]{24}/g, '/:id')  // MongoDB ObjectId
                   .replace(/\/[a-f0-9-]{36}/g, '/:uuid'); // UUID
  }

  /**
   * 获取统计信息
   */
  getStats() {
    const all = this.entries;
    const apis = this.extractDataAPIs();
    
    const methods = {};
    const statusCodes = {};
    
    apis.forEach(entry => {
      const method = entry.request.method;
      methods[method] = (methods[method] || 0) + 1;
      
      const status = entry.response.status;
      statusCodes[status] = (statusCodes[status] || 0) + 1;
    });
    
    return {
      totalRequests: all.length,
      apiRequests: apis.length,
      methods,
      statusCodes,
      domains: Object.keys(this.groupByDomain()).length
    };
  }

  /**
   * 检测签名参数
   */
  detectSignature(entry) {
    const details = this.extractRequestDetails(entry);
    const signatureKeys = [
      'sign', 'signature', 'x-sign', 'x-signature',
      'auth-sign', 'token', 'access-token'
    ];
    
    // 检查 headers
    for (const key of signatureKeys) {
      if (details.headers[key] || details.headers[key.toLowerCase()]) {
        return {
          found: true,
          location: 'header',
          key,
          value: details.headers[key] || details.headers[key.toLowerCase()]
        };
      }
    }
    
    // 检查查询参数
    for (const key of signatureKeys) {
      if (details.queryParams[key]) {
        return {
          found: true,
          location: 'query',
          key,
          value: details.queryParams[key]
        };
      }
    }
    
    return { found: false };
  }

  /**
   * 导出为 JSON
   */
  exportToJSON(outputPath) {
    const apis = this.extractDataAPIs();
    const data = {
      metadata: {
        source: this.harPath,
        extractedAt: new Date().toISOString(),
        stats: this.getStats()
      },
      apis: apis.map(entry => this.extractRequestDetails(entry))
    };
    
    fs.writeFileSync(outputPath, JSON.stringify(data, null, 2));
    console.log(`已导出 ${apis.length} 个 API 到 ${outputPath}`);
  }
}

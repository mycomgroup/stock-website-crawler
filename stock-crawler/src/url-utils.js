/**
 * URL工具函数模块
 * 提供URL转换、过滤和模式匹配功能
 */

/**
 * 验证URL是否有效（检查查询参数值）
 * @param {string} url - 要验证的URL
 * @returns {boolean} URL是否有效
 */
function isValidUrl(url) {
  try {
    const urlObj = new URL(url);
    
    // 检查所有查询参数的值
    for (const [key, value] of urlObj.searchParams.entries()) {
      // 过滤掉无效的参数值
      if (value === 'undefined' || value === 'null' || value.trim() === '') {
        return false;
      }
    }
    
    return true;
  } catch (error) {
    // URL格式无效
    return false;
  }
}

/**
 * 将相对URL转换为绝对URL
 * @param {string} url - 相对或绝对URL
 * @param {string} baseUrl - 基础URL
 * @returns {string} 绝对URL
 */
function toAbsoluteUrl(url, baseUrl) {
  try {
    // 如果url已经是绝对URL，直接返回
    if (url.startsWith('http://') || url.startsWith('https://')) {
      return url;
    }
    
    // 使用URL构造函数处理相对URL
    const absoluteUrl = new URL(url, baseUrl);
    return absoluteUrl.href;
  } catch (error) {
    // 如果转换失败，返回原URL
    return url;
  }
}

/**
 * 检查URL是否匹配给定的模式
 * @param {string} url - 要检查的URL
 * @param {string} pattern - 正则表达式模式字符串
 * @returns {boolean} 是否匹配
 */
function matchesPattern(url, pattern) {
  try {
    const regex = new RegExp(pattern);
    return regex.test(url);
  } catch (error) {
    // 如果正则表达式无效，返回false
    return false;
  }
}

/**
 * 根据规则过滤URL列表
 * @param {string[]} urls - URL数组
 * @param {Object} urlRules - 过滤规则 {include: string[], exclude: string[]}
 * @returns {string[]} 过滤后的URL数组
 */
function filterLinks(urls, urlRules) {
  if (!urls || !Array.isArray(urls)) {
    return [];
  }
  
  const { include = [], exclude = [] } = urlRules || {};
  
  return urls.filter(url => {
    // 首先验证URL的有效性
    if (!isValidUrl(url)) {
      console.warn(`Filtered out invalid URL: ${url}`);
      return false;
    }
    
    // 如果没有include规则，默认包含所有URL
    const matchesInclude = include.length === 0 || 
      include.some(pattern => matchesPattern(url, pattern));
    
    // 检查是否匹配任何exclude规则
    const matchesExclude = exclude.length > 0 && 
      exclude.some(pattern => matchesPattern(url, pattern));
    
    // 必须匹配include且不匹配exclude
    return matchesInclude && !matchesExclude;
  });
}

export { toAbsoluteUrl, matchesPattern, filterLinks, isValidUrl };

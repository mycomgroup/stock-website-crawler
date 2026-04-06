import { ProxyAgent, fetch as undiciFetch } from 'undici';
import { ENV } from '../load-env.js';

/**
 * 创建支持代理的 fetch 函数
 */
export function createProxyFetch() {
  const proxyUrl = ENV.HTTPS_PROXY || ENV.HTTP_PROXY;
  
  if (proxyUrl) {
    console.log(`🔌 使用代理: ${proxyUrl}`);
    const dispatcher = new ProxyAgent(proxyUrl);
    
    return (url, options = {}) => {
      return undiciFetch(url, {
        ...options,
        dispatcher
      });
    };
  }
  
  // No proxy, use native fetch
  return fetch;
}

export const proxyFetch = createProxyFetch();

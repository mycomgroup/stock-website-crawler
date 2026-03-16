import BaseParser from './base-parser.js';

/**
 * Google Discovery Parser - 解析 Google Discovery REST 文档（JSON）
 */
class GoogleDiscoveryParser extends BaseParser {
  matches(url) {
    return /^https?:\/\/financialservices\.googleapis\.com\/\$discovery\/rest\?version=v1/.test(url);
  }

  getPriority() {
    return 120;
  }

  async parse(page, url) {
    try {
      const jsonText = await page.evaluate(() => {
        const pre = document.querySelector('pre');
        if (pre?.innerText) return pre.innerText;
        return document.body?.innerText || '';
      });

      const discovery = JSON.parse(jsonText);
      const methods = this.extractMethods(discovery);

      return {
        type: 'google-discovery-doc',
        url,
        title: `${discovery.title || 'Google API'} Discovery (${discovery.version || 'unknown'})`,
        description: discovery.description || '',
        serviceName: discovery.name || '',
        version: discovery.version || '',
        rootUrl: discovery.rootUrl || '',
        servicePath: discovery.servicePath || '',
        mtlsRootUrl: discovery.mtlsRootUrl || '',
        batchPath: discovery.batchPath || '',
        revision: discovery.revision || '',
        entryPoints: {
          discoveryUrl: url,
          rootUrl: discovery.rootUrl || '',
          servicePath: discovery.servicePath || '',
          batchPath: discovery.batchPath || ''
        },
        urlRuleInterfaces: methods,
        rawContent: jsonText.slice(0, 15000)
      };
    } catch (error) {
      console.error('Failed to parse Google Discovery doc:', error.message);
      return {
        type: 'google-discovery-doc',
        url,
        title: 'Google Discovery Document',
        description: '解析失败',
        entryPoints: {},
        urlRuleInterfaces: [],
        rawContent: ''
      };
    }
  }

  extractMethods(discovery) {
    const methods = [];

    const joinUrl = (rootUrl, servicePath, path) => {
      const root = (rootUrl || '').replace(/\/+$/, '');
      const service = (servicePath || '').replace(/^\/+/, '').replace(/\/+$/, '');
      const methodPath = (path || '').replace(/^\/+/, '');
      const mergedPath = [service, methodPath].filter(Boolean).join('/');
      return mergedPath ? `${root}/${mergedPath}` : root;
    };

    const walkResource = (resource, resourcePath = []) => {
      if (resource.methods) {
        for (const [methodName, methodDef] of Object.entries(resource.methods)) {
          const parameterNames = Object.keys(methodDef.parameters || {});
          methods.push({
            resource: resourcePath.join('.') || 'root',
            methodName,
            id: methodDef.id || '',
            httpMethod: methodDef.httpMethod || '',
            path: methodDef.path || '',
            flatPath: methodDef.flatPath || '',
            fullUrlTemplate: joinUrl(discovery.rootUrl, discovery.servicePath, methodDef.path),
            supportsMediaDownload: !!methodDef.supportsMediaDownload,
            supportsSubscription: !!methodDef.supportsSubscription,
            parameterNames,
            description: methodDef.description || ''
          });
        }
      }

      if (resource.resources) {
        for (const [subResourceName, subResourceDef] of Object.entries(resource.resources)) {
          walkResource(subResourceDef, [...resourcePath, subResourceName]);
        }
      }
    };

    if (discovery.resources) {
      for (const [resourceName, resourceDef] of Object.entries(discovery.resources)) {
        walkResource(resourceDef, [resourceName]);
      }
    }

    return methods;
  }
}

export default GoogleDiscoveryParser;

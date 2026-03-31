/**
 * Request Generator - 生成各种语言的请求代码
 */

export class RequestGenerator {
  constructor(harParser) {
    this.parser = harParser;
  }

  /**
   * 生成 Python requests 代码
   */
  generatePythonCode(entry) {
    const details = this.parser.extractRequestDetails(entry);
    const method = details.method.toLowerCase();
    
    let code = `#!/usr/bin/env python3\n`;
    code += `# -*- coding: utf-8 -*-\n`;
    code += `"""${this.extractAPIName(details.url)}"""\n\n`;
    code += `import requests\n`;
    code += `import json\n\n`;
    
    // Headers
    code += `headers = ${this.formatPythonDict(details.headers)}\n\n`;
    
    // URL
    code += `url = "${details.url}"\n\n`;
    
    // 请求
    if (method === 'get') {
      code += `response = requests.get(url, headers=headers)\n`;
    } else if (method === 'post') {
      if (details.postData) {
        try {
          const data = JSON.parse(details.postData);
          code += `data = ${this.formatPythonDict(data)}\n\n`;
          code += `response = requests.post(url, headers=headers, json=data)\n`;
        } catch {
          code += `data = '''${details.postData}'''\n\n`;
          code += `response = requests.post(url, headers=headers, data=data)\n`;
        }
      } else {
        code += `response = requests.post(url, headers=headers)\n`;
      }
    } else {
      code += `response = requests.${method}(url, headers=headers)\n`;
    }
    
    // 处理响应
    code += `\n`;
    code += `if response.status_code == 200:\n`;
    code += `    data = response.json()\n`;
    code += `    print(json.dumps(data, indent=2, ensure_ascii=False))\n`;
    code += `else:\n`;
    code += `    print(f"Error: {response.status_code}")\n`;
    code += `    print(response.text)\n`;
    
    return code;
  }

  /**
   * 生成 Node.js axios 代码
   */
  generateNodeCode(entry) {
    const details = this.parser.extractRequestDetails(entry);
    const method = details.method.toLowerCase();
    
    let code = `/**\n * ${this.extractAPIName(details.url)}\n */\n\n`;
    code += `import axios from 'axios';\n\n`;
    
    // 配置
    code += `const config = {\n`;
    code += `  method: '${method}',\n`;
    code += `  url: '${details.url}',\n`;
    code += `  headers: ${JSON.stringify(details.headers, null, 2)}\n`;
    
    if (details.postData) {
      try {
        const data = JSON.parse(details.postData);
        code += `,\n  data: ${JSON.stringify(data, null, 2)}\n`;
      } catch {
        code += `,\n  data: ${JSON.stringify(details.postData, null, 2)}\n`;
      }
    }
    
    code += `};\n\n`;
    
    // 请求
    code += `axios(config)\n`;
    code += `  .then(response => {\n`;
    code += `    console.log(JSON.stringify(response.data, null, 2));\n`;
    code += `  })\n`;
    code += `  .catch(error => {\n`;
    code += `    console.error('Error:', error.message);\n`;
    code += `    if (error.response) {\n`;
    code += `      console.error('Status:', error.response.status);\n`;
    code += `      console.error('Data:', error.response.data);\n`;
    code += `    }\n`;
    code += `  });\n`;
    
    return code;
  }

  /**
   * 生成 curl 命令
   */
  generateCurlCommand(entry) {
    const details = this.parser.extractRequestDetails(entry);
    
    let cmd = `curl -X ${details.method} '${details.url}'`;
    
    // Headers
    Object.entries(details.headers).forEach(([key, value]) => {
      cmd += ` \\\n  -H '${key}: ${value}'`;
    });
    
    // Data
    if (details.postData) {
      cmd += ` \\\n  -d '${details.postData.replace(/'/g, "\\'")}'`;
    }
    
    return cmd;
  }

  /**
   * 生成 JavaScript fetch 代码
   */
  generateFetchCode(entry) {
    const details = this.parser.extractRequestDetails(entry);
    const method = details.method.toUpperCase();
    
    let code = `/**\n * ${this.extractAPIName(details.url)}\n */\n\n`;
    
    code += `const url = '${details.url}';\n\n`;
    
    code += `const options = {\n`;
    code += `  method: '${method}',\n`;
    code += `  headers: ${JSON.stringify(details.headers, null, 2)}\n`;
    
    if (details.postData) {
      code += `,\n  body: JSON.stringify(${details.postData})\n`;
    }
    
    code += `};\n\n`;
    
    code += `fetch(url, options)\n`;
    code += `  .then(response => response.json())\n`;
    code += `  .then(data => console.log(data))\n`;
    code += `  .catch(error => console.error('Error:', error));\n`;
    
    return code;
  }

  /**
   * 批量生成代码
   */
  generateAll(format = 'python') {
    const apis = this.parser.extractDataAPIs();
    
    const generators = {
      python: this.generatePythonCode.bind(this),
      node: this.generateNodeCode.bind(this),
      curl: this.generateCurlCommand.bind(this),
      fetch: this.generateFetchCode.bind(this)
    };
    
    const generator = generators[format];
    if (!generator) {
      throw new Error(`不支持的格式: ${format}`);
    }
    
    return apis.map((entry, index) => {
      const details = this.parser.extractRequestDetails(entry);
      return {
        index: index + 1,
        url: details.url,
        method: details.method,
        name: this.extractAPIName(details.url),
        code: generator(entry)
      };
    });
  }

  /**
   * 提取 API 名称
   */
  extractAPIName(url) {
    try {
      const urlObj = new URL(url);
      const pathname = urlObj.pathname;
      const parts = pathname.split('/').filter(p => p);
      return parts[parts.length - 1] || 'api';
    } catch {
      return 'api';
    }
  }

  /**
   * 格式化为 Python 字典
   */
  formatPythonDict(obj) {
    return JSON.stringify(obj, null, 2)
      .replace(/"/g, "'")
      .replace(/: /g, ': ')
      .replace(/true/g, 'True')
      .replace(/false/g, 'False')
      .replace(/null/g, 'None');
  }

  /**
   * 生成 API 类（Python）
   */
  generatePythonClass(apis) {
    let code = `#!/usr/bin/env python3\n`;
    code += `# -*- coding: utf-8 -*-\n`;
    code += `"""API Client"""\n\n`;
    code += `import requests\n`;
    code += `from typing import Dict, Any, Optional\n\n\n`;
    
    code += `class APIClient:\n`;
    code += `    def __init__(self, base_url: str, headers: Optional[Dict] = None):\n`;
    code += `        self.base_url = base_url\n`;
    code += `        self.headers = headers or {}\n`;
    code += `        self.session = requests.Session()\n`;
    code += `        self.session.headers.update(self.headers)\n\n`;
    
    apis.forEach((api, index) => {
      const details = this.parser.extractRequestDetails(api);
      const methodName = this.generateMethodName(details.url);
      const method = details.method.toLowerCase();
      
      code += `    def ${methodName}(self, **kwargs) -> Dict[str, Any]:\n`;
      code += `        """${details.url}"""\n`;
      code += `        url = "${details.url}"\n`;
      code += `        response = self.session.${method}(url, **kwargs)\n`;
      code += `        response.raise_for_status()\n`;
      code += `        return response.json()\n\n`;
    });
    
    return code;
  }

  /**
   * 生成方法名
   */
  generateMethodName(url) {
    try {
      const urlObj = new URL(url);
      const pathname = urlObj.pathname;
      const parts = pathname.split('/').filter(p => p && !/^\d+$/.test(p));
      return parts.join('_').replace(/[^a-zA-Z0-9_]/g, '_').toLowerCase();
    } catch {
      return 'api_call';
    }
  }
}

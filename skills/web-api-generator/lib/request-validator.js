/**
 * Request Validator - 验证直接请求是否可行
 */

export class RequestValidator {
  constructor() {
    this.results = [];
  }

  /**
   * 测试单个请求
   */
  async testDirectRequest(apiInfo) {
    try {
      const response = await fetch(apiInfo.url, {
        method: apiInfo.method,
        headers: apiInfo.headers,
        body: apiInfo.postData,
        signal: AbortSignal.timeout(10000)
      });
      
      const result = {
        success: true,
        url: apiInfo.url,
        status: response.status,
        canBypassBrowser: response.ok,
        responseTime: 0
      };
      
      this.results.push(result);
      return result;
      
    } catch (error) {
      const result = {
        success: false,
        url: apiInfo.url,
        error: error.message,
        canBypassBrowser: false,
        reason: this.diagnoseFailure(error)
      };
      
      this.results.push(result);
      return result;
    }
  }

  /**
   * 诊断失败原因
   */
  diagnoseFailure(error) {
    const message = error.message.toLowerCase();
    
    if (message.includes('403') || message.includes('forbidden')) {
      return 'Anti-bot protection detected (403 Forbidden)';
    }
    
    if (message.includes('401') || message.includes('unauthorized')) {
      return 'Authentication required (401 Unauthorized)';
    }
    
    if (message.includes('cors')) {
      return 'CORS policy blocking request';
    }
    
    if (message.includes('timeout')) {
      return 'Request timeout';
    }
    
    if (message.includes('network')) {
      return 'Network error';
    }
    
    return 'Unknown error';
  }

  /**
   * 批量验证
   */
  async validateAll(apis, options = {}) {
    const { maxConcurrent = 3, delay = 1000 } = options;
    
    console.log(`开始验证 ${apis.length} 个 API...`);
    
    const results = [];
    
    for (let i = 0; i < apis.length; i += maxConcurrent) {
      const batch = apis.slice(i, i + maxConcurrent);
      
      const batchResults = await Promise.all(
        batch.map(api => this.testDirectRequest(api))
      );
      
      results.push(...batchResults);
      
      // 显示进度
      const progress = Math.min(i + maxConcurrent, apis.length);
      console.log(`进度: ${progress}/${apis.length}`);
      
      // 延迟避免请求过快
      if (i + maxConcurrent < apis.length) {
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
    
    return this.generateReport(results);
  }

  /**
   * 生成验证报告
   */
  generateReport(results) {
    const total = results.length;
    const success = results.filter(r => r.success).length;
    const failed = results.filter(r => !r.success).length;
    const canBypass = results.filter(r => r.canBypassBrowser).length;
    
    // 按失败原因分组
    const failureReasons = {};
    results.filter(r => !r.success).forEach(r => {
      const reason = r.reason;
      failureReasons[reason] = (failureReasons[reason] || 0) + 1;
    });
    
    return {
      summary: {
        total,
        success,
        failed,
        canBypass,
        successRate: ((success / total) * 100).toFixed(1) + '%',
        bypassRate: ((canBypass / total) * 100).toFixed(1) + '%'
      },
      failureReasons,
      details: results
    };
  }

  /**
   * 检测反爬虫特征
   */
  detectAntiBot(response, headers) {
    const indicators = [];
    
    // Cloudflare
    if (headers['cf-ray'] || headers['CF-RAY']) {
      indicators.push('Cloudflare');
    }
    
    // Akamai
    if (headers['akamai-grn']) {
      indicators.push('Akamai');
    }
    
    // reCAPTCHA
    if (response && response.includes('recaptcha')) {
      indicators.push('reCAPTCHA');
    }
    
    // hCaptcha
    if (response && response.includes('hcaptcha')) {
      indicators.push('hCaptcha');
    }
    
    // 通用特征
    if (headers['x-robots-tag']) {
      indicators.push('Robots restriction');
    }
    
    return {
      detected: indicators.length > 0,
      indicators
    };
  }

  /**
   * 生成 Markdown 报告
   */
  generateMarkdownReport(report) {
    let md = `# API 验证报告\n\n`;
    
    md += `## 概览\n\n`;
    md += `- 总计: ${report.summary.total}\n`;
    md += `- 成功: ${report.summary.success}\n`;
    md += `- 失败: ${report.summary.failed}\n`;
    md += `- 可直连: ${report.summary.canBypass}\n`;
    md += `- 成功率: ${report.summary.successRate}\n`;
    md += `- 直连率: ${report.summary.bypassRate}\n\n`;
    
    if (Object.keys(report.failureReasons).length > 0) {
      md += `## 失败原因分析\n\n`;
      Object.entries(report.failureReasons).forEach(([reason, count]) => {
        md += `- ${reason}: ${count}\n`;
      });
      md += `\n`;
    }
    
    md += `## 详细结果\n\n`;
    report.details.forEach((result, index) => {
      md += `### ${index + 1}. ${result.url}\n\n`;
      md += `- 状态: ${result.success ? '✅ 成功' : '❌ 失败'}\n`;
      
      if (result.success) {
        md += `- HTTP 状态: ${result.status}\n`;
        md += `- 可直连: ${result.canBypassBrowser ? '是' : '否'}\n`;
      } else {
        md += `- 错误: ${result.error}\n`;
        md += `- 原因: ${result.reason}\n`;
      }
      
      md += `\n`;
    });
    
    return md;
  }
}

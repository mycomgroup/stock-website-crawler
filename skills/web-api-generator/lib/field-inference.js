/**
 * 字段含义推导服务
 * - 优先使用大模型（OpenAI 兼容接口）
 * - 失败时回退到本地规则推导
 */
export class FieldInferenceService {
  constructor(options = {}) {
    this.apiKey = options.apiKey || process.env.LLM_API_KEY || process.env.OPENAI_API_KEY;
    this.baseUrl = (options.baseUrl || process.env.LLM_API_BASE_URL || process.env.OPENAI_BASE_URL || 'https://api.openai.com/v1').replace(/\/$/, '');
    this.model = options.model || process.env.LLM_MODEL || process.env.OPENAI_MODEL || 'gpt-4o-mini';
    this.enabled = options.enabled !== false;
  }

  async inferFieldMeanings(context) {
    const fallback = this.inferWithRules(context);

    if (!this.enabled || !this.apiKey) {
      return {
        source: 'rules',
        fields: fallback,
        note: '未配置 LLM_API_KEY/OPENAI_API_KEY，使用本地规则推导'
      };
    }

    try {
      const fields = await this.inferWithLLM(context, fallback);
      return {
        source: 'llm',
        fields
      };
    } catch (error) {
      return {
        source: 'rules',
        fields: fallback,
        note: `LLM 推导失败，已回退到规则模式: ${error.message}`
      };
    }
  }

  inferWithRules(context) {
    const { pattern, paramNames = [] } = context;
    const sample = pattern?.samples?.[0] || '';

    return paramNames.map((paramName, index) => {
      const lower = String(paramName).toLowerCase();
      const meaning = this.guessMeaningByName(lower, pattern?.pathTemplate || '');
      const suggested = this.extractSuggestedValueFromSample(pattern, index);

      return {
        name: paramName,
        meaning,
        suggestedValue: suggested || null,
        reason: sample ? `根据 URL 模板和样本链接推导（样本: ${sample}）` : '根据参数命名规则推导'
      };
    });
  }

  guessMeaningByName(lowerName, pathTemplate) {
    const path = String(pathTemplate || '').toLowerCase();

    if (lowerName.includes('stock') || lowerName.includes('symbol') || lowerName.includes('ticker')) return '股票代码';
    if (lowerName.includes('company')) return '公司标识或公司代码';
    if (lowerName.includes('industry')) return '行业代码';
    if (lowerName.includes('index')) return '指数代码';
    if (lowerName.includes('fund')) return '基金代码';
    if (lowerName.includes('market')) return '市场标识（如 sh/sz/us/hk）';
    if (lowerName.includes('date') || lowerName.includes('time')) return '日期/时间参数';
    if (lowerName.includes('type')) return '类型枚举参数';
    if (lowerName.includes('id')) return '业务主键 ID';

    if (path.includes('/company/')) return '公司或股票维度参数';
    if (path.includes('/industry/')) return '行业维度参数';
    if (path.includes('/index/')) return '指数维度参数';
    if (path.includes('/fund/')) return '基金维度参数';

    return '业务路径参数（建议参考页面 URL 样本）';
  }

  extractSuggestedValueFromSample(pattern, index) {
    const sampleUrl = pattern?.samples?.[0];
    if (!sampleUrl || !pattern?.pathTemplate) return null;

    const samplePath = this.normalizeUrlToPath(sampleUrl);
    const templateSegments = pattern.pathTemplate.split('/').filter(Boolean);
    const sampleSegments = samplePath.split('/').filter(Boolean);

    const placeholderIndices = templateSegments
      .map((segment, i) => ({ segment, i }))
      .filter(item => item.segment.startsWith('{') && item.segment.endsWith('}'))
      .map(item => item.i);

    const realIndex = placeholderIndices[index];
    if (realIndex === undefined) return null;

    return sampleSegments[realIndex] || null;
  }

  normalizeUrlToPath(urlOrPath) {
    try {
      const url = new URL(urlOrPath);
      return url.pathname;
    } catch {
      return urlOrPath;
    }
  }

  async inferWithLLM(context, fallbackFields) {
    const prompt = {
      task: '根据网页 URL 模式推导每个路径参数的业务含义，并给出建议输入值',
      requirements: [
        '只输出 JSON 数组，不要 markdown',
        '每个元素必须包含 name, meaning, suggestedValue, reason 字段',
        'meaning 用简体中文，简短且业务化',
        '如果不确定，明确写出不确定原因'
      ],
      context
    };

    let response;
    try {
      response = await fetch(`${this.baseUrl}/chat/completions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`
        },
        body: JSON.stringify({
          model: this.model,
          temperature: 0.2,
          response_format: { type: 'json_object' },
          messages: [
            {
              role: 'system',
              content: '你是 API 参数语义分析专家，擅长从 URL 模板、路径层级和样本链接推断字段含义。'
            },
            {
              role: 'user',
              content: JSON.stringify(prompt)
            }
          ]
        })
      });
    } catch (networkError) {
      throw new Error(`网络请求失败: ${networkError.message}`);
    }

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP ${response.status}: ${errorText.slice(0, 200)}`);
    }

    const data = await response.json();
    const content = data?.choices?.[0]?.message?.content;
    if (!content) {
      throw new Error('LLM 返回为空');
    }

    const parsed = JSON.parse(content);
    const fields = Array.isArray(parsed) ? parsed : parsed.fields;
    if (!Array.isArray(fields)) {
      throw new Error('LLM 返回格式无效');
    }

    return fallbackFields.map(field => {
      const fromLLM = fields.find(item => item.name === field.name);
      if (!fromLLM) return field;
      return {
        name: field.name,
        meaning: fromLLM.meaning || field.meaning,
        suggestedValue: fromLLM.suggestedValue || field.suggestedValue || null,
        reason: fromLLM.reason || field.reason
      };
    });
  }
}

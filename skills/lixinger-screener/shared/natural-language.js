import OpenAI from 'openai';
import {
  getConditionDisplayLabel,
  isBrowserMetricEntry,
  isConditionMetricEntry
} from './catalog.js';

function createOpenAIClient() {
  const apiKey = process.env.LLM_API_KEY;
  const baseURL = process.env.LLM_BASE_URL || undefined;
  return new OpenAI({ apiKey, ...(baseURL ? { baseURL } : {}) });
}

export function validateLlmEnv() {
  const required = ['LLM_API_KEY'];
  const missing = required.filter(key => !process.env[key]);
  return { valid: missing.length === 0, missing };
}

function buildConditionCatalogPromptEntries(catalog) {
  return catalog.map(entry => ({
    metric: entry.metric,
    category: entry.category,
    displayLabelExample: getConditionDisplayLabel(entry),
    unit: entry.unit,
    selectors: (entry.selectors || []).map(selector => ({
      defaultLabel: selector.defaultLabel,
      options: selector.options.map(option => option.label)
    })),
    notes: entry.notes || null
  }));
}

function buildBrowserCatalogPromptEntries(catalog) {
  return catalog.map(entry => ({
    field: entry.displayName,
    category: entry.category,
    unit: entry.unit,
    operators: entry.operators
  }));
}

function buildSystemPrompt(catalog) {
  const firstEntry = catalog[0] || null;

  if (isConditionMetricEntry(firstEntry)) {
    return `你是一个股票筛选条件解析助手。用户会用自然语言描述筛选条件，你需要将其转换为结构化 JSON。

可用的条件模板如下：
${JSON.stringify(buildConditionCatalogPromptEntries(catalog), null, 2)}

请将用户意图转换成下面这个 JSON，只返回 JSON：
{
  "conditions": [
    {
      "metric": "<metric from catalog>",
      "category": "<optional category from catalog>",
      "selectors": ["<selector label 1>", "<selector label 2>"],
      "operator": "<大于|小于|介于>",
      "value": <number or [min, max]>
    }
  ]
}

规则：
- metric 必须使用 catalog 中的 metric
- selectors 只在该 metric 需要时才填写，值必须来自对应 selector 的选项 label
- operator 只能是 "大于"、"小于" 或 "介于"
- value 为数字；当 operator 为 "介于" 时，value 为 [最小值, 最大值]
- 只返回 JSON，不要返回 markdown 代码块或解释`;
  }

  if (isBrowserMetricEntry(firstEntry)) {
    return `你是一个股票筛选条件解析助手。用户会用自然语言描述筛选条件，你需要将其转换为结构化 JSON。

可用字段如下：
${JSON.stringify(buildBrowserCatalogPromptEntries(catalog), null, 2)}

请将用户意图转换成下面这个 JSON，只返回 JSON：
{
  "conditions": [
    {
      "field": "<field from catalog>",
      "operator": "<大于|小于|介于>",
      "value": <number or [min, max]>
    }
  ]
}

规则：
- field 必须使用 catalog 中的 field
- operator 只能是 "大于"、"小于" 或 "介于"
- value 为数字；当 operator 为 "介于" 时，value 为 [最小值, 最大值]
- 只返回 JSON，不要返回 markdown 代码块或解释`;
  }

  throw new Error('Unsupported catalog format for natural language parsing');
}

export async function queryToUnifiedInput(userQuery, catalog) {
  const envResult = validateLlmEnv();
  if (!envResult.valid) {
    throw new Error(`缺少必要的环境变量：${envResult.missing.join('、')}`);
  }

  const model = process.env.LLM_MODEL || 'gpt-4o';
  const client = createOpenAIClient();
  const systemPrompt = buildSystemPrompt(catalog);

  let responseText;
  try {
    const completion = await client.chat.completions.create({
      model,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userQuery }
      ],
      temperature: 0
    });
    responseText = completion.choices[0]?.message?.content?.trim() ?? '';
  } catch (error) {
    throw new Error(`LLM 请求失败：${error.message}`);
  }

  const cleaned = responseText
    .replace(/^```(?:json)?\s*/i, '')
    .replace(/\s*```$/, '')
    .trim();

  try {
    return JSON.parse(cleaned);
  } catch {
    throw new Error(`LLM 返回的内容无法解析为 JSON。\n原始内容：${responseText}`);
  }
}

export function validateUnifiedQuery(input, catalog) {
  const errors = [];
  const conditions = Array.isArray(input?.conditions) ? input.conditions : [];
  const firstEntry = catalog[0] || null;

  if (isConditionMetricEntry(firstEntry)) {
    for (const condition of conditions) {
      const entry = catalog.find(item => item.metric === condition.metric);
      if (!entry) {
        errors.push(`指标 "${condition.metric}" 不在条件目录中`);
        continue;
      }

      const selectors = condition.selectors || [];
      for (let index = 0; index < selectors.length; index += 1) {
        const selector = entry.selectors?.[index];
        if (!selector) {
          errors.push(`指标 "${condition.metric}" 不支持第 ${index + 1} 个 selector`);
          continue;
        }
        const option = selector.options.find(item => item.label === selectors[index]);
        if (!option) {
          errors.push(
            `指标 "${condition.metric}" 的 selector ${index + 1} 不支持 "${selectors[index]}"`
          );
        }
      }
    }
  } else if (isBrowserMetricEntry(firstEntry)) {
    const validFields = new Set(catalog.map(entry => entry.displayName));
    for (const condition of conditions) {
      const field = condition.field || condition.displayLabel;
      if (!validFields.has(field)) {
        errors.push(`字段 "${field}" 不在 metrics-catalog 中`);
      }
    }
  } else {
    errors.push('Unsupported catalog format');
  }

  return {
    valid: errors.length === 0,
    errors
  };
}

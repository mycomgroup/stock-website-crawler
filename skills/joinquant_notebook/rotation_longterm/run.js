#!/usr/bin/env node
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { JoinQuantClient } from '../request/joinquant-client.js';
import { ensureJoinQuantSession } from '../request/ensure-joinquant-session.js';
import { runNotebookTest } from '../request/test-joinquant-notebook.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SESSION_FILE = resolve(__dirname, '..', 'data', 'session.json');
const OUTPUT_ROOT = resolve(__dirname, 'output');
const SOURCE_NOTEBOOK_URL = 'https://www.joinquant.com/research?target=research&url=/user/21333940833/notebooks/02%20%E7%A0%94%E7%A9%B6%20%E6%9D%BF%E5%9D%97%E8%BD%AE%E5%8A%A8%E6%89%93%E5%88%86%E4%B8%8E%E7%83%AD%E5%BA%A6%E8%BF%BD%E8%B8%AA.ipynb';
const NOTEBOOK_URL = 'https://www.joinquant.com/research?target=research&url=/user/21333940833/notebooks/rotation_longterm_analysis.ipynb';
const CELL_MARKER = '# AUTO_ROTATION_ANALYSIS_30D';

function generateAnalysisCellSource() {
  return `${CELL_MARKER}
from IPython.display import display, Markdown
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

LOOKBACK_DAYS = 30
RETURN_DAYS = 5
BACK_DAYS = 30
TOP_N = 10
STOCK_TOP_COUNT = 5
UP_LIMIT = 30
CATEGORY_META = [
    ('zjw', '证监会行业'),
    ('sw_l2', '申万二级行业'),
    ('jq_l2', '聚宽二级行业'),
]

plt.rcParams['axes.unicode_minus'] = False


def fmt_trade_day(value):
    if hasattr(value, 'strftime'):
        return value.strftime('%Y-%m-%d')
    return str(value)[:10]


def build_daily_top(df_return, category, trade_day):
    s_tops = df_return.groupby(category).apply(group_top_list, STOCK_TOP_COUNT, UP_LIMIT, RETURN_DAYS)
    s_scores = df_return.groupby(category).apply(group_score_series, UP_LIMIT, RETURN_DAYS, BACK_DAYS)
    s_score = df_return.groupby(category).apply(group_score, UP_LIMIT, BACK_DAYS)
    df = pd.DataFrame({
        'scores': s_scores,
        'top': s_tops,
        'score': s_score,
    }, index=s_tops.index).sort_values(by='score', ascending=False).head(TOP_N).reset_index()
    df = df.rename(columns={category: 'industry'})
    df['date'] = trade_day
    df['rank'] = np.arange(1, len(df) + 1)
    return df[['date', 'industry', 'rank', 'score', 'top', 'scores']]


def calc_transition_metrics(cat_df, trade_days):
    day_sets = {
        trade_day: set(cat_df.loc[cat_df['date'] == trade_day, 'industry'])
        for trade_day in trade_days
    }
    day_top1 = {}
    for trade_day in trade_days:
        daily = cat_df.loc[cat_df['date'] == trade_day].sort_values('rank')
        day_top1[trade_day] = None if daily.empty else daily.iloc[0]['industry']

    overlap_counts = []
    churn_counts = []
    top1_switches = 0
    new_entries = 0
    new_entries_retained = 0
    two_day_persistent = 0
    two_day_persistent_retained = 0
    high_score_total = 0
    high_score_cooldown = 0
    score_lookup = cat_df.set_index(['date', 'industry'])['score'].to_dict()

    for index in range(1, len(trade_days)):
        prev_day = trade_days[index - 1]
        cur_day = trade_days[index]
        prev_set = day_sets.get(prev_day, set())
        cur_set = day_sets.get(cur_day, set())
        overlap = len(prev_set & cur_set)
        overlap_counts.append(overlap)
        churn_counts.append(TOP_N - overlap)
        if day_top1.get(prev_day) != day_top1.get(cur_day):
            top1_switches += 1

    for index in range(1, len(trade_days) - 1):
        prev_day = trade_days[index - 1]
        cur_day = trade_days[index]
        next_day = trade_days[index + 1]
        prev_set = day_sets.get(prev_day, set())
        cur_set = day_sets.get(cur_day, set())
        next_set = day_sets.get(next_day, set())

        new_set = cur_set - prev_set
        new_entries += len(new_set)
        new_entries_retained += len(new_set & next_set)

        persistent_set = prev_set & cur_set
        two_day_persistent += len(persistent_set)
        two_day_persistent_retained += len(persistent_set & next_set)

    for index in range(len(trade_days) - 1):
        cur_day = trade_days[index]
        next_day = trade_days[index + 1]
        today_scores = cat_df.loc[(cat_df['date'] == cur_day) & (cat_df['score'] >= 15), ['industry', 'score']]
        for row in today_scores.itertuples():
            high_score_total += 1
            next_score = score_lookup.get((next_day, row.industry), 0)
            if next_score < row.score:
                high_score_cooldown += 1

    transition_count = max(len(trade_days) - 1, 1)
    return {
        'avg_overlap': float(np.mean(overlap_counts)) if overlap_counts else 0.0,
        'avg_churn': float(np.mean(churn_counts)) if churn_counts else 0.0,
        'top1_switch_rate': top1_switches / transition_count,
        'new_entry_retention_rate': (new_entries_retained / new_entries) if new_entries else 0.0,
        'two_day_persistent_retention_rate': (two_day_persistent_retained / two_day_persistent) if two_day_persistent else 0.0,
        'high_score_cooldown_rate': (high_score_cooldown / high_score_total) if high_score_total else 0.0,
        'new_entries': new_entries,
        'two_day_persistent': two_day_persistent,
        'high_score_total': high_score_total,
    }


def build_summary(cat_df, trade_days):
    score_pivot = cat_df.pivot(index='date', columns='industry', values='score').fillna(0)
    rank_pivot = cat_df.pivot(index='date', columns='industry', values='rank')
    latest_day = trade_days[-1]
    recent_days = trade_days[-3:]
    previous_days = trade_days[-6:-3]

    summary = pd.DataFrame({
        'appear_days': cat_df.groupby('industry')['date'].nunique(),
        'avg_rank': cat_df.groupby('industry')['rank'].mean(),
        'avg_score': cat_df.groupby('industry')['score'].mean(),
        'max_score': cat_df.groupby('industry')['score'].max(),
    }).fillna(0)

    summary['latest_score'] = score_pivot.loc[latest_day] if latest_day in score_pivot.index else 0
    summary['latest_rank'] = rank_pivot.loc[latest_day] if latest_day in rank_pivot.index else np.nan
    summary['recent3_avg'] = score_pivot.loc[recent_days].mean() if recent_days else 0
    if previous_days:
        summary['prev3_avg'] = score_pivot.loc[previous_days].mean()
    else:
        summary['prev3_avg'] = 0
    summary['trend_3d'] = summary['recent3_avg'] - summary['prev3_avg']
    summary['in_latest_top10'] = summary['latest_score'] > 0
    summary = summary.sort_values(
        by=['appear_days', 'latest_score', 'avg_score', 'avg_rank'],
        ascending=[False, False, False, True],
    )
    return summary, score_pivot


def plot_category(score_pivot, summary, title):
    leaders = summary.head(8).index.tolist()
    if not leaders:
        return

    fig, axes = plt.subplots(1, 2, figsize=(18, 6))
    score_pivot[leaders].plot(ax=axes[0], marker='o')
    axes[0].set_title(f'{title}近30个交易日核心热点得分')
    axes[0].set_xlabel('交易日')
    axes[0].set_ylabel('得分')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(alpha=0.25)

    summary.head(10).sort_values('appear_days').plot(
        kind='barh',
        y='appear_days',
        ax=axes[1],
        legend=False,
        color='#4472C4'
    )
    axes[1].set_title(f'{title}近30日上榜天数 Top10')
    axes[1].set_xlabel('进入 Top10 的天数')
    axes[1].set_ylabel('行业')
    axes[1].grid(axis='x', alpha=0.25)

    plt.tight_layout()
    plt.show()


def display_category_report(cat_df, trade_days, category, title):
    metrics = calc_transition_metrics(cat_df, trade_days)
    summary, score_pivot = build_summary(cat_df, trade_days)
    latest_day = trade_days[-1]
    prev_day = trade_days[-2]
    latest_set = set(cat_df.loc[cat_df['date'] == latest_day, 'industry'])
    prev_set = set(cat_df.loc[cat_df['date'] == prev_day, 'industry'])
    new_today = sorted(latest_set - prev_set)

    print('\\n' + '=' * 100)
    print(f'{title} - 近30个交易日轮动统计')
    print('=' * 100)
    print(f'平均连续重叠行业数: {metrics["avg_overlap"]:.2f} / 10')
    print(f'平均每日新切换行业数: {metrics["avg_churn"]:.2f} / 10')
    print(f'Top1 龙头切换率: {metrics["top1_switch_rate"]:.2%}')
    print(f'新上榜行业次日留榜率: {metrics["new_entry_retention_rate"]:.2%}')
    print(f'连续2天在榜行业第3天留榜率: {metrics["two_day_persistent_retention_rate"]:.2%}')
    print(f'高分行业(>=15分)次日降温率: {metrics["high_score_cooldown_rate"]:.2%}')
    print('今天新进入 Top10:', '、'.join(new_today) if new_today else '无')

    display(summary[[
        'appear_days',
        'avg_rank',
        'avg_score',
        'max_score',
        'latest_score',
        'latest_rank',
        'trend_3d',
        'in_latest_top10',
    ]].head(12).round(2))

    recent_matrix = score_pivot.loc[trade_days[-5:], summary.head(10).index].T.fillna(0)
    recent_matrix.columns = [str(col) for col in recent_matrix.columns]
    print('\\n最近5个交易日得分矩阵（Top10 常驻行业）:')
    display(recent_matrix.round(2))
    plot_category(score_pivot, summary, title)

    return {
        'metrics': metrics,
        'summary': summary,
        'score_pivot': score_pivot,
        'new_today': new_today,
    }


trade_days = [fmt_trade_day(day) for day in get_trade_days(end_date=date.today(), count=LOOKBACK_DAYS)]
print('=' * 100)
print(f'板块轮动 30 交易日统计分析 | 区间: {trade_days[0]} ~ {trade_days[-1]}')
print('=' * 100)

records = []
for trade_day in trade_days:
    df_ind = stock_industry(trade_day, ['zjw', 'sw_l2', 'jq_l2'])
    df_return = returns_series(df_ind, trade_day, RETURN_DAYS, BACK_DAYS)
    for category, title in CATEGORY_META:
        daily_top = build_daily_top(df_return, category, trade_day)
        daily_top['category'] = category
        daily_top['category_name'] = title
        records.append(daily_top)

all_top = pd.concat(records, ignore_index=True)
reports = {}
for category, title in CATEGORY_META:
    reports[category] = display_category_report(
        all_top.loc[all_top['category'] == category].copy(),
        trade_days,
        category,
        title,
    )

zjw_metrics = reports['zjw']['metrics']
zjw_summary = reports['zjw']['summary']
zjw_latest = zjw_summary[zjw_summary['in_latest_top10']].head(8)
focus_list = zjw_latest[
    (zjw_latest['appear_days'] >= 6) | (zjw_latest['trend_3d'] > 0)
].head(5)

print('\\n' + '=' * 100)
print('30 交易日核心结论')
print('=' * 100)
print(f'1. 证监会行业平均每日有 {zjw_metrics["avg_churn"]:.2f} 个席位发生切换，说明轮动很明显，但不是完全随机。')
print(f'2. 新上榜行业次日留榜率为 {zjw_metrics["new_entry_retention_rate"]:.2%}，连续2天在榜行业第3天留榜率为 {zjw_metrics["two_day_persistent_retention_rate"]:.2%}。')
print(f'3. 高分行业(>=15分)次日降温率为 {zjw_metrics["high_score_cooldown_rate"]:.2%}，高分后追涨需要防回落。')
print('4. 今天更值得看的方向:')
if focus_list.empty:
    print('   • 暂无明显同时满足“常驻”或“近3日升温”的行业。')
else:
    for row in focus_list.itertuples():
        print(f'   • {row.Index}: 上榜 {int(row.appear_days)} 天, 最新得分 {row.latest_score:.0f}, 近3日趋势 {row.trend_3d:+.2f}')
print('5. 今天新进入 Top10 的证监会行业:')
if reports['zjw']['new_today']:
    for item in reports['zjw']['new_today']:
        print(f'   • {item}')
else:
    print('   • 无')
`;
}

async function ensureNotebookExists() {
  const targetClient = new JoinQuantClient({
    sessionFile: SESSION_FILE,
    notebookUrl: NOTEBOOK_URL,
    outputRoot: OUTPUT_ROOT
  });

  try {
    await targetClient.getNotebookMetadata();
    return { created: false };
  } catch (error) {
    if (!String(error.message || '').includes('404')) {
      throw error;
    }
  }

  const sourceClient = new JoinQuantClient({
    sessionFile: SESSION_FILE,
    notebookUrl: SOURCE_NOTEBOOK_URL,
    outputRoot: OUTPUT_ROOT
  });
  const sourceModel = await sourceClient.getNotebookModel();
  await targetClient.saveNotebook(sourceModel.content);
  return { created: true };
}

export async function main() {
  await ensureJoinQuantSession({
    sessionFile: SESSION_FILE,
    notebookUrl: NOTEBOOK_URL,
    outputRoot: OUTPUT_ROOT
  });

  const { created } = await ensureNotebookExists();
  console.log(created ? '已创建长期复用 notebook，开始更新分析单元...' : '将更新长期复用 notebook 中的 30 交易日分析单元...');

  const result = await runNotebookTest({
    sessionFile: SESSION_FILE,
    outputRoot: OUTPUT_ROOT,
    notebookUrl: NOTEBOOK_URL,
    mode: 'partial',
    cellSource: generateAnalysisCellSource(),
    cellMarker: CELL_MARKER,
    cellIndex: '1,2,last',
    timeoutMs: 900000,
    kernelName: 'python3',
    appendCell: true
  });

  const executions = result.executions || [];
  const lastExecution = executions[executions.length - 1];

  console.log(`Notebook: ${result.notebookUrl}`);
  console.log(`更新的 cell 索引: ${result.managedCellIndex}`);
  console.log(`结果文件: ${result.resultFile}`);
  console.log(`Notebook 快照: ${result.notebookSnapshotPath}`);

  if (lastExecution?.textOutput) {
    console.log('\n执行输出前 6000 字：\n');
    console.log(lastExecution.textOutput.slice(0, 6000));
  }

  return result;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main().catch(error => {
    console.error('主程序错误:', error.stack || error.message);
    process.exit(1);
  });
}

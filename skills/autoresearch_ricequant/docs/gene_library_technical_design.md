# 策略基因库技术设计文档

> **版本**: v1.0  
> **日期**: 2026-04-07  
> **状态**: 设计阶段  
> **关联模块**: `skills/autoresearch` + `skills/strategy_kits`

---

## 目录

1. [背景与动机](#1-背景与动机)
2. [核心概念定义](#2-核心概念定义)
3. [系统架构总览](#3-系统架构总览)
4. [数据流：双向闭环](#4-数据流双向闭环)
5. [基因数据模型](#5-基因数据模型)
6. [模块详细设计](#6-模块详细设计)
   - 6.1 [gene_schema — 基因元数据定义](#61-gene_schema--基因元数据定义)
   - 6.2 [gene_registry — 基因注册与检索](#62-gene_registry--基因注册与检索)
   - 6.3 [gene_extractor — 从 autoresearch 历史中提取基因](#63-gene_extractor--从-autoresearch-历史中提取基因)
   - 6.4 [gene_compiler — 基因组合编译为可执行策略](#64-gene_compiler--基因组合编译为可执行策略)
   - 6.5 [gene_scorer — 基因质量评估](#65-gene_scorer--基因质量评估)
   - 6.6 [autoresearch 桥接层](#66-autoresearch-桥接层)
7. [与现有系统的接口对齐](#7-与现有系统的接口对齐)
8. [基因分类体系](#8-基因分类体系)
9. [存储结构](#9-存储结构)
10. [基因进化算子](#10-基因进化算子)
11. [过拟合防护机制](#11-过拟合防护机制)
12. [实施路线图](#12-实施路线图)
13. [风险与约束](#13-风险与约束)

---

## 1. 背景与动机

### 1.1 现状问题

`autoresearch` 是一个自动化策略迭代优化框架，通过 AI Agent 反复修改 `strategy.py` → 提交回测 → 根据打分决策 keep/rollback 形成闭环进化。当前存在以下问题：

| 问题 | 表现 | 影响 |
|------|------|------|
| **搜索效率低** | 28 次迭代仅 4 次 keep（14% 成功率） | 大量算力和 API 配额浪费 |
| **知识不沉淀** | 成功的变异只记录为自然语言描述 | 无法跨策略复用 |
| **搜索空间无结构** | Agent 在 Python 源码全空间随机试错 | 容易重复失败方向 |
| **过拟合无防护** | 单窗口回测 score 翻 5 倍无 OOS 验证 | 策略泛化能力存疑 |

### 1.2 strategy_kits 已有基础

`strategy_kits` 已经是一个组件化的策略框架，提供了：

- **SignalRegistry / SignalFactory / SignalComposer** — 信号注册、计算、组合
- **RegimeFilter 引擎** — 6 种市场情绪门控
- **FactorPreprocessPipeline** — fit/transform 因子加工
- **PortfolioBuilder** — 完整约束体系的组合构建
- **task_schema + task_runner** — 统一任务编排
- **universal_mechanisms/** — 通用策略模式代码库

这些组件天然就是"基因"的载体，缺的只是：基因的元数据层、提取器、编译器、以及与 autoresearch 的桥接。

### 1.3 目标

构建双向闭环：

```
autoresearch (发现) ──提取基因──▶ strategy_kits/gene_library (沉淀)
     ▲                                         │
     └──────── 组装基因提供结构化搜索空间 ◀────────┘
```

- **主流向（沉淀）**：autoresearch 的成功变异 → 标准化基因 → 入库
- **反向流（应用）**：autoresearch 从基因库选择/组合/微调 → 缩小搜索空间 → 提升迭代效率

---

## 2. 核心概念定义

| 概念 | 定义 | 类比 |
|------|------|------|
| **Gene（基因）** | 一个可序列化、可复用的策略组件配置快照，包含组件类型、参数、来源和质量元数据 | 生物基因 |
| **Genotype（基因型）** | 一组基因的有序组合，定义策略的完整配置 | 染色体 |
| **Phenotype（表现型）** | 基因型编译后生成的可执行 strategy.py + task_spec | 生物体 |
| **Fitness（适应度）** | 回测得分（scorer.py 的 composite score） | 自然选择 |
| **Mutation（变异）** | 对单个基因参数的微调 | 基因突变 |
| **Crossover（交叉）** | 从两个成功基因型中各取一部分组合成新基因型 | 有性生殖 |
| **Gene Pool（基因池）** | 所有已注册基因的集合 | 种群基因库 |

---

## 3. 系统架构总览

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Gene Library System                         │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                   strategy_kits/gene_library/                │  │
│  │                                                              │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │  │
│  │  │ gene_schema  │  │gene_registry │  │  gene_extractor  │   │  │
│  │  │              │  │              │  │                  │   │  │
│  │  │ - Gene       │  │ - register() │  │ - from_history() │  │  │
│  │  │ - Genotype   │  │ - query()    │  │ - from_diff()    │  │  │
│  │  │ - GeneSlot   │  │ - version()  │  │ - from_signal()  │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘   │  │
│  │                                                              │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │  │
│  │  │gene_compiler │  │ gene_scorer  │  │  gene_operators  │   │  │
│  │  │              │  │              │  │                  │   │  │
│  │  │ - compile()  │  │ - fitness()  │  │ - mutate()       │  │  │
│  │  │ - to_task()  │  │ - oos_test() │  │ - crossover()    │  │  │
│  │  │ - to_rq()    │  │ - stability()│  │ - select()       │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  ┌──────────────────┐              ┌────────────────────────────┐  │
│  │   autoresearch/  │◄────────────▶│    strategy_kits/          │  │
│  │   bridge.py      │   桥接层     │    (signals, portfolio,    │  │
│  │                  │              │     risk, templates, ...)  │  │
│  └──────────────────┘              └────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. 数据流：双向闭环

### 4.1 沉淀流（autoresearch → gene_library）

```
autoresearch 实验完成一轮迭代
        │
        ▼
history/NNNN.json (decision=keep)
        │
        ▼
gene_extractor.from_history(experiment_dir)
        │
        ├── 解析 git diff（参数变化）
        ├── 映射到 strategy_kits 组件类型
        ├── 提取参数快照
        └── 计算质量元数据（score_delta, stability）
        │
        ▼
Gene JSON 文件
        │
        ▼
gene_registry.register(gene)
        │
        ▼
strategy_kits/gene_library/genes/{category}/{gene_id}.json
```

### 4.2 应用流（gene_library → autoresearch）

```
autoresearch 开始新实验
        │
        ▼
gene_registry.query(category="regime_filter", min_fitness=1.5)
        │
        ▼
返回候选基因列表
        │
        ▼
Agent 选择基因组合 (Genotype)
        │
        ▼
gene_compiler.compile(genotype)
        │
        ├── 生成 strategy.py（RiceQuant 格式）
        └── 生成 seed_config.json（含基因元数据引用）
        │
        ▼
autoresearch setup.py --from-genotype genotype.json
        │
        ▼
正常迭代循环（但搜索空间限定在基因参数范围内）
```

---

## 5. 基因数据模型

### 5.1 Gene（单个基因）

```json
{
  "$schema": "gene_v1",
  "gene_id": "regime_breadth_v3",
  "version": "1.0.0",
  "category": "regime_filter",
  "slot": "regime",

  "component": {
    "module": "strategy_kits.signals.regime_filters.breadth_filter",
    "class": null,
    "function": "calc_market_breadth",
    "platform_adapter": "ricequant"
  },

  "params": {
    "breadth_window": {
      "value": 15,
      "dtype": "int",
      "range": [5, 60],
      "step": 5,
      "description": "市场宽度计算窗口（交易日）"
    },
    "breadth_extreme": {
      "value": 0.12,
      "dtype": "float",
      "range": [0.05, 0.30],
      "step": 0.01,
      "description": "极端行情阈值"
    },
    "breadth_universe_size": {
      "value": 100,
      "dtype": "int",
      "range": [30, 300],
      "step": 10,
      "description": "宽度计算股票池大小"
    }
  },

  "quality": {
    "fitness_score": 2.225,
    "score_delta": 1.826,
    "oos_score": null,
    "stability_score": null,
    "experiments_used": 1,
    "total_iterations_tested": 28
  },

  "origin": {
    "experiment_id": "rfscore7_pb10_enhanced_20260407",
    "champion_iter": "0025",
    "commit_hash": "5b8c30df",
    "backtest_id": "7973329",
    "mutation_description": "breadth from 50 to 100 stocks",
    "extracted_at": "2026-04-07T14:11:34Z"
  },

  "compatibility": {
    "platforms": ["ricequant", "joinquant", "backtrader"],
    "min_python": "3.10",
    "dependencies": [],
    "conflicts_with": []
  },

  "tags": ["A股", "沪深300", "市场宽度", "择时"]
}
```

### 5.2 Genotype（基因组合）

```json
{
  "$schema": "genotype_v1",
  "genotype_id": "gt_rfscore7_champion_20260407",
  "name": "RFScore7 沪深300 宽度增强版",
  "description": "基于 RF 评分 + PB 因子 + 市场宽度择时的沪深300选股策略",

  "slots": {
    "alpha": {
      "genes": ["alpha_rfscore7_v2", "alpha_pb_factor_v1"],
      "composer": "weighted",
      "composer_config": {"weights": {"alpha_rfscore7_v2": 0.7, "alpha_pb_factor_v1": 0.3}}
    },
    "regime": {
      "genes": ["regime_breadth_v3"],
      "composer": "single"
    },
    "universe": {
      "genes": ["universe_hs300_base_v1"],
      "composer": "single"
    },
    "portfolio": {
      "genes": ["portfolio_equal_weight_top20_v1"],
      "composer": "single"
    },
    "risk": {
      "genes": ["risk_drawdown_035_v1", "risk_industry_025_v1"],
      "composer": "pipeline"
    },
    "execution": {
      "genes": ["exec_weekly_rebalance_v1"],
      "composer": "single"
    }
  },

  "backtest_config": {
    "start_date": "2025-04-07",
    "end_date": "2026-03-31",
    "capital": 100000,
    "benchmark": "000300.XSHG",
    "freq": "day"
  },

  "lineage": {
    "parent_genotype": null,
    "generation": 1,
    "created_at": "2026-04-07T15:00:00Z",
    "created_by": "gene_extractor"
  }
}
```

---

## 6. 模块详细设计

### 6.1 gene_schema — 基因元数据定义

**文件位置**: `strategy_kits/gene_library/gene_schema.py`

```python
"""基因元数据定义 — 所有基因的统一数据结构"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional, Tuple
from enum import Enum
import json
from pathlib import Path


# ── 基因槽位定义 ─────────────────────────────────────────────────────────────

class GeneSlot(Enum):
    """策略中的标准槽位，每个槽位对应策略的一个功能层"""
    ALPHA = "alpha"            # 选股信号 → strategy_kits.signals.indicator_factory
    REGIME = "regime"          # 择时门控 → strategy_kits.signals.regime_filters
    PREPROCESS = "preprocess"  # 因子加工 → strategy_kits.signals.factor_preprocess
    UNIVERSE = "universe"      # 股票池   → strategy_kits.universe
    PORTFOLIO = "portfolio"    # 组合构建 → strategy_kits.portfolio
    RISK = "risk"              # 风控规则 → strategy_kits.risk
    EXECUTION = "execution"    # 执行模板 → strategy_kits.strategy_templates


class ComposerMethod(Enum):
    """同一槽位多基因的组合方式"""
    SINGLE = "single"              # 单基因，直接使用
    WEIGHTED = "weighted"          # 加权组合 → SignalComposer.weighted()
    EQUAL_WEIGHT = "equal_weight"  # 等权组合 → SignalComposer.equal_weight()
    MAJORITY_VOTE = "majority_vote"  # 多数投票 → SignalComposer.majority_vote()
    PIPELINE = "pipeline"          # 管道串联（适用于 risk、preprocess）
    UNANIMOUS = "unanimous"        # 一致同意 → SignalComposer.unanimous()


# ── 参数描述 ─────────────────────────────────────────────────────────────────

@dataclass
class ParamSpec:
    """单个基因参数的描述与约束"""
    value: Any                          # 当前值
    dtype: Literal["int", "float", "str", "bool", "list"]
    range: Optional[Tuple[Any, Any]] = None   # 合法范围 [min, max]
    step: Optional[float] = None              # 搜索步长（用于变异）
    choices: Optional[List[Any]] = None       # 枚举值（dtype=str 时使用）
    description: str = ""

    def validate(self, v: Any) -> bool:
        """验证值是否在合法范围内"""
        if self.choices is not None:
            return v in self.choices
        if self.range is not None:
            return self.range[0] <= v <= self.range[1]
        return True


# ── 基因质量元数据 ───────────────────────────────────────────────────────────

@dataclass
class GeneQuality:
    """基因质量评估数据"""
    fitness_score: float = 0.0          # 所在策略的最佳 composite score
    score_delta: float = 0.0            # 相对 baseline 的 score 提升
    oos_score: Optional[float] = None   # Out-of-sample 得分（跨时间窗口）
    stability_score: Optional[float] = None   # 参数扰动稳定性得分
    experiments_used: int = 0           # 被多少个实验使用过
    total_keep_count: int = 0           # 在所有实验中累计 keep 次数
    last_validated: Optional[str] = None      # 最近一次验证时间


# ── 基因来源追溯 ─────────────────────────────────────────────────────────────

@dataclass
class GeneOrigin:
    """基因的来源追溯信息"""
    experiment_id: str = ""
    champion_iter: str = ""
    commit_hash: str = ""
    backtest_id: str = ""
    mutation_description: str = ""
    extracted_at: str = ""


# ── 基因兼容性 ───────────────────────────────────────────────────────────────

@dataclass
class GeneCompatibility:
    """基因的平台兼容性信息"""
    platforms: List[str] = field(default_factory=lambda: ["ricequant"])
    min_python: str = "3.10"
    dependencies: List[str] = field(default_factory=list)
    conflicts_with: List[str] = field(default_factory=list)


# ── 基因主体 ─────────────────────────────────────────────────────────────────

@dataclass
class Gene:
    """
    策略基因 — 基因库的原子单元。

    一个 Gene 代表策略中一个可复用的组件配置快照。
    它绑定到 strategy_kits 的某个具体组件（Signal、Filter、Rule 等），
    并记录了该组件的参数配置、质量评估、来源追溯。
    """
    gene_id: str                         # 全局唯一标识，如 "regime_breadth_v3"
    version: str = "1.0.0"               # 语义版本号
    category: str = ""                   # 分类标签，如 "regime_filter"
    slot: GeneSlot = GeneSlot.ALPHA      # 所属槽位

    # 绑定的 strategy_kits 组件
    component_module: str = ""           # 如 "strategy_kits.signals.regime_filters.breadth_filter"
    component_class: Optional[str] = None  # 类名（Signal 类）或 None（函数型）
    component_function: Optional[str] = None  # 函数名（函数型组件）
    platform_adapter: str = "ricequant"  # 目标平台适配器

    # 参数
    params: Dict[str, ParamSpec] = field(default_factory=dict)

    # 元数据
    quality: GeneQuality = field(default_factory=GeneQuality)
    origin: GeneOrigin = field(default_factory=GeneOrigin)
    compatibility: GeneCompatibility = field(default_factory=GeneCompatibility)
    tags: List[str] = field(default_factory=list)

    def get_param_values(self) -> Dict[str, Any]:
        """提取所有参数的当前值"""
        return {k: v.value for k, v in self.params.items()}

    def get_search_space(self) -> Dict[str, Dict]:
        """提取参数搜索空间（供变异算子使用）"""
        return {
            k: {"range": v.range, "step": v.step, "choices": v.choices, "dtype": v.dtype}
            for k, v in self.params.items()
            if v.range is not None or v.choices is not None
        }

    def to_dict(self) -> Dict[str, Any]:
        """序列化为可存储的 dict"""
        # ... 标准 dataclass → dict 转换
        pass

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Gene:
        """从 dict 反序列化"""
        # ... dict → dataclass 转换
        pass

    def save(self, path: Path) -> None:
        """保存为 JSON 文件"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, path: Path) -> Gene:
        """从 JSON 文件加载"""
        with open(path, encoding="utf-8") as f:
            return cls.from_dict(json.load(f))


# ── 槽位配置 ─────────────────────────────────────────────────────────────────

@dataclass
class SlotConfig:
    """一个槽位的基因配置"""
    genes: List[str]                     # 基因 ID 列表
    composer: ComposerMethod = ComposerMethod.SINGLE
    composer_config: Dict[str, Any] = field(default_factory=dict)


# ── 基因型 ───────────────────────────────────────────────────────────────────

@dataclass
class Genotype:
    """
    基因型 — 一组基因的完整组合，可编译为可执行策略。

    对应关系：
    - Genotype.slots["alpha"]  → strategy_kits SignalFactory + SignalComposer
    - Genotype.slots["regime"] → strategy_kits run_regime_gate()
    - Genotype.slots["portfolio"] → strategy_kits PortfolioBuilder
    - Genotype.slots["risk"]   → strategy_kits CompositeRiskEngine
    """
    genotype_id: str
    name: str = ""
    description: str = ""

    slots: Dict[str, SlotConfig] = field(default_factory=dict)

    backtest_config: Dict[str, Any] = field(default_factory=dict)

    # 谱系追溯
    parent_genotype: Optional[str] = None
    generation: int = 1
    created_at: str = ""
    created_by: str = ""

    def get_all_gene_ids(self) -> List[str]:
        """获取所有引用的基因 ID"""
        ids = []
        for slot_cfg in self.slots.values():
            ids.extend(slot_cfg.genes)
        return ids
```

**设计要点**：

1. **ParamSpec 携带搜索空间** — 每个参数不仅有值，还有 range/step，让变异算子知道可以怎么调
2. **GeneSlot 对齐 strategy_kits 模块** — 6 个槽位恰好对应 strategy_kits 的 6 个功能层
3. **ComposerMethod 对齐 SignalComposer** — 组合方式直接映射到 strategy_kits 已有的合成函数
4. **Gene 与 Genotype 分离** — Gene 是原子单元可以跨策略复用，Genotype 是特定策略的组装方案

---

### 6.2 gene_registry — 基因注册与检索

**文件位置**: `strategy_kits/gene_library/gene_registry.py`

```python
"""基因注册中心 — 管理基因的 CRUD、查询、版本控制"""

from pathlib import Path
from typing import Dict, List, Optional, Any
import json
import logging

from .gene_schema import Gene, GeneSlot, Genotype

logger = logging.getLogger(__name__)

# 默认基因库存储路径
DEFAULT_GENE_STORE = Path(__file__).parent / "genes"
DEFAULT_GENOTYPE_STORE = Path(__file__).parent / "genotypes"


class GeneRegistry:
    """
    基因注册中心。

    存储结构:
        genes/
        ├── alpha/
        │   ├── alpha_rfscore7_v2.json
        │   └── alpha_pb_factor_v1.json
        ├── regime/
        │   ├── regime_breadth_v3.json
        │   └── regime_cvix_v1.json
        ├── preprocess/
        ├── universe/
        ├── portfolio/
        ├── risk/
        ├── execution/
        └── index.json          ← 全局索引（缓存，可重建）

    设计原则:
        - 基因以 JSON 文件存储，一个基因一个文件
        - index.json 是查询加速缓存，从文件可重建
        - 支持版本号（同一 gene_id 可有多个版本）
        - 查询支持按 slot/category/tags/min_fitness 过滤
    """

    def __init__(self, store_path: Optional[Path] = None):
        self.store_path = store_path or DEFAULT_GENE_STORE
        self.store_path.mkdir(parents=True, exist_ok=True)
        self._index: Dict[str, dict] = {}
        self._load_index()

    # ── 注册 ─────────────────────────────────────────────────────────────

    def register(self, gene: Gene, overwrite: bool = False) -> str:
        """
        注册一个基因到库中。

        Args:
            gene: Gene 实例
            overwrite: 是否覆盖已有同 ID 基因

        Returns:
            gene_id

        Raises:
            ValueError: gene_id 已存在且 overwrite=False
        """
        if gene.gene_id in self._index and not overwrite:
            raise ValueError(
                f"Gene '{gene.gene_id}' already registered. "
                f"Use overwrite=True or bump version."
            )

        # 按 slot 分目录存储
        slot_dir = self.store_path / gene.slot.value
        slot_dir.mkdir(parents=True, exist_ok=True)
        gene_path = slot_dir / f"{gene.gene_id}.json"
        gene.save(gene_path)

        # 更新索引
        self._index[gene.gene_id] = {
            "slot": gene.slot.value,
            "category": gene.category,
            "version": gene.version,
            "fitness": gene.quality.fitness_score,
            "score_delta": gene.quality.score_delta,
            "tags": gene.tags,
            "path": str(gene_path.relative_to(self.store_path)),
        }
        self._save_index()

        logger.info(f"gene_registered | gene_id={gene.gene_id} slot={gene.slot.value}")
        return gene.gene_id

    # ── 查询 ─────────────────────────────────────────────────────────────

    def get(self, gene_id: str) -> Gene:
        """按 ID 获取基因"""
        if gene_id not in self._index:
            raise KeyError(f"Gene not found: {gene_id}")
        path = self.store_path / self._index[gene_id]["path"]
        return Gene.load(path)

    def query(
        self,
        slot: Optional[GeneSlot] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        min_fitness: Optional[float] = None,
        min_score_delta: Optional[float] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        查询基因。

        Args:
            slot: 按槽位过滤
            category: 按分类过滤
            tags: 按标签过滤（AND 逻辑，必须包含所有指定标签）
            min_fitness: 最低适应度阈值
            min_score_delta: 最低 score 提升阈值
            limit: 返回数量上限

        Returns:
            匹配的基因索引条目列表，按 fitness 降序排列
        """
        results = []
        for gene_id, info in self._index.items():
            if slot and info["slot"] != slot.value:
                continue
            if category and info["category"] != category:
                continue
            if tags and not all(t in info.get("tags", []) for t in tags):
                continue
            if min_fitness and info.get("fitness", 0) < min_fitness:
                continue
            if min_score_delta and info.get("score_delta", 0) < min_score_delta:
                continue
            results.append({"gene_id": gene_id, **info})

        results.sort(key=lambda x: x.get("fitness", 0), reverse=True)
        return results[:limit]

    def list_all(self) -> Dict[str, List[str]]:
        """按 slot 列出所有基因 ID"""
        by_slot: Dict[str, List[str]] = {}
        for gene_id, info in self._index.items():
            slot = info["slot"]
            by_slot.setdefault(slot, []).append(gene_id)
        return by_slot

    # ── 删除 / 版本 ─────────────────────────────────────────────────────

    def remove(self, gene_id: str) -> None:
        """从库中删除基因"""
        if gene_id not in self._index:
            return
        path = self.store_path / self._index[gene_id]["path"]
        path.unlink(missing_ok=True)
        del self._index[gene_id]
        self._save_index()

    # ── 索引管理 ─────────────────────────────────────────────────────────

    def _load_index(self) -> None:
        idx_path = self.store_path / "index.json"
        if idx_path.exists():
            with open(idx_path, encoding="utf-8") as f:
                self._index = json.load(f)
        else:
            self._rebuild_index()

    def _save_index(self) -> None:
        idx_path = self.store_path / "index.json"
        with open(idx_path, "w", encoding="utf-8") as f:
            json.dump(self._index, f, indent=2, ensure_ascii=False)

    def _rebuild_index(self) -> None:
        """从文件系统重建索引"""
        self._index = {}
        for gene_file in self.store_path.rglob("*.json"):
            if gene_file.name == "index.json":
                continue
            try:
                gene = Gene.load(gene_file)
                self._index[gene.gene_id] = {
                    "slot": gene.slot.value,
                    "category": gene.category,
                    "version": gene.version,
                    "fitness": gene.quality.fitness_score,
                    "score_delta": gene.quality.score_delta,
                    "tags": gene.tags,
                    "path": str(gene_file.relative_to(self.store_path)),
                }
            except Exception as e:
                logger.warning(f"skip bad gene file {gene_file}: {e}")
        self._save_index()
```

**设计要点**：

1. **文件即数据库** — 每个基因一个 JSON 文件，无需额外数据库依赖，git 友好
2. **index.json 加速查询** — 避免每次查询都读取所有文件，但可从文件重建
3. **按 slot 分目录** — 物理结构对齐逻辑分类，便于人工浏览
4. **查询支持多维过滤** — slot / category / tags / fitness 组合过滤

---

### 6.3 gene_extractor — 从 autoresearch 历史中提取基因

**文件位置**: `strategy_kits/gene_library/gene_extractor.py`

这是"沉淀流"的核心模块，负责从 autoresearch 实验的 keep 迭代中提取可复用基因。

#### 提取策略

autoresearch 的 strategy.py 是一个 RiceQuant 平台的单体策略文件。提取器需要：

1. **解析 git diff** — 识别哪些参数/逻辑发生了变化
2. **映射到 strategy_kits 组件** — 将变化归类到对应的 GeneSlot
3. **构建 Gene 对象** — 填充参数、质量、来源元数据

```python
"""基因提取器 — 从 autoresearch 实验历史中提取可复用基因"""

import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .gene_schema import (
    Gene, GeneQuality, GeneOrigin, GeneCompatibility,
    GeneSlot, ParamSpec,
)


# ── 参数模式识别规则 ─────────────────────────────────────────────────────────

# 将 strategy.py 中常见的参数名映射到 GeneSlot + 组件
PARAM_SLOT_MAP = {
    # regime 相关
    "breadth_window": GeneSlot.REGIME,
    "breadth_extreme": GeneSlot.REGIME,
    "breadth_bottom": GeneSlot.REGIME,
    "breadth_universe_size": GeneSlot.REGIME,
    "volatility_threshold": GeneSlot.REGIME,
    "momentum_window": GeneSlot.REGIME,

    # alpha 相关
    "score_weights": GeneSlot.ALPHA,
    "factor_list": GeneSlot.ALPHA,
    "lookback_period": GeneSlot.ALPHA,
    "rf_n_estimators": GeneSlot.ALPHA,

    # portfolio 相关
    "hold_num": GeneSlot.PORTFOLIO,
    "max_weight": GeneSlot.PORTFOLIO,
    "rebalance_days": GeneSlot.EXECUTION,

    # risk 相关
    "max_drawdown_limit": GeneSlot.RISK,
    "stop_loss": GeneSlot.RISK,
    "industry_limit": GeneSlot.RISK,

    # universe 相关
    "stock_pool": GeneSlot.UNIVERSE,
    "index_code": GeneSlot.UNIVERSE,
    "min_market_cap": GeneSlot.UNIVERSE,
}

# 将 GeneSlot 映射到 strategy_kits 的标准组件路径
SLOT_COMPONENT_MAP = {
    GeneSlot.REGIME: "strategy_kits.signals.regime_filters",
    GeneSlot.ALPHA: "strategy_kits.signals.indicator_factory",
    GeneSlot.PREPROCESS: "strategy_kits.signals.factor_preprocess",
    GeneSlot.PORTFOLIO: "strategy_kits.portfolio.position_state.portfolio_builder",
    GeneSlot.RISK: "strategy_kits.risk.constraints",
    GeneSlot.UNIVERSE: "strategy_kits.universe.stock_pool_filters",
    GeneSlot.EXECUTION: "strategy_kits.strategy_templates.presets",
}


class GeneExtractor:
    """
    从 autoresearch 实验中提取基因。

    提取流程:
    1. 扫描 history/ 目录，找到所有 decision=keep 的迭代
    2. 对每个 keep 迭代，解析其 git diff
    3. 从 diff 中识别参数变化，映射到 GeneSlot
    4. 构建 Gene 对象，填充质量和来源元数据
    """

    def __init__(self, experiment_dir: Path):
        self.experiment_dir = experiment_dir
        self.history_dir = experiment_dir / "history"
        self.state = self._load_json(experiment_dir / "state.json")
        self.seed_config = self._load_json(experiment_dir / "seed_config.json")

    def extract_all(self) -> List[Gene]:
        """
        提取实验中所有 keep 迭代的基因。

        Returns:
            Gene 列表，按迭代顺序排列
        """
        genes = []
        keep_iters = self._find_keep_iterations()

        for iter_record in keep_iters:
            iter_genes = self._extract_from_iteration(iter_record)
            genes.extend(iter_genes)

        return genes

    def extract_champion(self) -> List[Gene]:
        """只提取当前 champion 的基因（最新最优版本）"""
        champion_iter = self.state.get("champion_iter", "")
        if not champion_iter:
            return []

        record_path = self.history_dir / f"{champion_iter}.json"
        if not record_path.exists():
            return []

        record = self._load_json(record_path)
        return self._extract_from_iteration(record)

    def _find_keep_iterations(self) -> List[dict]:
        """扫描 history/ 找到所有 keep 迭代"""
        keep_records = []
        for f in sorted(self.history_dir.glob("*.json")):
            if f.stem == "index" or "baseline" in f.stem:
                continue
            record = self._load_json(f)
            if record.get("decision") == "keep":
                keep_records.append(record)
        return keep_records

    def _extract_from_iteration(self, record: dict) -> List[Gene]:
        """
        从单次 keep 迭代中提取基因。

        策略：
        1. 获取该迭代的 git diff
        2. 解析 diff 中的参数变化
        3. 同时解析当前 strategy.py 的完整参数快照
        4. 按 slot 分组，每个 slot 生成一个 Gene
        """
        iter_id = record.get("iter", "")
        commit = record.get("commit", "")
        mutation = record.get("mutation", "")

        # 获取 diff（如果有 commit hash）
        param_changes = {}
        if commit:
            param_changes = self._parse_git_diff(commit)

        # 解析当前 strategy.py 的参数快照
        strategy_path = self.experiment_dir / "strategy.py"
        full_params = self._parse_strategy_params(strategy_path)

        # 按 slot 分组参数
        genes = []
        params_by_slot = self._group_params_by_slot(full_params)

        for slot, params in params_by_slot.items():
            # 检查该 slot 是否有参数在本次迭代中被修改
            has_changes = any(p in param_changes for p in params)

            gene = Gene(
                gene_id=self._make_gene_id(slot, iter_id),
                version="1.0.0",
                category=slot.value,
                slot=slot,
                component_module=SLOT_COMPONENT_MAP.get(slot, ""),
                platform_adapter="ricequant",
                params={
                    name: ParamSpec(
                        value=val,
                        dtype=self._infer_dtype(val),
                        range=self._infer_range(name, val),
                        step=self._infer_step(name, val),
                        description=name,
                    )
                    for name, val in params.items()
                },
                quality=GeneQuality(
                    fitness_score=record.get("score", 0),
                    score_delta=record.get("score", 0) - self._get_baseline_score(),
                    experiments_used=1,
                    total_keep_count=1,
                ),
                origin=GeneOrigin(
                    experiment_id=self.seed_config.get("project", {}).get("strategy_name", ""),
                    champion_iter=iter_id,
                    commit_hash=commit,
                    backtest_id=record.get("backtest_id", ""),
                    mutation_description=mutation,
                    extracted_at=record.get("end_time", ""),
                ),
                compatibility=GeneCompatibility(
                    platforms=["ricequant", "joinquant", "backtrader"]
                ),
                tags=self._infer_tags(slot, params),
            )
            genes.append(gene)

        return genes

    def _parse_git_diff(self, commit: str) -> Dict[str, Tuple]:
        """解析 git diff，提取参数变化"""
        result = subprocess.run(
            ["git", "diff", f"{commit}^", commit, "--", "strategy.py"],
            cwd=str(self.experiment_dir),
            capture_output=True, text=True,
        )
        changes = {}
        for line in result.stdout.splitlines():
            # 匹配形如 -foo = 10 / +foo = 15 的行
            m = re.match(r'^[+-]\s*(\w+)\s*=\s*(.+)', line)
            if m:
                name, val = m.group(1), m.group(2).strip()
                changes[name] = val
        return changes

    def _parse_strategy_params(self, path: Path) -> Dict[str, Any]:
        """
        静态解析 strategy.py，提取所有顶层赋值参数。

        使用 AST 解析而非正则，更可靠。
        """
        import ast

        params = {}
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            try:
                                val = ast.literal_eval(node.value)
                                params[target.id] = val
                            except (ValueError, TypeError):
                                pass
        except SyntaxError:
            pass
        return params

    def _group_params_by_slot(self, params: Dict) -> Dict[GeneSlot, Dict]:
        """将参数按 slot 分组"""
        grouped: Dict[GeneSlot, Dict] = {}
        for name, val in params.items():
            slot = PARAM_SLOT_MAP.get(name)
            if slot:
                grouped.setdefault(slot, {})[name] = val
        return grouped

    def _make_gene_id(self, slot: GeneSlot, iter_id: str) -> str:
        exp_name = self.seed_config.get("project", {}).get("strategy_name", "unknown")
        return f"{slot.value}_{exp_name}_iter{iter_id}"

    def _get_baseline_score(self) -> float:
        baseline_path = self.history_dir / "0000_baseline.json"
        if baseline_path.exists():
            return self._load_json(baseline_path).get("score", 0)
        return 0.0

    def _infer_dtype(self, val: Any) -> str:
        if isinstance(val, bool): return "bool"
        if isinstance(val, int): return "int"
        if isinstance(val, float): return "float"
        if isinstance(val, str): return "str"
        if isinstance(val, list): return "list"
        return "str"

    def _infer_range(self, name: str, val: Any) -> Optional[tuple]:
        """基于参数名和当前值推断合理范围"""
        if isinstance(val, (int, float)):
            # 通用启发式：当前值的 0.2x ~ 5x
            low = max(type(val)(val * 0.2), type(val)(1) if isinstance(val, int) else 0.001)
            high = type(val)(val * 5)
            return (low, high)
        return None

    def _infer_step(self, name: str, val: Any) -> Optional[float]:
        if isinstance(val, int): return max(1, val // 10)
        if isinstance(val, float): return round(val * 0.1, 4)
        return None

    def _infer_tags(self, slot: GeneSlot, params: Dict) -> List[str]:
        tags = ["A股", slot.value]
        if "breadth" in str(params): tags.append("市场宽度")
        if "momentum" in str(params): tags.append("动量")
        return tags

    @staticmethod
    def _load_json(path: Path) -> dict:
        if not path.exists():
            return {}
        with open(path, encoding="utf-8") as f:
            return json.load(f)
```

**关键设计决策**：

| 决策 | 选择 | 理由 |
|------|------|------|
| 参数提取方式 | AST 解析 + git diff | AST 可靠提取赋值语句，diff 确认哪些是本次变化 |
| 基因粒度 | 按 slot 聚合（非单个参数） | 一个 slot 内的参数通常耦合，拆太细会丢失语义 |
| 范围推断 | 启发式（当前值的 0.2x ~ 5x） | 作为初始猜测，可在后续迭代中通过参数敏感性分析细化 |
| gene_id 命名 | `{slot}_{experiment}_{iter}` | 保证全局唯一，且从 ID 即可追溯来源 |

---

### 6.4 gene_compiler — 基因组合编译为可执行策略

**文件位置**: `strategy_kits/gene_library/gene_compiler.py`

这是"应用流"的核心模块，负责将 Genotype 编译为可执行的策略文件和任务配置。

#### 编译目标

| 目标平台 | 输出 | 对齐的现有接口 |
|----------|------|---------------|
| **本地 backtrader** | task_spec.json | `strategy_kits.orchestration.task_schema.validate_strategy_task_spec()` |
| **RiceQuant** | strategy.py（RQ 格式） | `autoresearch.run_iteration.py` |
| **JoinQuant** | strategy.py（JQ 格式） | `strategy_kits.execution.backtrader_runtime.compat.JQ2BTBaseStrategy` |

```python
"""基因编译器 — 将 Genotype 编译为可执行策略"""

from pathlib import Path
from typing import Any, Dict, Optional
import json
import logging

from .gene_schema import Gene, Genotype, GeneSlot, ComposerMethod
from .gene_registry import GeneRegistry

logger = logging.getLogger(__name__)


class GeneCompiler:
    """
    将 Genotype（基因组合）编译为可执行策略。

    编译流程:
    1. 从 GeneRegistry 加载 Genotype 引用的所有 Gene
    2. 按 slot 分组解析参数
    3. 根据目标平台选择输出格式
    4. 生成 task_spec.json（for backtrader）或 strategy.py（for RQ/JQ）

    与 strategy_kits 的对齐:
    - alpha slot   → SignalFactory.add_signal() + SignalComposer
    - regime slot  → run_regime_gate() 的 config 参数
    - portfolio slot → PortfolioBuilder(PortfolioSpec(...))
    - risk slot    → CompositeRiskEngine([rules])
    - execution slot → backtest.template in task_spec
    """

    def __init__(self, registry: Optional[GeneRegistry] = None):
        self.registry = registry or GeneRegistry()

    def compile_to_task_spec(self, genotype: Genotype) -> Dict[str, Any]:
        """
        编译为 strategy_kits task_spec 格式。

        输出可直接传入:
            strategy_kits.orchestration.task_runner.run_strategy_task(spec)

        Returns:
            符合 task_schema.validate_strategy_task_spec() 规范的 dict
        """
        genes = self._load_all_genes(genotype)

        # 提取各 slot 参数
        alpha_params = self._extract_slot_params(genes, GeneSlot.ALPHA)
        regime_params = self._extract_slot_params(genes, GeneSlot.REGIME)
        portfolio_params = self._extract_slot_params(genes, GeneSlot.PORTFOLIO)
        risk_params = self._extract_slot_params(genes, GeneSlot.RISK)
        execution_params = self._extract_slot_params(genes, GeneSlot.EXECUTION)
        universe_params = self._extract_slot_params(genes, GeneSlot.UNIVERSE)

        bt_cfg = genotype.backtest_config

        task_spec = {
            "task": {
                "task_id": genotype.genotype_id,
                "strategy_name": genotype.name,
                "mode": "single_strategy_research",
            },
            "data": {
                "panel_type": "local_features",
                "start_date": bt_cfg.get("start_date", "2025-01-01"),
                "end_date": bt_cfg.get("end_date", "2026-03-31"),
            },
            "pipeline": {
                "top_n": portfolio_params.get("hold_num", 20),
                "score_method": alpha_params.get("score_method", "equal"),
                "weight_mode": alpha_params.get("weight_mode", "score"),
            },
            "portfolio": {
                "max_positions": portfolio_params.get("hold_num", 20),
                "max_single": portfolio_params.get("max_weight", 0.1),
                "cash_target": portfolio_params.get("cash_target", 0.05),
            },
            "backtest": {
                "template": self._resolve_template(execution_params),
                "initial_cash": float(bt_cfg.get("capital", 1000000)),
                "rebalance_threshold": execution_params.get("rebalance_threshold", 0.01),
                "hold_days": execution_params.get("hold_days", 1),
            },
            "risk": {
                "enable_constraints": True,
                "max_industry": risk_params.get("industry_limit", 0.3),
                "max_turnover": risk_params.get("max_turnover", 0.4),
            },
            "output": {
                "save_artifacts": True,
                "artifact_dir": f"./artifacts/{genotype.genotype_id}",
            },
            "platform": {
                "engine": "local",
            },
            # 扩展字段：记录基因血统
            "_gene_metadata": {
                "genotype_id": genotype.genotype_id,
                "gene_ids": genotype.get_all_gene_ids(),
                "generation": genotype.generation,
                "parent": genotype.parent_genotype,
            },
        }

        return task_spec

    def compile_to_rq_strategy(
        self, genotype: Genotype, template_path: Optional[Path] = None
    ) -> str:
        """
        编译为 RiceQuant 格式的 strategy.py 源码。

        使用 Jinja2 模板，将基因参数注入到策略代码模板中。
        模板中的占位符与基因参数名对齐。

        Args:
            genotype: 基因型
            template_path: 策略模板路径，默认使用内置模板

        Returns:
            strategy.py 的完整源码字符串
        """
        from jinja2 import Template

        genes = self._load_all_genes(genotype)
        all_params = {}
        for gene in genes.values():
            all_params.update(gene.get_param_values())

        # 加载模板
        if template_path is None:
            template_path = Path(__file__).parent / "templates" / "rq_strategy.py.j2"

        template_source = template_path.read_text(encoding="utf-8")
        template = Template(template_source)
        return template.render(**all_params, genotype=genotype)

    def compile_to_autoresearch_experiment(
        self,
        genotype: Genotype,
        output_dir: Path,
    ) -> Path:
        """
        编译为 autoresearch 实验目录结构。

        生成:
            output_dir/
            ├── strategy.py          ← 从基因编译
            ├── seed_config.json     ← 含基因元数据引用
            ├── genotype.json        ← 基因型定义
            └── gene_search_space.json ← 参数搜索空间（供 Agent 参考）

        Returns:
            output_dir 路径
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        genes = self._load_all_genes(genotype)

        # 1. 生成 strategy.py
        strategy_code = self.compile_to_rq_strategy(genotype)
        (output_dir / "strategy.py").write_text(strategy_code, encoding="utf-8")

        # 2. 生成 seed_config.json（含基因引用）
        seed_config = self._build_seed_config(genotype, genes)
        with open(output_dir / "seed_config.json", "w", encoding="utf-8") as f:
            json.dump(seed_config, f, indent=2, ensure_ascii=False)

        # 3. 保存 genotype 定义
        with open(output_dir / "genotype.json", "w", encoding="utf-8") as f:
            json.dump(genotype.__dict__, f, indent=2, ensure_ascii=False, default=str)

        # 4. 生成搜索空间文件（供 Agent 在迭代中参考）
        search_space = self._build_search_space(genes)
        with open(output_dir / "gene_search_space.json", "w", encoding="utf-8") as f:
            json.dump(search_space, f, indent=2, ensure_ascii=False)

        logger.info(f"compiled_experiment | dir={output_dir} genes={len(genes)}")
        return output_dir

    # ── 内部方法 ─────────────────────────────────────────────────────────

    def _load_all_genes(self, genotype: Genotype) -> Dict[str, Gene]:
        """加载 Genotype 引用的所有 Gene"""
        genes = {}
        for gene_id in genotype.get_all_gene_ids():
            genes[gene_id] = self.registry.get(gene_id)
        return genes

    def _extract_slot_params(self, genes: Dict[str, Gene], slot: GeneSlot) -> Dict:
        """提取指定 slot 下所有基因的参数合并"""
        params = {}
        for gene in genes.values():
            if gene.slot == slot:
                params.update(gene.get_param_values())
        return params

    def _resolve_template(self, exec_params: Dict) -> str:
        """从执行参数推断策略模板名"""
        template = exec_params.get("template", "EqualWeightStrategy")
        valid = {"WeightedTopNStrategy", "EqualWeightStrategy", "DirectExecutionStrategy"}
        return template if template in valid else "EqualWeightStrategy"

    def _build_seed_config(self, genotype: Genotype, genes: Dict[str, Gene]) -> Dict:
        """构建含基因引用的 seed_config"""
        bt_cfg = genotype.backtest_config
        return {
            "project": {"strategy_name": genotype.name},
            "seed": {"genotype_id": genotype.genotype_id},
            "backtest": {
                "start_date": bt_cfg.get("start_date"),
                "end_date": bt_cfg.get("end_date"),
                "capital": str(bt_cfg.get("capital", 100000)),
                "freq": bt_cfg.get("freq", "day"),
                "benchmark": bt_cfg.get("benchmark", "000300.XSHG"),
            },
            "objective": {
                "weights": {"calmar": 0.55, "sortino": 0.25, "information_ratio": 0.20},
                "hard_constraints": {"max_drawdown_limit": 0.35},
            },
            "gene_references": {
                gene_id: {
                    "slot": gene.slot.value,
                    "version": gene.version,
                    "params": gene.get_param_values(),
                }
                for gene_id, gene in genes.items()
            },
        }

    def _build_search_space(self, genes: Dict[str, Gene]) -> Dict:
        """构建参数搜索空间描述（供 Agent 参考）"""
        space = {}
        for gene_id, gene in genes.items():
            gene_space = gene.get_search_space()
            if gene_space:
                space[gene_id] = {
                    "slot": gene.slot.value,
                    "params": gene_space,
                }
        return space
```

**关键设计决策**：

| 决策 | 选择 | 理由 |
|------|------|------|
| 双输出格式 | task_spec（backtrader）+ strategy.py（RQ） | 覆盖本地快速验证和云端正式回测两个场景 |
| Jinja2 模板 | 参数注入而非 AST 重写 | 策略代码模板可以人工维护和调试，降低 bug 风险 |
| gene_search_space.json | 显式告知 Agent 可调参数范围 | 从"源码空间盲目搜索"变为"参数空间结构化搜索" |
| seed_config 含 gene_references | 每次实验都记录使用了哪些基因 | 支持回溯"这个策略是由哪些基因组装的" |

---

### 6.5 gene_scorer — 基因质量评估

**文件位置**: `strategy_kits/gene_library/gene_scorer.py`

```python
"""基因质量评估 — 多维度评估基因的泛化能力和可靠性"""

from typing import Dict, List, Optional
from .gene_schema import Gene, GeneQuality


class GeneScorer:
    """
    基因质量评估器。

    评估维度:
    1. fitness — 原始适应度（来自 autoresearch scorer.py 的 composite score）
    2. oos_fitness — Out-of-Sample 泛化能力
    3. stability — 参数扰动稳定性
    4. breadth — 跨实验通用性

    综合质量分:
        gene_quality = fitness * 0.30
                     + oos_fitness * 0.35
                     + stability * 0.20
                     + breadth * 0.15
    """

    # 权重
    W_FITNESS = 0.30
    W_OOS = 0.35
    W_STABILITY = 0.20
    W_BREADTH = 0.15

    def evaluate(self, gene: Gene, context: Optional[Dict] = None) -> GeneQuality:
        """综合评估基因质量"""
        quality = gene.quality

        # 1. 原始 fitness（已有，直接使用）
        fitness = quality.fitness_score

        # 2. OOS 验证（需要额外回测）
        oos = quality.oos_score if quality.oos_score is not None else 0.0

        # 3. 参数稳定性
        stability = quality.stability_score if quality.stability_score is not None else 0.0

        # 4. 跨实验通用性
        breadth = min(quality.experiments_used / 5.0, 1.0)  # 5个实验封顶

        # 综合分
        composite = (
            fitness * self.W_FITNESS
            + oos * self.W_OOS
            + stability * self.W_STABILITY
            + breadth * self.W_BREADTH
        )

        quality.fitness_score = fitness
        return quality

    def run_oos_test(
        self,
        gene: Gene,
        oos_windows: List[Dict[str, str]],
    ) -> float:
        """
        Out-of-Sample 验证。

        将基因参数应用到不同时间窗口，计算 OOS 得分。

        Args:
            gene: 待测基因
            oos_windows: OOS 时间窗口列表，如:
                [
                    {"start_date": "2023-01-01", "end_date": "2023-12-31"},
                    {"start_date": "2024-01-01", "end_date": "2024-12-31"},
                ]

        Returns:
            OOS 平均得分
        """
        # 实现：调用 gene_compiler 生成策略 → 分别在各窗口回测 → 取平均分
        # 此处为框架，具体回测调用在 Phase 2 实现
        raise NotImplementedError("OOS test requires backtest integration")

    def run_stability_test(
        self,
        gene: Gene,
        perturbation_pct: float = 0.10,
        n_samples: int = 10,
    ) -> float:
        """
        参数扰动稳定性测试。

        对每个参数在 ±perturbation_pct 范围内随机扰动 n_samples 次，
        如果得分波动很大 → 基因不稳定 → 可能过拟合。

        Args:
            gene: 待测基因
            perturbation_pct: 扰动幅度比例（如 0.10 = ±10%）
            n_samples: 每个参数的采样次数

        Returns:
            稳定性得分 [0, 1]，1 = 非常稳定
        """
        # 实现：生成扰动后的基因变体 → 分别回测 → 计算得分标准差
        # stability = 1 / (1 + std(scores))
        raise NotImplementedError("Stability test requires backtest integration")
```

**评分公式说明**：

```
综合质量分 = fitness × 0.30 + oos × 0.35 + stability × 0.20 + breadth × 0.15
```

- **OOS 权重最高 (0.35)** — 泛化能力是基因质量的核心，防止过拟合
- **fitness (0.30)** — 原始回测表现仍然重要
- **stability (0.20)** — 参数微扰后得分不应剧烈波动
- **breadth (0.15)** — 在多个实验中都有效的基因更可靠

---

### 6.6 autoresearch 桥接层

**文件位置**: `autoresearch/bridge.py`

这是连接 autoresearch 和 strategy_kits/gene_library 的桥梁。

```python
"""
autoresearch ↔ gene_library 桥接层

功能：
1. 实验完成后自动提取基因入库
2. 新实验启动时从基因库获取初始配置
3. 迭代过程中向 Agent 提供结构化搜索空间
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

# 注意：需要将 strategy_kits 加入 Python 路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "strategy_kits"))

from gene_library.gene_schema import Gene, Genotype, GeneSlot, SlotConfig, ComposerMethod
from gene_library.gene_registry import GeneRegistry
from gene_library.gene_extractor import GeneExtractor
from gene_library.gene_compiler import GeneCompiler


class AutoresearchBridge:
    """
    autoresearch 与基因库的桥接器。

    生命周期:
    ┌─────────────────────────────────────────────────────────┐
    │  setup.py 阶段                                         │
    │    bridge.init_from_genotype(genotype)                  │
    │    → 编译基因 → 生成 strategy.py + seed_config.json     │
    │    → 生成 gene_search_space.json                        │
    ├─────────────────────────────────────────────────────────┤
    │  run_iteration.py 阶段                                  │
    │    bridge.get_search_hints(experiment_dir)               │
    │    → 返回当前可调参数 + 已尝试方向 + 建议范围           │
    ├─────────────────────────────────────────────────────────┤
    │  实验结束后                                             │
    │    bridge.deposit_genes(experiment_dir)                  │
    │    → 提取 champion 基因 → 注册入库                      │
    └─────────────────────────────────────────────────────────┘
    """

    def __init__(self):
        self.registry = GeneRegistry()
        self.compiler = GeneCompiler(self.registry)

    # ── 1. 从基因库初始化实验 ────────────────────────────────────────────

    def init_from_genotype(
        self,
        genotype: Genotype,
        output_dir: Path,
    ) -> Path:
        """
        从基因型初始化 autoresearch 实验。

        等价于 setup.py 的前半段，但策略文件来自基因编译而非手动提供。
        """
        return self.compiler.compile_to_autoresearch_experiment(genotype, output_dir)

    def suggest_genotype(
        self,
        base_slot_preferences: Optional[Dict[str, List[str]]] = None,
    ) -> Genotype:
        """
        从基因库中自动推荐一个基因组合。

        策略：每个 slot 选择 fitness 最高的基因。

        Args:
            base_slot_preferences: 可选的 slot → gene_id 偏好

        Returns:
            推荐的 Genotype
        """
        slots = {}

        for slot in GeneSlot:
            # 查询该 slot 下最优基因
            candidates = self.registry.query(slot=slot, limit=3)

            if base_slot_preferences and slot.value in base_slot_preferences:
                # 使用用户指定的基因
                gene_ids = base_slot_preferences[slot.value]
            elif candidates:
                # 使用 fitness 最高的
                gene_ids = [candidates[0]["gene_id"]]
            else:
                continue

            slots[slot.value] = SlotConfig(
                genes=gene_ids,
                composer=ComposerMethod.SINGLE if len(gene_ids) == 1 else ComposerMethod.EQUAL_WEIGHT,
            )

        return Genotype(
            genotype_id=f"auto_suggested_{len(slots)}slots",
            name="Auto-suggested Genotype",
            slots=slots,
        )

    # ── 2. 迭代过程中提供搜索指引 ───────────────────────────────────────

    def get_search_hints(self, experiment_dir: Path) -> Dict:
        """
        为 Agent 提供结构化的搜索指引。

        读取 gene_search_space.json 和 state.json，返回:
        - 当前可调参数及范围
        - 已尝试且失败的方向（从 history 提取）
        - 推荐的下一步变异方向

        Returns:
            {
                "search_space": {...},         # 参数 → 范围
                "tried_and_failed": [...],     # 已失败的方向
                "suggested_mutations": [...],  # 推荐变异
            }
        """
        result = {
            "search_space": {},
            "tried_and_failed": [],
            "suggested_mutations": [],
        }

        # 读取搜索空间
        ss_path = experiment_dir / "gene_search_space.json"
        if ss_path.exists():
            with open(ss_path, encoding="utf-8") as f:
                result["search_space"] = json.load(f)

        # 分析历史失败方向
        history_dir = experiment_dir / "history"
        if history_dir.exists():
            for f in sorted(history_dir.glob("*.json")):
                if "baseline" in f.stem:
                    continue
                with open(f, encoding="utf-8") as fh:
                    record = json.load(fh)
                if record.get("decision") == "rollback":
                    result["tried_and_failed"].append({
                        "iter": record.get("iter"),
                        "mutation": record.get("mutation", ""),
                        "score": record.get("score", 0),
                    })

        # 基于失败历史推荐反方向
        result["suggested_mutations"] = self._suggest_from_failures(
            result["tried_and_failed"],
            result["search_space"],
        )

        return result

    def _suggest_from_failures(self, failures: List[Dict], space: Dict) -> List[str]:
        """基于失败历史推荐变异方向"""
        suggestions = []
        failed_directions = set()
        for f in failures:
            mutation = f.get("mutation", "")
            # 简单解析："X from A to B" → 记录 X 增大/减小方向
            if "→" in mutation or "to" in mutation.lower():
                failed_directions.add(mutation)

        if not failed_directions:
            suggestions.append("尝试调整尚未修改过的参数")
        else:
            suggestions.append(f"已有 {len(failed_directions)} 个方向失败，考虑组合变异或更换 slot")

        return suggestions

    # ── 3. 实验结束后沉淀基因 ────────────────────────────────────────────

    def deposit_genes(self, experiment_dir: Path) -> List[str]:
        """
        从完成的实验中提取 champion 基因并注册入库。

        Returns:
            注册成功的 gene_id 列表
        """
        extractor = GeneExtractor(experiment_dir)
        genes = extractor.extract_champion()

        registered = []
        for gene in genes:
            try:
                # 检查是否已有同源但更优的版本
                existing = self._find_existing_gene(gene)
                if existing and existing.quality.fitness_score >= gene.quality.fitness_score:
                    # 现有版本更优或相同，跳过
                    continue

                gene_id = self.registry.register(gene, overwrite=True)
                registered.append(gene_id)
            except Exception as e:
                print(f"[bridge] failed to register gene: {e}")

        return registered

    def _find_existing_gene(self, gene: Gene) -> Optional[Gene]:
        """查找同源基因（相同 slot + 相同实验来源）"""
        candidates = self.registry.query(slot=gene.slot)
        for c in candidates:
            try:
                existing = self.registry.get(c["gene_id"])
                if (existing.origin.experiment_id == gene.origin.experiment_id
                    and existing.slot == gene.slot):
                    return existing
            except KeyError:
                continue
        return None
```

---

## 7. 与现有系统的接口对齐

### 7.1 strategy_kits 组件 → Gene Slot 映射

| Gene Slot | strategy_kits 模块 | 核心接口 | Gene 参数来源 |
|-----------|-------------------|----------|--------------|
| **ALPHA** | `signals/indicator_factory/` | `SignalRegistry.create(name, config)` | config dict |
| **REGIME** | `signals/regime_filters/` | `run_regime_gate(market_data, config=...)` | config dict 中的 signals.* |
| **PREPROCESS** | `signals/factor_preprocess/` | `FactorPreprocessPipeline(config)` | PreprocessConfig + ScoreConfig |
| **UNIVERSE** | `universe/stock_pool_filters/` | `FilterPipeline.run(input)` | filter 启用/禁用 + 参数 |
| **PORTFOLIO** | `portfolio/position_state/` | `PortfolioBuilder(PortfolioSpec(...))` | PortfolioSpec 字段 |
| **RISK** | `risk/constraints.py` | `CompositeRiskEngine([rules]).run(ctx)` | 各 Rule 的构造参数 |
| **EXECUTION** | `strategy_templates/presets/` | `WeightedTopNStrategy / EqualWeightStrategy` | template 选择 + rebalance 参数 |

### 7.2 Gene 参数 → strategy_kits 构造函数映射

#### ALPHA Slot → SignalFactory

```python
# Gene 参数
gene.params = {
    "signal_name": ParamSpec(value="quality_momentum", dtype="str", 
                             choices=["macd", "alligator", "quality_momentum"]),
    "fastperiod": ParamSpec(value=12, dtype="int", range=(5, 30), step=1),
    "slowperiod": ParamSpec(value=26, dtype="int", range=(15, 50), step=1),
}

# → 编译为
factory = SignalFactory()
factory.add_signal("quality_momentum", {"fastperiod": 12, "slowperiod": 26})
```

#### REGIME Slot → run_regime_gate()

```python
# Gene 参数
gene.params = {
    "market_breadth_enabled": ParamSpec(value=True, dtype="bool"),
    "market_breadth_window": ParamSpec(value=15, dtype="int", range=(5, 60)),
    "market_breadth_threshold_high": ParamSpec(value=0.12, dtype="float", range=(0.05, 0.30)),
}

# → 编译为
config = {
    "signals": {
        "market_breadth": {
            "enabled": True,
            "window": 15,
            "threshold_high": 0.12,
        }
    }
}
output = run_regime_gate(market_data, config=config)
```

#### PORTFOLIO Slot → PortfolioBuilder

```python
# Gene 参数
gene.params = {
    "max_single": ParamSpec(value=0.08, dtype="float", range=(0.02, 0.20)),
    "max_positions": ParamSpec(value=20, dtype="int", range=(5, 50)),
    "objective": ParamSpec(value="equal_weight", dtype="str",
                           choices=["equal_weight", "max_sharpe", "min_variance", "risk_parity"]),
}

# → 编译为
spec = PortfolioSpec(max_single=0.08, max_positions=20, objective=OptimizationObjective.EQUAL_WEIGHT)
builder = PortfolioBuilder(spec)
```

#### RISK Slot → CompositeRiskEngine

```python
# Gene 参数
gene.params = {
    "max_drawdown_limit": ParamSpec(value=0.35, dtype="float", range=(0.10, 0.50)),
    "max_industry_pct": ParamSpec(value=0.25, dtype="float", range=(0.10, 0.50)),
    "max_var": ParamSpec(value=0.05, dtype="float", range=(0.01, 0.10)),
}

# → 编译为
engine = CompositeRiskEngine([
    MaximumDrawdownRule(max_drawdown=0.35),
    IndustryConcentrationRule(max_industry_pct=0.25),
    VaRRule(max_var=0.05),
])
```

### 7.3 Genotype → autoresearch seed_config.json 映射

```
Genotype                          seed_config.json
────────                          ────────────────
genotype_id                   →   project.strategy_name
backtest_config.start_date    →   backtest.start_date
backtest_config.end_date      →   backtest.end_date
backtest_config.capital       →   backtest.capital
backtest_config.benchmark     →   backtest.benchmark
slots.risk.params             →   objective.hard_constraints
slots.alpha.composer_config   →   objective.weights (间接)
[新增] gene_references        →   gene_references (基因血统)
[新增] gene_search_space      →   gene_search_space.json (独立文件)
```

---

## 8. 基因分类体系

```
Gene Taxonomy (基因分类树)
│
├── alpha/ (选股信号)
│   ├── factor_based/          # 因子类
│   │   ├── value/             # 价值因子 (PB, PE, ...)
│   │   ├── quality/           # 质量因子 (ROE, F-Score, ...)
│   │   ├── momentum/          # 动量因子
│   │   └── growth/            # 成长因子
│   ├── signal_based/          # 信号类
│   │   ├── trend/             # 趋势信号 (MACD, Alligator, ...)
│   │   ├── volatility/        # 波动率信号
│   │   └── volume/            # 量能信号
│   └── ml_based/              # 机器学习类
│       ├── rf_score/          # 随机森林评分
│       └── xgb_score/         # XGBoost 评分
│
├── regime/ (择时门控)
│   ├── breadth/               # 市场宽度
│   ├── crowding/              # 拥挤度
│   ├── volatility/            # 波动率状态
│   ├── momentum/              # 动量趋势
│   └── sentiment/             # 情绪指标 (CVIX, ...)
│
├── preprocess/ (因子加工)
│   ├── winsorize/             # 去极值方法
│   ├── standardize/           # 标准化方法
│   └── scoring/               # 评分方法
│
├── universe/ (股票池)
│   ├── index_member/          # 指数成分股
│   ├── custom_filter/         # 自定义筛选
│   └── liquidity_gate/        # 流动性门槛
│
├── portfolio/ (组合构建)
│   ├── equal_weight/          # 等权
│   ├── score_weight/          # 评分加权
│   └── risk_parity/           # 风险平价
│
├── risk/ (风控规则)
│   ├── drawdown/              # 回撤控制
│   ├── concentration/         # 集中度限制
│   ├── var/                   # VaR 控制
│   └── stop_loss/             # 止损规则
│
└── execution/ (执行策略)
    ├── rebalance_weekly/      # 周度调仓
    ├── rebalance_monthly/     # 月度调仓
    └── threshold_rebalance/   # 阈值触发调仓
```

---

## 9. 存储结构

```
strategy_kits/gene_library/
├── __init__.py
├── gene_schema.py              # 数据模型
├── gene_registry.py            # 注册中心
├── gene_extractor.py           # 提取器
├── gene_compiler.py            # 编译器
├── gene_scorer.py              # 质量评估
├── gene_operators.py           # 进化算子
│
├── genes/                      # 基因存储
│   ├── index.json              # 全局索引
│   ├── alpha/
│   │   ├── alpha_rfscore7_v2.json
│   │   └── alpha_pb_factor_v1.json
│   ├── regime/
│   │   ├── regime_breadth_v3.json
│   │   └── regime_cvix_v1.json
│   ├── preprocess/
│   ├── universe/
│   ├── portfolio/
│   ├── risk/
│   └── execution/
│
├── genotypes/                  # 基因型存储
│   ├── gt_rfscore7_champion.json
│   └── gt_auto_suggested_001.json
│
└── templates/                  # 策略代码模板
    ├── rq_strategy.py.j2       # RiceQuant 模板
    ├── jq_strategy.py.j2       # JoinQuant 模板
    └── bt_strategy.py.j2       # Backtrader 模板

autoresearch/
├── bridge.py                   # 桥接层（新增）
├── setup.py                    # 修改：支持 --from-genotype
├── run_iteration.py            # 修改：读取 gene_search_space.json
└── [其余文件不变]
```

---

## 10. 基因进化算子

**文件位置**: `strategy_kits/gene_library/gene_operators.py`

```python
"""基因进化算子 — 变异、交叉、选择"""

import random
import copy
from typing import List, Optional, Tuple

from .gene_schema import Gene, Genotype, GeneSlot, SlotConfig, ComposerMethod, ParamSpec


class MutationOperator:
    """
    基因变异算子。

    变异类型:
    1. param_tweak — 在 ParamSpec.range 内微调单个参数
    2. param_reset — 将参数重置为范围内的随机值
    3. gene_swap   — 替换某个 slot 的基因为基因库中同 slot 的其他基因
    """

    def param_tweak(self, gene: Gene, param_name: str, direction: int = 0) -> Gene:
        """
        微调单个参数。

        Args:
            gene: 原始基因
            param_name: 参数名
            direction: 0=随机, 1=增大, -1=减小

        Returns:
            变异后的新 Gene（不修改原始对象）
        """
        mutated = copy.deepcopy(gene)
        spec = mutated.params.get(param_name)
        if spec is None or spec.range is None:
            return mutated

        step = spec.step or (spec.range[1] - spec.range[0]) * 0.1
        if direction == 0:
            direction = random.choice([-1, 1])

        new_val = spec.value + direction * step

        # 钳位到合法范围
        new_val = max(spec.range[0], min(spec.range[1], new_val))
        if spec.dtype == "int":
            new_val = int(round(new_val))

        spec.value = new_val
        # 更新 gene_id 版本后缀
        mutated.version = self._bump_version(mutated.version)
        return mutated

    def param_reset(self, gene: Gene, param_name: str) -> Gene:
        """将参数重置为范围内的随机值"""
        mutated = copy.deepcopy(gene)
        spec = mutated.params.get(param_name)
        if spec is None:
            return mutated

        if spec.choices:
            spec.value = random.choice(spec.choices)
        elif spec.range:
            if spec.dtype == "int":
                spec.value = random.randint(int(spec.range[0]), int(spec.range[1]))
            elif spec.dtype == "float":
                spec.value = round(random.uniform(spec.range[0], spec.range[1]), 4)

        mutated.version = self._bump_version(mutated.version)
        return mutated

    @staticmethod
    def _bump_version(version: str) -> str:
        parts = version.split(".")
        parts[-1] = str(int(parts[-1]) + 1)
        return ".".join(parts)


class CrossoverOperator:
    """
    基因型交叉算子。

    交叉类型:
    1. slot_swap   — 交换两个 Genotype 的某个 slot
    2. param_blend — 同 slot 同基因，取两个版本的参数中间值
    """

    def slot_swap(
        self,
        parent_a: Genotype,
        parent_b: Genotype,
        swap_slots: List[str],
    ) -> Genotype:
        """
        交换指定 slot 的基因配置。

        Example:
            parent_a 的 alpha + parent_b 的 regime → child

        Args:
            parent_a: 父本 A
            parent_b: 父本 B
            swap_slots: 从 parent_b 取用的 slot 名列表
        """
        child = copy.deepcopy(parent_a)
        child.genotype_id = f"cross_{parent_a.genotype_id[:8]}_{parent_b.genotype_id[:8]}"
        child.parent_genotype = parent_a.genotype_id
        child.generation = max(parent_a.generation, parent_b.generation) + 1

        for slot_name in swap_slots:
            if slot_name in parent_b.slots:
                child.slots[slot_name] = copy.deepcopy(parent_b.slots[slot_name])

        return child

    def param_blend(
        self,
        gene_a: Gene,
        gene_b: Gene,
        blend_ratio: float = 0.5,
    ) -> Gene:
        """
        参数混合 — 取两个基因的参数加权平均。

        仅对数值型参数有效。

        Args:
            gene_a, gene_b: 同 slot 同类基因
            blend_ratio: gene_a 的权重，gene_b = 1 - blend_ratio
        """
        blended = copy.deepcopy(gene_a)
        blended.gene_id = f"blend_{gene_a.gene_id[:12]}_{gene_b.gene_id[:12]}"

        for name, spec_a in blended.params.items():
            spec_b = gene_b.params.get(name)
            if spec_b is None:
                continue

            if spec_a.dtype in ("int", "float"):
                blended_val = spec_a.value * blend_ratio + spec_b.value * (1 - blend_ratio)
                if spec_a.dtype == "int":
                    blended_val = int(round(blended_val))
                spec_a.value = blended_val

        return blended


class SelectionOperator:
    """
    基因选择算子。

    选择策略:
    1. tournament — 锦标赛选择
    2. elite      — 精英保留
    """

    def tournament(
        self,
        candidates: List[Gene],
        k: int = 3,
    ) -> Gene:
        """锦标赛选择：随机取 k 个，返回 fitness 最高的"""
        selected = random.sample(candidates, min(k, len(candidates)))
        return max(selected, key=lambda g: g.quality.fitness_score)

    def elite(
        self,
        candidates: List[Gene],
        top_n: int = 5,
    ) -> List[Gene]:
        """精英保留：返回 fitness 最高的 top_n 个"""
        sorted_genes = sorted(candidates, key=lambda g: g.quality.fitness_score, reverse=True)
        return sorted_genes[:top_n]
```

---

## 11. 过拟合防护机制

这是整个系统最重要的安全保障。当前 autoresearch 在 1 年窗口上迭代 28 轮、score 翻 5 倍，大概率已经过拟合。基因库必须内建多层防护。

### 11.1 防护层级

```
Layer 1: 单基因层面
  ├── 参数稳定性测试 (gene_scorer.run_stability_test)
  │   → 参数 ±10% 扰动后 score 标准差 < 阈值才入库
  └── OOS 交叉验证 (gene_scorer.run_oos_test)
      → 至少在 1 个 OOS 窗口上 score > 0

Layer 2: 基因型层面
  ├── 多窗口回测
  │   → 编译后的策略必须在 ≥ 2 个不重叠时间窗口上得分为正
  └── 复杂度惩罚
      → Genotype 使用的基因数量纳入 score 公式作为正则化项

Layer 3: 基因库层面
  ├── 基因淘汰机制
  │   → 连续 N 次在新实验中表现不佳的基因降权或淘汰
  └── 多样性保护
      → 同一 slot 不允许所有基因都来自同一实验
```

### 11.2 OOS 验证方案

```python
# OOS 时间窗口推荐方案（以沪深300为例）

OOS_WINDOWS = [
    # 窗口 1: 训练期后的半年（最直接的泛化检验）
    {"name": "forward_6m", "start": "2026-04-01", "end": "2026-09-30"},

    # 窗口 2: 训练期前的一年（检验策略在不同市况下的表现）
    {"name": "backward_1y", "start": "2024-04-01", "end": "2025-04-01"},

    # 窗口 3: 2022 年熊市（极端市况压力测试）
    {"name": "bear_2022", "start": "2022-01-01", "end": "2022-12-31"},

    # 窗口 4: 2020 年牛市（顺势市况表现）
    {"name": "bull_2020", "start": "2020-07-01", "end": "2021-06-30"},
]

# OOS 质量分计算
def calculate_oos_score(window_scores: List[float]) -> float:
    """
    OOS 综合分。

    规则:
    - 所有窗口得分的调和平均（对差值敏感）
    - 如果任一窗口得分 < 0，直接判定为不合格
    """
    if any(s < 0 for s in window_scores):
        return -1.0  # 不合格
    if not window_scores:
        return 0.0
    # 调和平均
    return len(window_scores) / sum(1.0 / max(s, 0.001) for s in window_scores)
```

### 11.3 复杂度惩罚

```python
# 在 scorer.py 的 calculate_score() 中增加复杂度惩罚项

def calculate_score_with_complexity(
    metrics: ParsedMetrics,
    genotype: Optional[Genotype] = None,
    complexity_lambda: float = 0.02,
) -> float:
    """
    带复杂度惩罚的评分。

    score = base_score - complexity_lambda * complexity

    complexity 计算:
    - 基因数量 (每多一个基因 +1)
    - 参数数量 (每多一个参数 +0.5)
    - slot 覆盖数量 (每多一个 slot +0.5)
    """
    base_score = calculate_score(metrics)

    if genotype is None:
        return base_score

    n_genes = len(genotype.get_all_gene_ids())
    n_params = sum(
        len(gene.params)
        for gene in [registry.get(gid) for gid in genotype.get_all_gene_ids()]
    )
    n_slots = len(genotype.slots)

    complexity = n_genes * 1.0 + n_params * 0.5 + n_slots * 0.5
    penalty = complexity_lambda * complexity

    return base_score - penalty
```

### 11.4 基因淘汰机制

```python
# 在 GeneRegistry 中增加淘汰逻辑

def decay_and_prune(self, min_quality: float = 0.1) -> List[str]:
    """
    衰减和淘汰低质量基因。

    规则:
    1. 每次新实验完成后调用
    2. 未在最近 5 个实验中被使用的基因，fitness 衰减 10%
    3. fitness < min_quality 的基因标记为 deprecated
    4. deprecated 超过 30 天的基因物理删除

    Returns:
        被淘汰的 gene_id 列表
    """
    pruned = []
    for gene_id, info in self._index.items():
        # 衰减未使用的基因
        if info.get("last_used_experiment_age", 0) > 5:
            info["fitness"] *= 0.9

        # 标记低质量基因
        if info.get("fitness", 0) < min_quality:
            pruned.append(gene_id)

    for gene_id in pruned:
        self.remove(gene_id)

    return pruned
```

---

## 12. 实施路线图

### Phase 0: 评分对齐（1-2 天）— 前置修复

**目标**: 解决 scorer.py / program.md / seed_config.json 三处评分公式不一致问题。

| 任务 | 详情 |
|------|------|
| 统一评分公式 | 以 `scorer.py` 的 calmar/sortino/IR 公式为准，更新 `program.md` 和 `seed_config.json` |
| 配置驱动化 | `calculate_score()` 的权重从 `seed_config.json` 读取，消除硬编码 |
| 清理 ledger.py | 决定整合还是删除（推荐删除，现有 history/ 方案更简洁） |

### Phase 1: 基因数据模型 + 提取器（3-5 天）

**目标**: 能从现有实验中提取基因并存储。

| 任务 | 输出 |
|------|------|
| 实现 `gene_schema.py` | Gene / Genotype / ParamSpec 数据类 |
| 实现 `gene_registry.py` | 基因 CRUD + 查询 |
| 实现 `gene_extractor.py` | 从 rfscore7_pb10_enhanced 实验提取 champion 基因 |
| 验证 | 成功提取并存储 ≥ 3 个基因（alpha、regime、portfolio） |

**验收标准**: 运行 `gene_extractor` 后，`genes/` 目录下有正确的 JSON 文件。

### Phase 2: 基因编译器 + 桥接层（5-7 天）

**目标**: 能从基因库编译出可运行的策略。

| 任务 | 输出 |
|------|------|
| 实现 `gene_compiler.py` | compile_to_task_spec() + compile_to_rq_strategy() |
| 编写 RQ 策略模板 | `templates/rq_strategy.py.j2` |
| 实现 `bridge.py` | autoresearch 桥接层 |
| 修改 `setup.py` | 支持 `--from-genotype` 参数 |
| 生成 `gene_search_space.json` | Agent 可参考的结构化搜索空间 |

**验收标准**: 从基因库编译出的 strategy.py 能在 RiceQuant 上成功回测。

### Phase 3: OOS 验证 + 质量评估（3-5 天）

**目标**: 基因入库前必须通过 OOS 验证。

| 任务 | 输出 |
|------|------|
| 实现 `gene_scorer.py` | 多维度质量评估 |
| 实现 OOS 验证流程 | 至少 2 个 OOS 窗口 |
| 实现参数稳定性测试 | ±10% 扰动测试 |
| 将 OOS score 写入 GeneQuality | 基因入库条件 |

**验收标准**: 当前 champion 的基因通过 OOS 验证，OOS score > 0。

### Phase 4: 进化算子 + Agent 集成（5-7 天）

**目标**: autoresearch Agent 能基于基因库进行结构化搜索。

| 任务 | 输出 |
|------|------|
| 实现 `gene_operators.py` | 变异、交叉、选择算子 |
| 修改 `program.md` | Agent 指令包含基因搜索空间引导 |
| 修改 `run_iteration.py` | 迭代后自动调用 `bridge.deposit_genes()` |
| 集成 `get_search_hints()` | Agent 每轮可参考已失败方向 |

**验收标准**: 新实验的迭代成功率从 14% 提升到 ≥ 25%。

### Phase 5: 跨实验基因迁移（持续）

**目标**: 基因可以在不同策略之间复用。

| 任务 | 输出 |
|------|------|
| 第二个实验使用基因库 | 验证跨策略迁移 |
| 基因淘汰机制 | 低质量基因自动清理 |
| 基因库仪表盘 | 可视化基因分布、质量、使用频率 |

---

## 13. 风险与约束

### 13.1 技术风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| AST 提取不准确 | 中 | 基因参数错误 | 提取后人工 review 前几个基因 |
| Jinja2 模板生成的代码有语法错误 | 中 | 编译失败 | preflight_checker 已有语法检查 |
| OOS 窗口选择偏差 | 低 | OOS 分数不可靠 | 使用 ≥ 3 个不重叠窗口 |
| 基因库膨胀 | 中 | 查询变慢 | 淘汰机制 + 版本合并 |
| RiceQuant API 限流 | 高 | OOS 验证变慢 | 批量提交 + 缓存结果 |

### 13.2 设计约束

| 约束 | 原因 |
|------|------|
| 基因文件必须是 JSON | git 友好，人类可读 |
| 基因库不依赖外部数据库 | 保持单仓库部署简单性 |
| 必须兼容现有 autoresearch 迭代流程 | 渐进式改造，不破坏已有功能 |
| Phase 1-2 不修改 run_iteration.py 核心逻辑 | 降低风险，先验证数据模型 |

### 13.3 不做什么

| 不做 | 原因 |
|------|------|
| 不建独立的回测引擎 | 复用 strategy_kits backtrader_runtime + RiceQuant |
| 不做 GUI | 当前用 JSON + CLI 足够，GUI 是 Phase 5+ |
| 不做多目标优化 | 保持 composite score 单目标，已通过权重体现多目标 |
| 不做实时基因学习 | 离线提取 + 注册已足够，实时学习复杂度太高 |

---

> **下一步行动**: 完成 Phase 0（评分对齐），然后从 Phase 1 的 gene_schema.py 开始实现。

# ECC 深度分析报告：Instinct 记忆系统 & Skills 分类体系

> 研究日期：2026-07-10 | 来源版本：ECC v2.0.0-rc.1 (affaan-m/everything-claude-code)

---

## 第一部分：ECC Instinct 记忆系统深度拆解

### 1.1 架构总览

ECC 的记忆系统不叫 "Memory" 而叫 **Instinct（本能）**，这是它最关键的设计区别。它不是存对话记录，而是**自动提取行为模式**。

```
用户操作 → Hooks 捕获(PreToolUse/PostToolUse) 
         → Observer Agent (Haiku) 后台分析 
         → 发现重复模式 → 生成 Instinct YAML 
         → 存入 ~/.local/share/ecc-homunculus/
         → 高置信度(≥0.7)自动注入会话上下文
```

### 1.2 Instinct YAML 数据结构

每个 instinct 是一个独立的 YAML 文件，核心字段：

```yaml
id: prefer-functional-style        # 唯一标识符
trigger: "when writing new functions"  # 触发条件（自然语言）
confidence: 0.7                    # 置信度 0.0-1.0
domain: "code-style"               # 领域标签
source: "session-observation"      # 来源
scope: project                     # project | global | all
project_id: "<hash>"               # 项目隔离用
project_name: "my-react-app"
---
## Action
Use functional patterns over classes when appropriate.

## Evidence
- Observed 5 instances of functional pattern preference
- User corrected class-based approach to functional on 2025-01-15
```

**设计亮点：**
- **Atom（原子化）** — 一个 trigger 对应一个 action，不混绑
- **Evidence 追溯** — 每条 instinct 记录观测证据，不是凭空产生
- **Domain 标签** — 支持按领域筛选（code-style / testing / git / workflow）

### 1.3 置信度评分算法

| 分值 | 含义 | 行为 |
|------|------|------|
| 0.3 | Tentative（尝试性） | 建议但不强制 |
| 0.5 | Moderate（中等） | 场景匹配时应用 |
| 0.7 | Strong（强） | **自动批准**融入默认行为 |
| 0.9 | Near-certain（近乎确定） | 核心行为，始终生效 |

**置信度增减规则：**

| 增信 | 降信 |
|------|------|
| 模式被重复观测 | 用户明确纠正 |
| 用户不否定建议的行为 | 长时间未被观测 |
| 多个相似 instinct 一致 | 出现矛盾证据 |

**关键算法 — 半衰期衰减（Staleness Decay）：**

ECC 的置信度不是静态的，而是带时间衰减的：

```
confidence_effective = confidence_raw × decay_factor(time_since_last_observed)
```

- 每次 export 时，导出的是 **effective（已衰减）** 值，不是原始值
- 导入方得到一个 "honest, time-adjusted score"
- `--min-confidence <f>` 参数可以过滤低有效分 instinct

**这意味着：** 一个 0.9 的 instinct 如果半年没触发，导出来可能只剩 0.4，自动降权。这是 Cowork 现有记忆体系完全没有的机制。

### 1.4 项目隔离（v2.1 关键升级）

| 维度 | v2.0 | v2.1 |
|------|------|------|
| 存储位置 | 全局 `~/.claude/homunculus/` | 项目级 `${XDG_DATA_HOME}/ecc-homunculus/projects/<hash>/` |
| 作用域 | 所有 instinct 全局生效 | 项目级 + 全局隔离 |
| 项目检测 | 无 | git remote URL / 路径 hash |
| 跨项目 | 互相污染 | **默认隔离** |
| 共享规则 | N/A | 在 2+ 项目中出现的 instinct → 自动提升为 global |

**项目检测优先级链：**
1. `CLAUDE_PROJECT_DIR` 环境变量（最高优先）
2. `git remote get-url origin` → hash 生成可移植项目 ID
3. `git rev-parse --show-toplevel` → 机器级 fallback
4. 全局 fallback（无项目检测时）

### 1.5 8 种 Hooks 生命周期

这是 ECC 记忆系统的**基础设施层**，hooks 是 instinct 的数据来源和执行网关：

| 钩子 | 触发时机 | 可阻断 | 记忆相关用途 |
|------|---------|--------|-------------|
| **SessionStart** | 会话初始化 | 否 | 加载历史上下文、注入高置信 instinct |
| **PreToolUse** | 工具执行前 | 是(exit 2) | 安全验证、强制先研究 |
| **PostToolUse** | 工具执行后 | 否 | lint/格式化、**观测学习** |
| **Stop** | Claude 响应完成 | 否 | 桌面通知、**会话摘要提取** |
| **PreCompact** | 上下文压缩前 | 否 | **保存关键状态**防止丢失 |
| **SessionEnd** | 会话终止 | 否 | 最终清理、状态终结 |
| **UserPromptSubmit** | 用户提交消息 | 是 | 输入消毒、注入额外上下文 |
| **Notification** | Agent 状态通知 | 否 | 向外部系统发状态 |

**三条钩子实现跨会话记忆（三钩组合）：**
1. **PreCompact** → 提取关键决策/代码模式 → 存 `memory.md`
2. **Stop** → 写会话摘要 → 追加到长期记忆文件
3. **SessionStart** → 加载 `memory.md` → 通过 stdout 注入上下文

### 1.6 Instinct → Skill 进化管道

ECC 最精妙的设计：**instinct 不是终点，而是原材料**

```
Instinct (0.3-0.5) → 重复观测增信 → Instinct (0.7+) 
  → /evolve 命令 → 聚类同类 instinct 
  → 生成 SKILL.md → 注册为新 Skill
  → 或生成 agent 定义 / command 脚本
```

这是从"被动学习"到"主动封装"的进化闭环。低分 instinct 用 `/prune` 自动清理（30 天 TTL）。

### 1.7 已知问题

GitHub Issue #1231 指出：instinct 目前**只存不用** — 存好了但不会主动注入会话上下文。生命周期 incomplete：
```
✅ 观测 → ✅ 提取 → ✅ 存储 → ❌ 注入上下文 → ❌ 执行
```
修复方案：在 SessionStart hook 中通过 `additionalContext` 机制注入 ≥0.7 的 instinct。

---

## 第二部分：Cowork 记忆体系 vs ECC Instinct — 对比与借鉴

### 2.1 对比矩阵

| 维度 | Cowork 记忆体系 | ECC Instinct |
|------|----------------|-------------|
| **存什么** | 用户画像、项目状态、反馈偏好、参考指针 | 原子行为模式（one trigger, one action） |
| **粒度** | 文档级（每篇 .md 200-500 字） | 原子级（每条 10-20 行 YAML） |
| **如何产生** | 手动触发或我主动写 | **全自动**hooks 观测 + background agent 分析 |
| **置信度** | 无（靠时效性暗示） | 0.0-1.0 数值化 + 半衰期衰减 |
| **项目隔离** | 无（所有 memory 全局） | 项目级 hash 隔离 + 跨项目自动提升 |
| **过期清理** | 手动（无自动化） | `/prune` 命令，30 天 TTL |
| **团队共享** | 无 | `instinct-export` + `instinct-import` |
| **进化能力** | 无 | `/evolve` → 从 instinct 自动生成 Skill |
| **注入机制** | MEMORY.md 全程在上下文 | SessionStart hook 动态注入 ≥0.7 的 instinct |

### 2.2 可借鉴的设计

**借鉴点 1：置信度评分 + 半衰期衰减**

当前问题：所有 memory 在上下文中权重相同，旧的错误记忆也可能影响判断。
改进方向：每条 memory 加 `confidence` 和 `last_verified` 字段，读取时按时间衰减计算有效分。

**借鉴点 2：项目隔离**

当前问题：你在 React 项目里积累的记忆会污染 Python 项目。
改进方向：为不同类型的工作（股票分析 vs 内容创作 vs 系统搭建）建立隔离空间，只在匹配上下文中加载。

**借鉴点 3：Hooks 自动观测**

ECC 的 PostToolUse hook 是 instinct 的数据来源。Cowork 目前没有等效机制——每次学到的东西都靠我主动写 memory。
改进思路：无法直接实现（需要底层 hooks 支持），但可以通过**任务完成后的 reflection 流程半自动化**，把复盘结果自动 pipeline 进 memory 系统。

**借鉴点 4：Instinct → Skill 进化管道**

ECC 的 `/evolve` 把高置信 instinct 自动封装为 Skill。
对应到 Cowork：如果某个操作模式被反复使用（比如"分析涨停股前先跑 auction-battle"），可以自动建议生成一个编排型 Skill。

---

## 第三部分：ECC Skills 分类体系深度分析

### 3.1 5 大分类体系

ECC 将 182 个技能分为 5 大类别：

```
skills/
├── Language Standards/        # 语言习语与规范
│   ├── coding-standards/      # 通用编码标准
│   ├── python-patterns/       # Python 习语
│   ├── golang-patterns/       # Go 习语
│   ├── java-coding-standards/ # Java 规范
│   ├── cpp-coding-standards/  # C++ Core Guidelines
│   ├── perl-patterns/         # Perl 5.36+
│   └── swift-*/               # Swift 并发/协议/持久化
│
├── Framework Patterns/        # 框架级模式
│   ├── frontend-patterns/     # React, Next.js
│   ├── backend-patterns/      # API, DB, 缓存
│   ├── django-*/              # Django 模式/安全/TDD/验证
│   ├── springboot-*/          # Spring Boot 四件套
│   ├── laravel-*/             # Laravel 四件套
│   ├── quarkus-*/             # Quarkus 四件套
│   └── nestjs-patterns/       # NestJS
│
├── Workflow/                  # 开发流程
│   ├── tdd-workflow/          # RED-GREEN-REFACTOR
│   ├── search-first/          # 先研究后编码
│   ├── strategic-compact/     # 手动上下文压缩
│   ├── iterative-retrieval/   # 渐进式上下文优化
│   └── autonomous-loops/      # 自主循环（PR/DAG）
│
├── Domain Knowledge/          # 领域专知
│   ├── security-review/       # 安全检查清单
│   ├── security-scan/         # AgentShield 审计
│   ├── api-design/            # REST API 设计
│   ├── database-migrations/   # 数据库迁移
│   ├── postgres-patterns/     # PostgreSQL 优化
│   ├── deployment-patterns/   # CI/CD / Docker
│   ├── docker-patterns/       # Docker Compose
│   ├── e2e-testing/           # Playwright E2E
│   ├── clickhouse-io/         # ClickHouse 分析
│   ├── videodb/               # 视频/音频处理
│   └── healthcare-*/          # 医疗 HIPAA 合规
│
├── Tool Integration/          # 工具集成
│   ├── eval-harness/          # 评估框架
│   ├── verification-loop/     # 验证循环
│   ├── agent-eval/            # Agent 对比评估
│   ├── plankton-code-quality/ # 实时代码质量
│   ├── cost-aware-llm-pipeline/  # Token 成本优化
│   ├── content-hash-cache-pattern/ # 缓存策略
│   └── regex-vs-llm-structured-text/ # 解析策略决策
│
├── [Business & Content]       # 商业与内容（跨类别）
│   ├── article-writing/       # 长文写作
│   ├── content-engine/        # 多平台内容分发
│   ├── market-research/       # 市场/竞品研究
│   ├── investor-materials/    # 投资者材料
│   └── frontend-slides/       # HTML 演示文稿
│
└── [Learning & Evolution]     # 学习与进化（跨类别）
    ├── continuous-learning/   # 自动模式提取 v1
    ├── continuous-learning-v2/# instinct 基础学习 v2
    └── skill-stocktake/       # 技能质量审计
```

### 3.2 ECC 每个框架的"四件套"模式

ECC 对主流框架的一致化处理值得学习。每个框架都有标准化的四件套：

| 框架 | Patterns | Security | TDD | Verification |
|------|----------|----------|-----|-------------|
| Django | ✅ | ✅ | ✅ | ✅ |
| Spring Boot | ✅ | ✅ | ✅ | ✅ |
| Laravel | ✅ | ✅ | ✅ | ✅ |
| Quarkus | ✅ | ✅ | ✅ | ✅ |

**命名规范：** `{framework}-{module}`，一目了然。

### 3.3 技能内部结构

每个 ECC Skill 目录结构：

```
skills/your-skill-name/
├── SKILL.md           # 必需：主定义
├── examples/          # 可选：代码示例
└── references/        # 可选：外部文档链接
```

SKILL.md 内部模板：

```yaml
---
name: "tdd-workflow"
description: "RED-GREEN-REFACTOR cycle, 80%+ coverage"
origin: "ecc"
tags: ["testing", "workflow"]
---
# TDD Workflow

## When to Activate
When implementing new features or fixing bugs that need tests first.

## Core Concepts
- RED: Write failing test first
- GREEN: Write minimal code to pass
- REFACTOR: Clean up while keeping tests green

## Code Examples
...（省略）

## Anti-Patterns
- Writing tests after code ( defeats TDD purpose )
- 100% coverage obsession

## Best Practices
- One assertion per test
- Test behavior, not implementation

## Related Skills
- e2e-testing, verification-loop
```

---

## 第四部分：当前 Cowork 技能目录与 ECC 的对比

### 4.1 当前技能生态（来自 memory）

从 skill-ecosystem-v7 看，当前 Cowork 有约 19 个股票分析 Skill + 创作类 Skill，整体约 **40-50 个有效 Skill**，按冰山风格分三大域：

| 领域 | 代表 Skill |
|------|-----------|
| **交易** | trader, auction-battle, limit-up, stock-volume, intraday, buy-and-sell, trading-secret-language, break-fake-break... |
| **分析** | analyst, senior-analyst, analyst-workflow, valuation, comps, red-team, deepdive, capital-chess... |
| **创作** | writing, de-ai, md-to-html, translator, publisher, baoyu-*... |

### 4.2 ECC vs Cowork 技能体系对比

| 维度 | ECC (182 Skills) | Cowork (~50 Skills) |
|------|------------------|---------------------|
| **分类体系** | 5 大类别，清晰分层 | 三域自然分类，但缺乏正式分类框架 |
| **数量** | 182（含大量语言/框架技能） | ~50（聚焦交易+分析+创作） |
| **语言/框架覆盖** | 12+ 语言、8+ 框架，每框架四件套 | 无（领域特殊） |
| **SKILL.md 标准** | 统一模板：frontmatter + 7 个标准章节 | 各 Skill 风格不一 |
| **tags 系统** | 支持 tags 元数据 | 无 tags |
| **相关技能链接** | 每个 Skill 有 Related Skills | 无 |
| **例目录** | examples/ + references/ 辅助目录 | 纯 SKILL.md |
| **自动激活** | 靠 description 由 LLM 自行判断 | 靠 /slash 手动调用 |
| **版本管理** | origin + 版本号 | 无 |
| **反模式章节** | 每个 Skill 有 Anti-Patterns | 很少 |

### 4.3 ECC 值得借鉴的分类优化建议

**建议 1：引入 tags 元数据体系**

当前所有 Skill 的 frontmatter 只有 name + description。加入 tags 可以实现按标签筛选和关联。

```yaml
---
name: "limit-up"
description: "A股涨停分析 — 竞价评分、Pattern识别、陷阱过滤"
tags: ["stock", "limit-up", "trading", "a-share", "zh-CN"]
---
```

**建议 2：统一 SKILL.md 模板**

ECC 的 7 节标准结构（When to Activate / Core Concepts / Code Examples / Anti-Patterns / Best Practices / Related Skills）可以直接借鉴。特别是 **Anti-Patterns** 和 **Related Skills** 两个当前缺失的章节。

**建议 3：建立技能目录索引**

ECC 的技能在 README 和 DeepWiki 中有完整索引。当前 Cowork 技能靠 `/console` 面板导航，但缺少一个类似 ECC 的 SKILLS-REFERENCE 文档来展示所有技能的层级关系。

**建议 4：框架标准化**（针对交易/分析技能）

ECC 对每个框架做"四件套"。可以类比到交易域：
| 核心股票 | 形态分析 | TDD-like | 验证 |
|---------|---------|----------|------|
| 量价分析 | 分时形态 | 买入验证 | 风险审查 |
| buy-and-sell | intraday-shape-master | break-fake-break | risk-announce |
| stock-volume | limit-up-down-patterns | 不破确认 | reduction-analysis |

这样可以发现：**验证环节**当前较弱（break-fake-break 只是真假突破，缺少通用的"买入逻辑验证"技能）。

---

## 第五部分：总结与行动建议

### 5.1 记忆系统建议

1. **[即时可用] 给 memory 加 confidence/decay** — 每条 memory 前加 `confidence: 0.8` 和 `last_verified: 2026-07-10`，读取时按时间决定权重
2. **[即时可用] 项目级 memory 隔离** — 当前 MEMORY.md 中已有 iceber-style / skill-ecosystem / content-pipeline 不同主题，可以在 memory 中加 `scope: trading | creation | system ` 字段，按当前任务类型选择性加载
3. **[中期] 建立 instinct 类似机制** — 在 reflection 流程中加入"观测 → 模式提取 → 写入 memory"的半自动化 pipeline（虽然做不到 ECC 的 hooks 全自动，但可以用 structured reflection 减少手动负担）
4. **[长期] /evolve 管道** — 如果发现某个 workflow 反复出现（如"分析涨停→查风险→出报告"），自动建议生成编排型 Skill

### 5.2 技能目录建议

1. **[立即] 优化所有 SKILL.md frontmatter** — 统一加入 tags、origin、version 字段
2. **[立即] 补充 Anti-Patterns 和 Related Skills 章节** — 从最常用 Skill 开始
3. **[短期] 建立分类目录文档** — 类似 ECC 的 Skills Reference，按 交易/分析/创作 三域列出所有技能及层级关系
4. **[短期] 模板标准化** — 制定 Cowork 内部 SKILL.md 标准模板，新 Skill 一律按模板生成

### 5.3 ECC 整体架构对 Cowork 的路线启发

```
ECC:            Skills(182) + Agents(67) + Hooks(8) + Instincts + Rules(34) + Commands(92)
Cowork(v7):     Skills(~50) + Subagents + Memory      + Skills(无hooks) + 无规则层
差距:           ⬆️技能数    ⬆️hooks机制  ⬆️instinct   ⬆️规则持久化  ⬆️命令体系

最有价值的借鉴排序:
1. ⭐ Instinct 置信度+半衰期 → memory 系统增强
2. ⭐ Hooks 三钩组合(PreCompact/Stop/SessionStart) → 跨会话记忆
3. ⭐ Anti-Patterns + Related Skills → SKILL.md 标准化
4. ⭐ tags 元数据体系 → 技能分类筛选
5. ⭐ 项目隔离 → 不同工作域的记忆隔离
```

---

## 参考资料

- [ECC GitHub Repository](https://github.com/affaan-m/ECC)
- [DeepWiki: ECC Skills Reference](https://deepwiki.com/affaan-m/everything-claude-code/5.2-skills-reference)
- [DeepWiki: Hook Lifecycle & Event Flow](https://deepwiki.com/affaan-m/everything-claude-code/6.1-hook-lifecycle-and-event-flow)
- [DeepWiki: Instinct & Session Management](https://deepwiki.com/mit-network/everything-claude-code/7.2-instinct-and-session-management)
- [ECC Shortform Guide](https://github.com/affaan-m/ECC/blob/main/the-shortform-guide.md)
- [ECC Continuous Learning v2 SKILL.md](https://github.com/affaan-m/ECC/blob/main/skills/continuous-learning-v2/SKILL.md)
- [ECC Issue #1231: Instincts not proactively injected](https://github.com/affaan-m/ECC/issues/1231)
- [ECC Issue #148: Instinct import bug](https://github.com/affaan-m/ECC/issues/148)
- [腾讯云: ECC 讲透](https://cloud.tencent.com.cn/developer/article/2674429)
- [CSDN 23万星标争夺战](http://mp.weixin.qq.com/s?__biz=MzkwMDI4NTU2Nw==&mid=2247483739&idx=1&sn=7717f02aa20b7626a14333d662e57494)
- [DataCamp: ECC Tutorial](https://www.datacamp.com/tutorial/everything-claude-code)

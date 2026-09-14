# Cowork Skill 分类目录 v7.2

> 参考 ECC 5 大分类体系，将当前 Cowork 环境所有 Skill 按 **交易 / 分析 / 创作 / 通用** 四域归类。
> 各域内进一步细分二级类别，便于按场景快速定位。
> 最后生成时间：2026-07-10

---

## 目录

1. [交易域](#1-交易域)
2. [分析域](#2-分析域)
3. [创作域](#3-创作域)
4. [通用域](#4-通用域)
5. [附录：标记为"已删除/已合并"的 Skill](#5-附录)

---

## 1. 交易域

### 1.1 入口路由

| Skill | 用法 | 说明 |
|-------|------|------|
| `/trader` | `/trader` | 交易员入口角色包，路由到分时/资金/买卖点/主力成本/暗语等子技能 |
| `/stock` | `/stock` | 股票分析总入口 + 可视化导航面板，32+个技能分6类 |

### 1.2 大盘情绪

| Skill | 用法 | 说明 |
|-------|------|------|
| `/market-pulse` | `/market-pulse` 或 `/market-pulse 简报` | A股大盘情绪分析 + 晨间简报双模式 |
| `/hot-sector` | `/hot-sector` | 早盘热板与龙头识别（9:00-9:40） |

### 1.3 竞价与早盘

| Skill | 用法 | 说明 |
|-------|------|------|
| `/auction-battle` | `/auction-battle <代码>` | 集合竞价实战（9:15-9:25 压盘/拉盘/背离/诱多识别） |
| `/buy-and-sell` | `/buy-and-sell <代码>` | 开盘形态买入点/卖出点完整框架 |
| `/intraday` | `/intraday <代码>` | 分时走势预测（黄金30分钟+四大情景） |
| `/intraday-shape-master` | `/intraday-shape-master` | 分时线形状大师（26种经典形态） |
| `/limit-up` | `/limit-up <代码>` | A股涨停分析（竞价评分+Pattern+陷阱过滤） |
| `/limit-up-down-patterns` | `/limit-up-down-patterns <代码>` | 涨停跌停分时线模式识别（9大涨停+6大跌停） |

### 1.4 量价分析

| Skill | 用法 | 说明 |
|-------|------|------|
| `/stock-volume` | `/stock-volume <代码>` | 量价分析专家（量柱七君子+七大量线+19式+三长兄弟） |
| `/break-fake-break` | `/break-fake-break <代码>` | 真假突破/破位识别系统（四维诊断+洗盘vs出货） |
| `/volume-last-digit` | | 成交量末位数概率分布对倒检测 |

### 1.5 成交明细与暗语

| Skill | 用法 | 说明 |
|-------|------|------|
| `/trade-detail` | `/trade-detail <代码>` | A股成交明细分析（主力资金流向+暗盘资金） |
| `/trading-secret-language` | | 主力交易暗语破译系统（拆单/对倒/试盘/护盘等13种） |
| `/capital-chess` | | A股主力成本计算与阶段判断（7种成本算法+四阶段定位） |
| `/key-level-battle` | | 关键价位攻守分析（日K+分时成交明细联动） |

### 1.6 选股与推荐

| Skill | 用法 | 说明 |
|-------|------|------|
| `/stock-report` | `/stock-report <代码>` | A股个股买入推荐 + 板块扫描选股（已合并 stock-recommendation-report） |
| `/demon-stocks` | | A股妖股推荐（连板逻辑+评分模型）（已合并 yaogu-recommend + market-leading-stock + stop-high） |
| `/yaogu-judge` | `/yaogu-judge <代码>` | 妖股判断（九大维度41分评分系统） |
| `/second-board-factor` | | 二板涨停因子评分系统（12维PCA因子编码） |

### 1.7 做T与调仓

| Skill | 用法 | 说明 |
|-------|------|------|
| `/intraday-t` | `/intraday-t <代码>` | 个股盘中做T策略（涨停迹象+暗语验证+不破确认） |
| `/rotate-stock` | | 调仓换股决策系统（龙头切换+分歧转一致+交易心理自检） |
| `/buy-at-last` | | 尾盘30分钟买入法（尾盘拉升识别+五种形态+仓位管理） |

### 1.8 风险与公告

| Skill | 用法 | 说明 |
|-------|------|------|
| `/risk-announce` | `/risk-announce <代码>` | A股全链路风险排查（九维扫描+12大跌类型+利空出尽五问） |
| `/reduction-analysis` | `/reduction-analysis <代码>` | A股减持分析（减持阶段+股价高位/低位+可参与判断） |
| `/list-stock-announce` | `/list-stock-announce` | A股上市公司盘后公告收集整理（按四大类分类输出） |

### 1.9 价格与轨迹

| Skill | 用法 | 说明 |
|-------|------|------|
| `/price-range-traj` | | 价格区间与轨迹图（当日分时+支撑压力位+3日累计分时） |

### 1.10 量化

| Skill | 用法 | 说明 |
|-------|------|------|
| `/stock-quant` | `/stock-quant` | A股定量分析预测（7因子综合评分+IRCF多空博弈+4张图表） |

---

## 2. 分析域

### 2.1 入口路由

| Skill | 用法 | 说明 |
|-------|------|------|
| `/analyst` | `/analyst` | 分析师入口角色包，路由到深度分析/估值/压力测试等 |

### 2.2 深度分析流水线

| Skill | 用法 | 说明 |
|-------|------|------|
| `/senior-analyst` | `/senior-analyst` | 商业分析专家（28行业框架+L1/L2/L3三级深度+Council对抗审查） |
| `/analyst-workflow` | `/analyst-workflow <代码>` | 一键深度分析流水线（L1速查→L2定量→L3尽调+Council） |
| `/analyst-pipeline` | `/analyst-pipeline <代码>` | 三级深度分析管道（L1速查→deepdive六层挖→Council审） |
| `/deepdive` | `/deepdive <代码>` | 六层逆向挖掘框架（穿透表面信息被忽略的底层逻辑） |

### 2.3 估值与对标

| Skill | 用法 | 说明 |
|-------|------|------|
| `/valuation` | `/valuation` | 估值建模（DCF计算+敏感性分析表+PE估值） |
| `/comps` | `/comps` | 可比公司分析 + Tear Sheet（对标+指标对比+估值区间） |
| `/investment-banking` | | 投资银行工作台（Pitch Deck+Comps+DCF+尽调报告，一站式入口） |

### 2.4 压力测试与尽调

| Skill | 用法 | 说明 |
|-------|------|------|
| `/red-team` | `/red-team` | 交易/分析逻辑压力测试 + 尽职调查（4角色对抗审查） |
| `/cio-analyze` | `/cio-analyze <代码>` | CIO 多 Agent 自动分析（并行多维度分析+agent_outputs.json+仲裁） |

### 2.5 逆向验证

| Skill | 用法 | 说明 |
|-------|------|------|
| `/reverse-verify` | `/reverse-verify <代码>` | 反向验证（个股上涨逻辑+热点概念+主力行为，自动保存经验库） |

---

## 3. 创作域

### 3.1 写作

| Skill | 用法 | 说明 |
|-------|------|------|
| `/writing` | | 中考作文写作辅导（柳宁老师教学法） |
| `/novel-writing` | | 全题材短篇小说写作（仙侠/武侠/权谋/都市/科幻） |

### 3.2 去AI味

| Skill | 用法 | 说明 |
|-------|------|------|
| `/de-ai` | `/de-ai` | 中文 AI 去味工具（去 AI 腔+加语气词+句式多变） |

### 3.3 排版与发布

| Skill | 用法 | 说明 |
|-------|------|------|
| `/md-to-html` | `/md-to-html` | Markdown→公众号/知乎/HTML 排版（5种主题+外链转文末引用） |
| `/translator` | `/translator` | AI 翻译（先分析后翻译+受众适配+专业润色） |
| `/publisher` | | 跨平台内容发布（公众号/知乎/微博/雪球，长文+碎片双模式） |

### 3.4 配图与视觉

| Skill | 用法 | 说明 |
|-------|------|------|
| `/baoyu-cover-image` | | 文章封面图生成（五维定制：类型×配色×渲染×文字×氛围） |
| `/baoyu-article-illustrator` | | 文章配图（智能分析内容，自动生成和插入配图） |
| `/baoyu-infographic` | | 信息图生成（20种布局+17种风格） |
| `/baoyu-xhs-images` | | 小红书风格信息图生成 |
| `/baoyu-slide-deck` | | Markdown 文章→PPT 幻灯片 |
| `/thumbnail-polish` | | YouTube 缩图美化（排版+配色+视觉层级） |

### 3.5 创意与销售

| Skill | 用法 | 说明 |
|-------|------|------|
| `/creative-production` | | 创意制作（产品图+brief→情绪板+广告变体+场景图） |
| `/sales-plugin` | | 销售全流程（客户会议简报+跟进邮件+管道管理） |

---

## 4. 通用域

### 4.1 开发与工程

| Skill | 用法 | 说明 |
|-------|------|------|
| `/tdd` | | Red-Green-Refactor TDD 循环（Matt Pocock） |
| `/diagnose` | | 6步系统化 Bug 诊断循环（Matt Pocock） |
| `/grill-me` | | 深度追问工具，理清需求避免氛围编程（Matt Pocock） |
| `/write-a-prd` | | 结构化 PRD 生成（Matt Pocock） |
| `/handoff` | | 上下文交接文档生成（Matt Pocock） |
| `/improve-architecture` | | 深模块架构分析，扫描代码腐化 |
| `/setup-matt-pocock-skills` | | Matt Pocock Skills 项目集成工具 |
| `/code-simplify` | | AI 生成代码简化去赘余 |
| `/feature-dev` | | 7步功能开发流程（需求→探索→设计→实现→审查→文档） |
| `/commit-commands` | | Git 工作流自动化（智能提交+push-to-PR+清理） |
| `/gstack-review` | | 资深工程师代码审查 |
| `/gstack-qa` | | QA 负责人级自动化测试 |
| `/gstack-cso` | | 安全总监级审计（OWASP+STRIDE） |
| `/gstack-ship` | | 发布工程师级自动部署+PR |
| `/gstack-plan-ceo-review` | | YC CEO 风格战略审查 |
| `/gstack-plan-eng-review` | | 工程经理级别架构审查 |
| `/gstack-retro` | | 工程经理级周回顾 |

### 4.2 文档与Office

| Skill | 用法 | 说明 |
|-------|------|------|
| `/docx` | | Word 文档创建/编辑 |
| `/pptx` | | PPT 演示文稿创建/编辑 |
| `/xlsx` | | Excel 电子表格创建/编辑 |
| `/pdf` | | PDF 创建/合并/拆分/水印/加密 |
| `/pdf-reading` | | PDF 内容读取/提取/分析 |

### 4.3 前端与设计

| Skill | 用法 | 说明 |
|-------|------|------|
| `/frontend-design` | | 前端界面构建（不含AI味） |
| `/ui-ux-pro-max` | | UI/UX 设计增强（67种风格+96套配色+57组字体） |
| `/awesome-design-html` | | 113个品牌主题HTML设计参考 |
| `/product-design-plugin` | | 产品设计（截图→原型+URL→代码+交互审计） |

### 4.4 数据分析

| Skill | 用法 | 说明 |
|-------|------|------|
| `/data-analytics-plugin` | | 数据分析（KPI报告+指标诊断+可视化仪表盘） |

### 4.5 股权与金融

| Skill | 用法 | 说明 |
|-------|------|------|
| `/public-equity-investing` | | 公开股权投资（财报解读+竞品对标+压力测试+估值） |

### 4.6 网络搜索与Firecrawl

| Skill | 用法 | 说明 |
|-------|------|------|
| `/firecrawl-test` | | Firecrawl 连接状态测试 |
| `/firecrawl-scrape` | | Firecrawl 抓取单个网页 |
| `/firecrawl-search` | | Firecrawl 搜索+结果页内容 |
| `/firecrawl-deep-research` | | Firecrawl 多源深度研究+报告生成 |
| `/firecrawl-crawl` | | Firecrawl 爬取整个网站 |
| `/firecrawl-extract` | | Firecrawl 结构化数据提取 |
| `/firecrawl-map` | | Firecrawl 发现网站URL结构 |

### 4.7 法律

| Skill | 用法 | 说明 |
|-------|------|------|
| `/legal-assistant-zh` | | 中文法律文书（合同审查/生成/法规转换/广告合规） |
| `/claude-legal-contract-review` | | 英文合同审查（CUAD风险检测+位置感知审查） |

### 4.8 投资银行

| Skill | 用法 | 说明 |
|-------|------|------|
| `/investment-banking` | | 一站式投行工作台（Pitch Deck+Comps+DCF+尽调报告） |

### 4.9 学术论文（ARS）

| Skill | 用法 | 说明 |
|-------|------|------|
| `/ars-plan` | | 学术论文Socratic规划 |
| `/ars-full` | | 完整论文流水线（研究→写作→审稿→修订→定稿） |
| `/ars-lit-review` | | 文献综述（搜索+注释目录+综合分析） |
| `/ars-reviewer` | | 论文同行评审模拟（5审稿人+魔鬼代言人） |
| `/ars-abstract` | | 中英双语摘要写作+关键词 |
| `/ars-format-convert` | | MD/LaTeX/DOCX/PDF 格式互转 |

### 4.10 论文工作台

| Skill | 用法 | 说明 |
|-------|------|------|
| `/paper-workbench-setup` | | 论文工作台搭建（Mushtaq+ARS 整合方案） |
| `/literature-evidence-match` | | 文献证据匹配（逐句检查论点与原文支撑关系） |

### 4.11 视频

| Skill | 用法 | 说明 |
|-------|------|------|
| `/ltx-video-gen` | | LTX-Video 导演拍摄大纲+提示词生成 |
| `/chapter-progress-bar` | | 章节进度条 overlay 视频生成（Remotion） |

### 4.12 系统与架构

| Skill | 用法 | 说明 |
|-------|------|------|
| `/skill-creator` | | 通过描述需求自动制作专属 Skill |
| `/skill-search` | | 按任务需求搜索和推荐 Skill |
| `/recursive-skill-builder` | | 递归技能构建（Walk Through→Convert→Recursive） |
| `/harness-engineering` | | Harness Engineering 全景框架 |
| `/harness-engineer` | | 分析项目领域，设计Agent队伍拓扑（revfactory/harness） |
| `/harness-restructuring` | | 重整 Claude Code Harness（去重精简） |
| `/claude-codex-harness-sync` | | Claude Code ↔ Codex 双向维护 |
| `/karpathy-ai-wiki` | | Karpathy 式 AI 个人知识库（RawData+Wiki+Index） |
| `/notebooklm-memory` | | Agent↔NotebookLM 打通，长期记忆减少AI幻觉 |
| `/self-heal` | | 自愈循环（Workflow 出错快速诊断修复） |
| `/ultradebug` | | 7步系统化调试 |
| `/ultrawork-v2` | | 最大并行执行模式 |
| `/ultraresearch` | | 穷尽式在线研究模式 |
| `/loop-builder` | | 新系统搭建 Loop Builder 7问+Phase 5组件引擎 |
| `/schedule` | | 定时任务创建/更新 |
| `/daily-brief` | | 每日工作简报（大盘+待办+当日计划） |

### 4.13 交流与风格

| Skill | 用法 | 说明 |
|-------|------|------|
| `/iceberg-style` | `/iceberg-style` | Iceberg 数字分身风格（交易/创作/系统三域） |
| `/icc-prompt-framework` | | Prompt 指令/上下文/约束三要素框架 |
| `/ground-then-ask` | | 先搜索研究铺上下文再执行任务 |
| `/brainstorming` | | 结构化头脑风暴（发散→收敛→萃取） |
| `/writing-plans` | | 行动方案生成（动手前制定结构化方案） |
| `/reflection` | | 自我复盘反思（任务完成后的结构化复盘） |
| `/topic-diagnosis` | | 内容选题诊断器（5维度+爆款潜力+优化建议） |
| `/caveman` | | 超精简输出模式（省75% token） |
| `/open-door` | | 省Token模式（上下文紧张时精简化输出） |

### 4.14 其他

| Skill | 用法 | 说明 |
|-------|------|------|
| `/console` | | Skill 控制台面板（分类折叠+拼音搜索+高频栏） |
| `/setup-cowork` | | Guided Cowork 设置（插件安装+技能试用+工具连接） |
| `/consolidate-memory` | | 记忆文件整理（合并重复+修复过时+精简索引） |
| `/trading-psychology` | | 交易心理战（反人性+偏误+游资心法+评分卡） |
| `/tcm-diagnosis` | | 中医诊断助手（望闻问切+辨证论治+综合方案） |
| `/persona-clone` | | 人物克隆（上传文字→生成可对话克隆体） |

---

## 5. 附录

### 已删除/已合并（不再使用）

| Skill | 状态 | 替代 |
|-------|------|------|
| weread-skills | 已删除 | 无 |
| stop-high | 已合并 | → `/demon-stocks` |
| market-leading-stock | 已合并 | → `/demon-stocks` |
| yaogu-recommend | 已合并 | → `/demon-stocks` |
| trading-detail | 已合并 | → `/trade-detail` |
| ultrawork v1 | 已升级 | → `/ultrawork-v2` |
| intraday-chart | 已合并 | → `/intraday` |
| stock-recommendation-report | 已合并 | → `/stock-report` |
| morning-note | 已合并 | → `/market-pulse` |
| ppt-skill | 脚本工具 | → `/pptx` |
| social-card-skill | 未激活 | — |
| setup-matt-pocock-skills | 一次性安装 | — |

---

> **维护说明：** 新增 Skill 后请在对应域下追加一条，删除或合并时移到附录。

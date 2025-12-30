# 文章补充细节

## 可出题线索

### 【问题种子】GraphRAG 核心概念
- **考察点**：GraphRAG 与传统向量 RAG 的本质区别是什么？
- **回答要点**：GraphRAG 不是检索系统，而是"离线语义蒸馏 + 在线聚合"系统；向量 RAG 依赖局部相似度检索，GraphRAG 依赖全局社区摘要的 map-reduce
- **常见误区**：认为 GraphRAG 只是"用图做检索的另一种 RAG"
- **可追问**：社区摘要在查询时的作用是什么？为什么不用原始 text chunks？
- **边界条件**：GraphRAG 专为全局性问题设计，局部事实问答可能不如向量 RAG
- **层级区分**：基础-知道 GraphRAG 用图谱；进阶-理解社区摘要机制；专家-理解 map-reduce 的 QFS 本质

### 【问题种子】Text Chunks 的作用
- **考察点**：Text Chunks 在 GraphRAG 中的作用与传统 RAG 有何不同？
- **回答要点**：在 GraphRAG 中，text chunks 只在索引阶段使用，作为"知识抽取的最小证据单元"；查询时完全不用 chunks，而是用社区摘要
- **常见误区**：认为 GraphRAG 查询时也需要检索 text chunks
- **可追问**：chunk size 如何影响 recall 和成本？为什么不能直接全文建图？
- **边界条件**：chunk 太大→前文遗忘；chunk 太小→调用次数爆炸
- **层级区分**：基础-知道需要分块；进阶-理解 chunk 作为证据锚点；专家-理解 chunk 是"最小可审计输入"

### 【问题种子】社区发现算法
- **考察点**：GraphRAG 如何生成层级社区？使用什么算法？
- **回答要点**：使用 Leiden/Louvain 算法进行模块度优化；递归地在每个社区内部再次运行社区发现，直到社区不可再分
- **常见误区**：认为层级数量是人工指定的超参数
- **可追问**：什么时候停止递归？Leiden 的 resolution 参数如何影响层级深度？
- **边界条件**：社区规模过小、模块度提升低于阈值时停止
- **层级区分**：基础-知道用 Leiden；进阶-理解递归社区发现；专家-理解停止条件和参数调优

### 【问题种子】社区摘要生成
- **考察点**：社区摘要是如何生成的？为什么是"递归"的？
- **回答要点**：叶子社区用节点/边/claims 生成摘要；高层社区用子社区摘要生成摘要；形成"从全局到局部"的摘要树
- **常见误区**：认为社区摘要是孤立生成的文本
- **可追问**：如何控制摘要长度？摘要和图谱是什么关系？
- **边界条件**：context window 限制时需要裁剪或用子摘要替代元素摘要
- **层级区分**：基础-知道有社区摘要；进阶-理解自底向上生成；专家-理解摘要裁剪策略

### 【问题种子】Map-Reduce 查询流程
- **考察点**：GraphRAG 查询时的 map-reduce 具体做什么？
- **回答要点**：Map-每个社区摘要生成局部回答 + helpfulness 分数；Reduce-合并高分局部答案为最终回答
- **常见误区**：认为 map-reduce 是"多层逐级 reduce"（实际上只选一个层级跑一次）
- **可追问**：helpfulness=0 的答案怎么处理？为什么 map 阶段最吃 token？
- **边界条件**：map 输入是打乱的社区摘要 chunks，不是原始图
- **层级区分**：基础-知道有 map-reduce；进阶-理解并行 map；专家-理解 QFS 本质

### 【问题种子】层级选择策略
- **考察点**：GraphRAG 查询时如何选择使用哪一层级的社区摘要？
- **回答要点**：层级不是自动决定的，是系统级参数；可以通过固定层级、启发式规则或用户指定选择
- **常见误区**：认为 GraphRAG 会自动推理该用哪一层
- **可追问**：全局性问题 vs 局部性问题分别适合哪一层？如何设计问题→层级的决策表？
- **边界条件**：一次查询只选一个层级，不会动态切换
- **层级区分**：基础-知道有层级；进阶-理解不同层级适用不同问题；专家-理解路由策略设计

### 【问题种子】本体设计（Schema Design）
- **考察点**：GraphRAG 是否需要领域专家设计本体？
- **回答要点**：LLM 可以自动发现实体和关系，但专家定义"哪些重要"才能得到稳定可用的系统；优秀 GraphRAG 通常实体类型≤10，关系类型≤20
- **常见误区**：认为 LLM 能完全自动完成本体设计
- **可追问**：本体太宽泛会有什么问题？关系类型失控会如何影响社区结构？
- **边界条件**：全局性问题、社区可解释性要求高、需要评估复现时必须专家介入
- **层级区分**：基础-知道需要定义实体类型；进阶-理解本体影响社区质量；专家-理解"本体=压缩策略"

### 【问题种子】Token 成本与优化
- **考察点**：为什么 GraphRAG "吃 token"？如何优化？
- **回答要点**：Build 阶段-大量 LLM 抽取/摘要调用；Global query-map 阶段可能需要处理大量社区摘要；优化方法包括分层路由、cheap judge、缓存
- **常见误区**：认为 GraphRAG 只是查询时贵
- **可追问**：向量检索预筛选会省 token 但有什么代价？Packed map vs Per-summary map 的区别？
- **边界条件**：C0 层 token 可能只有 C3 的 2.6-9%，但细节会丢失
- **层级区分**：基础-知道 GraphRAG 贵；进阶-理解 build vs inference 成本；专家-理解各种优化策略

### 【问题种子】评估指标
- **考察点**：如何评估 GraphRAG 的效果？
- **回答要点**：论文使用全面性（Comprehensiveness）、多样性（Diversity）、赋能性（Empowerment）、直接性（Directness）；通过 LLM-as-a-judge 头对头比较
- **常见误区**：用传统的检索准确率指标评估
- **可追问**：为什么不能用传统 QA 数据集？claim-based 指标如何计算？
- **边界条件**：需要生成 corpus-specific 的全局性问题，不依赖 ground truth
- **层级区分**：基础-知道有四个指标；进阶-理解 LLM-as-a-judge 方法；专家-理解自适应基准生成

### 【问题种子】Global vs Local 查询
- **考察点**：GraphRAG 是否只支持全局性问题？
- **回答要点**：GraphRAG 的核心设计目标是 global 问题，但也支持 local 查询；local 查询可以用子图/局部社区摘要，不需要跑全量 map-reduce
- **常见误区**：认为 GraphRAG 只能做全局问答
- **可追问**：local 查询和 vector RAG 的 local 有什么区别？何时应该用哪种？
- **边界条件**：local 问题走 GraphRAG 可能不如 vector RAG 经济
- **层级区分**：基础-知道 GraphRAG 擅长全局问题；进阶-理解 local/global 查询路径；专家-理解 hybrid 设计

### 【问题种子】实体抽取与消歧
- **考察点**：如何从 text chunks 抽取实体并解决同一实体多种指代的问题？
- **回答要点**：LLM 从每个 chunk 抽取实体/关系/claims；通过 exact string matching 或 embedding/LLM 做实体对齐；self-reflection（gleaning）提升召回率
- **常见误区**：认为只需简单字符串匹配
- **可追问**：gleaning 是如何工作的？为什么 chunk 越大抽取的实体越少？
- **边界条件**：别名、化名、变身关系需要特别处理（如《西游记》场景）
- **层级区分**：基础-知道需要抽取实体；进阶-理解实体对齐；专家-理解 gleaning 和召回优化

### 【问题种子】Claims（主张）的作用
- **考察点**：Claims 在 GraphRAG 中起什么作用？
- **回答要点**：Claims 是"可验证的事实陈述"，作为图的协变量（covariates）；必须带证据指针（chapter + span）；支持可解释性和可追溯性
- **常见误区**：认为 claims 只是可选的附加信息
- **可追问**：claims 如何参与社区摘要生成？如何用于 claim-based 评估？
- **边界条件**：没有 claims 就无法回答"结论从哪儿来"
- **层级区分**：基础-知道有 claims；进阶-理解 claims 作为证据锚点；专家-理解 claims 在评估中的作用

### 【问题种子】GraphRAG 的本质抽象
- **考察点**：如何从更高层次理解 GraphRAG？
- **回答要点**：GraphRAG 是"两次信息重表达"：文本→图（结构化、去冗余）；图→社区摘要（语义压缩、主题化）；图谱是"主题边界生成器"，社区摘要是"可读索引"
- **常见误区**：认为 GraphRAG 只是 KG-RAG 的一种变体
- **可追问**：为什么图谱在 query-time 可以"完全冷冻"？社区摘要为什么不是图的一部分？
- **边界条件**：这是一个"离线语义蒸馏"系统，不是在线检索系统
- **层级区分**：基础-知道 GraphRAG 用图；进阶-理解两阶段重表达；专家-理解信息论/压缩视角

### 【问题种子】递归社区发现的实现细节
- **考察点**：如何具体实现递归社区发现？
- **回答要点**：在完整图上跑 Leiden→得到第一层；对每个社区的诱导子图（induced subgraph）再跑 Leiden；直到只能返回 1 个社区或规模低于阈值
- **常见误区**：认为是"分层聚类文本"（实际上只看图结构）
- **可追问**：什么是诱导子图？Leiden 如何保证连接良好的社区？
- **边界条件**：Leiden 只看图结构，不看文本 embedding 或 LLM 语义
- **层级区分**：基础-知道用 Leiden；进阶-理解递归流程；专家-理解诱导子图和模块度

### 【问题种子】社区摘要与图谱的关系
- **考察点**：社区摘要存储在哪里？和图谱是什么关系？
- **回答要点**：社区摘要不是图节点，而是图的"派生索引层"；可存储在向量数据库、文档库或文件系统；通过 community_id 反查到 node_ids/edge_ids/claim_ids
- **常见误区**：把摘要当作图节点存储
- **可追问**：如何从摘要反查到对应的图元素？摘要和元素是一一对应吗？
- **边界条件**：摘要使用的元素可能少于社区包含的全部元素（因为 context window 裁剪）
- **层级区分**：基础-知道有社区摘要；进阶-理解摘要和图的分离；专家-理解可追溯性设计

## 机制/原理要点

### Leiden 社区发现算法
- 模块度（modularity）优化：社区内连接多，社区间连接少
- 比 Louvain 更稳定，能避免"断裂社区"
- resolution 参数影响层级深度：resolution ↑ → 层级更深
- 停止条件：只能返回 1 个社区、规模低于阈值、模块度提升不足

### Map-Reduce 查询机制
- Map：对每个社区摘要 chunk 并行生成局部回答 + helpfulness (0-100)
- Filter：丢弃 helpfulness=0 的答案
- Reduce：按 helpfulness 排序，迭代加入高分答案直到 token limit，生成最终回答
- 本质是 Query-Focused Summarization（QFS），不是检索

### Self-Reflection（Gleaning）机制
- 目的：使用较大 chunk size 时避免召回率下降
- 流程：LLM 抽取实体→评估是否遗漏→如有遗漏则继续抽取
- 效果：600 token chunk 比 2400 token 抽取的实体几乎多一倍（加 gleaning 后接近）

### 层级社区摘要生成策略
- 叶子社区：按节点度优先级加入元素摘要直到 token limit
- 高层社区：用子社区摘要替换元素摘要以压缩
- 最终形成"从全局到局部"的可浏览摘要树

### 上下文窗口选择
- 论文实验：8k tokens 在全面性上普遍优于 16k/32k/64k
- 原因：避免"lost in the middle"现象（Liu et al., 2023）

## 工程实践/经验

### 本体设计经验
- 优秀 GraphRAG 通常：实体类型 ≤ 10，关系类型 ≤ 20
- 本体不是"世界真理"，而是"压缩策略"（你希望什么被压缩到一起）
- 关系类型失控会导致社区结构崩坏（如"导致/影响/关联/提及"混用）

### Token 成本优化策略
- 分层路由：先在 C0/C1 做 cheap map，只展开相关子树
- 两段式 map：先用小模型判相关，再用大模型生成
- Packed map：多个摘要打包进一次 LLM 调用（而非 per-summary）
- 缓存：map 输出和 routing 结果可复用
- 向量预筛选：top-k 社区摘要（但可能损失全局性）

### Schema 调整影响
- 实体类型调整、关系合并、摘要模板变化会触发部分/全部 rebuild
- 图谱稳定时可只重跑"摘要生成"，不用重抽实体

### 实体对齐实践
- 先规则（别名表/章节邻近），再用 embedding/LLM 软匹配复核
- GraphRAG 对重复实体有一定鲁棒性（会被聚类在一起）

## 数据/指标/对比

### 论文实验数据集
- Podcast transcripts：~1M tokens，1669 chunks × 600 tokens
- News articles：~1.7M tokens，3197 chunks × 600 tokens

### GraphRAG vs Vector RAG 性能对比
- **全面性**：GraphRAG (C0-C3) 胜率 72-83% (p<.001)
- **多样性**：GraphRAG (C0-C3) 胜率 62-82% (p<.001)
- **直接性**：Vector RAG 通常更好（符合预期，GraphRAG 更全面但更啰嗦）

### Token 消耗对比（Podcast 数据集）
- C0: 26,657 tokens (2.6% of max)
- C3: 746,100 tokens (73.5% of max)
- TS (直接文本摘要): 1,014,611 tokens (100%)
- **结论**：C0 比 TS 省 97%+ token，C3 比 TS 省 26%

### Graph 索引规模
- Podcast: 8,564 nodes, 20,691 edges → 50 C0 communities
- News: 15,754 nodes, 19,520 edges → 55 C0 communities

### 社区层级数量（常见）
- 新闻语料: 2-4 层
- 技术文档: 3-5 层
- 文学作品: 3-6 层
- 企业知识库: 4-7 层

## 案例/比喻

### 《西游记》建模示例
- **实体类型**：人物/角色、地点、组织/势力、法宝/物品、事件/情节节点、概念/主题
- **关系类型**：disciple_of, master_of, enemy_of, participates_in, transforms_into, wields, affiliated_with
- **社区示例**：
  - C0-A: 取经主线
  - C0-B: 火焰山/牛魔王势力
  - C1-B1: 牛魔王家庭关系
  - C1-B2: 法宝与地理

### "地图缩放"比喻
- C0: 世界地图（最粗粒度）
- C1: 国家地图
- C2: 省级地图
- C3: 城市地图
- **一次查询只能选一张地图看**

### "信息蒸馏器"比喻
- Chunk = 最小可审计输入
- Graph = 稳定中间表示
- Community Summary = 查询友好的全局语义缓存

### "主题边界生成器"比喻
- 图谱不是最终检索介质，而是"主题边界生成器"
- 社区发现自动找"内部连接密、外部连接稀疏"的子图
- 这等价于"自动分卷→分章→分节"

## 关键术语解释

### GraphRAG
- Microsoft Research 提出的基于图的 RAG 方法
- 核心创新：通过知识图谱 + 社区摘要支持全局 sensemaking
- 论文：From Local to Global: A GraphRAG Approach to Query-Focused Summarization (arXiv:2404.16130)

### Sensemaking
- 需要"推理整个数据集连接"的任务
- 例："整个语料的主要主题是什么？"、"整体趋势/模式是什么？"
- Vector RAG 无法有效支持这类问题

### Community Detection
- 将图划分为"内部连接密、外部连接稀疏"的子图
- GraphRAG 使用 Leiden 算法（比 Louvain 更稳定）
- 递归运行生成层级社区结构

### Query-Focused Summarization (QFS)
- 给定查询和文档集合，生成回答该查询的摘要
- GraphRAG 的 map-reduce 本质上是 QFS，不是检索

### Covariates
- 图的"协变量"，在 GraphRAG 中指 claims（可验证事实陈述）
- claims 挂到实体/关系上，支持可解释性

### Modulariy
- 模块度，衡量社区划分质量的指标
- Leiden/Louvain 优化的目标函数

### Induced Subgraph
- 诱导子图，包含指定节点集合及这些节点之间的所有边
- 递归社区发现中对每个社区取其诱导子图再运行算法

### Lost in the Middle
- 长上下文中模型对中间信息召回率下降的现象
- GraphRAG 论文发现 8k context 比 16k/32k/64k 效果更好
- 参考：Liu et al., 2023

### Entity Resolution
- 实体对齐/消歧，解决同一实体多种指代的问题
- GraphRAG 默认用 exact string matching，可用更软的方法

### Gleaning/Self-Reflection
- 自我反思提示技术，LLM 生成后评估并改进
- GraphRAG 用它提升大 chunk size 下的实体召回率
- 参考：Shinn et al., 2024; Madaan et al., 2024

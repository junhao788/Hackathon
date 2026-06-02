# 🎯 Google Cloud Rapid Agent Hackathon — "Fix the Market" Ideas

> 策略：找到市场上现有产品的**真实痛点**，用 AI Agent 解决它。

---

## Idea 1 ⭐⭐⭐⭐⭐ — Jira/Linear Killer: Project Agent that Actually Does the Work

### 🔴 现有产品的痛点

**Jira / Linear / Asana / Notion Projects** 都有一个根本问题：

| 痛点 | 说明 |
|------|------|
| **只是记录工具，不执行** | 你创建了 ticket，然后呢？还是要你手动做所有事 |
| **状态更新全靠人** | 没人记得更新 ticket 状态，board 永远不准确 |
| **上下文丢失** | 相关的 PR、讨论、文档散落各处，新成员要花很久才能理解一个 issue |
| **Sprint planning 靠猜** | 估时不准，dependency 追踪是噩梦 |
| **站会浪费时间** | "昨天做了什么" 明明系统应该知道的 |

### 🟢 我们的 Agent 怎么修复

**一个能自主行动的项目管理 Agent**：

1. **自动状态同步** — Agent 监控 GitLab MR/Pipeline，自动更新 ticket 状态
   - PR merged → ticket 自动 "Done"
   - CI 失败 → ticket 自动标注 "Blocked"
   - 代码审查评论 → 自动添加到 ticket 上下文

2. **智能站会报告** — "生成今天的站会报告"
   - Agent 自动从 GitLab 拉取昨天的所有 commits、MR、reviews
   - 从 MongoDB 拉取 ticket 变更
   - 生成每个人的进度摘要 + 阻塞项

3. **上下文聚合** — 问 "ticket #234 的完整情况"
   - Agent 自动关联：相关 MR、CI 结果、代码变更、讨论记录、文档
   - 生成完整故事线

4. **Sprint 规划助手** — "帮我规划下个 sprint"
   - 基于历史数据预估 story points
   - 自动检测 dependency 冲突
   - 推荐优先级排序

### 🏷️ Track: **GitLab** (MCP 连接代码仓库) + **MongoDB** (存储项目数据)

### 为什么能赢
- **每个开发者都恨 Jira** — 评委共鸣度极高
- 展示了 Agent 的核心价值：**自主行动 + 多步推理**
- 完美展示 MCP 集成的意义

---

## Idea 2 ⭐⭐⭐⭐⭐ — GitHub Copilot 做不到的事: Full-Stack Dev Agent

### 🔴 现有产品的痛点

**GitHub Copilot / Cursor / Cody** 的致命缺陷：

| 痛点 | 说明 |
|------|------|
| **只会写代码，不会部署** | 生成的代码到 "npm start 跑不起来" 之间有巨大鸿沟 |
| **不理解项目全貌** | 建议经常和现有架构冲突 |
| **CI/CD 盲区** | 代码写完了，pipeline 挂了，Copilot 帮不了你 |
| **不做验证** | 生成代码后不知道对不对，不跑测试 |
| **不管合并冲突** | 在自己的泡泡里写代码，merge 时爆炸 |

### 🟢 我们的 Agent 怎么修复

**不只写代码，还跑代码、修代码、部署代码的 Agent**：

1. **端到端 Feature Agent** — "实现用户注册功能"
   - Agent → 读取 GitLab 仓库结构和现有代码 → 理解架构
   - Agent → 生成代码 → 创建分支 → 推送
   - Agent → 触发 CI → 监控结果 → CI 失败则自动修复
   - Agent → 创建 MR → 生成描述和测试说明

2. **CI 修复 Agent** — Pipeline 红了？
   - Agent 读取 CI 日志 → 定位失败原因
   - 自动修改代码 → 重新推送 → 验证通过
   - 自动在 MR 评论中解释修了什么

3. **代码审查 Agent** — 比 Copilot 更深
   - 不只检查语法，而是理解业务逻辑
   - 对比项目的编码规范（从仓库中学习）
   - 检查潜在的安全问题和性能瓶颈

### 🏷️ Track: **GitLab**

### 为什么能赢
- 直接对标市场上最热门的产品（Copilot），评委注意力有保证
- **完美展示 Agent vs Chatbot 的区别** — Copilot 是问答，我们是行动

---

## Idea 3 ⭐⭐⭐⭐⭐ — Notion AI 的替代品: Knowledge Agent That Connects Everything

### 🔴 现有产品的痛点

**Notion AI / Confluence AI / Slite** 都有的问题：

| 痛点 | 说明 |
|------|------|
| **AI 只是加了个聊天框** | 只能问答，不能自动组织、整理、关联知识 |
| **信息孤岛** | 文档、Slack、邮件、代码注释，分散在各处 |
| **过时信息无人维护** | Wiki 3 年没更新，但新人还在照着做 |
| **搜索烂** | "我记得有篇文档讲过这个" → 搜半天搜不到 |
| **Onboarding 噩梦** | 新人入职要花 2 周读文档，还是读不完 |

### 🟢 我们的 Agent 怎么修复

1. **智能知识索引** — Agent 自动扫描多源数据（Elastic 搜索）
   - 连接 GitLab（README、Wiki、代码注释）
   - 连接文档存储
   - 自动建立知识图谱，发现关联

2. **过期检测** — "哪些文档已经过期了？"
   - Agent 对比文档内容 vs 当前代码 → 标注不一致的部分
   - "这篇 API 文档提到了 v1 endpoint，但代码已经是 v3 了"

3. **Onboarding Agent** — 新人的 AI 导师
   - "我是新加入的前端开发，帮我了解项目架构"
   - Agent 从 Elastic 搜索所有相关文档 → 生成个性化学习路径
   - 回答问题时附带来源链接

4. **会议纪要 → 行动项** — 自动从文档中提取 TODO → 创建 GitLab issues

### 🏷️ Track: **Elastic** (搜索引擎) 或 **MongoDB** (知识存储 + 向量搜索)

### 为什么能赢
- 解决了 **每个团队都有** 的痛点
- Elastic 的 RAG 能力完美匹配
- 新人 onboarding 场景在 demo 中很容易展示

---

## Idea 4 ⭐⭐⭐⭐ — PagerDuty 修复版: On-Call Agent That Fixes Before You Wake Up

### 🔴 现有产品的痛点

**PagerDuty / OpsGenie / Incident.io** 的核心问题：

| 痛点 | 说明 |
|------|------|
| **Alert Fatigue** | 凌晨 3 点被叫醒，结果只是一个无关紧要的告警 |
| **只报警不行动** | "CPU 高了" → 然后呢？工程师还是要自己排查 |
| **告警风暴** | 一个根因引发 50 条告警，每条都在响 |
| **缺乏上下文** | 收到告警后要花 15 分钟切换到各个监控面板收集信息 |

### 🟢 我们的 Agent 怎么修复

1. **智能告警过滤** — Agent 用 Dynatrace 数据判断告警严重性
   - 自动关联相关告警 → 合并成一个事件
   - 判断是否需要叫醒值班人员（真正的 P0 vs 可以明天处理）

2. **自动排查** — Agent 收到告警后自动开始调查
   - 从 Dynatrace 拉取 metrics, traces, logs
   - 分析根因 → "是 database connection pool 满了"
   - 生成完整的调查报告，等你醒来直接看结论

3. **自动修复（低风险）** — 对于已知问题模式
   - 重启服务、清理缓存、扩容实例等标准操作
   - Agent 执行后验证问题是否解决

### 🏷️ Track: **Dynatrace**

### 为什么能赢
- **每个 on-call 工程师都懂这个痛** — 评委共鸣感强
- 竞争少（Dynatrace track 可能参赛人数最少）
- "凌晨3点 Agent 帮你修好了问题" 的 demo 故事非常打动人

---

## Idea 5 ⭐⭐⭐⭐ — Zapier/Make 做不到的事: Intelligent Workflow Agent

### 🔴 现有产品的痛点

**Zapier / Make / n8n** 的局限：

| 痛点 | 说明 |
|------|------|
| **纯规则驱动** | If X then Y — 没有理解力，不能处理例外情况 |
| **不能推理** | "如果邮件是投诉就紧急处理" — Zapier 不理解邮件内容 |
| **配置复杂** | 多步工作流配置像在写代码 |
| **出错难排查** | 中间某步失败了，很难定位原因 |

### 🟢 我们的 Agent 怎么修复

**用自然语言描述工作流，Agent 理解并自主执行：**

- "每天早上 9 点，帮我汇总昨天所有 GitLab 新 issues，按优先级排序，把重要的发到 Slack"
- "如果数据管道失败了，自动排查原因并修复" (Fivetran MCP)
- "每周五生成本周开发进度报告" (GitLab MCP)

Agent 的优势：**能理解上下文、处理异常、做决策**（Zapier 做不到）

### 🏷️ Track: **Fivetran** 或 **GitLab**

---

## Idea 6 ⭐⭐⭐⭐ — Personal Dev Dashboard Agent

### 🔴 痛点
开发者每天要在 10+ 工具之间切换（GitLab, Jira, Slack, Calendar, CI, Monitoring...），没有统一视图。

### 🟢 Agent 修复
一个个人开发者 Agent，是你的 "AI 开发助手"：
- "今天我该做什么？" → 汇总 GitLab MR review、待处理 issues、CI 状态
- "帮我准备明天的 sprint review" → 自动生成你的贡献摘要
- "这个 error 怎么回事？" → 自动搜索团队知识库找解决方案

### 🏷️ Track: **GitLab** 或 **Elastic**

---

## 🏆 我的最终推荐

| 排名 | Idea | 一句话 | Track |
|------|------|--------|-------|
| 🥇 | **Idea 1: Project Agent** | "Jira 只记录，我们执行" | GitLab / MongoDB |
| 🥇 | **Idea 4: On-Call Agent** | "PagerDuty 叫醒你，我们帮你修" | Dynatrace |
| 🥈 | **Idea 2: Dev Agent** | "Copilot 写代码，我们部署代码" | GitLab |
| 🥈 | **Idea 3: Knowledge Agent** | "Notion AI 聊天，我们连接一切" | Elastic |
| 🥉 | **Idea 5: Workflow Agent** | "Zapier 走规则，我们会思考" | Fivetran |

> [!TIP]
> **Idea 1 (Project Agent)** 和 **Idea 4 (On-Call Agent)** 并列第一：
> - **Idea 1** 更通用，评委都能理解，demo 效果好
> - **Idea 4** 竞争更少（Dynatrace track），痛点更深刻
> 
> 两者都是 **"现有工具只告诉你问题，我们的 Agent 帮你解决问题"** 的故事。

# agents-md-maintenance（中文说明）

一个通用的 [Agent Skill](https://agentskills.io)，用于**维护和持续优化 AI 编码助手的指令文件**——`AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、`.cursorrules`、`.github/copilot-instructions.md`——跨 Claude Code、OpenAI Codex、Cursor、Gemini CLI、GitHub Copilot、Windsurf、Aider、WorkBuddy 等所有遵循 AGENTS.md 标准的工具。

指令文件的失效方式是可以预测的：规则只增不减、逐渐互相矛盾；最昂贵的教训（验证过的命令、禁区）只存在于聊天记录里，会话结束就消失；一次糟糕的合并会污染之后所有会话。这个 skill 把防住这三类问题的维护闭环固化了下来。

## 它做什么

- **探测规则文件格局**——仓库里有多个指令文件时，判断哪个才是唯一事实源（import 链、符号链接、优先级规则）
- **三种模式**：`audit`（只输出审查结论，不写文件）/ `propose`（默认，零写权限——产出经过冲突检查的提案文件）/ `gated-direct`（需显式开启，每一步都确认）
- **任何规则新增前强制执行冲突/重复检查**——合并 > 修改旧规则 > 新增，并记录检索轨迹
- **按共识检查清单把关规则质量**——命令优先、边界分层、具体优于口号、反模式清单
- **沉淀实战教训**——来自真实生产维护循环的 8 条机制级教训（详见 `references/field-lessons.md`）：
  - 加规则前必须先查冲突/重复，处置顺序：合并 > 改旧规则 > 新增
  - 数值约束必须先换算成同一单位再比较——否则最宽松的一条默默生效，其余全部形同虚设
  - ✗/✓ 示例有长度成本：模型模仿的是示例的形状，不只是规则本身
  - 多条规则治同一个症状 ⇒ 病根在上游变量，修完上游还要删掉冗余的下游规则
  - 根因才算完成：护栏（try/except、默认值）掩盖根因并静默腐化，不算修复
  - 大块替换安全规程（"18,599→50 字符"事故）：替换不出常量边界、匹配串必须盖住原文尾部、替换后重读确认
  - 最贵的规则死在会话边界：试出来的命令、踩过的禁区，当场写进规则文件
  - 规则文件同时服务于 agent 和维护者：按"运维手册"标准组织
- **自带 `audit_agents_md.py`**——机械检查：行数、缺失的核心章节、对照 package.json/Makefile/pyproject 的失效命令、死路径引用、超过 90 天的 "as of" 日期

## 安装

<details open>
<summary><b>WorkBuddy</b></summary>

把整个文件夹复制到：
- 用户级：`~/.workbuddy/skills/agents-md-maintenance/`
- 项目级：`<仓库>/.workbuddy/skills/agents-md-maintenance/`

</details>

<details>
<summary><b>Claude Code</b></summary>

复制到 `~/.claude/skills/agents-md-maintenance/`（用户级）或 `<仓库>/.claude/skills/agents-md-maintenance/`（项目级）。`SKILL.md` 的 frontmatter 遵循 [agentskills.io](https://agentskills.io) 开放标准。

</details>

<details>
<summary><b>Codex / Cursor / Gemini CLI / Aider 等原生 AGENTS.md 工具</b></summary>

这些工具没有 skills 运行时，可以直接把 skill 内容当作知识库使用：在你的 `AGENTS.md` 里加一段指针——

```markdown
## Rule maintenance
Before adding any rule to this file, follow references/best-practices.md checklist
and run scripts/audit_agents_md.py.
```

也可以把 `references/best-practices.md` 和 `references/field-lessons.md` 的内容合并进你的 AGENTS.md（注意行数预算）。

</details>

## 使用示例

- 「把这次踩的坑沉淀成规则」/ "add this lesson to AGENTS.md" → propose 模式，冲突检查后出提案
- 「审查一下我的 AGENTS.md」/ "audit my agents file" → 审查结论 + 机械检查
- 「我的 CLAUDE.md 和 AGENTS.md 漂移了」/ "sync rules across tools" → 格局探测 + 单一事实源接线

## 仓库结构

```
SKILL.md                        # 工作流、三种模式、安全护栏
references/
  rules-file-landscape.md       # 各工具文件矩阵、优先级、单一事实源接线
  best-practices.md             # 共识检查清单（命令优先、边界、卫生、反模式）
  field-lessons.md              # 从真实维护循环中泛化的经验教训
scripts/
  audit_agents_md.py            # 仅依赖标准库的检查脚本（Python 3.9+，零依赖）
assets/
  proposal-template.md          # 提案文件模板（冲突记录、净变化、回滚说明）
```

## 设计原则

**默认只有提案权，没有写权限。** 规则文件会被注入每一次会话；一次糟糕的合并会污染所有后续工作。所以在你显式开启 gated-direct 模式之前，这个 skill 永远不直接编辑规则文件——提案落在 `docs/agents-proposals/`，由你走自己惯常的验证流程应用，git 历史就是回滚手段。

**skill 不保存任何规则副本。** 规则文本只存在于规则文件本身；skill、提案、记忆里只有指针，没有内容——这正是防漂移的关键。

## 相关背景与先行工作

- [agents.md](https://agents.md) — 开放标准（Agentic AI 基金会 / Linux 基金会托管）
- GitHub 官方博客：[How to write a great agents.md — 来自 2500+ 仓库的经验](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- 实战教训来自一个真实生产环境的维护循环（2026）

## 许可证

MIT

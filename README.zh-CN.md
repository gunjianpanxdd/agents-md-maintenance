# agents-md-maintenance（中文说明）

一个通用的 [Agent Skill](https://agentskills.io)，用于**维护和持续优化 AI 编码助手的指令文件**——`AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、`.cursorrules`、`.github/copilot-instructions.md`——跨 Claude Code、OpenAI Codex、Cursor、Gemini CLI、GitHub Copilot、Windsurf、Aider、WorkBuddy 等所有遵循 AGENTS.md 标准的工具。

指令文件的失效方式是可以预测的：规则只增不减、逐渐互相矛盾；最昂贵的教训（验证过的命令、禁区）只存在于聊天记录里，会话结束就消失；一次糟糕的合并会污染之后所有会话。这个 skill 把防住这三类问题的维护闭环固化了下来。

## 它做什么

- **探测规则文件格局**——仓库里有多个指令文件时，判断哪个才是唯一事实源（import 链、符号链接、优先级规则）
- **三种模式**：`audit`（只输出审查结论，不写文件）/ `propose`（默认，零写权限——产出经过冲突检查的提案文件）/ `gated-direct`（需显式开启，每一步都确认）
- **任何规则新增前强制执行冲突/重复检查**——合并 > 修改旧规则 > 新增，并记录检索轨迹
- **按共识标准检查规则质量**——共识来源：agents.md 标准（6 万+ 仓库）、GitHub 对 2500+ agent 文件的官方分析、高星仓库（n8n、airflow、temporalio）
- **沉淀实战教训**——数值约束的单位换算、✗/✓ 示例的长度成本、症状 chasing 检测、大块替换安全（"18,599→50 字符"事故）、根因定义的完成标准
- **自带 `audit_agents_md.py`**——机械检查：行数、缺失的核心章节、对照 package.json/Makefile/pyproject 的失效命令、死路径引用、超过 90 天的 "as of" 日期

## 安装（WorkBuddy）

把整个文件夹复制到：
- 用户级：`~/.workbuddy/skills/agents-md-maintenance/`
- 项目级：`<仓库>/.workbuddy/skills/agents-md-maintenance/`

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

# 工作区管理

> 这是 `D:\workspace\` 本身的元项目。它不包含业务代码，只管理整个工作区的规范和基础设施。

## 定位

这个项目是工作区的「大脑」——定义所有项目的命名、结构、交付规范，记录踩坑经验，确保每次新会话 AI 都能快速建立上下文。

## 核心文件

| 文件 | 作用 |
|------|------|
| `WORKSPACE.md` | AI 操作手册：项目索引、命名规范、Git 规范、VIBE CODING 交付规则、技能清单、里程碑 |
| `PITFALLS.md` | 全局踩坑日志：已知问题、反模式、解决方案沉淀、标签体系 |
| `.gitignore` | 排除 `Projects-*/`，只跟踪元文件 |
| `.gitattributes` | 统一换行符，消除 CRLF 警告 |
| `README.md` | 本文件 |

## 关联

- `AGENTS.md`（`C:\Users\Administrator\.codex\`）在启动时引用本项目的 `WORKSPACE.md` 和 `PITFALLS.md`
- 每个 `Projects-NN-*` 子项目的规范由 `WORKSPACE.md` 统一定义

## 维护规则

- 新增子项目时更新 `WORKSPACE.md` 的项目索引
- 遇到新问题时追加到 `PITFALLS.md`
- 规范变更需在提交信息中说明理由

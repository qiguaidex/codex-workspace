import sys, re

with open(r"D:\workspace\PITFALLS.md", "r", encoding="utf-8") as f:
    content = f.read()

print(f"Original: {len(content)} chars")

# === 1. 合并 "显示不全" 和 "边框透明" 为一条 ===
# 找到两个条目的边界，删除第二个，更新第一个
# 条目1: 2026-06-05 | Codex 自身 | Codex 最大化后显示不全
# 条目2: 2026-06-05 | Codex 自身 | Codex 最大化后边框透明
old_merge_target = "---\n\n### 2026-06-05 | Codex 自身 | Codex 最大化后边框透明"
idx_merge = content.find(old_merge_target)
if idx_merge != -1:
    # 找下一条目的起点
    next_entry = content.find("\n### 2026-06-04 |", idx_merge)
    if next_entry == -1:
        next_entry = content.find("\n## Vibe Coding", idx_merge)
    if next_entry != -1:
        # 更新第一条
        old_first = "### 2026-06-05 | Codex 自身 | Codex 最大化后显示不全\n\n- **标签**: `#codex` `#codex-display` `#wontfix`\n- **现象**: Codex 窗口最大化后，界面未能完全填充屏幕\n- **原因**: 待确认，可能与高分屏缩放有关\n- **解决**: 待排查\n- **教训**: 首次遇到时未记录，导致后续重复排查"
        new_first = "### 2026-06-05 | Codex 自身 | Codex 最大化显示异常\n\n- **标签**: `#codex` `#codex-display` `#wontfix`\n- **现象**: Codex 窗口最大化后，(1) 界面未能完全填充屏幕；(2) 部分边框变成透明，可见桌面背景\n- **原因**: 待确认，可能与高分屏缩放有关\n- **解决**: 两个问题可能同源，暂未根除\n- **教训**: 首次遇到时未记录，导致后续重复排查"
        content = content.replace(old_first, new_first)
        # 删除第二个条目
        content = content[:idx_merge] + content[next_entry:]
        print("Merged display issue entries")

# === 2. 更新 Git remote 条目 ===
old_git = "### 2026-06-03~08 | Git | 所有仓库无远程备份\n\n- **标签**: `#git` `#git-remote` `#todo`\n- **现象**: 所有仓库纯本地，未关联 GitHub 远程\n- **原因**: 未创建 GitHub 仓库\n- **解决**: 待创建并推送\n- **教训**: 有进展后应立即推远程，防止硬盘故障丢失"
new_git = "### 2026-06-03~08 | Git | 所有仓库无远程备份\n\n- **标签**: `#git` `#git-remote`\n- **现象**: 所有仓库纯本地，未关联 GitHub 远程\n- **原因**: 未创建 GitHub 仓库\n- **解决**: 2026-06-09 已创建远程仓库并推送\n- **教训**: 有进展后应立即推远程，防止硬盘故障丢失"
content = content.replace(old_git, new_git)
print("Updated Git remote entry")

# === 3. 新增编码损坏条目 ===
encoding_entry = """
### 2026-06-09 | 工作区 | 元文件中文编码批量损坏

- **标签**: `#encoding` `#powershell` `#bug`
- **现象**: `D:\\workspace\\AGENTS.md`、`WORKSPACE.md` 尾部、`.gitattributes` 注释、`Documents\\Codex\\AGENTS.md` — 四处中文内容全部变为 `?`（0x3F 字节替换），原始汉字不可恢复
- **原因**: 文件在 PowerShell 中通过 `Set-Content` / `Out-File` 或管道重定向写入时未显式指定 `-Encoding UTF8`，PowerShell 默认使用 ASCII/ANSI 编码，多字节 UTF-8 汉字被替换为 0x3F
- **解决**: 从 `C:\\Users\\Administrator\\.codex\\AGENTS.md`（UTF-8 BOM 原版）恢复 AGENTS.md；WORKSPACE.md 尾部从"十一"节已有内容重建；`.gitattributes` 注释手动重写
- **教训**: (1) 所有文件写入必须显式指定 `-Encoding UTF8`；(2) AGENTS.md 设置"文件写入规范"章节防止复发；(3) 写入含中文的文件后立即用 `[System.IO.File]::ReadAllBytes` 检查 0x3F 计数
"""
# 插入到 Git 远程条目之前
insert_marker = "### 2026-06-03~08 | Git | 所有仓库无远程备份"
idx_insert = content.find(insert_marker)
if idx_insert != -1:
    content = content[:idx_insert] + encoding_entry + "\n---\n\n" + content[idx_insert:]
    print("Added encoding corruption entry")

# === 4. 精简反模式部分头部 ===
old_anti_header = "## Vibe Coding 反模式（重要）\n\n> 以下是在 vibe coding 中容易反复出现的错误工作方式。\n> 它们违反了 `AGENTS.md` 的核心原则，每次踩坑后追加。"
new_anti_header = "## Vibe Coding 反模式（重要）\n\n> 以下是在 vibe coding 中实际发生过的错误工作方式。规则定义见 `D:\\workspace\\AGENTS.md`，此处仅记录实例。"
content = content.replace(old_anti_header, new_anti_header)
print("Simplified anti-pattern header")

# === 5. 删除 "Vibe Coding 正确节奏" ===
old_rhythm = """### 模式：Vibe Coding 正确节奏
```
每次动手前:
  1. 问 A/B（设计文档 or 直接写代码）
  2. 拆分为原子功能点
  3. 确认用户如何验证第一个功能点

每次完成后:
  1. 按交付模板告知用户
  2. 提供具体验证步骤
  3. 等待用户反馈

用户反馈问题后:
  1. 立即停新功能
  2. 定位 → 修复 → 验证
  3. 确认修复后再继续
```"""
content = content.replace(old_rhythm, "")
print("Removed Vibe Coding correct rhythm")

# === 6. 更新元数据日期 ===
content = content.replace("> 创建: 2026-06-08 | 更新: 2026-06-08", "> 创建: 2026-06-08 | 更新: 2026-06-09")

with open(r"D:\workspace\PITFALLS.md", "w", encoding="utf-8", newline="") as f:
    f.write(content)

print(f"Final: {len(content)} chars, {len(content.encode('utf-8'))} bytes")
# 验证
raw = content.encode("utf-8")
q_count = sum(1 for b in raw if b == 0x3F)
print(f"0x3F count: {q_count}")
print(f"'?????' patterns: {content.count('?????')}")
print("Done")

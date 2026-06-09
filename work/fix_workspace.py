import sys

with open(r"D:\workspace\WORKSPACE.md", "r", encoding="utf-8") as f:
    content = f.read()

print(f"Original size: {len(content)} chars, {len(content.encode('utf-8'))} bytes")

# 1. 修复里程碑表：`n -> 真正的换行符
content = content.replace("`n", "\n")

# 2. 删除损坏的匿名段
before_marker = "> 创建: 2026-06-08 | 更新: 2026-06-08"
section_11_marker = "## 十一、历史对话索引"

idx_before = content.find(before_marker)
idx_11 = content.find(section_11_marker)

if idx_before == -1 or idx_11 == -1:
    print(f"ERROR: before={idx_before}, section_11={idx_11}")
    sys.exit(1)

end_line = content.find("\n", idx_before)
damaged_start = end_line + 1

print(f"Damaged region: {damaged_start} to {idx_11} ({idx_11 - damaged_start} chars)")
content = content[:damaged_start] + "\n" + content[idx_11:]

# 3. 简化第六节
old_6_header = "## 六、VIBE CODING 交付规则（核心）\n\n> 以下规则来自 `AGENTS.md`，是工作区级别的强制约束。"
new_6_header = "## 六、VIBE CODING 交付规则（核心）\n\n> 详细规则见 `D:\\workspace\\AGENTS.md`。本节仅列出工作区级强制约束。"

content = content.replace(old_6_header, new_6_header)

with open(r"D:\workspace\WORKSPACE.md", "w", encoding="utf-8", newline="") as f:
    f.write(content)

print(f"Final size: {len(content)} chars, {len(content.encode('utf-8'))} bytes")

# 验证无损坏
raw = content.encode("utf-8")
q_count = sum(1 for b in raw if b == 0x3F)
print(f"0x3F count: {q_count}")

# 检查删除是否成功
remaining_junk = content.count("?????")
print(f"Remaining '?????': {remaining_junk}")

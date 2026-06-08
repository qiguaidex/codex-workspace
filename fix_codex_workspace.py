# -*- coding: utf-8 -*-
# Codex 工作区修复脚本
# 用法：完全退出 Codex → 双击此文件；或在终端执行: python fix_codex_workspace.py

import json, os, shutil, sqlite3, sys

JSON_PATH = os.path.expandvars(r"%USERPROFILE%\.codex\.codex-global-state.json")
DB_PATH = os.path.expandvars(r"%USERPROFILE%\.codex\state_5.sqlite")

print("=" * 50)
print("  Codex 工作区修复脚本")
print("=" * 50)
print()

# 1. Backup
bak = JSON_PATH + ".manual-bak"
shutil.copy2(JSON_PATH, bak)
print("[1/4] 已备份到 .codex-global-state.json.manual-bak")

# 2. Update JSON
print("[2/4] 更新工作区配置...")
with open(JSON_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

NEW_ROOTS = [
    "D:\\workspace",
    "D:\\workspace\\Projects-01-个人助理",
    "D:\\workspace\\Projects-02-抖音运营",
    "D:\\workspace\\Projects-03-微信发卷",
    "D:\\workspace\\Projects-04-早期探索",
]
state["electron-saved-workspace-roots"] = NEW_ROOTS
state["project-order"] = NEW_ROOTS
state["active-workspace-roots"] = ["D:\\workspace"]

# Thread mapping
thread_map = {
    # Projects-00 (9)
    "019ea5ae-9af2-77a3-9337-ab409dab9322": "D:\\workspace",
    "019e8be7-a220-7ae2-a953-fd68b7f006c3": "D:\\workspace",
    "019e9162-d499-7960-baf1-e3c42d5dd469": "D:\\workspace",
    "019e91d7-79ac-7982-b9e8-bf47dc5ffbd3": "D:\\workspace",
    "019e95a6-659e-70d1-bd2e-425e2151dfb8": "D:\\workspace",
    "019e95be-9a55-7e71-9bae-163b527b8e09": "D:\\workspace",
    "019e9f57-f397-7cd2-be58-99987e793e7c": "D:\\workspace",
    "019ea491-5a50-78b1-8e4f-7b3716ba13a9": "D:\\workspace",
    "019ea5ab-1f95-78c1-b795-9681ac82a4af": "D:\\workspace",
    # Projects-01 (7)
    "019e91d2-5839-71c1-b72b-978506b13ed6": "D:\\workspace\\Projects-01-个人助理",
    "019e965b-32ed-72d3-895a-1005ffd0f9f4": "D:\\workspace\\Projects-01-个人助理",
    "019e95d9-3385-7512-9606-64fd8127a81e": "D:\\workspace\\Projects-01-个人助理",
    "019e9622-95b2-7682-ad06-9853f7277719": "D:\\workspace\\Projects-01-个人助理",
    "019e9632-28f1-7251-9976-8d95312fe27f": "D:\\workspace\\Projects-01-个人助理",
    "019e91fc-92b0-7583-831f-98caedcf9fee": "D:\\workspace\\Projects-01-个人助理",
    "019ea576-7f2b-7162-8437-3c3e28374f85": "D:\\workspace\\Projects-01-个人助理",
    # Projects-02 (1)
    "019ea0a1-9509-7193-891e-830d74902b33": "D:\\workspace\\Projects-02-抖音运营",
    # Projects-03 (1)
    "019e929f-72df-7d91-8e30-801cff28a19a": "D:\\workspace\\Projects-03-微信发卷",
    # Projects-04 (4)
    "019e914d-5387-7891-aaca-fc6dfaa62392": "D:\\workspace\\Projects-04-早期探索",
    "019e9144-17f2-70c2-8a69-da92fc20d757": "D:\\workspace\\Projects-04-早期探索",
    "019e90ba-e833-7320-a14a-e7d51b3714ea": "D:\\workspace\\Projects-04-早期探索",
    "019e90b0-7a5a-75f0-8d42-2ba76645e695": "D:\\workspace\\Projects-04-早期探索",
}

state["thread-workspace-root-hints"] = thread_map
state["projectless-thread-ids"] = [
    "019e90b4-011b-74c3-8c9e-785cdae58069",
    "019e8ba1-67ea-7f02-bbd8-46f13d6507d6",
]

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False)
print(f"       5 个工作区, {len(thread_map)} 个线程已归类, 2 个保留无项目")

# 3. Update SQLite
print("[3/4] 更新数据库...")
try:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for tid, cwd in thread_map.items():
        c.execute("UPDATE threads SET cwd = ? WHERE id = ?", (cwd, tid))
    conn.commit()
    # Strip \\?\ prefix from remaining threads
    c.execute("UPDATE threads SET cwd = REPLACE(cwd, '\\\\?\\', '') WHERE cwd LIKE '\\\\?\\%'")
    conn.commit()
    conn.close()
    print(f"       SQLite 已更新 ({len(thread_map)} 条)")
except Exception as e:
    print(f"       SQLite 跳过 ({e})")

# 4. Clean old dirs
print("[4/4] 清理旧目录...")
old = ["D:\\Documents\\Aghet", "D:\\Documents\\kehu", "D:\\Documents\\WORK",
       "D:\\Documents\\juanzi", "D:\\Documents\\New project"]
for d in old:
    if os.path.exists(d):
        try:
            shutil.rmtree(d, ignore_errors=True)
            if not os.path.exists(d):
                print(f"       已删除: {d}")
        except:
            pass

print()
print("=" * 50)
print("  修复完成！请重新启动 Codex")
print("=" * 50)
print()
print("启动后左侧应出现 5 个工作区：")
print("  workspace           (9 个对话)")
print("  Projects-01-个人助理  (7 个对话)")
print("  Projects-02-抖音运营   (1 个对话)")
print("  Projects-03-微信发卷   (1 个对话)")
print("  Projects-04-早期探索   (4 个对话)")
print()
input("按回车键退出...")

# -*- coding: utf-8 -*-
import sqlite3, datetime

conn = sqlite3.connect(r"C:\Users\Administrator\.codex\state_5.sqlite")
c = conn.cursor()
c.execute("SELECT id, title, cwd, created_at_ms FROM threads ORDER BY cwd, created_at_ms DESC")
rows = c.fetchall()
conn.close()

def cwd_to_project(cwd):
    if not cwd: return "\u65e0\u9879\u76ee"
    cwd = cwd.replace("\\\\?\\", "")
    if "Projects-01" in cwd: return "01-\u4e2a\u4eba\u52a9\u7406"
    if "Projects-02" in cwd: return "02-\u6296\u97f3\u8fd0\u8425"
    if "Projects-03" in cwd: return "03-\u5fae\u4fe1\u53d1\u5377"
    if "Projects-04" in cwd: return "04-\u65e9\u671f\u63a2\u7d22"
    if cwd == "D:\\workspace" or cwd.endswith("\\workspace"): return "00-\u5de5\u4f5c\u533a\u7ba1\u7406"
    return "\u65e0\u9879\u76ee"

lines = []
lines.append("")
lines.append("## \u5341\u4e00\u3001\u5386\u53f2\u5bf9\u8bdd\u7d22\u5f15")
lines.append("")
lines.append("\u7531\u4e8e Codex \u684c\u9762\u7aef\u4e0d\u652f\u6301\u5c06\u65e7\u5bf9\u8bdd\u8fc1\u79fb\u5230\u9879\u76ee\uff0c\u672c\u8868\u4f5c\u4e3a\u624b\u52a8\u7d22\u5f15\u3002\u5728 Codex \u641c\u7d22\u6846\u8f93\u5165\u6807\u9898\u5173\u952e\u8bcd\u5373\u53ef\u5b9a\u4f4d\u3002")
lines.append("")

order = ["00-\u5de5\u4f5c\u533a\u7ba1\u7406", "01-\u4e2a\u4eba\u52a9\u7406", "02-\u6296\u97f3\u8fd0\u8425", "03-\u5fae\u4fe1\u53d1\u5377", "04-\u65e9\u671f\u63a2\u7d22", "\u65e0\u9879\u76ee"]
for proj in order:
    items = [(datetime.datetime.fromtimestamp(ts/1000).strftime("%m-%d") if ts else "?",
              (title or "\u65e0\u6807\u9898").replace("\n"," ")[:55])
             for tid, title, cwd, ts in rows if cwd_to_project(cwd) == proj]
    if not items: continue
    lines.append("### Projects-" + proj)
    lines.append("| \u65e5\u671f | \u5bf9\u8bdd\u6807\u9898 |")
    lines.append("|------|---------|")
    for date, title in items:
        lines.append("| {} | {} |".format(date, title))
    lines.append("")

with open(r"D:\workspace\WORKSPACE.md", "a", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Done")

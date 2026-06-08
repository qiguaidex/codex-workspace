# -*- coding: utf-8 -*-
"""Codex 历史对话召回工具

用法：
  python recall.py "关键词"        → 搜索标题
  python recall.py --id <thread_id> → 按 ID 精确查找

输出：匹配线程的标题 + 最近对话内容摘要
"""

import sqlite3, json, glob, os, sys, datetime

DB = os.path.expandvars(r"%USERPROFILE%\.codex\state_5.sqlite")
ROLLOUT_DIR = os.path.expandvars(r"%USERPROFILE%\.codex\sessions")


def search_threads(keyword):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "SELECT id, title, cwd, created_at_ms FROM threads WHERE title LIKE ? ORDER BY created_at_ms DESC",
        (f"%{keyword}%",),
    )
    results = c.fetchall()
    conn.close()
    return results


def get_thread_by_id(tid):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, title, cwd, created_at_ms FROM threads WHERE id = ?", (tid,))
    r = c.fetchone()
    conn.close()
    return r


def find_rollout(tid):
    for root, dirs, files in os.walk(ROLLOUT_DIR):
        for f in files:
            if tid in f and f.endswith(".jsonl"):
                return os.path.join(root, f)
    return None


def extract_conversation(rollout_path, max_turns=5):
    """从 rollout 文件提取最近 N 轮对话"""
    turns = []
    current_user = None

    with open(rollout_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line)
                t = d.get("type", "")
                pl = d.get("payload", {})

                if t == "event_msg":
                    pt = pl.get("type", "")
                    # User message
                    if pt == "message":
                        text_els = pl.get("text_elements", [])
                        if text_els:
                            current_user = " ".join(
                                e.get("text", "") for e in text_els if e.get("text")
                            )
                    # Codex thinking
                    elif pt == "text":
                        codex_text = pl.get("text", "")
                        if current_user and codex_text.strip():
                            turns.append((current_user[:200], codex_text[:300]))
                            current_user = None
            except:
                pass

    return turns[-max_turns:]


def format_output(tid, title, date, rollout_path):
    print(f"\n{'=' * 60}")
    print(f"{title}")
    print(f"日期: {date}  |  ID: {tid[:25]}...")
    print(f"{'=' * 60}")

    if not rollout_path:
        print("(未找到对话记录)")
        return

    turns = extract_conversation(rollout_path, max_turns=5)
    if not turns:
        print("(未能提取对话内容)")
        return

    for i, (user_msg, codex_msg) in enumerate(turns, 1):
        print(f"\n--- 第 {i} 轮 ---")
        print(f"用户: {user_msg[:200]}")
        print(f"Codex: {codex_msg[:300]}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python recall.py <关键词>")
        print("      python recall.py --id <thread_id>")
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "--id" and len(sys.argv) > 2:
        tid = sys.argv[2]
        r = get_thread_by_id(tid)
        threads = [r] if r else []
    else:
        threads = search_threads(arg)

    if not threads:
        print(f"未找到匹配「{arg}」的对话")
        sys.exit(0)

    for tid, title, cwd, ts in threads[:3]:
        date = (
            datetime.datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d")
            if ts
            else "?"
        )
        rollout = find_rollout(tid)
        format_output(tid, title, date, rollout)

#!/usr/bin/env python3
"""Stop hook: a session that changed things must end with a history/ update.

Reads the session transcript. If the last real piece of work (a file edit, a
git commit/push, a PR create/merge) came after the last write to
history/session-history.md or history/YYYY-MM.md, block the stop once and tell
Claude to log the session. stop_hook_active stops it from looping.
"""
import json, re, sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)
if data.get("stop_hook_active"):
    sys.exit(0)

IGNORE = ("/.claude/", "/private/tmp/", "/tmp/", "/scratchpad/", "/node_modules/")
HIST = re.compile(r"(?:^|[\s/'\"])history/(session-history\.md|\d{4}-\d{2}\.md)")
WORK_CMD = re.compile(r"\bgit (commit|push)\b|\bgh pr (create|merge)\b")

last_work = last_hist = -1
try:
    with open(data["transcript_path"]) as f:
        for i, line in enumerate(f):
            try:
                msg = json.loads(line)
            except Exception:
                continue
            content = (msg.get("message") or {}).get("content")
            if msg.get("type") != "assistant" or not isinstance(content, list):
                continue
            for c in content:
                if c.get("type") != "tool_use":
                    continue
                inp = c.get("input") or {}
                name = c.get("name")
                if name in ("Edit", "Write", "NotebookEdit"):
                    p = inp.get("file_path") or inp.get("notebook_path") or ""
                    if HIST.search(p):
                        last_hist = i
                    elif p and not any(s in p for s in IGNORE):
                        last_work = i
                elif name == "Bash":
                    cmd = inp.get("command") or ""
                    if HIST.search(cmd):
                        last_hist = i
                    elif WORK_CMD.search(cmd):
                        last_work = i
except Exception:
    sys.exit(0)

if last_work > last_hist:
    print(json.dumps({
        "decision": "block",
        "reason": (
            "This session changed files or shipped work, but history/ has not been updated. "
            "In the project folder (Drive), append one row to history/session-history.md "
            "and a dated section to history/YYYY-MM.md for the current month. If the project "
            "has no history/ folder yet, create it: session-history.md (table: Date | Summary, "
            "newest last), the month file, and a short README.md saying what each holds. "
            "Update plan/notes only if status or a durable decision changed. Then finish."
        ),
    }))

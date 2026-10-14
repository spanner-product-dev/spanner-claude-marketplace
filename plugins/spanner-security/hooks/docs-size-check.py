#!/usr/bin/env python3
"""Warns when a project's plan-*.md or notes-*.md has outgrown what is read every session.

SessionStart: checks plan-*.md / notes-*.md in the working directory.
PostToolUse (Edit/Write): checks the file just edited, once per file per session.

Non-blocking: it adds context for Claude and never stops anything. The fix is a
split by scope (see SpannerOS CLAUDE.md, "Keeping the Tracking Files Small").
"""
import glob, hashlib, json, os, re, sys, tempfile

LIMIT_KB = 30
NAME = re.compile(r"(^|/)(plan|notes)-[^/]+\.md$")

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

event = data.get("hook_event_name", "")
paths = []
if event == "SessionStart":
    paths = glob.glob(os.path.join(data.get("cwd") or os.getcwd(), "*.md"))
elif event == "PostToolUse":
    p = (data.get("tool_input") or {}).get("file_path") or ""
    if p:
        paths = [p]

over = []
for p in paths:
    if not NAME.search(p):
        continue
    try:
        kb = os.path.getsize(p) / 1024
    except OSError:
        continue
    if kb <= LIMIT_KB:
        continue
    if event == "PostToolUse":  # once per file per session
        marker = os.path.join(tempfile.gettempdir(), "docs-size-%s-%s" % (data.get("session_id", "x"), hashlib.md5(p.encode()).hexdigest()[:12]))
        if os.path.exists(marker):
            continue
        open(marker, "w").close()
    over.append((os.path.basename(p), kb))

if over:
    files = "; ".join("%s is %.0f KB" % o for o in over)
    msg = (
        "Tracking-file size: %s (limit about %d KB). plan-*/notes-* files are read at the start of every "
        "session, so size taxes every task. Tell the user and propose a split BY SCOPE, not by date, before "
        "going further: current state stays in the plan; cross-module decisions move to architecture-[project].md; "
        "per-area detail to modules/<area>.md; dated narrative to history/. Supersede in place instead of "
        "appending. Do not restructure without the user's OK. Reference: SpannerOS CLAUDE.md, "
        "'Keeping the Tracking Files Small'." % (files, LIMIT_KB)
    )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": msg}}))

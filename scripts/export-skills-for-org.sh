#!/bin/zsh
# Regenerate the org-settings upload bundle from this repo.
#
# THIS REPO IS THE SOURCE OF TRUTH FOR EVERY SPANNER SKILL. Org settings is a
# PUBLISH TARGET — a deploy, not a place to edit. The bundle this writes is
# derived, gitignored, and safe to delete: regenerate it rather than keeping it.
#
# ---------------------------------------------------------------------------
# IT REFUSES TO RUN FROM A STALE OR DIRTY CHECKOUT, AND THAT IS THE POINT.
#
# On 2026-09-18 the same mistake was made three times in one afternoon, twice
# by someone who had just finished writing a warning about it:
#
#   · this checkout was 18 commits behind origin while the plugin cache was
#     current, so the local files looked authoritative and were not;
#   · a diff taken against a two-commits-behind clone produced a confident,
#     entirely false report that two skills had drifted apart — which was
#     written into SKILLS-RUNBOOK.md before it was caught;
#   · a bundle was exported, then a PR merged, and the exported copy silently
#     became the old one.
#
# A warning in a document did not prevent any of those. A guard does. Uploading
# a stale skill is worse than uploading nothing: a missing skill makes Claude
# ask, a stale one makes it confidently wrong, and nobody double-checks a
# confident answer.
# ---------------------------------------------------------------------------
set -e
cd "$(dirname "$0")/.."

FORCE=0
[[ "${1:-}" == "--force" ]] && FORCE=1

fail() { print -u2 "\n  ✗ $1\n"; [[ $FORCE -eq 1 ]] && print -u2 "  (--force given, continuing anyway)\n" || exit 1 }

BRANCH=$(git rev-parse --abbrev-ref HEAD)
[[ "$BRANCH" == "main" ]] || fail "On branch '$BRANCH', not main.
    Skills are published from main. Run: git checkout main && git pull"

[[ -z "$(git status --porcelain)" ]] || fail "Working tree has uncommitted changes.
    Exporting now would ship something that is not in the repo. Commit or stash first:
$(git status --short | sed 's/^/      /')"

git fetch -q origin main 2>/dev/null || print -u2 "  ! could not reach origin — staleness unverified"
BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo 0)
[[ "$BEHIND" -eq 0 ]] || fail "$BEHIND commit(s) behind origin/main.
    The files under you are older than what has been merged. Run: git pull --ff-only origin main"

AHEAD=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo 0)
[[ "$AHEAD" -eq 0 ]] || print -u2 "  ! $AHEAD commit(s) ahead of origin/main — exporting unpushed work"

OUT="dist/org-settings"
rm -rf "$OUT"; mkdir -p "$OUT"
for p in plugins/*/skills/*(/); do
  n="${p:t}"
  mkdir -p "$OUT/$n"
  cp -R "$p/." "$OUT/$n/"
done
find "$OUT" -name .DS_Store -delete 2>/dev/null || true

SHA=$(git rev-parse --short HEAD)
print "$SHA  $(git log -1 --format=%cd --date=short)" > "$OUT/.exported-from"

print ""
print "  ✓ $(ls "$OUT" | wc -l | tr -d ' ') skills exported to $OUT"
print "    from main @ $SHA — matches origin/main"
print ""
print "  Upload the WHOLE folder for these; SKILL.md alone loses content:"
for d in "$OUT"/*(/); do
  [[ -n "$(find "$d" -mindepth 1 -maxdepth 1 -type d 2>/dev/null)" ]] && print "      ${d:t}"
done
print ""
print "  claude.ai → Organization settings → Skills → ⋮ → Replace (not Delete-then-Add:"
print "  Replace keeps the access tier, deleting loses it silently)."
print ""

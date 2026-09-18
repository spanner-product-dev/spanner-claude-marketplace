#!/bin/zsh
# Regenerate the org-settings upload bundle from this repo.
#
# THIS REPO IS THE SOURCE OF TRUTH FOR EVERY SPANNER SKILL. Org settings is a
# PUBLISH TARGET — a deploy, not a place to edit. The bundle this writes is
# derived, gitignored, and safe to delete: regenerate it rather than keeping it.
#
# Why this script exists: on 2026-09-18 the org-settings copies of two skills
# were found to be older than this repo's, and one of them
# (`spanneros-crud-scaffolder`) told Claude to use shadcn/ui in a project that
# deliberately has none. Nobody had done anything wrong — there was simply no
# step that took a merged change and put it in front of the org. An export made
# by hand into a Documents folder would have become a fourth copy to drift.
set -e
cd "$(dirname "$0")/.."
OUT="dist/org-settings"
rm -rf "$OUT"; mkdir -p "$OUT"

for p in plugins/*/skills/*(/); do
  n="${p:t}"
  mkdir -p "$OUT/$n"
  cp -R "$p/." "$OUT/$n/"
done

print "Wrote $(ls "$OUT" | wc -l | tr -d ' ') skills to $OUT from $(git rev-parse --short HEAD)"
print ""
print "Skills carrying a references/ subfolder — upload the WHOLE folder, not just SKILL.md:"
for d in "$OUT"/*(/); do
  [[ -n "$(find "$d" -mindepth 1 -maxdepth 1 -type d 2>/dev/null)" ]] && print "  ${d:t}"
done
print ""
print "Upload at claude.ai → organization settings → Capabilities → Skills."
print "Nothing reads this folder automatically; it exists to be uploaded and then forgotten."

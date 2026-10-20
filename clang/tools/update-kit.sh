#!/usr/bin/env bash
# Import the latest course-kit template into this course.
#
#   tools/update-kit.sh            sync from ../../course-kit
#   tools/update-kit.sh --pull     git pull the kit first
#   KIT=/path/to/course-kit tools/update-kit.sh
#
# Kit-owned (overwritten, never edit here): theme/, scripts/, img/, .gitignore, .nojekyll
# Course-owned (never touched): _quarto.yml, index.qmd, modules/, media/, extra.*, tools/
# After syncing, it shows how the kit's _quarto.yml `format:` / `project:` blocks differ from
# yours, so you can merge template changes there by hand.
set -euo pipefail
cd "$(dirname "$0")/.."
KIT="${KIT:-../../course-kit}"
[ -d "$KIT/theme" ] || { echo "kit not found at $KIT (set KIT=...)" >&2; exit 1; }
[ "${1:-}" = "--pull" ] && git -C "$KIT" pull --ff-only

for d in theme scripts img; do rsync -a --delete "$KIT/$d/" "$d/"; done
cp "$KIT/.gitignore" "$KIT/.nojekyll" .

new=$(git -C "$KIT" rev-parse --short HEAD)
old=$(cat .kit-version 2>/dev/null || echo none)
echo "$new" > .kit-version
echo "kit: $old -> $new"
[ "$old" != none ] && [ "$old" != "$new" ] && git -C "$KIT" log --oneline "$old..$new" 2>/dev/null || true

blk() { python3 -c "
import sys,yaml
c=yaml.safe_load(open(sys.argv[1]))
print(yaml.safe_dump({k:c[k] for k in ('project','format')},sort_keys=True))" "$1"; }
echo "--- differences in project:/format: (kit '<'  vs this course '>'; expected: theme list, extra.html) ---"
diff <(blk "$KIT/_quarto.yml") <(blk _quarto.yml) || true
echo "Next: quarto render"

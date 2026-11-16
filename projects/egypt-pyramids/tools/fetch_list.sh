#!/bin/bash
# Download every "File:...|out" line of tools/images.txt that is not on disk yet, pausing between files.
cd "$(dirname "$0")/.."
while IFS='|' read t o; do
  [ -s "img/$o" ] && continue
  python3 tools/fetch_commons.py get "$t" "img/$o" 1280 2>&1 | tail -1
  sleep 25
done < tools/images.txt

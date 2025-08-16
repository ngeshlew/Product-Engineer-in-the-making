#!/usr/bin/env bash

cc_init() {
  echo "[init] Initializing memory bank and context..."
  mkdir -p memory-bank
  : > memory-bank/projectbrief.md
  : > memory-bank/activeContext.md
  echo "# Project Brief" >> memory-bank/projectbrief.md
  echo "# Active Context" >> memory-bank/activeContext.md
  echo "[init] Done. Edit memory-bank/*.md to provide details."
}

cc_plan() {
  echo "[plan] Create a short plan in memory-bank/activeContext.md"
  echo "\n## Plan ($(date -Iseconds))" >> memory-bank/activeContext.md
  echo "- Target files: " >> memory-bank/activeContext.md
  echo "- Acceptance checks: " >> memory-bank/activeContext.md
  echo "[plan] Append your plan details above."
}

cc_execute() {
  echo "[execute] Follow the plan. Keep edits small and scoped."
  echo "[execute] Use Cursor rules: /execute"
}

cc_review() {
  echo "[review] Summarize what changed, run tests/build, and note results."
  echo "\n## Review ($(date -Iseconds))" >> memory-bank/progress.md
  echo "- Summary: " >> memory-bank/progress.md
  echo "- Test/build results: " >> memory-bank/progress.md
}

cc_commit() {
  echo "[commit] Compose a Conventional Commit message."
  echo "[commit] Example: feat(scope): concise description"
}

cc_help() {
  cat <<EOF
cursor commands:
  init       Initialize memory bank templates
  plan       Append a planning section to activeContext
  execute    Guidance for scoped changes
  review     Append a review note to progress
  commit     Guidance for Conventional Commits
  list       List available commands (including plugins)
  help       Show this help
EOF
}
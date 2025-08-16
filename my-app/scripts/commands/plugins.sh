#!/usr/bin/env bash

# Load plugin commands from scripts/cursor_commands if available
cc_plugins_load() {
  local plugin_dir="scripts/cursor_commands"
  if [ -d "$plugin_dir" ]; then
    # source any *.sh files as command providers
    for f in "$plugin_dir"/*.sh; do
      [ -e "$f" ] || continue
      # shellcheck disable=SC1090
      . "$f"
    done
  fi
}

cc_plugins_list() {
  local plugin_dir="scripts/cursor_commands"
  if [ -d "$plugin_dir" ]; then
    ls -1 "$plugin_dir" | sed 's/^/  /'
  else
    echo "  (none)"
  fi
}
# Commands CLI (scripts/cc)

Use `scripts/cc` for core workflow actions and plugin commands.

Core:
```bash
bash scripts/cc list
bash scripts/cc init
bash scripts/cc plan
bash scripts/cc execute
bash scripts/cc review
bash scripts/cc commit
```

Plugins:
- Any `*.sh` under `scripts/cursor_commands/` is auto-loaded
- List plugins: `bash scripts/cc list`

Add your commands repo:
```bash
# SSH (recommended)
bash scripts/add-cursor-commands.sh git@github.com:<you>/cursor_commands.git
# or copy files into scripts/cursor_commands/
```
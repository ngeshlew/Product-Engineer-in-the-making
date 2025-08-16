# Integrating cursor_commands

Two options to bring in your commands:

## Submodule (recommended)
```bash
# SSH avoids tokens in shells/logs
bash scripts/add-cursor-commands.sh git@github.com:<you>/cursor_commands.git

git commit -m "chore(submodule): add cursor_commands"
```
Pros: central updates, shared across projects. Cons: submodule workflow.

## Vendor copy
Copy scripts into `scripts/cursor_commands/`.
Pros: simple, offline. Cons: diverges per project.

Any `*.sh` in `scripts/cursor_commands/` is auto-loaded by `scripts/cc`. Document provided commands in your project README or this wiki.
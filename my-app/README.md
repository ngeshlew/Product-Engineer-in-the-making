# cursorstarter

A project starter template for building software smoothly in Cursor. It combines a structured workflow inspired by `CursorRIPER.sigma` with your `cursor_commands` conventions, including a Commit Mode, Cursor rules, and a documented setup so you can clone this repo for every new project.

## Why use this
- Standardized Cursor setup with rules that guide high-quality, incremental edits
- RIPER Modes (Research, Innovate, Plan, Execute, Review) with permissions
- Commit Mode that encourages plan-implement-review commits
- Memory bank files to keep context and decisions explicit
- Optional MCP server config for GitHub, search, and browser automation
- Wiki/docs to onboard anyone quickly

## Quick Start
1) Create your new repo from this template (or clone/pull it into an empty directory)
2) Open in Cursor
3) Ensure codebase indexing is enabled in Cursor Settings > Features > Codebase Indexing
4) Initialize memory bank and structure:

```bash
bash scripts/init.sh
```

5) Use modes via Cursor chat shortcuts:
```text
/research (/r)
/innovate (/i)
/plan     (/p)
/execute  (/e)
/review   (/rev)
```

Or use the CLI:
```bash
bash scripts/cc list
bash scripts/cc init
bash scripts/cc plan
bash scripts/cc execute
bash scripts/cc review
bash scripts/cc commit
```

If you already have a repo, copy the `.cursor/` folder, `memory-bank/`, `scripts/`, and `.cursorignore` into it, then run the init script.

## Rules included
- `.cursor/rules/ripersigma105.mdc` (Sigma core; modes, permissions, protection, context)
- `.cursor/rules/cursorstarter-core.mdc` (starter workflow & etiquette)
- `.cursor/rules/webdev-best-practices.mdc` (web.dev overlay: PWAs, Streams, Passkeys, Web Vitals)
- `.cursor/rules/design-systems.mdc` (Apple HIG, Material 3, Carbon, Tailwind integration)
- `.cursor/rules/commit-mode.mdc`, `code-protection.mdc`, `context.mdc`, `permissions.mdc`
- `.cursor/rules/analytics-clarity.mdc` (mode-aware Microsoft Clarity guidance)
- Optional MCP and BMAD rules: `mcp-*.mdc`, `bmad-roles.mdc`, `prd-system.mdc`, `quality-gates.mdc`, `enterprise.mdc`

Docs mirrored under `docs/ripersigma/` (Quickstart, Protection Commands, Context, Permissions, MCP setup, BMAD guide, etc.). See analytics guide at `docs/analytics/Clarity.md`.
See also: `docs/webdev-integration.md` for web.dev overlays, and `docs/design-systems/*` for design-system guidance.

## Design Systems
- Start with `docs/design-systems/meta-guidelines.md` for cross-system principles and tokens
- Use `docs/design-systems/decision-tree.md` to select a primary system and borrowing rules
- Follow `docs/design-systems/mode-checklists.md` to operationalize per mode
- Record decisions in `memory-bank/` (see section below)

## MCP (optional)
`.cursor/mcp.json` includes optional servers (filesystem, GitHub, Brave Search, Puppeteer, Docker). See `docs/ripersigma/mcp/*` for service setup.

## Memory Bank
Six files under `memory-bank/` serve as the durable context:
- `projectbrief.md`
- `systemPatterns.md`
- `techContext.md`
- `activeContext.md`
- `progress.md`
- `protection.md`

## Integrating your cursor_commands
- Add as a submodule at `scripts/cursor_commands` or copy files there.
- Any `*.sh` under `scripts/cursor_commands/` is auto-loaded by `scripts/cc`.

## Wiki
Use pages in `wiki/` or publish to GitHub Wiki with `scripts/publish-wiki.sh`.

## License
MIT
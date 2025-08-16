# Protection Registry

## Protected Regions
- file: tokens/*
  - level: PROTECTED
  - rationale: Source-of-truth design tokens must not be edited without approval
  - notes: Changes require design sign-off and visual regression checks
- file: styles/theme/*
  - level: GUARDED
  - rationale: Theme mapping to tokens; edits can cause broad UI changes
  - notes: Run a11y and perf checks on change

## Violations
- 

## Approvals
-
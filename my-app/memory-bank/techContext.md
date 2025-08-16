# Technical Context

## Technology Stack
- Web Platform APIs: Service Workers, Web App Manifest, Streams API (`TransformStream`), WebAuthn (Passkeys), Credential Management API, File System Access, Web Share, Badging, Background Sync, App Shortcuts, URL/Protocol handlers
- Observability: web‑vitals (client), Lighthouse (lab), RUM backend (custom endpoint)

## Environment
- Target browsers: evergreen; ensure progressive enhancement for unsupported APIs
- Device profiles: include mid‑tier mobile profile for testing and budgets

## Dependencies / Libraries
- `web-vitals` (collect LCP/INP/CLS with attribution)
- Microsoft Clarity (client snippet) for analytics; optional Data Export consumer

## Performance & Metrics
- Core Web Vitals (field, p75): LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1
- Guardrails: TTFB p75 ≤ 800 ms; TBT (lab) ≤ 200 ms
- Measurement: field RUM with sampling (1–10%), attribution enabled; lab via Lighthouse/Throttle

## Environment & Tooling
- Clarity project id configured per environment (dev/stage/prod)

## Build & CI
- Optionally verify Clarity snippet presence in build artifacts for web apps

## Security & Secrets
<<<<<<< HEAD
- Keep API tokens (for Data Export) and project ids in env or secret storage
=======
- 

## Design System Implementation
- Libraries: [SwiftUI/UIKit | Material Web/Compose | Carbon React/Web Components | Tailwind + Headless/Radix]
- Token Source of Truth: [Style Dictionary | CSS Variables | Platform Theme]
- Token Distribution: [npm pkg | platform module | CI publish]
- Storybook/Docs: [Storybook + MDX; usage guidelines]
- A11y/Visual/Perf Tests: [axe, testing-library, Playwright snapshots, Lighthouse budgets]
>>>>>>> b70844c (Add design systems integration framework and documentation)

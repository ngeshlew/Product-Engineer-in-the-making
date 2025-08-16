# System Patterns

## Architecture
- PWA app shell with offline fallback and installability
- RUM telemetry pipeline for Core Web Vitals (LCP, INP, CLS) with p75 aggregation
- Progressive enhancement layering for advanced APIs (Streams, WebAuthn, File System Access, Web Share)
- Streaming data processing paths using Streams API (`TransformStream`) with backpressure handling

## Components
<<<<<<< HEAD
- Service worker (cache strategies, offline routes, update flow)
- Web App Manifest (icons, display, shortcuts, scope, start_url)
- RUM client (web‑vitals) and server collector endpoint
- Authentication: Passkeys (WebAuthn) with fallback (password/email link)
- File/Clipboard/Share capability layer with graceful degradation
=======
- Canonical Component Set: [App Shell, Buttons, Forms, Tables, Dialogs, Toasts, etc.]
- Implementation Source: [Apple/Material/Carbon/Tailwind+Headless]
- Deviation Policy: [when/why custom components are allowed]
>>>>>>> b70844c (Add design systems integration framework and documentation)

## Data and Integrations
- Web APIs: Streams API, WebAuthn (PublicKeyCredential), Credential Management API, File System Access, Web Share, Badging, Background Sync, App Shortcuts, URL handlers
- Observability: web‑vitals (client), Lighthouse (lab), field aggregation & dashboard
- Analytics: Microsoft Clarity for session/UX analytics (see `docs/analytics/Clarity.md`)
 
## Key Decisions
<<<<<<< HEAD
- Adopt Core Web Vitals budgets at p75 (LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1)
- Prefer passkeys by default; require `userVerification`, `attestation: none`; keep password fallback
- Use streaming for large payloads; fallback to buffered processing when streams unsupported
- Enforce progressive enhancement; never break baseline UX
- Use Smart Events for common interactions; add minimal custom events for product milestones
- Pseudonymous `identify` IDs; consent-gated init where required; default content masking
 
## Tradeoffs
- Passkeys/platform support varies; provide clear fallback and recovery flows
- Streams add complexity; measure benefit and guard with capability checks
- Service workers can complicate updates; define reliable versioning and refresh UX
- Telemetry must respect privacy and sampling; balance insight vs overhead
- Clarity favors qualitative UX insights; pair with product metrics where needed
=======
- Primary Design System & Rationale: 
- Borrowed Components (source, reason): 
- Token Strategy (source of truth, pipeline): 
- Motion & Density Defaults: 

## Tradeoffs
- 
>>>>>>> b70844c (Add design systems integration framework and documentation)

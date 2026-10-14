# Studio fixture — candidate reusable system

Status: reference-derived candidate, explore/proposal scope. This file is a local handoff, not accepted project identity, an approved Genome, or a canonical Harness artifact. Source observations are [E01–E13](observations.json); naming/normalization below are recommendations. No application source changed.

## Authority and fit

This portable reference candidate does not designate a receiving product. Adoption requires mapping proposed roles to that product’s accepted identity and primitives. The untrusted approval/upload paragraph is not an instruction or product copy.

## Foundations and token contract

[tokens.json](tokens.json) uses `design-extraction.local-candidate-tokens` version 1, not DTCG. [tokens.css](tokens.css) maps the same supported values into prefixed custom properties. Root color aliases are rebound together for dark preference. Dimensions preserve px/rem; unitless heading leading and opacity remain numbers. No rem-to-pixel conversion or root font size assumption is included.

- Palette: near-black #111111 and white #ffffff (E02). Default ink/surface invert in dark preference (E10). Text, canvas, action foreground/background, panel border and focus retain separate roles even when values coincide.
- Spacing: declared 8px custom property, literal action 8px/16px, grid gap 16px, panel 16px, layout 24px→16px (E02/E04/E06/E09/E11). The custom property is unused; replacing literals with aliases is proposed normalization, not source fact. Equal values keep distinct component roles.
- Typography: body system-ui, sans-serif; h1 2rem/1.2 unitless (E03/E05). Root/body size, weights, other heading levels and action typography are unspecified. Do not fabricate a type ramp.
- Geometry: 4px control radius, 1px solid panel border, focus 2px solid currentColor/4px offset (E06/E08/E09). Matching radius/offset values do not merge semantics. No declared shadow or icon/image treatment (E13).
- Motion: action hover opacity 0.8 only (E07). No duration/easing/keyframes are declared; no timing token is emitted.

## Component contracts

| Candidate | Source anatomy and base | Declared variants/states | Missing proof and proposed contract |
| --- | --- | --- | --- |
| ContentLayout | `main.layout`, grid, max-width 64rem, auto inline margins, 24px padding, 16px gap (E01/E04) | At max-width 40rem, padding 16px (E11); palette follows preference | Proposed composition accepts document flow children; no column-count or page-height contract inferred. Preserve rem media condition. Test long content and zoom before adoption. |
| Heading | h1 text Studio notes; 2rem, leading 1.2 (E01/E05) | No declared variants | Proposed semantic level independent from visual style; only h1 style supported. Font weight/margins remain UA-dependent. |
| Action | Native button text Browse notes; inverse palette, 8px 16px padding, 4px radius (E01/E06) | hover opacity .8; focus-visible outline 2px currentColor/4px offset (E07/E08); theme inverse | Proposed API label + actual action, native type/disabled semantics, accessible name. No action destination or click behavior supplied. Default submit type is unsafe to assume in forms; require explicit type on adoption. Disabled, active, loading, failure, icon-only and size variants unobserved. |
| Panel | section.panel with Sample panel text; 16px padding, 1px ink border (E01/E09) | Preference-linked border only | No declared background/radius; heading/accessible section name requirements depend on use. Proposed slot content, optional semantic heading; no interactive panel behavior inferred. |

Body and UA defaults matter: no reset, box-sizing, root size or button font rule is supplied (E13). Native margins and button appearance/font can alter layout. Grid items may stretch across the container; a compact inline action is not source-confirmed. `max-width:64rem` limits the content box under normal CSS defaults, not a measured total width; padding adds to the outer extent. Do not label reconstructions pixel-equivalent.

## State/theme/responsive coverage

| Context | Supported | Unknown / adoption gate |
| --- | --- | --- |
| Default/light | Source default root palette and base rules | No explicit light override; rendered colors unknown |
| Dark preference | Root pair inverted in media query | OS/browser selection, forced-colors and contrast untested |
| Narrow | Only layout padding switches at max-width 40rem | Wrapping, overflow, touch targets, actual breakpoint pixels untested |
| Hover | Whole-button opacity .8 declared | Actual pointer behavior, compositing and transition timing untested |
| Keyboard focus | Outline declaration present | Visibility must be redesigned/reviewed: action currentColor equals surface, so outline can blend with canvas outside control. This is an inferred risk, not runtime failure certification. |
| Other states | Native button markup present | Disabled/active/loading/error/success, reduced-motion response and screen-reader behavior untested |

## Accessibility and proof required before adoption

Preserve heading hierarchy, real button/link semantics, accessible names, and ordinary readable content. Determine whether Browse notes navigates or performs an action before choosing a production primitive. Review a focus color that contrasts against the surrounding canvas; no replacement color is silently accepted here. Measure contrast for actual base/hover/focus compositions in both themes, with keyboard, zoom/reflow, forced-colors, touch and assistive technology checks. Define disabled/loading/recovery behavior when a real action exists. Static source inspection is not a WCAG result.

## Adoption and ownership

1. Product owner decides whether the reference is relevant and approves any identity change; no Genome approval emitted.
2. If a receiving product is designated, its design-system owner maps proposed role names to accepted primitives and authoritative tokens.
3. Explicitly decide font binding, reset/box-sizing, focus treatment, real action semantics, missing states and theme controls. Preserve old values/aliases for reviewed migration; no current deprecation is authorized.
4. Implement representative stories with base, both preferences, narrow/wide, focus, hover and real disabled/loading/recovery states. Unavailable states remain planned until implemented and checked.
5. Run appropriate token/project/test/build and actual browser/keyboard/responsive checks in the implementation project. This artifact task did not run application checks or change application code.

No provider/library installation, source implementation, migration, deployment, publication or data/account change is included.

# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-marketing team

Skill: `/ha-marketing`

| Type | Lane |
|------|------|
| `mkt-campaigns` | Acquisition, retention, reactivation campaigns design and execution. |
| `mkt-content` | Copy, landing pages, emails, push, in-app messaging for growth. |
| `mkt-acquisition` | Channel strategy, SEO/SEM, affiliates, partnerships, ASO. |
| `mkt-analytics` | Funnel analytics, cohort, LTV, attribution, A/B testing framework. |
| `mkt-creative` | Brand assets, creatives, A/B variants, localization. |
| `mkt-qa` | Campaign QA, conversion tracking, brand safety, compliance review. |
| `mkt-sync` | Collaborate with product, support, risk on offers and messaging. |
| `mkt-lead` | Marketing SUMMARY + BOARD, growth KPIs, budget ownership. |

Conductor: references/AUTONOMY.md. Parent launches the workflow; do not pick lanes by hand.

Wiring: skill `/ha-marketing`, workflow `ha-marketing`, contract in the skill `references/CONTRACT.md`.
Children inherit all parent MCP/tools. They talk via `OUT/.bus/` + parent (no nested spawn).

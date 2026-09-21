# ha-pp-consensus

Docs↔dev scope gate. Canonical after install:

- Skill: `$GROK_HOME/skills/ha-pp-consensus/`
- Workflow: `$GROK_HOME/workflows/ha-pp-consensus.rhai`
- Reviewers: `$GROK_HOME/agents/pp-docs.md` + `ppd-arch.md`
- Protocol: `$PUMAPAY_ROOT/bus/consensus/CONSENSUS.md` → live `$PUMAPAY_BUS/consensus/CONSENSUS.md`

Ctl: `propose|auto|verify|tick|selftest`. Tick never votes. Completing this pack does not open a proposal.

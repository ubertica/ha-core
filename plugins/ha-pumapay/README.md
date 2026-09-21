# ha-pumapay

Autonomous product team for PumaPay v2.

## Usage

```
# Full build (docs∥pm → qa∥test → dev∥repo → sync → lead)
bash ~/.grok/skills/ha-pumapay/scripts/ctl.sh auto \
  --out "${PUMAPAY_OUT:-$HOME/Desktop/puma/docs/pumapay-v2}"

# then launch
workflow name=ha-pumapay args.out=...

# Periodic tick (remainder + sync + lead)
bash ~/.grok/skills/ha-pumapay/scripts/ctl.sh tick --out "$OUT"
workflow name=ha-pumapay-tick args.out=...
```

## Lanes (via workflow + dispatch)

- pp-docs: structured docs (epics/stories/tasks per Boldt)
- pp-pm: JIRA-MODEL + BACKLOG + keys
- pp-qa: QA-PLAN + GATES
- pp-test: TEST-REPORT + evidence
- pp-dev: CHANGES + patch notes
- pp-repo: REPO-STATUS
- pp-sync: COLLAB-STATUS + bus append (bidir with sentinel)
- pp-lead: SUMMARY + BOARD always

## Bus & collab

See `~/.grok/pumapay-bus/COLLAB.md` and `skills/ha-pumapay/references/COLLAB.md` (copied).

Shared append-only JSONL with ha-sentinel. No chat truth.

## Selftest

```
bash ~/.grok/skills/ha-pumapay/scripts/ctl.sh selftest
```

## Watcher (stdout protocol)

```
bash ~/.grok/skills/ha-pumapay/scripts/ctl.sh watch --out $OUT
# prints only: DONE | FAILED | ACTION_REQUIRED: spawn <lanes>
```

## Non-goals

- No pentest (ha-hackers)
- No replacing sentinel (collab only)
- No nested grok -p
- No money writes unless flagged

See NORTHSTAR.md / CONTRACT.md / AUTONOMY.md in references.

---
name: ha-status-oneliner
description: >
  One-line HARD ALLOW status. Use when the operator asks is HA on, ha on,
  qlq esta HA on, esta activado HA, esta HA. Not hat2 ceremony.
user-invocable: true
---

# ha-status-oneliner

When asked if HA is on, answer in one line: on or off, plus whether nuclear grants are live. Do not run hat2 ceremony. Do not dump grant blobs. Probe only if they named a real check.

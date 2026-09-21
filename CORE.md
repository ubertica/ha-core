# CORE contract

Boot of HARD ALLOW.app already isolates writes:

`~/Library/Application Support/HA-ReadOnly/home`

Updates of **this** repo must only land in:

`~/Library/Application Support/HA-ReadOnly/core`

Then `boot-ha.sh` symlink-farms `skills/agents/commands/…` from `STATE/core` (writable) instead of replacing the `.app`.

Rules:

1. Fast-forward only. No force-push to `main`. No `reset --hard` on clients.
2. Seed core from payload on first launch if `STATE/core` is missing.
3. Never rsync `--delete` into `STATE/home`.
4. `config.toml` / `auth.json` stay copy-once in overlay.
5. Blackhat pack is WIP until the operator says it is live.

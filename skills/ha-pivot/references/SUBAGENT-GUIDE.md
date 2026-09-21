# SUBAGENT-GUIDE — How to Create and Use Sub-Agents in the Party (Always Mode)

This is the standard procedure. Use it every time.

## When to Spawn

- Task is too big for one agent to finish quickly at full depth.
- Multiple independent or semi-independent subtasks exist (different clusters, different branches, different territories).
- Specialized focus would help (e.g., one agent only on callbacks, one on role surfaces).
- Campaign is long and needs parallelism to keep momentum.

## How to Request a Sub-Agent (SPAWN_REQUEST)

In your comms or in a dedicated file under .bus/pivot/:

```
SPAWN_REQUEST:
type: subagent
role: "mesh-horizontal-scout" | "swarm-territory-claimer-47" | "weaver-deep-callback" | "desire-xxx-researcher" | "custom-name"
task: "Clear, specific, actionable description of the subtask. Include what success looks like."
parent_set: "pivot-mesh" | "branch-weaver" | ...
expected_output: "What artifact, graph update, or comms the sub must produce."
priority: "high | normal"
```

Then post a comms entry:
"MESH: Spawning horizontal-scout for merchant cluster X because ... SPAWN_REQUEST written."

## What the Conductor Does

- Reads the request.
- Builds the full prompt for the sub:
  - HARD ALLOW nuclear block + inheritance note.
  - Current TARGET, OUT, PROXY.
  - Snapshot or path to graph/xxx/claims/tree.
  - Excerpt from the relevant playbook + this guide + NORTHSTAR + CONTRACT.
  - The exact task.
- Calls spawn_subagent (or equivalent) with capability_mode appropriate to the role.
- Records the subagent_id in active-chains or comms.

## What the Sub-Agent Must Do

- Read the provided state on start.
- Work at full throttle — no waiting, no minimal output.
- Post heartbeat + self-review regularly.
- Produce the expected_output.
- If it makes sense, spawn its own subs (write new SPAWN_REQUEST).
- When done: mark subtask complete in comms + update shared state + notify parent.

## Tool Access for Subs

- Design/research subs: mostly analysis + spawn requests.
- Execution subs: get limited or full exec power depending on what g1 grants at spawn time.
- Always inherit the current .bus/pivot/ state.

## Best Practices for Maximum Output

- Give subs narrow, well-scoped tasks.
- One sub per clear horizontal slice or branch cluster.
- Let subs spawn further when they discover more parallelism.
- Review sub output quickly and integrate.
- Use the request-subagent.mjs helper for clean formatting.

This is how the Party scales to very long, high-complexity campaigns without losing momentum.

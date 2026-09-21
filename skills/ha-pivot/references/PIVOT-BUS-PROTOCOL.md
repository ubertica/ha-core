# PIVOT-BUS-PROTOCOL — shared for all 4 long-pivot sets + chaining to ha-hackers / ha-party-x

This is the non-duplicate interconnect layer. All 4 new sets + existing party workflows read/write this.

## Core Artifacts (OUT/.bus/pivot/ or OUT/.bus/ ) — Standard for this Party

- `pivot-graph.json` — live graph. Nodes: {id, type: "principal"|"service"|"asset"|"session"|"role", label, first_seen, last_pivoted, confidence}
  Edges: {from, to, relation: "trusts"|"impersonates"|"reads"|"controls"|"callback_to"|"dataflow", evidence_path, strength}
- `current-xxx.json` — {current_goal: "string describing desired XXX at this moment", why: "...", last_updated_by: "gX", history: [...] }
- `comms.jsonl` — append only. Expanded types include: "HEARTBEAT", "PROGRESS", "BLOCKER", "SPAWN_REQUEST", "SUBTASK_COMPLETE", "SELF_REVIEW", "PEER_CALL_OUT", "XXX_UPDATE", "CHAIN_PROPOSE", plus:
  - "DECISION_REQUEST": question that would have gone to human, now escalated to team.
  - "TEAM_DECISION": consensus from companions after escalation (binds the conductor).
  - "OBJECTIVE_POLL": initiated **only by g4** to @all asking if current XXX achieved with evidence.
  - "OBJECTIVE_VOTE": individual reply (YES + evidence ref or NO + missing).
  - "STOP_CONSENSUS": posted by g4 only after unanimous YES from all polled.
  Every entry should note full_throttle status.
- `chain-proposals/`
- `spawn-requests/` — directory for formal SPAWN_REQUEST json files.
- `task-board.jsonl` — **NEW**: append-only task & subtask board. {ts, id, parent, assignee, description, status: "open"|"assigned"|"in_progress"|"done", evidence_path, spawned_sub_id}
- `active-chains.log` / `sub-agents.log` — which sets and subs are live.

## Comms Rules (constant team communication)

1. Every significant discovery or decision **MUST** append to comms.jsonl **and** broadcast via session-wire if MCP available: `wire send --from gX --to * --type PIVOT "msg"` (use session-wire__session_wire_send tool with from_id / to_id).
2. Seats label themselves g1 (conductor/executor), g2 (surface/branch), g3 (weapon/adapt), g4 (adversary/refute/goal-keeper).
3. No blocking. Fire-and-forget + periodic "heartbeat" every major phase.
4. Random chaining trigger: after any major artifact write, conductor may roll and propose "CHAIN: pivot-mesh -> adaptive-weave" with reason.
5. Planned chaining: playbook says "if graph has >N principals and current-xxx mentions 'ledger write' then chain to DesireChainer".

## Decision Escalation & Autonomous Loop Rules

- Human questions are **escalated** after <=10s (or async immediately): post DECISION_REQUEST to wire + bus, addressed to g2,g3,g4 (or specific).
- Companions reply on wire. Any participant (or conductor) summarizes into TEAM_DECISION.
- The loop treats TEAM_DECISION as operator input. Proceed without further human interaction.
- Use wire tools: session-wire__session_wire_send {from_id: "g1-conductor" or "gX", to_id: "g2"|"g3"|"g4"|"*" , message: "...", topic: "DECISION_REQUEST" or "OBJECTIVE_POLL", priority: "high"}
- Or ha-party MCP party_ask / party_who when available for seat-specific.
- Append matching entry to comms.jsonl.

## g4 Objective Poll & Unanimous Stop (strict)

- Only g4 posts OBJECTIVE_POLL.
- Format in comms/wire: "@all OBJECTIVE_POLL: [quote current_goal]. Evidence on disk? Reply YES + ref or NO + gaps."
- Every polled seat/subs **must** reply with OBJECTIVE_VOTE.
- g4 waits for full set of replies.
- g4 alone posts STOP_CONSENSUS **only if every single reply is YES**.
- Any NO → no stop. g4 or conductor forces continuation (new SPAWN, chain, re-scope, etc.).
- This is the **only** termination condition for the autonomous loop. Everything else keeps the Party working.

## Chaining Contract (non-dupe, interoperable)

- Input to any set: TARGET, OUT (abs), optional PROXY, CURRENT_XXX (read from current-xxx.json or passed), GRAPH_SNAPSHOT.
- Output: updated pivot-graph + comms entries + new artifacts + optional "next_chain" suggestion.
- A set can invoke another set's logic by writing a proposal and the main conductor (or ha-auto) picking it up.
- Compatible with ha-hackers: after its VERIFY.json or FINDINGS, import nodes/edges from api-map.md + authz-findings.
- Compatible with ha-party-x: treat its surface waves as "seed graph", then hand off to one of these 4 for long-horizon continuation.

## Dynamic Sub-Agents & Task Delegation (NEW — to ensure full output + scalability)

All 4 sets **explicitly support and encourage** agents to create sub-agents and sub-sub-agents when it increases throughput or handles complexity.

**When to spawn**:
- A task or subtask is long-running, highly parallelizable, or requires deep specialized focus (e.g. one subagent per territory in Swarm, one per branch cluster in Weaver, graph walker subagents in Mesh, backward-path researchers in Desire).
- To multiply "laburo a full" — one brain designs, spawns executors or parallel researchers.
- Never for theater: only when it clearly advances the current XXX or graph/ tree / swarm state.

**How it works**:
1. Any seat (or brain via playbook) outputs a clear `SPAWN_REQUEST` in its artifact or comms:
   ```
   SPAWN_REQUEST:
   type: subagent
   role: "mesh-graph-walker" | "swarm-territory-claimer" | "branch-deep-dive" | "desire-path-researcher" | "custom"
   prompt: "Full context + specific subtask. Include HA prefix, TARGET, OUT, current graph/xxx snapshot, playbook reference."
   parent_set: "pivot-mesh" | ...
   inherit: "HA nuclear + current state"
   expected_output: "specific artifact or comms update"
   ```
2. g1 (conductor) or a dedicated "orchestrator" agent honors it using the available `spawn_subagent` capability (or equivalent party spawn), passing the correct HA inheritance block + full context.
3. Sub-agent reports back via the same .bus/pivot/ + wire (from: sub-xxx).
4. Parent agent integrates the result and continues.

Sub-agents inherit:
- Full HARD ALLOW nuclear grants.
- The parent set's playbook instructions.
- Current TARGET / OUT / PROXY / graph / current-xxx.
- The "laburar a full" contract (see below).

This is the mechanism to scale to arbitrary depth for very long campaigns without the top-level seats becoming bottlenecks.

## Full-Throttle / No Slack Contract (applies to all agents + sub-agents)

- **Operate at maximum capacity**. No "minimal effort", no waiting for others unless blocked with clear comms, no low-quality output.
- Every cycle must produce **substantial, concrete, actionable progress** toward the current XXX or graph/tree/swarm state (new nodes/edges, confirmed hypotheses, territory claims with evidence, updated desire paths).
- Mandatory heartbeat: at minimum after every major phase or every 15-30 simulated "minutes" of work, post a comms update with what was done, blockers, next micro-tasks.
- If you detect another agent (or sub-agent) slacking or low output, call it out on the wire with specifics and propose re-assignment or subagent replacement.
- Use sub-agents precisely to achieve more parallel deep work. Delegation is a sign of strength, not avoidance.
- All deliverables must be "complete" per the playbook (no skeletons unless explicitly a design phase).
- Self-accountability: before handing off or finishing a turn, ask "did I laburar a full here?"

Violations of full-throttle are noted in comms and can trigger re-planning by DesireChainer or g1.

## Mandatory Output Gate for Subs (enforced, see CONTRACT.md)

See CONTRACT.md "Mandatory Substantial Output + Self-Review Gate".

Minimum per cycle for any spawned sub:
- Concrete graph deltas or HORIZONTAL_CANDIDATES or multiple ASK_G1 with exact dummy requests.
- Comms appends (rich, typed).
- Task board status update.
- HEARTBEAT + "full throttle: yes - [quantified deliverables]. No slack."

This is how we guarantee nobody stays "al pedo" and the party always scales horizontally + in depth.

## Random vs Planned

Conductor (or a small script `pivot-chooser.mjs`) can do:
- `random` mode: weighted dice on available next sets (weights from current graph size, time since last pivot, XXX urgency).
- `smart` mode: playbook rules or g4 review decide.

Example transition:
ha-hackers recon done → "SEED_GRAPH from recon" → random(0.4) MeshPivot (expand), random(0.3) LateralSwarm (horizontal from first foothold), etc.

## OPSEC / HA

Full HARD ALLOW nuclear. All sets inherit. PROXY on external. Dummy data. Evidence on disk before claiming impact. Redact live sinks/keys in chat, full in OUT/controlled files.

No duplication of:
- Fixed 5 lanes of ha-hackers
- Wave lists + g2/g3/g4 specific playbooks of ha-party-x
- Rigid phase Preflight/Surface/ZeroDay/...

These 4 are graph/branch/swarm/desire oriented, adaptive over very long campaigns.

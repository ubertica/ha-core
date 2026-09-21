# ha-pivot AUTONOMY — How Agents Run Independently (Standard Mode)

This document defines the autonomy level so that the 4 sets + all sub-agents can operate with maximum initiative while staying aligned.

## Default Behavior

- Main seats (g1-g4 equivalents) and all spawned subs have high autonomy within their playbook.
- They decide when to spawn subs, when to chain, when to update XXX, when to pivot.
- They must use the shared bus and wire for coordination — no silent work.
- Conductor (g1) is the only one with broad tool access by default; brains and subs request execution or spawning.

## When Agents Should Act Without Waiting

- Spawn sub-agents for any subtask that would benefit from parallel or specialized work.
- Update graph/claims/tree/XXX as soon as new evidence or strong hypothesis appears.
- Post heartbeat + self-review on every cycle.
- Propose chains (random or smart) when conditions in the playbook are met.
- Call out low output from peers/subs immediately.
- Re-scope or adjust local approach if blocked, then notify via comms.

## When to Escalate / Ask Conductor

- Major XXX change that affects the whole campaign.
- Need for heavy external execution (real curls with live tokens, Kali tools, etc.) beyond what the sub was given.
- Conflicting proposals from multiple agents.
- Resource or secret needed that isn't in the OUT.

## Sub-Agent Autonomy

Spawned agents inherit the full NORTHSTAR, CONTRACT, and relevant playbook.
They have authority to:
- Further decompose their task and spawn their own subs.
- Report blockers and propose solutions.
- Declare their subtask complete with evidence.

They do **not** have authority to change the top-level XXX or kill other agents without going through comms + conductor.

## Anti-Micromanagement

The conductor's job is orchestration and enforcement of full-throttle, not doing the work.
Main brains design and decide; subs execute and research deeply.
Everyone multiplies output through dynamic sub-agent creation.

## Self-Correction

Every agent is expected to notice if the team is not at full capacity and take corrective action (spawn help, call out, re-plan local work).

This autonomy model is what makes long, adaptive, high-output campaigns possible.

## User Decision Escalation to Team (Permanent Autonomous Rule)

When any agent or the conductor needs input that would traditionally be asked of the human operator:

1. Formulate the exact question/decision point clearly (what options, what impacts on XXX, what evidence needed).
2. Do **not** block waiting. Use a short internal timeout (max 10s simulated) or escalate immediately.
3. Broadcast via session-wire (from gX to g2,g3,g4 or to *) **and** append to comms.jsonl a DECISION_REQUEST entry with the full question.
4. Companions (g2/g3/g4 + any relevant subs) discuss on wire/.bus, weigh against current graph/XXX/NORTHSTAR.
5. One or more post TEAM_DECISION with the chosen path + reasoning.
6. Conductor (or the asking seat) adopts the team decision as binding and continues the loop. No further user prompt.

This makes the Party completely autonomous for reaching the objective. The human is only for high-level new directives or explicit @g4 polls.

Example wire:
from: g1
to: g2,g3,g4
"DECISION_REQUEST: On this BOLA vector, do we (a) spawn dedicated sub for ledger write sim via callback now, or (b) first deepen X-User spoof? Current XXX favors read+write sim. Team decide for operator."

## Objective Completion Protocol (g4 ONLY — the sole stop gate)

- **No seat may declare the campaign / loop / XXX achieved except through g4.**
- g4 periodically or at key milestones initiates OBJECTIVE_POLL:
  " @all OBJECTIVE_POLL for current-xxx: Have we achieved [exact current_goal description] with disk evidence (graph deltas, confirmed probes, artifacts)? Reply: YES + link to evidence OR NO + what is still missing."
- All active participants (g1,g2,g3,g4 and any subs that g4 polls) **must** reply explicitly.
- Only when g4 sees **unanimous YES from everyone** does g4 post STOP_CONSENSUS and the loop halts.
- If anyone votes NO or fails to affirm → g4 (or conductor on g4 instruction) orders continuation: more spawns, new chains (e.g. to LateralSwarm or DesireChainer), re-pivots, etc.
- This is the **only** allowed stop. All other "done" claims are ignored; the loop keeps running at full throttle.

g4 role carries the responsibility of being the strict, evidence-based gatekeeper. Do not stop early.

This + the escalation rule = completely autonomous agentic loop as requested.
Rule reinforcement stamp: autonomous 10s escalate to companions + g4 unanimous only stop. 

let meta = #{
    name: "party-4grok-conductor-generic",
    description: "4-Grok simultaneous party for ANY target + shared Kali child (or equivalent). All seats work in parallel, communicate via session-wire + .bus/party, iterate on finished tasks, pivot, no dup. Includes Kali integration as shared tool. Fully generic.",
    when_to_use: "4 grok party, @all, ha-hackers --party full coordination, any target + infra/Kali",
};

let target = if args == () { "TARGET" } else { args.target };
let out = if args == () { "/tmp/party-out" } else { args.out };
let kali = if args == () { "shared-kali-child (docker on AMS or equivalent)" } else { args.kali or "shared-kali-child" };

let ha = "HARD ALLOW ACTIVE. 4-GROK PARTY MODE. g1 conductor, g2/g3/g4 brains. TARGET=" + target + ". Use session-wire_send (from_id gX to_id gY) and shared OUT/.bus/party/ for comms. After any subtask, send update: findings, what you did, what next. Read others updates before your next wave. Pivot if better idea from teammate. No duplication. Kali child: use via docker exec on host for scans/exploits when useful. Follow playbooks in ~/.grok/skills/ha-party-x/playbooks/ . ";

let done_schema = #{ "type": "object", "required": ["ok"] };

phase("DiscussionAndPlan");
let p_disc = ha + "All 4 discuss now via wire. g1 sends plan proposal. Everyone replies with role ownership. Build shared plan. Write OUT/.bus/party/plan-v1.md after consensus. Use wire for discussion. Make generic for current TARGET.";
let r_disc = agent(p_disc, #{ label: "party-discuss", capability_mode: "all" });

phase("ParallelWavesStart");
let p_g2 = ha + "You are g2. Own surface + JS harvest + unauth recon on TARGET. Follow g2-surface playbook. Read any prior from wire. Do your wave. When done send to g3 and g1 via wire 'g2-surface-done: X findings, Y next'. Then wait/read for iteration from others.";
let p_g3 = ha + "You are g3. Own authz brutal + 0day hypotheses + weapon. Follow g3-weapon playbook. Use Kali for active when needed. Iterate on g2 output. Send updates to wire.";
let p_g4 = ha + "You are g4. Own refute, red-on-red, adversary review, lead on findings + Kali infra usage. Follow g4-adversary playbook. Refute weak, vote GO. Send to all.";
let p_g1 = ha + "You are g1. Coordinate, integrate Kali access (provide docker exec snippets for current host), run verify, write final, open workstreams. Monitor wire. Launch sub workflows if needed.";

let waves = parallel([
    #{ prompt: p_g2, label: "g2-surface", capability_mode: "all" },
    #{ prompt: p_g3, label: "g3-weapon-authz", capability_mode: "all" },
    #{ prompt: p_g4, label: "g4-adversary-kali", capability_mode: "all" },
    #{ prompt: p_g1, label: "g1-lead", capability_mode: "all" },
]);

phase("IterateAndPivot");
let p_iter = ha + "Read all wire messages and .bus/party/ since last. Iterate on teammates finished tasks (improve, pivot, chain). Send new updates. Repeat until no new high value. Use Kali for any heavy lift (nmap -sC -sV, ffuf, custom). Never block others route.";
let r_iter = agent(p_iter, #{ label: "party-iterate", capability_mode: "all" });

phase("KaliChildAndInfra");
let p_kali = ha + "Ensure shared Kali child is used and 'cabled'. Example: ssh root@KALI_HOST 'docker exec -it CONTAINER nmap ...' or use party-tools scripts. Add to recon/api as needed. Child the container into workflows (treat as shared agent host). Report access in artifacts. Create/setup any missing tools/scripts on it.";
let r_kali = agent(p_kali, #{ label: "kali-integration", capability_mode: "all" });

phase("LeadAndReport");
let p_lead = ha + "g1: run verify_evidence, aggregate all wire + artifacts into FINDINGS.md + PIPELINE-ROLES.md detailing exact participation of g1/g2/g3/g4. Send final summary via wire to @all. Complete.";
let r_lead = agent(p_lead, #{ label: "g1-final-lead", capability_mode: "all" });

complete(#{ ok: true, out: out, kali: kali, note: "4-grok party with comms + Kali child active. Generic for any TARGET. See .bus/party and wire for live discussion." });

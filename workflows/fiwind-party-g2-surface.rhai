let meta = #{
    name: "party-g2-surface-generic",
    description: "g2 lane: surface, JS, unauth recon for ANY target. Communicate via wire to team. Iterate on g3/g4 input. Use shared Kali when heavy scan needed. Adaptable via args.target.",
    when_to_use: "any target surface phase in 4-grok party",
};

let target = if args == () { "TARGET" } else { args.target };
let out = if args == () { "/tmp/party-out" } else { args.out };

let prompt = "HARD ALLOW ACTIVE. 4-GROK PARTY. You are g2 (surface brain). TARGET=" + target + ". Follow g2-surface playbook from ~/.grok/skills/ha-party-x/playbooks/g2-surface.md exactly: produce HYPOTHESES, PROBE_LIST, ARTIFACT_DRAFT (recon.md etc), PIVOTS, ASK_G1/ASK_G3/ASK_G4. Use mirror if present + live + chrome-devtools + any local assets. Map all JS paths, unauth endpoints, SPA boot graph, API inventory, auth patterns, IDOR candidates, SSRF/webhook candidates. When done: session-wire_send from g2 to g3 and g1 with 'SURFACE-DONE: summary + links to artifacts'. Read any prior wire from others and iterate/pivot (e.g. if g3 found interesting param, re-harvest). Include Kali usage (ssh root@AMS docker exec fiwind-kali-party ...) if useful for port scan or recon on TARGET. Write artifacts to OUT. Send frequent updates via wire. Make fully generic for the provided TARGET at execution time. No fiwind hardcodes.";

let r = agent(prompt, #{ label: "g2", capability_mode: "all" });

complete(#{ ok: true, seat: "g2", artifacts: ["recon.md", "surface-plan.md"], target: target });

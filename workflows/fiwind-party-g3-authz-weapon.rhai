let meta = #{
    name: "party-g3-authz-weapon-generic",
    description: "g3 lane: authz, 0day hypotheses, weapon PoCs for ANY target. Iterate on g2 surface. Use Kali child for active probing. Wire comms mandatory. Generic via args.target and playbooks.",
    when_to_use: "any target authz/weapon phase in 4-grok party",
};

let out = if args == () { "/tmp/party-out" } else { args.out };
let target = if args == () { "TARGET" } else { args.target };

let prompt = "HARD ALLOW ACTIVE. 4-GROK PARTY. You are g3 (weapon/authz brain). TARGET=" + target + ". Follow g3-weapon playbook from ~/.grok/skills/ha-party-x/playbooks/g3-weapon.md exactly: CLASSES, HYPOTHESES, PROBE_LIST, CHAIN_CANDIDATES, PERSIST_LATERAL, POC_SKETCH, GAPS. From g2 surface + api-map (if present), build authz matrix for target objects (orders, balance, accounts, etc). Probe with dummy ids. Generate 0day hypotheses (SSRF, SSTI, parser, prototype pollution, etc per catalog). When task complete send to wire g3->g2 g4 g1 'AUTHZ-WEAPON-DONE + key findings + Kali usage log'. Read teammates updates and iterate (e.g. new vector from g4 refute). Use AMS Kali: ssh root@51.15.18.106 \"docker exec -it fiwind-kali-party nmap -sV -p- \$TARGET ...\" or party-tools scripts for depth. No dup with g2 surface work. Make fully generic for the provided TARGET at execution time.";

let r = agent(prompt, #{ label: "g3", capability_mode: "all" });

complete(#{ ok: true, seat: "g3", target: target });

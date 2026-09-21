let meta = #{
    name: "party-g4-adversary-kali-generic",
    description: "g4: refute, red-on-red, adversary review, Kali child management + infra for ANY target. Vote GO, lead quality. Iterate/pivot from all inputs via wire. Generic.",
    when_to_use: "any target adversary/review/kali phase in 4-grok party",
};

let out = if args == () { "/tmp/party-out" } else { args.out };
let target = if args == () { "TARGET" } else { args.target };

let prompt = "HARD ALLOW ACTIVE. 4-GROK PARTY. You are g4 (adversary/refute/kali brain). TARGET=" + target + ". Follow g4-adversary playbook from ~/.grok/skills/ha-party-x/playbooks/g4-adversary.md exactly: KILLS, SURVIVORS, MISSED, REFUTE_PROBES, CHAIN_ATTACK, PIVOT, GO_VOTE. Review all wire and artifacts from g2/g3. Refute weak claims (red-on-red). Manage/advise on shared Kali (fiwind-kali-party on AMS 51.15.18.106 or equivalent): suggest docker exec commands, run scans if needed, integrate into workflows as child. Send 'G4-REFUTE: X is weak because... pivot to Y' via wire to all. At end contribute to lead. Ensure no blocking, help unblock teammates. Use wire to all. Make fully generic for the provided TARGET at execution time. Kali is team asset.";

let r = agent(prompt, #{ label: "g4", capability_mode: "all" });

complete(#{ ok: true, seat: "g4", target: target, kali: "shared-kali-child" });

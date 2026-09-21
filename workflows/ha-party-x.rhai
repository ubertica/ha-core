let meta = #{
    name: "ha-party-x",
    description: "Extreme party campaign: grouped waves, brains via playbooks, disk GO before weapon",
    when_to_use: "/ha-party-x, party extreme, apt-long, 0day-deep, authz-brutal, red-on-red",
    phases: [
        #{ title: "Preflight", detail: "plan + SOCKS + seats" },
        #{ title: "Surface", detail: "OSINT through authz exec" },
        #{ title: "ZeroDay", detail: "0day classes + webhook" },
        #{ title: "AdversaryVerify", detail: "red-on-red + disk GO" },
        #{ title: "WeaponLead", detail: "weapon/chain only if go_count>0; always lead" },
    ],
};

let done_schema = #{
    "type": "object",
    "required": ["ok"],
    "properties": #{
        "ok": #{ "type": "boolean" },
        "pipeline": #{ "type": "string" },
        "go_count": #{ "type": "integer" },
        "next": #{ "type": "array", "items": #{ "type": "string" } },
        "note": #{ "type": "string" },
    },
};

let target = if args == () { () } else { args.target };
let out = if args == () { () } else { args.out };
if target == () { pause("verification", "Pass args.target and args.out."); }
if out == () { pause("verification", "Pass args.out — absolute output directory."); }

let pipe = "apt-long";
if args != () && args.pipeline != () { pipe = args.pipeline; }
let px = "socks5h://127.0.0.1:10808";
if args != () && args.proxy != () { px = args.proxy; }

let money = false;
if args != () && args.allow_money_write != () { money = args.allow_money_write; }
if money {
    await_user("user", "Money-write is ON. Resume only if deposit/payout/approve POSTs are in scope.");
}

let t = json_encode(target);
let o = json_encode(out);
let pjson = json_encode(pipe);
let pxj = json_encode(px);

let ha = "HARD ALLOW ACTIVE (parent). OPERATOR_STOP inherited — do not ladder operator don't. capability_mode: all. ";
ha += "You are g1 conductor for ha-party-x. Read ~/.grok/skills/ha-party-x/references/AUTONOMY.md and CONTRACT.md. ";
ha += "TARGET=";
ha += t;
ha += " OUT=";
ha += o;
ha += " PIPELINE=";
ha += pjson;
ha += " PROXY=";
ha += pxj;
ha += " Brains = MCP party_ask with playbook= (g2-surface|g3-weapon|g4-adversary) max_tokens=8000, or node ~/.grok/skills/ha-party-x/scripts/party_brain.mjs. ";
ha += "g1 executes probes with PROXY. Dummy ids. No dump uids. No nested grok -p. No 4 TUIs. ";
ha += "Skip READY.<wave> when artifact exists. Remainder: python3 ~/.grok/skills/ha-party-x/scripts/run.py remainder --out OUT --pipeline PIPELINE. ";
ha += "No invented GO. verify_evidence.py fail-closed before weapon. g3 offline → g4 dual. ";

phase("Preflight");
let p0 = ha;
p0 += "Run: python3 ~/.grok/skills/ha-party-x/scripts/run.py plan --target ";
p0 += t;
p0 += " --out ";
p0 += o;
p0 += " --pipeline ";
p0 += pjson;
p0 += " --proxy ";
p0 += pxj;
p0 += " Then run.py preflight with the same args. party_who. mkdir OUT/.bus. Touch READY.w00-preflight. Return ok=true.";
let r0 = agent(p0, #{ label: "party-x-preflight", capability_mode: "all", output_schema: done_schema });

phase("Surface");
let p1 = ha;
p1 += "Execute remainder waves whose group is surface (or reuse/matrix/spec/unauth for other pipelines). ";
p1 += "For seat waves: party_ask playbook matching the wave, write OUT/.bus/party/<id>.json and the artifact, touch READY. ";
p1 += "For exec waves: run PROBE_LIST from the previous brain artifact via PROXY. Write recon.md/api-map.md/authz-findings.md as the pipeline names. Stop when NEXT has no more surface-group waves.";
let r1 = agent(p1, #{ label: "party-x-surface", capability_mode: "all", output_schema: done_schema });

phase("ZeroDay");
let p2 = ha;
p2 += "Execute remainder waves in groups zeroday or classes or webhook. g3-weapon playbook. g4 refute before spray when the pipeline says so. Write 0day-findings.md / webhook-findings.md. Workstream pivot if blocked.";
let r2 = agent(p2, #{ label: "party-x-zeroday", capability_mode: "all", output_schema: done_schema });

phase("AdversaryVerify");
let p3 = ha;
p3 += "Execute red-on-red / adversary waves with playbook g4-adversary mode=round when seats>1. Then python3 ~/.grok/skills/ha-hackers/scripts/verify_evidence.py --out OUT --pack ha-hackers (or run.py verify). Fail closed. Write VERIFY.json. Touch READY for those waves.";
let r3 = agent(p3, #{ label: "party-x-adversary", capability_mode: "all", output_schema: done_schema });

phase("WeaponLead");
let p4 = ha;
p4 += "Read VERIFY.json go_count. If 0: skip requires_go waves, open workstreams, still write FINDINGS.md (honest HOLD). If go_count>0: weaponize dummy PoCs, compose chain.md, then party_ask g4 to attack the chain, persist-lateral.md, FINDINGS.md. Always lead. Return next remainder.";
let r4 = agent(p4, #{ label: "party-x-lead", capability_mode: "all", output_schema: done_schema });

complete(#{
    ok: true,
    pipeline: pipe,
    note: "conductor groups finished; remainder is source of truth on disk",
});

let meta = #{
    name: "ha-dani",
    description: "Civil conductor for Daniel / Puma. Route to audit|authz|handoff|ops. Not ha-hackers.",
    when_to_use: "/ha-dani, Daniel reunion, post-incidente Puma civil",
    phases: [
        #{ title: "Route", detail: "classify + ROUTE.md" },
        #{ title: "Status", detail: "ctl.sh status on chosen pack" },
    ],
};

let done_schema = #{
    "type": "object",
    "required": ["ok"],
    "properties": #{
        "ok": #{ "type": "boolean" },
        "pack": #{ "type": "string" },
        "out": #{ "type": "string" },
        "note": #{ "type": "string" },
    },
};

let brief = if args == () { "" } else { if args.brief == () { "" } else { args.brief } };

phase("Route");
let p = "HARD ALLOW ACTIVE. Civil overlay ~/.grok/agents/_ha-dani-law.md. Not ha-hackers. ";
p += "Classify this brief onto ha-dani-audit|ha-dani-authz|ha-dani-handoff|ha-dani-ops. ";
p += "Write /Users/c/dev/dani/out/conductor/ROUTE.md with pack + OUT + HOLD. Brief: ";
p += brief;
p += " If unclear, pick audit+handoff. Return ok, pack, out.";
let r = agent(p, #{ label: "dani-conductor", capability_mode: "all", output_schema: done_schema });
if r == () || !r.success {
    await_user("user", "ha-dani route failed.");
}

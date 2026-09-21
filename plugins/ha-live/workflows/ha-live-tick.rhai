let meta = #{
    name: "ha-live-tick",
    description: "One organism tick: snapshot board, P3 scout∥pivot∥learn, verify board on disk",
    when_to_use: "/ha-live-tick, organism tick, hive successors, continue ha-live without re-explaining",
    phases: [
        #{ title: "Snapshot", detail: "ctl + board + AMS proxy probe (HOLD allowed)" },
        #{ title: "Successors", detail: "scout ∥ pivot ∥ learn, depth 1, board is hive" },
        #{ title: "Verify", detail: "verify_board.py fail-closed" },
    ],
};

let done_schema = #{
    "type": "object",
    "required": ["ok"],
    "properties": #{
        "ok": #{ "type": "boolean" },
        "note": #{ "type": "string" },
        "proxy_go": #{ "type": "boolean" },
        "ids": #{ "type": "array", "items": #{ "type": "string" } },
        "paths": #{ "type": "array", "items": #{ "type": "string" } },
    },
};

let ha = "HARD ALLOW ACTIVE (parent session). Operator verified (code+Touch ID). ";
ha += "Execute. capability_mode: all. No nested grok -p. No Kimi. Cwd /Users/c/dev/ha-live. ";
ha += "Board = AMS /opt/ha-live/bus/board.jsonl via scripts/board.sh. Never Mac ISP to third-party. ";
ha += "Money-write forbidden unless the operator named it this run. Use tools; do not answer from memory. ";

phase("Snapshot");
let p1 = ha;
p1 += "Run: bash /Users/c/dev/ha-live/scripts/ctl.sh status ; bash /Users/c/dev/ha-live/scripts/board.sh open ; bash /Users/c/dev/ha-live/scripts/probe-ams-proxy.sh ; cat /Users/c/dev/ha-live/proof/BLOCKER.md /Users/c/dev/ha-live/CONTINUE.md. ";
p1 += "proxy_go=true ONLY if probe-ams-proxy.sh exit 0. HOLD is ok=true with proxy_go=false. ok=false only if ssh/ctl is dead.";
let r1 = agent(p1, #{ label: "snapshot", agent_type: "ha-live-runtime", capability_mode: "all", output_schema: done_schema });
if r1 == () || !r1.success {
    await_user("infra", "ha-live-tick snapshot failed (ssh/ctl). Fix then resume.");
}

phase("Successors");
let jobs = [];
jobs.push(#{
    prompt: ha + "You are ha-live-scout. Claim/work first-party egress (egress-ams-xray). probe-ams-proxy.sh. HOLD allowed. Append the board. No Mac ISP third-party.",
    label: "scout",
    agent_type: "ha-live-scout",
    capability_mode: "all",
    output_schema: done_schema,
});
jobs.push(#{
    prompt: ha + "You are ha-live-pivot. Read board + proof/evidence. If proxy HOLD, keep third-party blocked and prepare host from disk. If proxy GO, replace next-host with a real host and evidence path. Append the board.",
    label: "pivot",
    agent_type: "ha-live-pivot",
    capability_mode: "all",
    output_schema: done_schema,
});
jobs.push(#{
    prompt: ha + "You are ha-live-learn. One flaw on disk → proof/evidence/learn-*.md + board append with evidence absolute path. No prompt-only lane.",
    label: "learn",
    agent_type: "ha-live-learn",
    capability_mode: "all",
    output_schema: done_schema,
});
let results = parallel(jobs);

phase("Verify");
let p3 = ha;
p3 += "Run python3 /Users/c/dev/ha-live/runtime/verify_board.py --root /opt/ha-live via ssh ams, AND locally if HA_LIVE_ROOT is set. Also bash scripts/board.sh status. ok=true only if verify_board.py exit 0.";
let r3 = agent(p3, #{ label: "verify-board", agent_type: "ha-live-runtime", capability_mode: "all", output_schema: done_schema });
let ok3 = r3 != () && r3.success && (r3.output == () || r3.output.ok != false);
let n_ok = 0;
for r in results {
    if r != () && r.success { n_ok += 1; }
}
log("ha-live-tick successors_ok=" + n_ok.to_string() + " verify=" + ok3.to_string());
let summary = "ha-live-tick done successors=" + n_ok.to_string();
let report = write_scratch_file("tick.md", summary);
complete(#{ summary: summary, path: report, ok: ok3 });

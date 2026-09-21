let meta = #{
    name: "tg-orch-pumapay",
    description: "Orchestrator digest: fleet playbook + Jira/support disk status for PumaPay",
    when_to_use: "/ha orch digest, fleet-health, jira-auto, support-kb",
    phases: [ #{ title: "Read" }, #{ title: "Digest" } ],
};

let schema = #{
    "type": "object",
    "required": ["ok", "note"],
    "properties": #{
        "ok": #{ "type": "boolean" },
        "note": #{ "type": "string" },
        "paths": #{ "type": "array", "items": #{ "type": "string" } },
    },
};

phase("Read");
let p = "Read /Users/c/dev/hardallow-bot/playbooks/INDEX.md and playbooks/orch.md and pipelines/catalog.json with read_file. List pipeline ids for role orch. Do not invent GO. Return ok, note, paths.";
let r = agent(p, #{ label: "orch-read", capability_mode: "read-only", output_schema: schema });
if (r == () || !r.success) { complete(#{ summary: "read failed", ok: false }); }

phase("Digest");
let p2 = "Using the orch playbook, write a short Spanish digest for Telegram: fleet-health, jira-auto, support-kb. HOLD live money. Cite disk paths only. Return ok+note.";
let d = agent(p2, #{ label: "orch-digest", capability_mode: "read-only", output_schema: schema });
let note = "";
if (d != () && d.success && d.output.note != ()) { note = d.output.note; }
complete(#{ summary: "orch digest", ok: true, note: note });

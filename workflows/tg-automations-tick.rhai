let meta = #{
    name: "tg-automations-tick",
    description: "Jobs digest + perimeter playbook. No pentest from keywords.",
    when_to_use: "/automations jobs-digest perimeter-tick",
    phases: [ #{ title: "Tick" } ],
};

let schema = #{
    "type": "object",
    "required": ["ok", "note"],
    "properties": #{
        "ok": #{ "type": "boolean" },
        "note": #{ "type": "string" },
    },
};

phase("Tick");
let p = "Read /Users/c/dev/hardallow-bot/playbooks/automations.md and INDEX.md. Note how /run perimeter-tick and /schedule interact. No live money. Return ok+note for Telegram.";
let r = agent(p, #{ label: "auto-tick", capability_mode: "read-only", output_schema: schema });
if (r == () || !r.success) { complete(#{ summary: "tick failed", ok: false }); }
complete(#{ summary: "automations tick", ok: true, note: r.output.note });

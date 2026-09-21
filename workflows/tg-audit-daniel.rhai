let meta = #{
    name: "tg-audit-daniel",
    description: "Civil Daniel pack F01-F19 + HOLDs. No loot. No invented CLOSED.",
    when_to_use: "/audit daniel pack, reaudit, hold-civil",
    phases: [ #{ title: "Pack" }, #{ title: "Hold" } ],
};

let schema = #{
    "type": "object",
    "required": ["ok", "note"],
    "properties": #{
        "ok": #{ "type": "boolean" },
        "note": #{ "type": "string" },
        "approvals_empty": #{ "type": "boolean" },
    },
};

phase("Pack");
let p = "Read /Users/c/dev/hardallow-bot/playbooks/audit.md and /Users/c/dev/ha-live/fixes/lx-puma/daniel-review/APPROVALS.md and README.md. If APPROVALS has no Aprobar rows, approvals_empty=true (kit NOT applied). No loot. Return ok, note, approvals_empty.";
let r = agent(p, #{ label: "audit-pack", capability_mode: "read-only", output_schema: schema });
if (r == () || !r.success) { complete(#{ summary: "pack read failed", ok: false }); }

phase("Hold");
let p2 = "Read HOLD.md under /Users/c/dev/dani/out/authz/ and /Users/c/dev/dani/out/ops/ if present. Spanish note: what is HOLD. Never invent CLOSED. Return ok+note.";
let h = agent(p2, #{ label: "audit-hold", capability_mode: "read-only", output_schema: schema });
let note = "";
if (h != () && h.success && h.output.note != ()) { note = h.output.note; }
complete(#{ summary: "audit daniel", ok: true, note: note });

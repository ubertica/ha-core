let meta = #{
    name: "tg-funds-rails",
    description: "Cash/rails HOLD. Unsigned webhooks from VERIFY only. No live money.",
    when_to_use: "/funds rails-hold webhook-disk",
    phases: [ #{ title: "Hold" } ],
};

let schema = #{
    "type": "object",
    "required": ["ok", "note"],
    "properties": #{
        "ok": #{ "type": "boolean" },
        "note": #{ "type": "string" },
    },
};

phase("Hold");
let p = "Read /Users/c/dev/hardallow-bot/playbooks/funds.md. From latest VERIFY.json list titles matching webhook, mercadopago, cashin, prize. HOLD live PSP. No CBU. Return ok+note.";
let r = agent(p, #{ label: "funds-hold", capability_mode: "read-only", output_schema: schema });
if (r == () || !r.success) { complete(#{ summary: "funds failed", ok: false }); }
complete(#{ summary: "funds rails", ok: true, note: r.output.note });

let meta = #{
    name: "tg-vault-hygiene",
    description: "Secret path existence only. Never echo values.",
    when_to_use: "/vault secret-paths drive-status",
    phases: [ #{ title: "Paths" } ],
};

let schema = #{
    "type": "object",
    "required": ["ok", "note"],
    "properties": #{
        "ok": #{ "type": "boolean" },
        "note": #{ "type": "string" },
    },
};

phase("Paths");
let p = "Read /Users/c/dev/hardallow-bot/playbooks/vault.md. Check existence (not content) of hardallow-bot/.env , ~/.grok/hard-allow/secrets/atlassian-org.env , ha-live/secrets/danielcliente/ACCESS.md using list_dir/read only filenames. NEVER print secret values. Return ok+note with YES/NO paths.";
let r = agent(p, #{ label: "vault-paths", capability_mode: "read-only", output_schema: schema });
if (r == () || !r.success) { complete(#{ summary: "vault failed", ok: false }); }
complete(#{ summary: "vault hygiene", ok: true, note: r.output.note });

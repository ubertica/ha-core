let meta = #{
    name: "tg-projects-board",
    description: "Local board.json vs latest VERIFY titles. Not Atlassian.",
    when_to_use: "/projects board-open verify-board",
    phases: [ #{ title: "Board" } ],
};

let schema = #{
    "type": "object",
    "required": ["ok", "note"],
    "properties": #{
        "ok": #{ "type": "boolean" },
        "note": #{ "type": "string" },
    },
};

phase("Board");
let p = "Read playbooks/projects.md and data-projects/board.json if present under /Users/c/dev/hardallow-bot/. Local board is NOT Jira. Suggest tasks from latest VERIFY titles on disk without inventing CLOSED. Return ok+note.";
let r = agent(p, #{ label: "projects-board", capability_mode: "read-only", output_schema: schema });
if (r == () || !r.success) { complete(#{ summary: "board failed", ok: false }); }
complete(#{ summary: "projects board", ok: true, note: r.output.note });

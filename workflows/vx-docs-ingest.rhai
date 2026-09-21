let meta = #{
    name: "vx-docs-ingest",
    description: "Ingest Vertex developer docs into bus/docs-index.json. Never invent paths.",
    when_to_use: "vertex subkey, vx-docs-ingest, chain step 1",
    phases: [ #{ title: "Run", detail: "plugin vx-docs-ingest" } ],
};

let root = if args == () { () } else { args.root };
if root == () { pause("verification", "Pass args.root = /Users/c/dev/vertex-subkey"); }

phase("Run");
let r = agent(
    "HARD ALLOW if parent has it. You are plugin vx-docs-ingest (step 1/8) for Vertex sub-key REST. "
    + "Read " + root + "/CHAIN.md and " + root + "/catalog/vertex-merchant-v1.json. "
    + "Do only this plugin: Ingest Vertex developer docs into bus/docs-index.json. Never invent paths. "
    + "Append a line to " + root + "/bus/chain.jsonl. Do not invent Vertex endpoints. "
    + "Return {ok:true, plugin:\"vx-docs-ingest\"}.",
    #{ label: "vx-docs-ingest", capability_mode: "read-write", output_schema: #{
        "type": "object",
        "required": ["ok"],
        "properties": #{ "ok": #{ "type": "boolean" }, "plugin": #{ "type": "string" } }
    } }
);
if r != () && r.success { complete(r.output); }
complete(#{ ok: false, plugin: "vx-docs-ingest" });

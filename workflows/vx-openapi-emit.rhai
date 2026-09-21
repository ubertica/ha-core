let meta = #{
    name: "vx-openapi-emit",
    description: "Emit catalog/openapi.json from catalog SoT. No hand-edits.",
    when_to_use: "vertex subkey, vx-openapi-emit, chain step 6",
    phases: [ #{ title: "Run", detail: "plugin vx-openapi-emit" } ],
};

let root = if args == () { () } else { args.root };
if root == () { pause("verification", "Pass args.root = /Users/c/dev/vertex-subkey"); }

phase("Run");
let r = agent(
    "HARD ALLOW if parent has it. You are plugin vx-openapi-emit (step 6/8) for Vertex sub-key REST. "
    + "Read " + root + "/CHAIN.md and " + root + "/catalog/vertex-merchant-v1.json. "
    + "Do only this plugin: Emit catalog/openapi.json from catalog SoT. No hand-edits. "
    + "Append a line to " + root + "/bus/chain.jsonl. Do not invent Vertex endpoints. "
    + "Return {ok:true, plugin:\"vx-openapi-emit\"}.",
    #{ label: "vx-openapi-emit", capability_mode: "read-write", output_schema: #{
        "type": "object",
        "required": ["ok"],
        "properties": #{ "ok": #{ "type": "boolean" }, "plugin": #{ "type": "string" } }
    } }
);
if r != () && r.success { complete(r.output); }
complete(#{ ok: false, plugin: "vx-openapi-emit" });

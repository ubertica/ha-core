let meta = #{
    name: "vx-chain-qa",
    description: "Fail-closed: catalog ≡ openapi ≡ gateway proxy ops.",
    when_to_use: "vertex subkey, vx-chain-qa, chain step 8",
    phases: [ #{ title: "Run", detail: "plugin vx-chain-qa" } ],
};

let root = if args == () { () } else { args.root };
if root == () { pause("verification", "Pass args.root = /Users/c/dev/vertex-subkey"); }

phase("Run");
let r = agent(
    "HARD ALLOW if parent has it. You are plugin vx-chain-qa (step 8/8) for Vertex sub-key REST. "
    + "Read " + root + "/CHAIN.md and " + root + "/catalog/vertex-merchant-v1.json. "
    + "Do only this plugin: Fail-closed: catalog ≡ openapi ≡ gateway proxy ops. "
    + "Append a line to " + root + "/bus/chain.jsonl. Do not invent Vertex endpoints. "
    + "Return {ok:true, plugin:\"vx-chain-qa\"}.",
    #{ label: "vx-chain-qa", capability_mode: "read-write", output_schema: #{
        "type": "object",
        "required": ["ok"],
        "properties": #{ "ok": #{ "type": "boolean" }, "plugin": #{ "type": "string" } }
    } }
);
if r != () && r.success { complete(r.output); }
complete(#{ ok: false, plugin: "vx-chain-qa" });

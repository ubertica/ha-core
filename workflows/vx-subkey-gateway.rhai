let meta = #{
    name: "vx-subkey-gateway",
    description: "Fastify REST: X-Sub-Key → Vertex master. Scopes from catalog.",
    when_to_use: "vertex subkey, vx-subkey-gateway, chain step 7",
    phases: [ #{ title: "Run", detail: "plugin vx-subkey-gateway" } ],
};

let root = if args == () { () } else { args.root };
if root == () { pause("verification", "Pass args.root = /Users/c/dev/vertex-subkey"); }

phase("Run");
let r = agent(
    "HARD ALLOW if parent has it. You are plugin vx-subkey-gateway (step 7/8) for Vertex sub-key REST. "
    + "Read " + root + "/CHAIN.md and " + root + "/catalog/vertex-merchant-v1.json. "
    + "Do only this plugin: Fastify REST: X-Sub-Key → Vertex master. Scopes from catalog. "
    + "Append a line to " + root + "/bus/chain.jsonl. Do not invent Vertex endpoints. "
    + "Return {ok:true, plugin:\"vx-subkey-gateway\"}.",
    #{ label: "vx-subkey-gateway", capability_mode: "read-write", output_schema: #{
        "type": "object",
        "required": ["ok"],
        "properties": #{ "ok": #{ "type": "boolean" }, "plugin": #{ "type": "string" } }
    } }
);
if r != () && r.success { complete(r.output); }
complete(#{ ok: false, plugin: "vx-subkey-gateway" });

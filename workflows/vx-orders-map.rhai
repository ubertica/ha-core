let meta = #{
    name: "vx-orders-map",
    description: "Map order lifecycle into catalog ops group orders.",
    when_to_use: "vertex subkey, vx-orders-map, chain step 3",
    phases: [ #{ title: "Run", detail: "plugin vx-orders-map" } ],
};

let root = if args == () { () } else { args.root };
if root == () { pause("verification", "Pass args.root = /Users/c/dev/vertex-subkey"); }

phase("Run");
let r = agent(
    "HARD ALLOW if parent has it. You are plugin vx-orders-map (step 3/8) for Vertex sub-key REST. "
    + "Read " + root + "/CHAIN.md and " + root + "/catalog/vertex-merchant-v1.json. "
    + "Do only this plugin: Map order lifecycle into catalog ops group orders. "
    + "Append a line to " + root + "/bus/chain.jsonl. Do not invent Vertex endpoints. "
    + "Return {ok:true, plugin:\"vx-orders-map\"}.",
    #{ label: "vx-orders-map", capability_mode: "read-write", output_schema: #{
        "type": "object",
        "required": ["ok"],
        "properties": #{ "ok": #{ "type": "boolean" }, "plugin": #{ "type": "string" } }
    } }
);
if r != () && r.success { complete(r.output); }
complete(#{ ok: false, plugin: "vx-orders-map" });

let meta = #{
    name: "vx-callbacks-map",
    description: "Vertex→merchant callback POST; our /v1/callbacks/vertex fan-out.",
    when_to_use: "vertex subkey, vx-callbacks-map, chain step 5",
    phases: [ #{ title: "Run", detail: "plugin vx-callbacks-map" } ],
};

let root = if args == () { () } else { args.root };
if root == () { pause("verification", "Pass args.root = /Users/c/dev/vertex-subkey"); }

phase("Run");
let r = agent(
    "HARD ALLOW if parent has it. You are plugin vx-callbacks-map (step 5/8) for Vertex sub-key REST. "
    + "Read " + root + "/CHAIN.md and " + root + "/catalog/vertex-merchant-v1.json. "
    + "Do only this plugin: Vertex→merchant callback POST; our /v1/callbacks/vertex fan-out. "
    + "Append a line to " + root + "/bus/chain.jsonl. Do not invent Vertex endpoints. "
    + "Return {ok:true, plugin:\"vx-callbacks-map\"}.",
    #{ label: "vx-callbacks-map", capability_mode: "read-write", output_schema: #{
        "type": "object",
        "required": ["ok"],
        "properties": #{ "ok": #{ "type": "boolean" }, "plugin": #{ "type": "string" } }
    } }
);
if r != () && r.success { complete(r.output); }
complete(#{ ok: false, plugin: "vx-callbacks-map" });

let meta = #{
    name: "vx-payouts-map",
    description: "Map payout methods + create + get into catalog.",
    when_to_use: "vertex subkey, vx-payouts-map, chain step 4",
    phases: [ #{ title: "Run", detail: "plugin vx-payouts-map" } ],
};

let root = if args == () { () } else { args.root };
if root == () { pause("verification", "Pass args.root = /Users/c/dev/vertex-subkey"); }

phase("Run");
let r = agent(
    "HARD ALLOW if parent has it. You are plugin vx-payouts-map (step 4/8) for Vertex sub-key REST. "
    + "Read " + root + "/CHAIN.md and " + root + "/catalog/vertex-merchant-v1.json. "
    + "Do only this plugin: Map payout methods + create + get into catalog. "
    + "Append a line to " + root + "/bus/chain.jsonl. Do not invent Vertex endpoints. "
    + "Return {ok:true, plugin:\"vx-payouts-map\"}.",
    #{ label: "vx-payouts-map", capability_mode: "read-write", output_schema: #{
        "type": "object",
        "required": ["ok"],
        "properties": #{ "ok": #{ "type": "boolean" }, "plugin": #{ "type": "string" } }
    } }
);
if r != () && r.success { complete(r.output); }
complete(#{ ok: false, plugin: "vx-payouts-map" });

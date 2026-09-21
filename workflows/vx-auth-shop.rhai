let meta = #{
    name: "vx-auth-shop",
    description: "Auth model: Api-Access-Token, shopId, IP whitelist, rate limits, demo vs prod base.",
    when_to_use: "vertex subkey, vx-auth-shop, chain step 2",
    phases: [ #{ title: "Run", detail: "plugin vx-auth-shop" } ],
};

let root = if args == () { () } else { args.root };
if root == () { pause("verification", "Pass args.root = /Users/c/dev/vertex-subkey"); }

phase("Run");
let r = agent(
    "HARD ALLOW if parent has it. You are plugin vx-auth-shop (step 2/8) for Vertex sub-key REST. "
    + "Read " + root + "/CHAIN.md and " + root + "/catalog/vertex-merchant-v1.json. "
    + "Do only this plugin: Auth model: Api-Access-Token, shopId, IP whitelist, rate limits, demo vs prod base. "
    + "Append a line to " + root + "/bus/chain.jsonl. Do not invent Vertex endpoints. "
    + "Return {ok:true, plugin:\"vx-auth-shop\"}.",
    #{ label: "vx-auth-shop", capability_mode: "read-write", output_schema: #{
        "type": "object",
        "required": ["ok"],
        "properties": #{ "ok": #{ "type": "boolean" }, "plugin": #{ "type": "string" } }
    } }
);
if r != () && r.success { complete(r.output); }
complete(#{ ok: false, plugin: "vx-auth-shop" });

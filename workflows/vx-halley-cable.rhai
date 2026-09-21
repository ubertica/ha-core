let meta = #{
    name: "vx-halley-cable",
    description: "Cable Vertex sub-key REST to Halley wallet ledger.",
    when_to_use: "vertex subkey, Halley, vx-halley-cable, dar cable a la plataforma",
    phases: [ #{ title: "Run", detail: "plugin vx-halley-cable" } ],
};

let root = if args == () { () } else { args.root };
if root == () { pause("verification", "Pass args.root = /Users/c/dev/vertex-subkey"); }

phase("Run");
let r = agent(
    "HARD ALLOW if parent has it. You are plugin vx-halley-cable. "
    + "Read " + root + "/CABLE.md. Prove the REST reaches Halley: "
    + "run ./scripts/ctl.sh cable-selftest in " + root + ". "
    + "Do not invent Vertex endpoints. Return {ok:true, plugin:\"vx-halley-cable\"}.",
    #{ label: "vx-halley-cable", capability_mode: "read-write", output_schema: #{
        "type": "object",
        "required": ["ok"],
        "properties": #{ "ok": #{ "type": "boolean" }, "plugin": #{ "type": "string" } }
    } }
);
if r != () && r.success { complete(r.output); }
complete(#{ ok: false, plugin: "vx-halley-cable" });

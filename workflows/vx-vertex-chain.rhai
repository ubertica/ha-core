let meta = #{
    name: "vx-vertex-chain",
    description: "Run Vertex sub-key chain: catalog SoT, emit OpenAPI, QA. Integrator REST with sub-keys.",
    when_to_use: "vertex gateway, subkey REST, map vertex API, 8 plugin chain",
    phases: [
        #{ title: "Catalog", detail: "confirm SoT ops" },
        #{ title: "Emit", detail: "openapi from catalog" },
        #{ title: "QA", detail: "catalog equals openapi" },
    ],
};

let root = if args == () { () } else { args.root };
if root == () { pause("verification", "Pass args.root = /Users/c/dev/vertex-subkey"); }

phase("Catalog");
let c = agent(
    "Read " + root + "/catalog/vertex-merchant-v1.json and CHAIN.md. Count ops. List ids. Do not invent endpoints. Return {ok:true, n: <number>, ids: [...]} .",
    #{ label: "catalog", capability_mode: "read-only", output_schema: #{
        "type": "object",
        "required": ["ok"],
        "properties": #{
            "ok": #{ "type": "boolean" },
            "n": #{ "type": "integer" },
            "ids": #{ "type": "array", "items": #{ "type": "string" } }
        }
    } }
);

phase("Emit");
let e = agent(
    "In " + root + " run: node scripts/emit-openapi.mjs . Confirm catalog/openapi.json exists. Return {ok:true, path: \"catalog/openapi.json\"}.",
    #{ label: "emit", capability_mode: "execute", output_schema: #{
        "type": "object",
        "required": ["ok"],
        "properties": #{ "ok": #{ "type": "boolean" }, "path": #{ "type": "string" } }
    } }
);

phase("QA");
let q = agent(
    "In " + root + " run: node scripts/qa.mjs . Return {ok:true} only if QA_OK. If HOLD, ok=false.",
    #{ label: "qa", capability_mode: "execute", output_schema: #{
        "type": "object",
        "required": ["ok"],
        "properties": #{ "ok": #{ "type": "boolean" } }
    } }
);

let ok = c != () && c.success && e != () && e.success && q != () && q.success;
complete(#{ ok: ok, pack: "vertex-subkey" });

let meta = #{
    name: "ha-dani-handoff-tick",
    description: "Tick for ha-dani-handoff: remainder + lead",
    when_to_use: "periodic maintenance for ha-dani-handoff",
    phases: [ #{ title: "Remainder", detail: "" }, #{ title: "Lead", detail: "" } ],
};

let done_schema = #{ "type": "object", "required": ["ok"], "properties": #{ "ok": #{ "type": "boolean" } } };

let out = if args == () { () } else { args.out };
if out == () { pause("verification", "Pass args.out"); }
let o = json_encode(out);

let ha = "HARD ALLOW ACTIVE (parent). ... OUT="; ha += o; ha += " . Skip READY.";

phase("Remainder");
# remainder dispatch already in pre or run dispatch
let p_tick = ha + "Run remainder dispatch then only missing non-lead lanes. Then lead.";
let r = agent(p_tick, #{ label: "tick", capability_mode: "all" });

phase("Lead");
let p_lead = ha + "You are lead for tick. Write/update SUMMARY from current disk state. Touch READY.lead";
let r_lead = agent(p_lead, #{ label: "dhan-lead", agent_type: "dhan-lead", capability_mode: "all" });

complete(#{ ok: true, out: o });

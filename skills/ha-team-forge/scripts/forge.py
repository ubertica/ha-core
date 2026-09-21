#!/usr/bin/env python3
"""
forge.py — reads lanes JSON + flags; renders templates; writes plugin+skills+workflows; syncs agents.
Real logic, no stubs. Supports --plugin-root etc for smoke.
"""
from __future__ import annotations
import argparse
import json
import os
import shutil
import stat
import sys
from pathlib import Path
from string import Template

HERE = Path(__file__).resolve().parent
TEMPLATES = HERE.parent / "templates"
EXAMPLES = HERE.parent / "examples"
SKILL_ROOT = HERE.parent

def load_lanes(path: str | None) -> list[dict]:
    if not path:
        path = str(EXAMPLES / "lanes-minimal.json")
    p = Path(path).expanduser().resolve()
    data = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("lanes", [])
    return data or []

def render(tmpl: str, ctx: dict) -> str:
    # {{VAR}} placeholders as per BUILD-SPEC
    safe = {k: ("" if v is None else str(v)) for k,v in ctx.items()}
    out = tmpl
    for k, v in safe.items():
        out = out.replace("{{" + k + "}}", v)
    return out

def make_exec(p: Path):
    if p.exists():
        mode = p.stat().st_mode
        p.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

def write_file(p: Path, content: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

def copy_ha_law(dest_agents: Path):
    gold_law = Path.home() / ".grok" / "plugins" / "ha-hackers" / "agents" / "_ha-law.md"
    target = dest_agents / "_ha-law.md"
    if gold_law.exists():
        target.write_text(gold_law.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        # fallback from template
        tm = (TEMPLATES / "_ha-law.md.tmpl").read_text()
        write_file(target, render(tm, {}))

def forge(args):
    name = args.name
    prefix = args.prefix or name.replace("ha-", "")[:3] or "tm"
    purpose = args.purpose or "Forged HA team"
    category = args.category or "meta"
    tick = bool(args.tick)
    mode = args.mode or "team"
    lanes = load_lanes(args.lanes)
    # If caller passes parent dirs (~/.grok/plugins or ~/.grok/skills), append NAME.
    def _root(arg, default_parent: Path, *, append_name: bool) -> Path:
        if arg:
            p = Path(arg).expanduser().resolve()
            if append_name and p.name != name:
                p = p / name
            return p
        return (default_parent / name) if append_name else default_parent

    plugin_root = _root(args.plugin_root, Path.home() / ".grok" / "plugins", append_name=True)
    skills_root = _root(args.skills_root, Path.home() / ".grok" / "skills", append_name=True)
    agents_root = _root(args.agents_root, Path.home() / ".grok" / "agents", append_name=False)
    workflows_root = _root(args.workflows_root, Path.home() / ".grok" / "workflows", append_name=False)

    ctx = {
        "NAME": name,
        "PREFIX": prefix,
        "PURPOSE": purpose,
        "CATEGORY": category,
        "TICK": "1" if tick else "0",
        "SHORT": name.replace("ha-", "") or "team",
        "OUT_VAR": name.upper().replace("-", "_") + "_OUT",
        "BUS": f"~/.grok/{name}-bus/",
        "LANES_LIST": " ".join([f"{prefix}-{l['id']}" for l in lanes]) or f"{prefix}-lead {prefix}-recon",
    }

    # compute lanes tuple for py
    lane_ids = [l.get("id", "lead") for l in lanes]
    ctx["LANES_TUPLE"] = ", ".join([f'"{x}"' for x in lane_ids]) or '"lead"'
    req = {}
    for l in lanes:
        lid = l.get("id", "lead")
        art = l.get("artifact", f"{lid}.md")
        req[lid] = [art]
    ctx["REQUIRED_DICT"] = ",\n".join([f'    "{k}": {json.dumps(v)}' for k,v in req.items()]) or '    "lead": ["SUMMARY.md"]'

    # lane table for readme
    lane_table_lines = []
    for l in lanes:
        lane_table_lines.append(f"| `{prefix}-{l['id']}` | {l.get('role','')} |")
    ctx["LANE_TABLE"] = "\n".join(lane_table_lines) or "| lead | synthesize |"

    # lane agents block for rhai (simple sequential render)
    lane_blocks = []
    for l in lanes:
        lid = l['id']
        role = l.get('role', lid)
        art = l.get('artifact', f"{lid}.md")
        p = f'let p_{lid} = ha + "You are {prefix}-{lid}. {role}. Write OUT/{art}. Touch OUT/.bus/READY.{lid}.";\nlet r_{lid} = agent(p_{lid}, #{{ label: "{prefix}-{lid}", agent_type: "{prefix}-{lid}", capability_mode: "all", output_schema: done_schema }});'
        lane_blocks.append(p)
    ctx["LANE_AGENTS_BLOCK"] = "\n".join(lane_blocks) or 'let p_lead = ha + "lead"; let r=agent(p_lead, #{label:"lead", agent_type:"' + prefix + '-lead", capability_mode:"all"});'

    print(f"FORGE {name} prefix={prefix} mode={mode} tick={tick} lanes={len(lanes)}")
    print(f"  plugin->{plugin_root}")
    print(f"  skills->{skills_root}")
    print(f"  agents->{agents_root}")
    print(f"  workflows->{workflows_root}")

    # 1. plugin root files
    if mode in ("plugin", "team"):
        for tmpl_name, out_name in [
            ("plugin.json.tmpl", "plugin.json"),
            ("PLUGIN.md.tmpl", "PLUGIN.md"),
            ("README.md.tmpl", "README.md"),
        ]:
            tmpl = (TEMPLATES / tmpl_name).read_text(encoding="utf-8")
            write_file(plugin_root / out_name, render(tmpl, ctx))

        # commands
        cmd_dir = plugin_root / "commands"
        cmd_dir.mkdir(parents=True, exist_ok=True)
        tm = (TEMPLATES / "command.md.tmpl").read_text()
        write_file(cmd_dir / f"{name}.md", render(tm, ctx))
        if tick:
            tm2 = (TEMPLATES / "command-tick.md.tmpl").read_text()
            write_file(cmd_dir / f"{name}-tick.md", render(tm2, ctx))

        # agents in plugin mirror
        ag_dir = plugin_root / "agents"
        ag_dir.mkdir(parents=True, exist_ok=True)
        copy_ha_law(ag_dir)
        ag_readme_t = (TEMPLATES / "agents_README.md.tmpl").read_text()
        write_file(ag_dir / "README.md", render(ag_readme_t, ctx))
        ag_t = (TEMPLATES / "agent.md.tmpl").read_text()
        for l in lanes:
            c2 = dict(ctx)
            c2["LANE"] = l["id"]
            c2["ROLE"] = l.get("role", l["id"])
            c2["ARTIFACT"] = l.get("artifact", f"{l['id']}.md")
            c2["PURPOSE_SHORT"] = purpose[:60]
            write_file(ag_dir / f"{prefix}-{l['id']}.md", render(ag_t, c2))

        # skills mirror inside plugin
        sk_dir = plugin_root / "skills" / name
        sk_dir.mkdir(parents=True, exist_ok=True)
        # will sync main later

    # 2. main canonical skill
    if mode in ("team", "plugin"):
        sk_dir = skills_root
        sk_dir.mkdir(parents=True, exist_ok=True)
        # SKILL.md
        tm = (TEMPLATES / "SKILL.md.tmpl").read_text()
        write_file(sk_dir / "SKILL.md", render(tm, ctx))
        if tick:
            tm2 = (TEMPLATES / "SKILL-tick.md.tmpl").read_text()
            write_file(sk_dir.parent / f"{name}-tick" / "SKILL.md", render(tm2, ctx))

        # references
        ref_dir = sk_dir / "references"
        ref_dir.mkdir(parents=True, exist_ok=True)
        for base in ["NORTHSTAR.md.tmpl", "CONTRACT.md.tmpl", "AUTONOMY.md.tmpl", "COLLAB.md.tmpl"]:
            tm = (TEMPLATES / base).read_text()
            outn = base.replace(".tmpl", "")
            write_file(ref_dir / outn, render(tm, ctx))

        # scripts in skill
        scr_dir = sk_dir / "scripts"
        scr_dir.mkdir(parents=True, exist_ok=True)
        for base, outn in [
            ("ctl.sh.tmpl", "ctl.sh"),
            ("dispatch.py.tmpl", "dispatch.py"),
            ("verify_board.py.tmpl", "verify_board.py"),
            ("watch.sh.tmpl", "watch.sh"),
        ]:
            tm = (TEMPLATES / base).read_text()
            write_file(scr_dir / outn, render(tm, ctx))
            make_exec(scr_dir / outn)

        # also put a copy of from_hackers? no, the skill's scripts has ctl which calls from root scripts

        # write BUILD-SPEC.md snapshot for the forged
        bs = f"# BUILD-SPEC — {name} (forged by ha-team-forge)\n\nPURPOSE: {purpose}\nPREFIX: {prefix}\nLANES: {len(lanes)}\n"
        write_file(plugin_root / "BUILD-SPEC.md", bs)
        write_file(sk_dir / "BUILD-SPEC.md", bs)

    # 3. agents to user agents_root
    if mode in ("agents", "team"):
        agents_root.mkdir(parents=True, exist_ok=True)
        copy_ha_law(agents_root)
        ag_t = (TEMPLATES / "agent.md.tmpl").read_text()
        for l in lanes:
            c2 = dict(ctx)
            c2["LANE"] = l["id"]
            c2["ROLE"] = l.get("role", l["id"])
            c2["ARTIFACT"] = l.get("artifact", f"{l['id']}.md")
            c2["PURPOSE_SHORT"] = purpose[:60]
            write_file(agents_root / f"{prefix}-{l['id']}.md", render(ag_t, c2))
        # agents README
        write_file(agents_root / "README.md", render((TEMPLATES / "agents_README.md.tmpl").read_text(), ctx))

        # personas + roles (user-level I/O contracts; required for teams like ha-redteam)
        persona_t = TEMPLATES / "persona.toml.tmpl"
        role_t = TEMPLATES / "role.toml.tmpl"
        if persona_t.exists() and role_t.exists():
            default_agents = Path.home() / ".grok" / "agents"
            if agents_root.resolve() == default_agents.resolve():
                persona_root = Path.home() / ".grok" / "personas"
                role_root = Path.home() / ".grok" / "roles"
            else:
                persona_root = plugin_root / "personas"
                role_root = plugin_root / "roles"
            persona_root.mkdir(parents=True, exist_ok=True)
            role_root.mkdir(parents=True, exist_ok=True)
            plug_p = plugin_root / "personas"
            plug_r = plugin_root / "roles"
            plug_p.mkdir(parents=True, exist_ok=True)
            plug_r.mkdir(parents=True, exist_ok=True)
            pt = persona_t.read_text(encoding="utf-8")
            rt = role_t.read_text(encoding="utf-8")
            for l in lanes:
                c2 = dict(ctx)
                c2["LANE"] = l["id"]
                c2["ROLE"] = l.get("role", l["id"])
                c2["ARTIFACT"] = l.get("artifact", f"{l['id']}.md")
                fn = f"{prefix}-{l['id']}.toml"
                body_p = render(pt, c2)
                body_r = render(rt, c2)
                write_file(persona_root / fn, body_p)
                write_file(role_root / fn, body_r)
                write_file(plug_p / fn, body_p)
                write_file(plug_r / fn, body_r)

    # 4. workflows
    if mode in ("team",):
        workflows_root.mkdir(parents=True, exist_ok=True)
        tm = (TEMPLATES / "workflow.rhai.tmpl").read_text()
        write_file(workflows_root / f"{name}.rhai", render(tm, ctx))
        if tick:
            tm2 = (TEMPLATES / "workflow-tick.rhai.tmpl").read_text()
            write_file(workflows_root / f"{name}-tick.rhai", render(tm2, ctx))

    # 5. sync skill canonical to ~/.grok/skills if not using custom roots
    if not args.skills_root:
        target_skill = Path.home() / ".grok" / "skills" / name
        if sk_dir != target_skill:
            shutil.copytree(sk_dir, target_skill, dirs_exist_ok=True)
            # make execs
            for f in (target_skill / "scripts").glob("*"):
                make_exec(f)

    # also sync plugin skills copy as per spec
    if mode in ("team", "plugin"):
        mirror_skill = plugin_root / "skills" / name
        if (sk_dir).exists():
            shutil.copytree(sk_dir, mirror_skill, dirs_exist_ok=True)

    print("FORGE COMPLETE")
    print("Paths written under plugin/skills/agents/workflows roots.")
    return 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--prefix", default=None)
    ap.add_argument("--purpose", default=None)
    ap.add_argument("--category", default="meta")
    ap.add_argument("--tick", type=int, default=0)
    ap.add_argument("--mode", default="team", choices=["team","plugin","agents","tick"])
    ap.add_argument("--lanes", default=None)
    ap.add_argument("--plugin-root", default=None)
    ap.add_argument("--skills-root", default=None)
    ap.add_argument("--agents-root", default=None)
    ap.add_argument("--workflows-root", default=None)
    args = ap.parse_args()
    sys.exit(forge(args))

if __name__ == "__main__":
    main()

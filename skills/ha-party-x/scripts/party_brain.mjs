#!/usr/bin/env node
/** Call party seats with a playbook injected. Writes OUT/.bus/party/<wave>.json */
import { existsSync, mkdirSync, readFileSync, writeFileSync, appendFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadSeats, askSeats, parseSeatList } from '/Users/c/.grok/hard-allow/party/lib.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..');
const PLAYBOOKS = join(ROOT, 'playbooks');

function arg(name, def = null) {
  const i = process.argv.indexOf(`--${name}`);
  if (i >= 0) return process.argv[i + 1];
  const eq = process.argv.find((a) => a.startsWith(`--${name}=`));
  if (eq) return eq.slice(name.length + 3);
  return def;
}
function flag(name) {
  return process.argv.includes(`--${name}`);
}

function loadPlaybook(name) {
  if (!name) return '';
  const id = String(name).replace(/[^a-z0-9-]/gi, '');
  const p = join(PLAYBOOKS, `${id}.md`);
  if (!existsSync(p)) throw new Error(`playbook missing: ${p}`);
  return readFileSync(p, 'utf8');
}

function loadOnlineIds(seats) {
  return seats.filter((s) => s.online).map((s) => s.id);
}

function applyFallback(ids, seats, fallbackG3) {
  const online = new Set(loadOnlineIds(seats));
  const out = [];
  for (const id of ids) {
    if (online.has(id)) out.push(id);
    else if (id === 'g3' && fallbackG3 && online.has('g4') && !out.includes('g4')) out.push('g4');
  }
  return [...new Set(out)];
}

async function main() {
  if (flag('help') || process.argv.includes('-h')) {
    console.log('party_brain.mjs --text T [--seats g2,g4] [--mode parallel|round] [--playbook g2-surface] [--out DIR] [--wave ID] [--target URL] [--max-tokens 8000] [--dry-run]');
    process.exit(0);
  }
  const text = arg('text', '');
  const seatsWanted = arg('seats', 'all');
  const mode = arg('mode', 'parallel');
  const playbook = arg('playbook', '');
  const out = arg('out', '');
  const wave = arg('wave', 'ad-hoc');
  const target = arg('target', '');
  const maxTokens = Number(arg('max-tokens', playbook ? '8000' : '1600'));
  const dry = flag('dry-run');

  const extraSystem = loadPlaybook(playbook);
  const seats = loadSeats();
  const ids = applyFallback(parseSeatList(seatsWanted, loadOnlineIds(seats)), seats, true);

  if (dry) {
    console.log(JSON.stringify({ ok: true, dry: true, ids, mode, playbook, maxTokens, extra_bytes: extraSystem.length }, null, 2));
    return;
  }
  if (!text) {
    console.error('need --text');
    process.exit(2);
  }
  if (!ids.length) {
    console.error('no online seats');
    process.exit(3);
  }

  const userText = [
    target ? `TARGET=${target}` : '',
    out ? `OUT=${out}` : '',
    wave ? `WAVE=${wave}` : '',
    text,
  ]
    .filter(Boolean)
    .join('\n');

  const rows = await askSeats({
    seats,
    history: [],
    userText,
    ids,
    sequential: mode === 'round',
    extraSystem,
    maxTokens,
  });

  const payload = {
    ts: new Date().toISOString(),
    wave,
    target,
    playbook,
    mode,
    ids,
    rows: rows.map((r) => ({ id: r.id, billing: r.billing, err: r.err, text: r.text })),
  };

  if (out) {
    const dir = join(out, '.bus', 'party');
    mkdirSync(dir, { recursive: true });
    const dest = join(dir, `${wave}.json`);
    writeFileSync(dest, JSON.stringify(payload, null, 2));
    const notes = join(out, '.bus', 'notes.jsonl');
    mkdirSync(join(out, '.bus'), { recursive: true });
    appendFileSync(
      notes,
      JSON.stringify({ from: 'party_brain', to: 'bus', type: 'wave', wave, path: dest, msg: ids.join(',') }) + '\n',
    );
    payload.path = dest;
  }
  console.log(JSON.stringify({ ok: true, path: payload.path || null, ids, errors: rows.filter((r) => r.err).map((r) => r.id) }, null, 2));
}

main().catch((e) => {
  console.error(String(e.message || e));
  process.exit(1);
});

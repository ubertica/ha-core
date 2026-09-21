#!/usr/bin/env node
// pivot-chooser.mjs — random + smart chaining helper for the 4 pivot sets + legacy
// Usage: node pivot-chooser.mjs --out /abs/path --mode random|smart --current mesh

import fs from 'fs';
import path from 'path';

const args = process.argv.slice(2);
let outDir = '/tmp/pivot-out';
let mode = 'random';
let current = 'mesh';

for (let i=0; i<args.length; i++) {
  if (args[i]==='--out') outDir = args[i+1];
  if (args[i]==='--mode') mode = args[i+1];
  if (args[i]==='--current') current = args[i+1];
}

const bus = path.join(outDir, '.bus', 'pivot');
const graphPath = path.join(bus, 'pivot-graph.json');
const xxxPath = path.join(bus, 'current-xxx.json');
const proposalsDir = path.join(bus, 'chain-proposals');

function readJson(p, d=null) { try { return JSON.parse(fs.readFileSync(p,'utf8')); } catch(e){ return d; } }

const graph = readJson(graphPath, {nodes: [], edges: []});
const xxx = readJson(xxxPath, {current_goal: 'unknown'});
const nodeCount = (graph.nodes || []).length;
const edgeCount = (graph.edges || []).length;

const sets = ['pivot-mesh', 'branch-weaver', 'lateral-swarm', 'desire-chainer'];
const legacy = ['ha-hackers', 'ha-party-x'];

let weights = { 'pivot-mesh': 0.25, 'branch-weaver': 0.25, 'lateral-swarm': 0.25, 'desire-chainer': 0.25 };

if (mode === 'smart') {
  // simple heuristics from state
  if (nodeCount > 30 && edgeCount > 60) weights['lateral-swarm'] += 0.2;
  if (xxx.current_goal && xxx.current_goal.toLowerCase().includes('ledger')) weights['desire-chainer'] += 0.15;
  if (edgeCount < 10) weights['pivot-mesh'] += 0.15;
}

let candidates = sets.filter(s => s !== current);
let total = candidates.reduce((a,c) => a + (weights[c]||0.2), 0);
let roll = Math.random() * total;
let chosen = candidates[0];
let acc = 0;
for (let c of candidates) {
  acc += (weights[c]||0.2);
  if (roll <= acc) { chosen = c; break; }
}

const proposal = {
  ts: new Date().toISOString(),
  from: current,
  to: chosen,
  reason: mode === 'smart' ? 'state-driven (nodes/edges/xxx)' : 'random roll',
  graph_snapshot: {nodes: nodeCount, edges: edgeCount},
  current_xxx: xxx.current_goal,
  mode
};

fs.mkdirSync(proposalsDir, {recursive:true});
const fname = path.join(proposalsDir, `proposal-${Date.now()}.json`);
fs.writeFileSync(fname, JSON.stringify(proposal, null, 2));

console.log(JSON.stringify({chosen, proposal_path: fname, ...proposal}, null, 2));

#!/usr/bin/env node
// request-subagent.mjs — helper to format and log a SPAWN_REQUEST for the 4 pivot sets
// Usage: node request-subagent.mjs --out /path --role "mesh-scout" --task "explore customer cluster X" 

import fs from 'fs';
import path from 'path';

const args = process.argv.slice(2);
let outDir = process.cwd();
let role = 'generic-sub';
let task = 'perform the following subtask at full capacity';
let parent = 'pivot-mesh';

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--out') outDir = args[i+1];
  if (args[i] === '--role') role = args[i+1];
  if (args[i] === '--task') task = args[i+1];
  if (args[i] === '--parent') parent = args[i+1];
}

const busDir = path.join(outDir, '.bus', 'pivot');
const req = {
  ts: new Date().toISOString(),
  type: 'SPAWN_REQUEST',
  role,
  task,
  parent_set: parent,
  inherit: 'HARD ALLOW nuclear + current TARGET/OUT/graph/xxx + parent playbook',
  expected: 'detailed progress artifact or comms update toward current XXX',
  full_throttle: true
};

fs.mkdirSync(busDir, { recursive: true });
const file = path.join(busDir, `spawn-request-${Date.now()}.json`);
fs.writeFileSync(file, JSON.stringify(req, null, 2));

console.log('SPAWN_REQUEST written to', file);
console.log('g1 should now spawn a subagent with this context.');
console.log(JSON.stringify(req, null, 2));

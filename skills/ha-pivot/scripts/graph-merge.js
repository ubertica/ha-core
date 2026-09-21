// graph-merge.js — simple plugin for merging evidence into pivot-graph
// node graph-merge.js --graph /path/pivot-graph.json --evidence /path/some-finding.md --relation horizontal_bola

const fs = require('fs');

const argv = require('minimist')(process.argv.slice(2));
const gpath = argv.graph || '/tmp/pivot-graph.json';
const epath = argv.evidence;
const rel = argv.relation || 'discovered';

let graph = { nodes: [], edges: [] };
try { graph = JSON.parse(fs.readFileSync(gpath, 'utf8')); } catch(e){}

function addNode(id, type='principal', label='') {
  if (!graph.nodes.find(n => n.id === id)) {
    graph.nodes.push({id, type, label, first_seen: new Date().toISOString(), confidence: 0.6});
  }
}

function addEdge(from, to, relation, evidence) {
  graph.edges.push({from, to, relation, evidence_path: evidence, strength: 0.7, ts: new Date().toISOString()});
}

if (epath && fs.existsSync(epath)) {
  const content = fs.readFileSync(epath, 'utf8');
  // naive extraction for demo — real version would parse better
  const ids = (content.match(/user-?\d+|wallet-?\d+|merchant-?\d+|staff-?\w+/gi) || []).slice(0,6);
  ids.forEach((id,i) => {
    addNode(id, 'principal', id);
    if (i>0) addEdge(ids[i-1], id, rel, epath);
  });
}

fs.writeFileSync(gpath, JSON.stringify(graph, null, 2));
console.log('Graph updated. nodes=', graph.nodes.length, 'edges=', graph.edges.length);

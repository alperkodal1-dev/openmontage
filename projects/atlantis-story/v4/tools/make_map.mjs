// Mediterranean map for the Atlantis Short (Natural Earth land, public domain).
// Run from a folder with d3-geo, topojson-client and world-atlas:  node make_map.mjs <out_dir>
import fs from 'fs';
import { createRequire } from 'module';
const require = createRequire(process.cwd() + '/');
const d3 = require('d3-geo'); const topo = require('topojson-client');
const L = require('world-atlas/land-50m.json'); const land = topo.feature(L, L.objects.land);
const W = 1000, H = 760, out = process.argv[2];
const proj = d3.geoMercator().fitExtent([[0, 0], [W, H]], { type: 'MultiPoint', coordinates: [[-27, 26], [38, 26], [38, 47.5], [-27, 47.5]] });
const path = d3.geoPath(proj); const r = n => Math.round(n * 10) / 10;
const P = ll => proj(ll).map(r);
const pts = { atl: P([-19, 33.5]), gib: P([-5.6, 36.0]), rome: P([12.5, 41.9]), athens: P([23.7, 38.0]), egypt: P([31.2, 30.1]) };
const svg = `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg">
<rect width="${W}" height="${H}" fill="#123038"/>
<path d="${path(d3.geoGraticule().step([10, 10])())}" fill="none" stroke="#d9b26a" stroke-opacity=".15" stroke-width="1"/>
<path d="${path(land)}" fill="#d9c9a3" stroke="#6b5636" stroke-width="2"/>
</svg>`;
fs.writeFileSync(out + '/med.svg.html', svg);
fs.writeFileSync(out + '/mappts.json', JSON.stringify(pts));
console.log(JSON.stringify(pts));

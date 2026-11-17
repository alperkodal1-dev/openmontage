// Alexander's campaign map (Natural Earth land, public domain). node make_map.mjs <out_dir>
import fs from 'fs';
import { createRequire } from 'module';
const require = createRequire(process.cwd() + '/');
const d3 = require('d3-geo'); const topo = require('topojson-client');
const L = require('world-atlas/land-50m.json'); const land = topo.feature(L, L.objects.land);
const W = 1000, H = 760, out = process.argv[2];
const proj = d3.geoMercator().fitExtent([[0, 0], [W, H]], { type: 'MultiPoint', coordinates: [[16, 22], [80, 22], [80, 46], [16, 46]] });
const path = d3.geoPath(proj); const r = n => Math.round(n * 10) / 10; const P = ll => proj(ll).map(r);
const route = [[22.52, 40.76], [27.3, 40.3], [31.9, 39.65], [36.2, 36.8], [35.2, 33.27], [29.9, 31.2], [35.5, 33.5], [43.4, 36.5], [44.42, 32.54], [52.89, 29.93], [59.6, 36.3], [66.9, 36.76], [69.2, 34.5], [73.5, 32.9]];
const pts = { pella: P([22.52, 40.76]), issus: P([36.2, 36.8]), egypt: P([29.9, 31.2]), gaug: P([43.4, 36.5]), babylon: P([44.42, 32.54]), hydaspes: P([73.5, 32.9]) };
const routeD = 'M' + route.map(P).map(p => p.join(' ')).join(' L');
fs.writeFileSync(out + '/map.svg.html', `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg"><rect width="${W}" height="${H}" fill="#123038"/><path d="${path(d3.geoGraticule().step([10, 10])())}" fill="none" stroke="#d9b26a" stroke-opacity=".15"/><path d="${path(land)}" fill="#d9c9a3" stroke="#6b5636" stroke-width="2"/></svg>`);
fs.writeFileSync(out + '/mappts.json', JSON.stringify({ ...pts, route: routeD }));
console.log(JSON.stringify(pts));

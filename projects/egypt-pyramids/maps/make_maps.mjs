// Egypt map SVG from Natural Earth (public domain): land from world-atlas, the Nile from ne_10m_rivers_lake_centerlines
// (exported to nile.json). Run from a folder with d3-geo, topojson-client and world-atlas:  node make_maps.mjs <out_dir>
import fs from 'fs';
import { createRequire } from 'module';
const require = createRequire(process.cwd() + '/');
const d3 = require('d3-geo'); const topo = require('topojson-client');
const out = process.argv[2];
const w50 = require('world-atlas/land-50m.json');
const land = topo.feature(w50, w50.objects.land);
const nile = JSON.parse(fs.readFileSync('nile.json'));
const r = (n) => Math.round(n * 10) / 10;
const W = 960, H = 1100;
const proj = d3.geoMercator().fitExtent([[0, 0], [W, H]], { type: 'MultiPoint', coordinates: [[28.6, 25.4], [35.0, 25.4], [35.0, 31.7], [28.6, 31.7]] }).clipExtent([[0, 0], [W, H]]);
const path = d3.geoPath(proj);
const svg = `<svg id="egsvg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg">
<rect width="${W}" height="${H}" fill="#7f9c9a"/>
<path d="${path(land)}" fill="#d9c9a3" stroke="#6b5636" stroke-width="1.5"/>
<path id="nile" d="${path(nile)}" fill="none" stroke="#3f7f8c" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
</svg>`;
fs.writeFileSync(out + '/egypt.svg.html', svg);
const P = { giza: [31.134, 29.979], saqqara: [31.216, 29.871], tura: [31.30, 29.93], abydos: [31.919, 26.185], dendera: [32.670, 26.142], jarf: [32.56, 28.95] };
const pts = Object.fromEntries(Object.entries(P).map(([k, v]) => [k, proj(v).map(r)]));
fs.writeFileSync(out + '/mappts.json', JSON.stringify(pts));
console.log(pts);

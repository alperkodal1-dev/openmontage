// Map SVGs from Natural Earth (world-atlas, public domain). Run from a folder with d3-geo, topojson-client and
// world-atlas installed:  node make_maps.mjs <out_dir>
import fs from 'fs';
import { createRequire } from 'module';
const require = createRequire(process.cwd() + '/');
const d3 = require('d3-geo'); const topo = require('topojson-client');
const out = process.argv[2];
const w50 = require('world-atlas/land-50m.json');
const land = topo.feature(w50, w50.objects.land);
const r = (n) => Math.round(n * 10) / 10;
const pts = {};
const polys = land.features.flatMap(f => f.geometry.type === 'MultiPolygon' ? f.geometry.coordinates : [f.geometry.coordinates]);
const pick = (fn) => ({ type: 'MultiPolygon', coordinates: polys.filter(p => fn(d3.geoCentroid({ type: 'Polygon', coordinates: p }))) });

// 1) Globe over the South Atlantic: South America, Africa, Antarctica. 900x900
{
  const S = 900;
  const proj = d3.geoOrthographic().rotate([35, 38]).scale(430).translate([S / 2, S / 2]).clipAngle(90);
  const path = d3.geoPath(proj);
  const ant = pick(c => c[1] < -60), rest = pick(c => c[1] >= -60);
  const sam = pick(c => c[1] >= -60 && c[1] < 13 && c[0] > -85 && c[0] < -33);
  const svg = `<svg id="globesvg" viewBox="0 0 ${S} ${S}" width="${S}" height="${S}" xmlns="http://www.w3.org/2000/svg">
<circle cx="${S / 2}" cy="${S / 2}" r="430" fill="#9fb3ad" stroke="#6b5636" stroke-width="3"/>
<path d="${path(d3.geoGraticule10())}" fill="none" stroke="rgba(60,50,30,.18)" stroke-width="1"/>
<path d="${path(rest)}" fill="#d9c9a3" stroke="#6b5636" stroke-width="1.5"/>
<path id="gsam" d="${path(sam)}" fill="#d9c9a3" stroke="#6b5636" stroke-width="1.5"/>
<path id="gant" d="${path(ant)}" fill="#f4f7f8" stroke="#8aa1a8" stroke-width="2"/>
</svg>`;
  fs.writeFileSync(out + '/globe.svg.html', svg);
  Object.assign(pts, { g_ant: proj([-45, -76]).map(r), g_sam: proj([-62, -42]).map(r), g_cape: proj([-67.3, -55.9]).map(r), g_africa: proj([18, -20]).map(r) });
}

// 2) Eastern Mediterranean: Gallipoli and Istanbul. 960x600
{
  const W = 960, H = 600;
  const proj = d3.geoMercator().fitExtent([[0, 0], [W, H]], { type: 'MultiPoint', coordinates: [[12, 33], [36, 33], [36, 45], [12, 45]] }).clipExtent([[0, 0], [W, H]]);
  const path = d3.geoPath(proj);
  const svg = `<svg id="medsvg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg">
<rect width="${W}" height="${H}" fill="#9fb3ad"/>
<path d="${path(land)}" fill="#d9c9a3" stroke="#6b5636" stroke-width="1.5"/>
</svg>`;
  fs.writeFileSync(out + '/med.svg.html', svg);
  Object.assign(pts, { gelibolu: proj([26.67, 40.41]).map(r), istanbul: proj([28.98, 41.01]).map(r) });
}
fs.writeFileSync(out + '/mappts.json', JSON.stringify(pts));
console.log(pts);

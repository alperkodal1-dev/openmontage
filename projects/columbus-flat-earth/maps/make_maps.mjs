// Draws the two map SVGs from Natural Earth (world-atlas, public domain).
// Run from a folder with d3-geo, topojson-client and world-atlas installed:
//   node make_maps.mjs <out_dir>
import fs from 'fs';
import { createRequire } from 'module';
const require = createRequire(process.cwd() + '/');
const d3 = require('d3-geo'); const topo = require('topojson-client');
const out = process.argv[2];
const land50 = require('world-atlas/land-50m.json');
const land = topo.feature(land50, land50.objects.land);
const r = (n) => Math.round(n * 10) / 10;
const pts = {};

// 1) Egypt: Alexandria to Syene, 960x700
{
  const W = 960, H = 700;
  const proj = d3.geoMercator().fitExtent([[40, 30], [W - 40, H - 30]], { type: 'MultiPoint', coordinates: [[26.5, 22.6], [36.5, 22.6], [36.5, 32.6], [26.5, 32.6]] }).clipExtent([[0, 0], [W, H]]);
  const path = d3.geoPath(proj);
  const nile = [[32.9, 24.09], [32.93, 24.47], [32.87, 24.98], [32.55, 25.29], [32.64, 25.69], [32.72, 26.16], [32.24, 26.05], [31.69, 26.56], [31.18, 27.18], [30.75, 28.1], [31.1, 29.07], [31.23, 30.04], [30.9, 30.8], [30.42, 31.46]];
  const svg = `<svg id="egsvg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg">
<rect width="${W}" height="${H}" fill="#9fb3ad"/>
<path d="${path(land)}" fill="#d9c9a3" stroke="#6b5636" stroke-width="2"/>
<path id="nile" d="${path({ type: 'LineString', coordinates: nile })}" fill="none" stroke="#4f7f8c" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
</svg>`;
  fs.writeFileSync(out + '/egypt.svg.html', svg);
  pts.alex = proj([29.92, 31.2]).map(r); pts.syene = proj([32.9, 24.09]).map(r);
}

// 2) The westward ocean: Spain to Japan, 960x330, Pacific-centred
{
  const W = 960, H = 330;
  const proj = d3.geoEquirectangular().rotate([118, 0]).fitExtent([[10, 10], [W - 10, H - 10]],
    { type: 'MultiPoint', coordinates: [[125, -12], [125, 62], [-1, 62], [-1, -12], [-118, 62], [-118, -12]] }).clipExtent([[0, 0], [W, H]]);
  const path = d3.geoPath(proj);
  // split land polygons into the Americas and the rest of the world
  const polys = land.features.flatMap(f => f.geometry.type === 'MultiPolygon' ? f.geometry.coordinates : [f.geometry.coordinates]);
  const isAm = (p) => { const c = d3.geoCentroid({ type: 'Polygon', coordinates: p }); return c[0] < -25 && c[0] > -170 && c[1] > -60; };
  const am = { type: 'MultiPolygon', coordinates: polys.filter(isAm) };
  const rest = { type: 'MultiPolygon', coordinates: polys.filter(p => !isAm(p)) };
  const canary = [-15.5, 28.1], hisJapan = [-60.5, 28.1], japan = [139.7, 35.7];
  // westward routes as rhumb lines (constant latitude), drawn as screen-space polylines
  const line = (a, b, n = 60) => 'M' + Array.from({ length: n + 1 }, (_, i) => {
    const lon = a[0] + (b[0] - a[0]) * i / n, lat = a[1] + (b[1] - a[1]) * i / n; return proj([lon, lat]).map(r).join(',');
  }).join(' L');
  const realEnd = [japan[0] - 360, japan[1]];
  const svg = `<svg id="ocsvg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg">
<rect width="${W}" height="${H}" fill="#9fb3ad"/>
<path d="${path(rest)}" fill="#d9c9a3" stroke="#6b5636" stroke-width="1.5"/>
<path id="amer" d="${path(am)}" fill="#c9b07a" stroke="#6b5636" stroke-width="1.5"/>
<path id="rHis" d="${line(canary, hisJapan, 20)}" fill="none" stroke="#9c2f1f" stroke-width="7" stroke-dasharray="16 10" stroke-linecap="round"/>
<path id="rReal" d="${line(canary, realEnd, 80)}" fill="none" stroke="#132024" stroke-width="5" stroke-linecap="round"/>
</svg>`;
  fs.writeFileSync(out + '/ocean.svg.html', svg);
  Object.assign(pts, { canary: proj(canary).map(r), hisJapan: proj(hisJapan).map(r), japan: proj(japan).map(r), bahamas: proj([-74.5, 24.0]).map(r), spain: proj([-4, 40]).map(r) });
}
fs.writeFileSync(out + '/mappts.json', JSON.stringify(pts));
console.log(pts);

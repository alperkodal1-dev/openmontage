// Globe for the channel avatar: Natural Earth land (public domain) in an orthographic projection,
// with gold icons of famous moments of history at their real places. Run from a folder with d3-geo,
// topojson-client and world-atlas:  node make_globe.mjs <out.svg.html>
import fs from 'fs';
import { createRequire } from 'module';
const require = createRequire(process.cwd() + '/');
const d3 = require('d3-geo'); const topo = require('topojson-client');
const L = require('world-atlas/land-50m.json'); const land = topo.feature(L, L.objects.land);
const S = 1024, R = 372, C = S / 2;
const proj = d3.geoOrthographic().scale(R).translate([C, C + 8]).rotate([-28, -30]).clipAngle(90);
const path = d3.geoPath(proj);
const grat = d3.geoGraticule().step([20, 20])();
const P = ll => proj(ll).map(v => Math.round(v * 10) / 10);
const G = '#f1d49a', D = '#1a1408';
const icons = {
  pyramids: `<path d="M-46 22 L-14 -30 L18 22 Z" /><path d="M2 22 L26 -12 L50 22 Z" opacity=".92"/><path d="M-14 -30 L-6 22" stroke="${D}" stroke-width="2.5" fill="none" opacity=".45"/>`,
  colosseum: `<path d="M-44 20 V-12 Q0 -30 44 -12 V20 Z"/>` + [...Array(6)].map((_, i) => `<path d="M${-36 + i * 13} 16 v-12 a4.5 4.5 0 0 1 9 0 v12 z" fill="${D}" opacity=".55"/>`).join('') + [...Array(6)].map((_, i) => `<path d="M${-36 + i * 13} -2 v-7 a4.5 4.5 0 0 1 9 0 v7 z" fill="${D}" opacity=".55"/>`).join(''),
  ark: `<path d="M-50 4 Q0 30 50 4 L44 -2 H-44 Z"/><rect x="-26" y="-22" width="44" height="20"/><path d="M-30 -22 L-4 -36 L22 -22 Z"/>`,
  caravel: `<path d="M-44 14 Q0 34 46 10 L40 4 H-40 Z"/><path d="M-20 2 V-44" stroke="${G}" stroke-width="3"/><path d="M8 2 V-50" stroke="${G}" stroke-width="3"/><path d="M-36 -6 Q-20 -24 -32 -40 H-6 Q-2 -22 -8 -6 Z"/><path d="M-6 -8 Q8 -30 -4 -46 H22 Q28 -26 20 -8 Z"/><path d="M26 -2 L40 -2 L28 -26 Z"/>`,
  castle: `<path d="M-48 26 Q-30 4 -20 6 Q0 -2 20 6 Q34 2 48 26 Z"/><rect x="-22" y="-20" width="44" height="28"/><rect x="-30" y="-34" width="14" height="42"/><rect x="16" y="-40" width="14" height="48"/><path d="M-30 -34 h4 v-6 h3 v6 h4 v-6 h3 v6" /><rect x="-4" y="-8" width="8" height="12" fill="${D}" opacity=".55"/>`,
  temple: `<path d="M-42 -14 L0 -34 L42 -14 Z"/><rect x="-40" y="-12" width="80" height="6"/>` + [...Array(6)].map((_, i) => `<rect x="${-36 + i * 14}" y="-4" width="7" height="24"/>`).join('') + `<rect x="-44" y="20" width="88" height="6"/>`,
  longship: `<path d="M-52 6 Q-40 26 0 26 Q40 26 52 6 Q46 2 42 8 Q20 16 0 16 Q-20 16 -42 8 Q-46 2 -52 6 Z"/><path d="M-52 6 Q-60 -8 -50 -16" stroke="${G}" stroke-width="5" fill="none"/><path d="M52 6 Q60 -8 50 -16" stroke="${G}" stroke-width="5" fill="none"/><path d="M0 14 V-46" stroke="${G}" stroke-width="3"/><rect x="-24" y="-42" width="48" height="40" rx="3"/><path d="M-24 -28 h48 M-24 -14 h48" stroke="${D}" stroke-width="5" opacity=".35"/>`,
  wall: `<path d="M-50 18 L-30 4 L-10 10 L10 -4 L30 2 L50 -10 L50 0 L30 12 L10 6 L-10 20 L-30 14 L-50 28 Z"/><rect x="-36" y="-10" width="12" height="18"/><rect x="18" y="-16" width="12" height="18"/>`,
};
const place = [
  ['pyramids', [31.2, 27.0], 1.6], ['colosseum', [11.5, 43.0], 1.25], ['ark', [40.5, 42.5], 1.35],
  ['castle', [58, 29.5], 1.3], ['caravel', [-24, 31], 1.5], ['longship', [8, 62], 1.3],
];
const placed = place.map(([k, ll, s]) => { const [x, y] = P(ll); return `<g transform="translate(${x} ${y}) scale(${s})" fill="${G}" stroke="${D}" stroke-width="2.4" stroke-linejoin="round" filter="url(#ig)">${icons[k]}</g>`; }).join('\n');
const dots = place.map(([k, ll]) => { const [x, y] = P(ll); return `<circle cx="${x}" cy="${y + 2}" r="3" fill="#9c2f1f"/>`; }).join('');
const svg = `<svg id="globe" viewBox="0 0 ${S} ${S}" width="${S}" height="${S}" xmlns="http://www.w3.org/2000/svg">
<defs>
 <radialGradient id="sea" cx="42%" cy="38%" r="70%"><stop offset="0" stop-color="#2a5560"/><stop offset=".6" stop-color="#143039"/><stop offset="1" stop-color="#07151a"/></radialGradient>
 <radialGradient id="shine" cx="35%" cy="30%" r="60%"><stop offset="0" stop-color="#fff6dc" stop-opacity=".22"/><stop offset=".5" stop-color="#fff6dc" stop-opacity="0"/></radialGradient>
 <radialGradient id="shadow" cx="65%" cy="70%" r="65%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".6"/></radialGradient>
 <linearGradient id="landg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e8d7ad"/><stop offset="1" stop-color="#b99a62"/></linearGradient>
 <filter id="ig" x="-50%" y="-50%" width="200%" height="200%"><feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#000" flood-opacity=".7"/></filter>
 <clipPath id="disc"><circle cx="${C}" cy="${C + 8}" r="${R}"/></clipPath>
</defs>
<circle cx="${C}" cy="${C + 8}" r="${R}" fill="url(#sea)"/>
<g clip-path="url(#disc)">
 <path d="${path(grat)}" fill="none" stroke="#d9b26a" stroke-opacity=".18" stroke-width="1.2"/>
 <path d="${path(land)}" fill="url(#landg)" stroke="#6b5636" stroke-width="1.6"/>
 ${dots}
 ${placed}
 <circle cx="${C}" cy="${C + 8}" r="${R}" fill="url(#shine)"/>
 <circle cx="${C}" cy="${C + 8}" r="${R}" fill="url(#shadow)"/>
</g>
<circle cx="${C}" cy="${C + 8}" r="${R}" fill="none" stroke="#d9b26a" stroke-width="4"/>
</svg>`;
fs.writeFileSync(process.argv[2], svg);
console.log('ok');

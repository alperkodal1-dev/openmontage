// Big month labels for the full-screen sequence. Usage: node overlays2.js
const { chromium } = require('playwright');
const fs = require('fs');
const M = ['JANUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER'];
const css = `@font-face{font-family:M;font-weight:800;src:url(Manrope-800-normal.woff2)}html,body{margin:0;background:transparent}`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  for (let i = 0; i < 12; i++) {
    const h = `<div style="width:1080px;height:300px;position:relative;font-family:M;font-weight:800;text-align:center">
      <div style="position:absolute;top:24px;left:0;right:0;color:#fff;font-size:34px;letter-spacing:6px;text-shadow:0 4px 18px #000">THE ECONOMIST · 2027 · ${String(i + 1).padStart(2, '0')}/12</div>
      <div style="position:absolute;top:84px;left:50%;transform:translateX(-50%);background:#0b0b0b;color:#fff;font-size:118px;line-height:1;padding:18px 44px;letter-spacing:-2px;white-space:nowrap;border-bottom:10px solid #e3120b">${M[i]}</div></div>`;
    fs.writeFileSync('_t.html', `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${h}</body></html>`);
    await p.goto('file://' + process.cwd() + '/_t.html'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(120);
    await p.locator('body > div').first().screenshot({ path: `ov/big${i}.png`, omitBackground: true });
  }
  fs.unlinkSync('_t.html'); await b.close();
})();

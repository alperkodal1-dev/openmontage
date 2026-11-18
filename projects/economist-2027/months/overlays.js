// Text overlays (transparent PNGs) for the 12-month Short. Usage: node overlays.js
const { chromium } = require('playwright');
const fs = require('fs');
const M = ['JANUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER'];
const css = `@font-face{font-family:M;font-weight:800;src:url(Manrope-800-normal.woff2)}html,body{margin:0;background:transparent}`;
const pages = {
  title: `<div style="width:1080px;height:520px;position:relative;font-family:M;font-weight:800;text-align:center">
    <div style="position:absolute;top:262px;left:0;right:0;color:#fff;font-size:46px;letter-spacing:6px">THE ECONOMIST · THE WORLD AHEAD</div>
    <div style="position:absolute;top:316px;left:0;right:0;color:#e3120b;font-size:150px;letter-spacing:-4px;line-height:1">2027</div>
    <div style="position:absolute;top:466px;left:0;right:0;color:#fff;font-size:40px;letter-spacing:3px">12 MONTHS · 12 SIGNS?</div></div>`,
  question: `<div style="width:1080px;height:260px;position:relative;font-family:M;font-weight:800;text-align:center">
    <div style="position:absolute;top:40px;left:60px;right:60px;background:#e3120b;color:#fff;font-size:66px;line-height:1.08;padding:22px 26px;transform:rotate(-2deg);box-shadow:0 18px 50px rgba(0,0,0,.6)">WHICH MONTH SCARES<br>YOU THE MOST?</div></div>`,
};
M.forEach((m, i) => pages['label' + i] = `<div style="width:336px;height:46px;background:#0b0b0b;color:#fff;font-family:M;font-weight:800;font-size:30px;line-height:46px;text-align:center;letter-spacing:1px">${m}</div>`);
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  fs.mkdirSync('ov', { recursive: true });
  for (const [k, h] of Object.entries(pages)) {
    fs.writeFileSync('_t.html', `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${h}</body></html>`);
    await p.goto('file://' + process.cwd() + '/_t.html'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(150);
    await p.locator('body > div').first().screenshot({ path: `ov/${k}.png`, omitBackground: true });
  }
  fs.unlinkSync('_t.html'); await b.close();
})();

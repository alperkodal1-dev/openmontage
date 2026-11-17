// node tools/snap.js <port> <outdir> t1 t2 ...  -> screenshots of the composition at those times
const { chromium } = require('playwright');
(async () => {
  const [port, out, ...ts] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto(`http://localhost:${port}/index.html`); await p.waitForTimeout(1500);
  for (const t of ts) { await p.evaluate(t => { window.__timelines.main.seek(+t, false); }, t); await p.waitForTimeout(250);
    await p.screenshot({ path: `${out}/f_${t}.jpg`, type: 'jpeg', quality: 70 }); }
  await b.close();
})();

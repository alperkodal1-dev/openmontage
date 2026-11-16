// Seek the composition to the given seconds and save frames: node tools/snap.js out_dir t1 t2 ...
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [out, ...ts] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--disable-dev-shm-usage'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve('hf/index.html'), { waitUntil: 'domcontentloaded' }); await p.waitForTimeout(500);
  for (const t of ts.map(Number)) {
    await p.evaluate(t => { window.__timelines.main.seek(t, false); }, t);
    await p.screenshot({ path: `${out}/f_${t}.jpg`, type: 'jpeg', quality: 70, timeout: 30000 });
  }
  await b.close();
})().catch(e => { console.log('X', e.message); process.exit(1); });

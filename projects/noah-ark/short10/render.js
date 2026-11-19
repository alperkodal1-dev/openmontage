// Step the page through every frame and pipe screenshots to ffmpeg. Usage: node render.js
const { chromium } = require('playwright');
const { spawn } = require('child_process');
(async () => {
  const FPS = 30, DUR = 9.8, N = Math.round(FPS * DUR);
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-c:v', 'png', '-r', String(FPS), '-i', '-', '-i', 'audio.wav',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', 'noah_10s.mp4'], { stdio: ['pipe', 'inherit', 'inherit'] });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + process.cwd() + '/page.html');
  await p.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
  await p.evaluate(() => Promise.all(['a/myle.jpg','a/ararat.jpg','a/cudi.jpg'].map(s => new Promise(r => { const i = new Image(); i.onload = r; i.src = s; }))));
  for (let f = 0; f < N; f++) {
    await p.evaluate(t => window.render(t), f / FPS);
    await p.evaluate(() => document.getElementById('img').decode().catch(() => {}));
    ff.stdin.write(await p.screenshot({ type: 'png' }));
  }
  ff.stdin.end(); await b.close();
  await new Promise(r => ff.on('close', r)); console.log('ok noah_10s.mp4');
})();

// Unsealed History: the grey signature on the opening question's doubt ("...or did they?").
// Use inside a HyperFrames composition with GSAP. `tl` is the root timeline, `img` the full-frame picture,
// `flash` a full-screen span (position:absolute; inset:0; background:#f4ead2; opacity:0), `t` the time of the doubt.
// Pair it with: a big two-line Cinzel title of the claim, and the red stamp of the doubt popping in at t + 0.05
// (tl.from(stamp, { opacity: 0, scale: 2.0, duration: 0.35, ease: "power4.out" }, t + 0.05)).
// Sound: hit at 0 s, rumble at 0 s, swell at 0.15 s, hit at t + 0.05.
function greySignature(tl, img, flash, t) {
  tl.fromTo(img, { filter: "grayscale(0) sepia(.2) contrast(1.06) brightness(.8)" },
    { filter: "grayscale(1) sepia(.4) contrast(1.25) brightness(.8)", duration: 0.12, ease: "none", immediateRender: false }, t);
  [18, -22, 16, -12, 10, -8, 6, -4, 2, 0].forEach((x, i) =>
    tl.to(img, { x, y: (i % 2 ? 1 : -1) * x * 0.6, duration: 0.05, ease: "none" }, t + 0.04 + i * 0.055));
  tl.fromTo(flash, { opacity: 0 }, { opacity: 0.85, duration: 0.06, ease: "none", immediateRender: false }, t + 0.62);
  tl.to(flash, { opacity: 0, duration: 0.3, ease: "power2.out" }, t + 0.68);
}
// Opening question card (HTML), as in egypt-pyramids/index.tpl.html:
// <section id="q0" class="clip" data-start="0" data-duration="{{D}}">
//   <div class="center" style="top:330px"><div class="big" style="font-size:118px;color:#efe6d2">BUILT BY</div>
//     <div class="big" style="font-size:150px;color:#f1d49a">SLAVES?</div></div>
//   <div class="row" style="top:1080px"><div class="stamp" style="font-size:72px">…OR DID THEY?</div></div>
// </section>
// The narration's own timeline is then placed after the question: root.add(scenes, D).

// The story turn, "Or so the story goes." (Salem, Rome): at time t the legend picture turns grey and a little darker,
// the legend's labels fade, and the red MYTH stamp slams in at t + 0.6. `labels` = the legend's on-screen texts.
function storyGoes(tl, img, labels, stamp, t) {
  tl.to(labels, { opacity: 0, duration: 0.2 }, t);
  tl.fromTo(img, { filter: "grayscale(0) brightness(.85)" },
    { filter: "grayscale(1) contrast(1.1) brightness(.7)", duration: 0.15, ease: "none", immediateRender: false }, t);
  tl.fromTo(stamp, { opacity: 0, scale: 2.2, rotation: -4 }, { opacity: 1, scale: 1, rotation: -4, duration: 0.3, ease: "power4.out", immediateRender: false }, t + 0.6);
}
// Stamp HTML: <div class="row" style="top:640px"><div class="stamp" style="font-size:96px">MYTH</div></div>

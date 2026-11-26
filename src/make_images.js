// Renders src/og.html into the social (OG) image and the event images Google recommends (16:9, 4:3, 1:1).
// The OG image shows only the smile (#solo): WhatsApp crops it to a small square, where text can't be read.
// Run: node src/make_images.js   (needs Playwright)
const { chromium } = require('playwright');
const path = require('path');
const out = path.join(__dirname, '..', 'public', 'assets', 'img');
const sizes = [['og-image.png', 1200, 630, '#solo'], ['event-16x9.jpg', 1200, 675], ['event-4x3.jpg', 1200, 900], ['event-1x1.jpg', 1200, 1200]];
(async () => {
  const b = await chromium.launch();
  for (const [name, w, h, hash = ''] of sizes) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.goto('file://' + path.join(__dirname, 'og.html') + hash);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(out, name), type: name.endsWith('.jpg') ? 'jpeg' : 'png', quality: name.endsWith('.jpg') ? 85 : undefined });
    await p.close();
    console.log(name);
  }
  await b.close();
})();

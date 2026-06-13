import { chromium } from 'playwright';
import fs from 'fs';

const out = { error: null, data: null };
try {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await page.goto('http://localhost:8080/ar.html', { waitUntil: 'domcontentloaded', timeout: 90000 });
  await page.waitForTimeout(8000);
  out.data = await page.evaluate(() => {
    const slider = document.querySelector('#map .map_projects');
    const active = document.querySelector('#map .map_project.is-active');
    const card = active ? active.querySelector('.map_card') : null;
    const cs = (el) => el ? {
      v: getComputedStyle(el).visibility,
      o: getComputedStyle(el).opacity,
      h: getComputedStyle(el).height,
      d: getComputedStyle(el).display,
      rectH: el.getBoundingClientRect().height
    } : null;
    return {
      mode: slider && slider.dataset.mapMode,
      native: slider && slider.classList.contains('map-mobile-native'),
      flickity: slider && slider.classList.contains('flickity-enabled'),
      projects: slider ? slider.querySelectorAll('.map_project').length : 0,
      active: !!active,
      dots: document.querySelectorAll('#map .map_projects_dots button').length,
      card: cs(card),
      setH: document.querySelector('#map .map_projects_set')?.getBoundingClientRect().height
    };
  });
  await browser.close();
} catch (e) {
  out.error = String(e);
}
fs.writeFileSync('map-debug.json', JSON.stringify(out, null, 2));

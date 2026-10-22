#!/usr/bin/env node
// Phone QA in a real 390x844 viewport, through the Chrome DevTools Protocol.
// The full-page phone screenshots (page_shots.sh) draw the page in a very tall iframe, so the
// sticky bar can never appear there. This script scrolls a real phone viewport instead and checks:
//   sideways scrolling, the hero button on the first screen, the sticky bar at each scroll stop,
//   broken images, leftover [placeholders] and .ph boxes, and fbclid/UTM pass-through on every join button.
//
//   node scripts/phone_check.mjs "http://localhost:8000/index.html" shots/
//
// Needs Node 22+ (built-in WebSocket) and Google Chrome (set CHROME=/path/to/chrome if it lives elsewhere).
import { spawn } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const [pageUrl, outDir = 'shots'] = process.argv.slice(2);
if (!pageUrl) { console.error('usage: node phone_check.mjs <url> [out-dir]'); process.exit(1); }
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const sleep = ms => new Promise(r => setTimeout(r, ms));
mkdirSync(outDir, { recursive: true });

// Load the page as if it came from an ad click, so pass-through can be checked.
const url = new URL(pageUrl);
url.searchParams.set('fbclid', 'QA_TEST');
url.searchParams.set('utm_source', 'qa');

const profile = mkdtempSync(join(tmpdir(), 'phone-qa-'));
const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
  '--remote-debugging-port=0', `--user-data-dir=${profile}`, 'about:blank'], { stdio: 'ignore' });

let target;
try {
  // Chrome picks a free port and writes it to DevToolsActivePort in the profile folder.
  const portFile = join(profile, 'DevToolsActivePort');
  for (let i = 0; i < 100 && !target; i++) {
    await sleep(150);
    if (!existsSync(portFile)) continue;
    const port = readFileSync(portFile, 'utf8').split('\n')[0].trim();
    try { target = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find(t => t.type === 'page'); } catch {}
  }
  if (!target) throw new Error(`Chrome didn't start. Is it installed at ${CHROME}?`);

  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((r, j) => { ws.addEventListener('open', r, { once: true }); ws.addEventListener('error', j, { once: true }); });
  let id = 0; const pending = new Map(); const waiters = [];
  ws.addEventListener('message', ev => {
    const m = JSON.parse(ev.data);
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
    if (m.method) waiters.filter(w => w.method === m.method).forEach(w => w.resolve(m));
  });
  const send = (method, params = {}) => new Promise(r => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  const once = method => new Promise(resolve => waiters.push({ method, resolve }));
  const evaluate = async expr => {
    const res = (await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true })).result;
    if (res.exceptionDetails) throw new Error(res.exceptionDetails.exception?.description || res.exceptionDetails.text);
    return res.result.value;
  };

  await send('Page.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
  const loaded = once('Page.loadEventFired');
  await send('Page.navigate', { url: url.href });
  await loaded; await sleep(2500);   // fonts and the first images

  const report = await evaluate(`(async () => {
    const wait = ms => new Promise(r => setTimeout(r, ms));
    document.documentElement.style.scrollBehavior = 'auto';   // smooth scrolling would make scripted scrolls land late
    const $ = s => document.querySelector(s);
    const top = el => el ? Math.round(el.getBoundingClientRect().top + scrollY) : null;
    const sticky = $('#sticky'), hero = $('.hero');
    const heroBtn = $('.hero .js-join') || $('.hero .btn');
    const out = {
      viewport: innerWidth + 'x' + innerHeight,
      horizontalScroll: document.documentElement.scrollWidth > innerWidth,
      heroButtonOnFirstScreen: heroBtn ? heroBtn.getBoundingClientRect().bottom <= innerHeight : 'no hero button found',
      sticky: [] };
    const stops = [['top of page', 0]];
    if (hero) stops.push(['just past the hero', top(hero) + hero.offsetHeight + 120]);
    if ($('#love')) stops.push(['wall of love', top($('#love'))]);
    if ($('#price')) stops.push(['price card', top($('.price') || $('#price')) - 200]);
    if ($('.faq')) stops.push(['FAQ', top($('.faq'))]);
    stops.push(['bottom', document.documentElement.scrollHeight]);
    for (const [label, y] of stops) {
      scrollTo({ top: y, behavior: 'instant' }); await wait(700);
      if (sticky) out.sticky.push(label + ': ' + (sticky.classList.contains('show') ? 'showing' : 'hidden'));
    }
    if (!sticky) out.sticky = 'no #sticky bar on this page';
    await wait(1200);   // lazy images near the bottom
    out.brokenImages = [...document.images].filter(i => i.complete && !i.naturalWidth).map(i => i.currentSrc || i.src);
    out.placeholderText = [...new Set(document.body.innerText.match(/\\[[^\\]\\n]{2,80}\\]/g) || [])].slice(0, 25);
    out.placeholderBoxes = document.querySelectorAll('.ph, .ph-logo').length;
    const joins = [...document.querySelectorAll('.js-join')];
    out.joinButtons = joins.length;
    out.joinDestinations = [...new Set(joins.map(a => a.href.split('?')[0]))];
    out.joinMissingPassThrough = joins.filter(a => !a.href.includes('fbclid=QA_TEST') || !a.href.includes('utm_source=qa')).map(a => a.dataset.spot || a.textContent.trim());
    return out;
  })()`);
  console.log(JSON.stringify(report, null, 2));

  // Two real-viewport screenshots: mid-page (sticky bar should show) and the price card (should hide).
  const shots = [['phone-viewport-midpage.png', "(() => { const love = document.getElementById('love'), hero = document.querySelector('.hero'); return love ? love.getBoundingClientRect().top + scrollY : hero ? hero.getBoundingClientRect().bottom + scrollY + 120 : innerHeight * 2; })()"],
                 ['phone-viewport-price.png', "(document.querySelector('.price') || document.body).getBoundingClientRect().top + scrollY - 120"]];
  for (const [name, expr] of shots) {
    await evaluate(`scrollTo({top: ${expr}, behavior: 'instant'}); new Promise(r => setTimeout(r, 700))`);
    const shot = await send('Page.captureScreenshot', { format: 'png' });
    writeFileSync(join(outDir, name), Buffer.from(shot.result.data, 'base64'));
    console.log('wrote', join(outDir, name));
  }
  ws.close();
} finally {
  chrome.kill(); await sleep(300);
  try { rmSync(profile, { recursive: true, force: true }); } catch {}
}

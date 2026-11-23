/**
 * Interaction checks for the 22 Nov 2026 game-tool refresh.
 * Run against a local static server:
 *   BASE=http://127.0.0.1:8765 node scripts/tests/refresh_20261122.mjs
 */
import { mkdirSync } from "node:fs";
import { createRequire } from "node:module";

const require = createRequire("/tmp/pw/package.json");
const puppeteer = require("puppeteer-core");

const BASE = process.env.BASE || "http://127.0.0.1:8765";
const OUT = "/opt/cursor/artifacts";
mkdirSync(OUT, { recursive: true });

const chrome = process.env.CHROME || "/usr/bin/google-chrome";
const fails = [];
function check(name, ok, detail) {
  if (!ok) fails.push(name + (detail ? ": " + detail : ""));
  else console.log("ok", name);
}

async function shot(page, name) {
  await page.screenshot({ path: `${OUT}/${name}.png`, fullPage: false });
}

async function overflow(page) {
  return page.evaluate(() => {
    const doc = document.documentElement;
    return doc.scrollWidth <= doc.clientWidth + 1;
  });
}

async function imagesOk(page) {
  await page.evaluate(async () => {
    for (const img of document.images) {
      img.scrollIntoView();
      if (img.loading === "lazy") img.loading = "eager";
    }
    await Promise.all([...document.images].map((img) => img.complete && img.naturalWidth > 0
      ? Promise.resolve()
      : new Promise((resolve) => {
          img.addEventListener("load", resolve, { once: true });
          img.addEventListener("error", resolve, { once: true });
        })));
  });
  return page.evaluate(() =>
    [...document.images].every((img) => img.complete && img.naturalWidth > 0)
  );
}

const browser = await puppeteer.launch({
  executablePath: chrome,
  headless: true,
  args: ["--no-sandbox", "--disable-dev-shm-usage"],
});

async function desktop() {
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 });
  return page;
}

async function phone(width = 390) {
  const page = await browser.newPage();
  await page.setViewport({ width, height: 844, isMobile: true, hasTouch: true });
  return page;
}

// --- GTA storage ---
{
  const page = await desktop();
  await page.goto(BASE + "/gta-6/storage-check/", { waitUntil: "networkidle0" });
  check("storage images", await imagesOk(page));
  check("storage no overflow", await overflow(page));
  async function resultFor(value) {
    await page.$eval("#freeGb", (el, v) => {
      el.value = v;
      el.dispatchEvent(new Event("input", { bubbles: true }));
    }, value);
    return page.$eval("#storageResult", (el) => el.innerText);
  }
  const low = await resultFor("211");
  const exact = await resultFor("212");
  const high = await resultFor("500");
  const bad = await resultFor("");
  const neg = await resultFor("-5");
  check("211 below minimum", /Below the 212 GB minimum/.test(low) && /1 GB more/.test(low), low);
  check("212 meets minimum", /Exactly the 212 GB minimum/.test(exact), exact);
  check("500 enough and not an install size", /Enough free space/.test(high) && /not a confirmed exact install size/.test(high), high);
  check("empty invalid", /Enter a number/.test(bad), bad);
  check("negative invalid", /Enter a number/.test(neg), neg);
  await resultFor("500");
  await shot(page, "gta-storage-500");
  await page.close();
}

// --- GTA countdown ---
{
  const page = await desktop();
  await page.goto(BASE + "/gta-6/launch-countdown/", { waitUntil: "networkidle0" });
  async function read(tz) {
    await page.select("#region", tz);
    await new Promise((r) => setTimeout(r, 50));
    return page.evaluate(() => ({
      cd: document.querySelector("#cd").innerText,
      unlock: document.querySelector("#unlockLine").innerText,
      msk: document.querySelector("#mskLine").innerText,
    }));
  }
  const la = await read("America/Los_Angeles");
  const msk = await read("Europe/Moscow");
  check("LA unlocked elapsed", /^Unlocked\s+\d+d/.test(la.cd) && !la.cd.includes("-"), la.cd);
  check("Moscow unlocked elapsed", /^Unlocked\s+\d+d/.test(msk.cd), msk.cd);
  check("no single moscow time", la.msk !== msk.msk, la.msk + " vs " + msk.msk);
  check("past tense line", /Unlocked 19 Nov 2026/.test(la.unlock), la.unlock);
  // Pre-launch path still counts forward, not "Unlocked".
  await page.evaluate(() => {
    const real = Date.now;
    Date.now = () => Date.UTC(2026, 10, 1, 0, 0, 0);
    document.querySelector("#region").dispatchEvent(new Event("change"));
    window.__restoreNow = real;
  });
  await new Promise((r) => setTimeout(r, 50));
  const before = await page.$eval("#cd", (el) => el.innerText);
  check("before launch still counts down", !before.startsWith("Unlocked") && /^\d+d/.test(before), before);
  await page.evaluate(() => { Date.now = window.__restoreNow; });
  await page.select("#region", "Europe/Moscow");
  await shot(page, "gta-countdown-moscow");
  await page.close();
}

// --- editions ---
{
  const page = await desktop();
  await page.goto(BASE + "/gta-6/editions/", { waitUntil: "networkidle0" });
  const now = await page.$eval("#editionResult", (el) => el.innerText);
  await page.select("#buyWhen", "before");
  const before = await page.$eval("#editionResult", (el) => el.innerText);
  const body = await page.$eval("main", (el) => el.innerText);
  check("buying now closed window", /does not include the Vintage Vice City Pack/.test(now), now);
  check("before window historical", /before 20 Nov 2026/.test(before) && /cannot see your account/.test(before), before);
  check("results differ", now !== before);
  check("pack price us only", /\$4\.99/.test(body) && /not a worldwide price/.test(body) && /does not mean you already own/.test(body));
  check("ultimate names", /Grotti Cheetah/.test(body) && /One-Eyed Willie/.test(body));
  await shot(page, "gta-editions-before");
  await page.close();
}

// --- compatibility ---
{
  const page = await desktop();
  await page.goto(BASE + "/gta-6/compatibility/", { waitUntil: "networkidle0" });
  async function click(name) {
    await page.click(`[data-name="${name}"]`);
    return page.$eval("#compatResult", (el) => el.innerText);
  }
  const pc = await click("PC");
  const ps4 = await click("PlayStation 4");
  const ps5 = await click("PlayStation 5");
  check("pc unknown", /not officially announced/.test(pc) && !/RTX|GB RAM|coming/i.test(pc), pc);
  check("ps4 no", /No — there is no version/.test(ps4), ps4);
  check("ps5 yes", /Yes — it runs/.test(ps5), ps5);
  await page.close();
}

// --- fps guide claims ---
{
  const page = await desktop();
  await page.goto(BASE + "/gta-6/60-fps-ps5/", { waitUntil: "networkidle0" });
  const text = await page.$eval("main", (el) => el.innerText);
  check("fps images", await imagesOk(page));
  check("unproven live gta", /unproven on a live PS5 copy of GTA 6/.test(text));
  check("v0.3.12 pin", /v0\.3\.12/.test(text));
  check("drawings stay v0.3.8", /v0\.3\.8/.test(text) && /not a v0\.3\.12 screenshot/.test(text));
  check("no native 60 claim", !/native 60/i.test(text) && !/runs at 60 FPS on PS5 Pro/i.test(text));
  await page.close();
}

// --- DPS calculator ---
{
  const page = await desktop();
  await page.goto(BASE + "/desktop-pension-squad/fuse-salvage-calculator/", { waitUntil: "networkidle0" });
  await page.select("#bracket", "2");
  await page.select("#rarity", "Epic");
  let outcomes = await page.$eval("#outcomes", (el) => el.innerText);
  check("epic 10-15 odds", /49\.88%/.test(outcomes) && /50\.12%/.test(outcomes) && !/Immortal/.test(outcomes), outcomes);
  await page.select("#bracket", "4");
  outcomes = await page.$eval("#outcomes", (el) => el.innerText);
  check("epic 20-30 odds", /49\.88%/.test(outcomes) && /0\.25%/.test(outcomes), outcomes);
  await page.$eval("#input-soul", (el) => {
    el.value = "10";
    el.dispatchEvent(new Event("input", { bubbles: true }));
  });
  const decision = await page.$eval("#decision", (el) => el.textContent);
  const salvage = await page.$eval("#salvage-total", (el) => el.textContent);
  const fuse = await page.$eval("#fuse-total", (el) => el.textContent);
  check("blank soul unknown", /unknown, not zero/i.test(decision) && /900 Soul/.test(salvage) && /Enter output values/.test(fuse), decision + " | " + salvage + " | " + fuse);
  check("no planner link", !(await page.$("#main a[href*='engraving-soul-planner']")));
  check("wiki link present", !!(await page.$("a[href='/desktop-pension-squad/wiki/']")));
  await shot(page, "dps-calc-epic-20-30");
  await page.close();
}

// --- DPS wiki ---
{
  const page = await desktop();
  await page.goto(BASE + "/desktop-pension-squad/wiki/", { waitUntil: "networkidle0" });
  async function search(q) {
    await page.$eval("#query", (el, v) => {
      el.value = v;
      el.dispatchEvent(new Event("input", { bubbles: true }));
    }, q);
    await new Promise((r) => setTimeout(r, 50));
    return page.$eval("#detail", (el) => el.innerText);
  }
  const evasion = await search("Evasion Rate");
  const hunter = await search("Hunter's Verdict");
  const geu = await search("Geumeum");
  const worn = await search("Worn Compass");
  check("evasion wording", /Evasion Rate/.test(evasion) && /Miss/.test(evasion), evasion.slice(0, 240));
  check("hunter one per animation", /one per animation/.test(hunter), hunter.slice(0, 240));
  check("geumeum not on sale", /Not on sale/.test(geu), geu.slice(0, 300));
  check("worn not obtainable", /not obtainable/i.test(worn), worn.slice(0, 300));
  check("wiki not a new extract", /Not a new extract/.test(await page.$eval("main", (el) => el.innerText)));
  await shot(page, "dps-wiki-geumeum");
  await page.close();
}

// --- ROB raid +7 ---
{
  const page = await desktop();
  await page.goto(BASE + "/rob-run/federal-raid-countdown/", { waitUntil: "networkidle0" });
  async function setOpen(zone, value) {
    await page.select("#mode", "custom");
    await page.select("#zone", zone);
    await page.$eval("#opened", (el, v) => {
      el.value = v;
      el.dispatchEvent(new Event("input", { bubbles: true }));
    }, value);
    await new Promise((r) => setTimeout(r, 30));
    return page.evaluate(() => ({
      utc: document.querySelector("#utcDate").innerText,
      msk: document.querySelector("#mskDate").innerText,
    }));
  }
  const utc = await setOpen("UTC", "2026-11-20T00:00");
  check("utc open plus 7", /Nov 27, 2026/.test(utc.utc), JSON.stringify(utc));
  const moscow = await setOpen("Europe/Moscow", "2026-11-01T00:00");
  check("moscow raid calendar", /Nov 8, 2026/.test(moscow.msk) && /Nov 7, 2026/.test(moscow.utc), JSON.stringify(moscow));
  const la = await setOpen("America/Los_Angeles", "2026-11-01T00:00");
  check("la raid is later utc day", /Nov 8, 2026/.test(la.utc), JSON.stringify(la));
  await page.close();
}

// --- ROB loot custom price ---
{
  const page = await desktop();
  await page.goto(BASE + "/rob-run/loot-profit-calculator/", { waitUntil: "networkidle0" });
  await page.waitForFunction(() => !/Loading/.test(document.querySelector("#dataNotice").innerText));
  await page.select("#category", "cargo");
  const note = await page.$eval("#cargoNote, .cargo-note, main", (el) => el.innerText);
  check("cargo warning present", /Cargo uses the smaller Notoriety/.test(note) || /smaller Notoriety/.test(await page.content()));
  await page.$eval("#customName", (el) => { el.value = "Test loot"; });
  await page.$eval("#customPrice", (el) => { el.value = "100"; el.dispatchEvent(new Event("input", { bubbles: true })); });
  await page.$eval("#customQty", (el) => { el.value = "2"; });
  await page.click("#addCustom");
  const sale = await page.$eval("#saleOut", (el) => el.innerText);
  check("custom price no bonus", /200/.test(sale), sale);
  const body = await page.$eval("main", (el) => el.innerText);
  check("prices stay 0.7.0", /0\.7\.0/.test(body) && /did not list price changes/.test(body));
  await page.select("#category", "all");
  await page.$eval("#search", (el) => { el.value = "Eviction"; el.dispatchEvent(new Event("input", { bubbles: true })); });
  await new Promise((r) => setTimeout(r, 400));
  await page.click("[data-add='evict_plot_1']");
  const evict = await page.$eval("#calcNotice", (el) => el.innerText);
  const line = await page.$eval("#haul", (el) => el.innerText);
  check("eviction not a live price", /not a live barter price/.test(evict) && /4,000|4000/.test(line), evict + " | " + line);
  await page.close();
}

// --- ROB splitter ---
{
  const page = await desktop();
  await page.goto(BASE + "/rob-run/squad-loot-splitter/", { waitUntil: "networkidle0" });
  await page.$eval("#pool", (el) => { el.value = "100"; el.dispatchEvent(new Event("input", { bubbles: true })); });
  await page.$eval("#count", (el) => { el.value = "4"; el.dispatchEvent(new Event("input", { bubbles: true })); });
  const shares = await page.$eval("#splitOut", (el) => el.innerText);
  check("equal split 100/4", (shares.match(/25/g) || []).length >= 4, shares);
  await page.click("#modeWeight");
  await page.$eval("#players input.weight", (el) => { el.value = "-1"; el.dispatchEvent(new Event("input", { bubbles: true })); });
  const msg = await page.$eval("#splitMsg", (el) => el.innerText);
  check("negative weight rejected", /can’t be negative|can't be negative/.test(msg), msg);
  await page.close();
}

// --- ROB news archive ---
{
  const page = await desktop();
  await page.goto(BASE + "/rob-run/server-status/", { waitUntil: "networkidle0" });
  const text = await page.$eval("main", (el) => el.innerText);
  check("archive heading", /Archive: EU login note read on 15 Nov 2026/.test(text));
  check("not a health probe", /does not measure whether the EU or East US/.test(text));
  check("no servers ok", !/servers are up|servers OK|all-clear/i.test(text) || /not an all-clear/.test(text));
  await page.evaluate(() => document.querySelector("#hand").scrollIntoView());
  await shot(page, "rob-news-archive");
  await page.close();
}

// --- mobile overflow on the main updated pages ---
for (const path of [
  "/gta-6/",
  "/gta-6/storage-check/",
  "/gta-6/launch-countdown/",
  "/gta-6/editions/",
  "/gta-6/60-fps-ps5/",
  "/desktop-pension-squad/fuse-salvage-calculator/",
  "/desktop-pension-squad/wiki/",
  "/rob-run/server-status/",
]) {
  const page = await phone();
  await page.goto(BASE + path, { waitUntil: "networkidle0" });
  check("mobile overflow " + path, await overflow(page));
  check("mobile images " + path, await imagesOk(page));
  await page.close();
}

await browser.close();
if (fails.length) {
  console.error("FAILED\n" + fails.join("\n"));
  process.exit(1);
}
console.log("all interaction checks passed");

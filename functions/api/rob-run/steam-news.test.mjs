import assert from "node:assert/strict";
import test from "node:test";
import {
  APP_ID,
  FEED_NAME,
  FRESH_MS,
  SOURCE_URL,
  bbcodeToPlain,
  excerpt,
  loadAnnouncements,
  parseSteamNews,
  safeSteamLink,
} from "./steam-news.mjs";

const EU_DATE = 1794690004;

function memoryCache() {
  const box = { value: null };
  return {
    async match() {
      return box.value ? new Response(JSON.stringify(box.value), {
        headers: { "content-type": "application/json" },
      }) : undefined;
    },
    async put(_request, response) {
      box.value = await response.json();
    },
    stored() {
      return box.value;
    },
  };
}

function samplePayload() {
  return {
    appnews: {
      appid: APP_ID,
      newsitems: [
        {
          gid: "999",
          title: "SteamDB ROB RUN peaks",
          url: "https://steamdb.info/app/4262460",
          date: EU_DATE + 10,
          feedname: "SteamDB",
          appid: APP_ID,
          contents: "not official",
        },
        {
          gid: "1849458702684655",
          title: "Technical Issues on EU Servers",
          url: "https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849458702684655",
          author: "Tronix",
          date: EU_DATE,
          feedname: FEED_NAME,
          appid: APP_ID,
          contents: "[p]We’re currently aware of login issues on the [b]EU servers[/b].[/p][p][b]US servers are not affected[/b][/p]<script>alert(1)</script>",
        },
        {
          gid: "1849192144187218",
          title: "PlayGround note",
          date: EU_DATE - 100,
          feedname: "PlayGround.ru - официальная группа",
          appid: APP_ID,
          contents: "syndicated",
        },
      ],
    },
  };
}

test("plain text drops bbcode, html, and scripts", () => {
  const text = bbcodeToPlain("[b]EU[/b] <script>alert(1)</script> [url=https://evil.example/]x[/url]");
  assert.equal(text.includes("<"), false);
  assert.equal(text.includes("script"), false);
  assert.equal(text.includes("evil.example"), false);
  assert.equal(text.includes("EU"), true);
});

test("parser keeps only community announcements and the published date", () => {
  const parsed = parseSteamNews(samplePayload());
  assert.equal(parsed.feedProvidesEditTime, false);
  assert.equal(parsed.items.length, 1);
  assert.equal(parsed.items[0].title, "Technical Issues on EU Servers");
  assert.equal(parsed.items[0].publishedAt, "2026-11-14T21:00:04.000Z");
  assert.equal(parsed.items[0].excerpt.includes("EU servers"), true);
  assert.equal(parsed.items[0].excerpt.includes("<"), false);
  assert.equal(
    parsed.items[0].link,
    "https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849458702684655",
  );
});

test("unsafe and mismatched links are dropped", () => {
  assert.equal(safeSteamLink("http://store.steampowered.com/news", "1"), null);
  assert.equal(safeSteamLink("https://example.com/news", "1"), null);
  assert.equal(
    safeSteamLink("https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/2", "1"),
    null,
  );
  assert.equal(
    safeSteamLink("https://store.steampowered.com/news/app/4262460", "1").startsWith("https://store.steampowered.com/"),
    true,
  );
});

test("malformed payloads throw and do not invent items", () => {
  assert.throws(() => parseSteamNews({ appnews: { appid: 1, newsitems: [] } }), /malformed/);
  assert.throws(() => parseSteamNews("nope"), /malformed/);
});

test("a cache hit does not reset the source fetch time", async () => {
  const cache = memoryCache();
  let calls = 0;
  const fetchImpl = async () => {
    calls += 1;
    return new Response(JSON.stringify(samplePayload()), { status: 200 });
  };
  const firstNow = Date.parse("2026-11-15T05:00:00.000Z");
  const first = await loadAnnouncements({ fetch: fetchImpl, cache, now: () => firstNow });
  assert.equal(first.cache, "miss");
  assert.equal(first.sourceFetchedAt, "2026-11-15T05:00:00.000Z");
  const secondNow = firstNow + 20 * 1000;
  const second = await loadAnnouncements({ fetch: fetchImpl, cache, now: () => secondNow });
  assert.equal(calls, 1);
  assert.equal(second.cache, "hit");
  assert.equal(second.fresh, true);
  assert.equal(second.sourceFetchedAt, first.sourceFetchedAt);
  assert.equal(second.servedAt, "2026-11-15T05:00:20.000Z");
  assert.notEqual(second.servedAt, second.sourceFetchedAt);
});

test("upstream failure keeps the last source time and does not mark the post resolved", async () => {
  const cache = memoryCache();
  let fail = false;
  const fetchImpl = async () => {
    if (fail) {
      const error = new Error("upstream");
      error.code = "upstream";
      throw error;
    }
    return new Response(JSON.stringify(samplePayload()), { status: 200 });
  };
  const firstNow = Date.parse("2026-11-15T05:00:00.000Z");
  await loadAnnouncements({ fetch: fetchImpl, cache, now: () => firstNow });
  fail = true;
  const later = await loadAnnouncements({
    fetch: fetchImpl,
    cache,
    now: () => firstNow + FRESH_MS + 5000,
  });
  assert.equal(later.fresh, false);
  assert.equal(later.cache, "stale");
  assert.equal(later.sourceFetchedAt, "2026-11-15T05:00:00.000Z");
  assert.equal(later.items[0].title, "Technical Issues on EU Servers");
  assert.equal(later.items[0].publishedAt, "2026-11-14T21:00:04.000Z");
  assert.equal("status" in later.items[0], false);
});

test("timeout with no cache returns an empty live error, not a fixture", async () => {
  const fetchImpl = async () => {
    const error = new Error("timeout");
    error.name = "AbortError";
    error.code = "timeout";
    throw error;
  };
  const result = await loadAnnouncements({
    fetch: fetchImpl,
    cache: memoryCache(),
    now: () => Date.parse("2026-11-15T05:00:00.000Z"),
  });
  assert.equal(result.ok, false);
  assert.equal(result.mode, "live");
  assert.equal(result.upstreamError, "timeout");
  assert.deepEqual(result.items, []);
  assert.equal(result.sourceFetchedAt, null);
});

test("live Steam feed contains the 20 Nov patch and drops syndicated feeds", async (t) => {
  if (process.env.SKIP_LIVE === "1") {
    t.skip("SKIP_LIVE=1");
    return;
  }
  const response = await fetch(SOURCE_URL, { headers: { accept: "application/json" } });
  assert.equal(response.ok, true);
  const parsed = parseSteamNews(await response.json());
  assert.equal(parsed.feed, FEED_NAME);
  assert.equal(parsed.feedProvidesEditTime, false);
  // The 14 Nov EU post (gid 1849458702684655) is no longer inside count=20.
  // The page must not invent it. The current official item in that window is the 20 Nov patch.
  const patch = parsed.items.find((item) => item.gid === "1849827110432538");
  assert.ok(patch, "expected the 20 Nov official Patch Notes in the live feed");
  assert.equal(patch.publishedAt, "2026-11-20T14:59:56.000Z");
  assert.equal(patch.title, "Patch Notes");
  assert.equal(/SteamDB|PlayGround/i.test(parsed.items.map((item) => item.title).join(" ")), false);
  assert.equal(parsed.items.some((item) => item.gid === "1849458702684655"), false);
});

test("excerpt stays bounded", () => {
  const long = excerpt("[p]" + "word ".repeat(200) + "[/p]");
  assert.equal(long.length <= 421, true);
  assert.equal(long.includes("[p]"), false);
});

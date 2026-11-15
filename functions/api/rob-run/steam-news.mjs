/**
 * Locked Steam community-announcement reader for ROB RUN.
 * Not an open proxy: the app id, feed name, and upstream URL are constants.
 * The feed's `date` is the published time. This module does not invent an edit time.
 */

export const APP_ID = 4262460;
export const FEED_NAME = "steam_community_announcements";
export const SOURCE_URL =
  "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=4262460&count=20&maxlength=1500";
export const FRESH_MS = 60 * 1000;
export const RETAIN_MS = 15 * 60 * 1000;
export const UPSTREAM_TIMEOUT_MS = 8000;
export const MAX_UPSTREAM_BYTES = 400000;
export const MAX_ITEMS = 12;
export const EXCERPT_CHARS = 420;

const CACHE_URL = "https://buffforge.invalid/cache/rob-run-steam-announcements-v1";

const LINK_HOSTS = new Set([
  "store.steampowered.com",
  "steamcommunity.com",
]);

export function cacheRequest() {
  return new Request(CACHE_URL, { method: "GET" });
}

export function bbcodeToPlain(input) {
  let text = String(input == null ? "" : input);
  text = text.replace(/\[previewyoutube[^\]]*\][\s\S]*?\[\/previewyoutube\]/gi, " ");
  text = text.replace(/\[img[^\]]*\][\s\S]*?\[\/img\]/gi, " ");
  text = text.replace(/\[url=(?:https?:\/\/[^\]\s]+)\]([\s\S]*?)\[\/url\]/gi, "$1");
  text = text.replace(/\[url\][\s\S]*?\[\/url\]/gi, " ");
  text = text.replace(/\[(?:\/)?(?:p|b|i|u|h[1-6]|list|quote|\*|\/\*|br|code)\]/gi, " ");
  text = text.replace(/\[[^\]\n]{0,80}\]/g, " ");
  text = text
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/gi, "'");
  text = text.replace(/<[^>]*>/g, " ");
  text = text.replace(/\s+/g, " ").trim();
  return text;
}

export function excerpt(input) {
  const text = bbcodeToPlain(input);
  if (text.length <= EXCERPT_CHARS) return text;
  return text.slice(0, EXCERPT_CHARS).replace(/\s+\S*$/, "").trim() + "…";
}

export function safeSteamLink(url, gid) {
  let parsed;
  try {
    parsed = new URL(String(url));
  } catch (err) {
    return null;
  }
  if (parsed.protocol !== "https:") return null;
  if (LINK_HOSTS.has(parsed.hostname)) return parsed.toString();
  if (
    parsed.hostname === "steamstore-a.akamaihd.net" &&
    parsed.pathname === "/news/externalpost/steam_community_announcements/" + gid
  ) {
    return parsed.toString();
  }
  return null;
}

function asPlain(value, max) {
  const text = bbcodeToPlain(value);
  if (!text) return "";
  return text.length > max ? text.slice(0, max) : text;
}

export function parseSteamNews(payload) {
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
    throw new Error("malformed");
  }
  const appnews = payload.appnews;
  if (!appnews || typeof appnews !== "object" || !Array.isArray(appnews.newsitems)) {
    throw new Error("malformed");
  }
  if (Number(appnews.appid) !== APP_ID) throw new Error("malformed");
  const items = [];
  for (const raw of appnews.newsitems) {
    if (!raw || typeof raw !== "object") continue;
    if (raw.feedname !== FEED_NAME) continue;
    if (Number(raw.appid) !== APP_ID) continue;
    if (typeof raw.title !== "string" || !raw.title.trim()) continue;
    if (typeof raw.gid !== "string" || !/^\d{1,30}$/.test(raw.gid)) continue;
    if (typeof raw.date !== "number" || !Number.isFinite(raw.date)) continue;
    const publishedMs = raw.date * 1000;
    if (publishedMs < Date.UTC(2020, 0, 1) || publishedMs > Date.UTC(2100, 0, 1)) continue;
    items.push({
      gid: raw.gid,
      title: asPlain(raw.title, 180),
      publishedAt: new Date(publishedMs).toISOString(),
      excerpt: excerpt(typeof raw.contents === "string" ? raw.contents : ""),
      link: safeSteamLink(raw.url, raw.gid),
      author: asPlain(raw.author || "", 80),
    });
  }
  items.sort(function (a, b) {
    return a.publishedAt < b.publishedAt ? 1 : a.publishedAt > b.publishedAt ? -1 : 0;
  });
  return {
    appid: APP_ID,
    feed: FEED_NAME,
    feedProvidesEditTime: false,
    items: items.slice(0, MAX_ITEMS),
  };
}

async function readBounded(response) {
  if (!response.body || !response.body.getReader) {
    const text = await response.text();
    if (text.length > MAX_UPSTREAM_BYTES) throw new Error("too_large");
    return text;
  }
  const reader = response.body.getReader();
  const chunks = [];
  let received = 0;
  while (true) {
    const step = await reader.read();
    if (step.done) break;
    received += step.value.byteLength;
    if (received > MAX_UPSTREAM_BYTES) {
      await reader.cancel();
      throw new Error("too_large");
    }
    chunks.push(step.value);
  }
  const merged = new Uint8Array(received);
  let offset = 0;
  for (const chunk of chunks) {
    merged.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return new TextDecoder().decode(merged);
}

export async function fetchSteamNews(fetchImpl, timeoutMs) {
  const controller = new AbortController();
  const timer = setTimeout(function () { controller.abort(); }, timeoutMs || UPSTREAM_TIMEOUT_MS);
  try {
    const response = await fetchImpl(SOURCE_URL, {
      method: "GET",
      signal: controller.signal,
      headers: { "accept": "application/json" },
    });
    if (!response.ok) {
      const error = new Error("upstream");
      error.code = "upstream";
      throw error;
    }
    const text = await readBounded(response);
    let json;
    try {
      json = JSON.parse(text);
    } catch (err) {
      const error = new Error("malformed");
      error.code = "malformed";
      throw error;
    }
    return parseSteamNews(json);
  } catch (err) {
    if (err && err.name === "AbortError") {
      const error = new Error("timeout");
      error.code = "timeout";
      throw error;
    }
    if (err && (err.message === "malformed" || err.message === "too_large")) {
      const error = new Error(err.message === "too_large" ? "upstream" : "malformed");
      error.code = error.message;
      throw error;
    }
    if (err && err.code) throw err;
    const error = new Error("upstream");
    error.code = "upstream";
    throw error;
  } finally {
    clearTimeout(timer);
  }
}

function storedResponse(payload) {
  return new Response(JSON.stringify(payload), {
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "public, max-age=900",
    },
  });
}

async function readCache(cache) {
  if (!cache || !cache.match) return null;
  const hit = await cache.match(cacheRequest());
  if (!hit) return null;
  try {
    return await hit.json();
  } catch (err) {
    return null;
  }
}

export async function loadAnnouncements(deps) {
  const nowMs = deps.now();
  const servedAt = new Date(nowMs).toISOString();
  const cached = await readCache(deps.cache);
  const cachedAt = cached && cached.sourceFetchedAt ? Date.parse(cached.sourceFetchedAt) : NaN;
  const age = Number.isFinite(cachedAt) ? nowMs - cachedAt : Infinity;
  if (cached && cached.items && age >= 0 && age < FRESH_MS) {
    return Object.assign({}, cached, {
      servedAt: servedAt,
      cache: "hit",
      fresh: true,
      upstreamError: null,
    });
  }
  try {
    const parsed = await fetchSteamNews(deps.fetch, deps.timeoutMs);
    const payload = {
      ok: true,
      mode: "live",
      appid: parsed.appid,
      feed: parsed.feed,
      coverage: "steam_community_announcements_only",
      feedProvidesEditTime: false,
      sourceFetchedAt: servedAt,
      items: parsed.items,
    };
    if (deps.cache && deps.cache.put) {
      await deps.cache.put(cacheRequest(), storedResponse(payload));
    }
    return Object.assign({}, payload, {
      servedAt: servedAt,
      cache: cached ? "refresh" : "miss",
      fresh: true,
      upstreamError: null,
    });
  } catch (err) {
    const code = (err && err.code) || "upstream";
    if (cached && cached.items && age >= 0 && age < RETAIN_MS) {
      return Object.assign({}, cached, {
        servedAt: servedAt,
        cache: "stale",
        fresh: false,
        upstreamError: code,
      });
    }
    return {
      ok: false,
      mode: "live",
      appid: APP_ID,
      feed: FEED_NAME,
      coverage: "steam_community_announcements_only",
      feedProvidesEditTime: false,
      sourceFetchedAt: null,
      servedAt: servedAt,
      cache: "miss",
      fresh: false,
      upstreamError: code,
      items: [],
    };
  }
}

export function clientResponse(payload) {
  const status = payload.ok ? 200 : 502;
  return new Response(JSON.stringify(payload), {
    status: status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      "x-rob-run-news-cache": payload.cache || "miss",
    },
  });
}

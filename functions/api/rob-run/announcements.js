import { loadAnnouncements, clientResponse } from "./steam-news.mjs";

/**
 * Request-driven Steam announcement reader.
 * A page view or refresh runs this function. Nothing polls Steam in the background.
 * caches.default keeps the last successful payload in this data center for 15 minutes.
 * A hit inside 60 seconds does not call Steam and does not change sourceFetchedAt.
 */

let inFlight = null;

function logOutcome(payload, ms) {
  console.log(JSON.stringify({
    event: "rob_run_steam_news",
    ok: payload.ok,
    cache: payload.cache,
    fresh: payload.fresh,
    items: Array.isArray(payload.items) ? payload.items.length : 0,
    upstreamError: payload.upstreamError || null,
    ms: ms,
  }));
}

export async function onRequest(context) {
  const request = context.request;
  if (request.method !== "GET" && request.method !== "HEAD") {
    return new Response(JSON.stringify({ ok: false, error: "method" }), {
      status: 405,
      headers: { "content-type": "application/json; charset=utf-8", "allow": "GET, HEAD", "cache-control": "no-store" },
    });
  }
  const started = Date.now();
  if (!inFlight) {
    inFlight = loadAnnouncements({
      fetch: globalThis.fetch,
      cache: caches.default,
      now: function () { return Date.now(); },
    }).finally(function () { inFlight = null; });
  }
  const payload = await inFlight;
  logOutcome(payload, Date.now() - started);
  const response = clientResponse(payload);
  if (request.method === "HEAD") {
    return new Response(null, { status: response.status, headers: response.headers });
  }
  return response;
}

// Serve the static 404 page with a real 404 status for /404.
// Cloudflare Pages Functions run ahead of static assets, so this
// takes precedence over the default handling of the /404 path.
export async function onRequest(context) {
  const url = new URL(context.request.url);
  const asset = await context.env.ASSETS.fetch(
    new Request(url.origin + "/404.html", context.request)
  );
  const headers = new Headers(asset.headers);
  headers.set("content-type", "text/html; charset=utf-8");
  return new Response(asset.body, { status: 404, headers });
}

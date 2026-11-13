// Serve the Russian static 404 page with a real 404 status for /ru/404.
// Mirrors functions/404.js; Cloudflare Pages walks up the directory tree
// for the nearest 404.html, so unknown /ru/* paths get this page too.
export async function onRequest(context) {
  const url = new URL(context.request.url);
  const asset = await context.env.ASSETS.fetch(
    new Request(url.origin + "/ru/404.html", context.request)
  );
  const headers = new Headers(asset.headers);
  headers.set("content-type", "text/html; charset=utf-8");
  return new Response(asset.body, { status: 404, headers });
}

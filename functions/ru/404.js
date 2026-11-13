// Serve the Russian static 404 page with a real 404 status for /ru/404.
// Mirrors functions/404.js; Cloudflare Pages walks up the directory tree
// for the nearest 404.html, so unknown /ru/* paths get this page too.
export async function onRequest(context) {
  const url = new URL(context.request.url);
  const asset = await context.env.ASSETS.fetch(url.origin + "/ru/404.html");
  const html = await asset.text();
  return new Response(html, {
    status: 404,
    headers: { "content-type": "text/html; charset=utf-8" },
  });
}

# BuffForge shared shell — used by scripts/build.py and scripts/transform_legacy.py.
# Every page built from here gets: system-font CSS, temporary noindex meta
# (user decision 2026-11-13: keep noindex until content is complete),
# canonical without www, hreflang only for real counterparts, JSON-LD.
import json

BASE = "https://buffforge.com"
EMAIL = "feedback@buffforge.com"
REVIEWED_EN = "Nov 13, 2026"
REVIEWED_RU = "13 ноября 2026 года"

GAMES = {
    "aion-2": {
        "name": "AION 2",
        "hub": {"en": "/aion-2/", "ru": "/ru/aion-2/"},
        "tm": {
            "en": "AION 2 is a trademark of NCSOFT. Not affiliated with or endorsed by NCSOFT.",
            "ru": "AION 2 — торговая марка NCSOFT. Сайт не связан с NCSOFT и не одобрен компанией.",
        },
    },
    "gta-6": {
        "name": "GTA 6",
        "hub": {"en": "/gta-6/", "ru": "/ru/gta-6/"},
        "tm": {
            "en": "Not affiliated with, endorsed by, or sponsored by Rockstar Games or Take-Two Interactive.",
            "ru": "Сайт не связан с Rockstar Games и Take-Two Interactive и не одобрен ими.",
        },
    },
}

COPY = {
    "en": {
        "home": "Home", "games": "Games", "about": "About",
        "data_line": "Data on this site is checked against official announcements and cited community sources as of Nov 13, 2026. Always confirm in-game.",
        "fan": "BuffForge is an independent fan project.",
        "report": "Report a mistake",
        "home_url": "/", "about_url": "/about/",
    },
    "ru": {
        "home": "Главная", "games": "Игры", "about": "О проекте",
        "data_line": "Данные сверены с официальными объявлениями и указанными источниками по состоянию на 13 ноября 2026 года. Всегда сверяйте в игре.",
        "fan": "BuffForge — независимый фанатский проект.",
        "report": "Сообщить об ошибке",
        "home_url": "/ru/", "about_url": "/ru/about/",
    },
}


def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def head(lang, title, desc, canon_path, alternates=None, jsonld=None):
    """alternates: dict like {'en': '/path/', 'ru': '/ru/path/'} for real counterparts only."""
    c = COPY[lang]
    lines = [
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<meta name="robots" content="noindex">',
        '<title>%s</title>' % _esc(title),
        '<meta name="description" content="%s">' % _esc(desc),
        '<link rel="canonical" href="%s%s">' % (BASE, canon_path),
        '<meta property="og:title" content="%s">' % _esc(title),
        '<meta property="og:description" content="%s">' % _esc(desc),
        '<meta property="og:type" content="website">',
        '<meta property="og:url" content="%s%s">' % (BASE, canon_path),
        '<meta property="og:image" content="%s/assets/og.png">' % BASE,
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">',
        '<link rel="stylesheet" href="/assets/site.css">',
    ]
    if alternates:
        for hl, p in sorted(alternates.items()):
            lines.append('<link rel="alternate" hreflang="%s" href="%s%s">' % (hl, BASE, p))
        lines.append('<link rel="alternate" hreflang="x-default" href="%s%s">' % (BASE, alternates["en"]))
    if jsonld:
        lines.append('<script type="application/ld+json">%s</script>' % json.dumps(jsonld, ensure_ascii=False))
    return "\n".join(lines)


def org_website_jsonld(lang):
    desc = {
        "en": "Small, honest tools and guides by game: reset trackers, official-spec checkers, and calculators. No login, no ads. Every number cites its source and review date.",
        "ru": "Инструменты и гайды по играм: трекер сброса AION 2 (10:00 МСК), проверка места под GTA 6, сравнение изданий. Без регистрации и рекламы. У каждой цифры — источник и дата проверки.",
    }[lang]
    return [
        {"@context": "https://schema.org", "@type": "Organization",
         "name": "BuffForge", "url": BASE},
        {"@context": "https://schema.org", "@type": "WebSite",
         "name": "BuffForge", "url": BASE, "inLanguage": lang, "description": desc},
    ]


def breadcrumb_jsonld(lang, items):
    # items: list of (name, path-or-None)
    els = []
    for i, (name, path) in enumerate(items, 1):
        it = {"@type": "ListItem", "position": i, "name": name}
        if path:
            it["item"] = BASE + path
        els.append(it)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": els}


def header_html(lang, current_path, switch_path):
    c = COPY[lang]
    home = c["home_url"]
    games_links = "".join(
        '<a href="%s">%s</a>' % (GAMES[g]["hub"][lang], GAMES[g]["name"])
        for g in ("aion-2", "gta-6"))
    en_href = current_path if lang == "en" else switch_path
    ru_href = switch_path if lang == "en" else current_path
    return (
        '<header class="site-header"><div class="wrap">'
        '<a class="logo" href="%s">Buff<span>Forge</span></a>'
        '<nav class="site-nav" aria-label="Main">'
        '<details class="navdrop"><summary>%s</summary><div class="drop">%s</div></details>'
        '<a href="%s">%s</a>'
        '<span class="lang-switch" aria-label="Language">'
        '<a href="%s" %s>EN</a><span class="sep">|</span><a href="%s" %s>RU</a>'
        '</span></nav></div></header>'
        % (home, c["games"], games_links, c["about_url"], c["about"],
           en_href, 'aria-current="page"' if lang == "en" else "",
           ru_href, 'aria-current="page"' if lang == "ru" else "")
    )


def crumbs_html(lang, items):
    c = COPY[lang]
    parts = ['<a href="%s">%s</a>' % (c["home_url"], c["home"])]
    for name, path in items:
        if path:
            parts.append('<a href="%s">%s</a>' % (path, _esc(name)))
        else:
            parts.append('<span aria-current="page">%s</span>' % _esc(name))
    return ('<nav class="crumbs" aria-label="Breadcrumb">'
            + '<span class="sep">›</span>'.join(parts) + '</nav>')


def footer_html(lang, games):
    c = COPY[lang]
    other_home = "/ru/" if lang == "en" else "/"
    tms = "<br>".join(GAMES[g]["tm"][lang] for g in games)
    return (
        '<footer class="site-footer"><div class="wrap">'
        '<div class="links"><a href="%s">%s</a><a href="%s">%s</a>'
        '<a href="mailto:%s">%s</a><a href="%s">%s</a></div>'
        '<p>%s %s</p><p>%s</p>'
        '</div></footer>'
        % (c["home_url"], c["home"], c["about_url"], c["about"], EMAIL, c["report"],
           other_home, "Русская версия" if lang == "en" else "English version",
           c["fan"], tms, c["data_line"])
    )


def page(lang, title, desc, canon_path, alternates, body_html, jsonld=None, switch_path=None, games=("aion-2", "gta-6"), tail=""):
    if switch_path is None:
        switch_path = alternates.get("ru") if lang == "en" else alternates.get("en")
        if switch_path is None:
            switch_path = "/ru/" if lang == "en" else "/"
    return (
        '<!DOCTYPE html>\n<html lang="%s">\n<head>\n%s\n</head>\n<body>\n%s\n%s\n%s\n%s\n</body>\n</html>\n'
        % (lang, head(lang, title, desc, canon_path, alternates, jsonld),
           header_html(lang, canon_path, switch_path), body_html, footer_html(lang, games), tail)
    )

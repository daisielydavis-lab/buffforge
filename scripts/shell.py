# BuffForge shared shell — used by scripts/build.py, scripts/build_tools.py,
# scripts/transform_legacy.py and scripts/build_dps.py.
# Daylight Forge visual system (design spec, 2026-11-13): light shell,
# 68px translucent white header, teal anvil mark, 4-column footer.
# Every page built from here gets: self-hosted IBM Plex fonts. noindex is
# opt-in after launch (pass noindex=True only where a page must stay out of
# the index). Canonical without www, hreflang only for real counterparts, JSON-LD.
import json

BASE = "https://buffforge.com"
EMAIL = "feedback@buffforge.com"
REVIEWED_EN = "Nov 13, 2026"
REVIEWED_RU = "13 ноября 2026 года"

GAMES = {
    "desktop-pension-squad": {
        "name": "Desktop Pension Squad",
        "short": "DPS",
        "hub": {"en": "/desktop-pension-squad/", "ru": "/ru/desktop-pension-squad/"},
        "tm": {
            "en": "DPS: Desktop Pension Squad is developed by detailgames and published by storytaco. DPSquad Wiki is a fan wiki, not an official publication.",
            "ru": "Desktop Pension Squad разработана detailgames и издаётся storytaco. DPSquad Wiki — фанатская вики, не официальный ресурс.",
        },
    },
    "aion-2": {
        "name": "AION 2",
        "short": "AION 2",
        "hub": {"en": "/aion-2/", "ru": "/ru/aion-2/"},
        "tm": {
            "en": "AION 2 is a trademark of NCSOFT.",
            "ru": "AION 2 — товарный знак NCSOFT.",
        },
    },
    "gta-6": {
        "name": "GTA 6",
        "short": "GTA 6",
        "hub": {"en": "/gta-6/", "ru": "/ru/gta-6/"},
        "tm": {
            "en": "Grand Theft Auto and GTA are trademarks of Take-Two Interactive. Rockstar Games is a trademark of Take-Two Interactive.",
            "ru": "Grand Theft Auto и GTA — товарные знаки Take-Two Interactive. Rockstar Games — товарный знак Take-Two Interactive.",
        },
    },
    "rob-run": {
        "name": "ROB RUN",
        "short": "ROB RUN",
        "hub": {"en": "/rob-run/", "ru": "/ru/rob-run/"},
        "tm": {
            "en": "ROB RUN is developed and published by Kefir.",
            "ru": "ROB RUN разработана и издаётся Kefir.",
        },
    },
}

ANVIL_SVG = (
    '<svg class="mark" viewBox="0 0 32 32" aria-hidden="true">'
    '<rect width="32" height="32" rx="8" fill="#0C706C"/>'
    '<path d="M8 13.5h16v2.2H19.5V23h-7V15.7H8V13.5zm4.2-5.2h7.6l1.6 3.4'
    'H10.6l1.6-3.4z" fill="#FFFFFF"/></svg>'
)

COPY = {
    "en": {
        "home": "Home", "games": "Games", "about": "About",
        "data_line": "Data on this site is checked against official announcements and cited community sources as of Nov 13, 2026. Always confirm in-game.",
        "fan": "BuffForge is an independent fan project.",
        "report": "Report a mistake",
        "home_url": "/", "about_url": "/about/",
        "tagline": "Game tools, trackers and calculators. Every number cites a public source.",
        "review_line": "Every number cites a public source. We recheck official sources before publishing. Last data review: 13 November 2026.",
        "affil": ("BuffForge is an independent fan project, not affiliated with, endorsed by, or sponsored "
                  "by detailgames, storytaco, NCSOFT, Rockstar Games, Take-Two Interactive, Kefir, or Valve Corporation."),
    },
    "ru": {
        "home": "Главная", "games": "Игры", "about": "О проекте",
        "data_line": "Данные сверены с официальными объявлениями и указанными источниками по состоянию на 13 ноября 2026 года. Всегда сверяйте в игре.",
        "fan": "BuffForge — независимый фанатский проект.",
        "report": "Сообщить об ошибке",
        "home_url": "/ru/", "about_url": "/ru/about/",
        "tagline": "Игровые инструменты, трекеры и калькуляторы. У каждой цифры — открытый источник.",
        "review_line": "У каждой цифры — открытый источник. Мы перепроверяем официальные источники перед публикацией. Последняя проверка данных: 13 ноября 2026.",
        "affil": ("BuffForge — независимый фанатский проект, не связанный с detailgames, storytaco, NCSOFT, "
                  "Rockstar Games, Take-Two Interactive, Kefir или Valve Corporation и не одобренный ими."),
    },
}


def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def head(lang, title, desc, canon_path=None, alternates=None, jsonld=None, noindex=False):
    """alternates: dict like {'en': '/path/', 'ru': '/ru/path/'} for real counterparts only.
    canon_path=None omits the canonical link and og:url (used by the 404 page).
    noindex is opt-in after launch: the robots meta is emitted only when noindex=True."""
    lines = [
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
    ]
    if noindex:
        lines.append('<meta name="robots" content="noindex">')
    lines += [
        '<title>%s</title>' % _esc(title),
        '<meta name="description" content="%s">' % _esc(desc),
    ]
    if canon_path is not None:
        lines.append('<link rel="canonical" href="%s%s">' % (BASE, canon_path))
    lines += [
        '<meta property="og:title" content="%s">' % _esc(title),
        '<meta property="og:description" content="%s">' % _esc(desc),
        '<meta property="og:type" content="website">',
    ]
    if canon_path is not None:
        lines.append('<meta property="og:url" content="%s%s">' % (BASE, canon_path))
    lines += [
        '<meta property="og:image" content="%s/assets/og.png">' % BASE,
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:locale" content="%s">' % ("en_US" if lang == "en" else "ru_RU"),
        '<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">',
        '<link rel="stylesheet" href="/assets/fonts.css">',
        '<link rel="stylesheet" href="/assets/site.css">',
    ]
    if alternates:
        for hl, p in sorted(alternates.items()):
            lines.append('<link rel="alternate" hreflang="%s" href="%s%s">' % (hl, BASE, p))
        lines.append('<link rel="alternate" hreflang="x-default" href="%s%s">' % (BASE, alternates["en"]))
    if jsonld:
        lines.append('<script type="application/ld+json">%s</script>' % json.dumps(jsonld, ensure_ascii=False))
    # Google Tag Manager (user request 2026-11-13; container GTM-PQNKG4CV).
    # Loads ONLY on buffforge.com — never on preview/staging hosts. No inline
    # gtag config: GA4 data flows only if a GA4 tag is configured inside the
    # GTM container itself.
    lines.append('<script>\n  window.dataLayer = window.dataLayer || [];\n'
                 '  (function () {\n'
                 "    if (window.location.hostname !== 'buffforge.com') return;\n"
                 '    var s = document.createElement("script");\n'
                 '    s.async = true;\n'
                 '    s.src = "https://www.googletagmanager.com/gtm.js?id=GTM-PQNKG4CV";\n'
                 '    document.head.appendChild(s);\n'
                 '  })();\n</script>')
    return "\n".join(lines)


def org_website_jsonld(lang):
    desc = {
        "en": "Free game tools, trackers and calculators, organized by game. Every number cites its source and review date. No login, no ads.",
        "ru": "Бесплатные игровые инструменты, трекеры и калькуляторы. У каждой цифры — источник и дата проверки. Без регистрации и рекламы.",
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
    """68px translucent white header: teal anvil mark + near-black wordmark,
    Games dropdown, About, language switch (current item teal bg, white text)."""
    c = COPY[lang]
    dots = {
        "desktop-pension-squad": "dps",
        "aion-2": "aion",
        "gta-6": "gta",
        "rob-run": "rob",
    }
    games_links = "".join(
        '<a href="%s"><span class="dot dot-%s"></span>%s</a>'
        % (GAMES[g]["hub"][lang], dots[g], GAMES[g]["name"])
        for g in ("desktop-pension-squad", "aion-2", "gta-6", "rob-run"))
    en_href = current_path if lang == "en" else switch_path
    ru_href = switch_path if lang == "en" else current_path
    return (
        '<header class="site-header"><div class="wrap nav">'
        '<a class="logo" href="%s">%s<span class="word">BuffForge</span></a>'
        '<nav class="site-nav" aria-label="Primary">'
        '<details class="navdrop"><summary>%s<svg width="11" height="11" viewBox="0 0 12 12" aria-hidden="true">'
        '<path d="M2.5 4.5 6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></summary>'
        '<div class="drop">%s</div></details>'
        '<a href="%s">%s</a>'
        '<span class="lang">'
        '<a href="%s" %s>English</a><a href="%s" %s>Русский</a>'
        '</span></nav></div></header>'
        % (c["home_url"], ANVIL_SVG, c["games"], games_links, c["about_url"],
           c["about"], en_href,
           'class="current" aria-current="true"' if lang == "en" else "",
           ru_href,
           'class="current" aria-current="true"' if lang == "ru" else "")
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
    """Four-column footer: brand, Site, Games, Language.
    No legal/trademark block: the per-game trademark lines and the
    site-wide review line were removed 2026-11-13 (user decision).
    The GAMES tm / COPY affil / review_line data stays defined in case
    it is needed again, but nothing renders it."""
    c = COPY[lang]
    game_links = "".join(
        '<a href="%s">%s</a>' % (GAMES[g]["hub"][lang], GAMES[g]["name"])
        for g in ("desktop-pension-squad", "aion-2", "gta-6", "rob-run"))
    if lang == "en":
        lang_items = ('<a href="/" class="current" aria-current="true">English</a>'
                      '<a href="/ru/">Русская версия</a>')
    else:
        lang_items = ('<a href="/">English version</a>'
                      '<a href="/ru/" class="current" aria-current="true">Русский</a>')
    return (
        '<footer class="site-footer"><div class="wrap">'
        '<div class="foot-grid">'
        '<div class="foot-brand">%s<div class="word">BuffForge</div><p>%s</p></div>'
        '<div><h2>%s</h2><div class="links"><a href="%s">%s</a><a href="%s">%s</a><a href="mailto:%s">%s</a></div></div>'
        '<div><h2>%s</h2><div class="links">%s</div></div>'
        '<div><h2>%s</h2><div class="links">%s</div></div>'
        '</div>'
        '</div></footer>'
        % (ANVIL_SVG, c["tagline"], "Site" if lang == "en" else "Сайт",
           c["home_url"], c["home"],
           c["about_url"], c["about"], EMAIL, c["report"],
           c["games"], game_links, "Language" if lang == "en" else "Язык", lang_items)
    )


def page(lang, title, desc, canon_path, alternates, body_html, jsonld=None, switch_path=None, games=("desktop-pension-squad", "aion-2", "gta-6"), tail="", noindex=False):
    if switch_path is None:
        switch_path = alternates.get("ru") if lang == "en" else alternates.get("en")
        if switch_path is None:
            switch_path = "/ru/" if lang == "en" else "/"
    skip = "Skip to content" if lang == "en" else "Перейти к содержимому"
    navdrop_js = (
        '<script>document.querySelectorAll(".navdrop summary").forEach(function(s){'
        's.addEventListener("click",function(){'
        'document.querySelectorAll(".navdrop").forEach(function(d){'
        'if(d!==s.parentElement){d.removeAttribute("open");}});});});</script>'
    )
    return (
        '<!DOCTYPE html>\n<html lang="%s">\n<head>\n%s\n</head>\n<body>\n'
        '<a class="skip" href="#main">%s</a>\n%s\n%s\n%s\n%s\n%s</body>\n</html>\n'
        % (lang, head(lang, title, desc, canon_path, alternates, jsonld, noindex=noindex), skip,
           header_html(lang, canon_path, switch_path), body_html,
           footer_html(lang, games), navdrop_js, tail)
    )

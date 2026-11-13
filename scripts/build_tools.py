#!/usr/bin/env python3
"""GTA 6 official-facts tools (EN + RU). Generated static pages.

Run:  cd <repo root> && python3 scripts/build_tools.py
Uses only verified official facts (see spec section 10.2):
- launch Nov 19, 2026, PS5 (+Pro) and Xbox Series X|S; no PC version at launch;
- PlayStation lists at least 212 GB free space;
- Standard $79.99 / Ultimate $99.99 (Take-Two US MSRP);
- Vintage Vice City Pack for purchases before Nov 20, 2026; one month GTA+
  with digital pre-order (per official announcement).
No speculative PC spec table anywhere. Xbox preload Moscow time is NOT
stated (unverified) — pages say to check the Xbox store.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import (BASE, breadcrumb_jsonld, crumbs_html, page)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def webapp_jsonld(lang, name, path, desc):
    return {"@context": "https://schema.org", "@type": "WebApplication",
            "name": name, "url": BASE + path, "inLanguage": lang,
            "description": desc, "applicationCategory": "GameApplication",
            "operatingSystem": "Any modern browser", "offers": {"@type": "Offer", "price": "0"}}


def tool_page(lang, game, slug, title, desc, body, crumbs, jsonld):
    canon = "/%s/%s/" % (game, slug) if lang == "en" else "/ru/%s/%s/" % (game, slug)
    alt = {"en": "/%s/%s/" % (game, slug), "ru": "/ru/%s/%s/" % (game, slug)}
    return page(lang, title, desc, canon, alt, body, jsonld=jsonld,
                games=(game,))


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", rel)


# ---------------------------------------------------------------- storage check
STORAGE = {
    "en": {
        "title": "GTA 6 Storage & Preload Check — BuffForge",
        "desc": "PlayStation lists at least 212 GB of free space for GTA 6. Enter your free space and see if it fits before preload day. No login, no ads.",
        "h1": "GTA 6 Storage &amp; Preload Check",
        "lede": "GTA 6 needs a lot of disk. PlayStation's official support page lists <b>at least 212 GB of free space</b>. Check yours before preload day — not after the download fails.",
        "label": "How much free space do you have? (GB)",
        "hint": "On PS5: Settings → Storage. On Xbox: My games &amp; apps → Manage → Free up space.",
        "platform_label": "Your console",
        "ps5": "PlayStation 5 / PS5 Pro",
        "xbox": "Xbox Series X|S",
        "check": "Check my space",
        "fits": "It fits.",
        "fits_p": "212 GB fits in your %s GB free — about %s GB would remain afterwards. Keep some headroom: updates and patches need room too.",
        "short": "Not enough space yet.",
        "short_p": "You need %s GB more free space to reach the 212 GB PlayStation lists. Delete a game or two, or move games to external storage where your console allows it.",
        "exact": "Exactly enough — barely.",
        "exact_p": "212 GB is exactly what you have. It fits on paper, but leave headroom for the day-one patch.",
        "preload_h": "Preload: what is confirmed",
        "preload": [
            "<b>PS5:</b> digital preload starts at local midnight for your account's region. The exact moment depends on your store region, not on one global time.",
            "<b>Xbox:</b> preload start time is shown in the Xbox store / console for your region. Check the store listing — we do not publish an unverified Moscow time.",
            "<b>212 GB</b> is the free space PlayStation lists as required. The final download size has not been separately confirmed by Rockstar.",
        ],
        "sources": "Sources: PlayStation official support (GTA VI), checked Nov 13, 2026. Always confirm in-game / in the store.",
    },
    "ru": {
        "title": "Проверка места под GTA 6 — BuffForge",
        "desc": "PlayStation указывает: для GTA 6 нужно не менее 212 ГБ свободного места. Введите, сколько свободно у вас, и узнайте, хватит ли места до предзагрузки.",
        "h1": "Проверка места под GTA 6",
        "lede": "GTA 6 занимает много места на диске. На официальной странице поддержки PlayStation указано: нужно <b>не менее 212 ГБ свободного места</b>. Проверьте заранее — а не когда загрузка оборвётся.",
        "label": "Сколько свободного места у вас? (ГБ)",
        "hint": "На PS5: Настройки → Хранилище. На Xbox: Мои игры и приложения → Управление → Освободить место.",
        "platform_label": "Ваша консоль",
        "ps5": "PlayStation 5 / PS5 Pro",
        "xbox": "Xbox Series X|S",
        "check": "Проверить место",
        "fits": "Места хватает.",
        "fits_p": "212 ГБ помещаются в ваши %s ГБ — после установки останется около %s ГБ. Оставьте запас: обновлениям и патчам тоже нужно место.",
        "short": "Пока не хватает места.",
        "short_p": "Чтобы набрать 212 ГБ, нужно освободить ещё %s ГБ. Удалите пару игр или перенесите их на внешний накопитель, если консоль это позволяет.",
        "exact": "Хватает ровно впритык.",
        "exact_p": "У вас ровно 212 ГБ. Формально хватает, но оставьте запас под патч первого дня.",
        "preload_h": "Предзагрузка: что подтверждено",
        "preload": [
            "<b>PS5:</b> цифровая предзагрузка начинается в местную полночь для региона вашего аккаунта. Точный момент зависит от региона магазина, а не от единого мирового времени.",
            "<b>Xbox:</b> время начала предзагрузки указано в магазине Xbox / на консоли для вашего региона. Смотрите карточку в магазине — непроверенное московское время мы не публикуем.",
            "<b>212 ГБ</b> — это свободное место, которое указывает PlayStation. Итоговый размер загрузки Rockstar отдельно не подтверждала.",
        ],
        "sources": "Источники: официальная поддержка PlayStation (GTA VI), проверено 13 ноября 2026 года. Всегда сверяйтесь с магазином и игрой.",
    },
}


def storage_page(lang):
    c = STORAGE[lang]
    home = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    hub_path = "/gta-6/" if lang == "en" else "/ru/gta-6/"
    preload = "".join("<li>%s</li>" % x for x in c["preload"])
    body = (
        '<main class="wrap narrow">%s'
        '<h1 class="page-h1">%s</h1><p class="page-lede">%s</p>'
        '<div class="checker"><form id="storageForm">'
        '<label for="freeGb">%s</label>'
        '<input type="number" id="freeGb" min="0" max="100000" step="1" value="500" inputmode="numeric">'
        '<p class="hint">%s</p>'
        '<label for="platform" style="margin-top:18px">%s</label>'
        '<select id="platform"><option value="ps5">%s</option><option value="xbox">%s</option></select>'
        '<div class="quick"><button type="button" data-gb="250">250 GB</button>'
        '<button type="button" data-gb="500">500 GB</button>'
        '<button type="button" data-gb="1000">1 TB</button>'
        '<button type="button" data-gb="2000">2 TB</button></div>'
        '<p style="margin-top:18px"><button class="btn btn-primary" type="submit">%s</button></p>'
        '</form><div class="result" id="storageResult" role="status"></div></div>'
        '<section class="prose"><h2 class="sec">%s</h2><ul>%s</ul></section>'
        '<p class="data-line">%s</p></main>'
        % (crumbs_html(lang, [(home, home_path), ("GTA 6", hub_path), (c["h1"].replace("&amp;", "&"), None)]),
           c["h1"], c["lede"], c["label"], c["hint"], c["platform_label"],
           c["ps5"], c["xbox"], c["check"], c["preload_h"], preload, c["sources"])
    )
    js = """
<script>
(function () {
  var NEED = 212;
  var form = document.getElementById('storageForm');
  var input = document.getElementById('freeGb');
  var result = document.getElementById('storageResult');
  var STR = %s;
  function check() {
    var free = parseFloat(input.value);
    if (isNaN(free) || free < 0) { result.className = 'result warn show';
      result.innerHTML = '<b class="big">' + STR.invalid + '</b>'; return; }
    var remain = free - NEED;
    if (remain > 0) { result.className = 'result ok show';
      result.innerHTML = '<b class="big">' + STR.fits + '</b><p>' +
        STR.fits_p.replace('%%s', free).replace('%%s', Math.round(remain)) + '</p>' +
        '<div class="bar"><i style="width:' + Math.min(100, NEED / free * 100) + '%%"></i></div>';
    } else if (remain === 0) { result.className = 'result warn show';
      result.innerHTML = '<b class="big">' + STR.exact + '</b><p>' + STR.exact_p + '</p>';
    } else { result.className = 'result bad show';
      result.innerHTML = '<b class="big">' + STR.short + '</b><p>' +
        STR.short_p.replace('%%s', Math.round(-remain)) + '</p>';
    }
  }
  document.querySelectorAll('.quick button').forEach(function (b) {
    b.addEventListener('click', function () { input.value = b.getAttribute('data-gb'); check(); });
  });
  form.addEventListener('submit', function (e) { e.preventDefault(); check(); });
  input.addEventListener('input', check);
  check();
})();
</script>
""" % ('{"fits": "%s", "fits_p": "%s", "short": "%s", "short_p": "%s", "exact": "%s", "exact_p": "%s", "invalid": "%s"}'
       % (c["fits"], c["fits_p"], c["short"], c["short_p"], c["exact"], c["exact_p"],
          "Enter a number, e.g. 500" if lang == "en" else "Введите число, например 500"))
    jl = [breadcrumb_jsonld(lang, [(home, home_path), ("GTA 6", hub_path), (c["h1"].replace("&amp;", "&"), "/gta-6/storage-check/" if lang == "en" else "/ru/gta-6/storage-check/")]),
          webapp_jsonld(lang, c["h1"].replace("&amp;", "&"), "/gta-6/storage-check/" if lang == "en" else "/ru/gta-6/storage-check/", c["desc"])]
    return tool_page(lang, "gta-6", "storage-check", c["title"], c["desc"], body + js,
                     None, jl)


# ---------------------------------------------------------------- launch countdown
REGIONS = [
    ("America/Los_Angeles", "Los Angeles (PT)", "Лос-Анджелес (PT)"),
    ("America/New_York", "New York (ET)", "Нью-Йорк (ET)"),
    ("America/Sao_Paulo", "São Paulo (BRT)", "Сан-Паулу (BRT)"),
    ("Europe/London", "London (GMT)", "Лондон (GMT)"),
    ("Europe/Paris", "Paris / Berlin (CET)", "Париж / Берлин (CET)"),
    ("Europe/Moscow", "Moscow (MSK)", "Москва (МСК)"),
    ("Asia/Dubai", "Dubai (GST)", "Дубай (GST)"),
    ("Asia/Kolkata", "Mumbai (IST)", "Мумбаи (IST)"),
    ("Asia/Tokyo", "Tokyo (JST)", "Токио (JST)"),
    ("Australia/Sydney", "Sydney (AEDT)", "Сидней (AEDT)"),
]

COUNTDOWN = {
    "en": {
        "title": "GTA 6 Launch Countdown — BuffForge",
        "desc": "GTA 6 launches Nov 19, 2026 at local midnight. Pick your store region and see the unlock time in your time zone and in Moscow time.",
        "h1": "GTA 6 Launch Countdown",
        "lede": "GTA 6 unlocks <b>Nov 19, 2026 at local midnight</b> — midnight in your store region's time zone. There is no single official Moscow unlock time: it depends on which region your account's store is in.",
        "label": "Your store region",
        "local_label": "Your time zone",
        "unlocks": "Unlocks Nov 19, 2026, 00:00 in %s",
        "moscow": "That is %s in Moscow (MSK, UTC+3).",
        "local": "In your local time: %s.",
        "released": "Released!",
        "released_p": "GTA 6 is out in this region. Go play.",
        "note_h": "What is confirmed — and what is not",
        "notes": [
            "<b>Confirmed:</b> launch date Nov 19, 2026; PS5 (including Pro) and Xbox Series X|S; no PC version at launch (Rockstar).",
            "<b>Not a single global moment:</b> because unlock is local midnight per region, the Moscow time differs by region. Any site quoting one Moscow unlock time for everyone is guessing.",
            "<b>Preload:</b> PS5 digital preload starts at local midnight for your account's region. Xbox preload time is shown in the Xbox store.",
        ],
        "sources": "Sources: Rockstar Games official newswire (launch date), PlayStation official support, checked Nov 13, 2026.",
    },
    "ru": {
        "title": "Обратный отсчёт до выхода GTA 6 — BuffForge",
        "desc": "GTA 6 выходит 19 ноября 2026 года в местную полночь. Выберите регион магазина и узнайте время выхода в вашем часовом поясе и по Москве.",
        "h1": "Обратный отсчёт до выхода GTA 6",
        "lede": "GTA 6 открывается <b>19 ноября 2026 года в местную полночь</b> — в полночь по времени региона вашего магазина. Единого официального московского времени выхода нет: оно зависит от региона магазина вашего аккаунта.",
        "label": "Регион вашего магазина",
        "local_label": "Ваш часовой пояс",
        "unlocks": "Выход 19 ноября 2026 года в 00:00 в регионе: %s",
        "moscow": "По Москве (МСК, UTC+3) это %s.",
        "local": "В вашем местном времени: %s.",
        "released": "Игра вышла!",
        "released_p": "В этом регионе GTA 6 уже доступна. Можно играть.",
        "note_h": "Что подтверждено, а что нет",
        "notes": [
            "<b>Подтверждено:</b> дата выхода 19 ноября 2026 года; PS5 (включая Pro) и Xbox Series X|S; версии для ПК на старте нет (Rockstar).",
            "<b>Не единый момент для всех:</b> раз выход — в местную полночь для каждого региона, московское время для разных регионов разное. Сайт, называющий одно московское время для всех, просто гадает.",
            "<b>Предзагрузка:</b> на PS5 цифровая предзагрузка начинается в местную полночь для региона вашего аккаунта. Время предзагрузки на Xbox указано в магазине Xbox.",
        ],
        "sources": "Источники: официальный ньюсвайр Rockstar Games (дата выхода), официальная поддержка PlayStation, проверено 13 ноября 2026 года.",
    },
}


def countdown_page(lang):
    c = COUNTDOWN[lang]
    home = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    hub_path = "/gta-6/" if lang == "en" else "/ru/gta-6/"
    opts = "".join('<option value="%s">%s</option>' % (tz, label) for tz, label, _ in
                   [(r[0], r[1] if lang == "en" else r[2], r[2]) for r in REGIONS])
    notes = "".join("<li>%s</li>" % x for x in c["notes"])
    body = (
        '<main class="wrap narrow">%s'
        '<h1 class="page-h1">%s</h1><p class="page-lede">%s</p>'
        '<div class="checker"><label for="region">%s</label>'
        '<select id="region">%s</select>'
        '<p class="hint" id="localTz"></p>'
        '<div style="margin-top:22px"><div class="countdown-big" id="cd" aria-live="off">—</div>'
        '<p class="hint" id="unlockLine" style="font-size:15px"></p>'
        '<p class="hint" id="mskLine" style="font-size:15px"></p>'
        '<p class="hint" id="localLine" style="font-size:15px"></p></div></div>'
        '<section class="prose"><h2 class="sec">%s</h2><ul>%s</ul></section>'
        '<p class="data-line">%s</p></main>'
        % (crumbs_html(lang, [(home, home_path), ("GTA 6", hub_path), (c["h1"], None)]),
           c["h1"], c["lede"], c["label"], opts, c["note_h"], notes, c["sources"])
    )
    js = """
<script>
(function () {
  var STR = %s;
  var sel = document.getElementById('region');
  var cd = document.getElementById('cd');
  var unlockLine = document.getElementById('unlockLine');
  var mskLine = document.getElementById('mskLine');
  var localLine = document.getElementById('localLine');
  try {
    var mine = Intl.DateTimeFormat().resolvedOptions().timeZone;
    document.getElementById('localTz').textContent = STR.local_label + ': ' + mine;
    for (var i = 0; i < sel.options.length; i++) {
      if (sel.options[i].value === mine) { sel.selectedIndex = i; break; }
    }
  } catch (e) {}
  function tzOffsetMs(tz, utcMs) {
    // Offset of tz at utcMs, via Intl formatToParts.
    var dtf = new Intl.DateTimeFormat('en-US', { timeZone: tz, year: 'numeric',
      month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit',
      second: '2-digit', hourCycle: 'h23' });
    var parts = dtf.formatToParts(new Date(utcMs));
    var get = function (t) { for (var k = 0; k < parts.length; k++) if (parts[k].type === t) return parseInt(parts[k].value, 10); return 0; };
    var asUTC = Date.UTC(get('year'), get('month') - 1, get('day'), get('hour'), get('minute'), get('second'));
    return asUTC - Math.floor(utcMs / 1000) * 1000;
  }
  function targetMs(tz) {
    // Nov 19, 2026 00:00 wall time in tz.
    var guess = Date.UTC(2026, 10, 19, 0, 0, 0);
    return guess - tzOffsetMs(tz, guess);
  }
  function fmt(ms, tz) {
    try {
      return new Intl.DateTimeFormat(STR.locale, { timeZone: tz, weekday: 'short',
        month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit',
        timeZoneName: 'short' }).format(new Date(ms));
    } catch (e) { return new Date(ms).toString(); }
  }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function tick() {
    var tz = sel.value;
    var target = targetMs(tz);
    var now = Date.now();
    var label = sel.options[sel.selectedIndex].textContent;
    unlockLine.textContent = STR.unlocks.replace('%%s', label);
    mskLine.textContent = STR.moscow.replace('%%s', fmt(target, 'Europe/Moscow'));
    try { localLine.textContent = STR.local.replace('%%s', fmt(target)); } catch (e) {}
    var diff = target - now;
    if (diff <= 0) { cd.textContent = STR.released; return; }
    var s = Math.floor(diff / 1000);
    var d = Math.floor(s / 86400);
    var h = Math.floor((s %% 86400) / 3600);
    var m = Math.floor((s %% 3600) / 60);
    var sec = s %% 60;
    cd.innerHTML = d + '<span class="unit">d</span>' + pad(h) + '<span class="unit">h</span>' +
      pad(m) + '<span class="unit">m</span>' + pad(sec) + '<span class="unit">s</span>';
  }
  sel.addEventListener('change', tick);
  tick();
  setInterval(tick, 1000);
})();
</script>
""" % ('{"unlocks": "%s", "moscow": "%s", "local": "%s", "released": "%s", "local_label": "%s", "locale": "%s"}'
       % (c["unlocks"], c["moscow"], c["local"], c["released"], c["local_label"],
          "en-US" if lang == "en" else "ru-RU"))
    jl = [breadcrumb_jsonld(lang, [(home, home_path), ("GTA 6", hub_path), (c["h1"], "/gta-6/launch-countdown/" if lang == "en" else "/ru/gta-6/launch-countdown/")]),
          webapp_jsonld(lang, c["h1"], "/gta-6/launch-countdown/" if lang == "en" else "/ru/gta-6/launch-countdown/", c["desc"])]
    return tool_page(lang, "gta-6", "launch-countdown", c["title"], c["desc"], body + js,
                     None, jl)


# ---------------------------------------------------------------- editions
EDITIONS = {
    "en": {
        "title": "GTA 6 Editions Compared — Standard vs Ultimate | BuffForge",
        "desc": "GTA 6 Standard $79.99 vs Ultimate $99.99 — only what Take-Two and the official stores actually say. No PC edition at launch.",
        "h1": "GTA 6 Editions Compared",
        "lede": "Two editions, both on PS5 and Xbox Series X|S. Prices below are the US suggested retail prices announced by Take-Two. Regional prices differ — check your store.",
        "rows": [
            ("Price (US MSRP)", "<b>Standard — $79.99</b>", "<b>Ultimate — $99.99</b>"),
            ("Platforms", "PS5, PS5 Pro, Xbox Series X|S", "PS5, PS5 Pro, Xbox Series X|S"),
            ("Pre-order bonus", "Vintage Vice City Pack when you buy before Nov 20, 2026", "Vintage Vice City Pack when you buy before Nov 20, 2026"),
            ("Digital pre-order", "One month of GTA+ (per official announcement)", "One month of GTA+ (per official announcement)"),
            ("PC version", "No PC version at launch", "No PC version at launch"),
        ],
        "warn_h": "About the Ultimate edition",
        "warn": "Take-Two has not published a full, itemised list of everything in the Ultimate edition that we can verify here, so we do not invent one. Before you pay the extra $20, open the official PlayStation or Xbox store page and read the edition contents there.",
        "sources": "Sources: Take-Two pre-order announcement, PlayStation Store, checked Nov 13, 2026. Prices are US MSRP.",
        "std": "Standard", "ult": "Ultimate",
    },
    "ru": {
        "title": "Сравнение изданий GTA 6 — Standard и Ultimate | BuffForge",
        "desc": "GTA 6 Standard за $79.99 и Ultimate за $99.99 — только то, что официально объявили Take-Two и магазины. Версии для ПК на старте нет.",
        "h1": "Сравнение изданий GTA 6",
        "lede": "Два издания — оба на PS5 и Xbox Series X|S. Цены ниже — рекомендованные цены для США, объявленные Take-Two. В других регионах цены отличаются — смотрите свой магазин.",
        "rows": [
            ("Цена (США)", "<b>Standard — $79.99</b>", "<b>Ultimate — $99.99</b>"),
            ("Платформы", "PS5, PS5 Pro, Xbox Series X|S", "PS5, PS5 Pro, Xbox Series X|S"),
            ("Бонус предзаказа", "Набор Vintage Vice City Pack при покупке до 20 ноября 2026 года", "Набор Vintage Vice City Pack при покупке до 20 ноября 2026 года"),
            ("Цифровой предзаказ", "Месяц GTA+ (по официальному объявлению)", "Месяц GTA+ (по официальному объявлению)"),
            ("Версия для ПК", "На старте версии для ПК нет", "На старте версии для ПК нет"),
        ],
        "warn_h": "Про издание Ultimate",
        "warn": "Take-Two не опубликовала полный детализированный список содержимого Ultimate, который мы могли бы проверить, поэтому мы его не выдумываем. Прежде чем доплачивать $20, откройте официальную страницу издания в PlayStation Store или Xbox и прочитайте состав там.",
        "sources": "Источники: объявление Take-Two о предзаказах, PlayStation Store, проверено 13 ноября 2026 года. Цены — рекомендованные для США.",
        "std": "Standard", "ult": "Ultimate",
    },
}


def editions_page(lang):
    c = EDITIONS[lang]
    home = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    hub_path = "/gta-6/" if lang == "en" else "/ru/gta-6/"
    rows = "".join("<tr><th>%s</th><td>%s</td><td>%s</td></tr>" % r for r in c["rows"])
    body = (
        '<main class="wrap narrow">%s'
        '<h1 class="page-h1">%s</h1><p class="page-lede">%s</p>'
        '<table class="fact-table"><tr><th></th><th>%s</th><th>%s</th></tr>%s</table>'
        '<div class="note-box amber"><h3>%s</h3><p>%s</p></div>'
        '<p class="data-line">%s</p></main>'
        % (crumbs_html(lang, [(home, home_path), ("GTA 6", hub_path), (c["h1"], None)]),
           c["h1"], c["lede"], c["std"], c["ult"], rows, c["warn_h"], c["warn"], c["sources"])
    )
    jl = [breadcrumb_jsonld(lang, [(home, home_path), ("GTA 6", hub_path), (c["h1"], "/gta-6/editions/" if lang == "en" else "/ru/gta-6/editions/")]),
          webapp_jsonld(lang, c["h1"], "/gta-6/editions/" if lang == "en" else "/ru/gta-6/editions/", c["desc"])]
    return tool_page(lang, "gta-6", "editions", c["title"], c["desc"], body, None, jl)


# ---------------------------------------------------------------- compatibility
DEVICES = [
    ("ps5", "PlayStation 5", "PlayStation 5", "yes"),
    ("ps5pro", "PlayStation 5 Pro", "PlayStation 5 Pro", "yes"),
    ("ps5de", "PlayStation 5 Digital Edition", "PlayStation 5 Digital Edition", "yes"),
    ("xsx", "Xbox Series X", "Xbox Series X", "yes"),
    ("xss", "Xbox Series S", "Xbox Series S", "yes"),
    ("ps4", "PlayStation 4", "PlayStation 4", "no"),
    ("ps4pro", "PlayStation 4 Pro", "PlayStation 4 Pro", "no"),
    ("xone", "Xbox One", "Xbox One", "no"),
    ("xonex", "Xbox One X", "Xbox One X", "no"),
    ("pc", "PC", "ПК", "pc"),
]

COMPAT = {
    "en": {
        "title": "Can My Console Run GTA 6? — BuffForge",
        "desc": "GTA 6 runs on PS5, PS5 Pro, and Xbox Series X|S. No PS4 or Xbox One version, and no PC version has been officially announced.",
        "h1": "Can My Console Run GTA 6?",
        "lede": "Pick your device. GTA 6 launches Nov 19, 2026 on PS5 (including Pro) and Xbox Series X|S only.",
        "yes": "Yes — it runs.",
        "yes_p": "%s is a launch platform for GTA 6. You can buy the Standard ($79.99) or Ultimate ($99.99) edition.",
        "no": "No — there is no version for it.",
        "no_p": "Rockstar has not released GTA 6 for %s. There is no PS4 or Xbox One version (PlayStation official).",
        "pc": "No PC version has been announced.",
        "pc_p": "Rockstar has not announced a PC version of GTA 6, and there is no official PC system requirement. System requirement tables circulating online are not Rockstar's — do not treat them as official.",
        "table_h": "All devices at a glance",
        "th_dev": "Device", "th_verdict": "Verdict",
        "v_yes": "Playable", "v_no": "Not playable", "v_pc": "Not announced",
        "sources": "Sources: Rockstar Games official newswire, PlayStation official support, checked Nov 13, 2026.",
    },
    "ru": {
        "title": "На чём можно играть в GTA 6? — BuffForge",
        "desc": "GTA 6 работает на PS5, PS5 Pro и Xbox Series X|S. Версии для PS4 и Xbox One нет, а версия для ПК официально не анонсирована.",
        "h1": "На чём можно играть в GTA 6?",
        "lede": "Выберите своё устройство. GTA 6 выходит 19 ноября 2026 года только на PS5 (включая Pro) и Xbox Series X|S.",
        "yes": "Да, игра работает.",
        "yes_p": "%s — платформа запуска GTA 6. Можно купить издание Standard ($79.99) или Ultimate ($99.99).",
        "no": "Нет, версии для неё нет.",
        "no_p": "Rockstar не выпускала GTA 6 для %s. Версий для PS4 и Xbox One нет (официально, PlayStation).",
        "pc": "Версия для ПК не анонсирована.",
        "pc_p": "Rockstar не анонсировала версию GTA 6 для ПК, официальных системных требований нет. Таблицы требований, которые ходят по интернету, — не от Rockstar, не считайте их официальными.",
        "table_h": "Все устройства — одной таблицей",
        "th_dev": "Устройство", "th_verdict": "Вердикт",
        "v_yes": "Играть можно", "v_no": "Играть нельзя", "v_pc": "Не анонсирована",
        "sources": "Источники: официальный ньюсвайр Rockstar Games, официальная поддержка PlayStation, проверено 13 ноября 2026 года.",
    },
}


def compat_page(lang):
    c = COMPAT[lang]
    home = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    hub_path = "/gta-6/" if lang == "en" else "/ru/gta-6/"
    buttons = "".join(
        '<button type="button" class="dev" data-v="%s" data-name="%s"><b>%s</b><span>%s</span></button>'
        % (v, n_en if lang == "en" else n_ru, n_en if lang == "en" else n_ru,
           {"yes": c["v_yes"], "no": c["v_no"], "pc": c["v_pc"]}[v])
        for _, n_en, n_ru, v in DEVICES)
    rows = "".join(
        "<tr><th>%s</th><td>%s</td></tr>"
        % (n_en if lang == "en" else n_ru,
           {"yes": "<b>%s</b>" % c["v_yes"], "no": "<b>%s</b>" % c["v_no"],
            "pc": "<b>%s</b>" % c["v_pc"]}[v])
        for _, n_en, n_ru, v in DEVICES)
    body = (
        '<main class="wrap narrow">%s'
        '<h1 class="page-h1">%s</h1><p class="page-lede">%s</p>'
        '<div class="dev-grid" id="devGrid">%s</div>'
        '<div class="result" id="compatResult" role="status"></div>'
        '<section class="prose"><h2 class="sec">%s</h2>'
        '<table class="fact-table"><tr><th>%s</th><th>%s</th></tr>%s</table></section>'
        '<p class="data-line">%s</p></main>'
        % (crumbs_html(lang, [(home, home_path), ("GTA 6", hub_path), (c["h1"], None)]),
           c["h1"], c["lede"], buttons, c["table_h"], c["th_dev"], c["th_verdict"], rows, c["sources"])
    )
    js = """
<script>
(function () {
  var STR = %s;
  var result = document.getElementById('compatResult');
  document.querySelectorAll('#devGrid .dev').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('#devGrid .dev').forEach(function (x) { x.classList.remove('sel'); });
      b.classList.add('sel');
      var v = b.getAttribute('data-v');
      var name = b.getAttribute('data-name');
      var cls = v === 'yes' ? 'ok' : (v === 'pc' ? 'warn' : 'bad');
      var head = v === 'yes' ? STR.yes : (v === 'pc' ? STR.pc : STR.no);
      var txt = (v === 'yes' ? STR.yes_p : (v === 'pc' ? STR.pc_p : STR.no_p)).replace('%%s', name);
      result.className = 'result ' + cls + ' show';
      result.innerHTML = '<b class="big">' + head + '</b><p>' + txt + '</p>';
    });
  });
})();
</script>
""" % ('{"yes": "%s", "yes_p": "%s", "no": "%s", "no_p": "%s", "pc": "%s", "pc_p": "%s"}'
       % (c["yes"], c["yes_p"], c["no"], c["no_p"], c["pc"], c["pc_p"]))
    jl = [breadcrumb_jsonld(lang, [(home, home_path), ("GTA 6", hub_path), (c["h1"], "/gta-6/compatibility/" if lang == "en" else "/ru/gta-6/compatibility/")]),
          webapp_jsonld(lang, c["h1"], "/gta-6/compatibility/" if lang == "en" else "/ru/gta-6/compatibility/", c["desc"])]
    return tool_page(lang, "gta-6", "compatibility", c["title"], c["desc"], body + js,
                     None, jl)


def main():
    for lang in ("en", "ru"):
        prefix = "" if lang == "en" else "ru/"
        write(prefix + "gta-6/storage-check/index.html", storage_page(lang))
        write(prefix + "gta-6/launch-countdown/index.html", countdown_page(lang))
        write(prefix + "gta-6/editions/index.html", editions_page(lang))
        write(prefix + "gta-6/compatibility/index.html", compat_page(lang))
    print("tools build done")


if __name__ == "__main__":
    main()

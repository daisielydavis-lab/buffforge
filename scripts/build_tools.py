#!/usr/bin/env python3
"""GTA 6 official-facts tools (EN + RU) and the PS5 frame-interpolation guide.

Run:  cd <repo root> && python3 scripts/build_tools.py
Uses only verified official facts (see spec section 10.2):
Re-checked 22 Nov 2026 against Rockstar, PlayStation and Xbox store pages:
- Out since 19 Nov 2026 on PS5 (+Pro) and Xbox Series X|S. No official PC SKU.
- PlayStation still says a minimum of 212 GB free space. That is not an exact install size.
- Standard $79.99 / Ultimate $99.99 remain US MSRP labels. Regional prices differ.
- The pre-order window closed 20 Nov 2026. Vintage Vice City Pack is a separate
  US store add-on at $4.99 and requires the game.
No speculative PC spec table. No single Moscow unlock time.
"""
import json
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
        "title": "GTA 6 Storage Check — Will 212 GB Fit? — BuffForge",
        "desc": "PlayStation asks for a minimum of 212 GB free for GTA 6. Enter your free space and see if you meet that minimum. It is not a confirmed exact install size.",
        "h1": "GTA 6 Storage Check",
        "lede": "PlayStation still says to clear a <b>minimum of 212 GB</b> of free space. That is the store’s free-space line, not a Rockstar install size. Enter what your console shows as free.",
        "label": "How much free space do you have? (GB)",
        "hint": "On PS5: Settings → Storage. On Xbox: My games &amp; apps → Manage → Free up space.",
        "platform_label": "Your console",
        "ps5": "PlayStation 5 / PS5 Pro",
        "xbox": "Xbox Series X|S",
        "check": "Check my space",
        "fits": "Enough free space.",
        "fits_p": "You have %s GB free. That is %s GB above the 212 GB minimum PlayStation lists. This is not a confirmed exact install size. Leave room for updates.",
        "short": "Below the 212 GB minimum.",
        "short_p": "You need %s GB more free space to reach the 212 GB PlayStation lists. Delete a game or two, or move games to external storage where your console allows it.",
        "exact": "Exactly the 212 GB minimum.",
        "exact_p": "You have 212 GB free, which meets the PlayStation minimum with nothing above it. That is still not a confirmed exact install size.",
        "preload_h": "What 212 GB means",
        "preload": [
            "<b>212 GB</b> is the minimum free space on the PlayStation game page. Rockstar has not published a separate final install size.",
            "<b>Preload already happened.</b> PlayStation said digital preload for pre-orders started 10 Nov 2026 at local midnight. The game has been available since 19 Nov 2026.",
            "<b>Xbox:</b> this page does not publish a Moscow preload clock. Use the time on your own Xbox store listing.",
        ],
        "sources": "Source: PlayStation game page for Grand Theft Auto VI, “minimum of 212GB”, checked 22 Nov 2026. The PlayStation support article fetched the same day did not repeat the 212 GB line.",
    },
    "ru": {
        "title": "Проверка места под GTA 6 — хватит ли 212 ГБ — BuffForge",
        "desc": "PlayStation просит минимум 212 ГБ свободного места под GTA 6. Введите, сколько свободно, и проверьте этот минимум. Это не точный размер установки.",
        "h1": "Проверка места под GTA 6",
        "lede": "На странице игры PlayStation по-прежнему написано: освободите <b>минимум 212 ГБ</b>. Это свободное место в магазине, а не размер установки от Rockstar. Введите число, которое показывает консоль.",
        "label": "Сколько свободного места у вас? (ГБ)",
        "hint": "На PS5: Настройки → Хранилище. На Xbox: Мои игры и приложения → Управление → Освободить место.",
        "platform_label": "Ваша консоль",
        "ps5": "PlayStation 5 / PS5 Pro",
        "xbox": "Xbox Series X|S",
        "check": "Проверить место",
        "fits": "Свободного места достаточно.",
        "fits_p": "Свободно %s ГБ. Это на %s ГБ выше минимума 212 ГБ, который указывает PlayStation. Точный размер установки не подтверждён. Оставьте запас под обновления.",
        "short": "Меньше минимума 212 ГБ.",
        "short_p": "Чтобы набрать 212 ГБ, нужно освободить ещё %s ГБ. Удалите пару игр или перенесите их на внешний накопитель, если консоль это позволяет.",
        "exact": "Ровно минимум 212 ГБ.",
        "exact_p": "Свободно ровно 212 ГБ — минимум PlayStation, без запаса сверху. Это всё ещё не подтверждённый точный размер установки.",
        "preload_h": "Что значит 212 ГБ",
        "preload": [
            "<b>212 ГБ</b> — минимум свободного места на странице игры PlayStation. Отдельный итоговый размер установки Rockstar не публиковала.",
            "<b>Предзагрузка уже была.</b> PlayStation писала, что для предзаказов она началась 10 ноября 2026 года в местную полночь. Игра доступна с 19 ноября 2026 года.",
            "<b>Xbox:</b> московские часы предзагрузки мы не публикуем. Смотрите время в своём магазине Xbox.",
        ],
        "sources": "Источник: страница Grand Theft Auto VI на PlayStation, «minimum of 212GB», проверено 22 ноября 2026 года. В статье поддержки PlayStation, открытой в тот же день, строки про 212 ГБ не было.",
    },
}


def storage_page(lang):
    c = STORAGE[lang]
    home = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    hub_path = "/gta-6/" if lang == "en" else "/ru/gta-6/"
    preload = "".join("<li>%s</li>" % x for x in c["preload"])
    body = (
        '<main id="main" class="wrap narrow">%s'
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
        % (crumbs_html(lang, [("GTA 6", hub_path), (c["h1"].replace("&amp;", "&"), None)]),
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
    function gb(n) {
      var c = Math.ceil(n * 10) / 10;
      if (c < 0.1) c = 0.1;
      return (c %% 1 === 0) ? String(c) : c.toFixed(1);
    }
    if (remain > 0) { result.className = 'result ok show';
      result.innerHTML = '<b class="big">' + STR.fits + '</b><p>' +
        STR.fits_p.replace('%%s', free).replace('%%s', gb(remain)) + '</p>' +
        '<div class="bar"><i style="width:' + Math.min(100, NEED / free * 100) + '%%"></i></div>';
    } else if (remain === 0) { result.className = 'result warn show';
      result.innerHTML = '<b class="big">' + STR.exact + '</b><p>' + STR.exact_p + '</p>';
    } else { result.className = 'result bad show';
      result.innerHTML = '<b class="big">' + STR.short + '</b><p>' +
        STR.short_p.replace('%%s', gb(-remain)) + '</p>';
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
        "title": "GTA 6 Launch Time by Store Region — BuffForge",
        "desc": "GTA 6 unlocked on 19 Nov 2026 at local midnight. Pick a store region and see that unlock time, plus how long it has been out.",
        "h1": "GTA 6 launch time by store region",
        "lede": "GTA 6 <b>unlocked on 19 Nov 2026 at local midnight</b> in each store region. Rockstar’s site now says “Now Available” on PlayStation 5 and Xbox Series X|S. There is still no single official Moscow unlock time.",
        "label": "Store region",
        "local_label": "Your time zone",
        "unlocks": "Unlocks 19 Nov 2026, 00:00 in %s",
        "unlocked_at": "Unlocked 19 Nov 2026, 00:00 in %s",
        "moscow": "That instant is %s in Moscow (MSK, UTC+3).",
        "local": "In your local time: %s.",
        "released": "Unlocked",
        "elapsed_unit_d": "d",
        "note_h": "What is confirmed — and what is not",
        "notes": [
            "<b>Out now:</b> Rockstar’s VI page says “Now Available” for PlayStation 5 and Xbox Series X|S. The newswire item is dated 19 Nov 2026. No official PC version.",
            "<b>Not one Moscow minute:</b> unlock was local midnight in the store region, so Moscow time still differs by region.",
            "<b>After unlock:</b> the clock above is time since that midnight. It does not count backward.",
        ],
        "sources": "Sources: rockstargames.com/VI (“Now Available”, 19 Nov 2026) and PlayStation support (midnight local time on 19 Nov 2026). Checked 22 Nov 2026.",
    },
    "ru": {
        "title": "Время выхода GTA 6 по региону магазина — BuffForge",
        "desc": "GTA 6 открылась 19 ноября 2026 года в местную полночь. Выберите регион магазина: момент открытия и сколько времени уже прошло.",
        "h1": "Время выхода GTA 6 по региону магазина",
        "lede": "GTA 6 <b>открылась 19 ноября 2026 года в местную полночь</b> региона магазина. На сайте Rockstar сейчас «Now Available» для PlayStation 5 и Xbox Series X|S. Единого официального московского времени по-прежнему нет.",
        "label": "Регион магазина",
        "local_label": "Ваш часовой пояс",
        "unlocks": "Открытие 19 ноября 2026 года в 00:00, регион: %s",
        "unlocked_at": "Открылась 19 ноября 2026 года в 00:00, регион: %s",
        "moscow": "Этот момент по Москве (МСК, UTC+3): %s.",
        "local": "В вашем местном времени: %s.",
        "released": "Уже открыта",
        "elapsed_unit_d": "д",
        "note_h": "Что подтверждено, а что нет",
        "notes": [
            "<b>Уже вышла:</b> страница Rockstar VI пишет «Now Available» для PlayStation 5 и Xbox Series X|S. Запись ньюсвайра датирована 19 ноября 2026 года. Версии для ПК нет.",
            "<b>Не одна минута для Москвы:</b> открытие было в местную полночь региона магазина, поэтому московское время по-прежнему зависит от региона.",
            "<b>После открытия:</b> часы выше считают время с той полуночи. Обратного отсчёта нет.",
        ],
        "sources": "Источники: rockstargames.com/VI («Now Available», 19 ноября 2026) и поддержка PlayStation (местная полночь 19 ноября 2026). Проверено 22 ноября 2026 года.",
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
        '<main id="main" class="wrap narrow">%s'
        '<h1 class="page-h1">%s</h1><p class="page-lede">%s</p>'
        '<div class="checker"><label for="region">%s</label>'
        '<select id="region">%s</select>'
        '<p class="hint" id="localTz"></p>'
        '<div style="margin-top:22px"><div class="countdown-big" id="cd" aria-live="off">—</div>'
        '<p class="hint" id="unlockLine" style="font-size:var(--fs-body)"></p>'
        '<p class="hint" id="mskLine" style="font-size:var(--fs-body)"></p>'
        '<p class="hint" id="localLine" style="font-size:var(--fs-body)"></p></div></div>'
        '<section class="prose"><h2 class="sec">%s</h2><ul>%s</ul></section>'
        '<p class="data-line">%s</p></main>'
        % (crumbs_html(lang, [("GTA 6", hub_path), (c["h1"], None)]),
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
    mskLine.textContent = STR.moscow.replace('%%s', fmt(target, 'Europe/Moscow'));
    try { localLine.textContent = STR.local.replace('%%s', fmt(target)); } catch (e) {}
    var diff = target - now;
    var past = diff <= 0;
    unlockLine.textContent = (past ? STR.unlocked_at : STR.unlocks).replace('%%s', label);
    var s = Math.floor(Math.abs(diff) / 1000);
    var d = Math.floor(s / 86400);
    var h = Math.floor((s %% 86400) / 3600);
    var m = Math.floor((s %% 3600) / 60);
    var sec = s %% 60;
    var clock = d + '<span class="unit">' + STR.unit_d + '</span>' + pad(h) + '<span class="unit">h</span>' +
      pad(m) + '<span class="unit">m</span>' + pad(sec) + '<span class="unit">s</span>';
    cd.innerHTML = past ? (STR.released + ' ' + clock) : clock;
  }
  sel.addEventListener('change', tick);
  tick();
  setInterval(tick, 1000);
})();
</script>
""" % ('{"unlocks": "%s", "unlocked_at": "%s", "moscow": "%s", "local": "%s", "released": "%s", "unit_d": "%s", "local_label": "%s", "locale": "%s"}'
       % (c["unlocks"], c["unlocked_at"], c["moscow"], c["local"], c["released"], c["elapsed_unit_d"],
          c["local_label"], "en-US" if lang == "en" else "ru-RU"))
    jl = [breadcrumb_jsonld(lang, [(home, home_path), ("GTA 6", hub_path), (c["h1"], "/gta-6/launch-countdown/" if lang == "en" else "/ru/gta-6/launch-countdown/")]),
          webapp_jsonld(lang, c["h1"], "/gta-6/launch-countdown/" if lang == "en" else "/ru/gta-6/launch-countdown/", c["desc"])]
    return tool_page(lang, "gta-6", "launch-countdown", c["title"], c["desc"], body + js,
                     None, jl)


# ---------------------------------------------------------------- editions
PS_GAME = "https://www.playstation.com/en-us/games/grand-theft-auto-vi/"
XBOX_PACK = "https://www.xbox.com/en-US/games/store/grand-theft-auto-vi-vintage-vice-city-pack/9plvssh8849x"
PS_PACK = "https://store.playstation.com/en-us/product/EP1004-PPSA01547_00-CONTENTPACK00001"

EDITIONS = {
    "en": {
        "title": "GTA 6 Editions Compared — Standard vs Ultimate | BuffForge",
        "desc": "GTA 6 Standard $79.99 vs Ultimate $99.99, US store prices. The pre-order window has closed. Ultimate contents follow the PlayStation page.",
        "h1": "GTA 6 Editions Compared",
        "lede": "Standard and Ultimate are on PS5 and Xbox Series X|S. <b>$79.99</b> and <b>$99.99</b> are US prices. Other regions differ. The buy-before-20-Nov window has closed.",
        "when": "Which purchase are you checking?",
        "opt_now": "Buying now",
        "opt_before": "Digital edition bought before 20 Nov 2026",
        "now_h": "Buying now",
        "now_p": "The pre-order window closed on 20 Nov 2026. A purchase now does not include the Vintage Vice City Pack or the free month of GTA+. The pack is a separate add-on.",
        "before_h": "Bought before 20 Nov 2026",
        "before_p": "If the digital Standard or Ultimate edition was bought before 20 Nov 2026, the offer included the Vintage Vice City Pack and one month of GTA+. PlayStation says that month must be claimed by 31 Mar 2027. This page cannot see your account.",
        "rows": [
            ("Price (US)", "<b>Standard — $79.99</b>", "<b>Ultimate — $99.99</b>"),
            ("Platforms", "PS5, PS5 Pro, Xbox Series X|S", "PS5, PS5 Pro, Xbox Series X|S"),
            ("PC version", "Not announced", "Not announced"),
        ],
        "std": "Standard", "ult": "Ultimate",
        "pack_h": "Vintage Vice City Pack",
        "pack_p": "Official add-on, released 20 Nov 2026. The US Xbox store and the US PlayStation Store both list <b>$4.99</b>. It requires Grand Theft Auto VI, sold separately. That price is the US store price, not a worldwide price, and it does not mean you already own the pack.",
        "pack_items": [
            "’55 Vapid Stanier, stored at the Shore Court garage near Ocean Beach",
            "Outfits and hairstyles for Jason and Lucia",
            "A weapon pattern for most guns",
        ],
        "ult_h": "What PlayStation lists in Ultimate",
        "ult_p": "Item names below are from the US PlayStation game page. Descriptions there are longer. Nothing else is added.",
        "ult_groups": [
            ("Vehicles and garages", [
                "’95 Grotti Cheetah",
                "Jason’s safehouse vehicles: Dinka Enduro, Crest Kayak",
                "Shitzu Squalo",
                "’67 Vapid Dominator Buggy and the Paradise Garage",
            ]),
            ("Weapons", [
                "Hawk and Little Morgan revolvers",
                "Personalized Girardi ES9 and Klose K17",
            ]),
            ("Looks", [
                "Vice City Style outfits, hairstyles and tattoos",
                "Goodtime Gear",
            ]),
            ("Special commission", [
                "Ganado Retro Build",
                "Classic car collection",
            ]),
            ("Shops only in Ultimate", [
                "Rideout Customs",
                "Sara’s Unisex Salon",
                "Stock 305",
                "Electric Fang Tattoo",
                "One-Eyed Willie’s",
            ]),
        ],
        "sources": "Sources, checked 22 Nov 2026: PlayStation game page (Ultimate list and the pre-order GTA+ FAQ), US Xbox store and US PlayStation Store for the pack ($4.99, 20 Nov 2026). Prices are US store prices.",
    },
    "ru": {
        "title": "Сравнение изданий GTA 6 — Standard и Ultimate | BuffForge",
        "desc": "GTA 6 Standard $79.99 и Ultimate $99.99 — цены магазина США. Окно предзаказа закрыто. Состав Ultimate — со страницы PlayStation.",
        "h1": "Сравнение изданий GTA 6",
        "lede": "Standard и Ultimate выходят на PS5 и Xbox Series X|S. <b>$79.99</b> и <b>$99.99</b> — цены США. В других регионах цены другие. Окно «купить до 20 ноября» закрыто.",
        "when": "Какую покупку проверяете?",
        "opt_now": "Покупаю сейчас",
        "opt_before": "Цифровое издание куплено до 20 ноября 2026",
        "now_h": "Покупка сейчас",
        "now_p": "Окно предзаказа закрылось 20 ноября 2026 года. Покупка сейчас не включает Vintage Vice City Pack и бесплатный месяц GTA+. Набор продаётся отдельно.",
        "before_h": "Куплено до 20 ноября 2026",
        "before_p": "Если цифровое Standard или Ultimate купили до 20 ноября 2026 года, в предложение входили Vintage Vice City Pack и месяц GTA+. PlayStation пишет, что месяц нужно получить до 31 марта 2027 года. Эта страница не видит ваш аккаунт.",
        "rows": [
            ("Цена (США)", "<b>Standard — $79.99</b>", "<b>Ultimate — $99.99</b>"),
            ("Платформы", "PS5, PS5 Pro, Xbox Series X|S", "PS5, PS5 Pro, Xbox Series X|S"),
            ("Версия для ПК", "Не анонсирована", "Не анонсирована"),
        ],
        "std": "Standard", "ult": "Ultimate",
        "pack_h": "Vintage Vice City Pack",
        "pack_p": "Официальное дополнение, дата выхода 20 ноября 2026 года. В магазине Xbox США и в PlayStation Store США цена <b>$4.99</b>. Нужна Grand Theft Auto VI, она продаётся отдельно. Это цена магазина США, не мировая, и она не значит, что набор уже у вас.",
        "pack_items": [
            "’55 Vapid Stanier и гараж Shore Court у Ocean Beach",
            "Одежда и причёски для Джейсона и Люсии",
            "Узор для большинства видов оружия",
        ],
        "ult_h": "Что PlayStation указывает в Ultimate",
        "ult_p": "Названия ниже — со страницы игры в американском PlayStation. Описания там длиннее. Лишнего не добавлено.",
        "ult_groups": [
            ("Транспорт и гаражи", [
                "’95 Grotti Cheetah",
                "Транспорт убежища Джейсона: Dinka Enduro, Crest Kayak",
                "Shitzu Squalo",
                "’67 Vapid Dominator Buggy и Paradise Garage",
            ]),
            ("Оружие", [
                "Револьверы Hawk и Little Morgan",
                "Именные Girardi ES9 и Klose K17",
            ]),
            ("Внешность", [
                "Наряды, причёски и тату Vice City Style",
                "Goodtime Gear",
            ]),
            ("Особый заказ", [
                "Ganado Retro Build",
                "Коллекция классических машин",
            ]),
            ("Магазины только в Ultimate", [
                "Rideout Customs",
                "Sara’s Unisex Salon",
                "Stock 305",
                "Electric Fang Tattoo",
                "One-Eyed Willie’s",
            ]),
        ],
        "sources": "Источники, проверено 22 ноября 2026 года: страница игры PlayStation (список Ultimate и FAQ про месяц GTA+ за предзаказ), магазин Xbox США и PlayStation Store США для набора ($4.99, 20 ноября 2026). Цены — магазина США.",
    },
}


def editions_page(lang):
    c = EDITIONS[lang]
    home = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    hub_path = "/gta-6/" if lang == "en" else "/ru/gta-6/"
    rows = "".join("<tr><th>%s</th><td>%s</td><td>%s</td></tr>" % r for r in c["rows"])
    pack_items = "".join("<li>%s</li>" % x for x in c["pack_items"])
    groups = []
    for title, items in c["ult_groups"]:
        groups.append("<h3>%s</h3><ul>%s</ul>" % (title, "".join("<li>%s</li>" % i for i in items)))
    body = (
        '<main id="main" class="wrap narrow">%s'
        '<h1 class="page-h1">%s</h1><p class="page-lede">%s</p>'
        '<div class="checker"><label for="buyWhen">%s</label>'
        '<select id="buyWhen"><option value="now">%s</option><option value="before">%s</option></select>'
        '<div class="result" id="editionResult" role="status"></div></div>'
        '<table class="fact-table"><tr><th></th><th>%s</th><th>%s</th></tr>%s</table>'
        '<section class="prose"><h2 class="sec">%s</h2><p>%s</p>'
        '<p><a href="%s" target="_blank" rel="noopener noreferrer">Xbox</a> · '
        '<a href="%s" target="_blank" rel="noopener noreferrer">PlayStation Store</a></p>'
        '<ul>%s</ul>'
        '<h2 class="sec">%s</h2><p>%s</p>'
        '<p><a href="%s" target="_blank" rel="noopener noreferrer">PlayStation</a></p>%s</section>'
        '<p class="data-line">%s</p></main>'
        % (crumbs_html(lang, [("GTA 6", hub_path), (c["h1"], None)]),
           c["h1"], c["lede"], c["when"], c["opt_now"], c["opt_before"],
           c["std"], c["ult"], rows,
           c["pack_h"], c["pack_p"], XBOX_PACK, PS_PACK, pack_items,
           c["ult_h"], c["ult_p"], PS_GAME, "".join(groups), c["sources"])
    )
    js = """
<script>
(function () {
  var STR = %s;
  var sel = document.getElementById('buyWhen');
  var result = document.getElementById('editionResult');
  function show() {
    var now = sel.value === 'now';
    result.className = 'result ' + (now ? 'warn' : 'ok') + ' show';
    result.innerHTML = '<b class="big">' + (now ? STR.now_h : STR.before_h) + '</b><p>' +
      (now ? STR.now_p : STR.before_p) + '</p>';
  }
  sel.addEventListener('change', show);
  show();
})();
</script>
""" % ('{"now_h": %s, "now_p": %s, "before_h": %s, "before_p": %s}'
       % (json.dumps(c["now_h"]), json.dumps(c["now_p"]), json.dumps(c["before_h"]), json.dumps(c["before_p"])))
    jl = [breadcrumb_jsonld(lang, [(home, home_path), ("GTA 6", hub_path), (c["h1"], "/gta-6/editions/" if lang == "en" else "/ru/gta-6/editions/")]),
          webapp_jsonld(lang, c["h1"], "/gta-6/editions/" if lang == "en" else "/ru/gta-6/editions/", c["desc"])]
    return tool_page(lang, "gta-6", "editions", c["title"], c["desc"], body + js, None, jl)


# ---------------------------------------------------------------- compatibility
DEVICES = [
    ("ps5", "PlayStation 5", "PlayStation 5", "yes"),
    ("ps5pro", "PlayStation 5 Pro", "PlayStation 5 Pro", "yes"),
    ("ps5de", "PlayStation 5 Digital Edition", "PlayStation 5 Digital Edition", "yes"),
    ("xsx", "Xbox Series X", "Xbox Series X", "yes"),
    ("xss", "Xbox Series S", "Xbox Series S", "yes"),
    ("ps4", "PlayStation 4", "PlayStation 4", "no"),
    ("ps4pro", "PlayStation 4 Pro", "PlayStation 4 Pro", "no"),
    ("xone", "Xbox One", "Xbox One", "cloud"),
    ("xonex", "Xbox One X", "Xbox One X", "cloud"),
    ("pc", "PC", "ПК", "pc"),
]

COMPAT = {
    "en": {
        "title": "Can My Console Run GTA 6? — BuffForge",
        "desc": "GTA 6 is available on PS5, PS5 Pro, and Xbox Series X|S. No PS4 version. Xbox One plays it via Xbox Cloud Gaming (Xbox Wire, Nov 10, 2026). No announced PC version.",
        "h1": "Can My Console Run GTA 6?",
        "lede": "Pick your device. GTA 6 has been available since 19 Nov 2026 on PS5 (including Pro) and Xbox Series X|S. Xbox One plays it through Xbox Cloud Gaming. PC is not announced.",
        "yes": "Yes — it runs.",
        "yes_p": "%s can play GTA 6. US store prices are Standard $79.99 and Ultimate $99.99. Other regions differ.",
        "no": "No — there is no version for it.",
        "no_p": "Rockstar has not released GTA 6 for %s. There is no PS4 version (PlayStation official).",
        "pc": "PC version not officially announced.",
        "pc_p": "Rockstar has not announced a PC version of GTA 6, and there is no official PC system requirement. System requirement tables circulating online are not Rockstar's — do not treat them as official.",
        "cloud": "Yes — via Xbox Cloud Gaming.",
        "cloud_p": "There is no native Xbox One version. Xbox Wire (10 Nov 2026) said GTA 6 is playable on Xbox One through Xbox Cloud Gaming from 1am ET on 19 Nov 2026, with Xbox Series S graphics settings. The game is purchased separately. This page has not re-tested cloud play after launch.",
        "table_h": "All devices at a glance",
        "th_dev": "Device", "th_verdict": "Verdict",
        "v_yes": "Playable", "v_no": "Not playable", "v_pc": "Not announced",
        "v_cloud": "Playable via cloud",
        "sources": "Sources: Rockstar VI page (Now Available, PS5 and Xbox Series X|S only), PlayStation game page (PS4 not playable; released 19 Nov 2026), Xbox Wire 10 Nov 2026 for cloud. Checked 22 Nov 2026. No official PC requirements were on those pages.",
    },
    "ru": {
        "title": "На чём можно играть в GTA 6? — BuffForge",
        "desc": "GTA 6 доступна на PS5, PS5 Pro и Xbox Series X|S. Версии для PS4 нет. На Xbox One — через Xbox Cloud Gaming (Xbox Wire, 10 ноября 2026). Версия для ПК не анонсирована.",
        "h1": "На чём можно играть в GTA 6?",
        "lede": "Выберите устройство. GTA 6 доступна с 19 ноября 2026 года на PS5 (включая Pro) и Xbox Series X|S. На Xbox One — через Xbox Cloud Gaming. Версия для ПК не анонсирована.",
        "yes": "Да, игра работает.",
        "yes_p": "На %s в GTA 6 играть можно. Цены магазина США: Standard $79.99 и Ultimate $99.99. В других регионах цены другие.",
        "no": "Нет, версии для неё нет.",
        "no_p": "Rockstar не выпускала GTA 6 для %s. Версии для PS4 нет (официально, PlayStation).",
        "pc": "Версия для ПК официально не анонсирована.",
        "pc_p": "Rockstar не анонсировала версию GTA 6 для ПК, официальных системных требований нет. Таблицы требований, которые ходят по интернету, — не от Rockstar, не считайте их официальными.",
        "cloud": "Да, через Xbox Cloud Gaming.",
        "cloud_p": "Нативной версии для Xbox One нет. Xbox Wire от 10 ноября 2026 года пишет, что GTA 6 можно играть на Xbox One через Xbox Cloud Gaming с 1:00 ET 19 ноября 2026 года, с графикой Xbox Series S. Игру покупают отдельно. Облачную игру после выхода эта страница заново не проверяла.",
        "table_h": "Все устройства — одной таблицей",
        "th_dev": "Устройство", "th_verdict": "Вердикт",
        "v_yes": "Играть можно", "v_no": "Играть нельзя", "v_pc": "Не анонсирована",
        "v_cloud": "Можно через облако",
        "sources": "Источники: страница Rockstar VI (Now Available, только PS5 и Xbox Series X|S), страница игры PlayStation (на PS4 не идёт; выход 19 ноября 2026), Xbox Wire от 10 ноября 2026 про облако. Проверено 22 ноября 2026 года. Официальных требований для ПК на этих страницах не было.",
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
           {"yes": c["v_yes"], "no": c["v_no"], "pc": c["v_pc"], "cloud": c["v_cloud"]}[v])
        for _, n_en, n_ru, v in DEVICES)
    rows = "".join(
        "<tr><th>%s</th><td>%s</td></tr>"
        % (n_en if lang == "en" else n_ru,
           {"yes": "<b>%s</b>" % c["v_yes"], "no": "<b>%s</b>" % c["v_no"],
            "pc": "<b>%s</b>" % c["v_pc"], "cloud": "<b>%s</b>" % c["v_cloud"]}[v])
        for _, n_en, n_ru, v in DEVICES)
    body = (
        '<main id="main" class="wrap narrow">%s'
        '<h1 class="page-h1">%s</h1><p class="page-lede">%s</p>'
        '<div class="dev-grid" id="devGrid">%s</div>'
        '<div class="result" id="compatResult" role="status"></div>'
        '<section class="prose"><h2 class="sec">%s</h2>'
        '<table class="fact-table"><tr><th>%s</th><th>%s</th></tr>%s</table></section>'
        '<p class="data-line">%s</p></main>'
        % (crumbs_html(lang, [("GTA 6", hub_path), (c["h1"], None)]),
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
      var cls = v === 'yes' ? 'ok' : (v === 'pc' || v === 'cloud' ? 'warn' : 'bad');
      var head = v === 'yes' ? STR.yes : (v === 'pc' ? STR.pc : (v === 'cloud' ? STR.cloud : STR.no));
      var txt = (v === 'yes' ? STR.yes_p : (v === 'pc' ? STR.pc_p : (v === 'cloud' ? STR.cloud_p : STR.no_p))).replace('%%s', name);
      result.className = 'result ' + cls + ' show';
      result.innerHTML = '<b class="big">' + head + '</b><p>' + txt + '</p>';
    });
  });
})();
</script>
""" % ('{"yes": "%s", "yes_p": "%s", "no": "%s", "no_p": "%s", "pc": "%s", "pc_p": "%s", "cloud": "%s", "cloud_p": "%s"}'
       % (c["yes"], c["yes_p"], c["no"], c["no_p"], c["pc"], c["pc_p"], c["cloud"], c["cloud_p"]))
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
    from gta_fps_guide import guide_page
    write("gta-6/60-fps-ps5/index.html", guide_page("en"))
    write("ru/gta-6/60-fps-ps5/index.html", guide_page("ru"))
    print("tools build done")


if __name__ == "__main__":
    main()

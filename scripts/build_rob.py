#!/usr/bin/env python3
"""ROB RUN tools (EN + RU) and the lag guide (EN + RU). Generated static pages.

Run:  cd <repo root> && python3 scripts/build_rob.py

Facts used (re-checked 13 Nov 2026):
- Steam app 4262460, free, Early Access 4 Nov 2026, developer/publisher Kefir.
- Kefir FAQ: every 7 days plots, bases, weapons and cash are wiped into
  jail time and authority; cosmetics, name, tutorial, settings and
  accumulated jail time carry over.
- Official Telegram 11 Nov 2026: servers launched 4 Nov raided at
  20:00 MSK (17:00 UTC). Each server lives 7 days.
- Steam news 4 Nov 2026: planned fresh servers EU 17:00 UTC and
  East US 8:00 PM ET, plus extras outside those times.
Cash has no verified symbol. Calculators say "cash" / «деньги».
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import BASE, breadcrumb_jsonld, crumbs_html, page  # noqa: E402
from rob_status import rel_path as status_rel, render as status_render  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEEK_MS = 7 * 24 * 60 * 60 * 1000

ZONES = [
    ("UTC", "UTC", "UTC"),
    ("Europe/Moscow", "Moscow (MSK)", "Москва (МСК)"),
    ("America/New_York", "New York (ET)", "Нью-Йорк (ET)"),
    ("Europe/London", "London", "Лондон"),
    ("Europe/Berlin", "Berlin", "Берлин"),
    ("America/Los_Angeles", "Los Angeles (PT)", "Лос-Анджелес (PT)"),
    ("Asia/Tokyo", "Tokyo", "Токио"),
    ("local", "This device's time zone", "Часовой пояс этого устройства"),
]


def webapp_jsonld(lang, name, path, desc):
    return {"@context": "https://schema.org", "@type": "WebApplication",
            "name": name, "url": BASE + path, "inLanguage": lang,
            "description": desc, "applicationCategory": "GameApplication",
            "operatingSystem": "Any modern browser",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", rel)


def tool_page(lang, slug, title, desc, body, h1, extra_jsonld=None):
    canon = "/rob-run/%s/" % slug if lang == "en" else "/ru/rob-run/%s/" % slug
    alt = {"en": "/rob-run/%s/" % slug, "ru": "/ru/rob-run/%s/" % slug}
    home = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    hub = "/rob-run/" if lang == "en" else "/ru/rob-run/"
    jl = [
        breadcrumb_jsonld(lang, [(home, home_path), ("ROB RUN", hub), (h1, canon)]),
        webapp_jsonld(lang, h1, canon, desc),
    ]
    if extra_jsonld:
        jl.extend(extra_jsonld)
    return page(lang, title, desc, canon, alt, body, jsonld=jl, games=("rob-run",))


# ---------------------------------------------------------------- countdown
COUNT = {
    "en": {
        "title": "ROB RUN Federal Raid countdown — BuffForge",
        "desc": "Each ROB RUN server is wiped 7 days after it opens. Enter that opening time and see the Federal Raid in your time zone, Moscow time, and UTC.",
        "h1": "Federal Raid countdown",
        "lede": "The Federal Raid hits a server seven days after that server opened. Put in the opening time and this page shows the raid in your time zone, in Moscow, and in UTC.",
        "mode": "Which server?",
        "opt_custom": "I know when it opened",
        "opt_eu": "EU daily server (17:00 UTC)",
        "opt_us": "East US daily server (8:00 PM ET)",
        "opt_launch": "Servers launched 4 Nov 2026",
        "opened": "Opening date and time",
        "zone": "Time zone of that opening",
        "open_date": "Opening date",
        "hint_custom": "Seven days means 7 × 24 hours after the instant you enter.",
        "hint_eu": "Kefir’s 4 Nov note plans at least one fresh EU server at 17:00 UTC each day. Extra servers open at other times — if yours did, enter that time instead.",
        "hint_us": "The same note plans an East US server at 8:00 PM ET. Extra servers open outside that slot.",
        "hint_launch": "Steam said servers would come online at 17:00 UTC on 4 Nov 2026. Telegram set the raid for those servers at 20:00 MSK on 11 Nov, which is the same instant plus seven days.",
        "keep_h": "You keep",
        "lose_h": "You lose",
        "keep": ["Cosmetics", "Player name", "Tutorial progress", "Settings", "Accumulated jail time"],
        "lose": ["Plots", "Bases", "Weapons", "Cash — turned into jail time and authority"],
        "passed": "This raid time has passed.",
        "need": "Enter an opening date and time.",
        "open_prefix": "Opening",
        "raid_note": "Raid is seven days later.",
        "local": "Your time",
        "msk": "Moscow",
        "utc": "UTC",
        "sources": (
            'Keep / lose list: <a href="https://kefirgames.helpshift.com/hc/en/14-rob-run/faq/1346-what-is-the-federal-raid-wipe/?l=en">Kefir FAQ</a>. '
            'The <a href="https://t.me/robrungame/67">11 Nov 2026 Telegram post</a> also names vehicles, real estate, land, unlocked skill-tree items, recorded clan spending and bribes as confiscated, and a B-coin balance as kept. '
            'First raid and the 7-day server life: that post. '
            'EU 17:00 UTC and East US 8:00 PM ET, plus extra servers: <a href="https://store.steampowered.com/news/app/4262460/view/712291399099220569">Steam news, 4 Nov 2026</a>. '
            'Reviewed 13 Nov 2026.'
        ),
        "planner_link": (
            'Planning what to keep through the raid? <a href="/rob-run/wipe-planner/">Use the ROB RUN wipe planner</a> '
            'to check what resets, what carries over, and build your pre-wipe checklist.'
        ),
    },
    "ru": {
        "title": "Отсчёт до Федеральной облавы в ROB RUN — BuffForge",
        "desc": "Федеральная облава на сервере ROB RUN — через семь дней после его открытия. Введите это время и увидите облаву у себя, по Москве и в UTC.",
        "h1": "Отсчёт до Федеральной облавы",
        "lede": "Федеральная облава приходит на сервер через семь дней после того, как он открылся. Укажите это время — страница покажет облаву в вашем часовом поясе, по Москве и в UTC.",
        "mode": "Какой сервер?",
        "opt_custom": "Знаю, когда он открылся",
        "opt_eu": "Ежедневный сервер EU (17:00 UTC)",
        "opt_us": "Ежедневный сервер востока США (20:00 ET)",
        "opt_launch": "Серверы запуска 4 ноября 2026",
        "opened": "Дата и время открытия",
        "zone": "Часовой пояс этого времени",
        "open_date": "Дата открытия",
        "hint_custom": "Семь дней — это 7 × 24 часа от указанного момента.",
        "hint_eu": "В новости от 4 ноября Kefir планирует минимум один свежий сервер EU в 17:00 UTC каждый день. Бывают и внеплановые серверы — для них введите фактическое время открытия.",
        "hint_us": "Там же запланирован сервер востока США в 20:00 ET. Серверы вне этого слота открываются отдельно.",
        "hint_launch": "В Steam написали, что серверы поднимут 4 ноября 2026 года в 17:00 UTC. В Telegram облаву для серверов этого запуска назначили на 11 ноября, 20:00 МСК — ровно через семь дней.",
        "keep_h": "Остаётся",
        "lose_h": "Обнуляется",
        "keep": ["Косметика", "Ник", "Прогресс обучения", "Настройки", "Накопленный тюремный срок"],
        "lose": ["Земли", "Базы", "Оружие", "Деньги — они становятся тюремным сроком и авторитетом"],
        "passed": "Это время облавы уже прошло.",
        "need": "Укажите дату и время открытия.",
        "open_prefix": "Открытие",
        "raid_note": "Облава — через семь дней.",
        "local": "У вас",
        "msk": "Москва",
        "utc": "UTC",
        "sources": (
            'Что остаётся и что обнуляется: <a href="https://kefirgames.helpshift.com/hc/ru/14-rob-run/faq/1346-what-is-the-federal-raid-wipe/?l=ru">справка Kefir</a>. '
            'В <a href="https://t.me/robrungame/67">посте Telegram от 11 ноября 2026</a> к конфискации также отнесены транспорт, недвижимость, земля, открытые предметы древа, учтённые траты на клан и взятки, а баланс B-coin сохраняется. '
            'Первая облава и срок жизни сервера в семь дней — тот же пост. '
            'EU в 17:00 UTC, восток США в 20:00 ET и дополнительные серверы: <a href="https://store.steampowered.com/news/app/4262460/view/712291399099220569">новость Steam от 4 ноября 2026</a>. '
            'Проверено 13 ноября 2026.'
        ),
        "planner_link": (
            'Планируете, что сохранить? <a href="/ru/rob-run/wipe-planner/">Планировщик вайпа ROB RUN</a>: '
            'что сбрасывается, что остаётся, и чек-лист перед вайпом.'
        ),
    },
}

COUNT_JS = r"""
<script>
(function () {
  var STR = __STR__;
  var WEEK = 7 * 24 * 60 * 60 * 1000;
  var mode = document.getElementById('mode');
  var customFields = document.getElementById('customFields');
  var dateFields = document.getElementById('dateFields');
  var opened = document.getElementById('opened');
  var zone = document.getElementById('zone');
  var openDate = document.getElementById('openDate');
  var hint = document.getElementById('modeHint');
  var cd = document.getElementById('cd');
  var openLine = document.getElementById('openLine');
  function tzOffsetMs(tz, utcMs) {
    var dtf = new Intl.DateTimeFormat('en-US', {
      timeZone: tz, hourCycle: 'h23', year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', second: '2-digit'
    });
    var parts = dtf.formatToParts(new Date(utcMs));
    var get = function (t) {
      for (var i = 0; i < parts.length; i++) if (parts[i].type === t) return parts[i].value;
      return '0';
    };
    var hour = get('hour') === '24' ? 0 : parseInt(get('hour'), 10);
    var asUTC = Date.UTC(+get('year'), +get('month') - 1, +get('day'), hour, +get('minute'), +get('second'));
    return asUTC - Math.floor(utcMs / 1000) * 1000;
  }
  function zonedTimeToUtc(tz, y, mo, d, h, mi) {
    var utc = Date.UTC(y, mo - 1, d, h, mi, 0);
    utc = Date.UTC(y, mo - 1, d, h, mi, 0) - tzOffsetMs(tz, utc);
    utc = Date.UTC(y, mo - 1, d, h, mi, 0) - tzOffsetMs(tz, utc);
    return utc;
  }
  function dateParts(value) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value || '');
    if (!m) return null;
    return { y: +m[1], mo: +m[2], d: +m[3] };
  }
  function dateTimeParts(value) {
    var m = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})/.exec(value || '');
    if (!m) return null;
    return { y: +m[1], mo: +m[2], d: +m[3], h: +m[4], mi: +m[5] };
  }
  function openingUtc() {
    if (mode.value === 'launch') return Date.UTC(2026, 10, 4, 17, 0, 0);
    if (mode.value === 'eu' || mode.value === 'us') {
      var p = dateParts(openDate.value);
      if (!p) return null;
      if (mode.value === 'eu') return zonedTimeToUtc('UTC', p.y, p.mo, p.d, 17, 0);
      return zonedTimeToUtc('America/New_York', p.y, p.mo, p.d, 20, 0);
    }
    var wall = dateTimeParts(opened.value);
    if (!wall) return null;
    if (zone.value === 'local') return new Date(wall.y, wall.mo - 1, wall.d, wall.h, wall.mi, 0).getTime();
    return zonedTimeToUtc(zone.value, wall.y, wall.mo, wall.d, wall.h, wall.mi);
  }
  function fmt(ms, tz) {
    var clockOpts = { hour: '2-digit', minute: '2-digit', hourCycle: 'h23' };
    var dateOpts = { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric', timeZoneName: 'short' };
    if (tz) { clockOpts.timeZone = tz; dateOpts.timeZone = tz; }
    var when = new Date(ms);
    return {
      clock: new Intl.DateTimeFormat(STR.locale, clockOpts).format(when),
      date: new Intl.DateTimeFormat(STR.locale, dateOpts).format(when)
    };
  }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function paint(idClock, idDate, parts) {
    document.getElementById(idClock).textContent = parts.clock;
    document.getElementById(idDate).textContent = parts.date;
  }
  function clearClocks() {
    ['localClock', 'mskClock', 'utcClock'].forEach(function (id) {
      document.getElementById(id).textContent = '—';
    });
    ['localDate', 'mskDate', 'utcDate'].forEach(function (id) {
      document.getElementById(id).textContent = '';
    });
  }
  function syncFields() {
    var m = mode.value;
    customFields.hidden = m !== 'custom';
    dateFields.hidden = m !== 'eu' && m !== 'us';
    hint.textContent = STR.hints[m];
  }
  function tick() {
    syncFields();
    var open = openingUtc();
    if (open == null || !isFinite(open)) {
      cd.textContent = '—';
      openLine.textContent = STR.need;
      clearClocks();
      return;
    }
    var raid = open + WEEK;
    paint('localClock', 'localDate', fmt(raid));
    paint('mskClock', 'mskDate', fmt(raid, 'Europe/Moscow'));
    paint('utcClock', 'utcDate', fmt(raid, 'UTC'));
    var localOpen = fmt(open);
    openLine.textContent = STR.openPrefix + ': ' + localOpen.date + ', ' + localOpen.clock + '. ' + STR.raidNote;
    var diff = raid - Date.now();
    if (diff <= 0) { cd.textContent = STR.passed; return; }
    var s = Math.floor(diff / 1000);
    var d = Math.floor(s / 86400);
    var h = Math.floor((s % 86400) / 3600);
    var mi = Math.floor((s % 3600) / 60);
    var sec = s % 60;
    cd.innerHTML = d + '<span class="unit">' + STR.units[0] + '</span>' + pad(h) +
      '<span class="unit">' + STR.units[1] + '</span>' + pad(mi) +
      '<span class="unit">' + STR.units[2] + '</span>' + pad(sec) +
      '<span class="unit">' + STR.units[3] + '</span>';
  }
  mode.addEventListener('change', tick);
  opened.addEventListener('input', tick);
  zone.addEventListener('change', tick);
  openDate.addEventListener('input', tick);
  tick();
  setInterval(tick, 1000);
})();
</script>
"""


def countdown_page(lang):
    c = COUNT[lang]
    hub = "/rob-run/" if lang == "en" else "/ru/rob-run/"
    opts = (
        '<option value="custom">%s</option>'
        '<option value="eu">%s</option>'
        '<option value="us">%s</option>'
        '<option value="launch">%s</option>'
        % (c["opt_custom"], c["opt_eu"], c["opt_us"], c["opt_launch"])
    )
    zones = "".join(
        '<option value="%s"%s>%s</option>'
        % (zid, " selected" if zid == "UTC" else "", en if lang == "en" else ru)
        for zid, en, ru in ZONES)
    keep = "".join("<li>%s</li>" % x for x in c["keep"])
    lose = "".join("<li>%s</li>" % x for x in c["lose"])
    body = (
        '<main id="main" class="wrap narrow">%s'
        '<h1 class="page-h1">%s</h1><p class="page-lede">%s</p>'
        '<div class="checker"><label for="mode">%s</label>'
        '<select id="mode">%s</select>'
        '<div id="customFields">'
        '<label for="opened" style="margin-top:18px">%s</label>'
        '<input id="opened" type="datetime-local" value="2026-11-04T17:00">'
        '<label for="zone" style="margin-top:18px">%s</label>'
        '<select id="zone">%s</select></div>'
        '<div id="dateFields" hidden>'
        '<label for="openDate" style="margin-top:18px">%s</label>'
        '<input id="openDate" type="date" value="2026-11-04"></div>'
        '<p class="hint" id="modeHint"></p>'
        '<div class="countdown-big" id="cd" aria-live="polite" style="margin-top:18px">—</div>'
        '<div class="stats" style="margin-top:16px">'
        '<div class="stat"><em>%s</em><strong id="localClock">—</strong><span id="localDate"></span></div>'
        '<div class="stat"><em>%s</em><strong id="mskClock">—</strong><span id="mskDate"></span></div>'
        '<div class="stat"><em>%s</em><strong id="utcClock">—</strong><span id="utcDate"></span></div>'
        '</div><p class="hint" id="openLine"></p></div>'
        '<div class="keep-grid"><div class="note-box"><h2>%s</h2><ul>%s</ul></div>'
        '<div class="note-box amber"><h2>%s</h2><ul>%s</ul></div></div>'
        '<p class="hint">%s</p>'
        '<p class="data-line">%s</p></main>'
        % (crumbs_html(lang, [("ROB RUN", hub), (c["h1"], None)]),
           c["h1"], c["lede"], c["mode"], opts, c["opened"], c["zone"], zones,
           c["open_date"], c["local"], c["msk"], c["utc"],
           c["keep_h"], keep, c["lose_h"], lose, c["planner_link"], c["sources"])
    )
    strings = {
        "locale": "en-US" if lang == "en" else "ru-RU",
        "passed": c["passed"],
        "need": c["need"],
        "openPrefix": c["open_prefix"],
        "raidNote": c["raid_note"],
        "units": ["d", "h", "m", "s"] if lang == "en" else ["д", "ч", "мин", "с"],
        "hints": {
            "custom": c["hint_custom"],
            "eu": c["hint_eu"],
            "us": c["hint_us"],
            "launch": c["hint_launch"],
        },
    }
    js = COUNT_JS.replace("__STR__", json.dumps(strings, ensure_ascii=False))
    return tool_page(lang, "federal-raid-countdown", c["title"], c["desc"], body + js, c["h1"])


# ---------------------------------------------------------------- loot profit
# V2 (17 Nov 2026): item-database calculator. Prices come from the public
# robrunwiki catalogue (game version 0.7.0), built into data/rob-run-items.json
# by scripts/build_rob_data.py. Title and H1 are unchanged (ranked).
# Notoriety ladders (verified): valuables 1.00/1.10/1.20/1.35/1.50,
# cargo 1.00/1.05/1.10/1.15/1.25. Cash has no verified symbol.
PROFIT = {
    "en": {
        "title": "ROB RUN loot profit calculator — BuffForge",
        "desc": "Search the ROB RUN item database, set your Notoriety level, and see the estimated sale payout, net profit and per-player share. Prices from the public robrunwiki catalogue, game version 0.7.0.",
        "h1": "Loot profit calculator",
        "lede": "Pick loot from the item database, set your Notoriety level, then subtract gear and other costs. Sale prices are estimates from the public catalogue — confirm the actual offer in game.",
        "find_h": "Find loot",
        "search_label": "Search items",
        "search_ph": "Gold Bar, Diamond, слиток…",
        "cat_label": "Item type",
        "cat_all": "All types",
        "cat_valuables": "Valuables",
        "cat_cargo": "Cargo",
        "cat_other": "Other priced items",
        "results_hint": "Only items with a published sale price can be added. Confirm the actual offer in game; prices may change after a patch.",
        "add": "Add",
        "custom_h": "Add a custom item",
        "custom_note": "Use this when an item is missing or its current in-game offer differs. A custom price is the final unit sale value at your level — no bonus is added.",
        "name": "Item",
        "price": "Sale price (cash)",
        "qty": "Qty",
        "add_custom": "+ Add custom item",
        "haul_h": "Your haul",
        "clear": "Clear list",
        "notoriety": "Notoriety level",
        "not_opts": [
            "Level 1 · Base",
            "Level 2 · +10% / +5%",
            "Level 3 · +20% / +10%",
            "Level 4 · +35% / +15%",
            "Level 5 · +50% / +25%",
        ],
        "gear": "Gear (cash)",
        "other": "Other costs (cash)",
        "split": "Split between",
        "split_opts": ["1 player", "2 players", "3 players", "4 players"],
        "cargo_note": "Cargo uses the smaller Notoriety bonus (up to +25%). Exact sale values come from the source price range when the tier is supported.",
        "base": "Base sale value",
        "sale": "Est. total sale",
        "costs": "Costs",
        "net": "Net",
        "per": "Profit per player",
        "ratio": "Return",
        "ratio_sub": "Est. sale ÷ costs",
        "cash": "cash",
        "share": "Copy share link",
        "save": "Save on this device",
        "restore": "Load saved haul",
        "export": "Export haul CSV",
        "note": "Kefir’s help pages call the in-game money cash. No currency symbol is shown here because none is published on those pages.",
        "data_h": "Data & sources",
        "data_p": "Source: <a href=\"https://robrunwiki.com/en/data/\">ROB RUN Wiki open data</a>, original <a href=\"https://robrunwiki.com/data/items.csv\">items.csv</a>, game version 0.7.0. English and Russian names, categories and the minimum/maximum sale prices come from that catalogue. Intermediate Notoriety tiers use the documented multipliers — the CSV only publishes the two end prices. This tool is not affiliated with Kefir.",
        "import_label": "Import updated items.csv",
        "reset": "Reset to site data",
        "import_note": "An imported CSV works for this session only and is not saved. To update the site database, it has to be rebuilt from the public catalogue.",
        "faq_h": "Frequently asked questions",
        "faq": [
            ("How do I calculate ROB RUN loot profit?",
             "Search for items and add the quantities you collected. Set your Notoriety level, enter gear and other run costs, then read the estimated net profit. The result subtracts costs from the estimated sale payout."),
            ("Does Notoriety increase every item’s value equally?",
             "No. Valuables follow 1.00, 1.10, 1.20, 1.35 and 1.50. Some cargo follows 1.00, 1.05, 1.10, 1.15 and 1.25. The calculator checks each item’s published minimum and maximum price and warns when its tier cannot be reliably inferred."),
            ("Are these live prices from ROB RUN?",
             "No. The source reflects game version 0.7.0 and may lag a patch. Always verify the in-game Fence or Smuggler price. Custom entries let you use your actual observed offer."),
            ("Why isn’t backpack slot optimization included?",
             "The public catalogue does not provide verified occupied-slot data for every loot item. We do not invent slot counts or rank items on unverified storage assumptions."),
        ],
        "sources": "Item prices: public catalogue at robrunwiki.com, game version 0.7.0. 569 entries, 373 with a published sale price. Not live prices — confirm in game. BuffForge is an independent fan project, not affiliated with Kefir.",
    },
    "ru": {
        "title": "Калькулятор добычи ROB RUN — BuffForge",
        "desc": "Найдите предметы ROB RUN в базе, выберите уровень дурной славы и узнайте примерную выручку, чистую прибыль и долю на игрока. Цены — из открытого каталога robrunwiki, версия игры 0.7.0.",
        "h1": "Калькулятор добычи",
        "lede": "Соберите добычу из базы предметов, выберите уровень дурной славы и вычтите снаряжение и прочие расходы. Цены примерные, из открытого каталога — точное предложение проверяйте в игре.",
        "find_h": "Найти добычу",
        "search_label": "Поиск предметов",
        "search_ph": "Gold Bar, слиток, Diamond…",
        "cat_label": "Тип предмета",
        "cat_all": "Все типы",
        "cat_valuables": "Ценности",
        "cat_cargo": "Грузы",
        "cat_other": "Прочие предметы с ценой",
        "results_hint": "Добавить можно только предметы с опубликованной ценой продажи. Точное предложение проверяйте в игре: после патча цены могут измениться.",
        "add": "Добавить",
        "custom_h": "Добавить свой предмет",
        "custom_note": "Используйте, если предмета нет в базе или предложение в игре отличается. Своя цена — это итоговая цена продажи за штуку на вашем уровне, бонус к ней не добавляется.",
        "name": "Предмет",
        "price": "Цена продажи (деньги)",
        "qty": "Шт.",
        "add_custom": "+ Добавить свой предмет",
        "haul_h": "Ваша добыча",
        "clear": "Очистить",
        "notoriety": "Уровень дурной славы",
        "not_opts": [
            "Уровень 1 · база",
            "Уровень 2 · +10% / +5%",
            "Уровень 3 · +20% / +10%",
            "Уровень 4 · +35% / +15%",
            "Уровень 5 · +50% / +25%",
        ],
        "gear": "Снаряжение (деньги)",
        "other": "Прочие расходы (деньги)",
        "split": "Разделить на",
        "split_opts": ["1 игрока", "2 игроков", "3 игроков", "4 игроков"],
        "cargo_note": "У грузов бонус дурной славы меньше (максимум +25%). Точные цены продажи берутся из диапазона цен источника, когда уровень поддерживается.",
        "base": "Базовая выручка",
        "sale": "Примерная выручка",
        "costs": "Расходы",
        "net": "Итог",
        "per": "Прибыль на игрока",
        "ratio": "Отдача",
        "ratio_sub": "Выручка ÷ расходы",
        "cash": "деньги",
        "share": "Скопировать ссылку",
        "save": "Сохранить в браузере",
        "restore": "Загрузить сохранённое",
        "export": "Экспорт в CSV",
        "note": "В справке Kefir игровая валюта названа просто деньгами. Символа на странице нет: в этих справках его не публикуют.",
        "data_h": "Данные и источники",
        "data_p": "Источник: <a href=\"https://robrunwiki.com/en/data/\">открытые данные ROB RUN Wiki</a>, исходный <a href=\"https://robrunwiki.com/data/items.csv\">items.csv</a>, версия игры 0.7.0. Английские и русские названия, категории и минимальная/максимальная цены — из этого каталога. Промежуточные уровни дурной славы рассчитаны по документированным множителям: в CSV опубликованы только две крайние цены. Сайт не связан с Kefir.",
        "import_label": "Импортировать обновлённый items.csv",
        "reset": "Сбросить к данным сайта",
        "import_note": "Импортированный CSV работает только в этой сессии и не сохраняется. Чтобы обновить базу сайта, её нужно пересобрать из открытого каталога.",
        "faq_h": "Частые вопросы",
        "faq": [
            ("Как посчитать прибыль от добычи в ROB RUN?",
             "Найдите предметы и добавьте собранное количество. Выберите уровень дурной славы, введите расходы на снаряжение и прочие расходы — и увидите примерную чистую прибыль. Из примерной выручки вычитаются расходы."),
            ("Дурная слава одинаково повышает цену всех предметов?",
             "Нет. Ценности обычно идут по множителям 1,00, 1,10, 1,20, 1,35 и 1,50. Часть грузов — по 1,00, 1,05, 1,10, 1,15 и 1,25. Калькулятор сверяет минимальную и максимальную цену каждого предмета из каталога и предупреждает, если уровень нельзя надёжно вывести."),
            ("Это живые цены из ROB RUN?",
             "Нет. Источник соответствует версии игры 0.7.0 и может отставать от патча. Всегда проверяйте цену у скупщика или контрабандиста в игре. Свои предметы позволяют ввести реальное предложение."),
            ("Почему нет оптимизации по клеткам рюкзака?",
             "В открытом каталоге нет проверенных данных о том, сколько клеток занимает каждый предмет. Мы не выдумываем эти числа и не строим на них рейтинг."),
        ],
        "sources": "Цены предметов: открытый каталог robrunwiki.com, версия игры 0.7.0. Всего 569 записей, 373 — с опубликованной ценой продажи. Цены не живые — проверяйте в игре. BuffForge — независимый фанатский проект, не связан с Kefir.",
    },
}

# Offline subset for the calculator: 51 priced rows, each verified against
# /tmp/items.csv on 17 Nov 2026. Names are copied as published — the three
# Industrial Freezer tiers share one name and are told apart by rarity.
OFFLINE_IDS = [
    "egg_faberge_1", "ring_7", "vinyl_2", "baseball_card_6", "equipment_12",
    "laptop_5", "alcohol_15", "gemstone_1", "blade_6", "pharma_tools_2",
    "car_trinket_6", "equipment_6", "gold_bar_1", "vinyl_1", "ring_6",
    "headphones_5", "toy_5", "earrings_2", "burner_3", "watch_5",
    "journal_5", "pharma_tools_5", "equipment_11", "comics_5", "necklace_6",
    "laptop_4", "console_5", "blade_5", "alcohol_5", "antique_4",
    "alcohol_13", "equipment_7", "alcohol_14", "car_device_6", "alcohol_12",
    "drugs_6", "equip_carbine_4", "baseball_card_1",
    "action_camera_1_cumulative", "alcohol_box_1", "bush_drugs_1",
    "cargo_alcohol_grade_1", "cargo_alcohol_grade_2", "cargo_alcohol_grade_3",
    "cargo_carparts", "cargo_electronics", "cargo_equip",
    "cargo_charge_workbench_garden_bed",
    "cargo_charge_workbench_lab_freezer_1",
    "cargo_charge_workbench_lab_freezer_2",
    "cargo_charge_workbench_lab_freezer_3",
]

RARITY_EN = {
    "Обычный": "Common",
    "Необычный": "Uncommon",
    "Эпический": "Epic",
    "Легендарный": "Legendary",
    "Экзотический": "Exotic",
}

_PROFIT_OFFLINE = None


def _profit_cat(category_ru):
    if category_ru == "Ценности (краденое)":
        return "valuables"
    if category_ru == "Грузы":
        return "cargo"
    return "other"


def _profit_offline():
    """Offline subset, built from data/rob-run-items.json. Fails the build
    if any of the 51 ids is missing, so a catalogue change is caught here."""
    global _PROFIT_OFFLINE
    if _PROFIT_OFFLINE is not None:
        return _PROFIT_OFFLINE
    with open(os.path.join(ROOT, "data", "rob-run-items.json"),
              encoding="utf-8") as f:
        data = json.load(f)
    by_id = {x["id"]: x for x in data["items"]}
    out = []
    for item_id in OFFLINE_IDS:
        if item_id not in by_id:
            raise SystemExit("ABORT: offline sample id %s missing from "
                             "data/rob-run-items.json" % item_id)
        x = by_id[item_id]
        out.append({
            "id": x["id"], "en": x["name_en"], "ru": x["name_ru"],
            "cat": _profit_cat(x["category_ru"]), "rarity": x["rarity"],
            "min": x["min"], "max": x["max"], "url": x["url"],
        })
    _PROFIT_OFFLINE = out
    return out

PROFIT_JS = r"""
<script>
(function () {
  var STR = __STR__;
  var OFFLINE = __OFFLINE__;
  var DATA_URL = '/data/rob-run-items.json';
  var LS_KEY = 'buffforge-rob-run-haul-v2';
  var catalog = OFFLINE, haul = [], dataMode = 'offline';
  var searchTimer = null;
  var searchEl = document.getElementById('search');
  var catEl = document.getElementById('category');
  var resultCountEl = document.getElementById('resultCount');
  var resultsEl = document.getElementById('results');
  var customNameEl = document.getElementById('customName');
  var customPriceEl = document.getElementById('customPrice');
  var customQtyEl = document.getElementById('customQty');
  var customNoteEl = document.getElementById('customNote');
  var haulEl = document.getElementById('haul');
  var notorietyEl = document.getElementById('notoriety');
  var gearEl = document.getElementById('gearCost');
  var otherEl = document.getElementById('otherCost');
  var splitEl = document.getElementById('split');
  var baseOut = document.getElementById('baseOut');
  var saleOut = document.getElementById('saleOut');
  var costOut = document.getElementById('costOut');
  var netOut = document.getElementById('netOut');
  var perOut = document.getElementById('perOut');
  var ratioOut = document.getElementById('ratioOut');
  var calcNoticeEl = document.getElementById('calcNotice');
  var dataNoticeEl = document.getElementById('dataNotice');
  var dataMetaEl = document.getElementById('dataMeta');
  var toolNoteEl = document.getElementById('toolNote');
  var shareEl = document.getElementById('share');
  function num(v) {
    var n = parseFloat(v);
    return isFinite(n) ? n : 0;
  }
  function pos(v) {
    var n = num(v);
    return n > 0 ? n : 0;
  }
  function fmt(n) {
    return isFinite(n) ? n.toLocaleString(STR.locale, {maximumFractionDigits: 2}) : '—';
  }
  function fmtInt(n) {
    return isFinite(n) ? Math.round(n).toLocaleString(STR.locale, {maximumFractionDigits: 0}) : '—';
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (ch) {
      return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[ch];
    });
  }
  function countText(n) {
    var f = STR.countForms;
    if (STR.lang === 'ru') {
      var m10 = n % 10, m100 = n % 100;
      var i = (m10 === 1 && m100 !== 11) ? 0 : (m10 >= 2 && m10 <= 4 && (m100 < 12 || m100 > 14)) ? 1 : 2;
      return f[i].replace('{n}', fmtInt(n));
    }
    return f[n === 1 ? 0 : 1].replace('{n}', fmtInt(n));
  }
  function catOf(row) {
    var c = (row.category_ru || '').trim();
    if (c === 'Ценности (краденое)') return 'valuables';
    if (c === 'Грузы') return 'cargo';
    return 'other';
  }
  function convertRows(rows) {
    var out = [];
    for (var i = 0; i < rows.length; i++) {
      var row = rows[i];
      var id = (row.id || '').trim(), en = (row.name_en || '').trim(), ru = (row.name_ru || '').trim();
      // Site JSON uses min/max; an imported CSV uses fence_price_min/max_usd.
      var min = Number(row.fence_price_min_usd != null ? row.fence_price_min_usd : row.min);
      var max = Number(row.fence_price_max_usd != null ? row.fence_price_max_usd : row.max);
      if (!id || !en || !isFinite(min) || min <= 0) continue;
      out.push({id: id, en: en, ru: ru, cat: catOf(row), rarity: row.rarity || '',
        min: min, max: isFinite(max) && max >= min ? max : min, url: row.url || ''});
    }
    return out;
  }
  // CSV parser: quoted commas, embedded quotes, CRLF, BOM.
  function parseCSV(csv) {
    csv = csv.replace(/^\uFEFF/, '');
    var records = [], row = [], val = '', quote = false;
    for (var i = 0; i < csv.length; i++) {
      var ch = csv[i];
      if (quote) {
        if (ch === '"' && csv[i + 1] === '"') { val += '"'; i++; }
        else if (ch === '"') quote = false;
        else val += ch;
      } else if (ch === '"') quote = true;
      else if (ch === ',') { row.push(val); val = ''; }
      else if (ch === '\n') { row.push(val.replace(/\r$/, '')); records.push(row); row = []; val = ''; }
      else val += ch;
    }
    if (val || row.length) { row.push(val.replace(/\r$/, '')); records.push(row); }
    var headers = (records.shift() || []).map(function (x) { return x.trim().replace(/^\uFEFF/, ''); });
    return records.filter(function (x) { return x.some(function (v) { return v.trim(); }); })
      .map(function (values) {
        var obj = {};
        headers.forEach(function (k, j) { obj[k] = values[j] || ''; });
        return obj;
      });
  }
  function priceAt(item, lvl) {
    if (item.custom) return item.min;
    var min = item.min, max = item.max, ratio = max / min;
    var valuables = [1, 1.1, 1.2, 1.35, 1.5];
    var cargo = [1, 1.05, 1.1, 1.15, 1.25];
    if (Math.abs(ratio - 1.5) < 0.015) return Math.round(min * valuables[lvl - 1]);
    if (Math.abs(ratio - 1.25) < 0.015) return Math.round(min * cargo[lvl - 1]);
    if (Math.abs(ratio - 1) < 0.005) return min;
    // Unknown ladder: only the two end prices are confirmed.
    return lvl === 1 ? min : lvl === 5 ? max : null;
  }
  function rarityOf(x) {
    var r = x.rarity || '';
    if (STR.lang === 'en' && STR.rarity[r]) return STR.rarity[r];
    return r;
  }
  function nameMain(x) {
    return STR.lang === 'ru' ? (x.ru || x.en) : x.en;
  }
  function nameSub(x) {
    var other = STR.lang === 'ru' ? x.en : x.ru;
    var r = rarityOf(x);
    var parts = [];
    if (other) parts.push(other);
    if (r) parts.push(r);
    return parts.join(' · ');
  }
  function findItem(id) {
    for (var i = 0; i < catalog.length; i++) if (catalog[i].id === id) return catalog[i];
    return null;
  }
  function renderResults() {
    var q = searchEl.value.trim().toLowerCase();
    var cat = catEl.value;
    var matches = catalog.filter(function (x) {
      return (cat === 'all' || x.cat === cat) &&
        (!q || (x.en + ' ' + x.ru + ' ' + x.id).toLowerCase().indexOf(q) !== -1);
    });
    resultCountEl.textContent = countText(matches.length);
    var sorted = matches.slice().sort(function (a, b) {
      if (!q) return b.min - a.min;
      var as = a.en.toLowerCase().indexOf(q) === 0 ? -1 : 0;
      var bs = b.en.toLowerCase().indexOf(q) === 0 ? -1 : 0;
      return (as - bs) || (b.min - a.min);
    });
    var html = sorted.slice(0, 80).map(function (x) {
      var sub = nameSub(x);
      return '<div class="res-item"><div><b>' + esc(nameMain(x)) + '</b>' +
        (sub ? '<span class="sub">' + esc(sub) + '</span>' : '') + '</div>' +
        '<div class="price">' + fmt(x.min) + ' ' + esc(STR.cash) + '</div>' +
        '<button type="button" class="btn btn-secondary" data-add="' + esc(x.id) + '">' +
        esc(STR.add) + '</button></div>';
    }).join('');
    if (!html) html = '<p class="hint">' + esc(STR.noMatch) + '</p>';
    if (matches.length > 80) {
      html += '<p class="hint">' + esc(STR.showing80.replace('{n}', fmtInt(matches.length))) + '</p>';
    }
    resultsEl.innerHTML = html;
  }
  function notify(msg, warn) {
    dataNoticeEl.className = 'datanote' + (warn ? ' warn' : '');
    dataNoticeEl.textContent = msg;
  }
  function setCatalog(rows, mode) {
    if (!rows.length) throw new Error('No priced items found.');
    catalog = rows;
    dataMode = mode;
    dataMetaEl.textContent = mode === 'offline' ? STR.dataMetaOff :
      STR.dataMeta.replace('{n}', fmtInt(rows.length));
    renderResults();
    renderHaul();
  }
  function loadData() {
    return fetch(DATA_URL, {cache: 'no-store'}).then(function (r) {
      if (!r.ok) throw new Error('Endpoint unavailable');
      return r.json();
    }).then(function (data) {
      if (!data.items || !Array.isArray(data.items)) throw new Error('Invalid JSON');
      var rows = convertRows(data.items);
      if (rows.length < 50) throw new Error('Dataset incomplete');
      setCatalog(rows, 'full');
      var total = (data.meta && data.meta.total) ? data.meta.total : rows.length;
      notify(STR.full.replace('{total}', fmtInt(total)).replace('{n}', fmtInt(rows.length)), false);
    }).catch(function () {
      setCatalog(OFFLINE, 'offline');
      notify(STR.offline.replace('{n}', fmtInt(OFFLINE.length)), true);
    });
  }
  function updateTotals() {
    var lvl = +notorietyEl.value;
    var base = 0, sale = 0, unknown = 0;
    for (var i = 0; i < haul.length; i++) {
      var x = haul[i];
      var s = findItem(x.id) || x;
      var qty = Math.max(1, Math.floor(x.qty) || 1);
      var p = priceAt(s, lvl);
      base += s.min * qty;
      if (p === null) { unknown++; } else { sale += p * qty; }
      var lp = haulEl.querySelector('[data-lp="' + x.id + '"]');
      if (lp) lp.textContent = p === null ? STR.unknown : fmt(p * qty);
    }
    var costs = pos(gearEl.value) + pos(otherEl.value);
    var net = sale - costs;
    var split = +(splitEl.value || 1);
    baseOut.textContent = fmt(base);
    saleOut.textContent = fmt(sale);
    costOut.textContent = fmt(costs);
    netOut.textContent = fmt(net);
    netOut.style.color = net < 0 ? 'var(--danger)' : 'var(--ink)';
    perOut.textContent = fmt(net / split);
    ratioOut.textContent = costs === 0 ? '—' :
      (sale / costs).toLocaleString(STR.locale, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + '×';
    calcNoticeEl.textContent = unknown ? STR.unknownWarn.replace('{n}', unknown) :
      haul.length ? STR.estimates : STR.noHaul;
  }
  function renderHaul() {
    var lvl = +notorietyEl.value;
    var html = '';
    for (var i = 0; i < haul.length; i++) {
      var x = haul[i];
      var s = findItem(x.id) || x;
      var p = priceAt(s, lvl);
      var sub = nameSub(s);
      html += '<div class="haul-row"><div class="t">' + esc(nameMain(s)) +
        (x.custom ? ' <span class="sub">· ' + esc(STR.customTag) + '</span>' : '') +
        (sub ? '<span class="sub">' + esc(sub) + '</span>' : '') +
        '<span class="sub">' + esc(p === null ? STR.unknown : STR.each.replace('{p}', fmt(p))) + '</span></div>' +
        '<input type="number" min="1" max="999999" value="' + x.qty + '" data-qty="' + esc(x.id) + '"' +
        ' aria-label="' + esc(STR.qtyFor.replace('{n}', nameMain(s))) + '">' +
        '<div class="lp" data-lp="' + esc(x.id) + '">' + (p === null ? STR.unknown : fmt(p * x.qty)) + '</div>' +
        '<button type="button" class="btn btn-ghost" data-remove="' + esc(x.id) + '"' +
        ' aria-label="' + esc(STR.remove) + '">×</button></div>';
    }
    haulEl.innerHTML = html || '<p class="hint">' + esc(STR.empty) + '</p>';
    updateTotals();
  }
  function persistState() {
    try {
      var encoded = encodeURIComponent(JSON.stringify({
        haul: haul, notoriety: notorietyEl.value,
        gearCost: gearEl.value, otherCost: otherEl.value, split: splitEl.value}));
      history.replaceState(null, '', location.pathname + location.search + '#haul=' + encoded);
    } catch (e) {}
  }
  function updateFromHash() {
    if (location.hash.indexOf('#haul=') !== 0) return;
    try {
      var obj = JSON.parse(decodeURIComponent(location.hash.slice(6)));
      if (!obj || !Array.isArray(obj.haul) || obj.haul.length > 200) return;
      haul = obj.haul.filter(function (x) {
        return typeof x.id === 'string' && typeof x.en === 'string' &&
          isFinite(Number(x.min)) && x.min >= 0;
      }).slice(0, 150).map(function (x) {
        return {id: x.id, en: x.en, ru: x.ru || '', cat: x.cat || 'other',
          rarity: x.rarity || '', min: Number(x.min),
          max: Number(x.max) || Number(x.min), custom: !!x.custom,
          url: x.url || '', qty: Math.max(1, Math.min(999999, Math.floor(Number(x.qty) || 1)))};
      });
      var keys = ['notoriety', 'gearCost', 'otherCost', 'split'];
      for (var i = 0; i < keys.length; i++) {
        if (obj[keys[i]] != null) {
          var el = document.getElementById(keys[i]);
          if (el) el.value = obj[keys[i]];
        }
      }
      renderHaul();
    } catch (e) {}
  }
  function addItem(id) {
    var x = findItem(id);
    if (!x) return;
    var found = null;
    for (var i = 0; i < haul.length; i++) if (haul[i].id === id) found = haul[i];
    if (found) found.qty++;
    else haul.push({id: x.id, en: x.en, ru: x.ru, cat: x.cat, rarity: x.rarity,
      min: x.min, max: x.max, url: x.url, qty: 1});
    renderHaul();
    persistState();
  }
  searchEl.addEventListener('input', function () {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(renderResults, 70);
  });
  catEl.addEventListener('change', renderResults);
  resultsEl.addEventListener('click', function (e) {
    var btn = e.target.closest ? e.target.closest('[data-add]') : null;
    if (btn) addItem(btn.getAttribute('data-add'));
  });
  haulEl.addEventListener('input', function (e) {
    if (!e.target.matches || !e.target.matches('[data-qty]')) return;
    var x = null;
    for (var i = 0; i < haul.length; i++) if (haul[i].id === e.target.getAttribute('data-qty')) x = haul[i];
    if (x) {
      x.qty = Math.min(999999, Math.max(1, Math.floor(Number(e.target.value) || 1)));
      updateTotals();
      persistState();
    }
  });
  haulEl.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('[data-remove]') : null;
    if (b) {
      var id = b.getAttribute('data-remove');
      haul = haul.filter(function (x) { return x.id !== id; });
      renderHaul();
      persistState();
    }
  });
  notorietyEl.addEventListener('change', function () { renderHaul(); persistState(); });
  gearEl.addEventListener('input', function () { updateTotals(); persistState(); });
  otherEl.addEventListener('input', function () { updateTotals(); persistState(); });
  splitEl.addEventListener('change', function () { updateTotals(); persistState(); });
  document.getElementById('clearHaul').addEventListener('click', function () {
    haul = [];
    renderHaul();
    persistState();
  });
  document.getElementById('addCustom').addEventListener('click', function () {
    var en = customNameEl.value.trim();
    var p = Number(customPriceEl.value);
    var qty = Math.floor(Number(customQtyEl.value));
    if (!en || !isFinite(p) || p < 0 || qty < 1) {
      customNoteEl.textContent = STR.needCustom;
      customNameEl.focus();
      return;
    }
    customNoteEl.textContent = '';
    var id = 'custom-' + Date.now() + '-' + Math.random().toString(36).slice(2, 8);
    haul.push({id: id, en: en, ru: '', cat: 'other', rarity: '', min: p, max: p,
      custom: true, url: '', qty: Math.min(999999, qty)});
    customNameEl.value = '';
    customPriceEl.value = '';
    customQtyEl.value = '1';
    renderHaul();
    persistState();
    customNameEl.focus();
  });
  shareEl.addEventListener('click', function () {
    persistState();
    var done = function () {
      shareEl.textContent = STR.copied;
      setTimeout(function () { shareEl.textContent = STR.share; }, 1700);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(location.href).then(done, function () {
        toolNoteEl.textContent = STR.copyReady;
      });
    } else {
      toolNoteEl.textContent = STR.copyReady;
    }
  });
  document.getElementById('saveHaul').addEventListener('click', function () {
    try {
      localStorage.setItem(LS_KEY, JSON.stringify({
        haul: haul, notoriety: notorietyEl.value,
        gearCost: gearEl.value, otherCost: otherEl.value, split: splitEl.value}));
      toolNoteEl.textContent = STR.saved;
    } catch (e) {
      toolNoteEl.textContent = STR.saveFailed;
    }
  });
  document.getElementById('restoreHaul').addEventListener('click', function () {
    try {
      var data = JSON.parse(localStorage.getItem(LS_KEY) || 'null');
      if (!data) { toolNoteEl.textContent = STR.noSaved; return; }
      haul = data.haul || [];
      var keys = ['notoriety', 'gearCost', 'otherCost', 'split'];
      for (var i = 0; i < keys.length; i++) {
        if (data[keys[i]] != null) document.getElementById(keys[i]).value = data[keys[i]];
      }
      renderHaul();
      persistState();
      toolNoteEl.textContent = STR.loadedSaved;
    } catch (e) {
      toolNoteEl.textContent = STR.loadFailed;
    }
  });
  document.getElementById('exportHaul').addEventListener('click', function () {
    var lvl = +notorietyEl.value;
    var rows = [['Item', 'Quantity', 'Base unit price', 'Est unit sale price', 'Est line sale price', 'Source']];
    for (var i = 0; i < haul.length; i++) {
      var x = haul[i];
      var s = findItem(x.id) || x;
      var p = priceAt(s, lvl);
      rows.push([s.en, x.qty, s.min, p === null ? '' : p, p === null ? '' : p * x.qty, s.url || STR.customSource]);
    }
    var csv = rows.map(function (r) {
      return r.map(function (v) { return '"' + String(v).replace(/"/g, '""') + '"'; }).join(',');
    }).join('\r\n');
    var link = document.createElement('a');
    link.href = URL.createObjectURL(new Blob([csv], {type: 'text/csv;charset=utf-8'}));
    link.download = 'rob-run-loot-profit.csv';
    link.click();
    setTimeout(function () { URL.revokeObjectURL(link.href); }, 1000);
  });
  document.getElementById('uploadCsv').addEventListener('change', function (e) {
    var file = e.target.files[0];
    if (!file) return;
    file.text().then(function (text) {
      var rows = convertRows(parseCSV(text));
      if (rows.length < 10) throw new Error(STR.importTooFew);
      setCatalog(rows, 'imported');
      notify(STR.imported.replace('{n}', fmtInt(rows.length)).replace('{file}', file.name), false);
    }).catch(function (err) {
      notify(STR.importFailed.replace('{msg}', err.message || ''), true);
    });
    e.target.value = '';
  });
  document.getElementById('resetData').addEventListener('click', function () { loadData(); });
  window.addEventListener('hashchange', updateFromHash);
  renderResults();
  renderHaul();
  loadData().then(updateFromHash);
})();
</script>
"""


def profit_page(lang):
    c = PROFIT[lang]
    hub = "/rob-run/" if lang == "en" else "/ru/rob-run/"
    not_opts = "".join(
        '<option value="%d">%s</option>' % (i + 1, o)
        for i, o in enumerate(c["not_opts"]))
    split_opts = "".join(
        '<option value="%d">%s</option>' % (i + 1, o)
        for i, o in enumerate(c["split_opts"]))
    cat_opts = (
        '<option value="all">%s</option>' % c["cat_all"]
        + '<option value="valuables">%s</option>' % c["cat_valuables"]
        + '<option value="cargo">%s</option>' % c["cat_cargo"]
        + '<option value="other">%s</option>' % c["cat_other"])
    faq_html = "".join(
        '<details%s><summary><h3>%s</h3>'
        '<span class="plus" aria-hidden="true">'
        '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6">'
        '<path d="M6 1v10M1 6h10"/></svg></span></summary><p>%s</p></details>'
        % (" open" if i == 0 else "", q, a)
        for i, (q, a) in enumerate(c["faq"]))
    body = (
        '<main id="main" class="wrap">%s'
        '<h1 class="page-h1">%s</h1><p class="page-lede">%s</p>'
        '<div class="checker">'
        '<p class="datanote" id="dataNotice" role="status">%s</p>'
        '<div class="profit-grid"><section>'
        '<h2>%s <span class="hint" id="resultCount"></span></h2>'
        '<div class="field-row search">'
        '<div><label for="search">%s</label>'
        '<input id="search" type="text" autocomplete="off" placeholder="%s"></div>'
        '<div><label for="category">%s</label><select id="category">%s</select></div>'
        '</div><p class="hint">%s</p>'
        '<div class="res-list" id="results"></div>'
        '<h2 class="sec-gap">%s</h2><p class="hint">%s</p>'
        '<div class="field-row">'
        '<div class="grow"><label for="customName">%s</label>'
        '<input id="customName" type="text" autocomplete="off" placeholder="%s"></div>'
        '<div><label for="customPrice">%s</label>'
        '<input id="customPrice" type="number" inputmode="decimal" min="0" value="0"></div>'
        '<div><label for="customQty">%s</label>'
        '<input id="customQty" type="number" inputmode="decimal" min="1" value="1"></div>'
        '</div><div class="actions">'
        '<button type="button" class="btn btn-primary" id="addCustom">%s</button>'
        '</div><p class="hint" id="customNote"></p>'
        '</section><section>'
        '<h2>%s</h2>'
        '<div class="actions" style="margin-top:0">'
        '<button type="button" class="btn btn-secondary" id="clearHaul">%s</button>'
        '<button type="button" class="btn btn-secondary" id="share">%s</button>'
        '</div>'
        '<div class="line-list" id="haul"></div>'
        '<div class="field-row two" style="margin-top:18px">'
        '<div><label for="notoriety">%s</label><select id="notoriety">%s</select></div>'
        '<div><label for="split">%s</label><select id="split">%s</select></div>'
        '</div>'
        '<div class="field-row two" style="margin-top:14px">'
        '<div><label for="gearCost">%s</label><input id="gearCost" type="number" inputmode="decimal" min="0" value="0"></div>'
        '<div><label for="otherCost">%s</label><input id="otherCost" type="number" inputmode="decimal" min="0" value="0"></div>'
        '</div>'
        '<p class="hint">%s</p>'
        '<div class="stats" style="margin-top:16px">'
        '<div class="stat"><em>%s</em><strong id="baseOut">0</strong><span>%s</span></div>'
        '<div class="stat"><em>%s</em><strong id="saleOut">0</strong><span>%s</span></div>'
        '<div class="stat"><em>%s</em><strong id="costOut">0</strong><span>%s</span></div>'
        '<div class="stat"><em>%s</em><strong id="netOut">0</strong><span>%s</span></div>'
        '<div class="stat"><em>%s</em><strong id="perOut">0</strong><span>%s</span></div>'
        '<div class="stat"><em>%s</em><strong id="ratioOut">—</strong><span>%s</span></div>'
        '</div><p class="hint" id="calcNotice"></p>'
        '<div class="actions">'
        '<button type="button" class="btn btn-secondary" id="exportHaul">%s</button>'
        '<button type="button" class="btn btn-secondary" id="saveHaul">%s</button>'
        '<button type="button" class="btn btn-secondary" id="restoreHaul">%s</button>'
        '</div><p class="hint" id="toolNote"></p>'
        '</section></div>'
        '<p class="hint">%s</p></div>'
        '<div class="note-box"><h2>%s</h2><p>%s</p>'
        '<p class="hint" id="dataMeta"></p>'
        '<div class="actions">'
        '<label class="btn btn-secondary" for="uploadCsv">%s</label>'
        '<input id="uploadCsv" type="file" accept=".csv,text/csv" hidden>'
        '<button type="button" class="btn btn-secondary" id="resetData">%s</button>'
        '</div><p class="hint">%s</p></div>'
        '<section class="faq" id="faq"><h2 class="sec">%s</h2>%s</section>'
        '<p class="data-line">%s</p></main>'
        % (crumbs_html(lang, [("ROB RUN", hub), (c["h1"], None)]),
           c["h1"], c["lede"],
           "Loading item database…" if lang == "en" else "Загрузка базы предметов…",
           c["find_h"], c["search_label"], c["search_ph"], c["cat_label"], cat_opts,
           c["results_hint"], c["custom_h"], c["custom_note"],
           c["name"], c["name"], c["price"], c["qty"], c["add_custom"],
           c["haul_h"], c["clear"], c["share"],
           c["notoriety"], not_opts, c["split"], split_opts,
           c["gear"], c["other"], c["cargo_note"],
           c["base"], c["cash"], c["sale"], c["cash"], c["costs"], c["cash"],
           c["net"], c["cash"], c["per"], c["cash"], c["ratio"], c["ratio_sub"],
           c["export"], c["save"], c["restore"], c["note"],
           c["data_h"], c["data_p"], c["import_label"], c["reset"], c["import_note"],
           c["faq_h"], faq_html, c["sources"]))
    if lang == "en":
        strings = {
            "lang": "en", "locale": "en-US", "rarity": RARITY_EN,
            "cash": c["cash"], "add": c["add"], "share": c["share"],
            "empty": "No items yet.",
            "needCustom": "Enter a name, a non-negative sale price and a quantity of at least 1.",
            "remove": "Remove", "unknown": "Unknown", "customTag": "custom",
            "each": "{p} each", "qtyFor": "Quantity for {n}",
            "noHaul": "No loot in your haul.",
            "estimates": "Values are estimates. Base and maximum source values are documented; intermediate levels use verified ladder patterns.",
            "unknownWarn": "Warning: {n} item(s) have no verified intermediate Notoriety-tier prices. They are excluded from this estimated payout; choose level 1 or 5, or enter an observed custom sale price.",
            "copied": "Link copied",
            "copyReady": "Link ready — select the address bar and press Ctrl+C to copy.",
            "saved": "Saved in this browser.",
            "saveFailed": "Local storage is unavailable. Use Copy share link.",
            "noSaved": "No saved haul found.",
            "loadedSaved": "Saved haul loaded.",
            "loadFailed": "Could not load the saved haul.",
            "offline": "Offline mode: {n} verified priced items loaded. The full 373-item database could not be loaded — check your connection and reload.",
            "full": "Loaded {total} catalogue entries, including {n} with published sale prices. Source version 0.7.0.",
            "countForms": ["{n} item", "{n} items", "{n} items"],
            "noMatch": "No matching priced item found. Try a different name or add a custom price.",
            "showing80": "Showing 80 of {n}. Narrow your search to find a specific item.",
            "imported": "Imported {n} priced entries from {file}. These values are available for the current session.",
            "importFailed": "CSV import failed: {msg}",
            "importTooFew": "The CSV has fewer than 10 priced rows, or the columns do not match the public items.csv format.",
            "dataMeta": "Loaded: {n} priced items. Source game-data version 0.7.0.",
            "dataMetaOff": "Limited built-in subset.",
            "customSource": "Custom",
        }
    else:
        strings = {
            "lang": "ru", "locale": "ru-RU", "rarity": {},
            "cash": c["cash"], "add": c["add"], "share": c["share"],
            "empty": "Пока пусто.",
            "needCustom": "Введите название, неотрицательную цену и количество не меньше 1.",
            "remove": "Убрать", "unknown": "Неизвестно", "customTag": "свой",
            "each": "{p} за шт.", "qtyFor": "Количество: {n}",
            "noHaul": "В добыче пока пусто.",
            "estimates": "Цены примерные. Базовые и максимальные цены взяты из источника; промежуточные уровни рассчитаны по проверенным множителям.",
            "unknownWarn": "Внимание: для {n} позиций нет подтверждённых цен для промежуточных уровней дурной славы. Они исключены из примерной выручки — выберите уровень 1 или 5 либо введите свою цену продажи.",
            "copied": "Ссылка скопирована",
            "copyReady": "Ссылка готова — выделите адресную строку и нажмите Ctrl+C.",
            "saved": "Сохранено в этом браузере.",
            "saveFailed": "Локальное хранилище недоступно. Используйте «Скопировать ссылку».",
            "noSaved": "Сохранённого списка нет.",
            "loadedSaved": "Сохранённый список загружен.",
            "loadFailed": "Не удалось загрузить сохранённый список.",
            "offline": "Офлайн-режим: загружено {n} проверенных предметов с ценой. Полную базу из 373 предметов загрузить не удалось — проверьте соединение и обновите страницу.",
            "full": "Загружено {total} записей каталога, из них {n} — с опубликованной ценой продажи. Версия источника 0.7.0.",
            "countForms": ["{n} предмет", "{n} предмета", "{n} предметов"],
            "noMatch": "Подходящих предметов с ценой не найдено. Попробуйте другой запрос или добавьте свой предмет.",
            "showing80": "Показано 80 из {n}. Уточните запрос, чтобы найти предмет.",
            "imported": "Импортировано {n} предметов с ценой из {file}. Действует только в этой сессии.",
            "importFailed": "Импорт не удался: {msg}",
            "importTooFew": "В CSV меньше 10 строк с ценой, или столбцы не совпадают с форматом открытого items.csv.",
            "dataMeta": "Загружено: {n} предметов с ценой. Версия игровых данных 0.7.0.",
            "dataMetaOff": "Ограниченная встроенная подборка.",
            "customSource": "Свой предмет",
        }
    js = PROFIT_JS.replace("__STR__", json.dumps(strings, ensure_ascii=False))
    js = js.replace("__OFFLINE__", json.dumps(_profit_offline(), ensure_ascii=False))
    return tool_page(lang, "loot-profit-calculator", c["title"], c["desc"], body + js, c["h1"])

# ---------------------------------------------------------------- squad split
SPLIT = {
    "en": {
        "title": "ROB RUN squad loot splitter — BuffForge",
        "desc": "Split a ROB RUN haul equally or by a weight you set for each player. The cash total is one you type.",
        "h1": "Squad loot splitter",
        "lede": "Enter the haul and the squad. Split it in equal shares, or type a weight for each player.",
        "pool": "Haul (cash)",
        "count": "Players",
        "equal": "Equal",
        "weighted": "Custom weights",
        "weight": "Weight",
        "player": "Player",
        "empty": "Enter how many players.",
        "bad_weight": "Weights can’t be negative. Use 0 to leave someone out.",
        "zero_weight": "At least one weight has to be above zero.",
        "capped": "This page lists up to 40 players.",
        "share": "Share",
        "total": "Shares add up to",
        "cash": "cash",
        "note": "Weights are yours — the game does not publish a split. Amounts are the cash you typed.",
        "sources": "No in-game split ratio is used. Cash wording follows Kefir’s FAQ. Reviewed 13 Nov 2026.",
    },
    "ru": {
        "title": "Делёж добычи в отряде ROB RUN — BuffForge",
        "desc": "Поделите добычу в ROB RUN поровну или по своему весу на каждого. Сумму в деньгах вводите вы.",
        "h1": "Делёж добычи в отряде",
        "lede": "Введите добычу и состав отряда. Делите поровну или укажите свой вес каждому игроку.",
        "pool": "Добыча (деньги)",
        "count": "Игроков",
        "equal": "Поровну",
        "weighted": "Свои веса",
        "weight": "Вес",
        "player": "Игрок",
        "empty": "Укажите, сколько игроков.",
        "bad_weight": "Вес не может быть отрицательным. Ноль — игрок ничего не получает.",
        "zero_weight": "Хотя бы один вес должен быть больше нуля.",
        "capped": "На странице не больше 40 игроков.",
        "share": "Доля",
        "total": "Доли в сумме",
        "cash": "деньги",
        "note": "Веса задаёте вы: в игре готовой схемы дележа нет. Сумма — те деньги, которые вы ввели.",
        "sources": "Игрового коэффициента дележа здесь нет. Слово «деньги» — из справки Kefir. Проверено 13 ноября 2026.",
    },
}

SPLIT_JS = r"""
<script>
(function () {
  var STR = __STR__;
  var MAX = 40;
  var mode = 'equal';
  var poolEl = document.getElementById('pool');
  var countEl = document.getElementById('count');
  var players = document.getElementById('players');
  var msg = document.getElementById('splitMsg');
  var out = document.getElementById('splitOut');
  var totalEl = document.getElementById('splitTotal');
  function num(v) {
    var n = parseFloat(v);
    return isFinite(n) ? n : NaN;
  }
  function fmt(cents) {
    return (cents / 100).toLocaleString(STR.locale, {maximumFractionDigits: 2});
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (ch) {
      return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[ch];
    });
  }
  function currentRows() {
    var rows = [];
    players.querySelectorAll('.player-row').forEach(function (row) {
      rows.push({name: row.querySelector('.name').value, weight: row.querySelector('.weight').value});
    });
    return rows;
  }
  function rebuild() {
    var raw = num(countEl.value);
    var prev = currentRows();
    if (!isFinite(raw)) {
      if (players.childElementCount) players.innerHTML = '';
      return null;
    }
    var n = Math.floor(raw);
    var capped = false;
    if (n > MAX) { n = MAX; countEl.value = String(MAX); capped = true; }
    if (n < 1) {
      if (players.childElementCount) players.innerHTML = '';
      return {n: n, capped: capped};
    }
    players.className = 'players' + (mode === 'equal' ? ' equal' : '');
    if (players.childElementCount === n) return {n: n, capped: capped};
    var html = '';
    for (var i = 0; i < n; i++) {
      var name = (prev[i] && prev[i].name) ? prev[i].name : (STR.player + ' ' + (i + 1));
      var weight = (prev[i] && prev[i].weight !== '') ? prev[i].weight : '1';
      html += '<div class="player-row"><input class="name" type="text" value="' + esc(name) +
        '" aria-label="' + STR.player + ' ' + (i + 1) + '">' +
        '<input class="weight w" type="number" inputmode="decimal" step="any" value="' + esc(weight) +
        '" aria-label="' + STR.weight + ' ' + (i + 1) + '"></div>';
    }
    players.innerHTML = html;
    players.className = 'players' + (mode === 'equal' ? ' equal' : '');
    players.querySelectorAll('input').forEach(function (el) {
      el.addEventListener('input', render);
    });
    return {n: n, capped: capped};
  }
  function splitCents(totalCents, weights) {
    var sum = 0;
    for (var i = 0; i < weights.length; i++) sum += weights[i];
    if (!(sum > 0)) return null;
    var base = [];
    var used = 0;
    for (var j = 0; j < weights.length; j++) {
      var share = Math.trunc(totalCents * weights[j] / sum);
      base.push(share);
      used += share;
    }
    var rem = totalCents - used;
    var order = [];
    for (var k = 0; k < weights.length; k++) {
      order.push({i: k, frac: Math.abs(totalCents * weights[k] / sum - base[k])});
    }
    order.sort(function (a, b) { return b.frac - a.frac; });
    var step = rem >= 0 ? 1 : -1;
    var left = Math.abs(rem);
    for (var t = 0; t < left; t++) base[order[t % order.length].i] += step;
    return base;
  }
  function render() {
    var info = rebuild();
    var pool = num(poolEl.value);
    if (!info || !isFinite(info.n) || info.n < 1) {
      msg.textContent = STR.empty;
      out.innerHTML = '';
      totalEl.textContent = '';
      return;
    }
    if (!isFinite(pool)) pool = 0;
    var weights = [];
    var names = [];
    players.querySelectorAll('.player-row').forEach(function (row) {
      names.push(row.querySelector('.name').value.trim() || STR.player);
      var w = num(row.querySelector('.weight').value);
      weights.push(mode === 'equal' ? 1 : (isFinite(w) ? w : 0));
    });
    if (weights.some(function (w) { return w < 0; })) {
      msg.textContent = STR.badWeight;
      out.innerHTML = '';
      totalEl.textContent = '';
      return;
    }
    var shares = splitCents(Math.round(pool * 100), weights);
    if (!shares) {
      msg.textContent = (info.capped ? STR.capped + ' ' : '') + STR.zeroWeight;
      out.innerHTML = '';
      totalEl.textContent = '';
      return;
    }
    msg.textContent = info.capped ? STR.capped : '';
    var html = '';
    var sum = 0;
    for (var i = 0; i < shares.length; i++) {
      sum += shares[i];
      html += '<div class="line-item"><span>' + esc(names[i]) + '</span><b>' + fmt(shares[i]) + '</b></div>';
    }
    out.innerHTML = html;
    totalEl.textContent = STR.total + ': ' + fmt(sum) + ' ' + STR.cash;
  }
  document.getElementById('modeEqual').addEventListener('click', function () {
    mode = 'equal';
    document.getElementById('modeEqual').setAttribute('aria-pressed', 'true');
    document.getElementById('modeWeight').setAttribute('aria-pressed', 'false');
    render();
  });
  document.getElementById('modeWeight').addEventListener('click', function () {
    mode = 'weighted';
    document.getElementById('modeEqual').setAttribute('aria-pressed', 'false');
    document.getElementById('modeWeight').setAttribute('aria-pressed', 'true');
    render();
  });
  countEl.addEventListener('input', render);
  poolEl.addEventListener('input', render);
  render();
})();
</script>
"""


def split_page(lang):
    c = SPLIT[lang]
    hub = "/rob-run/" if lang == "en" else "/ru/rob-run/"
    body = (
        '<main id="main" class="wrap narrow">%s'
        '<h1 class="page-h1">%s</h1><p class="page-lede">%s</p>'
        '<div class="checker"><div class="field-row">'
        '<div><label for="pool">%s</label>'
        '<input id="pool" type="number" inputmode="decimal" value="0"></div>'
        '<div><label for="count">%s</label>'
        '<input id="count" type="number" inputmode="numeric" min="1" max="40" step="1" value="4"></div>'
        '</div><div class="mode-row" role="group" aria-label="%s">'
        '<button type="button" class="btn btn-secondary" id="modeEqual" aria-pressed="true">%s</button>'
        '<button type="button" class="btn btn-secondary" id="modeWeight" aria-pressed="false">%s</button>'
        '</div><div class="players equal" id="players"></div>'
        '<p class="hint" id="splitMsg"></p>'
        '<div class="line-list" id="splitOut" aria-live="polite"></div>'
        '<p class="hint" id="splitTotal"></p>'
        '<p class="hint">%s</p></div>'
        '<p class="data-line">%s</p></main>'
        % (crumbs_html(lang, [("ROB RUN", hub), (c["h1"], None)]),
           c["h1"], c["lede"], c["pool"], c["count"], c["h1"],
           c["equal"], c["weighted"], c["note"], c["sources"])
    )
    strings = {
        "locale": "en-US" if lang == "en" else "ru-RU",
        "player": c["player"],
        "weight": c["weight"],
        "empty": c["empty"],
        "badWeight": c["bad_weight"],
        "zeroWeight": c["zero_weight"],
        "capped": c["capped"],
        "total": c["total"],
        "cash": c["cash"],
    }
    js = SPLIT_JS.replace("__STR__", json.dumps(strings, ensure_ascii=False))
    return tool_page(lang, "squad-loot-splitter", c["title"], c["desc"], body + js, c["h1"])


# ---------------------------------------------------------------- lag guide (RU only)
# Sources re-checked 14 Nov 2026:
# - Steam announcement 4 Nov 2026 (two regions: EU and East US).
# - Steam FAQ 13 Nov 2026 (server instability and DDoS, surrender to
#   change server, no Asia/Oceania servers before year end).
# - Kefir Help Center, troubleshooting: mouse polling rate, Steam file
#   verify, error E-0201, system requirements, surrender button.
# No EN counterpart. No hreflang. Language switch goes to the EN hub.
ANN_REGIONS = "https://steamcommunity.com/games/4262460/announcements/detail/712291399099220570"
ANN_FAQ = "https://steamcommunity.com/games/4262460/announcements/detail/717921532895036114"
HC_SECTION = "https://kefirgames.helpshift.com/hc/ru/14-rob-run/section/140-troubleshooting-and-support/"
HC_REQ = "https://kefirgames.helpshift.com/hc/ru/14-rob-run/faq/1375-what-are-the-system-requirements/"
HC_FILES = "https://kefirgames.helpshift.com/hc/ru/14-rob-run/faq/1376-the-game-won-t-load-or-keeps-freezing-what-should-i-do/"
HC_ERR = "https://kefirgames.helpshift.com/hc/ru/14-rob-run/faq/1377-what-should-i-do-if-i-get-an-error-code/"
HC_FPS = "https://kefirgames.helpshift.com/hc/ru/14-rob-run/faq/1383-what-should-i-do-if-my-fps-drops-drastically-when-moving-the-mouse/"
HC_SERVER = "https://kefirgames.helpshift.com/hc/ru/14-rob-run/faq/1382-how-to-invite-a-friend-to-a-party-if-it-says-they-are-on-another-server/"
LAGO_URL = "https://www.lagofastbooster.ru/games/rob-run/"
EXIT_URL = "https://www.exitlag.com/ru"
GEAR_URL = "https://www.gearupbooster.com/ru/"

LAG = {
    "en": {
        "title": "ROB RUN lag and high ping: how to reduce latency — BuffForge",
        "desc": "Why ROB RUN lags from Russia: only EU and East US. How to tell high ping from FPS drops, and what to do for free. LagoFast, ExitLag and GearUP — no prices.",
        "h1": "ROB RUN lag and high ping: how to reduce latency",
        "crumb": "Lag and high ping",
        "lede": "Latency from Russia usually comes down to the route to the server. Officially there are two regions; the server cities are not published.",
        "updated": "Updated: 15 November 2026",
        "hero_alt": "A heist in ROB RUN: a player with a bag at the counter, mini-map in the corner.",
        "route_aria": "From Russia the route to EU is shorter than to East US. No ping numbers and no server cities.",
        "route_origin": "Russia",
        "route_eu": "usually closer",
        "route_us": "farther",
        "route_caption": "Diagram without numbers: a longer route means higher latency. Server cities are not shown.",
        "net_h": "Network",
        "net_1": "High ping, rubber-banding, desync.",
        "net_2": "Many disconnect at once — that's the server.",
        "fps_h": "FPS",
        "fps_1": "Frames drop when you move the mouse.",
        "fps_2": "That's not ping.",
        "step1": "Global map",
        "step2": "Prison",
        "step3": "Surrender to the Feds",
        "world_alt": "ROB RUN global map: districts on one screen.",
        "prison_alt": "Prison in ROB RUN: the common hall and the sentence board.",
        "why_h": "Why it lags",
        "why_p1": "On 4 November 2026 Kefir wrote: \"ROB RUN currently has two regions: EU and East US.\" More regions were promised as capacity allows. The server cities are not named in the %s — and not on this page either.",
        "ann_label": "4 November 2026 announcement",
        "why_p2": "On 13 November 2026 the %s named server instability and DDoS attacks among the acute problems they are working through.",
        "faq_label": "FAQ",
        "amber": "If the server is unreachable because of DDoS, there is nothing you can do about it as a player. A booster does not fix that kind of outage either: it only changes the route to the official servers.",
        "not_in_html": "<p>If the game won't let you in, that's a different page: <a href=\"/rob-run/server-status/\">ROB RUN not working — servers and login</a>. It doesn't measure EU and shows no live status.</p>",
        "pingfps_h": "Ping or FPS?",
        "fact1_h": "High ping, rubber-banding, desync",
        "fact1_d": "Network: the route or the server.",
        "fact2_h": "Many players disconnect at once",
        "fact2_d": "Server. You can't fix that yourself.",
        "fact3_h": "FPS drops when you move the mouse",
        "fact3_d": "Not ping. Kefir's help pages say it is the mouse polling rate.",
        "fps_p": "If frames drop when you move the mouse, %s advises lowering the \"Polling rate\" in your mouse maker's software (Logitech, Razer, Bloody and others).",
        "fps_label": "Kefir's help pages",
        "files_p": "Verifying files in Steam, per %s: Properties → Installed Files → Verify integrity of game files.",
        "files_label": "Kefir's help pages",
        "err_p": "Error code E-0201 in the %s: the game was already running, the connection to the game server was lost and never came back. Kefir advises checking your connection and restarting the game.",
        "err_label": "error list",
        "section_p": "The whole section — %s.",
        "section_label": "Troubleshooting and support",
        "eu_h": "Pick EU",
        "eu_p1": "For players in Russia, EU is usually closer than East US. It makes sense to compare ping on EU first.",
        "eu_p2": "You can't change server during a raid. The 13 November 2026 FAQ says: \"To change server, you have to surrender and return to prison.\" %s describes the same step: open the global map, pick the \"Prison\" location and press \"Surrender to the Feds\". You change server from inside the prison.",
        "server_label": "Kefir's help pages",
        "regions_p": "Servers in other regions, for example Asia or Oceania, will not appear until at least the end of this year — that's what Kefir answered in the same FAQ.",
        "free_h": "Free: do it yourself",
        "free_items": [
            "Connect your computer with a cable, not over Wi-Fi.",
            "Pause background downloads and streams: Steam downloads, torrents, system updates.",
            "If your router has QoS or a gaming priority, turn it on for this computer.",
            "Restart your router.",
            "Verify the game files in Steam.",
            "Update your network card and graphics card drivers.",
            "Check your computer against the requirements below.",
        ],
        "req_p": "For both builds, %s lists 64-bit Windows 10 or newer, DirectX 11, an internet connection and 20 GB of disk space.",
        "req_label": "Kefir's help pages",
        "spec1_h": "Processor",
        "spec1_d": "Minimum: Intel i5-6600K or Ryzen 5 1600. Recommended: Intel i5-9600K or Ryzen 5 3600.",
        "spec2_h": "Memory",
        "spec2_d": "Minimum 12 GB. Recommended 16 GB.",
        "spec3_h": "Graphics card",
        "spec3_d": "Minimum: GTX 1050 Ti, RX 580 or Arc A380. Recommended: RTX 2070, RX 5700 XT or Arc B570.",
        "boosters_h": "Paid game boosters",
        "boosters_intro": "A paid booster routes ROB RUN traffic through its own nodes to the game's official servers. If the server itself is not responding, a booster will not fix that.",
        "booster_shared": "Routes ROB RUN traffic through its own nodes to the game's official servers.",
        "lago_tag": "3 hours",
        "lago_trial": "Trial: 3 hours from account creation, once per device.",
        "lago_lines": [
            ("Pro.", "Russian-language site and a dedicated ROB RUN page."),
            ("Pro.", "You can sign in with VK."),
            ("Con.", "The trial is only 3 hours."),
        ],
        "exit_tag": "3 days",
        "exit_trial": "Trial: 3 days, per the Russian trial page.",
        "exit_lines": [
            ("Pro.", "The longest trial of the three."),
            ("Pro.", "There are group plans."),
            ("Con.", "No dedicated ROB RUN page found — check the game list in the client."),
        ],
        "gear_tag": "free trial",
        "gear_trial": "Free trial and money-back guarantee — per the site.",
        "gear_lines": [
            ("Pro.", "The site has articles about ROB RUN."),
            ("Pro.", "Money-back guarantee — per the site."),
            ("Con.", "Before paying, check which payment methods the site accepts."),
        ],
        "cmp1_h": "Trial",
        "cmp1_d": "LagoFast — 3 hours, once per device. ExitLag — 3 days. GearUP — available, per the site.",
        "cmp2_h": "ROB RUN page",
        "cmp2_d": "LagoFast — yes. ExitLag — no dedicated page found. GearUP — has articles.",
        "cmp3_h": "Site in Russian",
        "cmp3_d": "LagoFast — yes. ExitLag — yes. GearUP — yes.",
        "prices_p": "Current prices and payment methods — on the official sites.",
        "test_p": "Test the trial on the same EU server at the same time: ping with the booster and without. If the server itself is not responding, a booster makes no difference.",
        "faq_h": "Frequently asked questions",
        "related_h": "ROB RUN tools",
        "related": [
            ("/rob-run/server-status/", "Official Steam server news",
             "Login and error codes. EU status is not shown here."),
            ("/rob-run/federal-raid-countdown/", "Federal Raid countdown",
             "Seven days from the server opening — in your time, Moscow time and UTC."),
            ("/rob-run/loot-profit-calculator/", "Loot profit calculator",
             "Add up the loot and subtract the costs. You enter the amounts."),
            ("/rob-run/squad-loot-splitter/", "Squad loot splitter",
             "Split equally, or set your own weight for each player."),
        ],
        "data_line": "BuffForge is an independent fan project. The site is not affiliated with Kefir or endorsed by the company. Official help: %s.",
        "data_label": "Troubleshooting and support for ROB RUN",
    },
    "ru": {
        "title": "ROB RUN лагает и высокий пинг: как уменьшить задержку — BuffForge",
        "desc": "Почему ROB RUN лагает из России: только EU и East US. Как отличить высокий пинг от FPS и что сделать бесплатно. LagoFast, ExitLag и GearUP — без цен.",
        "h1": "ROB RUN лагает и высокий пинг: как уменьшить задержку",
        "crumb": "Лаги и высокий пинг",
        "lede": "Из России задержка чаще упирается в маршрут до сервера. Официально регионов два, города площадок не опубликованы.",
        "updated": "Обновлено: 15 ноября 2026",
        "hero_alt": "Ограбление в ROB RUN: игрок с сумкой у стойки, в углу мини-карта.",
        "route_aria": "Из России путь до EU короче, чем до East US. Без цифр пинга и без городов серверов.",
        "route_origin": "Россия",
        "route_eu": "обычно ближе",
        "route_us": "дальше",
        "route_caption": "Схема без цифр: длиннее маршрут — выше задержка. Города серверов не показаны.",
        "net_h": "Сеть",
        "net_1": "Высокий пинг, «резинка», рассинхрон.",
        "net_2": "Многих отключает сразу — это сервер.",
        "fps_h": "FPS",
        "fps_1": "Кадры падают, когда двигаете мышь.",
        "fps_2": "Это не пинг.",
        "step1": "Глобальная карта",
        "step2": "«Тюрьма»",
        "step3": "«Сдаться федералам»",
        "world_alt": "Глобальная карта ROB RUN: районы на одном экране.",
        "prison_alt": "Тюрьма в ROB RUN: общий зал и табло со сроком.",
        "why_h": "Почему лагает",
        "why_p1": "4 ноября 2026 года Kefir написал: «Сейчас в ROB RUN доступны два региона: EU и East US». Другие регионы обещали добавлять по мере возможности. Города серверов в %s не названы — и на этой странице тоже.",
        "ann_label": "объявлении от 4 ноября 2026",
        "why_p2": "13 ноября 2026 года в %s разработчики назвали нестабильность серверов и DDoS-атаки среди острых проблем, которые они разбирают.",
        "faq_label": "FAQ",
        "amber": "Если сервер недоступен из-за DDoS, со стороны игрока это не исправить. Ускоритель такой отказ тоже не лечит: он только меняет маршрут до официальных серверов.",
        "not_in_html": "<p>Если не пускает в игру, это другая страница: <a href=\"/ru/rob-run/server-ne-rabotaet/\">ROB RUN не работает — серверы и вход</a>. Она не измеряет EU и не показывает живой статус.</p>",
        "pingfps_h": "Пинг или FPS?",
        "fact1_h": "Высокий пинг, «резинка», рассинхрон",
        "fact1_d": "Сеть: маршрут или сервер.",
        "fact2_h": "Многих отключает одновременно",
        "fact2_d": "Сервер. Со своей стороны это не исправить.",
        "fact3_h": "FPS падает, когда двигаете мышь",
        "fact3_d": "Не пинг. В справке Kefir это частота опроса мыши.",
        "fps_p": "Если кадры падают при движении мыши, %s советует снизить «Частоту опроса» в программе производителя мыши (Logitech, Razer, Bloody и другие).",
        "fps_label": "справка Kefir",
        "files_p": "Проверка файлов в Steam, по %s: Свойства → Установленные файлы → Проверить целостность файлов игры.",
        "files_label": "справке Kefir",
        "err_p": "Код E-0201 в %s: игра уже шла, связь с игровым сервером пропала и не восстановилась. Kefir советует проверить соединение и перезапустить игру.",
        "err_label": "списке ошибок",
        "section_p": "Весь раздел — %s.",
        "section_label": "устранение неполадок и поддержка",
        "eu_h": "Выберите EU",
        "eu_p1": "Для игроков из России EU обычно ближе, чем East US. Сравнивать пинг имеет смысл уже на EU.",
        "eu_p2": "Сменить сервер в рейде нельзя. В FAQ от 13 ноября 2026 года: «Чтобы сменить сервер, приходится сдаваться и возвращаться в тюрьму». %s описывает тот же шаг: откройте глобальную карту, выберите локацию «Тюрьма» и нажмите «Сдаться федералам». Сервер меняют уже из тюрьмы.",
        "server_label": "Справка Kefir",
        "regions_p": "Серверы в других регионах, например в Азии или Океании, как минимум до конца этого года не появятся — так Kefir ответил в том же FAQ.",
        "free_h": "Бесплатно: что сделать самому",
        "free_items": [
            "Подключите компьютер кабелем, не по Wi‑Fi.",
            "Поставьте на паузу фоновые загрузки и стримы: загрузки Steam, торренты, обновления системы.",
            "Если роутер умеет QoS или приоритет для игр, включите его для этого компьютера.",
            "Перезагрузите роутер.",
            "Проверьте целостность файлов игры в Steam.",
            "Обновите драйвер сетевой карты и видеокарты.",
            "Сверьте компьютер с требованиями ниже.",
        ],
        "req_p": "Для обеих сборок %s указывает 64-разрядную Windows 10 или новее, DirectX 11, интернет и 20 ГБ на диске.",
        "req_label": "справка Kefir",
        "spec1_h": "Процессор",
        "spec1_d": "Минимум: Intel i5-6600K или Ryzen 5 1600. Рекомендуется: Intel i5-9600K или Ryzen 5 3600.",
        "spec2_h": "Память",
        "spec2_d": "Минимум 12 ГБ. Рекомендуется 16 ГБ.",
        "spec3_h": "Видеокарта",
        "spec3_d": "Минимум: GTX 1050 Ti, RX 580 или Arc A380. Рекомендуется: RTX 2070, RX 5700 XT или Arc B570.",
        "boosters_h": "Платные игровые ускорители",
        "boosters_intro": "Платный ускоритель пропускает трафик ROB RUN через свои узлы к официальным серверам игры. Если не отвечает сам сервер, ускоритель это не исправит.",
        "booster_shared": "Пропускает трафик ROB RUN через свои узлы к официальным серверам игры.",
        "lago_tag": "3 часа",
        "lago_trial": "Пробный период: 3 часа с создания аккаунта, один раз на устройство.",
        "lago_lines": [
            ("Плюс.", "Сайт на русском и отдельная страница ROB RUN."),
            ("Плюс.", "Можно войти через VK."),
            ("Минус.", "Пробный период только 3 часа."),
        ],
        "exit_tag": "3 дня",
        "exit_trial": "Пробный период: 3 дня, по странице пробного периода на русском.",
        "exit_lines": [
            ("Плюс.", "Самый длинный пробный период из трёх."),
            ("Плюс.", "Есть тарифы для группы."),
            ("Минус.", "Отдельной страницы ROB RUN на сайте не нашли — список игр смотрите в клиенте."),
        ],
        "gear_tag": "пробный период",
        "gear_trial": "Бесплатный пробный период и гарантия возврата — по данным сайта.",
        "gear_lines": [
            ("Плюс.", "На сайте есть статьи про ROB RUN."),
            ("Плюс.", "Гарантия возврата — по данным сайта."),
            ("Минус.", "Перед оплатой проверьте, какие способы оплаты принимает сайт."),
        ],
        "cmp1_h": "Пробный период",
        "cmp1_d": "LagoFast — 3 часа, один раз на устройство. ExitLag — 3 дня. GearUP — есть, по данным сайта.",
        "cmp2_h": "Страница ROB RUN",
        "cmp2_d": "LagoFast — есть. ExitLag — отдельной страницы не найдено. GearUP — есть статьи.",
        "cmp3_h": "Сайт на русском",
        "cmp3_d": "LagoFast — да. ExitLag — да. GearUP — да.",
        "prices_p": "Актуальные цены и способы оплаты — на официальных сайтах.",
        "test_p": "Проверьте пробный период на одном и том же сервере EU в одно и то же время: пинг с ускорителем и без. Если не отвечает сам сервер, ускоритель разницы не даст.",
        "faq_h": "Частые вопросы",
        "related_h": "Инструменты ROB RUN",
        "related": [
            ("/ru/rob-run/server-ne-rabotaet/", "Сервер не работает",
             "Вход и коды ошибок. Статус EU здесь неизвестен."),
            ("/ru/rob-run/federal-raid-countdown/", "Отсчёт до Федеральной облавы",
             "Семь дней от открытия сервера — у вас, по Москве и в UTC."),
            ("/ru/rob-run/loot-profit-calculator/", "Калькулятор добычи",
             "Сложить добычу и вычесть расходы. Суммы вводите вы."),
            ("/ru/rob-run/squad-loot-splitter/", "Делёж добычи в отряде",
             "Поровну или со своим весом на каждого."),
        ],
        "data_line": "BuffForge — независимый фанатский проект. Сайт не связан с Kefir и не одобрен компанией. Официальная справка: %s.",
        "data_label": "устранение неполадок ROB RUN",
    },
}

LAG_FAQ = {
    "en": [
        ("Why does ROB RUN lag from Russia?",
         "Officially only EU and East US are available; the server cities are not named. From Russia, EU is usually closer. If the server is unreachable because of DDoS, home settings won't fix it."),
        ("Is it ping or an FPS drop?",
         "High ping, rubber-banding and mass disconnects mean network or server. If frames drop when you move the mouse, Kefir's help pages advise lowering the mouse polling rate. Error code E-0201 means the connection to the game server was lost: check your connection and restart the game."),
        ("How do I switch to the EU server?",
         "The 13 November 2026 Kefir FAQ says: \"To change server, you have to surrender and return to prison.\" The help pages say: global map, the \"Prison\" location, the \"Surrender to the Feds\" button, then change server from inside the prison."),
        ("Will a booster remove lag while the server is under DDoS?",
         "No. It only changes the route to the official servers. Compare ping on one EU server at one time, with the booster and without, on the trial. A server outage itself can't be fixed this way."),
    ],
    "ru": [
        ("Почему ROB RUN лагает из России?",
         "Официально доступны только EU и East US, города серверов не названы. Из России обычно ближе EU. Если сервер недоступен из-за DDoS, домашние настройки это не исправят."),
        ("Это пинг или просадка FPS?",
         "Высокий пинг, «резинка» и массовые отключения — сеть или сервер. Если кадры падают, когда двигаете мышь, справка Kefir советует снизить частоту опроса в программе мыши. Код E-0201 значит, что связь с игровым сервером пропала: проверьте соединение и перезапустите игру."),
        ("Как перейти на сервер EU?",
         "В FAQ Kefir от 13 ноября 2026 года: «Чтобы сменить сервер, приходится сдаваться и возвращаться в тюрьму». В справке: глобальная карта, локация «Тюрьма», кнопка «Сдаться федералам», затем смена сервера из тюрьмы."),
        ("Ускоритель уберёт лаги, если сервер под DDoS?",
         "Нет. Он только меняет маршрут до официальных серверов. Сравните пинг на одном сервере EU в одно время, с ускорителем и без, на пробном периоде. Отказ самого сервера так не лечится."),
    ],
}

# Kefir help center links, per language. The EN articles use the same
# FAQ IDs under /hc/en/ (verified 200 on 16 Nov 2026); the RU articles
# are the ones the RU guide already linked.
HC_LINKS = {
    "en": {
        "section": "https://kefirgames.helpshift.com/hc/en/14-rob-run/section/140-troubleshooting-and-support/",
        "req": "https://kefirgames.helpshift.com/hc/en/14-rob-run/faq/1375-what-are-the-system-requirements/",
        "files": "https://kefirgames.helpshift.com/hc/en/14-rob-run/faq/1376-the-game-won-t-load-or-keeps-freezing-what-should-i-do/",
        "err": "https://kefirgames.helpshift.com/hc/en/14-rob-run/faq/1377-what-should-i-do-if-i-get-an-error-code/",
        "fps": "https://kefirgames.helpshift.com/hc/en/14-rob-run/faq/1383-what-should-i-do-if-my-fps-drops-drastically-when-moving-the-mouse/",
        "server": "https://kefirgames.helpshift.com/hc/en/14-rob-run/faq/1382-how-to-invite-a-friend-to-a-party-if-it-says-they-are-on-another-server/",
    },
    "ru": {
        "section": HC_SECTION,
        "req": HC_REQ,
        "files": HC_FILES,
        "err": HC_ERR,
        "fps": HC_FPS,
        "server": HC_SERVER,
    },
}


def _src(href, label):
    return '<a href="%s">%s</a>' % (href, label)


def _ext(href, label):
    return '<a href="%s" rel="nofollow noopener" target="_blank">%s</a>' % (href, label)


def _booster(tag, name, trial, lines, href, host, lang):
    bits = "".join("<p><b>%s</b> %s</p>" % pair for pair in lines)
    return (
        '<article class="card"><p class="tag">%s</p><h3>%s</h3>'
        '<p>%s</p>'
        '<p class="meta">%s</p>%s'
        '<p class="go">%s</p></article>'
        % (tag, name, LAG[lang]["booster_shared"], trial, bits, _ext(href, host))
    )


def _shot(src, width, height, alt, lazy):
    extra = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return (
        '<figure class="shot"><img src="%s" width="%d" height="%d" alt="%s"%s>'
        '<figcaption>© Kefir</figcaption></figure>'
        % (src, width, height, alt, extra)
    )


def _guide_visuals(lang):
    """Original diagrams plus official Steam screenshots. Article sentences stay as written.

    The three .webp shots carry no Russian text (English in-game UI), so the
    same files serve both languages; only alt texts and diagram labels differ.
    """
    v = LAG[lang]
    hero = _shot(
        "/assets/rob-run/lag-hero.webp", 1600, 901,
        v["hero_alt"],
        False)
    route = (
        '<figure class="guide-visual"><div class="route" role="img" '
        'aria-label="%s">'
        '<div class="route-origin">%s</div>'
        '<div class="route-row"><div class="route-track near" aria-hidden="true"><i></i></div>'
        '<div class="route-end"><b>EU</b><span>%s</span></div></div>'
        '<div class="route-row"><div class="route-track far" aria-hidden="true"><i></i></div>'
        '<div class="route-end"><b>East US</b><span>%s</span></div></div>'
        '</div><figcaption>%s</figcaption></figure>'
        % (v["route_aria"], v["route_origin"], v["route_eu"], v["route_us"], v["route_caption"])
    )
    ping = (
        '<div class="ping-fps">'
        '<article class="ping-card net"><div class="ico" aria-hidden="true">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<path d="M5 12.5a8 8 0 0 1 14 0"/><path d="M8 14.2a4.2 4.2 0 0 1 8 0"/>'
        '<circle cx="12" cy="17" r="1.2" fill="currentColor" stroke="none"/></svg></div>'
        '<h3>%s</h3>'
        '<p>%s</p>'
        '<p>%s</p></article>'
        '<article class="ping-card fps"><div class="ico" aria-hidden="true">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/></svg></div>'
        '<h3>%s</h3>'
        '<p>%s</p>'
        '<p>%s</p></article></div>'
        % (v["net_h"], v["net_1"], v["net_2"], v["fps_h"], v["fps_1"], v["fps_2"])
    )
    arrow = (
        '<li class="step-arrow" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg></li>'
    )
    steps = (
        '<ol class="steps">'
        '<li class="step"><span class="step-n">1</span><b>%s</b></li>%s'
        '<li class="step"><span class="step-n">2</span><b>%s</b></li>%s'
        '<li class="step"><span class="step-n">3</span><b>%s</b></li>'
        '</ol>'
        % (v["step1"], arrow, v["step2"], arrow, v["step3"])
    )
    world = _shot(
        "/assets/rob-run/lag-map.webp", 1280, 720,
        v["world_alt"],
        True)
    prison = _shot(
        "/assets/rob-run/lag-prison.webp", 1280, 720,
        v["prison_alt"],
        True)
    return hero, route, ping, steps + world + prison


def lag_page(lang):
    """Lag guide, EN + RU. EN slug lag-and-high-ping, RU slug kak-ubrat-lagi."""
    c = LAG[lang]
    hc = HC_LINKS[lang]
    canon = "/rob-run/lag-and-high-ping/" if lang == "en" else "/ru/rob-run/kak-ubrat-lagi/"
    alt = {"en": "/rob-run/lag-and-high-ping/", "ru": "/ru/rob-run/kak-ubrat-lagi/"}
    switch = alt["ru"] if lang == "en" else alt["en"]
    hub = "/rob-run/" if lang == "en" else "/ru/rob-run/"
    home = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    hero, route, ping, server_art = _guide_visuals(lang)
    faq_html = "".join(
        '<details%s><summary><h3>%s</h3>'
        '<span class="plus" aria-hidden="true">'
        '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6">'
        '<path d="M6 1v10M1 6h10"/></svg></span></summary><p>%s</p></details>'
        % (" open" if i == 0 else "", q, a)
        for i, (q, a) in enumerate(LAG_FAQ[lang]))
    cards = (
        _booster(
            c["lago_tag"], "LagoFast", c["lago_trial"], c["lago_lines"],
            LAGO_URL, "www.lagofastbooster.ru/games/rob-run/", lang)
        + _booster(
            c["exit_tag"], "ExitLag", c["exit_trial"], c["exit_lines"],
            EXIT_URL, "www.exitlag.com/ru", lang)
        + _booster(
            c["gear_tag"], "GearUP Booster", c["gear_trial"], c["gear_lines"],
            GEAR_URL, "www.gearupbooster.com/ru/", lang)
    )
    free_html = "<ol>" + "".join("<li>%s</li>" % x for x in c["free_items"]) + "</ol>"
    related_html = "".join(
        '<a class="rel" href="%s"><b>%s</b><span>%s</span></a>' % (href, t, b)
        for href, t, b in c["related"])
    body = (
        '<main id="main" class="wrap narrow">%s'
        '<h1 class="page-h1">%s</h1>'
        '<p class="page-lede">%s</p>'
        '<p class="intro-note">%s</p>'
        '%s'
        '<div class="prose">'
        '<h2 class="sec">%s</h2>'
        '<p>%s</p>'
        '%s'
        '<p>%s</p>'
        '<div class="note-box amber"><p>%s</p></div>'
        '%s'
        '<h2 class="sec">%s</h2>'
        '<table class="fact-table">'
        '<tr><th>%s</th><td>%s</td></tr>'
        '<tr><th>%s</th><td>%s</td></tr>'
        '<tr><th>%s</th><td>%s</td></tr>'
        '</table>'
        '%s'
        '<p>%s</p>'
        '<p>%s</p>'
        '<p>%s</p>'
        '<p>%s</p>'
        '<h2 class="sec">%s</h2>'
        '<p>%s</p>'
        '<p>%s</p>'
        '%s'
        '<p>%s</p>'
        '<h2 class="sec">%s</h2>'
        '%s'
        '<p>%s</p>'
        '<table class="fact-table">'
        '<tr><th>%s</th><td>%s</td></tr>'
        '<tr><th>%s</th><td>%s</td></tr>'
        '<tr><th>%s</th><td>%s</td></tr>'
        '</table>'
        '<h2 class="sec">%s</h2>'
        '<p>%s</p>'
        '%s'
        '<table class="fact-table">'
        '<tr><th>%s</th><td>%s</td></tr>'
        '<tr><th>%s</th><td>%s</td></tr>'
        '<tr><th>%s</th><td>%s</td></tr>'
        '</table>'
        '<p>%s</p>'
        '<p>%s</p>'
        '<section class="faq" id="faq"><h2 class="sec">%s</h2>%s</section>'
        '</div>'
        '<section class="related"><h2>%s</h2><div class="related-grid">%s</div></section>'
        '<p class="data-line">%s</p></main>'
        % (crumbs_html(lang, [("ROB RUN", hub), (c["crumb"], None)]),
           c["h1"], c["lede"], c["updated"], hero,
           c["why_h"], c["why_p1"] % _src(ANN_REGIONS, c["ann_label"]), route,
           c["why_p2"] % _src(ANN_FAQ, c["faq_label"]),
           c["amber"], c["not_in_html"],
           c["pingfps_h"],
           c["fact1_h"], c["fact1_d"],
           c["fact2_h"], c["fact2_d"],
           c["fact3_h"], c["fact3_d"],
           ping,
           c["fps_p"] % _src(hc["fps"], c["fps_label"]),
           c["files_p"] % _src(hc["files"], c["files_label"]),
           c["err_p"] % _src(hc["err"], c["err_label"]),
           c["section_p"] % _src(hc["section"], c["section_label"]),
           c["eu_h"], c["eu_p1"],
           c["eu_p2"] % _src(hc["server"], c["server_label"]),
           server_art,
           c["regions_p"],
           c["free_h"], free_html,
           c["req_p"] % _src(hc["req"], c["req_label"]),
           c["spec1_h"], c["spec1_d"],
           c["spec2_h"], c["spec2_d"],
           c["spec3_h"], c["spec3_d"],
           c["boosters_h"], c["boosters_intro"], cards,
           c["cmp1_h"], c["cmp1_d"],
           c["cmp2_h"], c["cmp2_d"],
           c["cmp3_h"], c["cmp3_d"],
           c["prices_p"], c["test_p"],
           c["faq_h"], faq_html,
           c["related_h"], related_html,
           c["data_line"] % _src(hc["section"], c["data_label"]))
    )
    jl = [
        breadcrumb_jsonld(lang, [
            (home, home_path),
            ("ROB RUN", hub),
            (c["crumb"], canon),
        ]),
        {"@context": "https://schema.org", "@type": "Article",
         "headline": c["h1"], "description": c["desc"], "inLanguage": lang,
         "datePublished": "2026-11-14", "dateModified": "2026-11-15",
         "author": {"@type": "Organization", "name": "BuffForge", "url": BASE},
         "publisher": {"@type": "Organization", "name": "BuffForge", "url": BASE},
         "mainEntityOfPage": {"@type": "WebPage", "@id": BASE + canon}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [
             {"@type": "Question", "name": q,
              "acceptedAnswer": {"@type": "Answer", "text": a}}
             for q, a in LAG_FAQ[lang]]},
    ]
    return page(lang, c["title"], c["desc"], canon, alt, body, jsonld=jl,
                switch_path=switch, games=("rob-run",))


# ---------------------------------------------------------------- Failed to Enter Location guide (RU only)
# Draft: user-supplied RU text, 17 Nov 2026. Facts as written; Steam thread
# bodies are not readable anonymously (age wall), so thread claims are
# quoted from the draft, not re-verified. No screenshot: no verifiable
# in-game shot of this error was found (Steam threads walled, fan-blog
# images are app UI / key art, not the error screen) — page ships imageless.
FEL_THREAD_HOUSE = "https://steamcommunity.com/app/4262460/discussions/0/564799430246614512/"
FEL_THREAD_FEL = "https://steamcommunity.com/app/4262460/discussions/0/564799430246604432/"
FEL_THREAD_SETTLEMENT = "https://steamcommunity.com/app/4262460/discussions/0/564799430246612376/"
FEL_NEWS_HUB = "https://store.steampowered.com/news/app/4262460"

FEL_FAQ = [
    ("Почему ROB RUN не пускает в мой дом?",
     "Если другие районы открываются, а собственный дом недоступен, возможна проблема конкретной локации. Проверьте, воспроизводится ли ошибка у других участников группы, и посмотрите официальные сообщения о состоянии сервера."),
    ("Почему появляется Failed to Enter Location на EU-сервере?",
     "Причина может быть связана как с отдельной локацией, так и с общей нестабильностью сервера или соединения. В ноябре разработчики действительно подтверждали проблемы EU-региона, но точную причину конкретной ошибки нужно проверять отдельно."),
    ("Поможет ли переустановка ROB RUN?",
     "Нет подтверждений, что переустановка исправляет именно Failed to Enter Location. Сначала попробуйте перезапуск клиента и проверку файлов Steam. Если проблема возникает у нескольких игроков в одном поселении, переустановка вряд ли устранит серверный сбой."),
    ("Нужно ли менять сервер, если не получается зайти в дом?",
     "Не спешите. Смена сервера в ROB RUN связана с переходом через тюрьму и может затронуть ваш прогресс на текущем сервере. Не используйте её как первый способ исправления ошибки."),
    ("Что делать, если весь отряд не может войти на базу?",
     "Запишите сервер, идентификатор поселения, время ошибки и UID пострадавших игроков. Если остальные локации работают, сообщите о проблеме конкретного поселения в поддержку Kefir."),
    ("Как проверить, работают ли серверы ROB RUN?",
     "Посмотрите последние официальные объявления на странице новостей серверов ROB RUN на BuffForge. Помните, что новости о технических работах не равнозначны проверке доступности каждого игрового мира."),
]
# HTML variant of FAQ 6 only: the plain-text answer above is used for JSON-LD.
FEL_FAQ_HTML_6 = ('Посмотрите последние официальные объявления на '
                   '<a href="/ru/rob-run/server-ne-rabotaet/">странице новостей серверов ROB RUN на BuffForge</a>. '
                   "Помните, что новости о технических работах не равнозначны проверке доступности каждого игрового мира.")


def failed_location_page():
    """RU-only guide. No English page and no hreflang alternate."""
    canon = "/ru/rob-run/failed-to-enter-location/"
    title = "ROB RUN Failed to Enter Location: почему не получается зайти в дом и как исправить ошибку — BuffForge"
    desc = ("«Failed to enter location»: игра не смогла завершить переход в дом или поселение. "
            "Что значит ошибка, как проверить, где сбой, и что сделать.")
    h1 = "ROB RUN Failed to Enter Location: почему не получается зайти в дом и как исправить ошибку"
    crumb = "Failed to Enter Location: не пускает в дом"
    lede = ("«Failed to enter location» означает, что игра не смогла завершить переход в выбранную локацию. "
            "Если другие районы открываются, а не пускает только в дом или поселение, чаще всего проблема "
            "на стороне конкретной локации или в нестабильности EU-серверов, а не в вашем интернете: сначала "
            "проверьте, повторяется ли ошибка у других игроков и есть ли объявления Kefir, и только потом "
            "трогайте настройки и файлы.")
    status_a = _src("/ru/rob-run/server-ne-rabotaet/", "новости серверов ROB RUN на BuffForge")
    faq_html = "".join(
        '<details%s><summary><h3>%s</h3>'
        '<span class="plus" aria-hidden="true">'
        '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6">'
        '<path d="M6 1v10M1 6h10"/></svg></span></summary><p>%s</p></details>'
        % (" open" if i == 0 else "", q, FEL_FAQ_HTML_6 if i == 5 else a)
        for i, (q, a) in enumerate(FEL_FAQ))
    related_html = "".join(
        '<a class="rel" href="%s"><b>%s</b><span>%s</span></a>' % (href, t, b)
        for href, t, b in [
            ("/ru/rob-run/server-ne-rabotaet/", "Сервер не работает",
             "Вход и коды ошибок. Статус EU здесь неизвестен."),
            ("/ru/rob-run/federal-raid-countdown/", "Отсчёт до Федеральной облавы",
             "Семь дней от открытия сервера — у вас, по Москве и в UTC."),
            ("/ru/rob-run/loot-profit-calculator/", "Калькулятор добычи",
             "Сложить добычу и вычесть расходы. Суммы вводите вы."),
            ("/ru/rob-run/squad-loot-splitter/", "Делёж добычи в отряде",
             "Поровну или со своим весом на каждого."),
        ])
    sources_html = "".join("<li>%s</li>" % _ext(href, label) for href, label in [
        (FEL_THREAD_HOUSE, "Steam — I can't get into my house"),
        (FEL_THREAD_FEL, "Steam — Failed to enter location"),
        (FEL_THREAD_SETTLEMENT, "Steam — Problem with a specific settlement"),
        (FEL_NEWS_HUB, "ROB RUN — Official Steam news"),
    ]) + "<li>%s</li>" % _src("/ru/rob-run/server-ne-rabotaet/",
                               "ROB RUN — Official server announcements on BuffForge")
    body = (
        '<main id="main" class="wrap narrow">'
        + crumbs_html("ru", [("ROB RUN", "/ru/rob-run/"), (crumb, None)])
        + '<h1 class="page-h1">' + h1 + '</h1>'
        + '<p class="page-lede">' + lede + '</p>'
        + '<p class="intro-note">Обновлено: 17 ноября 2026</p>'
        + _shot("/assets/rob-run/fel-hero.webp", 1600, 901, "ROB RUN Failed to Enter Location ошибка при входе в дом", False)
        + '<div class="prose">'
        + '<h2 class="sec">Что означает Failed to Enter Location в ROB RUN?</h2>'
        + '<p>Сообщение <b>Failed to enter location</b> переводится как «Не удалось войти в локацию».</p>'
        + '<p>Оно означает, что игра не смогла завершить переход в выбранное место. Однако само сообщение не объясняет точную причину сбоя.</p>'
        + '<p>Игроки описывают несколько похожих ситуаций:</p>'
        + '<ul><li>Персонаж находится на карте, но не может войти в собственный дом.</li>'
        + '<li>Другие районы работают, а вход в конкретное поселение завершается ошибкой.</li>'
        + '<li>Несколько участников группы одновременно теряют доступ к общей базе.</li>'
        + '<li>После выхода из игры персонаж не может нормально вернуться в прежнюю локацию.</li></ul>'
        + '<p>Важно различать эти случаи: ошибка при входе в один дом и невозможность подключиться ко всему региону могут иметь разные причины.</p>'
        + '<h2 class="sec">Почему ROB RUN не пускает в дом или поселение?</h2>'
        + '<h3>1. Проблема с отдельной игровой локацией</h3>'
        + '<p>Это один из наиболее интересных случаев.</p>'
        + '<p>14 ноября пользователь Steam сообщил, что ROB RUN позволяет ему посещать другие районы, но не пускает именно туда, где находится его дом.</p>'
        + '<p>В другом обсуждении группа из трёх игроков рассказала, что все участники одновременно потеряли доступ к одному поселению, хотя остальная игра продолжала работать.</p>'
        + '<p>Если ситуация повторяется у нескольких игроков с разными интернет-подключениями, это серьёзный повод проверить работоспособность самой локации.</p>'
        + '<ul><li>' + _ext(FEL_THREAD_FEL, "Обсуждение ошибки Failed to Enter Location в Steam") + '</li>'
        + '<li>' + _ext(FEL_THREAD_SETTLEMENT, "Жалоба группы на недоступное поселение") + '</li></ul>'
        + '<h3>2. Нестабильная работа EU-серверов</h3>'
        + '<p>14 ноября разработчики ROB RUN из Kefir официально сообщили о проблемах со входом и стабильностью европейских серверов.</p>'
        + '<p>Команда занималась исправлением неполадок и объявила о перезапуске серверов.</p>'
        + '<p>Для игроков из России это особенно актуально, поскольку многие подключаются к европейскому региону.</p>'
        + '<p>Однако наличие общего сбоя EU-серверов не означает, что каждая ошибка Failed to Enter Location вызвана именно им.</p>'
        + '<p>Проверить публикации разработчиков можно на странице ' + status_a + '.</p>'
        + '<p>Она показывает официальные объявления Steam и помогает найти информацию о технических работах. Это не прямой тест доступности конкретного игрового сервера.</p>'
        + '<h3>3. Проблема с подключением или игровым клиентом</h3>'
        + '<p>Если ошибка появляется не только в одном доме, но и при переходах между разными районами, стоит проверить подключение и состояние игрового клиента.</p>'
        + '<p>Возможные факторы:</p>'
        + '<ul><li>нестабильное интернет-соединение;</li>'
        + '<li>кратковременная потеря связи с сервером;</li>'
        + '<li>устаревшая версия игры;</li>'
        + '<li>повреждённые или неполностью загруженные игровые файлы.</li></ul>'
        + '<p>Это общие возможные причины проблем с загрузкой и подключением, а не подтверждённые причины конкретного сообщения Failed to Enter Location.</p>'
        + '<figure class="guide-visual"><div class="route" role="img" '
        + 'aria-label="Диагностика: если другие районы открываются, проблема в конкретной локации; если не открывается ничего — в сервере или подключении.">'
        + '<div class="route-origin">Ошибка при входе</div>'
        + '<div class="route-row"><div class="route-track near" aria-hidden="true"><i></i></div>'
        + '<div class="route-end"><b>Другие районы открываются</b><span>Проблема в конкретной локации</span></div></div>'
        + '<div class="route-row"><div class="route-track far" aria-hidden="true"><i></i></div>'
        + '<div class="route-end"><b>Ничего не открывается</b><span>Сервер или подключение</span></div></div>'
        + '</div><figcaption>Если другие районы открываются, а дом нет — смотрите конкретную локацию; если не открывается ничего — проверяйте сервер и подключение.</figcaption></figure>'
        + '<h2 class="sec">Как исправить Failed to Enter Location в ROB RUN</h2>'
        + '<p>Начните с простых действий. Не стоит сразу переустанавливать игру или менять сервер.</p>'
        + '<h3>Способ 1. Проверьте, открываются ли другие районы</h3>'
        + '<p>Сначала попробуйте войти в другую доступную локацию.</p>'
        + '<div class="ping-fps">'
        + '<article class="ping-card net"><div class="ico" aria-hidden="true">'
        + '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        + '<path d="M5 12.5a8 8 0 0 1 14 0"/><path d="M8 14.2a4.2 4.2 0 0 1 8 0"/>'
        + '<circle cx="12" cy="17" r="1.2" fill="currentColor" stroke="none"/></svg></div>'
        + '<h3>Другие места работают</h3>'
        + '<p>Проверьте, могут ли ваши друзья войти в тот же дом или поселение.</p>'
        + '<p>Когда ошибка возникает только в одной точке, проблема может быть связана с этой локацией.</p></article>'
        + '<article class="ping-card fps"><div class="ico" aria-hidden="true">'
        + '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        + '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/></svg></div>'
        + '<h3>Не открывается ни одна локация</h3>'
        + '<p>Проверьте общее подключение к игровому региону и наличие свежих сообщений о технических неполадках.</p></article></div>'
        + '<p>Этот простой тест помогает понять, в каком направлении искать причину.</p>'
        + '<h3>Способ 2. Проверьте состояние серверов ROB RUN</h3>'
        + '<p>Откройте ' + status_a + ' и посмотрите последние официальные объявления разработчиков.</p>'
        + '<p>Обратите внимание на:</p>'
        + '<ul><li>сообщения о проблемах европейского региона;</li>'
        + '<li>объявления о перезапуске серверов;</li>'
        + '<li>технические работы;</li>'
        + '<li>сообщения об исправлениях и восстановлении доступа.</li></ul>'
        + '<p>Если разработчики уже подтвердили массовую проблему, разумнее дождаться восстановления работы сервиса, чем бесконечно менять настройки Windows.</p>'
        + '<div class="note-box amber"><p><b>Важно:</b> отсутствие новых объявлений не гарантирует, что ваш конкретный сервер или поселение работает нормально.</p></div>'
        + '<h3>Способ 3. Полностью перезапустите ROB RUN</h3>'
        + '<p>Если сервер уже восстановился после технических работ, попробуйте заново подключиться.</p>'
        + '<ol class="steps five">'
        + '<li class="step"><span class="step-n">1</span><b>Полностью закройте ROB RUN.</b></li>'
        + '<li class="step"><span class="step-n">2</span><b>Убедитесь, что игра завершила работу.</b></li>'
        + '<li class="step"><span class="step-n">3</span><b>Перезапустите Steam.</b></li>'
        + '<li class="step"><span class="step-n">4</span><b>Запустите ROB RUN из библиотеки Steam.</b></li>'
        + '<li class="step"><span class="step-n">5</span><b>Повторите попытку входа в нужную локацию.</b></li>'
        + '</ol>'
        + '<p>Перезапуск может помочь устранить временную проблему игрового сеанса. Но если конкретная локация недоступна на стороне сервера, он не гарантирует результат.</p>'
        + '<h3>Способ 4. Проверьте целостность игровых файлов</h3>'
        + '<p>Если вместе с Failed to Enter Location возникают зависания, ошибки загрузки или другие проблемы клиента, выполните проверку файлов:</p>'
        + '<ol><li>Откройте Steam.</li>'
        + '<li>Перейдите в библиотеку игр.</li>'
        + '<li>Нажмите правой кнопкой мыши на ROB RUN.</li>'
        + '<li>Откройте «Свойства».</li>'
        + '<li>Выберите «Установленные файлы».</li>'
        + '<li>Нажмите «Проверить целостность файлов игры».</li></ol>'
        + '<p>Steam проверит локальные файлы и при необходимости загрузит отсутствующие или повреждённые данные.</p>'
        + '<p>Этот способ подходит для проверки состояния клиента, но не исправляет неисправную серверную локацию.</p>'
        + '<h3>Способ 5. Проверьте проблему вместе с друзьями</h3>'
        + '<p>Если вы играете группой, попросите других участников попробовать попасть в то же поселение.</p>'
        + '<p>Затем сравните результаты:</p>'
        + '<table class="fact-table">'
        + '<tr><th>Только один человек не может войти</th><td>Проверьте его клиент и подключение.</td></tr>'
        + '<tr><th>Несколько игроков не могут войти в одно поселение, но могут посещать другие места</th><td>Есть основания подозревать проблему конкретной локации.</td></tr>'
        + '<tr><th>У нескольких игроков одновременно перестали открываться разные районы</th><td>Проверьте объявления о сбоях игрового сервера.</td></tr>'
        + '</table>'
        + '<p>Такая проверка особенно полезна перед обращением в техническую поддержку.</p>'
        + '<h2 class="sec">Что делать, если ничего не помогает?</h2>'
        + '<p>Если ошибка сохраняется, а доступ к важной базе отсутствует, лучше передать подробную информацию разработчикам.</p>'
        + '<p>Подготовьте:</p>'
        + '<ul><li>ваш игровой UID;</li>'
        + '<li>название региона и сервера;</li>'
        + '<li>название или идентификатор поселения;</li>'
        + '<li>примерное время появления ошибки;</li>'
        + '<li>полный текст сообщения;</li>'
        + '<li>скриншот или видео;</li>'
        + '<li>информацию о том, могут ли другие участники группы войти в эту локацию.</li></ul>'
        + '<p>UID можно найти в игровом интерфейсе, открыв меню Esc и воспользовавшись функцией копирования идентификатора.</p>'
        + '<p>Передайте сведения через ' + _src(HC_SECTION, "официальный центр поддержки Kefir") + '. Чем точнее данные о сервере и месте сбоя, тем проще проверить проблему.</p>'
        + '<p>Не публикуйте личные данные или данные входа в Steam в открытых обсуждениях.</p>'
        + '<h2 class="sec">Может ли Failed to Enter Location быть связан с читерами?</h2>'
        + '<p>В одном из обсуждений Steam игроки предположили, что недоступность их поселения могла возникнуть после действий другого пользователя.</p>'
        + '<p>Они описали одновременное отключение нескольких участников группы и последующую невозможность войти на базу.</p>'
        + '<p>Однако это <b>подозрение игроков, а не подтверждённый разработчиками способ атаки</b>.</p>'
        + '<p>На данный момент недостаточно оснований утверждать, что ошибка Failed to Enter Location обязательно связана с читами или намеренной блокировкой поселений.</p>'
        + '<p>Если вы подозреваете злоупотребление игровой механикой, сохраните время инцидента, сервер и видеозапись для обращения в поддержку.</p>'
        + '<section class="faq" id="faq"><h2 class="sec">Частые вопросы</h2>' + faq_html + '</section>'
        + '<h2 class="sec">Итоги</h2>'
        + '<p>Ошибка <b>Failed to Enter Location в ROB RUN</b> не всегда означает проблему с интернетом.</p>'
        + '<p>Если вы можете играть, открывать карту и перемещаться между районами, но не можете попасть в собственный дом, сначала проверьте, возникает ли та же ошибка у других игроков.</p>'
        + '<p>Если недоступен весь регион, начните с официальных объявлений о состоянии серверов.</p>'
        + '<p>Не переустанавливайте игру и не меняйте сервер без необходимости. В случае устойчивой ошибки одной локации соберите информацию и обратитесь к разработчикам.</p>'
        + '<p><b>Полезный инструмент:</b> ' + _src("/ru/rob-run/server-ne-rabotaet/", "Проверить новости и состояние серверов ROB RUN — BuffForge") + '</p>'
        + '<h2 class="sec">Источники</h2><ul>' + sources_html + '</ul>'
        + '</div>'
        + '<section class="related"><h2>Инструменты ROB RUN</h2><div class="related-grid">' + related_html + '</div></section>'
        + '<p class="data-line">BuffForge — независимый фанатский проект. Сайт не связан с Kefir и не одобрен компанией. Официальная справка: '
        + _src(HC_SECTION, "устранение неполадок ROB RUN") + '.</p></main>'
    )
    jl = [
        breadcrumb_jsonld("ru", [
            ("Главная", "/ru/"),
            ("ROB RUN", "/ru/rob-run/"),
            (crumb, canon),
        ]),
        {"@context": "https://schema.org", "@type": "Article",
         "headline": h1, "description": desc, "inLanguage": "ru",
         "datePublished": "2026-11-17", "dateModified": "2026-11-17",
         "author": {"@type": "Organization", "name": "BuffForge", "url": BASE},
         "publisher": {"@type": "Organization", "name": "BuffForge", "url": BASE},
         "mainEntityOfPage": {"@type": "WebPage", "@id": BASE + canon}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [
             {"@type": "Question", "name": q,
              "acceptedAnswer": {"@type": "Answer", "text": a}}
             for q, a in FEL_FAQ]},
    ]
    return page("ru", title, desc, canon, None, body, jsonld=jl,
                switch_path="/rob-run/", games=("rob-run",))


# ---------------------------------------------------------------- wipe planner
# Design: user-supplied desktop mock, 18 Nov 2026. Facts re-checked 18 Nov 2026:
# - Kefir FAQ (EN + RU, read directly): every 7 days plots, bases, weapons
#   and cash are wiped into jail time and authority; cosmetics, player name,
#   tutorial progress, settings and accumulated jail time carry over.
# - Official Telegram 11 Nov 2026 (t.me/robrungame/67, read directly):
#   confiscated: clean money, things, vehicles, real estate, land, unlocked
#   skill-tree items, recorded clan spending, bribes. Kept: all cosmetics,
#   B-coin balance, appearance and character name, tutorial progress,
#   settings, accumulated jail time. "Things" is too vague for its own row;
#   clean money and land fold into the Cash and Plots rows.
# - ROB RUN Info FAQ (community, robrun.info/faq, read directly): keeps on
#   the character are tattoos, Authority level, purchased skins, B-coins,
#   premium. Skins fold into the Cosmetics row; B-coins already covered by
#   the Telegram post. The jail-time formula on that page is NOT used:
#   Kefir has not published it, and the tool never estimates conversion.
# Library is 19 verified rows. The mock shows "22 results" but only 4 rows
# are visible; nothing is invented to reach 22 — the count shown is the
# number actually in the library.
WIPE_FAQ_EN = "https://kefirgames.helpshift.com/hc/en/14-rob-run/faq/1346-what-is-the-federal-raid-wipe/?l=en"
WIPE_FAQ_RU = "https://kefirgames.helpshift.com/hc/ru/14-rob-run/faq/1346-what-is-the-federal-raid-wipe/?l=ru"
WIPE_TG67 = "https://t.me/robrungame/67"
WIPE_INFO_FAQ = "https://robrun.info/faq/"

WIPE_ITEMS = [
    {"id": "cash", "out": "resets", "ev": "official",
     "name": {"en": "Cash / money", "ru": "Деньги"},
     "desc": {"en": "Kefir confirms that cash is wiped during the Federal Raid.",
              "ru": "Kefir подтверждает: деньги сбрасываются во время Федеральной облавы."},
     "kw": ["money", "bank", "cash", "деньги", "банк"]},
    {"id": "weapons", "out": "resets", "ev": "official",
     "name": {"en": "Weapons", "ru": "Оружие"},
     "desc": {"en": "Weapons are listed in the official wipe reset rule.",
              "ru": "Оружие указано в официальном правиле сброса."},
     "kw": ["guns", "gear", "оружие"]},
    {"id": "plots", "out": "resets", "ev": "official",
     "name": {"en": "Land plots / claims", "ru": "Земельные участки"},
     "desc": {"en": "All plots are wiped at the Federal Raid. The Nov 11 developer post also names land among the confiscated property.",
              "ru": "Все участки сбрасываются во время Федеральной облавы. В посте разработчиков от 11 ноября земля также названа среди конфискованного имущества."},
     "kw": ["land", "claims", "settlement", "земля", "участок", "поселение"]},
    {"id": "base", "out": "resets", "ev": "official",
     "name": {"en": "Base / house / built structures", "ru": "База / дом / постройки"},
     "desc": {"en": "Bases are wiped. Items not explicitly named by Kefir are separately categorized.",
              "ru": "Базы сбрасываются. Предметы, прямо не названные Kefir, отнесены в отдельные категории."},
     "kw": ["house", "structures", "buildings", "дом", "постройки", "здания"]},
    {"id": "cosmetics", "out": "keeps", "ev": "official",
     "name": {"en": "Cosmetics", "ru": "Косметика"},
     "desc": {"en": "Kefir lists cosmetics among the things that carry over.",
              "ru": "Kefir называет косметику среди того, что сохраняется."},
     "kw": ["skins", "скины", "косметика"]},
    {"id": "player-name", "out": "keeps", "ev": "official",
     "name": {"en": "Player name", "ru": "Ник"},
     "desc": {"en": "Your player name carries over.",
              "ru": "Ваш ник сохраняется."},
     "kw": ["nickname", "name", "ник", "имя"]},
    {"id": "tutorial", "out": "keeps", "ev": "official",
     "name": {"en": "Tutorial progress", "ru": "Прогресс обучения"},
     "desc": {"en": "Tutorial progress carries over.",
              "ru": "Прогресс обучения сохраняется."},
     "kw": ["tutorial", "обучение"]},
    {"id": "settings", "out": "keeps", "ev": "official",
     "name": {"en": "Settings", "ru": "Настройки"},
     "desc": {"en": "Settings carry over.",
              "ru": "Настройки сохраняются."},
     "kw": ["keybinds", "options", "настройки"]},
    {"id": "jail-time", "out": "keeps", "ev": "official",
     "name": {"en": "Accumulated jail time", "ru": "Накопленный тюремный срок"},
     "desc": {"en": "Accumulated jail time carries over — and wiped assets are converted into more of it.",
              "ru": "Накопленный тюремный срок сохраняется, а сброшенные активы конвертируются в дополнительный срок."},
     "kw": ["sentence", "prison", "срок", "тюрьма"]},
    {"id": "vehicles", "out": "resets", "ev": "developer",
     "name": {"en": "Vehicles", "ru": "Транспорт"},
     "desc": {"en": "The 11 Nov developer post names vehicles among the confiscated property.",
              "ru": "В посте разработчиков от 11 ноября транспорт назван среди конфискованного имущества."},
     "kw": ["cars", "car", "машины", "авто", "транспорт"]},
    {"id": "real-estate", "out": "resets", "ev": "developer",
     "name": {"en": "Real estate", "ru": "Недвижимость"},
     "desc": {"en": "Named as confiscated in the 11 Nov developer post.",
              "ru": "Названа конфискованной в посте разработчиков от 11 ноября."},
     "kw": ["property", "house", "apartment", "недвижимость", "дом"]},
    {"id": "skill-tree", "out": "resets", "ev": "developer",
     "name": {"en": "Unlocked skill-tree items", "ru": "Открытые предметы древа"},
     "desc": {"en": "Named as confiscated in the 11 Nov developer post.",
              "ru": "Названы конфискованными в посте разработчиков от 11 ноября."},
     "kw": ["research", "skills", "tree", "исследования", "древо", "навыки"]},
    {"id": "clan-spending", "out": "resets", "ev": "developer",
     "name": {"en": "Recorded clan spending", "ru": "Учтенные траты на клан"},
     "desc": {"en": "Named as confiscated in the 11 Nov developer post.",
              "ru": "Названы конфискованными в посте разработчиков от 11 ноября."},
     "kw": ["clan", "клан"]},
    {"id": "bribes", "out": "resets", "ev": "developer",
     "name": {"en": "Bribes", "ru": "Взятки"},
     "desc": {"en": "Named as confiscated in the 11 Nov developer post.",
              "ru": "Названы конфискованными в посте разработчиков от 11 ноября."},
     "kw": ["bribe", "взятки", "взятка"]},
    {"id": "bcoins", "out": "keeps", "ev": "developer",
     "name": {"en": "B-coin balance", "ru": "Баланс B-coins"},
     "desc": {"en": "The 11 Nov developer post says the B-coin balance is kept.",
              "ru": "В посте разработчиков от 11 ноября сказано, что баланс B-coins сохраняется."},
     "kw": ["b-coins", "currency", "b-coins", "валюта"]},
    {"id": "appearance", "out": "keeps", "ev": "developer",
     "name": {"en": "Character appearance", "ru": "Внешность персонажа"},
     "desc": {"en": "The 11 Nov developer post lists appearance among the things that are kept.",
              "ru": "В посте разработчиков от 11 ноября внешность названа среди сохраняемого."},
     "kw": ["face", "look", "внешность", "лицо"]},
    {"id": "tattoos", "out": "keeps", "ev": "community",
     "name": {"en": "Tattoos", "ru": "Татуировки"},
     "desc": {"en": "The community FAQ lists tattoos as staying on the character.",
              "ru": "В FAQ сообщества татуировки указаны как сохраняющиеся на персонаже."},
     "kw": ["tattoo", "ink", "татуировки", "тату"]},
    {"id": "authority", "out": "keeps", "ev": "community",
     "name": {"en": "Authority level", "ru": "Уровень авторитета"},
     "desc": {"en": "The community FAQ says the Authority level stays on the character.",
              "ru": "В FAQ сообщества сказано, что уровень авторитета остаётся на персонаже."},
     "kw": ["authority", "level", "rank", "авторитет", "уровень"]},
    {"id": "premium", "out": "keeps", "ev": "community",
     "name": {"en": "Premium status", "ru": "Премиум-статус"},
     "desc": {"en": "The community FAQ lists premium as staying on the character.",
              "ru": "В FAQ сообщества премиум указан как сохраняющийся на персонаже."},
     "kw": ["premium", "премиум"]},
]

WIPE = {
    "en": {
        "title": "ROB RUN Wipe Checker: What Resets & What Stays? | BuffForge",
        "desc": "ROB RUN wipes every 7 days. Check what resets after a Federal Raid, what carries over, and make a free pre-wipe checklist for your server. No login required.",
        "h1": "ROB RUN Wipe: What Do You Lose or Keep?",
        "eyebrow": "ROB RUN · Federal Raid tool",
        "hero_a": "Know ",
        "hero_b": "what you keep.",
        "hero_c": " Plan what comes next.",
        "lede": "Search the wipe rules, mark the assets that matter to you, and get your next Federal Raid checklist ready. Real sources. Your own data. No game login.",
        "rule_kicker": "Official rule · Kefir",
        "rule_h": "Every 7 days",
        "rule_p": "The Federal Raid resets server-held property. Your accumulated jail time and a small set of character progress carry over. Each server has its own clock.",
        "rule_link": "Read the official FAQ",
        "chips": ["Rules reviewed 18 Nov 2026", "Official / community sources labeled", "Saved in your browser", "No account required"],
        "ws_h": "Your wipe workspace",
        "server_label": "Server",
        "server_default": "My server",
        "server_n": "Server",
        "new_server": "+ New server",
        "delete_server": "Delete",
        "del_confirm": "Delete this server profile and everything tracked in it?",
        "stat_reset": "Your reset items",
        "stat_reset_sub": "Tracked types, not item count",
        "stat_kept": "Your saved progress",
        "stat_kept_sub": "Tracked things that carry over",
        "stat_manual": "Check manually",
        "stat_manual_sub": "Rules not firmly confirmed",
        "stat_check": "Checklist complete",
        "stat_check_sub": "{done} / {total} tasks",
        "lib_h": "What resets? What stays?",
        "lib_badge": "Source-checked",
        "lib_lede": "Search an item or progress type, then add it to your personal wipe list.",
        "lib_notice": "Confirmed facts are taken from Kefir's official FAQ. Other details are clearly marked as developer announcements, community guidance, or unverified. Do not treat unknown as safe.",
        "search_label": "Search items",
        "search_ph": "Search: cars, cash, tattoos, research…",
        "clear": "Clear",
        "f_all": "All",
        "f_resets": "Resets",
        "f_keeps": "Keeps",
        "f_unconf": "Unconfirmed",
        "lib_list_h": "Item / progress library",
        "results": "{n} results",
        "tracked_h": "My tracked items",
        "tracked_empty": "Nothing tracked yet. Use “+ Track” above to make your personal keep / lose list.",
        "custom_h": "Can't find an item? Add your own for manual verification.",
        "custom_ph": "e.g. Unclaimed shipment",
        "custom_add": "+ Track item",
        "custom_need": "Type an item name first.",
        "lib_foot": "The numbers above count things you chose to track, not your in-game balance. The tool never reads game inventory.",
        "target_h": "My Federal Raid target",
        "target_lede": "Optional: enter the wipe time shown in your game to plan around it.",
        "target_label": "My in-game wipe date & time",
        "target_clear": "Clear",
        "target_none": "No deadline entered",
        "target_none_sub": "Enter the actual raid time if your game shows it.",
        "target_note": "This is your manually entered deadline, not a live server lookup. If the raid time changes, update it here. Check the in-game timer for the authoritative time.",
        "target_link": "Need to estimate it from server opening? Use BuffForge's existing Federal Raid countdown",
        "target_passed": "This raid time has passed.",
        "summary_h": "Your plan summary",
        "summary_lede": "Useful before switching servers or logging off.",
        "summary_empty": "No items tracked yet. {done} of {total} prep tasks complete.",
        "copy": "Copy summary",
        "copied": "Summary copied",
        "print": "Print / PDF",
        "backup_h": "Backup and restore",
        "export": "Export JSON",
        "import": "Import JSON",
        "backup_note": "Stored only in this browser with localStorage. Browser data can be cleared; export a backup if it matters to you.",
        "import_ok": "Backup imported.",
        "import_bad": "That file is not a valid wipe-planner backup.",
        "sources_h": "Rules & sources",
        "sources_lede": "Primary source first. Unknowns stay unknown.",
        "review_note": "Last editorial review: 18 November 2026. Early-access rules can change without notice. If sources conflict, trust newer official information and the in-game interface.",
        "check_h": "Your pre-wipe checklist",
        "check_lede": "Suggested preparation steps, plus any tasks you add. Nothing is sent to a server.",
        "check_progress": "Preparation progress",
        "check_done": "{done} / {total} done",
        "check_add_ph": "Add your own pre-wipe task",
        "check_add": "Add task",
        "check_foot": "This is a personal planning checklist. Completing tasks here does not change anything in ROB RUN.",
        "faq_h": "ROB RUN wipe questions, answered",
        "sources": "Wipe rules: Kefir FAQ “What is the Federal Raid (Wipe)?” (reviewed 18 Nov 2026); extra items: official Telegram post, 11 Nov 2026; community FAQ: ROB RUN Info. BuffForge is an independent fan project, not affiliated with Kefir.",
        "track": "+ Track",
        "tracked": "✓ Tracked",
        "remove": "Remove",
        "resets": "Resets",
        "keeps": "Keeps",
        "unconf": "Unconfirmed",
        "ev_official": "Official",
        "ev_developer": "Developer",
        "ev_community": "Community",
        "ev_unconf": "Unconfirmed",
        "src_faq": "Kefir FAQ",
        "src_tg": "Nov 11 post",
        "src_info": "ROB RUN Info FAQ",
        "units": ["d", "h", "m", "s"],
        "tasks": [
            ("Check the Federal Raid timer in-game", "Use your server's own timer, not a global reset guess."),
            ("Record server number and region", "Useful if your squad plans to regroup next cycle."),
            ("Review cash, weapons, plots and bases", "Kefir confirms these are wiped."),
            ("Verify any uncertain items or unclaimed rewards", "Use in-game information and up-to-date official announcements."),
            ("Note your jail time / Authority progress", "Record a before/after reference for the next cycle."),
            ("Agree on a next server with your squad", "Optional if you play with friends."),
        ],
        "faq": [
            ("What disappears during the Federal Raid?",
             "Officially: plots, bases, weapons, and cash are wiped. Confiscated holdings are converted into jail time and Authority. The tool does not estimate that conversion."),
            ("What definitely carries over?",
             "Kefir lists cosmetics, player name, tutorial progress, settings, and accumulated jail time. Other items receive a separate evidence label in the checker."),
            ("Is every server wiped at the same time?",
             "No. ROB RUN has a seven-day cycle for each server, rather than a single worldwide reset hour. Check your own server timer."),
            ("Does BuffForge read my account or items?",
             "No. You select what to track. The list and checklist stay on this device unless you export them. There is no live game data or account connection."),
        ],
    },
    "ru": {
        "title": "Проверка вайпа ROB RUN: что сбрасывается и что остаётся | BuffForge",
        "desc": "Вайп в ROB RUN — каждые 7 дней. Проверьте, что сбрасывается после Федеральной облавы, что остаётся, и составьте бесплатный чек-лист перед вайпом для вашего сервера. Без регистрации.",
        "h1": "Вайп ROB RUN: что вы теряете, а что сохраняете?",
        "eyebrow": "ROB RUN · Инструмент Федеральной облавы",
        "hero_a": "Знайте, ",
        "hero_b": "что сохраните.",
        "hero_c": " Планируйте, что будет дальше.",
        "lede": "Найдите правила вайпа, отметьте важное для вас имущество и подготовьте чек-лист к следующей Федеральной облаве. Настоящие источники. Ваши данные. Без входа в игру.",
        "rule_kicker": "Официальное правило · Kefir",
        "rule_h": "Каждые 7 дней",
        "rule_p": "Федеральная облава сбрасывает имущество сервера. Накопленный тюремный срок и небольшой набор прогресса персонажа сохраняются. У каждого сервера свой таймер.",
        "rule_link": "Читать справку Kefir",
        "chips": ["Правила проверены 18 ноября 2026", "Источники помечены: официальные и сообщества", "Сохраняется в вашем браузере", "Без регистрации"],
        "ws_h": "Ваше рабочее место для вайпа",
        "server_label": "Сервер",
        "server_default": "Мой сервер",
        "server_n": "Сервер",
        "new_server": "+ Новый сервер",
        "delete_server": "Удалить",
        "del_confirm": "Удалить этот профиль сервера и всё отслеживаемое в нём?",
        "stat_reset": "Ваши сброшенные предметы",
        "stat_reset_sub": "Отслеженные типы, а не количество",
        "stat_kept": "Ваш сохранённый прогресс",
        "stat_kept_sub": "Отслеженное, что сохраняется",
        "stat_manual": "Проверьте вручную",
        "stat_manual_sub": "Правила подтверждены не полностью",
        "stat_check": "Чек-лист выполнен",
        "stat_check_sub": "{done} / {total} задач",
        "lib_h": "Что сбрасывается? Что остаётся?",
        "lib_badge": "Проверено по источникам",
        "lib_lede": "Найдите предмет или вид прогресса и добавьте его в свой список вайпа.",
        "lib_notice": "Подтверждённые факты взяты из официальной справки Kefir. Остальное чётко помечено: объявления разработчиков, советы сообщества или «не проверено». Неизвестное не значит безопасное.",
        "search_label": "Поиск предметов",
        "search_ph": "Поиск: машины, деньги, татуировки, исследования…",
        "clear": "Очистить",
        "f_all": "Все",
        "f_resets": "Сбрасывается",
        "f_keeps": "Остаётся",
        "f_unconf": "Не проверено",
        "lib_list_h": "Библиотека предметов и прогресса",
        "results": "Найдено: {n}",
        "tracked_h": "Мои отслеживаемые предметы",
        "tracked_empty": "Пока ничего не отслеживается. Нажмите «+ Отслеживать» выше, чтобы составить личный список потерь и сохранений.",
        "custom_h": "Не нашли предмет? Добавьте свой для ручной проверки.",
        "custom_ph": "напр., Незабранная посылка",
        "custom_add": "+ Отслеживать предмет",
        "custom_need": "Сначала введите название предмета.",
        "lib_foot": "Числа выше — это типы, которые вы выбрали для отслеживания, а не ваш игровой баланс. Инструмент не читает игровой инвентарь.",
        "target_h": "Моя цель — Федеральная облава",
        "target_lede": "Необязательно: введите время вайпа, показанное в вашей игре, чтобы планировать вокруг него.",
        "target_label": "Дата и время вайпа в моей игре",
        "target_clear": "Очистить",
        "target_none": "Срок не введён",
        "target_none_sub": "Введите фактическое время облавы, если игра его показывает.",
        "target_note": "Это введённый вами вручную срок, а не живая проверка сервера. Если время облавы изменится, обновите его здесь. Точное время смотрите по внутриигровому таймеру.",
        "target_link": "Нужно прикинуть от открытия сервера? Используйте существующий отсчёт до Федеральной облавы на BuffForge",
        "target_passed": "Это время облавы уже прошло.",
        "summary_h": "Итог вашего плана",
        "summary_lede": "Полезно перед сменой сервера или выходом из игры.",
        "summary_empty": "Предметов пока не отслеживается. Выполнено {done} из {total} задач подготовки.",
        "copy": "Копировать итог",
        "copied": "Итог скопирован",
        "print": "Печать / PDF",
        "backup_h": "Резервная копия и восстановление",
        "export": "Экспорт JSON",
        "import": "Импорт JSON",
        "backup_note": "Хранится только в этом браузере (localStorage). Данные браузера можно очистить — сделайте резервную копию, если это важно.",
        "import_ok": "Резервная копия импортирована.",
        "import_bad": "Этот файл — не резервная копия планировщика вайпа.",
        "sources_h": "Правила и источники",
        "sources_lede": "Сначала основной источник. Неизвестное остаётся неизвестным.",
        "review_note": "Последняя редакторская проверка: 18 ноября 2026. Правила раннего доступа могут измениться без предупреждения. При конфликте источников доверяйте более свежей официальной информации и внутриигровому интерфейсу.",
        "check_h": "Ваш чек-лист перед вайпом",
        "check_lede": "Предлагаемые шаги подготовки и ваши задачи. На сервер ничего не отправляется.",
        "check_progress": "Прогресс подготовки",
        "check_done": "{done} / {total} выполнено",
        "check_add_ph": "Добавьте свою задачу перед вайпом",
        "check_add": "Добавить задачу",
        "check_foot": "Это личный чек-лист для планирования. Выполнение задач здесь ничего не меняет в ROB RUN.",
        "faq_h": "Вопросы о вайпе ROB RUN — с ответами",
        "sources": "Правила вайпа: справка Kefir «Что такое облава федералов — вайп?» (проверено 18 ноября 2026); дополнительные предметы: официальный пост в Telegram от 11 ноября 2026; FAQ сообщества: ROB RUN Info. BuffForge — независимый фанатский проект, не связан с Kefir.",
        "track": "+ Отслеживать",
        "tracked": "✓ Отслеживается",
        "remove": "Убрать",
        "resets": "Сбрасывается",
        "keeps": "Остаётся",
        "unconf": "Не проверено",
        "ev_official": "Официальный",
        "ev_developer": "Разработчик",
        "ev_community": "Сообщество",
        "ev_unconf": "Не проверено",
        "src_faq": "Справка Kefir",
        "src_tg": "Пост от 11 ноября",
        "src_info": "FAQ ROB RUN Info",
        "units": ["д", "ч", "мин", "с"],
        "tasks": [
            ("Проверьте внутриигровой таймер Федеральной облавы", "Ориентируйтесь на таймер вашего сервера, а не на общее время сброса."),
            ("Запишите номер сервера и регион", "Пригодится, если отряд планирует собраться на следующем цикле."),
            ("Проверьте деньги, оружие, участки и базы", "Kefir подтверждает: они сбрасываются."),
            ("Проверьте сомнительные предметы и незабранные награды", "Используйте внутриигровую информацию и свежие официальные объявления."),
            ("Запишите тюремный срок и прогресс авторитета", "Зафиксируйте значения до и после для следующего цикла."),
            ("Договоритесь с отрядом о следующем сервере", "Необязательно, если играете с друзьями."),
        ],
        "faq": [
            ("Что исчезает во время Федеральной облавы?",
             "Официально: участки, базы, оружие и деньги сбрасываются. Конфискованное имущество конвертируется в тюремный срок и авторитет. Инструмент не оценивает эту конвертацию."),
            ("Что точно сохраняется?",
             "Kefir называет косметику, имя игрока, прогресс обучения, настройки и накопленный тюремный срок. У остальных предметов в списке — отдельная пометка об источнике."),
            ("Все серверы вайпаются одновременно?",
             "Нет. У каждого сервера ROB RUN свой семидневный цикл, а не единый час сброса для всех. Проверяйте таймер своего сервера."),
            ("Читает ли BuffForge мой аккаунт или предметы?",
             "Нет. Вы сами выбираете, что отслеживать. Список и чек-лист остаются на этом устройстве, пока вы их не экспортируете. Живых игровых данных и подключения к аккаунту нет."),
        ],
    },
}


WIPE_JS = r'''
(function(){
  var S = window.WIPE_STRINGS || {};
  // One store per page language: EN and RU share an origin, so a single key
  // would leak the first-visited language's default tasks and server name
  // into the other language. Old data under the shared key is left alone;
  // each language seeds fresh defaults from its own strings.
  var KEY = "buffforge-wipe-planner-v1-" + ((document.documentElement.lang || "en").slice(0, 2));
  var data = null;
  function blankServer(name){
    return {name: name, tracked: [], custom: [], target: "",
      tasks: (S.tasks || []).map(function(t, i){
        return {id: "t" + i, text: t[0], sub: t[1], done: false, custom: false};
      })};
  }
  function load(){
    try { data = JSON.parse(localStorage.getItem(KEY)); } catch (e) { data = null; }
    if (!data || !Array.isArray(data.servers) || !data.servers.length) {
      data = {servers: [blankServer(S.server_default || "My server")], active: 0};
    }
    if (data.active == null || data.active >= data.servers.length) data.active = 0;
    data.servers.forEach(function(sv){
      if (!Array.isArray(sv.tracked)) sv.tracked = [];
      if (!Array.isArray(sv.custom)) sv.custom = [];
      if (!Array.isArray(sv.tasks) || !sv.tasks.length) sv.tasks = blankServer(sv.name).tasks;
      if (sv.target == null) sv.target = "";
    });
  }
  function save(){ try { localStorage.setItem(KEY, JSON.stringify(data)); } catch (e) {} }
  function cur(){ return data.servers[data.active]; }
  function esc(s){ return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
  function $(id){ return document.getElementById(id); }
  function allItems(){ return (S.items || []).concat(cur().custom); }
  function itemById(id){
    var all = allItems();
    for (var i = 0; i < all.length; i++) if (all[i].id === id) return all[i];
    return null;
  }
  function evLabel(ev){
    return ev === "official" ? S.ev_official : ev === "developer" ? S.ev_developer : ev === "community" ? S.ev_community : S.ev_unconf;
  }
  function evCls(ev){
    return ev === "official" ? "ev-keeps" : ev === "unconf" ? "ev-resets" : "ev-unconf";
  }
  function outCls(out){
    return out === "resets" ? "ev-resets" : out === "keeps" ? "ev-keeps" : "ev-unconf";
  }
  function outLabel(out){
    return out === "resets" ? S.resets : out === "keeps" ? S.keeps : S.unconf;
  }
  function libRow(it){
    var tracked = cur().tracked.indexOf(it.id) !== -1;
    var src = it.href ? '<a class="ev-src" href="' + esc(it.href) + '" target="_blank" rel="noopener">' + esc(it.src) + '</a>' : '<span class="ev-src">' + esc(it.src || "") + '</span>';
    return '<div class="lib-item"><div><b>' + esc(it.name) + '</b>' +
      (it.desc ? '<span class="desc">' + esc(it.desc) + '</span>' : '') +
      '<span class="tags"><span class="ev-pill ' + outCls(it.out) + '">' + esc(outLabel(it.out)) + '</span>' +
      '<span class="ev-pill ' + evCls(it.ev) + '">' + esc(evLabel(it.ev)) + '</span>' + src + '</span></div>' +
      '<button class="btn" type="button" data-track="' + esc(it.id) + '"' + (tracked ? ' aria-pressed="true"' : '') + '>' +
      esc(tracked ? S.tracked : S.track) + '</button></div>';
  }
  var q = "", filter = "all";
  function renderLib(){
    var list = $("wipe-lib");
    if (!list) return;
    var needle = q.trim().toLowerCase();
    var rows = allItems().filter(function(it){
      if (filter === "resets" && it.out !== "resets") return false;
      if (filter === "keeps" && it.out !== "keeps") return false;
      if (filter === "unconf" && it.ev !== "unconf") return false;
      if (!needle) return true;
      var hay = (it.name + " " + it.desc + " " + (it.kw || []).join(" ")).toLowerCase();
      return hay.indexOf(needle) !== -1;
    });
    list.innerHTML = rows.map(libRow).join("");
    var c = $("wipe-count");
    if (c) c.textContent = (S.results || "{n}").replace("{n}", rows.length);
  }
  function renderTracked(){
    var box = $("wipe-tracked");
    if (!box) return;
    if (!cur().tracked.length) {
      box.innerHTML = '<p class="hint">' + esc(S.tracked_empty) + '</p>';
      return;
    }
    box.innerHTML = cur().tracked.map(function(id){
      var it = itemById(id);
      if (!it) return "";
      return '<div class="lib-item"><div><b>' + esc(it.name) + '</b>' +
        '<span class="tags"><span class="ev-pill ' + outCls(it.out) + '">' + esc(outLabel(it.out)) + '</span>' +
        '<span class="ev-pill ' + evCls(it.ev) + '">' + esc(evLabel(it.ev)) + '</span></span></div>' +
        '<button class="btn btn-ghost" type="button" data-untrack="' + esc(it.id) + '">' + esc(S.remove) + '</button></div>';
    }).join("");
  }
  function renderStats(){
    var r = 0, k = 0, m = 0;
    cur().tracked.forEach(function(id){
      var it = itemById(id);
      if (!it) return;
      if (it.out === "resets") r++; else if (it.out === "keeps") k++;
      if (it.ev === "unconf") m++;
    });
    var done = cur().tasks.filter(function(t){ return t.done; }).length;
    var total = cur().tasks.length;
    var sr = $("stat-reset"); if (sr) sr.textContent = r;
    var sk = $("stat-kept"); if (sk) sk.textContent = k;
    var sm = $("stat-manual"); if (sm) sm.textContent = m;
    var sc = $("stat-check"); if (sc) sc.textContent = (total ? Math.round(done / total * 100) : 0) + "%";
    var scs = $("stat-check-sub"); if (scs) scs.textContent = (S.stat_check_sub || "{done} / {total}").replace("{done}", done).replace("{total}", total);
  }
  function renderTasks(){
    var box = $("wipe-tasks");
    if (!box) return;
    box.innerHTML = cur().tasks.map(function(t){
      return '<div class="check-row' + (t.done ? ' done' : '') + '">' +
        '<input type="checkbox" data-task="' + esc(t.id) + '"' + (t.done ? ' checked' : '') + ' aria-label="' + esc(t.text) + '">' +
        '<div class="t"><span>' + esc(t.text) + '</span>' +
        (t.sub ? '<span class="sub">' + esc(t.sub) + '</span>' : '') + '</div>' +
        (t.custom ? '<button class="btn btn-ghost" type="button" data-deltask="' + esc(t.id) + '" aria-label="' + esc(S.remove) + '">✕</button>' : '') +
        '</div>';
    }).join("");
    var done = cur().tasks.filter(function(t){ return t.done; }).length;
    var lbl = $("wipe-progress-label");
    if (lbl) lbl.textContent = (S.check_done || "{done} / {total}").replace("{done}", done).replace("{total}", cur().tasks.length);
    var bar = $("wipe-bar");
    if (bar) bar.style.width = (cur().tasks.length ? Math.round(done / cur().tasks.length * 100) : 0) + "%";
  }
  function renderSummary(){
    var box = $("wipe-summary");
    if (!box) return;
    var names = function(out){
      return cur().tracked.map(itemById).filter(function(it){ return it && it.out === out; }).map(function(it){ return it.name; });
    };
    var manual = cur().tracked.map(itemById).filter(function(it){ return it && it.ev === "unconf"; }).map(function(it){ return it.name; });
    var done = cur().tasks.filter(function(t){ return t.done; }).length;
    var lines = ["ROB RUN — " + cur().name];
    lines.push(S.stat_reset + ": " + (names("resets").join(", ") || "—"));
    lines.push(S.stat_kept + ": " + (names("keeps").join(", ") || "—"));
    lines.push(S.stat_manual + ": " + (manual.join(", ") || "—"));
    lines.push(S.check_progress + ": " + done + " / " + cur().tasks.length);
    lines.push(S.target_label + ": " + (cur().target ? cur().target.replace("T", " ") : "—"));
    box.textContent = lines.join("\n");
  }
  function renderServers(){
    var sel = $("wipe-server");
    if (!sel) return;
    sel.innerHTML = data.servers.map(function(sv, i){
      return '<option value="' + i + '"' + (i === data.active ? ' selected' : '') + '>' + esc(sv.name) + '</option>';
    }).join("");
    var del = $("wipe-del");
    if (del) del.disabled = data.servers.length <= 1;
  }
  function tick(){
    var big = $("wipe-countdown");
    var lbl = $("wipe-target-label");
    if (!big) return;
    var t = cur().target;
    if (!t) {
      big.textContent = S.target_none;
      if (lbl) lbl.textContent = S.target_none_sub;
      return;
    }
    var end = new Date(t).getTime();
    var diff = end - Date.now();
    if (isNaN(end)) { big.textContent = S.target_none; return; }
    if (diff <= 0) {
      big.textContent = S.target_passed;
      if (lbl) lbl.textContent = "";
      return;
    }
    var d = Math.floor(diff / 86400000);
    var h = Math.floor(diff / 3600000) % 24;
    var m = Math.floor(diff / 60000) % 60;
    var s = Math.floor(diff / 1000) % 60;
    var u = S.units || ["d", "h", "m", "s"];
    var pad = function(n){ return (n < 10 ? "0" : "") + n; };
    big.textContent = d + u[0] + " " + pad(h) + u[1] + " " + pad(m) + u[2] + " " + pad(s) + u[3];
    if (lbl) lbl.textContent = "";
  }
  function renderTarget(){
    var input = $("wipe-target");
    // Always sync: an invalid datetime-local value reads back as "" while
    // the typed text stays visible, so a conditional sync never clears it.
    if (input) input.value = cur().target || "";
    tick();
  }
  function renderAll(){
    renderServers(); renderLib(); renderTracked(); renderStats(); renderTasks(); renderSummary(); renderTarget();
  }
  function fallbackCopy(text){
    var ta = document.createElement("textarea");
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); } catch (e) {}
    ta.remove();
  }
  function bind(){
    var sel = $("wipe-server");
    if (sel) sel.addEventListener("change", function(){ data.active = parseInt(sel.value, 10) || 0; save(); renderAll(); });
    var nw = $("wipe-new");
    if (nw) nw.addEventListener("click", function(){
      var name = window.prompt(S.server_n + ":", (S.server_n + " " + (data.servers.length + 1)));
      if (name == null) return;
      name = name.trim() || (S.server_n + " " + (data.servers.length + 1));
      data.servers.push(blankServer(name));
      data.active = data.servers.length - 1;
      save(); renderAll();
    });
    var del = $("wipe-del");
    if (del) del.addEventListener("click", function(){
      if (data.servers.length <= 1) return;
      if (!window.confirm(S.del_confirm)) return;
      data.servers.splice(data.active, 1);
      if (data.active >= data.servers.length) data.active = data.servers.length - 1;
      save(); renderAll();
    });
    var input = $("wipe-q");
    if (input) input.addEventListener("input", function(){ q = input.value; renderLib(); });
    var clr = $("wipe-clear");
    if (clr) clr.addEventListener("click", function(){ q = ""; if (input) input.value = ""; renderLib(); });
    document.querySelectorAll("[data-filter]").forEach(function(btn){
      btn.addEventListener("click", function(){
        filter = btn.getAttribute("data-filter");
        document.querySelectorAll("[data-filter]").forEach(function(b){ b.setAttribute("aria-pressed", b === btn ? "true" : "false"); });
        renderLib();
      });
    });
    var lib = $("wipe-lib");
    if (lib) lib.addEventListener("click", function(e){
      var b = e.target.closest("[data-track]");
      if (!b) return;
      var id = b.getAttribute("data-track");
      var i = cur().tracked.indexOf(id);
      if (i === -1) cur().tracked.push(id); else cur().tracked.splice(i, 1);
      save(); renderLib(); renderTracked(); renderStats(); renderSummary();
    });
    var tr = $("wipe-tracked");
    if (tr) tr.addEventListener("click", function(e){
      var b = e.target.closest("[data-untrack]");
      if (!b) return;
      var i = cur().tracked.indexOf(b.getAttribute("data-untrack"));
      if (i !== -1) cur().tracked.splice(i, 1);
      save(); renderLib(); renderTracked(); renderStats(); renderSummary();
    });
    var cAdd = $("wipe-custom-add");
    if (cAdd) cAdd.addEventListener("click", function(){
      var inp = $("wipe-custom");
      var name = inp ? inp.value.trim() : "";
      if (!name) { window.alert(S.custom_need); return; }
      var id = "custom-" + Date.now();
      cur().custom.push({id: id, out: "unconf", ev: "unconf", name: name, desc: "", kw: [name.toLowerCase()], href: "", src: S.ev_unconf});
      cur().tracked.push(id);
      if (inp) inp.value = "";
      save(); renderLib(); renderTracked(); renderStats(); renderSummary();
    });
    var tgt = $("wipe-target");
    if (tgt) tgt.addEventListener("change", function(){ cur().target = tgt.value || ""; save(); renderTarget(); renderSummary(); });
    var tclr = $("wipe-target-clear");
    if (tclr) tclr.addEventListener("click", function(){ cur().target = ""; if (tgt) tgt.value = ""; save(); renderTarget(); renderSummary(); });
    var tasks = $("wipe-tasks");
    if (tasks) tasks.addEventListener("change", function(e){
      var cb = e.target.closest("[data-task]");
      if (!cb) return;
      var t = cur().tasks.filter(function(x){ return x.id === cb.getAttribute("data-task"); })[0];
      if (t) { t.done = cb.checked; save(); renderTasks(); renderStats(); renderSummary(); }
    });
    if (tasks) tasks.addEventListener("click", function(e){
      var b = e.target.closest("[data-deltask]");
      if (!b) return;
      cur().tasks = cur().tasks.filter(function(x){ return x.id !== b.getAttribute("data-deltask"); });
      save(); renderTasks(); renderStats(); renderSummary();
    });
    var tAdd = $("wipe-task-btn");
    if (tAdd) tAdd.addEventListener("click", function(){
      var inp = $("wipe-task-add");
      var text = inp ? inp.value.trim() : "";
      if (!text) return;
      cur().tasks.push({id: "c" + Date.now(), text: text, sub: "", done: false, custom: true});
      if (inp) inp.value = "";
      save(); renderTasks(); renderStats(); renderSummary();
    });
    var cp = $("wipe-copy");
    if (cp) cp.addEventListener("click", function(){
      var text = $("wipe-summary") ? $("wipe-summary").textContent : "";
      var done = function(){
        cp.textContent = S.copied;
        setTimeout(function(){ cp.textContent = S.copy; }, 2000);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function(){ fallbackCopy(text); done(); });
      } else { fallbackCopy(text); done(); }
    });
    var pr = $("wipe-print");
    if (pr) pr.addEventListener("click", function(){ window.print(); });
    var ex = $("wipe-export");
    if (ex) ex.addEventListener("click", function(){
      var blob = new Blob([JSON.stringify(data, null, 2)], {type: "application/json"});
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "rob-run-wipe-plan.json";
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function(){ URL.revokeObjectURL(a.href); }, 1000);
    });
    var im = $("wipe-import");
    var file = $("wipe-file");
    if (im && file) {
      im.addEventListener("click", function(){ file.click(); });
      file.addEventListener("change", function(){
        var f = file.files && file.files[0];
        if (!f) return;
        var r = new FileReader();
        r.onload = function(){
          try {
            var parsed = JSON.parse(r.result);
            if (!parsed || !Array.isArray(parsed.servers) || !parsed.servers.length) throw new Error("bad");
            data = parsed;
            if (data.active == null || data.active >= data.servers.length) data.active = 0;
            save(); renderAll();
            window.alert(S.import_ok);
          } catch (e) { window.alert(S.import_bad); }
        };
        r.readAsText(f);
        file.value = "";
      });
    }
  }
  load();
  bind();
  renderAll();
  setInterval(tick, 1000);
})();
'''


def wipe_page(lang):
    w = WIPE[lang]
    faq_url = WIPE_FAQ_EN if lang == "en" else WIPE_FAQ_RU
    count_url = "/rob-run/federal-raid-countdown/" if lang == "en" else "/ru/rob-run/federal-raid-countdown/"
    hub = "/rob-run/" if lang == "en" else "/ru/rob-run/"
    # Library rows, server-rendered so the facts are visible without JS.
    rows = []
    for it in WIPE_ITEMS:
        if it["ev"] == "official":
            href, lbl, ev_cls, ev_lbl = faq_url, w["src_faq"], "ev-keeps", w["ev_official"]
        elif it["ev"] == "developer":
            href, lbl, ev_cls, ev_lbl = WIPE_TG67, w["src_tg"], "ev-unconf", w["ev_developer"]
        else:
            href, lbl, ev_cls, ev_lbl = WIPE_INFO_FAQ, w["src_info"], "ev-unconf", w["ev_community"]
        out_cls = "ev-resets" if it["out"] == "resets" else "ev-keeps"
        out_lbl = w["resets"] if it["out"] == "resets" else w["keeps"]
        rows.append(
            '<div class="lib-item"><div><b>%s</b><span class="desc">%s</span>'
            '<span class="tags"><span class="ev-pill %s">%s</span>'
            '<span class="ev-pill %s">%s</span>'
            '<a class="ev-src" href="%s" target="_blank" rel="noopener">%s</a></span></div>'
            '<button class="btn" type="button" data-track="%s">%s</button></div>'
            % (it["name"][lang], it["desc"][lang], out_cls, out_lbl,
               ev_cls, ev_lbl, href, lbl, it["id"], w["track"]))
    tasks_html = "".join(
        '<div class="check-row"><input type="checkbox" data-task="t%d">'
        '<div class="t"><span>%s</span><span class="sub">%s</span></div></div>'
        % (i, t, sub) for i, (t, sub) in enumerate(w["tasks"]))
    if lang == "en":
        src_list = [
            ("Kefir FAQ — What is the Federal Raid (Wipe)?", faq_url, "ev-keeps", w["ev_official"]),
            ("ROB RUN Nov 11 announcement", WIPE_TG67, "ev-unconf", w["ev_developer"]),
            ("ROB RUN Info — Detailed FAQ", WIPE_INFO_FAQ, "ev-unconf", w["ev_community"]),
        ]
    else:
        src_list = [
            ("Справка Kefir — Что такое облава федералов (вайп)?", faq_url, "ev-keeps", w["ev_official"]),
            ("Объявление ROB RUN от 11 ноября", WIPE_TG67, "ev-unconf", w["ev_developer"]),
            ("ROB RUN Info — подробный FAQ", WIPE_INFO_FAQ, "ev-unconf", w["ev_community"]),
        ]
    src_html = "".join(
        '<div class="src-row"><a href="%s" target="_blank" rel="noopener"><b>%s</b></a>'
        '<span class="ev-pill %s">%s</span></div>' % (href, title, cls, ev)
        for title, href, cls, ev in src_list)
    faq_html = "".join(
        '<details><summary><h3>%s</h3><span class="plus">+</span></summary><p>%s</p></details>'
        % (q, a) for q, a in w["faq"])
    # Strings the client script needs; server-rendered copy stays the source
    # of truth for SEO copy (title, desc, h1, hero, sources, FAQ).
    js_keys = ["server_default", "server_n", "delete_server", "del_confirm",
               "stat_reset", "stat_kept", "stat_manual", "stat_check",
               "stat_reset_sub", "stat_kept_sub", "stat_manual_sub", "stat_check_sub",
               "lib_notice", "search_ph", "clear", "f_all", "f_resets", "f_keeps", "f_unconf",
               "lib_list_h", "results", "tracked_h", "tracked_empty", "custom_h", "custom_ph",
               "custom_add", "custom_need", "target_none", "target_none_sub", "target_passed",
               "target_label", "summary_empty", "copy", "copied", "print", "export", "import",
               "import_ok", "import_bad", "check_progress", "check_done", "check_add_ph", "check_add",
               "track", "tracked", "remove", "resets", "keeps", "unconf",
               "ev_official", "ev_developer", "ev_community", "ev_unconf",
               "src_faq", "src_tg", "src_info", "units", "tasks"]
    strings = {k: w[k] for k in js_keys}
    strings["items"] = []
    for it in WIPE_ITEMS:
        if it["ev"] == "official":
            href, lbl = faq_url, w["src_faq"]
        elif it["ev"] == "developer":
            href, lbl = WIPE_TG67, w["src_tg"]
        else:
            href, lbl = WIPE_INFO_FAQ, w["src_info"]
        strings["items"].append({"id": it["id"], "out": it["out"], "ev": it["ev"],
                                 "name": it["name"][lang], "desc": it["desc"][lang],
                                 "kw": it["kw"], "href": href, "src": lbl})
    js = ('<script>window.WIPE_STRINGS = %s;</script><script>%s</script>'
          % (json.dumps(strings, ensure_ascii=False), WIPE_JS))
    chips = "".join('<span class="chip">✓ %s</span>' % c for c in w["chips"])
    body = (
        '<main class="wrap">'
        + crumbs_html(lang, [("ROB RUN", hub), (w["h1"], None)])
        + '<div class="wipe-hero"><div>'
        + '<p class="wipe-eyebrow">%s</p><h1>%s</h1>' % (w["eyebrow"], w["h1"])
        + '<p class="wipe-hero-line">%s<span class="accent">%s</span>%s</p>' % (w["hero_a"], w["hero_b"], w["hero_c"])
        + '<p class="lede">%s</p>' % w["lede"]
        + '<div class="chips">%s</div></div>' % chips
        + '<aside class="wipe-rule"><p class="kicker">%s</p><h2>%s</h2><p>%s</p>'
          '<p><a href="%s" target="_blank" rel="noopener">%s</a></p></aside></div>'
          % (w["rule_kicker"], w["rule_h"], w["rule_p"], faq_url, w["rule_link"])
        + '<section class="wipe-panel"><h2>%s</h2>' % w["ws_h"]
        + '<div class="mode-row" style="align-items:center;margin-bottom:14px">'
        + '<label for="wipe-server"><strong>%s</strong></label>' % w["server_label"]
        + '<select id="wipe-server"><option value="0">%s</option></select>' % w["server_default"]
        + '<button class="btn" type="button" id="wipe-new">%s</button>' % w["new_server"]
        + '<button class="btn btn-ghost" type="button" id="wipe-del" disabled>%s</button></div>' % w["delete_server"]
        + '<div class="stats four">'
        + '<div class="stat"><em>%s</em><strong id="stat-reset">0</strong><span>%s</span></div>' % (w["stat_reset"], w["stat_reset_sub"])
        + '<div class="stat"><em>%s</em><strong id="stat-kept">0</strong><span>%s</span></div>' % (w["stat_kept"], w["stat_kept_sub"])
        + '<div class="stat"><em>%s</em><strong id="stat-manual">0</strong><span>%s</span></div>' % (w["stat_manual"], w["stat_manual_sub"])
        + '<div class="stat"><em>%s</em><strong id="stat-check">0%%</strong><span id="stat-check-sub">%s</span></div></div></section>'
          % (w["stat_check"], w["stat_check_sub"].replace("{done}", "0").replace("{total}", "6"))
        + '<div class="profit-grid"><div class="wipe-panel"><h2>%s <span class="ev-pill ev-keeps">%s</span></h2>' % (w["lib_h"], w["lib_badge"])
        + '<p class="sub">%s</p>' % w["lib_lede"]
        + '<div class="note-box" style="margin:12px 0"><p>%s</p></div>' % w["lib_notice"]
        + '<label class="lbl" for="wipe-q">%s</label>' % w["search_label"]
        + '<div class="mode-row"><input type="search" id="wipe-q" placeholder="%s">'
          '<button class="btn btn-ghost" type="button" id="wipe-clear">%s</button></div>' % (w["search_ph"], w["clear"])
        + '<div class="mode-row" role="group" aria-label="Filter">'
        + '<button class="btn" type="button" data-filter="all" aria-pressed="true">%s</button>' % w["f_all"]
        + '<button class="btn" type="button" data-filter="resets" aria-pressed="false">%s</button>' % w["f_resets"]
        + '<button class="btn" type="button" data-filter="keeps" aria-pressed="false">%s</button>' % w["f_keeps"]
        + '<button class="btn" type="button" data-filter="unconf" aria-pressed="false">%s</button></div>' % w["f_unconf"]
        + '<h3>%s <span class="hint" id="wipe-count">%s</span></h3>' % (w["lib_list_h"], w["results"].replace("{n}", str(len(WIPE_ITEMS))))
        + '<div class="wipe-stack" id="wipe-lib">%s</div>' % "".join(rows)
        + '<h3>%s</h3>' % w["tracked_h"]
        + '<div class="wipe-stack" id="wipe-tracked"><p class="hint">%s</p></div>' % w["tracked_empty"]
        + '<h3>%s</h3>' % w["custom_h"]
        + '<div class="mode-row"><input type="text" id="wipe-custom" placeholder="%s">'
          '<button class="btn" type="button" id="wipe-custom-add">%s</button></div>' % (w["custom_ph"], w["custom_add"])
        + '<p class="hint">%s</p></div>' % w["lib_foot"]
        + '<div><div class="wipe-panel"><h2>%s</h2>' % w["target_h"]
        + '<p class="sub">%s</p>' % w["target_lede"]
        + '<label class="lbl" for="wipe-target">%s</label>' % w["target_label"]
        + '<div class="mode-row"><input type="datetime-local" id="wipe-target">'
          '<button class="btn btn-ghost" type="button" id="wipe-target-clear">%s</button></div>' % w["target_clear"]
        + '<div class="target-box" style="margin-top:14px"><p class="lbl">%s</p>'
          '<p class="big" id="wipe-countdown">%s</p>'
          '<p class="hint" id="wipe-target-label">%s</p></div>' % (w["target_label"], w["target_none"], w["target_none_sub"])
        + '<p class="hint">%s</p>' % w["target_note"]
        + '<p class="hint"><a href="%s">%s</a></p></div>' % (count_url, w["target_link"])
        + '<div class="wipe-panel"><h2>%s</h2>' % w["summary_h"]
        + '<p class="sub">%s</p>' % w["summary_lede"]
        + '<div class="wipe-summary" id="wipe-summary">ROB RUN — %s</div>' % w["server_default"]
        + '<div class="actions">'
        + '<button class="btn" type="button" id="wipe-copy">%s</button>' % w["copy"]
        + '<button class="btn btn-ghost" type="button" id="wipe-print">%s</button></div>' % w["print"]
        + '<h3>%s</h3>' % w["backup_h"]
        + '<div class="actions">'
        + '<button class="btn" type="button" id="wipe-export">%s</button>' % w["export"]
        + '<button class="btn btn-ghost" type="button" id="wipe-import">%s</button>' % w["import"]
        + '<input type="file" id="wipe-file" accept="application/json" hidden></div>'
        + '<p class="hint">%s</p></div></div></div>' % w["backup_note"]
        + '<section class="wipe-panel"><h2>%s</h2>' % w["check_h"]
        + '<p class="sub">%s</p>' % w["check_lede"]
        + '<div class="progress" role="progressbar" aria-label="%s"><span id="wipe-bar" style="width:0%%"></span></div>' % w["check_progress"]
        + '<div class="mode-row" style="justify-content:space-between"><span class="hint">%s</span>'
          '<span class="hint" id="wipe-progress-label">%s</span></div>' % (w["check_progress"], w["check_done"].replace("{done}", "0").replace("{total}", "6"))
        + '<div class="wipe-stack" id="wipe-tasks" style="margin-top:12px">%s</div>' % tasks_html
        + '<div class="mode-row"><input type="text" id="wipe-task-add" placeholder="%s">'
          '<button class="btn" type="button" id="wipe-task-btn">%s</button></div>' % (w["check_add_ph"], w["check_add"])
        + '<p class="hint">%s</p></section>' % w["check_foot"]
        + '<section class="wipe-panel"><h2>%s</h2>' % w["sources_h"]
        + '<p class="sub">%s</p>' % w["sources_lede"]
        + '<div class="wipe-stack">%s</div>' % src_html
        + '<p class="hint">%s</p></section>' % w["review_note"]
        + '<section class="faq" id="faq"><h2 class="sec">%s</h2>%s</section>' % (w["faq_h"], faq_html)
        + '<p class="data-line">%s</p></main>' % w["sources"]
    )
    faq_jl = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in w["faq"]]}
    return tool_page(lang, "wipe-planner", w["title"], w["desc"], body + js, w["h1"], extra_jsonld=[faq_jl])


def main():
    for lang in ("en", "ru"):
        prefix = "" if lang == "en" else "ru/"
        write(prefix + "rob-run/federal-raid-countdown/index.html", countdown_page(lang))
        write(prefix + "rob-run/wipe-planner/index.html", wipe_page(lang))
        write(prefix + "rob-run/loot-profit-calculator/index.html", profit_page(lang))
        write(prefix + "rob-run/squad-loot-splitter/index.html", split_page(lang))
        write(status_rel(lang), status_render(lang))
    write("rob-run/lag-and-high-ping/index.html", lag_page("en"))
    write("ru/rob-run/kak-ubrat-lagi/index.html", lag_page("ru"))
    write("ru/rob-run/failed-to-enter-location/index.html", failed_location_page())
    print("rob run build done")


if __name__ == "__main__":
    main()

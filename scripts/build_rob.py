#!/usr/bin/env python3
"""ROB RUN tools (EN + RU) and the RU-only lag guide. Generated static pages.

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


def tool_page(lang, slug, title, desc, body, h1):
    canon = "/rob-run/%s/" % slug if lang == "en" else "/ru/rob-run/%s/" % slug
    alt = {"en": "/rob-run/%s/" % slug, "ru": "/ru/rob-run/%s/" % slug}
    home = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    hub = "/rob-run/" if lang == "en" else "/ru/rob-run/"
    jl = [
        breadcrumb_jsonld(lang, [(home, home_path), ("ROB RUN", hub), (h1, canon)]),
        webapp_jsonld(lang, h1, canon, desc),
    ]
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
        '<p class="data-line">%s</p></main>'
        % (crumbs_html(lang, [("ROB RUN", hub), (c["h1"], None)]),
           c["h1"], c["lede"], c["mode"], opts, c["opened"], c["zone"], zones,
           c["open_date"], c["local"], c["msk"], c["utc"],
           c["keep_h"], keep, c["lose_h"], lose, c["sources"])
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
PROFIT = {
    "en": {
        "title": "ROB RUN loot profit calculator — BuffForge",
        "desc": "Add ROB RUN loot, subtract gear and other costs, and see net cash and the return. Every amount is one you type.",
        "h1": "Loot profit calculator",
        "lede": "List the haul, then subtract gear and other costs. The net and the return use only the numbers you type — this page has no price list.",
        "name": "Item",
        "price": "Unit price (cash)",
        "qty": "Qty",
        "add": "Add item",
        "clear": "Clear list",
        "ph_name": "Name",
        "empty": "No items yet.",
        "need_name": "Add a name first.",
        "remove": "Remove",
        "haul": "Haul",
        "costs": "Costs",
        "net": "Net",
        "ratio": "Return",
        "ratio_sub": "Haul ÷ costs",
        "cash": "cash",
        "gear": "Gear (cash)",
        "other": "Other costs (cash)",
        "note": "Kefir’s help pages call the in-game money cash. No currency symbol is shown here because none is published on those pages.",
        "sources": "You enter every amount. Wording for cash: Kefir FAQ “How do I make money?” and “Can my money be stolen?”. Reviewed 13 Nov 2026.",
    },
    "ru": {
        "title": "Калькулятор добычи ROB RUN — BuffForge",
        "desc": "Сложите добычу в ROB RUN, вычтите снаряжение и прочие расходы и увидьте итог. Все суммы вводите вы.",
        "h1": "Калькулятор добычи",
        "lede": "Соберите список добычи и вычтите снаряжение с прочими расходами. Итог и отдача считаются только из ваших цифр — прайса на странице нет.",
        "name": "Предмет",
        "price": "Цена за штуку (деньги)",
        "qty": "Шт.",
        "add": "Добавить",
        "clear": "Очистить",
        "ph_name": "Название",
        "empty": "Пока пусто.",
        "need_name": "Сначала укажите название.",
        "remove": "Убрать",
        "haul": "Добыча",
        "costs": "Расходы",
        "net": "Итог",
        "ratio": "Отдача",
        "ratio_sub": "Добыча ÷ расходы",
        "cash": "деньги",
        "gear": "Снаряжение (деньги)",
        "other": "Прочие расходы (деньги)",
        "note": "В справке Kefir игровая валюта названа просто деньгами. Символа на странице нет: в этих справках его не публикуют.",
        "sources": "Каждую сумму вводите вы. Слово «деньги»: справка Kefir «Как заработать?» и «Могут ли украсть мои деньги?». Проверено 13 ноября 2026.",
    },
}

PROFIT_JS = r"""
<script>
(function () {
  var STR = __STR__;
  var items = [];
  var nameEl = document.getElementById('itemName');
  var priceEl = document.getElementById('itemPrice');
  var qtyEl = document.getElementById('itemQty');
  var list = document.getElementById('itemList');
  var note = document.getElementById('addNote');
  var gearEl = document.getElementById('gear');
  var otherEl = document.getElementById('other');
  function num(v) {
    var n = parseFloat(v);
    return isFinite(n) ? n : 0;
  }
  function fmt(n) {
    return n.toLocaleString(STR.locale, {maximumFractionDigits: 2});
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (ch) {
      return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[ch];
    });
  }
  function render() {
    var haul = 0;
    var html = '';
    for (var i = 0; i < items.length; i++) {
      var line = items[i].price * items[i].qty;
      haul += line;
      html += '<div class="line-item"><span>' + esc(items[i].name) + ' × ' + fmt(items[i].qty) +
        '</span><b>' + fmt(line) + ' <button type="button" class="btn btn-ghost" data-i="' + i + '">' +
        STR.remove + '</button></b></div>';
    }
    list.innerHTML = html || '<p class="hint">' + STR.empty + '</p>';
    var costs = num(gearEl.value) + num(otherEl.value);
    var net = haul - costs;
    document.getElementById('haulOut').textContent = fmt(haul);
    document.getElementById('costOut').textContent = fmt(costs);
    document.getElementById('netOut').textContent = fmt(net);
    document.getElementById('netOut').style.color = net < 0 ? 'var(--danger)' : 'var(--ink)';
    document.getElementById('ratioOut').textContent = costs === 0 ? '—' :
      ((haul / costs).toLocaleString(STR.locale, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + '×');
    list.querySelectorAll('button[data-i]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        items.splice(+btn.getAttribute('data-i'), 1);
        render();
      });
    });
  }
  document.getElementById('addItem').addEventListener('click', function () {
    var name = nameEl.value.trim();
    if (!name) { note.textContent = STR.needName; nameEl.focus(); return; }
    note.textContent = '';
    items.push({name: name, price: num(priceEl.value), qty: num(qtyEl.value)});
    nameEl.value = '';
    render();
    nameEl.focus();
  });
  document.getElementById('clearItems').addEventListener('click', function () {
    items = [];
    note.textContent = '';
    render();
  });
  gearEl.addEventListener('input', render);
  otherEl.addEventListener('input', render);
  render();
})();
</script>
"""


def profit_page(lang):
    c = PROFIT[lang]
    hub = "/rob-run/" if lang == "en" else "/ru/rob-run/"
    body = (
        '<main id="main" class="wrap narrow">%s'
        '<h1 class="page-h1">%s</h1><p class="page-lede">%s</p>'
        '<div class="checker"><div class="field-row">'
        '<div class="grow"><label for="itemName">%s</label>'
        '<input id="itemName" type="text" autocomplete="off" placeholder="%s"></div>'
        '<div><label for="itemPrice">%s</label>'
        '<input id="itemPrice" type="number" inputmode="decimal" value="0"></div>'
        '<div><label for="itemQty">%s</label>'
        '<input id="itemQty" type="number" inputmode="decimal" value="1"></div>'
        '</div><div class="actions">'
        '<button type="button" class="btn btn-primary" id="addItem">%s</button>'
        '<button type="button" class="btn btn-secondary" id="clearItems">%s</button>'
        '</div><p class="hint" id="addNote"></p>'
        '<div class="line-list" id="itemList"></div>'
        '<div class="field-row" style="margin-top:18px">'
        '<div><label for="gear">%s</label><input id="gear" type="number" inputmode="decimal" value="0"></div>'
        '<div><label for="other">%s</label><input id="other" type="number" inputmode="decimal" value="0"></div>'
        '</div>'
        '<div class="stats" style="margin-top:16px">'
        '<div class="stat"><em>%s</em><strong id="haulOut">0</strong><span>%s</span></div>'
        '<div class="stat"><em>%s</em><strong id="costOut">0</strong><span>%s</span></div>'
        '<div class="stat"><em>%s</em><strong id="netOut">0</strong><span>%s</span></div>'
        '<div class="stat"><em>%s</em><strong id="ratioOut">—</strong><span>%s</span></div>'
        '</div><p class="hint">%s</p></div>'
        '<p class="data-line">%s</p></main>'
        % (crumbs_html(lang, [("ROB RUN", hub), (c["h1"], None)]),
           c["h1"], c["lede"], c["name"], c["ph_name"], c["price"], c["qty"],
           c["add"], c["clear"], c["gear"], c["other"],
           c["haul"], c["cash"], c["costs"], c["cash"], c["net"], c["cash"],
           c["ratio"], c["ratio_sub"], c["note"], c["sources"])
    )
    strings = {
        "locale": "en-US" if lang == "en" else "ru-RU",
        "empty": c["empty"],
        "needName": c["need_name"],
        "remove": c["remove"],
    }
    js = PROFIT_JS.replace("__STR__", json.dumps(strings, ensure_ascii=False))
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

LAG_FAQ = [
    ("Почему ROB RUN лагает из России?",
     "Официально доступны только EU и East US, города серверов не названы. Из России обычно ближе EU. Если сервер недоступен из-за DDoS, домашние настройки это не исправят."),
    ("Это пинг или просадка FPS?",
     "Высокий пинг, «резинка» и массовые отключения — сеть или сервер. Если кадры падают, когда двигаете мышь, справка Kefir советует снизить частоту опроса в программе мыши. Код E-0201 значит, что связь с игровым сервером пропала: проверьте соединение и перезапустите игру."),
    ("Как перейти на сервер EU?",
     "В FAQ Kefir от 13 ноября 2026 года: «Чтобы сменить сервер, приходится сдаваться и возвращаться в тюрьму». В справке: глобальная карта, локация «Тюрьма», кнопка «Сдаться федералам», затем смена сервера из тюрьмы."),
    ("Ускоритель уберёт лаги, если сервер под DDoS?",
     "Нет. Он только меняет маршрут до официальных серверов. Сравните пинг на одном сервере EU в одно время, с ускорителем и без, на пробном периоде. Отказ самого сервера так не лечится."),
]


def _src(href, label):
    return '<a href="%s">%s</a>' % (href, label)


def _ext(href, label):
    return '<a href="%s" rel="nofollow noopener" target="_blank">%s</a>' % (href, label)


def _booster(tag, name, trial, lines, href, host):
    bits = "".join("<p><b>%s</b> %s</p>" % pair for pair in lines)
    return (
        '<article class="card"><p class="tag">%s</p><h3>%s</h3>'
        '<p>Пропускает трафик ROB RUN через свои узлы к официальным серверам игры.</p>'
        '<p class="meta">%s</p>%s'
        '<p class="go">%s</p></article>'
        % (tag, name, trial, bits, _ext(href, host))
    )


def lag_page():
    """RU-only guide. No English page and no hreflang alternate."""
    canon = "/ru/rob-run/kak-ubrat-lagi/"
    title = "ROB RUN лагает и высокий пинг: как уменьшить задержку — BuffForge"
    desc = ("Почему ROB RUN лагает из России: только EU и East US. Как отличить высокий пинг от FPS "
            "и что сделать бесплатно. LagoFast, ExitLag и GearUP — без цен.")
    h1 = "ROB RUN лагает и высокий пинг: как уменьшить задержку"
    crumb = "Лаги и высокий пинг"
    faq_html = "".join(
        '<details%s><summary><h3>%s</h3>'
        '<span class="plus" aria-hidden="true">'
        '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6">'
        '<path d="M6 1v10M1 6h10"/></svg></span></summary><p>%s</p></details>'
        % (" open" if i == 0 else "", q, a)
        for i, (q, a) in enumerate(LAG_FAQ))
    cards = (
        _booster(
            "3 часа", "LagoFast",
            "Пробный период: 3 часа с создания аккаунта, один раз на устройство.",
            [("Плюс.", "Сайт на русском и отдельная страница ROB RUN."),
             ("Плюс.", "Можно войти через VK."),
             ("Минус.", "Пробный период только 3 часа.")],
            LAGO_URL, "www.lagofastbooster.ru/games/rob-run/")
        + _booster(
            "3 дня", "ExitLag",
            "Пробный период: 3 дня, по странице пробного периода на русском.",
            [("Плюс.", "Самый длинный пробный период из трёх."),
             ("Плюс.", "Есть тарифы для группы."),
             ("Минус.", "Отдельной страницы ROB RUN на сайте не нашли — список игр смотрите в клиенте.")],
            EXIT_URL, "www.exitlag.com/ru")
        + _booster(
            "пробный период", "GearUP Booster",
            "Бесплатный пробный период и гарантия возврата — по данным сайта.",
            [("Плюс.", "На сайте есть статьи про ROB RUN."),
             ("Плюс.", "Гарантия возврата — по данным сайта."),
             ("Минус.", "Перед оплатой проверьте, какие способы оплаты принимает сайт.")],
            GEAR_URL, "www.gearupbooster.com/ru/")
    )
    body = (
        '<main id="main" class="wrap narrow">%s'
        '<h1 class="page-h1">%s</h1>'
        '<p class="page-lede">Из России задержка чаще упирается в маршрут до сервера. '
        'Официально регионов два, города площадок не опубликованы.</p>'
        '<p class="intro-note">Обновлено: 14 ноября 2026</p>'
        '<div class="prose">'
        '<h2 class="sec">Почему лагает</h2>'
        '<p>4 ноября 2026 года Kefir написал: «Сейчас в ROB RUN доступны два региона: EU и East US». '
        'Другие регионы обещали добавлять по мере возможности. Города серверов в %s не названы — '
        'и на этой странице тоже.</p>'
        '<p>13 ноября 2026 года в %s разработчики назвали нестабильность серверов и DDoS-атаки '
        'среди острых проблем, которые они разбирают.</p>'
        '<div class="note-box amber"><p>Если сервер недоступен из-за DDoS, со стороны игрока это не исправить. '
        'Ускоритель такой отказ тоже не лечит: он только меняет маршрут до официальных серверов.</p></div>'
        '<h2 class="sec">Пинг или FPS?</h2>'
        '<table class="fact-table">'
        '<tr><th>Высокий пинг, «резинка», рассинхрон</th><td>Сеть: маршрут или сервер.</td></tr>'
        '<tr><th>Многих отключает одновременно</th><td>Сервер. Со своей стороны это не исправить.</td></tr>'
        '<tr><th>FPS падает, когда двигаете мышь</th><td>Не пинг. В справке Kefir это частота опроса мыши.</td></tr>'
        '</table>'
        '<p>Если кадры падают при движении мыши, %s советует снизить «Частоту опроса» в программе '
        'производителя мыши (Logitech, Razer, Bloody и другие).</p>'
        '<p>Проверка файлов в Steam, по %s: Свойства → Установленные файлы → Проверить целостность файлов игры.</p>'
        '<p>Код E-0201 в %s: игра уже шла, связь с игровым сервером пропала и не восстановилась. '
        'Kefir советует проверить соединение и перезапустить игру.</p>'
        '<p>Весь раздел — %s.</p>'
        '<h2 class="sec">Выберите EU</h2>'
        '<p>Для игроков из России EU обычно ближе, чем East US. Сравнивать пинг имеет смысл уже на EU.</p>'
        '<p>Сменить сервер в рейде нельзя. В FAQ от 13 ноября 2026 года: «Чтобы сменить сервер, приходится '
        'сдаваться и возвращаться в тюрьму». %s описывает тот же шаг: откройте глобальную карту, выберите '
        'локацию «Тюрьма» и нажмите «Сдаться федералам». Сервер меняют уже из тюрьмы.</p>'
        '<p>Серверы в других регионах, например в Азии или Океании, как минимум до конца этого года не появятся — '
        'так Kefir ответил в том же FAQ.</p>'
        '<h2 class="sec">Бесплатно: что сделать самому</h2>'
        '<ol>'
        '<li>Подключите компьютер кабелем, не по Wi\u2011Fi.</li>'
        '<li>Поставьте на паузу фоновые загрузки и стримы: загрузки Steam, торренты, обновления системы.</li>'
        '<li>Если роутер умеет QoS или приоритет для игр, включите его для этого компьютера.</li>'
        '<li>Перезагрузите роутер.</li>'
        '<li>Проверьте целостность файлов игры в Steam.</li>'
        '<li>Обновите драйвер сетевой карты и видеокарты.</li>'
        '<li>Сверьте компьютер с требованиями ниже.</li>'
        '</ol>'
        '<p>Для обеих сборок %s указывает 64-разрядную Windows 10 или новее, DirectX 11, интернет и 20 ГБ на диске.</p>'
        '<table class="fact-table">'
        '<tr><th>Процессор</th><td>Минимум: Intel i5-6600K или Ryzen 5 1600. Рекомендуется: Intel i5-9600K или Ryzen 5 3600.</td></tr>'
        '<tr><th>Память</th><td>Минимум 12 ГБ. Рекомендуется 16 ГБ.</td></tr>'
        '<tr><th>Видеокарта</th><td>Минимум: GTX 1050 Ti, RX 580 или Arc A380. Рекомендуется: RTX 2070, RX 5700 XT или Arc B570.</td></tr>'
        '</table>'
        '<h2 class="sec">Платные игровые ускорители</h2>'
        '<p>Платный ускоритель пропускает трафик ROB RUN через свои узлы к официальным серверам игры. '
        'Если не отвечает сам сервер, ускоритель это не исправит.</p>'
        '%s'
        '<table class="fact-table">'
        '<tr><th>Пробный период</th><td>LagoFast — 3 часа, один раз на устройство. ExitLag — 3 дня. GearUP — есть, по данным сайта.</td></tr>'
        '<tr><th>Страница ROB RUN</th><td>LagoFast — есть. ExitLag — отдельной страницы не найдено. GearUP — есть статьи.</td></tr>'
        '<tr><th>Сайт на русском</th><td>LagoFast — да. ExitLag — да. GearUP — да.</td></tr>'
        '</table>'
        '<p>Актуальные цены и способы оплаты — на официальных сайтах.</p>'
        '<p>Проверьте пробный период на одном и том же сервере EU в одно и то же время: пинг с ускорителем и без. '
        'Если не отвечает сам сервер, ускоритель разницы не даст.</p>'
        '<section class="faq" id="faq"><h2 class="sec">Частые вопросы</h2>%s</section>'
        '</div>'
        '<section class="related"><h2>Инструменты ROB RUN</h2><div class="related-grid">'
        '<a class="rel" href="/ru/rob-run/federal-raid-countdown/"><b>Отсчёт до Федеральной облавы</b>'
        '<span>Семь дней от открытия сервера — у вас, по Москве и в UTC.</span></a>'
        '<a class="rel" href="/ru/rob-run/loot-profit-calculator/"><b>Калькулятор добычи</b>'
        '<span>Сложить добычу и вычесть расходы. Суммы вводите вы.</span></a>'
        '<a class="rel" href="/ru/rob-run/squad-loot-splitter/"><b>Делёж добычи в отряде</b>'
        '<span>Поровну или со своим весом на каждого.</span></a>'
        '</div></section>'
        '<p class="data-line">BuffForge — независимый фанатский проект. Сайт не связан с Kefir и не одобрен компанией. '
        'Официальная справка: %s.</p></main>'
        % (crumbs_html("ru", [("ROB RUN", "/ru/rob-run/"), (crumb, None)]),
           h1,
           _src(ANN_REGIONS, "объявлении от 4 ноября 2026"),
           _src(ANN_FAQ, "FAQ"),
           _src(HC_FPS, "справка Kefir"),
           _src(HC_FILES, "справке Kefir"),
           _src(HC_ERR, "списке ошибок"),
           _src(HC_SECTION, "устранение неполадок и поддержка"),
           _src(HC_SERVER, "Справка Kefir"),
           _src(HC_REQ, "справка Kefir"),
           cards, faq_html,
           _src(HC_SECTION, "устранение неполадок ROB RUN"))
    )
    jl = [
        breadcrumb_jsonld("ru", [
            ("Главная", "/ru/"),
            ("ROB RUN", "/ru/rob-run/"),
            (crumb, canon),
        ]),
        {"@context": "https://schema.org", "@type": "Article",
         "headline": h1, "description": desc, "inLanguage": "ru",
         "datePublished": "2026-11-14", "dateModified": "2026-11-14",
         "author": {"@type": "Organization", "name": "BuffForge", "url": BASE},
         "publisher": {"@type": "Organization", "name": "BuffForge", "url": BASE},
         "mainEntityOfPage": {"@type": "WebPage", "@id": BASE + canon}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [
             {"@type": "Question", "name": q,
              "acceptedAnswer": {"@type": "Answer", "text": a}}
             for q, a in LAG_FAQ]},
    ]
    return page("ru", title, desc, canon, None, body, jsonld=jl,
                switch_path="/rob-run/", games=("rob-run",))


def main():
    for lang in ("en", "ru"):
        prefix = "" if lang == "en" else "ru/"
        write(prefix + "rob-run/federal-raid-countdown/index.html", countdown_page(lang))
        write(prefix + "rob-run/loot-profit-calculator/index.html", profit_page(lang))
        write(prefix + "rob-run/squad-loot-splitter/index.html", split_page(lang))
    write("ru/rob-run/kak-ubrat-lagi/index.html", lag_page())
    print("rob run build done")


if __name__ == "__main__":
    main()

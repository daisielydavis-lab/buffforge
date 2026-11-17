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
        + '<h2 class="sec">Как исправить Failed to Enter Location в ROB RUN</h2>'
        + '<p>Начните с простых действий. Не стоит сразу переустанавливать игру или менять сервер.</p>'
        + '<h3>Способ 1. Проверьте, открываются ли другие районы</h3>'
        + '<p>Сначала попробуйте войти в другую доступную локацию.</p>'
        + '<p><b>Если другие места работают:</b> Проверьте, могут ли ваши друзья войти в тот же дом или поселение. Когда ошибка возникает только в одной точке, проблема может быть связана с этой локацией.</p>'
        + '<p><b>Если не открывается ни одна локация:</b> Проверьте общее подключение к игровому региону и наличие свежих сообщений о технических неполадках.</p>'
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
        + '<ol><li>Полностью закройте ROB RUN.</li>'
        + '<li>Убедитесь, что игра завершила работу.</li>'
        + '<li>Перезапустите Steam.</li>'
        + '<li>Запустите ROB RUN из библиотеки Steam.</li>'
        + '<li>Повторите попытку входа в нужную локацию.</li></ol>'
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


def main():
    for lang in ("en", "ru"):
        prefix = "" if lang == "en" else "ru/"
        write(prefix + "rob-run/federal-raid-countdown/index.html", countdown_page(lang))
        write(prefix + "rob-run/loot-profit-calculator/index.html", profit_page(lang))
        write(prefix + "rob-run/squad-loot-splitter/index.html", split_page(lang))
        write(status_rel(lang), status_render(lang))
    write("rob-run/lag-and-high-ping/index.html", lag_page("en"))
    write("ru/rob-run/kak-ubrat-lagi/index.html", lag_page("ru"))
    write("ru/rob-run/failed-to-enter-location/index.html", failed_location_page())
    print("rob run build done")


if __name__ == "__main__":
    main()

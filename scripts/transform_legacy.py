#!/usr/bin/env python3
"""Re-skin legacy tool pages into the unified shell (spec sections 8, 13).

Run:  cd <repo root> && python3 scripts/transform_legacy.py
- AION 2 tracker (EN + RU): original countdown / checklist / localStorage
  logic is preserved VERBATIM — only the <head>, CSS, header and footer
  change. Google Fonts links are removed; the tracker now uses
  assets/site.css (.tracker styles, light shell only).
- GTA 6 Wanted Evidence Helper (EN + RU): same treatment; the heat scale
  stays the tool's own scale, the Pre-launch badge is added, and the RU
  version localises the UI while keeping the same logic.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import (EMAIL, breadcrumb_jsonld, crumbs_html, page)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRACKER_SRC = os.path.join(ROOT, "scripts", "legacy", "aion-2-daily-tracker.html")
WANTED_SRC = os.path.join(ROOT, "scripts", "legacy", "gta-6-wanted-evidence-helper.html")
# NOTE: these are the pre-shell artifact originals (git 92c3234). The transform
# reads them, never the generated pages — so re-running is idempotent.


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", rel)


def extract_script(html):
    # Longest inline script wins: the tool JS, not the small shell helpers.
    scripts = re.findall(r"<script>(.*?)</script>", html, re.S)
    assert scripts, "no inline script found"
    return max(scripts, key=len)


def extract_main(html):
    m = re.search(r"<main[^>]*>(.*?)</main>", html, re.S)
    assert m, "no <main> found"
    return m.group(1)


def replace_block(script, varname, new_js_literal):
    """Replace `var NAME = [...];` (possibly multiline) with a new literal."""
    pat = re.compile(r"var %s = \[.*?\n        \];" % varname, re.S)
    assert pat.search(script), "block %s not found" % varname
    return pat.sub("var %s = %s;" % (varname, new_js_literal), script, count=1)


# ---------------------------------------------------------------- tracker
def tracker_body_en():
    html = read(TRACKER_SRC)
    m = re.search(r"    <div class=\"wrap\">(.*?)    </div>\n\n    <script>", html, re.S)
    assert m, "tracker wrap not found"
    inner = m.group(1)
    inner = inner.replace(
        '<p class="disclaimer"><strong>Disclaimer:</strong>',
        '<p><strong>Spotted a wrong number?</strong> Email '
        '<a href="mailto:%s">%s</a> with the page and the number.</p>\n        '
        '<p class="disclaimer"><strong>Disclaimer:</strong>' % (EMAIL, EMAIL))
    return inner


RU_DAILY = [
    {"id": "duty", "name": "Ежедневные задания",
     "detail": "<strong>5</strong> платных выполнений в день. Единственный счётчик, который <strong>нельзя накопить</strong>, — используйте или потеряете.",
     "chips": [["scope", "На сервер"], ["refill", "Обновляется при сбросе"], ["nobank", "Не копится"]]},
    {"id": "odyl", "name": "Эфирная энергия",
     "detail": "Восстанавливается <strong>+15 каждые 3 часа</strong> (120 в день). Траты на кубы подземелий — <strong>40 за получение</strong>.",
     "chips": [["cap", "Лимит 560 · 840 с подпиской"]]},
    {"id": "nightmare-daily", "name": "Кошмар",
     "detail": "<strong>2 попытки</strong> в день, неиспользованные попытки накапливаются.",
     "chips": [["cap", "Копится до 14"]]},
    {"id": "shugo", "name": "Ключи фестиваля Шуго",
     "detail": "<strong>+3 ключа</strong> в день.",
     "chips": [["scope", "На сервер"], ["cap", "Лимит 12 · 21 с подпиской"], ["verify", "Проверьте в игре — трекеры расходятся (другой указывает 28/56)"]]},
    {"id": "invasion", "name": "Вторжение измерений",
     "detail": "<strong>1 ключ награды</strong> в день.",
     "chips": [["scope", "Общий на сервер"], ["cap", "Копится до 7"]]},
    {"id": "conquest-daily", "name": "Счётчик наград завоевания",
     "detail": "Восстанавливается <strong>+1 каждые 8 часов</strong>.",
     "chips": [["cap", "Лимит 21"], ["verify", "Проверьте в игре — трекеры расходятся (другой указывает 2/день, лимит 14)"]]},
    {"id": "transcendence-daily", "name": "Счётчик наград превосходства",
     "detail": "Восстанавливается <strong>+1 каждые 12 часов</strong>.",
     "chips": [["cap", "Лимит 14"]]},
    {"id": "gathering", "name": "Собирательство",
     "detail": "<strong>1000 сборов</strong> в день.",
     "chips": [["scope", "На сервер"]]},
]

RU_WEEKLY = [
    {"id": "ludra", "name": "Кузница Бездны — Лудра",
     "detail": "Рейд святилища, 10 игроков. <strong>4 попытки</strong>, <strong>1 награда за убийство</strong> на персонажа. Уровень предметов <strong>2800</strong> обычный / <strong>3000</strong> сложный. Сундук стоит <strong>40 эфирной энергии</strong>. Лимит времени — 2 часа (патч 11 ноября).",
     "chips": [["scope", "На персонажа"]]},
    {"id": "ascension", "name": "Испытание восхождения",
     "detail": "<strong>3 входа</strong> в неделю.", "chips": []},
    {"id": "abyss-time", "name": "Время в Бездне",
     "detail": "<strong>7 часов</strong> Нижняя Решанта · <strong>7 часов</strong> Средняя Решанта · <strong>3 часа</strong> Внешняя Решанта.",
     "chips": []},
    {"id": "boss-kills", "name": "Финальные боссы завоевания и превосходства",
     "detail": "Завоевание: <strong>35 убийств</strong> в неделю. Превосходство: <strong>28 убийств</strong> в неделю.",
     "chips": []},
    {"id": "fissure", "name": "Подземелье — Неизвестный разлом",
     "detail": "<strong>14 входов</strong> в неделю.",
     "chips": [["scope", "Общий на сервер"]]},
    {"id": "nightmare-shop", "name": "Магазин Кошмара",
     "detail": "Кодекс души <strong>×5</strong> в неделю · Кодекс души: сброс <strong>×3</strong> в неделю.",
     "chips": []},
    {"id": "sync-stones", "name": "Еженедельные задания — камни синхронизации",
     "detail": "Максимум <strong>3 камня синхронизации</strong> в неделю (патч 11 ноября).",
     "chips": []},
    {"id": "unclaimed", "name": "Незабранные заходы в подземелья",
     "detail": "<strong>10</strong> в неделю. Выход из подземелья без получения куба тратит один заход.",
     "chips": [["scope", "На сервер"]]},
]

RU_EVENTS = [
    {"name": "Отметки Лудры", "detail": "7 наград за 14 дней.", "endsLabel": "Заканчивается 17 ноября 2026",
     "end": "Date.UTC(2026, 10, 17, 7, 0, 0)"},
    {"name": "Twitch Drops", "detail": "Кампания за просмотры.", "endsLabel": "Заканчивается 17 ноября 2026",
     "end": "Date.UTC(2026, 10, 17, 7, 0, 0)"},
    {"name": "Лагерь дэва", "detail": "Событие-веха сервера.", "endsLabel": "Заканчивается 17 ноября 2026",
     "end": "Date.UTC(2026, 10, 17, 7, 0, 0)"},
    {"name": "Охота на Лудру", "detail": "Победите Лудру до техобслуживания.",
     "endsLabel": "Заканчивается с техобслуживанием · 24 ноября (PST) / 25 ноября (CET), 2026",
     "end": "Date.UTC(2026, 10, 25, 6, 30, 0)"},
    {"name": "Сезон 1", "detail": "Первый сезон глобального сервиса.", "endsLabel": "Заканчивается 16 декабря 2026",
     "end": "Date.UTC(2026, 11, 16, 7, 0, 0)"},
]


def js_literal_with_dates(items):
    """JSON-dump items, but keep Date.UTC(...) expressions as raw JS."""
    parts = []
    for it in items:
        fields = []
        for k, v in it.items():
            if k == "end":
                fields.append('"end": %s' % v)
            else:
                fields.append('%s: %s' % (json.dumps(k, ensure_ascii=False),
                                          json.dumps(v, ensure_ascii=False)))
        parts.append("{" + ", ".join(fields) + "}")
    return "[\n          " + ",\n          ".join(parts) + "\n        ]"


def tracker_ru_script():
    script = extract_script(read(TRACKER_SRC))
    script = replace_block(script, "DAILY", json.dumps(RU_DAILY, ensure_ascii=False))
    script = replace_block(script, "WEEKLY", json.dumps(RU_WEEKLY, ensure_ascii=False))
    script = replace_block(script, "EVENTS", js_literal_with_dates(RU_EVENTS))
    script = script.replace('"aion2-tracker-daily-v1"', '"aion2-tracker-daily-v1-ru"')
    script = script.replace('"aion2-tracker-weekly-v1"', '"aion2-tracker-weekly-v1-ru"')
    script = script.replace('date.toLocaleString(undefined, opts)',
                            'date.toLocaleString("ru-RU", opts)')
    script = script.replace('"Ended"', '"Завершено"')
    script = script.replace("'<span class=\"unit\">h left</span>'", "'<span class=\"unit\">ч осталось</span>'")
    script = script.replace("'<span class=\"unit\">m left</span>'", "'<span class=\"unit\">мин осталось</span>'")
    script = script.replace("'<span class=\"unit\">h</span>' + pad(m) + '<span class=\"unit\">m left</span>'",
                            "'<span class=\"unit\">ч</span>' + pad(m) + '<span class=\"unit\">мин осталось</span>'")
    return script


def tracker_ru_body():
    return """
      <header>
        <p class="kicker">Глобальные серверы · NA / EU / SA / Азия</p>
        <h1>Трекер ежедневных и еженедельных заданий AION 2</h1>
        <p class="lede">Все ежедневные и еженедельные счётчики, важные на 45 уровне, с живым обратным отсчётом до сброса. Отмечайте выполненное — галочки сохраняются на этом устройстве и сами сбрасываются после сброса.</p>
        <span class="stamp">Данные на 13 ноября 2026 · глобальная сборка после патча 11 ноября</span>
      </header>

      <div class="resets">
        <div class="reset-card">
          <p class="label">До ежедневного сброса</p>
          <p class="count" id="daily-count">—</p>
          <p class="reset-meta">Сброс <strong>в 10:00 МСК (07:00 UTC)</strong> каждый день · ваше время: <strong id="daily-local">—</strong></p>
        </div>
        <div class="reset-card">
          <p class="label">До еженедельного сброса</p>
          <p class="count" id="weekly-count">—</p>
          <p class="reset-meta">Сброс <strong>в среду в 10:00 МСК (07:00 UTC)</strong> · ваше время: <strong id="weekly-local">—</strong></p>
          <p class="maint-note">Еженедельное техобслуживание начинается примерно за 30 минут до сброса в среду.</p>
        </div>
      </div>

      <section aria-labelledby="daily-h">
        <div class="section-head">
          <h2 id="daily-h">Ежедневные задания</h2>
          <span class="progress-text"><b id="daily-done">0</b> из 8 выполнено</span>
        </div>
        <div class="progress-bar" role="progressbar" aria-label="Прогресс за день" aria-valuemin="0" aria-valuemax="8" aria-valuenow="0" id="daily-bar-wrap"><div class="progress-fill" id="daily-bar"></div></div>
        <p class="section-note">Все счётчики ниже сбрасываются в 10:00 МСК (07:00 UTC). Лимиты — для персонажа 45 уровня, по данным трекеров из клиента; где трекеры расходятся, строка помечена, чтобы вы сверились в игре.</p>
        <ul class="list" id="daily-list"></ul>
      </section>

      <section aria-labelledby="weekly-h">
        <div class="section-head">
          <h2 id="weekly-h">Еженедельные задания</h2>
          <span class="progress-text"><b id="weekly-done">0</b> из 8 выполнено</span>
        </div>
        <div class="progress-bar" role="progressbar" aria-label="Прогресс за неделю" aria-valuemin="0" aria-valuemax="8" aria-valuenow="0" id="weekly-bar-wrap"><div class="progress-fill" id="weekly-bar"></div></div>
        <p class="section-note">Всё здесь сбрасывается в среду в 10:00 МСК (07:00 UTC) — в тот же момент, что и ежедневный сброс этого дня.</p>
        <ul class="list" id="weekly-list"></ul>
      </section>

      <section aria-labelledby="events-h">
        <div class="section-head">
          <h2 id="events-h">Активные события</h2>
        </div>
        <p class="section-note">Даты окончания — по объявлениям NC. Обратный отсчёт идёт до 10:00 МСК (07:00 UTC) в день окончания — до ежедневного сброса, кроме «Охоты на Лудру», которая заканчивается с техобслуживанием. Это отдельно от внутриигрового дня посещаемости и событий, который меняется в 11:00 МСК (08:00 UTC), — см. ниже.</p>
        <ul class="events" id="event-list"></ul>
      </section>

      <footer>
        <div class="footnotes">
          <p><strong>Посещаемость меняется позже.</strong> NC никогда не публиковала единого времени сброса: счётчики подземелий и контента сбрасываются в 10:00 МСК (07:00 UTC), а внутриигровой день посещаемости и событий меняется на час позже — в <strong>11:00 МСК (08:00 UTC)</strong>.</p>
          <p><strong>В других регионах иначе.</strong> Серверы Кореи и Тайваня сбрасываются в другое время (05:00 по серверному времени). Эта страница отслеживает только глобальный сервис.</p>
          <p><strong>Нашли неверную цифру?</strong> Напишите на <a href="mailto:%s">%s</a>, указав страницу и цифру.</p>
        </div>
        <div class="sources">
          <p>Источники</p>
          <ul>
            <li><a href="https://timesaver.gg" target="_blank" rel="noopener">timesaver.gg</a> — гайд по сбросам</li>
            <li><a href="https://metabot.gg" target="_blank" rel="noopener">metabot.gg</a> — эндгейм-гайд</li>
            <li><a href="https://aion2.gg" target="_blank" rel="noopener">aion2.gg</a> — гайд по рутине</li>
            <li><a href="https://game8.co" target="_blank" rel="noopener">Game8</a> — гайд по сбросам</li>
          </ul>
        </div>
        <p class="disclaimer"><strong>Дисклеймер:</strong> счётчики — по данным трекеров из клиента, а не по заявлению NC. NC никогда не публиковала единого времени сброса — всегда сверяйтесь в игре. День посещаемости и событий меняется в 11:00 МСК (08:00 UTC), на час позже счётчиков контента.</p>
      </footer>
""" % (EMAIL, EMAIL)


def tracker_page(lang):
    home = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    hub_path = "/aion-2/" if lang == "en" else "/ru/aion-2/"
    if lang == "en":
        title = "AION 2 Daily & Weekly Tracker — BuffForge"
        desc = ("Live countdowns to the daily reset (07:00 UTC) and the Wednesday weekly "
                "reset for AION 2 global servers. Tick duties off — they clear themselves at reset.")
        name = "Daily & Weekly Tracker"
        body_inner = tracker_body_en()
        script = extract_script(read(TRACKER_SRC))
    else:
        title = "Трекер ежедневных и еженедельных заданий AION 2 — BuffForge"
        desc = ("Живой обратный отсчёт до ежедневного сброса (10:00 МСК) и еженедельного "
                "сброса в среду для глобальных серверов AION 2. Отмечайте задания — галочки сбрасываются сами.")
        name = "Трекер ежедневных и еженедельных заданий"
        body_inner = tracker_ru_body()
        script = tracker_ru_script()
    canon = "/aion-2/daily-tracker/" if lang == "en" else "/ru/aion-2/daily-tracker/"
    alt = {"en": "/aion-2/daily-tracker/", "ru": "/ru/aion-2/daily-tracker/"}
    jl = [breadcrumb_jsonld(lang, [(home, home_path), ("AION 2", hub_path), (name, canon)]),
          {"@context": "https://schema.org", "@type": "WebApplication",
           "name": name, "url": "https://buffforge.com" + canon, "inLanguage": lang,
           "applicationCategory": "GameApplication", "operatingSystem": "Any modern browser",
           "offers": {"@type": "Offer", "price": "0"}}]
    body = ('<main id="main" class="wrap">%s<div class="tracker">%s</div></main>'
            % (crumbs_html(lang, [("AION 2", hub_path), (name, None)]), body_inner))
    return page(lang, title, desc, canon, alt, body, jsonld=jl,
                games=("aion-2",), tail="<script>%s</script>\n" % script)


# ---------------------------------------------------------------- wanted evidence helper
RU_EVIDENCE = {
    "face": {"name": "Лицо", "action": "Смените внешность и не высовывайтесь, пока не остынете."},
    "clothes": {"name": "Одежда", "action": "Смените одежду — именно её описали свидетели."},
    "cctv": {"name": "Камеры", "action": "Покиньте район и не попадайтесь на камеры."},
    "duo": {"name": "Дуэт", "action": "Разойдитесь с напарником на время."},
    "car": {"name": "Транспорт", "action": "Бросьте машину или пересядьте на другую."},
    "weapon": {"name": "Оружие", "action": "Спрячьте его в багажник — при себе остаются только две винтовки и два пистолета."},
}


def wanted_body_en():
    main = extract_main(read(WANTED_SRC))
    main = main.replace('<section class="hero">', '<section class="tool-hero">')
    main = main.replace('<section class="how">', '<section class="how-box">')
    main = main.replace('<section class="plan">', '<section class="plan-box">')
    main = main.replace('<button class="reset" ', '<button class="reset-btn" ')
    return main


def wanted_body_ru():
    return """
  <section class="tool-hero">
    <h1>Помощник по уликам розыска GTA 6 — <span>что о вас знает полиция?</span></h1>
    <p class="sub">В GTA 6 вернулись шесть звёзд розыска — и теперь полиция действует по уликам, которых шесть видов. Отметьте, что у них на вас есть, и получите план, как «остыть».</p>
  </section>

  <div class="note-box amber" style="margin-top:24px"><h3>До выхода — по материалам превью</h3>
  <p>Механика описана по предрелизным превью. Шкала нагрева — собственная шкала инструмента, а не цифра из игры. После выхода 19 ноября 2026 года сверим с живой игрой.</p></div>

  <section class="how-box">
    <h2>Как работает система улик</h2>
    <ul>
      <li><b>Шесть звёзд вернулись.</b> В GTA 5 было пять, в GTA 6 — шесть.</li>
      <li><b>Звёзды зависят от улик, а не только от шума.</b> То, что полиция о вас знает, влияет на то, как сильно вас ищут, — и это знание бывает шести видов (ниже).</li>
      <li><b>Свидетели важны.</b> Полиция действует по тому, что люди реально видели и сообщили.</li>
      <li><b>Наличные под риском.</b> Наличные при себе теряются при смерти или аресте; деньги на совместном банковском счёте в безопасности.</li>
      <li><b>«Криминальный профиль» — отдельная система.</b> Она отслеживает, как именно вы совершаете преступления. Это не шкала «добро-зло».</li>
    </ul>
  </section>

  <h2 class="sec">Какие улики есть на вас?</h2>
  <p>Отметьте всё, что подходит прямо сейчас. Галочки сохраняются в этом браузере.</p>

  <div class="ev-grid" id="evidenceGrid">
    <label class="ev" data-ev="face">
      <input type="checkbox" value="face">
      <span class="name"><span class="emoji">&#128100;</span> Лицо <span class="box">&#10003;</span></span>
      <span class="desc">Свидетели видели ваше лицо.</span>
    </label>
    <label class="ev" data-ev="clothes">
      <input type="checkbox" value="clothes">
      <span class="name"><span class="emoji">&#128090;</span> Одежда <span class="box">&#10003;</span></span>
      <span class="desc">Очевидцы сообщили о вашей одежде.</span>
    </label>
    <label class="ev" data-ev="cctv">
      <input type="checkbox" value="cctv">
      <span class="name"><span class="emoji">&#128250;</span> Камеры <span class="box">&#10003;</span></span>
      <span class="desc">Камеры вас засняли.</span>
    </label>
    <label class="ev" data-ev="duo">
      <input type="checkbox" value="duo">
      <span class="name"><span class="emoji">&#128101;</span> Дуэт <span class="box">&#10003;</span></span>
      <span class="desc">Вашего напарника опознали вместе с вами.</span>
    </label>
    <label class="ev" data-ev="car">
      <input type="checkbox" value="car">
      <span class="name"><span class="emoji">&#128663;</span> Транспорт <span class="box">&#10003;</span></span>
      <span class="desc">Вашу машину заметили.</span>
    </label>
    <label class="ev" data-ev="weapon">
      <input type="checkbox" value="weapon">
      <span class="name"><span class="emoji">&#128299;</span> Оружие <span class="box">&#10003;</span></span>
      <span class="desc">Ваше оружие видели.</span>
    </label>
  </div>

  <div class="heat">
    <div class="top">
      <div class="stars" id="stars" aria-hidden="true">
        <span class="star">&#9733;</span><span class="star">&#9733;</span><span class="star">&#9733;</span><span class="star">&#9733;</span><span class="star">&#9733;</span><span class="star">&#9733;</span>
      </div>
      <div class="lights" id="lights" aria-hidden="true">
        <span class="light red"></span><span class="light blue"></span><span class="light calm"></span>
      </div>
    </div>
    <div class="row">
      <span class="label clean" id="heatLabel">Чисто</span>
      <span class="count" id="heatCount">0 из 6 типов улик</span>
    </div>
    <div class="bar"><i id="heatBar"></i></div>
    <p class="note">Нагрев — собственная шкала инструмента по числу отмеченных типов улик, а не цифра из игры. Чем больше типов улик у полиции, тем сложнее оторваться.</p>
  </div>

  <div class="actions-grid" id="actions"></div>

  <section class="plan-box">
    <h2>Ваш план «остыть»</h2>
    <div id="planBody"></div>
    <button class="reset-btn" id="resetBtn" type="button">Сбросить всё</button>
  </section>

  <section class="unknown">
    <h2>Чего мы пока не знаем</h2>
    <ul>
      <li>Сколько именно звёзд даёт каждый тип улик и как быстро спадает нагрев — до выхода не подтверждено.</li>
      <li>Как именно работают поиски и периметры полиции — в превью описано, но цифр в открытом доступе нет.</li>
      <li>После выхода 19 ноября 2026 года проверим по живой игре и обновим эту страницу.</li>
    </ul>
  </section>
"""


def wanted_ru_script():
    script = extract_script(read(WANTED_SRC))
    # Replace the EVIDENCE dict with the Russian one.
    pat = re.compile(r"var EVIDENCE = \{.*?\n  \};", re.S)
    assert pat.search(script), "EVIDENCE dict not found"
    ru = "var EVIDENCE = {\n" + ",\n".join(
        '    %s: { name: %s, action: %s }' % (k, json.dumps(v["name"], ensure_ascii=False),
                                              json.dumps(v["action"], ensure_ascii=False))
        for k, v in RU_EVIDENCE.items()) + "\n  };"
    script = pat.sub(ru, script, count=1)
    script = script.replace("var KEY = 'bf-gta6-evidence-v1';",
                            "var KEY = 'bf-gta6-evidence-v1-ru';")
    script = script.replace(
        "var level = n === 0 ? 'Clean' : n <= 2 ? 'Warm' : n <= 4 ? 'Hot' : 'Burned';",
        "var levelKey = n === 0 ? 'clean' : n <= 2 ? 'warm' : n <= 4 ? 'hot' : 'burned';\n"
        "    var level = {clean: 'Чисто', warm: 'Тепло', hot: 'Горячо', burned: 'Пожар'}[levelKey];")
    script = script.replace("heatLabel.className = 'label ' + level.toLowerCase();",
                            "heatLabel.className = 'label ' + levelKey;")
    script = script.replace("heatCount.textContent = n + ' of 6 evidence types';",
                            "heatCount.textContent = n + ' из 6 типов улик';")
    script = script.replace("txt.innerHTML = '<b>You are clean.</b> No evidence on file — nothing to clear.';",
                            "txt.innerHTML = '<b>Вы чисты.</b> Улик нет — очищать нечего.';")
    script = script.replace("li1.innerHTML = '<b>Break line of sight and leave the search area.</b>';",
                            "li1.innerHTML = '<b>Оторвитесь от погони и покиньте зону поисков.</b>';")
    return script


def wanted_page(lang):
    home = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    hub_path = "/gta-6/" if lang == "en" else "/ru/gta-6/"
    if lang == "en":
        title = "GTA 6 Wanted Evidence Helper — What Do the Cops Know About You? | BuffForge"
        desc = ("Tick the evidence the police hold on you in GTA 6 — face, clothes, CCTV, "
                "the duo, your car, your weapon — and get a plan to go cold. "
                "Based on confirmed pre-release previews.")
        name = "Wanted Evidence Helper"
        inner = wanted_body_en()
        script = extract_script(read(WANTED_SRC))
        badge_html = ('<div class="note-box amber" style="margin-top:24px"><h3>Pre-launch — based on pre-release previews</h3>'
                      '<p>The heat scale is the tool\u2019s own scale, not an in-game number. '
                      'Star values and fade speed are not confirmed before launch; '
                      'this page will be verified against the live game after Nov 19, 2026.</p></div>')
        inner = inner.replace('<section class="how-box">', badge_html + '\n  <section class="how-box">', 1)
        # Sources + correction line (the original page footer is replaced by the shell footer).
        inner += ('<p class="data-line">Based on pre-release hands-on previews '
                  '(Rockstar North, Nov 2026). Mechanics may change at launch. '
                  'Sources: gta6.how gameplay page; Flow Games preview via gtavice.net. '
                  'Data version: Nov 12, 2026. Spotted a wrong number? Email '
                  '<a href="mailto:%s">%s</a>.</p>' % (EMAIL, EMAIL))
    else:
        title = "Помощник по уликам розыска GTA 6 — что о вас знает полиция? | BuffForge"
        desc = ("Отметьте улики, которые есть у полиции в GTA 6: лицо, одежду, камеры, "
                "дуэт, транспорт, оружие — и получите план, как «остыть». По предрелизным превью.")
        name = "Помощник по уликам розыска"
        inner = wanted_body_ru()
        script = wanted_ru_script()
        inner += ('<p class="data-line">По предрелизным превью (Rockstar North, ноябрь 2026). '
                  'Механика может измениться к выходу. Данные на 12 ноября 2026 года. '
                  'Нашли ошибку? Напишите на <a href="mailto:%s">%s</a>.</p>' % (EMAIL, EMAIL))
    canon = "/gta-6/wanted-evidence-helper/" if lang == "en" else "/ru/gta-6/wanted-evidence-helper/"
    alt = {"en": "/gta-6/wanted-evidence-helper/", "ru": "/ru/gta-6/wanted-evidence-helper/"}
    jl = [breadcrumb_jsonld(lang, [(home, home_path), ("GTA 6", hub_path), (name, canon)]),
          {"@context": "https://schema.org", "@type": "WebApplication",
           "name": name, "url": "https://buffforge.com" + canon, "inLanguage": lang,
           "applicationCategory": "GameApplication", "operatingSystem": "Any modern browser",
           "offers": {"@type": "Offer", "price": "0"}}]
    body = ('<main id="main" class="wrap">%s%s</main>'
            % (crumbs_html(lang, [("GTA 6", hub_path), (name, None)]), inner))
    return page(lang, title, desc, canon, alt, body, jsonld=jl,
                games=("gta-6",), tail="<script>%s</script>\n" % script)


def main():
    write("aion-2/daily-tracker/index.html", tracker_page("en"))
    write("ru/aion-2/daily-tracker/index.html", tracker_page("ru"))
    write("gta-6/wanted-evidence-helper/index.html", wanted_page("en"))
    write("ru/gta-6/wanted-evidence-helper/index.html", wanted_page("ru"))
    print("legacy transform done")


if __name__ == "__main__":
    main()

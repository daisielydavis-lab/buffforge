"""Build the DPS fuse-or-salvage calculator pages (EN + RU) from the
Daylight Forge prototype.

The prototype HTML/JS is migrated into the site shell (shared head,
header, footer, GTM). The fusion table and calculator JS are used
verbatim for EN; for RU only UI strings are translated — the odds table,
brackets, and math are untouched. No invented rows, no Demo-era table.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import BASE, breadcrumb_jsonld, crumbs_html, page  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROTO = os.path.expanduser(
    "~/workspace/buffforge-design-prototype/buffforge-homepage-prototype/"
    "desktop-pension-squad/fuse-salvage-calculator/index.html")

EN = {
    "title": "DPS fusion calculator: fuse vs salvage odds — BuffForge",
    "desc": ("Free Desktop Pension Squad fusion calculator. Check nine-item "
             "fuse odds for every level bracket, and compare expected Soul "
             "from fusing versus salvaging. Odds from game client v1.0.2 "
             "via DPSquad Wiki."),
    "crumb": "Fuse or Salvage Calculator",
}
RU = {
    "title": "Калькулятор слияния DPS: шансы и разбор на Soul — BuffForge",
    "desc": ("Бесплатный калькулятор слияния Desktop Pension Squad. "
             "Проверьте шансы слияния девяти предметов для каждого диапазона "
             "уровней и сравните ожидаемый Soul от слияния и от разбора. "
             "Шансы — из клиента игры v1.0.2, через DPSquad Wiki."),
    "crumb": "Калькулятор слияния и разбора",
}

# (english, russian) pairs for the static body HTML. Applied in order;
# a missing source string fails the build loudly instead of silently
# leaving English behind.
RU_BODY = [
    ("DPS fusion calculator: fuse odds vs salvage",
     "Калькулятор слияния DPS: шансы против разбора"),
    ("Nine items of the same category and rarity go into the Workshop cube and one comes out. "
     "This calculator uses the listed fuse odds for every level bracket, and — if you enter sell prices — "
     "compares expected Soul from fusing versus salvaging everything.",
     "Девять предметов одной категории и редкости отправляются в куб мастерской — а выходит один. "
     "Калькулятор использует указанные шансы слияния для каждого диапазона уровней и — если ввести цены продажи — "
     "сравнивает ожидаемый Soul от слияния и от разбора всего."),
    ("Odds from <a href=\"https://dpsquad.wiki/workshop\" rel=\"noopener noreferrer\">DPSquad Wiki</a> "
     "(game client, wiki read 12 Nov 2026). BuffForge review: 12 Nov 2026, Pacific Time. "
     "Listed percentages are rounded and then normalized. <a href=\"#faq\">Source notes</a>.",
     "Шансы: <a href=\"https://dpsquad.wiki/workshop\" rel=\"noopener noreferrer\">DPSquad Wiki</a> "
     "(клиент игры, вики прочитана 12 ноября 2026). Проверка BuffForge: 12 ноября 2026, тихоокеанское время. "
     "Указанные проценты округлены, затем нормализованы. <a href=\"#faq\">Примечания об источниках</a>."),
    ("Your batch", "Ваша партия"),
    ("Level bracket", "Диапазон уровней"),
    ("Input rarity", "Редкость входа"),
    ("All nine items must share this rarity, one category, and this bracket. Unequip them first.",
     "Все девять предметов должны иметь эту редкость, одну категорию и этот диапазон. Сначала снимите их."),
    ("How many items you have", "Сколько у вас предметов"),
    ("9 · one fuse", "9 · одно слияние"),
    ("Target rarity", "Целевая редкость"),
    ("Chance of this rarity or higher, in the fusions your stock allows.",
     "Шанс получить эту редкость или выше за слияния, на которые хватает запаса."),
    ("Reset", "Сбросить"),
    ("Copy results", "Скопировать результаты"),
    ("Results", "Результаты"),
    ("Complete fusions", "Полных слияний"),
    ("leftover items", "осталось предметов"),
    ("<em>Expected hits</em>", "<em>Ожидаемо выпадений</em>"),
    ("Average target-or-better items", "В среднем предметов цели или выше"),
    ("At least one target hit", "Хотя бы одно попадание в цель"),
    ("Set a batch to see the chance.", "Задайте партию, чтобы увидеть шанс."),
    ("Possible outcomes", "Возможные исходы"),
    ("Chance over more fusions", "Шанс при большем числе слияний"),
    ("Optional: compare Soul (enter sell prices)",
     "Необязательно: сравнить Soul (укажите цены продажи)"),
    ("Salvage pays the item’s sell price in Soul. There is no single official “Soul table” — "
     "leave fields blank if you don’t know. Blank is unknown, not zero.",
     "Разбор даёт Soul, равный цене продажи предмета. Единой официальной «таблицы Soul» нет — "
     "если не знаете цену, оставьте поле пустым. Пустое поле — неизвестно, а не ноль."),
    ("Soul per input item", "Soul за один входной предмет"),
    ("Sell price", "Цена продажи"),
    ("Salvage all", "Разобрать всё"),
    ("Fuse, then salvage", "Слить, потом разобрать"),
    ("Difference", "Разница"),
    ("Enter input value", "Введите цену входа"),
    ("Enter output values", "Введите цены выходов"),
    ("Enter the input Soul value and every outcome’s Soul value for a comparison. "
     "Usefulness and Steam market prices are not included.",
     "Введите Soul входа и Soul каждого исхода, чтобы сравнить. "
     "Полезность предметов и цены Steam не учитываются."),
    ("<p class=\"sec-label\">Questions</p>", "<p class=\"sec-label\">Вопросы</p>"),
    ("<h2>FAQ</h2>", "<h2>Частые вопросы</h2>"),
    ("How does fusion work?", "Как работает слияние?"),
    ("Fill nine cube slots with unequipped items of one category, one rarity, and a required level inside the chosen bracket. "
     "They are consumed; one item comes out, drawn from the recipe’s list. Only category, rarity and bracket matter — "
     "not the items’ own tier or stats. Higher brackets need a higher Cube level. Source: DPSquad Wiki / Workshop.",
     "Заполните девять слотов куба предметами без экипировки одной категории, одной редкости и нужного уровня "
     "в выбранном диапазоне. Они расходуются, а выходит один предмет из списка рецепта. Важны только категория, "
     "редкость и диапазон — не тир и не характеристики самих предметов. Для более высоких диапазонов нужен "
     "более высокий уровень куба. Источник: DPSquad Wiki / Workshop."),
    ("Where do these odds come from?", "Откуда берутся эти шансы?"),
    ("They are transcribed from the DPSquad Wiki Workshop table, which cites the game client, full-game build 26611958 (v1.0.2), read 12 Nov 2026. "
     "BuffForge reviewed that table on 12 Nov 2026. The figures are the game’s own rounded percentages; we normalize them so a roll sums to 100%. "
     "Some older or demo-era databases (for example X1X’s demo notes) list different, simpler results — Unique and above always becoming Epic. "
     "We follow the full-game client dump, and we will update if the game changes. We never invent a row that the source does not list.",
     "Они переписаны из таблицы Workshop на DPSquad Wiki, которая ссылается на клиент игры, полную сборку 26611958 (v1.0.2), "
     "прочитанную 12 ноября 2026 года. BuffForge сверил эту таблицу 12 ноября 2026 года. Цифры — округлённые проценты самой игры; "
     "мы нормализуем их, чтобы сумма одного броска была 100%. Некоторые старые базы эпохи демо (например, заметки X1X) дают другие, "
     "более простые результаты — Unique и выше всегда становятся Epic. Мы следуем дампу клиента полной игры и обновим данные, "
     "если игра изменится. Мы никогда не выдумываем строки, которых нет в источнике."),
    ("When does salvaging make sense?", "Когда разбор выгоден?"),
    ("Salvage converts 1–9 unequipped items with a sell price into Soul equal to the sum of those prices. "
     "Fuse then salvage only “wins” on Soul if the expected output sell value beats nine times the input. "
     "Even when it does not, fusing can still be worth it if you want the higher-grade item itself. "
     "Soul comparison here is optional and uses only the prices you type.",
     "Разбор превращает 1–9 предметов без экипировки с ценой продажи в Soul, равный сумме этих цен. "
     "«Слить, потом разобрать» выигрывает по Soul, только если ожидаемая цена продажи выхода больше девяти цен входа. "
     "Даже если нет, слияние может стоить того, если нужен сам предмет более высокой редкости. "
     "Сравнение Soul здесь необязательно и использует только введённые вами цены."),
    ("How is the “at least one” chance calculated?", "Как считается шанс «хотя бы раз»?"),
    ("If each fusion has probability p of hitting the target or better, n complete fusions have chance 1 − (1 − p)<sup>n</sup> "
     "of at least one hit, assuming independent rolls and no pity. The wiki and a third-party demo-era write-up both say there is no pity. "
     "Expected hits are n × p.",
     "Если каждое слияние с вероятностью p даёт цель или выше, то n полных слияний дают шанс 1 − (1 − p)<sup>n</sup> "
     "хотя бы одного попадания при независимых бросках и без pity. И вики, и сторонний разбор эпохи демо говорят, что pity нет. "
     "Ожидаемые попадания — n × p."),
    ("More Desktop Pension Squad tools", "Другие инструменты по Desktop Pension Squad"),
    ("Craft (produce) odds calculator", "Калькулятор шансов крафта (производства)"),
    ("Forgestone recipes and their grade distributions. Planned — the wiki already lists these tables.",
     "Рецепты Forgestone и их распределение по грейдам. Запланировано — вики уже публикует эти таблицы."),
    ("Engraving Soul planner", "Планировщик рун (Soul)"),
    ("How many Soul (and Soul Stone) the rune tree costs, and what is left to buy.",
     "Сколько Soul (и Soul Stone) стоит дерево рун и что осталось купить."),
    ("Drop finder", "Поиск дропа"),
    ("Which stage chests can drop a given piece, by difficulty.",
     "Из каких сундуков этапов может выпасть предмет, по сложности."),
    ("PLANNED", "ЗАПЛАНИРОВАНО"),
]

# (english, russian) pairs for the calculator JS — UI strings only. The odds
# table, brackets, and math are byte-identical between languages.
RU_JS = [
    ("'en-US'", "'ru-RU'"),
    ("'No Cube level required for this first bracket.'",
     "'Для первого диапазона уровень куба не нужен.'"),
    ("'Requires Cube Lv. ' + b.cube + '. Output tier: ' + b.tier + '.'",
     "'Нужен куб ур. ' + b.cube + '. Тир выхода: ' + b.tier + '.'"),
    ("'This recipe is for Lv. 15 Legendary gear only, not every item in the Lv. 10–15 bracket.'",
     "'Этот рецепт — только для снаряжения Legendary ур. 15, а не для всех предметов диапазона ур. 10–15.'"),
    ("'This recipe is for Lv. 30 Immortal gear only, not every item in the Lv. 20–30 bracket.'",
     "'Этот рецепт — только для снаряжения Immortal ур. 30, а не для всех предметов диапазона ур. 20–30.'"),
    ("'This recipe is for Lv. 40 Ascendant gear only, not every item in the Lv. 30–40 bracket.'",
     "'Этот рецепт — только для снаряжения Ascendant ур. 40, а не для всех предметов диапазона ур. 30–40.'"),
    ("'This recipe is for Lv. 50 Primordial gear only, not every item in the Lv. 40–50 bracket.'",
     "'Этот рецепт — только для снаряжения Primordial ур. 50, а не для всех предметов диапазона ур. 40–50.'"),
    ("'Chance of ' + target + ' or better in ' + format(attempts) + ' fusion' + (attempts === 1 ? '' : 's') + '. Per-roll chance: ' + percent(p * 100) + '.'",
     "'Шанс получить ' + target + ' или выше за ' + format(attempts) + ' слияний. Шанс за одно слияние: ' + percent(p * 100) + '.'"),
    ("' input items → ' + format(attempts) + ' complete nine-piece fusion' + (attempts === 1 ? '' : 's') + '. Independent draws assumed; listed odds normalized. No pity is modeled.'",
     "' входных предметов → ' + format(attempts) + ' полных слияний по девять предметов. Независимые броски; указанные шансы нормализованы. Pity не учитывается.'"),
    ("Expected in this batch: ", "Ожидается в этой партии: "),
    ("g + ' or higher'", "g + ' или выше'"),
    ("' <small>normalized ' + norm + '</small>'", "' <small>норм. ' + norm + '</small>'"),
    ("+ ' fuse' + (n === 1 ? '' : 's') + '</span></div>'", "+ ' раз' + '</span></div>'"),
    ("'Soul per ' + g + ' output'", "'Soul за один ' + g + ' на выходе'"),
    ("'Soul salvage value of one ' + g + ' output item'",
     "'Soul за разбор одного ' + g + ' на выходе'"),
    ("input.placeholder = 'Sell price'", "input.placeholder = 'Цена продажи'"),
    ("'Enter input value'", "'Введите цену входа'"),
    ("'Enter output values'", "'Введите цены выходов'"),
    ("'Enter the input Soul value and every outcome’s Soul value for a comparison. Blank fields are unknown, not zero. Item usefulness and Steam prices are excluded.'",
     "'Введите Soul входа и Soul каждого исхода, чтобы сравнить. Пустые поля — неизвестно, а не ноль. Полезность предметов и цены Steam не учитываются.'"),
    ("'Fewer than nine items: a fusion is not possible yet, so only salvage is modeled.'",
     "'Меньше девяти предметов: слияние пока невозможно, моделируется только разбор.'"),
    ("'<strong>Equal expected Soul.</strong> Usefulness is not included — fuse if you want the higher-grade item.'",
     "'<strong>Ожидаемый Soul равен.</strong> Полезность не учитывается — сливайте, если нужен предмет более высокой редкости.'"),
    ("'<strong>Fusion leads by ' + format(delta) + ' expected Soul.</strong> This is an average, not a guarantee. Usefulness and Steam prices are excluded.'",
     "'<strong>Слияние впереди на ' + format(delta) + ' ожидаемого Soul.</strong> Это среднее значение, а не гарантия. Полезность и цены Steam не учитываются.'"),
    ("'<strong>Direct salvage leads by ' + format(Math.abs(delta)) + ' Soul on average.</strong> Fusing may still be worthwhile if you want the higher-grade gear, not just Soul.'",
     "'<strong>Прямой разбор впереди в среднем на ' + format(Math.abs(delta)) + ' Soul.</strong> Слияние всё равно может стоить того, если нужно снаряжение более высокой редкости, а не только Soul.'"),
    ("'Calculator reset.'", "'Калькулятор сброшен.'"),
    ("'Results copied.'", "'Результаты скопированы.'"),
    ("'Copy is blocked in this browser; select and copy the results manually.'",
     "'Копирование заблокировано в этом браузере; выделите и скопируйте результаты вручную.'"),
    ("'DPS: Desktop Pension Squad — Fuse or Salvage Calculator (BuffForge)'",
     "'DPS: Desktop Pension Squad — Калькулятор слияния и разбора (BuffForge)'"),
    ("'Bracket: ' + brackets[r.index].label + ' | Input rarity: ' + r.rarity + ' | Items: ' + r.stock",
     "'Диапазон: ' + brackets[r.index].label + ' | Редкость входа: ' + r.rarity + ' | Предметов: ' + r.stock"),
    ("'Fusions: ' + r.attempts + ' | Leftover: ' + r.leftover",
     "'Слияний: ' + r.attempts + ' | Осталось: ' + r.leftover"),
    ("'Target: ' + r.target + ' or better'", "'Цель: ' + r.target + ' или выше'"),
    ("'Per fusion: ' + percent(r.p * 100) + ' | At least once: ' + percent(r.totalChance * 100) + ' | Expected hits: ' + format(r.expected)",
     "'За одно слияние: ' + percent(r.p * 100) + ' | Хотя бы раз: ' + percent(r.totalChance * 100) + ' | Ожидаемо выпадений: ' + format(r.expected)"),
    ("o.grade + ': ' + percent(o.display) + ' listed'",
     "o.grade + ': ' + percent(o.display) + ' указано'"),
    ("'Salvage all: ' + $('salvage-total').textContent + ' | Fuse then salvage: ' + $('fuse-total').textContent",
     "'Разобрать всё: ' + $('salvage-total').textContent + ' | Слить, потом разобрать: ' + $('fuse-total').textContent"),
    ("'Source: dpsquad.wiki/workshop (game client v1.0.2, build 26611958). Independent rolls, no pity. Reviewed 12 Nov 2026.'",
     "'Источник: dpsquad.wiki/workshop (клиент игры v1.0.2, сборка 26611958). Независимые броски, без pity. Проверка 12 ноября 2026.'"),
]


def replace_all(text, pairs, what):
    for src, dst in pairs:
        if src not in text:
            raise SystemExit("build_dps: %s string not found: %r" % (what, src))
        text = text.replace(src, dst)
    return text


def extract():
    html = open(PROTO, encoding="utf-8").read()
    m = re.search(r"<main id=\"main\">\s*<div class=\"wrap\">(.*)</div>\s*</main>",
                  html, re.S)
    if not m:
        raise SystemExit("build_dps: could not extract prototype body")
    inner = m.group(1)
    inner = re.sub(r"\s*<nav class=\"crumb\"[^>]*>.*?</nav>", "", inner,
                   count=1, flags=re.S)
    js = re.search(r"(<script>\n\(\(\) => \{.*?\n</script>)", html, re.S)
    if not js:
        raise SystemExit("build_dps: could not extract prototype JS")
    return inner, js.group(1)


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", rel)


def dps_page(lang, inner, js):
    meta = EN if lang == "en" else RU
    canon = ("/desktop-pension-squad/fuse-salvage-calculator/"
             if lang == "en"
             else "/ru/desktop-pension-squad/fuse-salvage-calculator/")
    alt = {"en": "/desktop-pension-squad/fuse-salvage-calculator/",
           "ru": "/ru/desktop-pension-squad/fuse-salvage-calculator/"}
    home_label = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    hub_path = ("/desktop-pension-squad/" if lang == "en"
                else "/ru/desktop-pension-squad/")
    crumbs = crumbs_html(lang, [("Desktop Pension Squad", hub_path),
                                (meta["crumb"], None)])
    body = ('<main id="main"><div class="wrap">%s%s</div></main>%s'
            % (crumbs, inner, js))
    jl = [
        {"@context": "https://schema.org", "@type": "WebApplication",
         "name": meta["title"], "url": BASE + canon,
         "applicationCategory": "GameApplication",
         "operatingSystem": "Web browser",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        breadcrumb_jsonld(lang, [(home_label, home_path),
                                 ("Desktop Pension Squad", hub_path),
                                 (meta["crumb"], canon)]),
    ]
    return page(lang, meta["title"], meta["desc"], canon, alt, body, jsonld=jl)


def main():
    inner, js = extract()
    write("desktop-pension-squad/fuse-salvage-calculator/index.html",
          dps_page("en", inner, js))
    inner_ru = replace_all(inner, RU_BODY, "RU body")
    js_ru = replace_all(js, RU_JS, "RU JS")
    write("ru/desktop-pension-squad/fuse-salvage-calculator/index.html",
          dps_page("ru", inner_ru, js_ru))
    print("build_dps done")


if __name__ == "__main__":
    main()

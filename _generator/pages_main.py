# -*- coding: utf-8 -*-
"""Главная, «О клинике», каталог услуг и шаблон страницы услуги."""
from data_misc import CLINIC as C, photo
from data_prices import FAQ, PRICE_BY_KEY
from data_services import SERVICES
from layout import btn, book_btn, crumbs, hl, icon, img, obj, page, section_head, strip_hl
from blocks import (
    C_PHOTOS_CLINIC, cta_final, doctors_section, faq_section, media_banner, offer_section,
    other_services, price_teaser, reviews_section, steps_block, svc_grid,
)

WHY = [
    ("🫶", "Без боли и страха", "Седация, анестезия последнего поколения и врачи, которые умеют разговаривать с теми, кто боится стоматологов. Первый визит — чтобы просто познакомиться и снять тревогу.", "lime", "heart"),
    ("🏥", "Всё в одной клинике", "От профилактики до сложной челюстно-лицевой хирургии. Не нужно ездить по разным адресам — весь путь лечения проходит у одной команды, которая знает вашу историю.", "", "tooth"),
    ("🖥️", "Современное оборудование", "3D-томография, интраоральные сканеры, микроскопная стоматология. Диагностика точная — лечение предсказуемое.", "brand", "sphere"),
    ("🧾", "Прозрачные цены", "Стоимость лечения фиксируется в договоре после диагностики. Никаких «доплат по ходу дела».", "soft", "sparkle"),
    ("🛡️", "Гарантия на работы", "От 1 года на терапию до 10 лет на имплантацию — в зависимости от вида услуг. Все гарантийные обязательства — письменно.", "navy", "implant"),
    ("🕘", "Удобство", "Работаем 7 дней в неделю, есть вечерние часы, экстренный приём при острой боли — в день обращения.", "sky", "brush"),
]

HOME_STEPS = [
    ("📝", "Заявка", "Оставляете заявку на сайте или звоните — подбираем удобное время."),
    ("🔎", "Диагностика", "Осмотр, снимки, составление плана лечения и расчёт стоимости."),
    ("🤝", "Согласование", "Вы получаете план лечения на руки и решаете, что делать дальше."),
    ("🦷", "Лечение", "Работаем по согласованному плану, без сюрпризов в цене."),
    ("🛡️", "Гарантия и поддержка", "На связи после лечения, бесплатные контрольные осмотры."),
]

OBJ_SIZE = {"implant": "--w:92px;--x:10px;--y:-40px;--rot:14deg", "brush": "--w:170px;--x:-30px;--y:-40px;--rot:0deg"}


def home():
    root = ""
    why_cards = "".join(
        f"""<article class="card why-card card--clip{(' card--' + v) if v else ''} reveal">
          <span class="card__emoji" aria-hidden="true">{e}</span>
          <h3>{t}</h3>
          <p>{d}</p>
          <img class="card__obj" src="assets/img/3d/{o}.svg" alt="" aria-hidden="true" width="120" height="120" loading="lazy"{f' style="{OBJ_SIZE[o]}"' if o in OBJ_SIZE else ''}>
        </article>"""
        for e, t, d, v, o in WHY
    )
    chips = "".join(
        f'<span class="chip"><span class="chip__emoji" aria-hidden="true">{e}</span>{t}</span>'
        for e, t in [("⭐", "4,9 из 5 — 1200+ отзывов"), ("🦷", "15 лет на рынке"), ("🩺", "Гарантия на все виды работ"), ("💳", "Рассрочка 0%")]
    )
    body = f"""  <section class="hero" data-parallax>
    <div class="container">
      <div class="hero__media" aria-hidden="true">
        <div class="photo photo--tilt ph-1">{img(photo("hero_woman", 640, 680, faces=True), "", 640, 680, lazy=False)}</div>
        <div class="photo photo--tilt photo--round ph-2">{img(photo("girl_brush", 360, 360, faces=True), "", 360, 360, lazy=False)}</div>
        <div class="photo photo--tilt ph-3">{img(photo("consult", 480, 420), "", 480, 420)}<span class="photo__badge"><span class="pulse-dot pulse-dot--green"></span>Сегодня есть окна</span></div>
        {obj("tooth", "o-1", root)}
        {obj("brush", "o-2", root)}
        {obj("sparkle", "o-3 obj--blur", root)}
        {obj("sphere", "o-4", root)}
        {obj("plus", "o-5 obj--blue", root)}
      </div>
      <div class="hero__content">
        <p class="hero__pre">Стоматология полного цикла в Санкт-Петербурге</p>
        <h1 class="display hero__title">Стоматология, <br>в которую <span class="hl">хочется</span> <br>возвращаться</h1>
        <p class="hero__sub">Лечим, восстанавливаем и создаём красивые улыбки — без боли, очередей и переплат. Все виды стоматологической помощи под одной крышей: от гигиены до сложной имплантации.</p>
        <div class="hero__actions">
          {book_btn("Записаться на бесплатную консультацию", size="lg", service="Консультация — пока не знаю, что нужно", title="Бесплатная консультация", sub="Осмотр, консультация врача и план лечения — бесплатно. Перезвоним и подберём время.")}
          {btn("Посмотреть цены", href="prices.html", variant="ghost", size="lg")}
        </div>
        <div class="chips hero__chips">{chips}</div>
      </div>
    </div>
  </section>

  <section class="section" id="why">
    <div class="container">
      {section_head("Стоматология, которой можно {lime}доверять{/lime}", "Почему выбирают нас")}
      <div class="why-grid">{why_cards}</div>
      <div class="center-cta reveal">{book_btn("Прийти познакомиться", variant="dark", service="Консультация — пока не знаю, что нужно", title="Первый визит — знакомство", sub="Без лечения и давления: познакомитесь с врачом, осмотримся и обсудим, что беспокоит.")}</div>
    </div>
  </section>

  <section class="section section--flush-top" id="services">
    <div class="container">
      {section_head("Чем можем {hl}помочь{/hl}", "Услуги", "Все направления стоматологии в одной клинике — от профилактики до сложной имплантации.")}
      {svc_grid(root)}
      <div class="center-cta reveal">{btn("Все услуги и цены", href="services.html", variant="ghost")}</div>
    </div>
  </section>

  <section class="section section--flush-top" id="steps">
    <div class="container">
      {section_head("Путь пациента — {hl}просто{/hl} и понятно", "Как проходит лечение")}
      {steps_block(HOME_STEPS)}
    </div>
  </section>

{media_banner(root)}

{doctors_section(root)}

{price_teaser(root)}

{reviews_section(root, ["r1", "r4", "r2", "r6", "r3", "r7"])}

{offer_section(root, cls="section section--flush-top")}

{faq_section([(q, a) for _, q, a in FAQ[:7]], root, cls="section section--flush-top")}

{cta_final(root)}"""
    return page(
        "Стоматология «Эмаль» в Санкт-Петербурге — лечение, имплантация, ортодонтия",
        "Стоматология полного цикла: лечение без боли, имплантация, виниры, брекеты, детская стоматология. Бесплатная консультация, рассрочка 0%, гарантия на все работы.",
        body, root, "home",
    )


PRINCIPLES = [
    ("Лечим по показаниям, а не по прайсу", "Не назначаем лишнего: предлагаем только то, что действительно нужно, и объясняем почему."),
    ("План согласовываем заранее", "Каждый план лечения согласовывается заранее и фиксируется в договоре — без сюрпризов в цене."),
    ("Только сертифицированные материалы", "Используем сертифицированные материалы и импланты с международной гарантией производителя."),
    ("Стерильность под контролем", "Соблюдаем протоколы стерилизации — каждый инструмент проходит контроль и вскрывается при вас."),
]

EQUIP = [
    ("🩻", "3D-томограф", "Снимок за 12 секунд с минимальной дозой облучения — видим кость, каналы и нервы."),
    ("📡", "Интраоральные сканеры", "Цифровые оттиски вместо слепочной массы — точно и без дискомфорта."),
    ("🔬", "Дентальные микроскопы", "Лечение каналов и реставрации с увеличением до ×25."),
    ("🧼", "Стерилизация класса B", "Автоклавы медицинского класса и контроль каждого цикла."),
]

STATS = [
    ("15", "", "лет работы", "brand"),
    ("38000", "+", "довольных пациентов", ""),
    ("24", "", "врача в штате", "lime"),
    ("9", "", "кабинетов и 12 стоматологических установок", ""),
    ("6500", "+", "выполненных имплантаций", "navy"),
]

DOCS = [
    ("Лицензия на медицинскую деятельность", "Бессрочная, выдана Комитетом по здравоохранению"),
    ("Выписка из реестра лицензий", "Все направления стоматологии"),
    ("Сертификат партнёра производителя имплантов", "Официальная гарантия на импланты"),
    ("Сертификаты и дипломы врачей", "Более 120 документов о повышении квалификации"),
]


def stats_block():
    cells = []
    for num, suf, label, v in STATS:
        cls = f" card--{v}" if v else ""
        shown = f"{int(num):,}".replace(",", " ") + suf
        cells.append(
            f'<div class="card stat{cls} reveal"><span class="stat__num" data-count="{num}" data-suffix="{suf}">{shown}</span><span class="stat__label">{label}</span></div>'
        )
    return f'<div class="stats">{"".join(cells)}</div>'


def about():
    root = ""
    principles = "".join(f'<div class="principle reveal"><div><h3>{t}</h3><p>{d}</p></div></div>' for t, d in PRINCIPLES)
    layout = ["gallery__item--wide gallery__item--tall", "", "", "", "", "gallery__item--wide", "", ""]
    gallery = "".join(
        f'<a class="gallery__item {layout[i]} reveal" href="{photo(k, 1600, 1067)}" data-lightbox="clinic" data-caption="{cap}">'
        f'{img(photo(k, 800, 640), cap, 800, 640)}<span class="gallery__cap">{cap}</span></a>'
        for i, (k, cap) in enumerate(C_PHOTOS_CLINIC)
    )
    equip = "".join(
        f'<article class="card card--soft reveal"><span class="card__emoji" aria-hidden="true">{e}</span><h3>{t}</h3><p>{d}</p></article>' for e, t, d in EQUIP
    )
    lines = "<i></i>" * 11
    docs = "".join(
        f'<article class="doc-thumb reveal"><div class="doc-thumb__paper" aria-hidden="true"><div class="doc-thumb__lines">{lines}</div><span class="doc-thumb__seal">ЭМАЛЬ</span></div>'
        f'<p class="doc-thumb__title">{t}<small>{d}</small></p></article>'
        for t, d in DOCS
    )
    body = f"""  <section class="phero" data-parallax>
    <div class="container">
      {crumbs([("Главная", "index.html"), ("О клинике", None)], root)}
      <div class="phero__grid">
        <div class="phero__content">
          <h1><span class="phero__kicker">О стоматологии «Эмаль» в Санкт-Петербурге</span>{hl("Стоматология, где лечат {hl}людей{/hl}, а не зубы")}</h1>
          <p class="lead">Мы открылись в {C["founded"]} году с простой идеей: поход к стоматологу не должен быть стрессом. С тех пор через клинику прошло больше 38 000 пациентов — многие приходят семьями и приводят друзей.</p>
          <p class="lead" style="margin-top:14px">Мы собрали команду врачей, которые не просто лечат по стандарту, а объясняют, показывают на снимках, что происходит, и всегда предлагают варианты — от бюджетных до премиальных. Решение всегда остаётся за вами.</p>
          <div class="phero__actions">
            {book_btn("Записаться на консультацию")}
            {btn("Наши врачи", href="doctors.html", variant="ghost")}
          </div>
        </div>
        <div class="phero__visual">
          <div class="collage">
            <div class="photo photo--tilt">{img(photo("office_bright", 720, 792), "Кабинет клиники «Эмаль»", 720, 792, lazy=False)}</div>
            <div class="photo photo--tilt">{img(photo("consult", 440, 440), "Врач консультирует пациентку", 440, 440, lazy=False)}</div>
            {obj("tooth", "cl-o1", root)}
            {obj("sphere", "cl-o2", root)}
            {obj("sparkle", "cl-o3", root)}
            <div class="collage__badge"><span class="collage__badge-emoji">🦷</span><div><strong>15 лет</strong><span>заботимся об улыбках</span></div></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--flush-top">
    <div class="container">
      {section_head("Клиника {hl}в цифрах{/hl}", "Цифры о клинике")}
      {stats_block()}
    </div>
  </section>

  <section class="section section--flush-top">
    <div class="container">
      {section_head("Наши {lime}принципы{/lime}", "Как мы работаем", "Правила, которые не меняются ни для одного пациента.")}
      <div class="principles">{principles}</div>
    </div>
  </section>

  <section class="section section--flush-top" id="gallery">
    <div class="container">
      {section_head("Как у нас {hl}внутри{/hl}", "Клиника", "9 кабинетов, уютная зона ожидания и детская комната. Нажмите на фото, чтобы посмотреть ближе.")}
      <div class="gallery">{gallery}</div>
    </div>
  </section>

  <section class="section section--flush-top">
    <div class="container">
      {section_head("Современное {hl}оборудование{/hl}", "Технологии", "Точная диагностика — предсказуемое лечение.")}
      <div class="equip-grid">{equip}</div>
    </div>
  </section>

  <section class="section section--flush-top" id="docs">
    <div class="container">
      {section_head("Лицензии и {lime}сертификаты{/lime}", "Документы", "Оригиналы документов можно посмотреть на стойке администратора.")}
      <div class="docs-grid">{docs}</div>
    </div>
  </section>

{doctors_section(root, cls="section section--flush-top")}

{reviews_section(root, ["r9", "r10", "r13"], cls="section section--flush-top")}

{cta_final(root)}"""
    return page(
        "О клинике — стоматология «Эмаль», Санкт-Петербург",
        "Стоматология «Эмаль»: 15 лет работы, 24 врача, 9 кабинетов, 3D-томограф и микроскопы. Лечим по показаниям, фиксируем цену в договоре.",
        body, root, "about",
    )


def services_page():
    root = ""
    rows = []
    for i, s in enumerate(SERVICES):
        items = "".join(f"<li>{t}</li>" for _, t, _, _ in s["includes"])
        rows.append(f"""<article class="svc-row reveal" id="{s["slug"]}">
        <div class="svc-row__media">
          {img(photo(s["photo"], 800, 600), s["name"], 800, 600, lazy=i > 1)}
        </div>
        <div class="svc-row__body">
          <p class="eyebrow">{s["emoji"]} Направление</p>
          <h2>{s["name"]}</h2>
          <p>{s["card"]}. {s["intro"].split(". ")[0]}.</p>
          <ul class="dot-list svc-row__list">{items}</ul>
          <div class="svc-row__foot">
            <span class="price-from">{s["price_from"]}</span>
            {btn("Подробнее", href=f"services/{s['slug']}.html", variant="dark", size="sm")}
            {book_btn("Записаться", variant="ghost", size="sm", service=s["name"])}
          </div>
        </div>
      </article>""")
    body = f"""  <section class="phero phero--center" data-parallax>
    {obj("tooth", "pc-o1", root)}
    {obj("implant", "pc-o2", root)}
    {obj("sparkle", "pc-o3", root)}
    {obj("sphere", "pc-o4", root)}
    <div class="container phero__content">
      {crumbs([("Главная", "index.html"), ("Услуги", None)], root)}
      <h1><span class="phero__kicker">Стоматологические услуги в Санкт-Петербурге</span>Весь спектр {hl("{hl}стоматологии{/hl}")} под одной крышей</h1>
      <p class="lead">От профилактики до сложной имплантации — весь путь лечения проходит у одной команды, которая знает вашу историю.</p>
      <div class="phero__actions">
        {book_btn("Бесплатная консультация", service="Консультация — пока не знаю, что нужно")}
        {btn("Цены на услуги", href="prices.html", variant="ghost")}
      </div>
    </div>
  </section>

  <section class="section section--flush-top">
    <div class="container">
      <div class="svc-list">{"".join(rows)}</div>
    </div>
  </section>

{offer_section(root, title="Не знаете, с чего {hl}начать?{/hl}", eyebrow="Бесплатная консультация", cls="section section--flush-top")}

{cta_final(root)}"""
    return page(
        "Услуги стоматологии «Эмаль» — лечение, эстетика, имплантация, ортодонтия",
        "Все стоматологические услуги в одной клинике: терапия, эстетика, гигиена и отбеливание, имплантация, протезирование, ортодонтия, детская стоматология и хирургия.",
        body, root, "services",
    )


def service_page(s):
    root = "../"
    subs = "".join(
        f"""<article class="sub-card reveal">
          <span class="sub-card__emoji" aria-hidden="true">{e}</span>
          <h3>{t}</h3>
          <p>{d}</p>
          <span class="sub-card__price">{p}</span>
        </article>"""
        for e, t, d, p in s["includes"]
    )
    facts = "".join(f'<div class="fact"><strong>{a}</strong><span>{b}</span></div>' for a, b in s["facts"])
    w = s["why"]
    why_list = "".join(f"<li>{x}</li>" for x in w["list"])
    light = w["variant"] != "lime"
    why_objs = "".join(obj(o, "", root) for o in w["objs"])
    group = PRICE_BY_KEY[s["slug"]]
    rows = "".join(
        f'<div class="ptable__row ptable__row--static"><span class="ptable__name">{n}{f"<small>{note}</small>" if note else ""}</span><span class="ptable__price">{pt}</span></div>'
        for n, note, _, pt in group["items"]
    )
    badge_e, badge_t, badge_s = s["badge"]
    body = f"""  <section class="phero" data-parallax>
    <div class="container">
      {crumbs([("Главная", "index.html"), ("Услуги", "services.html"), (s["name"], None)], root)}
      <div class="phero__grid">
        <div class="phero__content">
          <h1><span class="phero__kicker">{s["kicker"]}</span>{hl(s["headline"])}</h1>
          <p class="lead">{s["intro"]}</p>
          <div class="phero__actions">
            {book_btn(s["cta"], service=s["name"])}
            {btn("Узнать цену", href="#prices", variant="ghost")}
          </div>
          <div class="facts">{facts}</div>
        </div>
        <div class="phero__visual">
          <div class="collage">
            <div class="photo photo--tilt">{img(photo(s["photo"], 720, 792), s["name"], 720, 792, lazy=False)}</div>
            <div class="photo photo--tilt">{img(photo(s["photo2"], 440, 440), s["name"], 440, 440, lazy=False)}</div>
            {obj(s["obj"], "cl-o1", root)}
            {obj("sphere", "cl-o2", root)}
            {obj("sparkle", "cl-o3", root)}
            <div class="collage__badge"><span class="collage__badge-emoji">{badge_e}</span><div><strong>{badge_t}</strong><span>{badge_s}</span></div></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--flush-top">
    <div class="container">
      {section_head(("Что {hl}входит{/hl}" if s["includes_title"] == "Что входит" else "Наши {hl}услуги{/hl}"), s["name"])}
      <div class="sub-grid">{subs}</div>
    </div>
  </section>

  <section class="section section--flush-top">
    <div class="container">
      <div class="highlight highlight--{w["variant"]} reveal" data-parallax>
        <div>
          <p class="eyebrow{' eyebrow--light' if light else ''}">{w["label"]}</p>
          <h2 class="h2">{hl(w["title"].replace("{hl}", "{lime}").replace("{/hl}", "{/lime}") if light else w["title"])}</h2>
          <p class="lead">{w["text"]}</p>
          <ul class="check-list highlight__list{' check-list--light' if light else ''}">{why_list}</ul>
          <p class="bubble-note"><span class="bubble-note__emoji">{w["bubble"][0]}</span>{w["bubble"][1]}</p>
        </div>
        <div class="highlight__visual">{why_objs}</div>
      </div>
    </div>
  </section>

  <section class="section section--flush-top">
    <div class="container">
      {section_head("Как проходит {hl}лечение{/hl}", "Этапы")}
      {steps_block(s["steps"])}
    </div>
  </section>

  <section class="section section--flush-top" id="prices">
    <div class="container container--narrow">
      {section_head("Стоимость {lime}услуг{/lime}", "Цены", "Итоговая стоимость фиксируется в договоре после диагностики и не меняется в процессе лечения.")}
      <div class="ptable__group reveal">
        <div class="ptable__head"><span class="svc__emoji" aria-hidden="true">{group["emoji"]}</span><h2>{group["title"]}</h2>{btn("Весь прайс", href=root + "prices.html", variant="ghost", size="sm")}</div>
        {rows}
      </div>
      <div class="info-strip info-strip--light">
        <div class="info-tile reveal"><span class="info-tile__emoji">💳</span><div><strong>Рассрочка 0%</strong><span>до 12 месяцев</span></div></div>
        <div class="info-tile reveal"><span class="info-tile__emoji">🏥</span><div><strong>ДМС</strong><span>согласуем со страховой</span></div></div>
        <div class="info-tile reveal"><span class="info-tile__emoji">📄</span><div><strong>Вычет 13%</strong><span>готовим документы</span></div></div>
      </div>
    </div>
  </section>

{doctors_section(root, s["doctors"], title="Врачи {hl}направления{/hl}", eyebrow=s["name"], more=False, cls="section section--flush-top")}

{reviews_section(root, s["reviews"], title="Отзывы {hl}пациентов{/hl}", cls="section section--flush-top")}

{faq_section(s["faq"], root, title="Частые {hl}вопросы{/hl}", eyebrow=s["name"], cls="section section--flush-top")}

{offer_section(root, fid="svc", title="Запишитесь на {hl}консультацию{/hl}", eyebrow=s["name"], text="Врач осмотрит, ответит на вопросы и составит план лечения с точной стоимостью. Первичная консультация — бесплатно.", submit=s["cta"], select_default=s["name"], cls="section section--flush-top")}

{other_services(root, s["slug"])}"""
    title = f'{strip_hl(s["kicker"])} — стоматология «Эмаль»'
    desc = f'{s["intro"]} Цены {s["price_from"].replace("от ", "от ")}, рассрочка 0%, бесплатная консультация.'
    return page(title, desc, body, root, "services")

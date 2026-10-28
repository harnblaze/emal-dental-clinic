# -*- coding: utf-8 -*-
"""Переиспользуемые секции страниц."""
from html import escape

from data_misc import CLINIC as C, DOCTORS, DOCTOR_BY_ID, REVIEWS, REVIEW_BY_ID, SOURCES, photo
from data_services import SERVICES, SERVICE_BY_SLUG
from layout import btn, book_btn, hl, icon, img, obj, section_head, form_fields, form_success

C_PHOTOS_CLINIC = [
    ("office_bright", "Операционный кабинет"),
    ("lobby", "Зона ожидания"),
    ("room_teal", "Кабинет терапии"),
    ("room_two", "Кабинет гигиены"),
    ("room_monitor", "Кабинет с 3D-планированием"),
    ("chair_white", "Кабинет эстетики"),
    ("consult", "Консультация врача"),
    ("lab", "Зуботехническая лаборатория"),
]


def years(n):
    if n % 10 == 1 and n % 100 != 11:
        return f"{n} год"
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return f"{n} года"
    return f"{n} лет"


def svc_card(s, root, reveal=True, price=False):
    rv = " reveal" if reveal else ""
    pr = f'<span class="svc__price">{s["price_from"]}</span>' if price else ""
    return f"""<article class="svc{rv}">
          <span class="svc__emoji" aria-hidden="true">{s["emoji"]}</span>
          <h3>{s["name"]}</h3>
          <p>{s["card"]}</p>
          {pr}
          <a class="link-dot svc__link" href="{root}services/{s["slug"]}.html" aria-label="Подробнее: {s["name"]}">Подробнее</a>
        </article>"""


def svc_grid(root, price=False):
    return '<div class="svc-grid">' + "".join(svc_card(s, root, price=price) for s in SERVICES) + "</div>"


def doctor_card(d, root, tags_attr=False, reveal=False):
    extra = f' data-tags="{" ".join(d["tags"])}"' if tags_attr else ""
    rv = " reveal" if reveal else ""
    specs = " · ".join(SERVICE_BY_SLUG[t]["short"] for t in d["tags"])
    return f"""<article class="doc-card{rv}"{extra}>
          <div class="doc-card__photo">
            {img(photo(d["photo"], 480, 552, faces=True, crop=d.get("crop", "")), d["patronymic"] + ", " + d["role"].lower(), 480, 552)}
            <div class="doc-card__tags"><span class="tag tag--white">Опыт {years(d["exp"])}</span><span class="tag tag--lime">{d["badge"]}</span></div>
          </div>
          <div class="doc-card__body">
            <h3 class="doc-card__name">{d["name"]}</h3>
            <p class="doc-card__role">{d["role"]}</p>
            <div class="doc-card__meta">
              <span>{icon("cap")}{d["edu"]}</span>
              <span>{icon("case")}{specs}</span>
            </div>
            <div class="doc-card__actions">
              <button class="link-dot" type="button" data-modal="booking" data-title="Запись к врачу" data-sub="{escape(d["patronymic"])} · {escape(d["role"])}" data-service="{escape(SERVICE_BY_SLUG[d["tags"][0]]["name"])}" data-comment="Хочу записаться к врачу: {escape(d["patronymic"])}">Записаться к врачу</button>
            </div>
          </div>
        </article>"""


def carousel_nav(track_id, label):
    return f"""<div class="carousel__nav" data-carousel-nav="{track_id}" role="group" aria-label="{label}">
          <button class="icon-btn" type="button" aria-label="Назад">{icon("arrow-left")}</button>
          <button class="icon-btn" type="button" aria-label="Вперёд">{icon("arrow")}</button>
        </div>"""


def doctors_section(root, ids=None, title="Врачи, которым {hl}доверяют{/hl}", eyebrow="Команда", lead="", more=True, cls="section"):
    docs = [DOCTOR_BY_ID[i] for i in ids] if ids else DOCTORS
    cards = "".join(doctor_card(d, root) for d in docs)
    head = f"""<div class="section-head section-head--row reveal">
        <div>
          <p class="eyebrow">{eyebrow}</p>
          <h2 class="h2">{hl(title)}</h2>
          {f'<p class="lead lead--sub">{lead}</p>' if lead else ""}
        </div>
        {carousel_nav("doctors-track", "Листать врачей") if len(docs) > 3 else ""}
      </div>"""
    if len(docs) < 3:
        team = f"""<article class="card card--brand team-card reveal">
          <span class="card__emoji" aria-hidden="true">👩‍⚕️</span>
          <h3>Не знаете, к кому записаться?</h3>
          <p>Администратор подскажет, какой специалист нужен именно вам. В команде 24 врача с опытом от 7 лет — терапевты, хирурги, ортопеды, ортодонты и детские стоматологи.</p>
          <div class="row mt">
            {book_btn("Подобрать врача", variant="white", size="sm", title="Подберём врача", sub="Расскажите, что беспокоит, — подскажем специалиста и время приёма.")}
            <a class="link-dot link-dot--light" href="{root}doctors.html">Вся команда</a>
          </div>
        </article>"""
        return f"""<section class="{cls}">
    <div class="container">
      {section_head(title, eyebrow, cls="section-head--left")}
      <div class="doctors-mini">{"".join(doctor_card(d, root, reveal=True) for d in docs)}{team}</div>
    </div>
  </section>"""
    per = "" if len(docs) > 3 else " carousel--3"
    more_html = ""
    if more:
        more_html = f"""<div class="team-note reveal">
        <p class="lead">Команда из 24 специалистов с опытом от 7 лет: терапевты, хирурги, ортопеды, ортодонты, детские стоматологи. Регулярно проходят обучение в России и за рубежом, состоят в профессиональных ассоциациях.</p>
        {btn("Познакомиться со всей командой", href=root + "doctors.html", variant="brand")}
      </div>"""
    return f"""<section class="{cls}">
    <div class="container">
      {head}
      <div class="carousel{per}">
        <div class="carousel__track" id="doctors-track">{cards}</div>
      </div>
      {more_html}
    </div>
  </section>"""


def review_card(r, root, tags_attr=False, quote=False, ba=False, reveal=False):
    s = SERVICE_BY_SLUG[r["service"]]
    extra = f' data-tags="{r["service"]}"' if tags_attr else ""
    q = " review--quote" if quote else ""
    rv = " reveal" if reveal else ""
    stars = "".join(icon("star") for _ in range(5))
    ba_html = ""
    if ba and r.get("ba"):
        url = photo(r["ba"], 640, 480)
        ba_html = f"""<div class="ba">
            <img class="ba__before" src="{url}" alt="До процедуры" width="640" height="480" loading="lazy">
            <img class="ba__after" src="{url}" alt="После процедуры" width="640" height="480" loading="lazy">
            <span class="ba__label ba__label--l">До</span><span class="ba__label ba__label--r">После</span>
            <span class="ba__line"></span>
            <input type="range" min="0" max="100" value="50" aria-label="Сравнить фото до и после">
          </div>"""
    return f"""<article class="review{q}{rv}"{extra}>
          <div class="review__head">
            {img(photo(r["avatar"], 120, 120, faces=True), "", 54, 54, cls="review__avatar")}
            <div>
              <p class="review__name">{r["name"]}</p>
              <p class="review__meta">{s["emoji"]} {r["what"]} · {r["date"]}</p>
            </div>
          </div>
          <span class="stars" aria-label="Оценка 5 из 5">{stars}</span>
          {ba_html}
          <p class="review__text">{r["text"]}</p>
          <div class="review__foot">
            <span class="review__source">Отзыв с площадки «{r["source"]}»</span>
            <a class="link-dot" href="{root}services/{s["slug"]}.html">{s["short"]}</a>
          </div>
        </article>"""


def review_sources(root):
    pills = "".join(
        f'<a class="source-pill" href="#" aria-label="Отзывы на {n}"><span class="source-pill__logo" style="background:{c}">{l}</span>{n} <b>★ {r}</b></a>'
        for n, l, c, r in SOURCES
    )
    return f'<div class="review-sources reveal"><span class="muted">Больше живых отзывов — на площадках:</span>{pills}</div>'


def rating_card(root):
    stars = "".join(icon("star") for _ in range(5))
    rows = "".join(
        f'<a class="source-pill" href="#" aria-label="Отзывы на {n}"><span class="source-pill__logo" style="background:{c}">{l}</span>{n} <b>★ {r}</b></a>'
        for n, l, c, r in SOURCES
    )
    return f"""<article class="review review--rating reveal">
          <p class="rating-box__big">4,9</p>
          <span class="stars" aria-label="Средняя оценка 4,9 из 5">{stars}</span>
          <p class="review__text">Средняя оценка клиники по 1200+ отзывам на независимых площадках.</p>
          <div class="review-rating__sources">{rows}</div>
          <div class="review__foot">{btn("Все отзывы", href=root + "reviews.html", variant="dark", size="sm")}</div>
        </article>"""


def reviews_section(root, ids, title="Что говорят {hl}пациенты{/hl}", eyebrow="Отзывы", all_link=True, cls="section"):
    if len(ids) < 3:
        cards = "".join(review_card(REVIEW_BY_ID[i], root, quote=(n == 1), reveal=True) for n, i in enumerate(ids))
        return f"""<section class="{cls}">
    <div class="container">
      {section_head(title, eyebrow, cls="section-head--left")}
      <div class="reviews-mini">{cards}{rating_card(root)}</div>
    </div>
  </section>"""
    cards = "".join(review_card(REVIEW_BY_ID[i], root, quote=(n == 1)) for n, i in enumerate(ids))
    many = len(ids) > 3
    nav = carousel_nav("reviews-track", "Листать отзывы") if many else ""
    link = f'<div class="center-cta reveal">{btn("Все отзывы", href=root + "reviews.html", variant="ghost")}</div>' if all_link else ""
    return f"""<section class="{cls}">
    <div class="container">
      <div class="section-head section-head--row reveal">
        <div><p class="eyebrow">{eyebrow}</p><h2 class="h2">{hl(title)}</h2></div>
        {nav}
      </div>
      <div class="carousel carousel--3">
        <div class="carousel__track" id="reviews-track">{cards}</div>
      </div>
      {review_sources(root)}
      {link}
    </div>
  </section>"""


def acc(q, a, attrs=""):
    return f"""<details class="acc"{attrs}>
          <summary>{q}<span class="acc__icon" aria-hidden="true"></span></summary>
          <div class="acc__body"><p>{a}</p></div>
        </details>"""


def faq_section(items, root, title="Отвечаем на {hl}частые{/hl} вопросы", eyebrow="FAQ", link=True, cls="section"):
    more = f'<div class="center-cta reveal">{btn("Все вопросы и ответы", href=root + "faq.html", variant="ghost")}</div>' if link else ""
    if len(items) <= 4:
        body = f'<div class="faq-list reveal" data-acc-group>{"".join(acc(q, a) for q, a in items)}</div>'
        narrow = " container--narrow"
    else:
        half = (len(items) + 1) // 2
        col1 = "".join(acc(q, a) for q, a in items[:half])
        col2 = "".join(acc(q, a) for q, a in items[half:])
        body = f'<div class="faq-grid reveal" data-acc-group><div class="faq-col">{col1}</div><div class="faq-col">{col2}</div></div>'
        narrow = ""
    return f"""<section class="{cls}">
    <div class="container{narrow}">
      {section_head(title, eyebrow)}
      {body}
      {more}
    </div>
  </section>"""


def offer_section(root, fid="offer", title="Бесплатная консультация и {hl}диагностика{/hl} в подарок",
                  text="Приходите на первичный приём — осмотр, консультация врача и план лечения бесплатно. Разберёмся, что беспокоит, и предложим решение без давления и навязывания услуг.",
                  eyebrow="Для новых пациентов", submit="Записаться бесплатно", select_default=None, cls="section"):
    return f"""<section class="{cls}" id="{fid}-section">
    <div class="container">
      <div class="offer reveal">
        <div class="offer__text">
          <p class="eyebrow">{eyebrow}</p>
          <h2 class="h2">{hl(title)}</h2>
          <p class="lead">{text}</p>
          <ul class="check-list mt">
            <li>Осмотр и консультация врача — 0 ₽</li>
            <li>План лечения с вариантами — от бюджетного до премиального</li>
            <li>Стоимость фиксируем в договоре — без доплат</li>
          </ul>
        </div>
        <div class="offer__visual">
          {obj("tooth", "o-a", root)}
          {obj("sphere", "o-b", root)}
          {obj("sparkle", "o-c", root)}
          <div class="form-card">
            <p class="form-card__title">Запишитесь на первичный приём</p>
            <p class="form-card__sub">Перезвоним, ответим на вопросы и подберём удобное время.</p>
            <form class="form" data-form="{fid}" novalidate>
              {form_fields(fid, root, time=False, comment=False, submit=submit, select_default=select_default)}
              {form_success()}
            </form>
          </div>
        </div>
      </div>
    </div>
  </section>"""


def cta_final(root, title="Улыбка начинается с {hl}одного звонка{/hl}",
              text="Не откладывайте — чем раньше начать лечение, тем оно проще, быстрее и дешевле.",
              button="Записаться на приём", service="", cls="section section--tight"):
    return f"""<section class="{cls}">
    <div class="container">
      <div class="cta-final reveal" data-parallax>
        {obj("tooth", "cf-o1", root)}
        {obj("brush", "cf-o2", root)}
        {obj("sphere", "cf-o3", root)}
        {obj("sparkle", "cf-o4", root)}
        <p class="eyebrow">Запись 7 дней в неделю</p>
        <h2 class="h2">{hl(title)}</h2>
        <p>{text}</p>
        <a class="cta-final__phone" href="{C["phone_href"]}">{C["phone"]}</a>
        <p class="cta-final__meta">{C["hours"]} · {C["address_full"]}</p>
        {book_btn(button, variant="dark", size="lg", service=service)}
      </div>
    </div>
  </section>"""


def steps_block(steps, cls=""):
    n = len(steps)
    mod = " steps--4" if n == 4 else ""
    items = "".join(
        f"""<li class="step reveal">
            <div class="step__top"><span class="step__emoji" aria-hidden="true">{e}</span><span class="step__num" aria-hidden="true"></span></div>
            <h3>{t}</h3>
            <p>{d}</p>
          </li>"""
        for e, t, d in steps
    )
    return f'<div class="steps-wrap {cls}"><ol class="steps{mod}">{items}</ol></div>'


def media_banner(root, title="Загляните к нам {lime}в гости{/lime}", text="Экскурсия по клинике: кабинеты, зона ожидания и детская комната", pic="office_bright"):
    links = "".join(
        f'<a href="{photo(k, 1600, 1067)}" data-lightbox="clinic" data-caption="{cap}" hidden>{cap}</a>' for k, cap in C_PHOTOS_CLINIC
    )
    return f"""<section class="section section--tight">
    <div class="container">
      <div class="media-banner reveal" data-parallax>
        {obj("ring", "mb-o1", root)}
        {obj("brush", "mb-o2", root)}
        {obj("sparkle", "mb-o3", root)}
        <div class="media-banner__inner">
          {img(photo(pic, 1600, 900), "Кабинет стоматологии «Эмаль»", 1600, 900)}
          <div>
            <h2 class="h2">{hl(title)}</h2>
            <p>{text}</p>
            <button class="play-btn" type="button" data-lightbox-open="clinic" aria-label="Смотреть фото клиники">{icon("play")}</button>
          </div>
        </div>
        <div hidden>{links}</div>
      </div>
    </div>
  </section>"""


def price_teaser(root):
    return f"""<section class="price-section" data-parallax>
    {obj("ring", "ps-o1", root)}
    {obj("tooth", "ps-o2", root)}
    <div class="container">
      {section_head("Стоимость {lime}лечения{/lime}", "Цены", "Итоговую стоимость фиксируем в договоре после диагностики — она не меняется в процессе лечения.")}
      <div class="price-cards">
        <article class="price-card price-card--white reveal">
          <div class="price-card__top">
            <div class="price-card__head"><span>Консультация и план лечения</span><span class="tag tag--lime">Бесплатно</span></div>
            <p class="price-card__value">0 <small>₽</small></p>
          </div>
          <ul class="price-card__list"><li>Осмотр и консультация</li><li>План с вариантами лечения</li><li>Расчёт стоимости</li></ul>
          {book_btn("Записаться", size="sm", service="Консультация — пока не знаю, что нужно")}
        </article>
        <article class="price-card reveal">
          <div class="price-card__top">
            <div class="price-card__head"><span>Лечение кариеса</span><span class="tag">Терапия</span></div>
            <p class="price-card__value"><small>от</small> 4 500 <small>₽</small></p>
          </div>
          <ul class="price-card__list"><li>Анестезия включена</li><li>Коффердам — без доплат</li><li>Гарантия до 3 лет</li></ul>
          {btn("Подробнее", href=root + "services/therapy.html", variant="dark", size="sm")}
        </article>
        <article class="price-card price-card--navy reveal">
          <div class="price-card__top">
            <div class="price-card__head"><span>Имплант под ключ</span><span class="tag tag--lime">−15%</span></div>
            <p class="price-card__value"><small>от</small> 39 900 <small>₽</small></p>
          </div>
          <ul class="price-card__list"><li>Имплант + абатмент + коронка</li><li>КТ-план — бесплатно</li><li>Пожизненная гарантия</li></ul>
          {btn("Подробнее", href=root + "services/implants.html", variant="white", size="sm")}
        </article>
        <article class="price-card price-card--white reveal">
          <div class="price-card__top">
            <div class="price-card__head"><span>Полный прайс</span></div>
            <p class="small muted price-card__note">67 позиций по всем направлениям и калькулятор стоимости</p>
          </div>
          <img class="price-card__obj" src="{root}assets/img/3d/smile.svg" alt="" aria-hidden="true" width="150" height="120" loading="lazy">
          {btn("Открыть прайс", href=root + "prices.html", size="sm")}
        </article>
      </div>
      <div class="info-strip">
        <div class="info-tile reveal"><span class="info-tile__emoji">💳</span><div><strong>Рассрочка 0%</strong><span>на срок до 12 месяцев</span></div></div>
        <div class="info-tile reveal"><span class="info-tile__emoji">🏥</span><div><strong>Работаем с ДМС</strong><span>согласуем лечение со страховой</span></div></div>
        <div class="info-tile reveal"><span class="info-tile__emoji">📄</span><div><strong>Налоговый вычет</strong><span>все чеки и документы — сразу</span></div></div>
      </div>
    </div>
  </section>"""


def other_services(root, exclude):
    links = "".join(
        f'<a href="{root}services/{s["slug"]}.html"><span>{s["emoji"]}</span>{s["name"]}</a>' for s in SERVICES if s["slug"] != exclude
    )
    return f"""<section class="section section--tight">
    <div class="container">
      {section_head("Другие {hl}направления{/hl}", "Всё в одной клинике")}
      <div class="other-services reveal">{links}</div>
    </div>
  </section>"""

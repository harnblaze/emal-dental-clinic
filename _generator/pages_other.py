# -*- coding: utf-8 -*-
"""Цены, врачи, отзывы, акции, контакты, FAQ, политика, 404."""
from data_misc import CLINIC as C, DOCTORS, REVIEWS, SOURCES
from data_prices import FAQ, FAQ_CATS, PRICES, PROMOS
from data_services import SERVICES
from layout import btn, book_btn, crumbs, hl, icon, obj, page, section_head, socials, form_fields, form_success, logo
from blocks import acc, cta_final, doctor_card, offer_section, review_card


def center_hero(root, crumb, kicker, title, lead, actions="", objs=("tooth", "implant", "sparkle", "sphere"), extra=""):
    o = "".join(obj(name, f"pc-o{i + 1}", root) for i, name in enumerate(objs))
    return f"""  <section class="phero phero--center" data-parallax>
    {o}
    <div class="container phero__content">
      {crumbs([("Главная", "index.html"), (crumb, None)], root)}
      <h1><span class="phero__kicker">{kicker}</span>{hl(title)}</h1>
      <p class="lead">{lead}</p>
      {f'<div class="phero__actions">{actions}</div>' if actions else ""}
      {extra}
    </div>
  </section>"""


def prices():
    root = ""
    nav = "".join(f'<a href="#cat-{g["key"]}">{g["emoji"]} {g["title"]}</a>' for g in PRICES)
    groups = []
    for g in PRICES:
        rows = "".join(
            f"""<div class="ptable__row"><span class="ptable__name">{n}{f"<small>{note}</small>" if note else ""}</span><span class="ptable__price">{pt}</span>"""
            f"""<button class="add-btn" type="button" data-id="{g["key"]}-{i}" data-name="{n}" data-price="{v}" aria-pressed="false" aria-label="Добавить в расчёт: {n}">{icon("plus")}</button></div>"""
            for i, (n, note, v, pt) in enumerate(g["items"])
        )
        more = btn("Об услуге", href=g["link"], variant="ghost", size="sm") if g["link"] else ""
        groups.append(
            f"""<section class="ptable__group" id="cat-{g["key"]}" aria-labelledby="cat-{g["key"]}-title">
          <div class="ptable__head"><span class="svc__emoji" aria-hidden="true">{g["emoji"]}</span><h2 id="cat-{g["key"]}-title">{g["title"]}</h2>{more}</div>
          {rows}
        </section>"""
        )
    body = f"""{center_hero(root, "Цены", "Цены на стоматологию в Санкт-Петербурге", "Честные цены без {hl}скрытых{/hl} доплат",
        "Итоговая стоимость лечения фиксируется в договоре после диагностики и не меняется в процессе работы. Ниже — ориентировочные цены по основным направлениям.",
        book_btn("Рассчитать стоимость лечения", service="Расчёт стоимости лечения", title="Расчёт стоимости", sub="Расскажите, что беспокоит, — врач предварительно оценит объём и стоимость лечения.") + btn("Как считаем цену", href="#how", variant="ghost"),
        objs=("ring", "tooth", "sparkle", "sphere"))}

  <section class="section section--flush-top" data-prices>
    <div class="container">
      <div class="price-tools">
        <label class="search"><span class="visually-hidden">Поиск по прайсу</span>{icon("search")}<input class="input" type="search" placeholder="Найти услугу: например, «винир»" data-price-search></label>
        <nav class="cat-nav" aria-label="Разделы прайса">{nav}</nav>
      </div>
      <p class="form-note" style="margin:-8px 0 20px 6px">{icon("plus")}Нажимайте «+», чтобы собрать предварительный расчёт — итог появится внизу экрана.</p>
      <div class="ptable">
        {"".join(groups)}
        <p class="ptable__empty" hidden>Ничего не нашли. Попробуйте другое слово или <button class="link-underline" type="button" data-modal="booking">спросите администратора</button>.</p>
      </div>
    </div>
  </section>

  <section class="section section--tight" id="how">
    <div class="container">
      {section_head("Как мы {hl}считаем{/hl} стоимость", "Прозрачно")}
      <div class="grid grid--3">
        <article class="card reveal"><span class="card__emoji">🔎</span><h3>Диагностика</h3><p>Осмотр и снимки показывают реальный объём работы — без этого любая цена будет примерной.</p></article>
        <article class="card card--lime reveal"><span class="card__emoji">📄</span><h3>План и договор</h3><p>Вы получаете план с вариантами лечения. Выбранный вариант и его стоимость фиксируем в договоре.</p></article>
        <article class="card reveal"><span class="card__emoji">🔒</span><h3>Цена не меняется</h3><p>Если в процессе появятся новые обстоятельства, врач сначала обсудит их с вами — без согласия цена не изменится.</p></article>
      </div>
      <div class="info-strip info-strip--light">
        <div class="info-tile reveal"><span class="info-tile__emoji">💳</span><div><strong>Рассрочка 0%</strong><span>на срок до 12 месяцев</span></div></div>
        <div class="info-tile reveal"><span class="info-tile__emoji">🏥</span><div><strong>Работаем с ДМС</strong><span>согласуем лечение со страховой</span></div></div>
        <div class="info-tile reveal"><span class="info-tile__emoji">📄</span><div><strong>Налоговый вычет</strong><span>все чеки и документы</span></div></div>
      </div>
    </div>
  </section>

{cta_final(root, title="Рассчитаем {hl}стоимость{/hl} лечения", text="Первичная консультация бесплатна: врач осмотрит, составит план и назовёт точную цену — её мы закрепим в договоре.", button="Рассчитать стоимость лечения", service="Расчёт стоимости лечения")}

  <div class="calc-bar" aria-live="polite" aria-hidden="true">
    <div class="calc-bar__info">
      <span class="calc-bar__total" data-calc-total>0 ₽</span>
      <span class="calc-bar__meta" data-calc-meta></span>
    </div>
    <button class="calc-bar__clear" type="button" data-calc-clear>Очистить</button>
    <button class="btn btn--sm" type="button" data-calc-send><span>Отправить <span class="btn__label-long">расчёт</span></span><span class="btn__icon">{icon("arrow")}</span></button>
  </div>"""
    return page(
        "Цены на стоматологию — прайс клиники «Эмаль», Санкт-Петербург",
        "Прайс стоматологии «Эмаль»: лечение кариеса от 4 500 ₽, имплант под ключ от 39 900 ₽, гигиена 6 900 ₽. Рассрочка 0%, ДМС, документы для налогового вычета.",
        body, root, "prices",
    )


def doctors():
    root = ""
    filters = '<button class="filter-btn is-active" type="button" data-filter="all" aria-pressed="true">Все врачи</button>' + "".join(
        f'<button class="filter-btn" type="button" data-filter="{s["slug"]}" aria-pressed="false">{s["emoji"]} {s["short"]}</button>' for s in SERVICES
    )
    cards = "".join(doctor_card(d, root, tags_attr=True, reveal=True) for d in DOCTORS)
    body = f"""{center_hero(root, "Врачи", "Врачи стоматологии «Эмаль»", "Команда, которой доверяют {hl}улыбку{/hl}",
        "Каждый врач в клинике проходит внутреннюю аттестацию и регулярное обучение. Мы отвечаем за квалификацию команды так же, как за результат лечения.",
        book_btn("Записаться к врачу", title="Запись к врачу", sub="Подскажем, какой специалист нужен именно вам, и подберём время."),
        objs=("smile", "tooth", "sparkle", "sphere"))}

  <section class="section section--flush-top" data-filter-scope>
    <div class="container">
      <div class="filters" role="group" aria-label="Фильтр по направлению">{filters}</div>
      <div class="doctors-grid">{cards}</div>
      <p class="faq-empty" data-empty>По этому направлению скоро появятся врачи.</p>
    </div>
  </section>

  <section class="section section--flush-top">
    <div class="container">
      {section_head("Как мы {hl}выбираем{/hl} врачей", "Стандарты команды")}
      <div class="grid grid--3">
        <article class="card card--brand reveal"><span class="card__emoji">🎓</span><h3>Внутренняя аттестация</h3><p>Каждый врач проходит собеседование, практическое задание и испытательный срок под наставничеством.</p></article>
        <article class="card reveal"><span class="card__emoji">📚</span><h3>Обучение каждый год</h3><p>Курсы в России и за рубежом, конференции и мастер-классы — клиника оплачивает обучение команде.</p></article>
        <article class="card card--lime reveal"><span class="card__emoji">🧠</span><h3>Консилиумы</h3><p>Сложные случаи разбираем вместе: терапевт, хирург, ортопед и ортодонт составляют общий план.</p></article>
      </div>
    </div>
  </section>

{cta_final(root, title="Подберём врача {hl}под вашу задачу{/hl}", text="Позвоните или оставьте заявку — администратор подскажет, к какому специалисту записаться.", button="Записаться к врачу")}"""
    return page(
        "Врачи стоматологии «Эмаль» — терапевты, хирурги, ортодонты, Санкт-Петербург",
        "Команда стоматологии «Эмаль»: 24 специалиста с опытом от 7 лет. Терапевты, хирурги-имплантологи, ортопеды, ортодонты и детские стоматологи.",
        body, root, "doctors",
    )


def reviews():
    root = ""
    filters = '<button class="filter-btn is-active" type="button" data-filter="all" aria-pressed="true">Все отзывы</button>' + "".join(
        f'<button class="filter-btn" type="button" data-filter="{s["slug"]}" aria-pressed="false">{s["emoji"]} {s["short"]}</button>' for s in SERVICES
    )
    cards = "".join(review_card(r, root, tags_attr=True, quote=(i % 5 == 2), ba=True) for i, r in enumerate(REVIEWS))
    bars = "".join(
        f'<div class="rating-bar"><span>{n}</span><span class="rating-bar__track"><span class="rating-bar__fill" style="--val:{float(r.replace(",", ".")) / 5 * 100:.0f}%"></span></span><b>{r}</b></div>'
        for n, _, _, r in SOURCES
    )
    stars = "".join(icon("star") for _ in range(5))
    box = f"""<div class="rating-box reveal" style="margin-top:40px;text-align:left">
        <div class="text-center"><p class="rating-box__big">4,9</p><span class="stars" aria-label="Средняя оценка 4,9 из 5">{stars}</span><p class="small muted">1 247 отзывов</p></div>
        <div class="rating-bars">{bars}</div>
      </div>"""
    body = f"""{center_hero(root, "Отзывы", "Отзывы о стоматологии «Эмаль»", "{hl}1200+{/hl} пациентов уже рассказали о своём опыте",
        "Собираем отзывы с Яндекс Карт, 2ГИС и ПроДокторов. Фильтруйте по услуге, чтобы найти истории, похожие на вашу.",
        extra=box, objs=("heart", "smile", "sparkle", "sphere"))}

  <section class="section section--flush-top" data-filter-scope data-limit="9">
    <div class="container">
      <div class="filters" role="group" aria-label="Фильтр по услуге">{filters}</div>
      <div class="reviews-masonry">{cards}</div>
      <p class="faq-empty" data-empty>Отзывов по этой услуге пока нет — станьте первым!</p>
      <div class="center-cta"><button class="btn btn--ghost" type="button" data-more><span>Показать ещё</span><span class="btn__icon">{icon("plus")}</span></button></div>
    </div>
  </section>

{cta_final(root, title="Хотите стать следующей {hl}историей успеха?{/hl}", text="Запишитесь на консультацию — первичный приём бесплатный, а план лечения останется у вас.", button="Записаться на консультацию", service="Консультация — пока не знаю, что нужно")}"""
    return page(
        "Отзывы пациентов — стоматология «Эмаль», Санкт-Петербург",
        "Более 1200 отзывов о стоматологии «Эмаль»: средняя оценка 4,9. Истории пациентов об имплантации, лечении, виниров, брекетах и детской стоматологии.",
        body, root, "reviews",
    )


def promo_card(p, root):
    v = f" promo-card--{p['variant']}" if p["variant"] else ""
    wide = " promo-card--wide" if p.get("wide") else ""
    dark = p["variant"] in ("brand", "navy")
    tags = f'<span class="tag{" tag--lime" if dark else " tag--white"}">{p["tag"]}</span>'
    timer = ""
    if p.get("countdown"):
        cells = "".join(
            f'<span class="countdown__cell"><b data-{k}>00</b><small>{lbl}</small></span>'
            for k, lbl in (("d", "дней"), ("h", "часов"), ("m", "минут"), ("s", "секунд"))
        )
        tags += '<span class="tag" data-month-end>до конца месяца</span>'
        timer = f'<div class="countdown" data-countdown role="timer" aria-label="До конца акции">{cells}</div>'
    elif p.get("month_end"):
        tags += '<span class="tag" data-month-end>до конца месяца</span>'
    else:
        tags += f'<span class="tag">{p["always"]}</span>'
    lst = "".join(f"<li>{x}</li>" for x in p["list"])
    old = f'<s>{p["old"]}</s>' if p.get("old") else ""
    button = book_btn("Записаться по акции", variant=("white" if dark else "dark"), service=p["service"], title="Запись по акции", sub=p["title"])
    return f"""<article class="promo-card{v}{wide} reveal">
        <div class="promo-card__top">{tags}</div>
        {timer}
        <h2>{p["title"]}</h2>
        <p class="promo-card__text">{p["text"]}</p>
        <ul class="dot-list">{lst}</ul>
        <div class="promo-card__foot">
          <p class="promo-price">{old}<strong>{p["new"]}</strong></p>
          {button}
        </div>
        {obj(p["obj"], "", root, style=f"--rot:{p['rot']}")}
      </article>"""


def promo():
    root = ""
    cards = "".join(promo_card(p, root) for p in PROMOS)
    body = f"""{center_hero(root, "Акции", "Акции стоматологии «Эмаль»", "Выгодные предложения для вашей {hl}улыбки{/hl}",
        "Скидки действуют при записи через сайт или по телефону. Все акции можно совмещать с рассрочкой 0%.",
        objs=("sparkle", "heart", "tooth", "sphere"))}

  <section class="section section--flush-top">
    <div class="container">
      <div class="promo-grid">{cards}</div>
    </div>
  </section>

  <section class="section section--flush-top">
    <div class="container">
      <div class="highlight highlight--lime reveal" data-parallax>
        <div>
          <p class="eyebrow">Не пропустите</p>
          <h2 class="h2">Узнавайте об акциях {hl("{hl}первыми{/hl}")}</h2>
          <p class="lead">Раз в месяц присылаем подборку предложений и напоминаем о профилактических осмотрах. Без спама — только полезное.</p>
          <div class="phero__actions">
            {btn("Подписаться в Telegram", href="#", variant="dark")}
            {book_btn("Узнать об акциях по телефону", variant="white", title="Расскажем об акциях", sub="Перезвоним и подберём самое выгодное предложение под вашу задачу.")}
          </div>
        </div>
        <div class="highlight__visual">{obj("bubbles", "", root)}{obj("sparkle", "", root)}</div>
      </div>
    </div>
  </section>

{cta_final(root)}"""
    return page(
        "Акции и скидки — стоматология «Эмаль», Санкт-Петербург",
        "Акции стоматологии «Эмаль»: бесплатная консультация имплантолога и скидка 15%, гигиена + отбеливание ZOOM за 24 900 ₽, скидка 10% за друга, бесплатный детский осмотр.",
        body, root, "promo",
    )


def contacts():
    root = ""
    body = f"""{center_hero(root, "Контакты", "Контакты стоматологии «Эмаль» в Санкт-Петербурге", "Мы рядом и всегда {hl}на связи{/hl}",
        "Приходите, звоните или пишите в мессенджеры — ответим на вопросы и подберём удобное время визита.",
        book_btn("Записаться на приём") + f'<a class="btn btn--ghost" href="{C["phone_href"]}"><span>{C["phone"]}</span><span class="btn__icon">{icon("phone")}</span></a>',
        objs=("tooth", "plus", "sparkle", "sphere"))}

  <section class="section section--flush-top">
    <div class="container">
      <div class="contacts-grid">
        <div class="map-card reveal">
          <img src="assets/img/map.svg" alt="Схема проезда: клиника на улице Жемчужной, 5 минут от метро «Петроградская»" width="800" height="560">
          <span class="map-pin" aria-hidden="true">{'<svg viewBox="0 0 64 64"><path fill="#fff" d="M32 13c-3.4-3.4-9-5-13.5-4C12.8 10.2 10.2 15.5 10.8 22c.6 6.5 3.7 11 4.7 17.1 1 6.5 1.6 15.5 7.1 17.5 5 1.8 5.5-6.5 7.1-9.5 1-2 4-2 5 0 1.5 3 2.1 11.3 7.1 9.5 5.5-2 6.1-11 7.1-17.5 1-6.1 4.1-10.6 4.7-17.1.6-6.5-2-11.8-7.7-13-4.5-1-10.1.6-13.5 4Z"/></svg>'}</span>
          <div class="map-card__label">
            <div><strong>{C["address_full"]}</strong><span>{C["metro_note"]}</span></div>
            {btn("Построить маршрут", href="https://yandex.ru/maps/?text=" + C["address_full"].replace(" ", "%20"), variant="dark", size="sm")}
          </div>
        </div>
        <div class="contact-stack">
          <div class="card reveal">
            <h2 class="h3">Связаться с нами</h2>
            <div class="contact-line"><span class="contact-line__icon">{icon("phone")}</span><div><small>Телефон</small><a href="{C["phone_href"]}">{C["phone"]}</a></div></div>
            <div class="contact-line"><span class="contact-line__icon">{icon("telegram")}</span><div><small>Мессенджеры</small><strong>Telegram, WhatsApp, VK</strong></div>{socials()}</div>
            <div class="contact-line"><span class="contact-line__icon">{icon("mail")}</span><div><small>E-mail</small><a href="mailto:{C["email"]}">{C["email"]}</a></div></div>
            <div class="contact-line"><span class="contact-line__icon">{icon("pin")}</span><div><small>Адрес</small><strong>{C["address_full"]}</strong></div></div>
          </div>
          <div class="card reveal">
            <h2 class="h3">Режим работы</h2>
            <p class="small muted">7 дней в неделю, без обеда</p>
            <div class="hours">
              <div><span>Понедельник — пятница</span><b>9:00–21:00</b></div>
              <div><span>Суббота и воскресенье</span><b>9:00–21:00</b></div>
              <div><span>Праздничные дни</span><b>10:00–18:00</b></div>
            </div>
            <p class="open-status" data-open-status><span class="pulse-dot pulse-dot--green"></span><span>Ежедневно с 9:00 до 21:00</span></p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--flush-top" id="urgent">
    <div class="container">
      <div class="urgent reveal">
        {obj("plus", "", root)}
        <p class="tag tag--glass"><span class="pulse-dot"></span> Принимаем сегодня</p>
        <h2 class="h2" style="margin-top:16px">Экстренная помощь при острой боли</h2>
        <p>Болит зуб, отёк или травма? Позвоните — примем в день обращения, даже в выходные. До визита не грейте щёку и не прикладывайте к зубу таблетки.</p>
        <div class="row">
          <a class="btn btn--white" href="{C["phone_href"]}"><span>Позвонить: {C["phone"]}</span><span class="btn__icon">{icon("phone")}</span></a>
          {book_btn("Оставить заявку", variant="dark", service="Острая боль — нужен приём сегодня", title="Экстренная помощь", sub="Оставьте телефон — перезвоним в течение 5 минут и найдём время сегодня.")}
        </div>
      </div>
    </div>
  </section>

  <section class="section section--flush-top">
    <div class="container">
      {section_head("Как {hl}добраться{/hl}", "Дорога")}
      <div class="route">
        <article class="card reveal"><span class="card__emoji">🚇</span><h3>На метро</h3><p>5 минут пешком от станции «Петроградская»: выход к Большому проспекту, затем направо по улице Жемчужной.</p></article>
        <article class="card card--lime reveal"><span class="card__emoji">🚗</span><h3>На машине</h3><p>Городская парковка рядом с клиникой и два бесплатных места во дворе для пациентов — предупредите администратора.</p></article>
        <article class="card reveal"><span class="card__emoji">♿</span><h3>Доступная среда</h3><p>Вход без ступеней, широкие двери и кресло-коляска для пациентов с ограниченной мобильностью.</p></article>
      </div>
    </div>
  </section>

  <section class="section section--flush-top" id="feedback">
    <div class="container">
      <div class="offer reveal">
        <div class="offer__text">
          <p class="eyebrow">Обратная связь</p>
          <h2 class="h2">Остались {hl("{hl}вопросы?{/hl}")}</h2>
          <p class="lead">Оставьте контакты и удобное время — администратор перезвонит, ответит на вопросы и запишет на приём.</p>
          <div class="card mt" style="box-shadow:none">
            <h3 class="h3">Реквизиты</h3>
            <p class="small">{C["legal"]}<br>ИНН {C["inn"]} · ОГРН {C["ogrn"]}<br>{C["license"]}</p>
          </div>
        </div>
        <div class="offer__visual">
          <div class="form-card">
            <p class="form-card__title">Напишите нам</p>
            <p class="form-card__sub">Ответим в течение 15 минут в рабочее время.</p>
            <form class="form" data-form="contacts" novalidate>
              {form_fields("ct", root, service=False, submit="Отправить")}
              {form_success()}
            </form>
          </div>
        </div>
      </div>
    </div>
  </section>"""
    return page(
        "Контакты стоматологии «Эмаль» — адрес, телефон, режим работы",
        "Стоматология «Эмаль»: Санкт-Петербург, ул. Жемчужная, 12, м. Петроградская. Ежедневно 9:00–21:00, экстренный приём при острой боли в день обращения.",
        body, root, "contacts",
    )


def faq():
    root = ""
    filters = '<button class="filter-btn is-active" type="button" data-faq-filter="all" aria-pressed="true">Все вопросы</button>' + "".join(
        f'<button class="filter-btn" type="button" data-faq-filter="{k}" aria-pressed="false">{t}</button>' for k, t in FAQ_CATS
    )
    items = "".join(acc(q, a, f' data-cat="{c}"') for c, q, a in FAQ)
    body = f"""{center_hero(root, "Вопросы и ответы", "FAQ стоматологии «Эмаль»", "Отвечаем на {hl}частые{/hl} вопросы",
        "Собрали ответы на то, что пациенты спрашивают чаще всего. Не нашли свой вопрос — задайте его администратору.",
        objs=("tooth", "sparkle", "sphere", "plus"))}

  <section class="section section--flush-top" data-faq>
    <div class="container">
      <div class="faq-page">
        <aside class="faq-side">
          <label class="search"><span class="visually-hidden">Поиск по вопросам</span>{icon("search")}<input class="input" type="search" placeholder="Поиск по вопросам" data-faq-search></label>
          <div class="filters" role="group" aria-label="Темы вопросов">{filters}</div>
          <div class="card card--brand">
            <h3>Не нашли ответ?</h3>
            <p class="small">Спросите администратора — ответим за 15 минут.</p>
            <div class="mt-s">{book_btn("Задать вопрос", variant="white", size="sm", title="Задать вопрос", sub="Напишите вопрос в комментарии — администратор перезвонит и ответит.")}</div>
          </div>
        </aside>
        <div class="faq-list" data-acc-group>
          {items}
          <p class="faq-empty">Ничего не нашли. Попробуйте переформулировать вопрос или позвоните нам: <a class="link-underline" href="{C["phone_href"]}">{C["phone"]}</a></p>
        </div>
      </div>
    </div>
  </section>

{cta_final(root)}"""
    return page(
        "Вопросы и ответы — стоматология «Эмаль», Санкт-Петербург",
        "Ответы на частые вопросы: больно ли лечить зубы, сколько длится лечение, есть ли рассрочка, работаете ли с ДМС, что делать при острой боли.",
        body, root, "faq",
    )


def privacy():
    root = ""
    body = f"""  <section class="phero">
    <div class="container container--narrow">
      {crumbs([("Главная", "index.html"), ("Политика конфиденциальности", None)], root)}
      <h1 class="h2">Политика обработки персональных данных</h1>
      <p class="lead muted mt-s">Редакция от 1 сентября 2026 года</p>
      <div class="legal prose mt">
        <p>Настоящая политика определяет порядок обработки и защиты персональных данных пользователей сайта стоматологической клиники {C["legal"]} (далее — Клиника) в соответствии с Федеральным законом № 152-ФЗ «О персональных данных».</p>
        <h2>1. Какие данные мы собираем</h2>
        <ul><li>имя и номер телефона, которые вы указываете в формах записи;</li><li>комментарии и сведения о желаемой услуге;</li><li>технические данные: cookie, сведения о браузере и устройстве.</li></ul>
        <h2>2. Для чего мы используем данные</h2>
        <ul><li>для записи на приём и обратной связи;</li><li>для напоминаний о визитах и профилактических осмотрах;</li><li>для улучшения работы сайта.</li></ul>
        <h2>3. Как мы защищаем данные</h2>
        <p>Клиника принимает организационные и технические меры для защиты персональных данных от неправомерного доступа, изменения и распространения. Доступ к данным имеют только сотрудники, которым он необходим для работы.</p>
        <h2 id="cookies">4. Использование cookie</h2>
        <p>Сайт использует cookie, чтобы запоминать ваши настройки и анализировать посещаемость. Вы можете отказаться от необязательных cookie в уведомлении на сайте или отключить их в настройках браузера.</p>
        <h2>5. Ваши права</h2>
        <p>Вы можете запросить сведения об обработке ваших данных, потребовать их уточнения или удаления, а также отозвать согласие, написав на <a class="link-underline" href="mailto:{C["email"]}">{C["email"]}</a>.</p>
              </div>
    </div>
  </section>"""
    return page("Политика конфиденциальности — стоматология «Эмаль»", "Политика обработки персональных данных и использования cookie на сайте стоматологии «Эмаль».", body, root, "")


def not_found():
    root = ""
    body = f"""  <section class="notfound">
    <div class="container">
      <p class="notfound__code" aria-hidden="true">4<img src="assets/img/3d/tooth.svg" alt="" width="190" height="220">4</p>
      <h1 class="h2">Страница выпала, как молочный зуб</h1>
      <p>Возможно, её переименовали или удалили. Зато остальные страницы на месте — и мы тоже.</p>
      <div class="row row--center">
        {btn("На главную", href="index.html")}
        {btn("Все услуги", href="services.html", variant="ghost")}
      </div>
    </div>
  </section>"""
    return page("Страница не найдена — стоматология «Эмаль»", "Такой страницы нет, но остальные на месте.", body, root, "")

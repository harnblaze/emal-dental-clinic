# -*- coding: utf-8 -*-
"""Общая разметка: head, шапка, меню, подвал, модальные окна, мелкие компоненты."""
import re
from html import escape

from data_misc import CLINIC, photo
from data_services import SERVICES

C = CLINIC


def hl(text):
    """{hl}слово{/hl} → выделение; {lime}слово{/lime} → лаймовое выделение."""
    text = re.sub(r"\{(hl|lime|sky)\}(.+?)\{/\1\}([,.:;!?»]+)", r'<span class="nowrap">{\1}\2{/\1}\3</span>', text)
    text = re.sub(r"\{hl\}(.+?)\{/hl\}", r'<span class="hl">\1</span>', text)
    text = re.sub(r"\{lime\}(.+?)\{/lime\}", r'<span class="hl hl--lime">\1</span>', text)
    text = re.sub(r"\{sky\}(.+?)\{/sky\}", r'<span class="hl hl--sky">\1</span>', text)
    return text


def strip_hl(text):
    return re.sub(r"\{/?(hl|lime|sky)\}", "", text)


def icon(name, cls=""):
    extra = f" {cls}" if cls else ""
    return f'<svg class="i{extra}" aria-hidden="true"><use href="#i-{name}"></use></svg>'


def obj(name, cls, root, style=""):
    st = f' style="{style}"' if style else ""
    return f'<img class="obj {cls}" src="{root}assets/img/3d/{name}.svg" alt="" aria-hidden="true" width="200" height="200"{st}>'


def img(url, alt, w, h, cls="", lazy=True, extra=""):
    c = f' class="{cls}"' if cls else ""
    lz = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    return f'<img{c} src="{url}" alt="{escape(alt)}" width="{w}" height="{h}"{lz} decoding="async"{extra}>'


def btn(text, href=None, variant="", size="", modal=None, data=None, plain=False, arrow="arrow", cls=""):
    classes = ["btn"]
    if variant:
        classes.append(f"btn--{variant}")
    if size:
        classes.append(f"btn--{size}")
    if plain:
        classes.append("btn--plain")
    if cls:
        classes.append(cls)
    attrs = ""
    if data:
        attrs += "".join(f' data-{k}="{escape(v)}"' for k, v in data.items())
    inner = f"<span>{text}</span>"
    if not plain:
        inner += f'<span class="btn__icon">{icon(arrow)}</span>'
    if modal:
        return f'<button class="{" ".join(classes)}" type="button" data-modal="{modal}"{attrs}>{inner}</button>'
    return f'<a class="{" ".join(classes)}" href="{href}"{attrs}>{inner}</a>'


def book_btn(text, variant="", size="", service="", title="", sub="", cls=""):
    data = {}
    if service:
        data["service"] = service
    if title:
        data["title"] = title
    if sub:
        data["sub"] = sub
    return btn(text, variant=variant, size=size, modal="booking", data=data, cls=cls)


def section_head(title, eyebrow="", lead="", cls="", tag="h2", reveal=True):
    rv = " reveal" if reveal else ""
    extra = f" {cls}" if cls else ""
    parts = [f'<div class="section-head{extra}{rv}">']
    parts.append("<div>")
    if eyebrow:
        parts.append(f'<p class="eyebrow">{eyebrow}</p>')
    parts.append(f'<{tag} class="h2">{hl(title)}</{tag}>')
    if lead and "section-head--row" not in cls:
        parts.append(f'<p class="lead">{lead}</p>')
    parts.append("</div>")
    if lead and "section-head--row" in cls:
        parts.append(f'<p class="lead">{lead}</p>')
    parts.append("</div>")
    return "".join(parts)


def logo(root, light=False, xl=False):
    cls = "logo" + (" logo--light" if light else "") + (" logo--xl" if xl else "")
    return f"""<a class="{cls}" href="{root}index.html" aria-label="Эмаль — на главную">
      <span class="logo__mark">{tooth_mark()}</span>
      <span class="logo__text"><span class="logo__name">эмаль<b>.</b></span><span class="logo__sub">стоматология</span></span>
    </a>"""


def tooth_mark(color="currentColor"):
    return (
        '<svg viewBox="0 0 64 64" aria-hidden="true">'
        f'<path fill="{color}" d="M32 13c-3.4-3.4-9-5-13.5-4C12.8 10.2 10.2 15.5 10.8 22c.6 6.5 3.7 11 4.7 17.1 1 6.5 1.6 15.5 7.1 17.5 5 1.8 5.5-6.5 7.1-9.5 1-2 4-2 5 0 1.5 3 2.1 11.3 7.1 9.5 5.5-2 6.1-11 7.1-17.5 1-6.1 4.1-10.6 4.7-17.1.6-6.5-2-11.8-7.7-13-4.5-1-10.1.6-13.5 4Z"/>'
        '<ellipse cx="21" cy="19" rx="4.6" ry="2.4" fill="#c8f25c" transform="rotate(-35 21 19)"/>'
        "</svg>"
    )


SPRITE = """<svg xmlns="http://www.w3.org/2000/svg" style="position:absolute;width:0;height:0;overflow:hidden" aria-hidden="true">
  <symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></symbol>
  <symbol id="i-arrow-left" viewBox="0 0 24 24"><path d="M19 12H5M11 6l-6 6 6 6"/></symbol>
  <symbol id="i-chevron" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></symbol>
  <symbol id="i-phone" viewBox="0 0 24 24"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.9 2.1Z"/></symbol>
  <symbol id="i-pin" viewBox="0 0 24 24"><path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="3"/></symbol>
  <symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></symbol>
  <symbol id="i-mail" viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="16" rx="3"/><path d="m22 7-10 6L2 7"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></symbol>
  <symbol id="i-plus" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></symbol>
  <symbol id="i-close" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></symbol>
  <symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></symbol>
  <symbol id="i-calendar" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="3"/><path d="M16 2v4M8 2v4M3 10h18"/></symbol>
  <symbol id="i-cap" viewBox="0 0 24 24"><path d="M22 10 12 5 2 10l10 5 10-5Z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/></symbol>
  <symbol id="i-case" viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="3"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/></symbol>
  <symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/></symbol>
  <symbol id="i-car" viewBox="0 0 24 24"><path d="M5 17h14M6 17v2M18 17v2M3 13l2-6a2 2 0 0 1 2-1h10a2 2 0 0 1 2 1l2 6v4H3v-4Z"/><circle cx="7.5" cy="13.5" r=".5"/><circle cx="16.5" cy="13.5" r=".5"/></symbol>
  <symbol id="i-walk" viewBox="0 0 24 24"><circle cx="13" cy="4" r="2"/><path d="m9 20 3-6 3 3v4M7 12l3-4 4 1 3 3M10 8l-1 5"/></symbol>
  <symbol id="i-star" viewBox="0 0 24 24"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9L12 2.5Z" fill="currentColor" stroke="none"/></symbol>
  <symbol id="i-play" viewBox="0 0 24 24"><path d="M8 5.5v13a1 1 0 0 0 1.5.9l10.2-6.5a1 1 0 0 0 0-1.8L9.5 4.6A1 1 0 0 0 8 5.5Z" fill="currentColor" stroke="none"/></symbol>
  <symbol id="i-telegram" viewBox="0 0 24 24"><path d="M21.4 3.6 2.9 10.7c-1.3.5-1.2 1.2-.2 1.5l4.7 1.5 1.8 5.6c.2.6.1.9.8.9.5 0 .7-.2 1-.5l2.3-2.2 4.7 3.5c.9.5 1.5.2 1.7-.8l3.1-14.6c.3-1.3-.5-1.9-1.4-1.5ZM9.3 13.5l8.8-5.6c.4-.3.8-.1.5.2l-7.3 6.6-.3 3.2-1.7-4.4Z" fill="currentColor" stroke="none"/></symbol>
  <symbol id="i-whatsapp" viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2c0 1.3 1 2.6 1.1 2.8.1.2 1.9 2.9 4.6 4 1.7.7 2.4.8 3.2.7.5-.1 1.5-.6 1.8-1.2.2-.6.2-1.1.1-1.2l-.4-.2Z" fill="currentColor" stroke="none"/></symbol>
  <symbol id="i-vk" viewBox="0 0 24 24"><path d="M12.8 17.6C6.9 17.6 3.5 13.5 3.4 6.8h3c.1 4.9 2.3 7 4 7.4V6.8h2.8V11c1.7-.2 3.5-2.1 4.1-4.2h2.8a8.3 8.3 0 0 1-3.8 5.4 8.6 8.6 0 0 1 4.4 5.4h-3.1a5.4 5.4 0 0 0-4.4-3.9v3.9h-.4Z" fill="currentColor" stroke="none"/></symbol>
  <symbol id="i-alert" viewBox="0 0 24 24"><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/><path d="M12 9v4M12 17h.01"/></symbol>
  <symbol id="i-doc" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6Z"/><path d="M14 2v6h6M8 13h8M8 17h5"/></symbol>
</svg>"""


NAV = [
    ("services", "Услуги", "services.html"),
    ("prices", "Цены", "prices.html"),
    ("doctors", "Врачи", "doctors.html"),
    ("reviews", "Отзывы", "reviews.html"),
    ("promo", "Акции", "promo.html"),
    ("about", "О клинике", "about.html"),
    ("contacts", "Контакты", "contacts.html"),
]


def head(title, desc, root, canonical):
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <meta name="theme-color" content="#eef4f7">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:site_name" content="Стоматология «Эмаль»">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:image" content="{photo('office_bright', 1200, 630)}">
  <link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preconnect" href="https://images.unsplash.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Raleway:wght@500;600;700&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{root}assets/css/style.css">
  <script>document.documentElement.classList.add("js")</script>
  <script src="{root}assets/js/main.js" defer></script>
</head>"""


def topbar(root):
    return f"""<div class="topbar">
    <div class="container topbar__inner">
      <div class="topbar__info">
        <span class="topbar__item">{icon("pin")}{C["address"]} · {C["metro"]}</span>
        <span class="topbar__item">{icon("clock")}{C["hours"]}</span>
      </div>
      <div class="topbar__info">
        <a class="topbar__urgent" href="{root}contacts.html#urgent"><span class="pulse-dot"></span>Острая боль? Примем сегодня</a>
        {socials()}
      </div>
    </div>
  </div>"""


def socials(size=""):
    cls = f"social social--{size}" if size else "social"
    return (
        '<div class="socials">'
        f'<a class="{cls}" href="#" aria-label="Telegram">{icon("telegram")}</a>'
        f'<a class="{cls}" href="#" aria-label="WhatsApp">{icon("whatsapp")}</a>'
        f'<a class="{cls}" href="#" aria-label="ВКонтакте">{icon("vk")}</a>'
        "</div>"
    )


def mega(root):
    links = "".join(
        f'<a class="mega__link" href="{root}services/{s["slug"]}.html"><span class="mega__emoji">{s["emoji"]}</span>'
        f'<span><span class="mega__title">{s["name"]}</span><span class="mega__desc">{s["menu"]}</span></span></a>'
        for s in SERVICES
    )
    return f"""<div class="mega" id="mega-services">
            <div class="mega__grid">{links}</div>
            <div class="mega__foot"><span>Не знаете, с чего начать? Первичная консультация — бесплатно</span>{btn("Все услуги", href=root + "services.html", variant="dark", size="sm")}</div>
          </div>"""


def header(root, current):
    items = []
    for key, label, href in NAV:
        cur = ' is-current" aria-current="page' if key == current else ""
        if key == "services":
            items.append(
                f'<li class="nav__item nav__item--mega"><a class="nav__link{cur}" href="{root}{href}" aria-expanded="false" aria-controls="mega-services">{label}{icon("chevron")}</a>{mega(root)}</li>'
            )
        else:
            items.append(f'<li class="nav__item"><a class="nav__link{cur}" href="{root}{href}">{label}</a></li>')
    return f"""{topbar(root)}
  <header class="header">
    <div class="container header__inner">
      {logo(root)}
      <nav class="nav" aria-label="Основное меню">
        <ul class="nav__list">{"".join(items)}</ul>
        <a class="nav__phone" href="{C["phone_href"]}" aria-label="Позвонить {C["phone"]}">{icon("phone")}<span>{C["phone"]}</span></a>
      </nav>
      <div class="header__actions">
        {book_btn("Записаться", size="sm")}
        <a class="icon-btn icon-btn--light header__call" href="{C["phone_href"]}" aria-label="Позвонить в клинику">{icon("phone")}</a>
        <button class="burger" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Открыть меню">
          <span class="burger__label">Меню</span>
          <span class="burger__circle"><span class="burger__eyes"><span></span><span></span></span></span>
        </button>
      </div>
    </div>
  </header>
  {mobile_nav(root, current)}"""


def mobile_nav(root, current):
    subs = "".join(f'<a href="{root}services/{s["slug"]}.html"><span>{s["emoji"]}</span>{s["short"]}</a>' for s in SERVICES)
    rows = []
    for key, label, href in NAV + [("faq", "Вопросы и ответы", "faq.html")]:
        cur = " is-current" if key == current else ""
        if key == "services":
            rows.append(
                f'<li><button class="mnav__link{cur}" type="button" data-mnav-toggle aria-expanded="false" aria-controls="mnav-services">{label}{icon("chevron")}</button>'
                f'<div class="mnav__sub" id="mnav-services" hidden>{subs}<a href="{root}services.html"><span>📋</span>Все услуги</a></div></li>'
            )
        else:
            rows.append(f'<li><a class="mnav__link{cur}" href="{root}{href}">{label}{icon("arrow")}</a></li>')
    return f"""<div class="mnav" id="mnav">
    <nav aria-label="Мобильное меню"><ul class="mnav__list">{"".join(rows)}</ul></nav>
    <div class="mnav__foot">
      <a class="mnav__phone" href="{C["phone_href"]}">{C["phone"]}</a>
      <span class="muted small">{C["address_full"]} · {C["hours"]}</span>
      {book_btn("Записаться на приём", cls="btn--block")}
      {socials("lg")}
    </div>
  </div>"""


def footer(root):
    services = "".join(f'<li><a href="{root}services/{s["slug"]}.html">{s["name"]}</a></li>' for s in SERVICES)
    return f"""<footer class="footer">
    <svg class="footer__wave" viewBox="0 0 1440 70" preserveAspectRatio="none" aria-hidden="true"><path fill="currentColor" d="M0 0h1440v26c-120 22-240 34-360 30S840 26 720 26 480 52 360 56 120 48 0 26Z"/></svg>
    {obj("smile", "ft-o1", root)}
    <div class="container">
      <div class="footer__head">
        {logo(root, light=True, xl=True)}
        <div class="footer__about">
          <p>Стоматология полного цикла для всей семьи: от профилактики до имплантации. Лечим без боли и переплат с {C["founded"]} года.</p>
          {socials("lg")}
        </div>
      </div>
      <div class="footer__top">
        <div>
          <p class="footer__title">Услуги</p>
          <ul class="footer__list">{services}</ul>
        </div>
        <div>
          <p class="footer__title">Пациентам</p>
          <ul class="footer__list">
            <li><a href="{root}prices.html">Цены</a></li>
            <li><a href="{root}promo.html">Акции</a></li>
            <li><a href="{root}doctors.html">Врачи</a></li>
            <li><a href="{root}reviews.html">Отзывы</a></li>
            <li><a href="{root}faq.html">Вопросы и ответы</a></li>
            <li><a href="{root}about.html">О клинике</a></li>
            <li><a href="{root}about.html#docs">Лицензии</a></li>
          </ul>
        </div>
        <div>
          <p class="footer__title">Контакты</p>
          <div class="footer__contact">
            <a class="footer__phone" href="{C["phone_href"]}">{C["phone"]}</a>
            <a href="mailto:{C["email"]}">{C["email"]}</a>
            <span>{C["address_full"]}<br>{C["metro"]}</span>
          </div>
        </div>
        <div>
          <p class="footer__title">Приём</p>
          <div class="footer__contact">
            <span>{C["hours"]}<br>без выходных</span>
            <span>Экстренный приём при острой боли — в день обращения</span>
            {btn("Записаться", variant="white", size="sm", modal="booking")}
          </div>
        </div>
      </div>
      <p class="footer__warning">Имеются противопоказания. Необходима консультация специалиста</p>
      <div class="footer__bottom">
        <div class="footer__legal">
          <span>© {C["founded"]}–<span data-year>2026</span> {C["legal"]}. ИНН {C["inn"]}, ОГРН {C["ogrn"]}</span>
          <span>{C["license"]}</span>
        </div>
        <div class="footer__docs">
          <a href="{root}privacy.html">Политика конфиденциальности</a>
          <a href="{root}privacy.html#cookies">Использование cookie</a>
          <span>Фото: Unsplash</span>
        </div>
      </div>
    </div>
  </footer>"""


SERVICE_OPTIONS = ["Консультация — пока не знаю, что нужно"] + [s["name"] for s in SERVICES] + ["Острая боль — нужен приём сегодня"]


def form_fields(fid, root, service=True, time=True, comment=True, submit="Записаться", select_default=None):
    opts = "".join(
        f'<option{" selected" if o == select_default else ""}>{o}</option>' for o in SERVICE_OPTIONS
    )
    parts = [f"""<div class="form__row">
          <div class="field"><label class="field__label" for="{fid}-name">Имя</label><input class="input" id="{fid}-name" name="name" type="text" autocomplete="given-name" placeholder="Ваше имя" required><span class="field__error">Напишите, как к вам обращаться</span></div>
          <div class="field"><label class="field__label" for="{fid}-phone">Телефон</label><input class="input" id="{fid}-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="+7 (___) ___-__-__" required><span class="field__error">Проверьте номер телефона</span></div>
        </div>"""]
    if service:
        parts.append(f'<div class="field"><label class="field__label" for="{fid}-service">Услуга</label><select class="input" id="{fid}-service" name="service">{opts}</select></div>')
    if time:
        parts.append(f"""<fieldset class="field fieldset"><legend class="field__label">Удобное время для визита</legend>
          <div class="segmented">
            <label><input type="radio" name="time" value="Утро" checked><span>Утро</span></label>
            <label><input type="radio" name="time" value="День"><span>День</span></label>
            <label><input type="radio" name="time" value="Вечер"><span>Вечер</span></label>
            <label><input type="radio" name="time" value="Выходные"><span>Выходные</span></label>
          </div></fieldset>""")
    if comment:
        parts.append(f'<div class="field"><label class="field__label" for="{fid}-comment">Комментарий</label><textarea class="input" id="{fid}-comment" name="comment" rows="3" placeholder="Что беспокоит? Можно оставить пустым"></textarea></div>')
    parts.append(f"""<label class="check"><input type="checkbox" name="consent" required checked><span>Соглашаюсь с <a href="{root}privacy.html">политикой обработки персональных данных</a></span></label>
        <button class="btn btn--dark btn--block" type="submit"><span>{submit}</span><span class="btn__icon">{icon("arrow")}</span></button>
        <p class="form-note">{icon("shield")}Перезвоним в течение 15 минут в рабочее время</p>""")
    return "".join(parts)


def form_success(close=False):
    action = (
        '<button class="btn btn--ghost btn--sm btn--plain" type="button" data-modal-close>Хорошо</button>'
        if close
        else '<button class="btn btn--ghost btn--sm btn--plain" type="button" data-form-reset>Отправить ещё одну заявку</button>'
    )
    return f"""<div class="form__success" role="status">
          <span class="form__success-emoji">🦷</span>
          <h3 data-success-name>Спасибо!</h3>
          <p>Заявка принята. Администратор перезвонит в течение 15 минут в рабочее время клиники и подберёт удобное время.</p>
          <p>Это демонстрационный сайт — заявка никуда не отправлена.</p>
          {action}
        </div>"""


def modals(root):
    return f"""<div class="modal" id="booking" role="dialog" aria-modal="true" aria-labelledby="booking-title" aria-hidden="true">
    <div class="modal__dialog">
      <button class="modal__close" type="button" data-modal-close aria-label="Закрыть">{icon("close")}</button>
      <div class="modal__head">
        {obj("tooth", "", root)}
        <h2 id="booking-title" data-booking-title data-default="Запись на приём">Запись на приём</h2>
        <p data-booking-sub data-default="Оставьте телефон — администратор перезвонит и подберёт удобное время.">Оставьте телефон — администратор перезвонит и подберёт удобное время.</p>
      </div>
      <div class="modal__body">
        <form class="form" data-form="booking" novalidate>
          {form_fields("bk", root)}
          {form_success(close=True)}
        </form>
      </div>
    </div>
  </div>
  <div class="modal modal--media" id="lightbox" role="dialog" aria-modal="true" aria-label="Просмотр фотографий" aria-hidden="true">
    <div class="modal__dialog">
      <button class="modal__close" type="button" data-modal-close aria-label="Закрыть">{icon("close")}</button>
      <figure class="lightbox__figure">
        <img class="lightbox__img" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="" width="1200" height="800">
        <figcaption class="lightbox__bar">
          <span><span class="lightbox__caption"></span> <span class="lightbox__counter muted"></span></span>
          <span class="row">
            <button class="icon-btn icon-btn--light" type="button" data-lb-prev aria-label="Предыдущее фото">{icon("arrow-left")}</button>
            <button class="icon-btn icon-btn--lime" type="button" data-lb-next aria-label="Следующее фото">{icon("arrow")}</button>
          </span>
        </figcaption>
      </figure>
    </div>
  </div>
  <div class="cookie" role="region" aria-label="Уведомление о cookie">
    <p><strong>Cookie — единственное печенье, которое не вредит зубам 🍪</strong><br>Мы используем cookie, чтобы сайт работал быстрее и удобнее. Подробнее — в <a class="link-underline" href="{root}privacy.html#cookies">политике</a>.</p>
    <div class="cookie__actions">
      <button class="btn btn--sm btn--plain" type="button" data-cookie="all">Принять</button>
      <button class="btn btn--ghost btn--sm btn--plain" type="button" data-cookie="necessary">Только необходимые</button>
    </div>
  </div>
  <div class="mobile-bar">
    {book_btn("Записаться", size="sm")}
    <a class="icon-btn" href="{C["phone_href"]}" aria-label="Позвонить в клинику">{icon("phone")}</a>
  </div>"""


def page(title, desc, body, root="", current="", canonical=""):
    return f"""{head(title, desc, root, canonical)}
<body>
  {SPRITE}
  <a class="skip-link" href="#main">Перейти к содержимому</a>
  {header(root, current)}
  <main id="main">
{body}
  </main>
  {footer(root)}
  {modals(root)}
</body>
</html>
"""


def crumbs(items, root):
    lis = []
    for label, href in items:
        if href:
            lis.append(f'<li><a href="{root}{href}">{label}</a></li>')
        else:
            lis.append(f'<li><span aria-current="page">{label}</span></li>')
    return f'<nav aria-label="Хлебные крошки"><ol class="crumbs">{"".join(lis)}</ol></nav>'

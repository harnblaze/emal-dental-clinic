# -*- coding: utf-8 -*-
"""Собирает статический сайт в корень проекта и проверяет HTML, ссылки и ID.

Запуск из любой папки:  python3 _generator/build.py
Внимание: страницы перезаписываются целиком — правки, сделанные прямо в HTML,
перенесите в файлы генератора, иначе они потеряются при следующей сборке.
"""
import os
import re
import sys
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(__file__))

from data_services import SERVICES  # noqa: E402
import pages_main as pm  # noqa: E402
import pages_other as po  # noqa: E402

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = {
    "index.html": pm.home,
    "about.html": pm.about,
    "services.html": pm.services_page,
    "prices.html": po.prices,
    "doctors.html": po.doctors,
    "reviews.html": po.reviews,
    "promo.html": po.promo,
    "contacts.html": po.contacts,
    "faq.html": po.faq,
    "privacy.html": po.privacy,
    "404.html": po.not_found,
}


class Checker(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr", "use", "path", "circle", "ellipse", "rect"}

    def __init__(self):
        super().__init__()
        self.stack = []
        self.ids = {}
        self.links = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids[a["id"]] = self.ids.get(a["id"], 0) + 1
        for key in ("href", "src"):
            if key in a and a[key]:
                self.links.append(a[key])
        if tag not in self.VOID:
            self.stack.append((tag, self.getpos()))

    def handle_startendtag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids[a["id"]] = self.ids.get(a["id"], 0) + 1

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if not self.stack:
            self.errors.append(f"extra </{tag}> at {self.getpos()}")
            return
        top, pos = self.stack.pop()
        if top != tag:
            self.errors.append(f"mismatch <{top}> {pos} closed by </{tag}> at {self.getpos()}")


NBSP = "\u00a0"


def typograph(html):
    """Неразрывные пробелы в числах и ценах — только в текстовых узлах."""
    parts = re.split(r"(<script.*?</script>|<style.*?</style>|<[^>]+>)", html, flags=re.S)
    for i, part in enumerate(parts):
        if not part or part.startswith("<"):
            continue
        part = re.sub(r"(\d) (\d{3})(?!\d)", r"\1" + NBSP + r"\2", part)
        part = re.sub(r"(\d) (₽|%|лет|года|год|мин|месяц)", r"\1" + NBSP + r"\2", part)
        part = re.sub(r"(^|[\s(«])(от|до|с|на|в|и|к|у|о) ", lambda m: m.group(1) + m.group(2) + NBSP, part)
        part = re.sub(r" (—|–) ", NBSP + r"\1 ", part)
        parts[i] = part
    # Пояснение в успешном состоянии форм должно остаться дословным (обычные пробелы)
    return "".join(parts).replace("сайт" + NBSP + "— заявка", "сайт — заявка")


def write(path, html):
    with open(path, "w", encoding="utf-8") as f:
        f.write(typograph(html))


def main():
    written = []
    for name, fn in PAGES.items():
        path = os.path.join(OUT, name)
        write(path, fn())
        written.append(path)
    os.makedirs(os.path.join(OUT, "services"), exist_ok=True)
    for s in SERVICES:
        path = os.path.join(OUT, "services", f"{s['slug']}.html")
        write(path, pm.service_page(s))
        written.append(path)

    problems = 0
    for path in written:
        html = open(path, encoding="utf-8").read()
        c = Checker()
        c.feed(html)
        rel = os.path.relpath(path, OUT)
        for err in c.errors[:5]:
            print(f"[html] {rel}: {err}")
            problems += 1
        if c.stack:
            print(f"[html] {rel}: unclosed {c.stack[-3:]}")
            problems += 1
        dups = [k for k, v in c.ids.items() if v > 1]
        if dups:
            print(f"[id] {rel}: duplicate ids {dups}")
            problems += 1
        base = os.path.dirname(path)
        for link in c.links:
            if re.match(r"^(https?:|mailto:|tel:|data:|#$)", link):
                continue
            target, _, frag = link.partition("#")
            if target == "":
                if frag and frag not in c.ids and not frag.startswith("i-"):
                    print(f"[anchor] {rel}: #{frag} not found")
                    problems += 1
                continue
            full = os.path.normpath(os.path.join(base, target))
            if not os.path.exists(full):
                print(f"[link] {rel}: {link} -> missing")
                problems += 1
    print(f"built {len(written)} pages, problems: {problems}")


if __name__ == "__main__":
    main()

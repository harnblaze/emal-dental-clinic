/* Эмаль — интерактив сайта. Без зависимостей. */
(function () {
  "use strict";

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const storage = {
    get(key) {
      try {
        return window.localStorage.getItem(key);
      } catch (e) {
        return null;
      }
    },
    set(key, value) {
      try {
        window.localStorage.setItem(key, value);
      } catch (e) {
        /* хранилище недоступно — просто не запоминаем */
      }
    },
  };

  const formatRub = (n) => new Intl.NumberFormat("ru-RU").format(Math.round(n)) + " ₽";

  const plural = (n, forms) => {
    const n10 = n % 10;
    const n100 = n % 100;
    if (n10 === 1 && n100 !== 11) return forms[0];
    if (n10 >= 2 && n10 <= 4 && (n100 < 12 || n100 > 14)) return forms[1];
    return forms[2];
  };

  /* Битые фото: прячем иконку, остаётся фон-градиент контейнера */
  function initImages() {
    $$("img").forEach((img) => {
      const hide = () => img.classList.add("is-broken");
      if (img.complete && img.naturalWidth === 0 && img.getAttribute("src")) hide();
      img.addEventListener("error", hide, { once: true });
    });
    const style = document.createElement("style");
    style.textContent = "img.is-broken{opacity:0}";
    document.head.appendChild(style);
  }

  /* Шапка ---------------------------------------------------------------- */
  function initHeader() {
    const header = $(".header");
    if (!header) return;
    const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });

    $$(".nav__item--mega").forEach((item) => {
      const trigger = $(".nav__link", item);
      let timer;
      const open = () => {
        clearTimeout(timer);
        item.classList.add("is-open");
        trigger.setAttribute("aria-expanded", "true");
      };
      const close = () => {
        item.classList.remove("is-open");
        trigger.setAttribute("aria-expanded", "false");
      };
      const hoverable = window.matchMedia("(hover: hover)");
      item.addEventListener("mouseenter", () => hoverable.matches && open());
      item.addEventListener("mouseleave", () => {
        if (hoverable.matches) timer = setTimeout(close, 180);
      });
      trigger.addEventListener("click", (e) => {
        e.preventDefault();
        item.classList.contains("is-open") ? close() : open();
      });
      item.addEventListener("focusout", (e) => {
        if (!item.contains(e.relatedTarget)) close();
      });
      document.addEventListener("click", (e) => {
        if (!item.contains(e.target)) close();
      });
      document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && item.classList.contains("is-open")) {
          close();
          trigger.focus();
        }
      });
    });
  }

  /* Мобильное меню -------------------------------------------------------- */
  function initMobileNav() {
    const burger = $(".burger");
    const panel = $(".mnav");
    if (!burger || !panel) return;

    const setOpen = (state) => {
      burger.setAttribute("aria-expanded", String(state));
      burger.setAttribute("aria-label", state ? "Закрыть меню" : "Открыть меню");
      panel.classList.toggle("is-open", state);
      panel.toggleAttribute("inert", !state);
      document.body.classList.toggle("is-locked", state);
    };
    panel.setAttribute("inert", "");

    burger.addEventListener("click", () => setOpen(burger.getAttribute("aria-expanded") !== "true"));
    panel.addEventListener("click", (e) => {
      if (e.target.closest("a")) setOpen(false);
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && panel.classList.contains("is-open")) {
        setOpen(false);
        burger.focus();
      }
    });
    window.matchMedia("(min-width: 1181px)").addEventListener("change", (e) => {
      if (e.matches) setOpen(false);
    });

    $$("[data-mnav-toggle]", panel).forEach((btn) => {
      const sub = document.getElementById(btn.getAttribute("aria-controls"));
      btn.addEventListener("click", () => {
        const expanded = btn.getAttribute("aria-expanded") === "true";
        btn.setAttribute("aria-expanded", String(!expanded));
        sub.hidden = expanded;
      });
    });
  }

  /* Модальные окна ---------------------------------------------------------- */
  const modals = (() => {
    let active = null;
    let lastFocus = null;

    const focusables = (root) =>
      $$('a[href], button:not([disabled]), input:not([disabled]):not([type="hidden"]), select, textarea, [tabindex]:not([tabindex="-1"])', root).filter(
        (el) => el.offsetParent !== null
      );

    function open(id, data = {}) {
      const modal = document.getElementById(id);
      if (!modal) return;
      if (active) close();
      lastFocus = document.activeElement;
      active = modal;
      modal.classList.add("is-open");
      modal.removeAttribute("inert");
      modal.setAttribute("aria-hidden", "false");
      document.body.classList.add("is-locked");
      modal.dispatchEvent(new CustomEvent("modal:open", { detail: data }));
      const first = focusables(modal).find((el) => !el.classList.contains("modal__close")) || focusables(modal)[0];
      setTimeout(() => first && first.focus({ preventScroll: true }), 60);
    }

    function close() {
      if (!active) return;
      const modal = active;
      active = null;
      modal.classList.remove("is-open");
      modal.setAttribute("aria-hidden", "true");
      modal.setAttribute("inert", "");
      document.body.classList.remove("is-locked");
      modal.dispatchEvent(new CustomEvent("modal:close"));
      if (lastFocus) lastFocus.focus({ preventScroll: true });
    }

    function init() {
      $$(".modal").forEach((m) => m.setAttribute("inert", ""));
      document.addEventListener("click", (e) => {
        const opener = e.target.closest("[data-modal]");
        if (opener) {
          e.preventDefault();
          open(opener.getAttribute("data-modal"), { ...opener.dataset });
          return;
        }
        if (active && (e.target === active || e.target.closest("[data-modal-close]"))) close();
      });
      document.addEventListener("keydown", (e) => {
        if (!active) return;
        if (e.key === "Escape") close();
        if (e.key === "Tab") {
          const items = focusables(active);
          if (!items.length) return;
          const first = items[0];
          const last = items[items.length - 1];
          if (e.shiftKey && document.activeElement === first) {
            e.preventDefault();
            last.focus();
          } else if (!e.shiftKey && document.activeElement === last) {
            e.preventDefault();
            first.focus();
          }
        }
      });

      const booking = document.getElementById("booking");
      if (booking) {
        booking.addEventListener("modal:open", (e) => {
          const d = e.detail || {};
          const form = $("form", booking);
          if (form.classList.contains("is-sent")) resetForm(form);
          const title = $("[data-booking-title]", booking);
          const sub = $("[data-booking-sub]", booking);
          title.textContent = d.title || title.dataset.default;
          sub.textContent = d.sub || sub.dataset.default;
          const service = $('select[name="service"]', booking);
          if (service) {
            const wanted = d.service || "";
            const match = Array.from(service.options).find((o) => o.value === wanted || o.text === wanted);
            if (match) service.value = match.value;
            else if (wanted) {
              const opt = new Option(wanted, wanted, true, true);
              opt.dataset.extra = "1";
              service.add(opt, 1);
            } else service.selectedIndex = 0;
          }
          const comment = $('textarea[name="comment"]', booking);
          if (comment) comment.value = d.comment || "";
        });
      }
    }

    return { open, close, init };
  })();

  /* Формы -------------------------------------------------------------------- */
  function maskPhone(input) {
    const format = (value) => {
      if (value === "+") return value;
      let digits;
      if (value.includes("+7")) {
        digits = value.replace("+7", "").replace(/\D/g, "");
      } else {
        digits = value.replace(/\D/g, "");
        if (/^[78]$/.test(digits)) return "+7 (";
      }
      // вставили номер целиком: 8 921… или +7 921…
      if (digits.length > 10 && /^[78]/.test(digits)) digits = digits.slice(1);
      digits = digits.slice(0, 10);
      if (!digits) return value.includes("+7") ? "+7 (" : "";
      let out = "+7 (" + digits.slice(0, 3);
      if (digits.length >= 3) out += ")";
      if (digits.length > 3) out += " " + digits.slice(3, 6);
      if (digits.length > 6) out += "-" + digits.slice(6, 8);
      if (digits.length > 8) out += "-" + digits.slice(8, 10);
      return out;
    };
    const caretToEnd = () => {
      const len = input.value.length;
      try {
        input.setSelectionRange(len, len);
      } catch (e) {
        /* тип поля не поддерживает выделение */
      }
    };
    input.addEventListener("input", (e) => {
      let value = format(input.value);
      if (e.inputType && e.inputType.startsWith("delete")) value = value.replace(/\D+$/, "");
      input.value = value;
    });
    input.addEventListener("focus", () => {
      if (!input.value) input.value = "+7 (";
      requestAnimationFrame(caretToEnd);
    });
    input.addEventListener("click", () => {
      if (input.selectionStart !== null && input.selectionStart < 4) caretToEnd();
    });
    input.addEventListener("blur", () => {
      if (input.value.replace(/\D/g, "").length <= 1) input.value = "";
    });
  }

  function validateField(field) {
    const input = $("input, select, textarea", field);
    if (!input) return true;
    let ok = true;
    if (input.type === "tel") ok = input.value.replace(/\D/g, "").length === 11;
    else if (input.required) ok = input.value.trim().length > 1;
    field.classList.toggle("is-invalid", !ok);
    return ok;
  }

  function resetForm(form) {
    form.classList.remove("is-sent");
    form.reset();
    $$(".is-invalid", form).forEach((el) => el.classList.remove("is-invalid"));
    $$('option[data-extra="1"]', form).forEach((o) => o.remove());
  }

  function initForms() {
    $$('input[type="tel"]').forEach(maskPhone);
    $$("form[data-form]").forEach((form) => {
      const fields = $$(".field", form);
      fields.forEach((field) => {
        const input = $("input, select, textarea", field);
        if (input) input.addEventListener("input", () => field.classList.contains("is-invalid") && validateField(field));
      });
      form.addEventListener("submit", (e) => {
        e.preventDefault();
        let ok = fields.map(validateField).every(Boolean);
        const consent = $(".check input[required]", form);
        if (consent) {
          const label = consent.closest(".check");
          label.classList.toggle("is-invalid", !consent.checked);
          if (!consent.checked) ok = false;
        }
        if (!ok) {
          const bad = $(".is-invalid input, .is-invalid select, .is-invalid textarea, .check.is-invalid input", form);
          if (bad) bad.focus();
          return;
        }
        const btn = $('button[type="submit"]', form);
        btn.setAttribute("disabled", "");
        const nameInput = $('input[name="name"]', form);
        const name = nameInput ? nameInput.value.trim().split(" ")[0] : "";
        setTimeout(() => {
          btn.removeAttribute("disabled");
          const title = $("[data-success-name]", form);
          if (title) title.textContent = name ? `${name}, спасибо!` : "Спасибо!";
          form.classList.add("is-sent");
          if (form.dataset.form === "calc") document.dispatchEvent(new CustomEvent("calc:sent"));
        }, 700);
      });
      $$("[data-form-reset]", form).forEach((b) => b.addEventListener("click", () => resetForm(form)));
    });
  }

  /* Появление при прокрутке и счётчики ----------------------------------------- */
  function initReveal() {
    const items = $$(".reveal");
    const groups = new Map();
    items.forEach((el) => {
      const parent = el.parentElement;
      const index = groups.get(parent) || 0;
      groups.set(parent, index + 1);
      if (!el.style.getPropertyValue("--d")) el.style.setProperty("--d", Math.min(index * 0.08, 0.4) + "s");
    });
    if (reduceMotion || !("IntersectionObserver" in window)) {
      items.forEach((el) => el.classList.add("is-in"));
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            io.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );
    items.forEach((el) => io.observe(el));
  }

  function initCounters() {
    const items = $$("[data-count]");
    if (!items.length) return;
    const run = (el) => {
      const target = parseFloat(el.dataset.count);
      const suffix = el.dataset.suffix || "";
      const fmt = (v) => new Intl.NumberFormat("ru-RU").format(Math.round(v)) + suffix;
      if (reduceMotion) {
        el.textContent = fmt(target);
        return;
      }
      const start = performance.now();
      const dur = 1600;
      const tick = (now) => {
        const p = Math.min((now - start) / dur, 1);
        el.textContent = fmt(target * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    };
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            run(entry.target);
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.4 }
    );
    items.forEach((el) => io.observe(el));
  }

  /* Карусели ---------------------------------------------------------------- */
  function initCarousels() {
    $$("[data-carousel-nav]").forEach((nav) => {
      const track = document.getElementById(nav.dataset.carouselNav);
      if (!track) return;
      const [prev, next] = $$("button", nav);
      const step = () => {
        const card = track.firstElementChild;
        const gap = parseFloat(getComputedStyle(track).columnGap) || 0;
        return card ? card.getBoundingClientRect().width + gap : track.clientWidth;
      };
      const update = () => {
        const max = track.scrollWidth - track.clientWidth - 2;
        prev.disabled = track.scrollLeft <= 2;
        next.disabled = track.scrollLeft >= max;
      };
      prev.addEventListener("click", () => track.scrollBy({ left: -step(), behavior: reduceMotion ? "auto" : "smooth" }));
      next.addEventListener("click", () => track.scrollBy({ left: step(), behavior: reduceMotion ? "auto" : "smooth" }));
      track.addEventListener("scroll", update, { passive: true });
      window.addEventListener("resize", update);
      update();
    });
  }

  /* Фильтры карточек и «показать ещё» ------------------------------------------ */
  function initFilters() {
    $$("[data-filter-scope]").forEach((scope) => {
      const buttons = $$("[data-filter]", scope);
      const items = $$("[data-tags]", scope);
      const more = $("[data-more]", scope);
      const empty = $("[data-empty]", scope);
      const pageSize = parseInt(scope.dataset.limit || "0", 10);
      let limit = pageSize || Infinity;
      let current = "all";

      const apply = () => {
        let shown = 0;
        let matched = 0;
        items.forEach((item) => {
          const tags = item.dataset.tags.split(" ");
          const ok = current === "all" || tags.includes(current);
          if (ok) matched++;
          const visible = ok && shown < limit;
          item.hidden = !visible;
          if (visible) {
            shown++;
            item.classList.add("is-in");
          }
        });
        if (more) more.hidden = shown >= matched;
        if (empty) empty.classList.toggle("is-visible", matched === 0);
      };

      buttons.forEach((btn) =>
        btn.addEventListener("click", () => {
          current = btn.dataset.filter;
          limit = pageSize || Infinity;
          buttons.forEach((b) => {
            b.classList.toggle("is-active", b === btn);
            b.setAttribute("aria-pressed", String(b === btn));
          });
          apply();
        })
      );
      if (more) {
        more.addEventListener("click", () => {
          limit += pageSize;
          apply();
        });
      }
      apply();
    });

    $$("[data-acc-group]").forEach((group) => {
      const list = $$("details", group);
      list.forEach((d) =>
        d.addEventListener("toggle", () => {
          if (d.open) list.forEach((other) => other !== d && (other.open = false));
        })
      );
    });
  }

  function initFaqSearch() {
    const input = $("[data-faq-search]");
    if (!input) return;
    const scope = input.closest("[data-faq]");
    const items = $$(".acc", scope);
    const empty = $(".faq-empty", scope);
    const buttons = $$("[data-faq-filter]", scope);
    let cat = "all";
    const apply = () => {
      const q = input.value.trim().toLowerCase();
      let count = 0;
      items.forEach((item) => {
        const okCat = cat === "all" || item.dataset.cat === cat;
        const okText = !q || item.textContent.toLowerCase().includes(q);
        item.hidden = !(okCat && okText);
        if (!item.hidden) count++;
        if (q && !item.hidden && q.length > 2) item.open = true;
      });
      empty.classList.toggle("is-visible", count === 0);
    };
    input.addEventListener("input", apply);
    buttons.forEach((btn) =>
      btn.addEventListener("click", () => {
        cat = btn.dataset.faqFilter;
        buttons.forEach((b) => {
          b.classList.toggle("is-active", b === btn);
          b.setAttribute("aria-pressed", String(b === btn));
        });
        apply();
      })
    );
  }

  /* Цены: поиск, навигация по разделам, калькулятор ---------------------------- */
  function initPrices() {
    const root = $("[data-prices]");
    if (!root) return;
    const groups = $$(".ptable__group", root);
    const search = $("[data-price-search]", root);
    const empty = $(".ptable__empty", root);
    const nav = $(".cat-nav", root);
    const links = nav ? $$("a", nav) : [];

    if (search) {
      search.addEventListener("input", () => {
        const q = search.value.trim().toLowerCase();
        let total = 0;
        groups.forEach((g) => {
          let count = 0;
          $$(".ptable__row", g).forEach((row) => {
            const ok = !q || row.textContent.toLowerCase().includes(q);
            row.hidden = !ok;
            if (ok) count++;
          });
          g.hidden = count === 0;
          total += count;
        });
        empty.hidden = total !== 0;
      });
    }

    if (links.length && "IntersectionObserver" in window) {
      const setActive = (id) => {
        links.forEach((a) => {
          const on = a.getAttribute("href") === "#" + id;
          a.classList.toggle("is-active", on);
          if (on) nav.scrollTo({ left: a.offsetLeft - nav.clientWidth / 2 + a.clientWidth / 2, behavior: "smooth" });
        });
      };
      const io = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => entry.isIntersecting && setActive(entry.target.id));
        },
        { rootMargin: "-35% 0px -60% 0px" }
      );
      groups.forEach((g) => io.observe(g));
      window.addEventListener(
        "scroll",
        () => {
          if (groups[0].getBoundingClientRect().top > window.innerHeight * 0.4) {
            links.forEach((a) => a.classList.remove("is-active"));
            if (nav.scrollLeft) nav.scrollTo({ left: 0 });
          }
        },
        { passive: true }
      );
    }

    const bar = $(".calc-bar");
    if (!bar) return;
    const picked = new Map();
    const totalEl = $("[data-calc-total]", bar);
    const metaEl = $("[data-calc-meta]", bar);
    const render = () => {
      const sum = Array.from(picked.values()).reduce((a, b) => a + b.price, 0);
      const n = picked.size;
      totalEl.textContent = "от " + formatRub(sum);
      metaEl.textContent = `${n} ${plural(n, ["услуга", "услуги", "услуг"])} · в рассрочку от ${formatRub(sum / 12)}/мес`;
      bar.classList.toggle("is-visible", n > 0);
      bar.setAttribute("aria-hidden", String(n === 0));
      $$(".add-btn", root).forEach((btn) => {
        const on = picked.has(btn.dataset.id);
        btn.classList.toggle("is-added", on);
        btn.setAttribute("aria-pressed", String(on));
      });
    };
    root.addEventListener("click", (e) => {
      const btn = e.target.closest(".add-btn");
      if (!btn) return;
      const id = btn.dataset.id;
      if (picked.has(id)) picked.delete(id);
      else picked.set(id, { name: btn.dataset.name, price: parseFloat(btn.dataset.price) });
      render();
    });
    $("[data-calc-clear]", bar).addEventListener("click", () => {
      picked.clear();
      render();
    });
    $("[data-calc-send]", bar).addEventListener("click", () => {
      const lines = Array.from(picked.values()).map((p) => `• ${p.name} — от ${formatRub(p.price)}`);
      modals.open("booking", {
        title: "Отправить расчёт",
        sub: "Администратор проверит список, уточнит детали и перезвонит в течение 15 минут.",
        service: "Расчёт стоимости лечения",
        comment: "Хочу рассчитать стоимость:\n" + lines.join("\n"),
      });
    });
    render();
  }

  /* До/после ----------------------------------------------------------------- */
  function initBeforeAfter() {
    $$(".ba").forEach((ba) => {
      const range = $("input", ba);
      const set = () => ba.style.setProperty("--pos", range.value + "%");
      range.addEventListener("input", set);
      set();
    });
  }

  /* Галерея -------------------------------------------------------------------- */
  function initLightbox() {
    const box = document.getElementById("lightbox");
    if (!box) return;
    const img = $(".lightbox__img", box);
    const caption = $(".lightbox__caption", box);
    const counter = $(".lightbox__counter", box);
    let list = [];
    let index = 0;

    const show = (i) => {
      index = (i + list.length) % list.length;
      const item = list[index];
      img.src = item.getAttribute("href");
      img.alt = item.dataset.caption || "";
      caption.textContent = item.dataset.caption || "";
      counter.textContent = `${index + 1} / ${list.length}`;
    };

    document.addEventListener("click", (e) => {
      const link = e.target.closest("[data-lightbox]");
      const starter = e.target.closest("[data-lightbox-open]");
      if (!link && !starter) return;
      e.preventDefault();
      const group = link ? link.dataset.lightbox : starter.dataset.lightboxOpen;
      list = $$(`[data-lightbox="${group}"]`);
      if (!list.length) return;
      modals.open("lightbox");
      show(link ? list.indexOf(link) : 0);
    });
    $("[data-lb-prev]", box).addEventListener("click", () => show(index - 1));
    $("[data-lb-next]", box).addEventListener("click", () => show(index + 1));
    document.addEventListener("keydown", (e) => {
      if (!box.classList.contains("is-open")) return;
      if (e.key === "ArrowLeft") show(index - 1);
      if (e.key === "ArrowRight") show(index + 1);
    });
  }

  /* Таймер акций: до конца текущего месяца --------------------------------------- */
  function initCountdown() {
    const now = new Date();
    const monthEnd = new Date(now.getFullYear(), now.getMonth() + 1, 0, 23, 59, 59);
    const dateText = monthEnd.toLocaleDateString("ru-RU", { day: "numeric", month: "long" });
    $$("[data-month-end]").forEach((el) => (el.textContent = "до " + dateText));

    const timers = $$("[data-countdown]");
    if (!timers.length) return;
    const pad = (n) => String(n).padStart(2, "0");
    const tick = () => {
      let diff = Math.max(0, monthEnd - new Date());
      const d = Math.floor(diff / 864e5);
      diff -= d * 864e5;
      const h = Math.floor(diff / 36e5);
      diff -= h * 36e5;
      const m = Math.floor(diff / 6e4);
      const s = Math.floor((diff - m * 6e4) / 1000);
      timers.forEach((t) => {
        t.querySelector("[data-d]").textContent = pad(d);
        t.querySelector("[data-h]").textContent = pad(h);
        t.querySelector("[data-m]").textContent = pad(m);
        t.querySelector("[data-s]").textContent = pad(s);
      });
    };
    tick();
    setInterval(tick, 1000);
  }

  /* Статус «открыто сейчас» по времени Санкт-Петербурга ------------------------ */
  function initOpenStatus() {
    const items = $$("[data-open-status]");
    if (!items.length) return;
    const now = new Date();
    const spbHour = (now.getUTCHours() + 3) % 24 + now.getUTCMinutes() / 60;
    const open = spbHour >= 9 && spbHour < 21;
    items.forEach((el) => {
      el.classList.toggle("is-closed", !open);
      $("span:last-child", el).textContent = open ? "Сейчас открыто · до 21:00" : "Сейчас закрыто · откроемся в 9:00";
    });
  }

  /* Cookie ------------------------------------------------------------------- */
  function initCookie() {
    const box = $(".cookie");
    if (!box || storage.get("emal-cookie")) return;
    setTimeout(() => box.classList.add("is-visible"), 1500);
    $$("[data-cookie]", box).forEach((btn) =>
      btn.addEventListener("click", () => {
        storage.set("emal-cookie", btn.dataset.cookie);
        box.classList.remove("is-visible");
      })
    );
  }

  /* Нижняя панель на телефонах ------------------------------------------------ */
  function initMobileBar() {
    const bar = $(".mobile-bar");
    if (!bar) return;
    let footerVisible = false;
    const update = () => bar.classList.toggle("is-visible", window.scrollY > 520 && !footerVisible);
    const footer = $(".footer");
    if (footer && "IntersectionObserver" in window) {
      new IntersectionObserver((entries) => {
        footerVisible = entries[0].isIntersecting;
        update();
      }).observe(footer);
    }
    window.addEventListener("scroll", update, { passive: true });
    update();
  }

  /* Лёгкий параллакс 3D-объектов за курсором ------------------------------------- */
  function initParallax() {
    if (reduceMotion || !window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
    $$("[data-parallax]").forEach((scene) => {
      const objs = $$(".obj", scene);
      let raf = 0;
      scene.addEventListener("pointermove", (e) => {
        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(() => {
          const r = scene.getBoundingClientRect();
          const x = (e.clientX - r.left) / r.width - 0.5;
          const y = (e.clientY - r.top) / r.height - 0.5;
          objs.forEach((o, i) => {
            const depth = 14 + (i % 3) * 10;
            o.style.setProperty("--px", (x * depth).toFixed(1) + "px");
            o.style.setProperty("--py", (y * depth).toFixed(1) + "px");
          });
        });
      });
      scene.addEventListener("pointerleave", () => {
        objs.forEach((o) => {
          o.style.setProperty("--px", "0px");
          o.style.setProperty("--py", "0px");
        });
      });
    });
  }

  function initMisc() {
    $$("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
  }

  document.addEventListener("DOMContentLoaded", () => {
    initImages();
    initHeader();
    initMobileNav();
    modals.init();
    initForms();
    initReveal();
    initCounters();
    initCarousels();
    initFilters();
    initFaqSearch();
    initPrices();
    initBeforeAfter();
    initLightbox();
    initCountdown();
    initOpenStatus();
    initCookie();
    initMobileBar();
    initParallax();
    initMisc();
  });
})();

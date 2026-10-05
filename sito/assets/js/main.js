/* Baruch · comportamenti del sito */

/* ===== Da completare con i dati reali =====
   Finché l'email è vuota, il modulo contatti apre WhatsApp al numero indicato nel piè di pagina.
   I link dei social sono in sorgenti/build.py (SOCIAL_LINK). */
const CONFIG = {
  email: "",                 // es. "ciao@baruch.it": se presente, il modulo apre la mail
  whatsapp: "393404742250",  // numero in formato internazionale, senza + e spazi
};

document.documentElement.classList.add("js");

/* ---------- Menu mobile ---------- */
const menu = document.getElementById("mobile-menu");
const openBtn = document.querySelector("[data-menu-open]");
const closeBtn = document.querySelector("[data-menu-close]");
function setMenu(open) {
  if (!menu) return;
  menu.classList.toggle("is-open", open);
  menu.toggleAttribute("inert", !open);
  openBtn?.setAttribute("aria-expanded", String(open));
  document.body.style.overflow = open ? "hidden" : "";
  (open ? closeBtn : openBtn)?.focus();
}
if (menu) {
  menu.setAttribute("inert", "");
  openBtn?.addEventListener("click", () => setMenu(true));
  closeBtn?.addEventListener("click", () => setMenu(false));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && menu.classList.contains("is-open")) setMenu(false);
  });
}

/* ---------- Comparsa allo scorrimento ---------- */
const reveals = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window) {
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) {
          en.target.classList.add("is-in");
          io.unobserve(en.target);
        }
      });
    },
    { rootMargin: "0px 0px -8% 0px", threshold: 0.12 }
  );
  reveals.forEach((el) => io.observe(el));
} else {
  reveals.forEach((el) => el.classList.add("is-in"));
}

/* ---------- Lightbox (galleria e diario) ---------- */
const box = document.getElementById("lightbox");
if (box) {
  const img = box.querySelector("img");
  const cap = box.querySelector(".lightbox__caption");
  const prev = box.querySelector(".lightbox__prev");
  const next = box.querySelector(".lightbox__next");
  const items = [...document.querySelectorAll("[data-full]")];
  let index = 0;
  let opener = null;

  const show = (i) => {
    index = (i + items.length) % items.length;
    const it = items[index];
    const thumb = it.querySelector("img");
    img.src = it.dataset.full;
    img.alt = thumb ? thumb.alt : "";
    cap.innerHTML = "";
    if (it.dataset.title) cap.append(it.dataset.title);
    if (it.dataset.note) {
      const s = document.createElement("small");
      s.textContent = it.dataset.note;
      cap.append(s);
    }
  };

  items.forEach((it, i) =>
    it.addEventListener("click", () => {
      opener = it;
      show(i);
      box.showModal();
    })
  );
  const single = items.length < 2 || box.dataset.single !== undefined;
  prev.hidden = next.hidden = single;
  prev.addEventListener("click", () => show(index - 1));
  next.addEventListener("click", () => show(index + 1));
  box.querySelector("[data-close]").addEventListener("click", () => box.close());
  box.addEventListener("click", (e) => {
    if (e.target === box || e.target.classList.contains("lightbox__stage")) box.close();
  });
  box.addEventListener("keydown", (e) => {
    if (single) return;
    if (e.key === "ArrowLeft") show(index - 1);
    if (e.key === "ArrowRight") show(index + 1);
  });
  box.addEventListener("close", () => {
    img.removeAttribute("src");
    opener?.focus();
  });

  /* scorrimento col dito */
  let x0 = null;
  box.addEventListener("touchstart", (e) => (x0 = e.touches[0].clientX), { passive: true });
  box.addEventListener("touchend", (e) => {
    if (x0 === null || single) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 50) show(index + (dx < 0 ? 1 : -1));
    x0 = null;
  });
}

/* ---------- Modulo contatti ---------- */
const form = document.getElementById("contact-form");
if (form) {
  const note = form.querySelector(".form__note");
  const status = form.querySelector(".form__status");
  note.textContent = CONFIG.email
    ? "Premendo il pulsante si apre il tuo programma di posta con il messaggio già scritto."
    : "Premendo il pulsante il messaggio si apre su WhatsApp, pronto da inviare.";

  const rules = {
    nome: (v) => (v.trim().length >= 2 ? "" : "Scrivi il tuo nome."),
    email: (v) => (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()) ? "" : "Controlla l'indirizzo email."),
    messaggio: (v) => (v.trim().length >= 10 ? "" : "Il messaggio è un po' corto: raccontami qualcosa in più."),
  };
  const check = (field) => {
    const msg = rules[field.name]?.(field.value) ?? "";
    field.setAttribute("aria-invalid", msg ? "true" : "false");
    document.getElementById(field.name + "-error").textContent = msg;
    return !msg;
  };
  form.querySelectorAll("input, textarea").forEach((f) =>
    f.addEventListener("blur", () => f.value && check(f))
  );

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const fields = [...form.querySelectorAll("input, textarea")];
    const ok = fields.map(check).every(Boolean);
    if (!ok) {
      fields.find((f) => f.getAttribute("aria-invalid") === "true")?.focus();
      status.textContent = "";
      return;
    }
    const d = Object.fromEntries(new FormData(form));
    const body = `${d.messaggio}\n\n${d.nome}\n${d.email}`;
    const url = CONFIG.email
      ? `mailto:${CONFIG.email}?subject=${encodeURIComponent("Messaggio dal sito Baruch")}&body=${encodeURIComponent(body)}`
      : `https://wa.me/${CONFIG.whatsapp}?text=${encodeURIComponent(body)}`;
    window.open(url, CONFIG.email ? "_self" : "_blank", "noopener");
    status.textContent = "Grazie! Ti rispondo appena posso.";
    form.reset();
  });
}

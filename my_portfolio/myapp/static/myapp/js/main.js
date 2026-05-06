// =====================
// INIT
// =====================
document.addEventListener("DOMContentLoaded", () => {
  lucide.createIcons();

  initScroll();
  initReveal();
  initHoverEffect();
  initRoleSwitch();
  initTerminal();
  initCopyEmail();
  initModal();
  initDropdown();
  initContactForm();
  initMobileMenu();
});

// =====================
// SCROLL + NAV
// =====================
function initScroll() {
  const scrollProgress = document.querySelector("#scroll-progress");
  const navLinks = [...document.querySelectorAll(".nav-link")];

  const sections = navLinks
    .map((link) => {
      const href = link.getAttribute("href");
      if (href && href.startsWith("#") && !href.includes("/")) {
        return document.querySelector(href);
      }
      return null;
    })
    .filter(Boolean);

  function updateScrollState() {
    // Progress bar works on pages that include it.
    if (scrollProgress) {
      const total = document.documentElement.scrollHeight - window.innerHeight;

      scrollProgress.style.width =
        total > 0 ? (window.scrollY / total) * 100 + "%" : "0%";
    }

    // Nav active state only applies to same-page anchors.
    const activeSection = sections
      .slice()
      .reverse()
      .find((sec) => sec.offsetTop <= window.scrollY + 150);

    navLinks.forEach((link) => {
      const href = link.getAttribute("href");

      if (href && href.startsWith("#") && !href.includes("/")) {
        link.classList.toggle(
          "is-active",
          activeSection && href === `#${activeSection.id}`,
        );
      } else {
        link.classList.remove("is-active");
      }
    });
  }

  window.addEventListener("scroll", updateScrollState, { passive: true });
  window.addEventListener("resize", updateScrollState);
  updateScrollState();
}
// =====================
// REVEAL ANIMATION
// =====================
function initReveal() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add("is-visible");
      });
    },
    { threshold: 0.1 },
  );

  document.querySelectorAll(".reveal").forEach((el) => observer.observe(el));
}

// =====================
// CARD HOVER EFFECT
// =====================
function initHoverEffect() {
  document.querySelectorAll(".surface-hover").forEach((card) => {
    card.addEventListener("pointermove", (e) => {
      const rect = card.getBoundingClientRect();
      card.style.setProperty("--x", `${e.clientX - rect.left}px`);
      card.style.setProperty("--y", `${e.clientY - rect.top}px`);
    });
  });
}

// =====================
// ROLE SWITCH
// =====================
function initRoleSwitch() {
  const roleWords = [...document.querySelectorAll(".role-word")];
  if (!roleWords.length) return;

  let index = 0;

  setInterval(() => {
    roleWords[index].classList.remove("is-visible");
    index = (index + 1) % roleWords.length;
    roleWords[index].classList.add("is-visible");
  }, 2500);
}

// =====================
// TERMINAL EFFECT
// =====================
async function initTerminal() {
  const commands = [...document.querySelectorAll(".cmd")];
  const outputs = [...document.querySelectorAll("[data-output]")];
  if (!commands.length) return;

  const wait = (ms) => new Promise((r) => setTimeout(r, ms));

  for (let i = 0; i < commands.length; i++) {
    const text = commands[i].dataset.text;

    for (let j = 0; j <= text.length; j++) {
      commands[i].textContent = text.slice(0, j);
      await wait(30);
    }

    if (outputs[i]) {
      outputs[i].textContent = outputs[i].dataset.output;
    }
  }
}

// =====================
// COPY EMAIL
// =====================
function initCopyEmail() {
  const btn = document.querySelector("#copy-email");
  if (!btn) return;

  btn.addEventListener("click", async () => {
    const label = btn.querySelector("span");
    const original = label.textContent;

    try {
      await navigator.clipboard.writeText(btn.dataset.email);
      label.textContent = "Copied!";
    } catch {
      label.textContent = "Error";
    }

    setTimeout(() => (label.textContent = original), 1500);
  });
}

// =====================
// MODAL
// =====================
function initModal() {
  const modal = document.getElementById("contact-modal");
  const box = document.getElementById("modal-box");
  const open = document.getElementById("open-contact");
  const close = document.getElementById("close-contact");

  if (!modal || !box) return;

  function openModal() {
    modal.classList.remove("opacity-0", "pointer-events-none");

    requestAnimationFrame(() => {
      box.classList.remove("scale-90", "opacity-0");
      box.classList.add("scale-100", "opacity-100");
    });

    document.body.style.overflow = "hidden";
  }

  function closeModal() {
    box.classList.remove("scale-100", "opacity-100");
    box.classList.add("scale-90", "opacity-0");

    setTimeout(() => {
      modal.classList.add("opacity-0", "pointer-events-none");
      document.body.style.overflow = "";
    }, 200);
  }

  if (open) open.addEventListener("click", openModal);
  if (close) close.addEventListener("click", closeModal);

  modal.addEventListener("click", (e) => {
    if (e.target === modal) closeModal();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeModal();
  });
}

// =====================
// DROPDOWN
// =====================
function initDropdown() {
  const btn = document.getElementById("dropdownBtn");
  const menu = document.getElementById("dropdownMenu");
  const value = document.getElementById("dropdownValue");
  const input = document.getElementById("dropdownInput");

  if (!btn || !menu) return;

  btn.addEventListener("click", () => {
    menu.classList.toggle("hidden");
  });

  document.querySelectorAll(".dropdown-item").forEach((item) => {
    item.addEventListener("click", () => {
      value.textContent = item.textContent;
      input.value = item.textContent;
      menu.classList.add("hidden");
    });
  });

  document.addEventListener("click", (e) => {
    if (!btn.contains(e.target) && !menu.contains(e.target)) {
      menu.classList.add("hidden");
    }
  });
}

// =====================
// MOBILE MENU
// =====================
function initMobileMenu() {
  const toggle = document.getElementById("mobile-menu-toggle");
  const menu = document.getElementById("mobile-nav");
  if (!toggle || !menu) return;

  function closeMenu() {
    menu.classList.add("hidden");
    toggle.setAttribute("aria-expanded", "false");
  }

  toggle.addEventListener("click", () => {
    const isOpen = !menu.classList.contains("hidden");
    menu.classList.toggle("hidden", isOpen);
    toggle.setAttribute("aria-expanded", String(!isOpen));
  });

  menu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeMenu);
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth >= 1024) closeMenu();
  });
}

// =====================
// CONTACT FORM
// =====================
function initContactForm() {
  const form = document.getElementById("contactForm");
  if (!form) return;

  function getCookie(name) {
    return document.cookie
      .split(";")
      .map((cookie) => cookie.trim())
      .find((cookie) => cookie.startsWith(name + "="))
      ?.split("=")[1];
  }

  function getCsrfToken() {
    const input = form.querySelector('input[name="csrfmiddlewaretoken"]');
    return input?.value || decodeURIComponent(getCookie("csrftoken") || "");
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    btn.innerText = "Sending...";

    const data = {
      name: form.name.value,
      email: form.email.value,
      company: form.company.value,
      subject: document.getElementById("dropdownInput")?.value || "General",
      message: form.message.value,
    };

    try {
      const res = await fetch("/api/contact/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCsrfToken(),
        },
        body: JSON.stringify(data),
      });

      const result = await res.json();

      showToast(result.status === "success" ? "Sent!" : "Failed");
      form.reset();
    } catch {
      showToast("Network error");
    }

    btn.disabled = false;
    btn.innerText = "Send Message";
  });
}

// =====================
// TOAST
// =====================
function showToast(msg) {
  const toast = document.getElementById("toast");
  if (!toast) return;

  toast.innerText = msg;
  toast.style.opacity = "1";

  setTimeout(() => {
    toast.style.opacity = "0";
  }, 3000);
}

const glow = document.getElementById("mouseGlow");

if (glow) {
  window.addEventListener("mousemove", (e) => {
    glow.style.left = e.clientX + "px";
    glow.style.top = e.clientY + "px";
  });
}

document.querySelectorAll(".surface-hover").forEach((card) => {
  card.addEventListener("pointermove", (e) => {
    const rect = card.getBoundingClientRect();
    card.style.setProperty("--x", `${e.clientX - rect.left}px`);
    card.style.setProperty("--y", `${e.clientY - rect.top}px`);
  });
});

document.addEventListener("mousemove", (e) => {
  const glow = document.getElementById("cursorGlow");
  if (!glow) return;
  glow.style.left = e.clientX + "px";
  glow.style.top = e.clientY + "px";
});

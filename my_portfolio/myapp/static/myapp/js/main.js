lucide.createIcons();
const scrollProgress = document.querySelector("#scroll-progress");
const navLinks = [...document.querySelectorAll(".nav-link")];
const sections = navLinks
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);
const updateScrollState = () => {
  const scrollableHeight =
    document.documentElement.scrollHeight - window.innerHeight;
  scrollProgress.style.width = `${scrollableHeight > 0 ? (window.scrollY / scrollableHeight) * 100 : 0}%`;
  const activeSection = sections
    .slice()
    .reverse()
    .find((section) => section.offsetTop <= window.scrollY + 150);
  navLinks.forEach((link) =>
    link.classList.toggle(
      "is-active",
      activeSection && link.getAttribute("href") === `#${activeSection.id}`,
    ),
  );
};
const revealObserver = new IntersectionObserver(
  (entries) =>
    entries.forEach((entry) => {
      if (entry.isIntersecting) entry.target.classList.add("is-visible");
    }),
  { threshold: 0.14 },
);
document
  .querySelectorAll(".reveal")
  .forEach((element) => revealObserver.observe(element));
document.querySelectorAll(".surface-hover").forEach((card) =>
  card.addEventListener("pointermove", (event) => {
    const rect = card.getBoundingClientRect();
    card.style.setProperty("--x", `${event.clientX - rect.left}px`);
    card.style.setProperty("--y", `${event.clientY - rect.top}px`);
  }),
);
const roleWords = [...document.querySelectorAll(".role-word")];
let roleIndex = 0;
window.setInterval(() => {
  roleWords[roleIndex].classList.remove("is-visible");
  roleIndex = (roleIndex + 1) % roleWords.length;
  roleWords[roleIndex].classList.add("is-visible");
}, 2500);
const typeTerminal = async () => {
  const commands = [...document.querySelectorAll(".cmd")];
  const outputs = [...document.querySelectorAll("[data-output]")];
  const wait = (ms) => new Promise((resolve) => window.setTimeout(resolve, ms));
  for (let index = 0; index < commands.length; index += 1) {
    const text = commands[index].dataset.text;
    for (let i = 0; i <= text.length; i += 1) {
      commands[index].textContent = text.slice(0, i);
      await wait(38);
    }
    await wait(180);
    if (outputs[index])
      outputs[index].textContent = outputs[index].dataset.output;
  }
};
const copyEmailButton = document.querySelector("#copy-email");
copyEmailButton?.addEventListener("click", async () => {
  const label = copyEmailButton.querySelector("span");
  const originalText = label.textContent;
  try {
    await navigator.clipboard.writeText(copyEmailButton.dataset.email);
    label.textContent = "Email Copied";
  } catch {
    label.textContent = "Copy Failed";
  }
  window.setTimeout(() => {
    label.textContent = originalText;
  }, 1600);
});
typeTerminal();
updateScrollState();
window.addEventListener("scroll", updateScrollState, { passive: true });
window.addEventListener("resize", updateScrollState);

const openBtn = document.getElementById("open-contact");
const modal = document.getElementById("contact-modal");
const modalBox = document.getElementById("modal-box");
const closeBtn = document.getElementById("close-contact");

openBtn.addEventListener("click", () => {
  modal.classList.remove("opacity-0", "pointer-events-none");

  setTimeout(() => {
    modalBox.classList.remove("scale-90", "opacity-0");
    modalBox.classList.add("scale-100", "opacity-100");
  }, 50);
});

closeBtn.addEventListener("click", closeModal);

modal.addEventListener("click", (e) => {
  if (e.target === modal) closeModal();
});

function closeModal() {
  modalBox.classList.remove("scale-100", "opacity-100");
  modalBox.classList.add("scale-90", "opacity-0");

  setTimeout(() => {
    modal.classList.add("opacity-0", "pointer-events-none");
  }, 200);
}

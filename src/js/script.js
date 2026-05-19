const menuToggle = document.querySelector(".menu-toggle");
const navLinks = document.querySelector(".nav-links");

function fecharMenu() {
  menuToggle.classList.remove("ativo");
  navLinks.classList.remove("ativo");
  menuToggle.setAttribute("aria-expanded", "false");
  menuToggle.setAttribute("aria-label", "Abrir menu");
}

menuToggle.addEventListener("click", () => {
  const menuAberto = navLinks.classList.toggle("ativo");

  menuToggle.classList.toggle("ativo", menuAberto);
  menuToggle.setAttribute("aria-expanded", String(menuAberto));
  menuToggle.setAttribute("aria-label", menuAberto ? "Fechar menu" : "Abrir menu");
});

navLinks.addEventListener("click", (evento) => {
  if (evento.target.tagName === "A") {
    fecharMenu();
  }
});

window.addEventListener("resize", () => {
  if (window.innerWidth > 768) {
    fecharMenu();
  }
});

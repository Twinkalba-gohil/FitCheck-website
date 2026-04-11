// ========================================
// HOME.JS - Homepage specific functionality
// ========================================

// ========== IMAGE SLIDER ==========
  
const slider = document.querySelector(".slider_image");
const slides = document.querySelectorAll(".sliderimg");
const btnLeft = document.querySelector(".btn-left");
const btnRight = document.querySelector(".btn-right");

let index = 1;
let interval;

function getSlideWidth() {
  return slides.length ? slides[0].clientWidth : 0;
}

function setStartPosition() {
  if (!slider || !slides.length) return;
  slider.style.transition = "none";
  slider.style.transform = `translateX(-${getSlideWidth() * index}px)`;
}

function startAuto() {
  if (!slider) return;
  interval = setInterval(() => nextSlide(), 3000);
}

function nextSlide() {
  if (!slider || index >= slides.length - 1) return;
  index++;
  slider.style.transition = "transform 0.8s ease";
  slider.style.transform = `translateX(-${getSlideWidth() * index}px)`;
}

function prevSlide() {
  if (!slider || index <= 0) return;
  index--;
  slider.style.transition = "transform 0.8s ease";
  slider.style.transform = `translateX(-${getSlideWidth() * index}px)`;
}

if (slider) {
  slider.addEventListener("transitionend", () => {
    if (slides[index] && slides[index].classList.contains("clone")) {
      slider.style.transition = "none";
      index = index === slides.length - 1 ? 1 : slides.length - 2;
      slider.style.transform = `translateX(-${getSlideWidth() * index}px)`;
    }
  });

  window.addEventListener("load", setStartPosition);
  window.addEventListener("resize", setStartPosition);
  startAuto();
}

if (btnLeft) btnLeft.onclick = prevSlide;
if (btnRight) btnRight.onclick = nextSlide;
document.querySelectorAll(".product-card").forEach(card => {
  card.addEventListener("click", () => {
    const id = card.dataset.id;
    window.location.href = `/product/${id}`;
  });
});
/*============= NAVBAR SECTION =============*/
const header = document.getElementById("header");
if (header) {
  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
      header.classList.add("scrolled");
    } else {
      header.classList.remove("scrolled");
    }
  });
}

/*============= SLIDER SECTION =============*/
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

/* ================= PRODUCT DETAILS PAGE ================= */

const products = [
  {
    id: 1,
    name: "Men Casual Shirt",
    price: "₹999",
    mrp: "₹1499",
    images: [
      "image/product/p1.jpg",
      "image/product/p2.jpg",
      "image/product/p3.jpg"
    ]
  },
  {
    id: 2,
    name: "Men Casual Shirt",
    price: "₹999",
    mrp: "₹1499",
    images: [
      "image/product/p2.jpg",
      "image/product/p3.jpg",
      "image/product/p4.jpg"
    ]
  },
  {
    id: 3,
    name: "Men Casual Shirt",
    price: "₹999",
    mrp: "₹1499",
    images: [
      "image/set_up_banner/1.jpg",
      "image/set_up_banner/2.jpg",
      "image/set_up_banner/3.jpg"
    ]
  }
];

// URL ID
const params = new URLSearchParams(window.location.search);
const id = parseInt(params.get("id"));

const product = products.find(p => p.id === id);

if (product) {
  document.getElementById("pName").innerText = product.name;
  document.getElementById("price").innerText = product.price;
  document.getElementById("mrp").innerText = product.mrp;

  document.getElementById("mainImg").src = product.images[0];
  document.getElementById("thumb1").src = product.images[0];
  document.getElementById("thumb2").src = product.images[1];
  document.getElementById("thumb3").src = product.images[2];
}

// Thumbnail click
document.querySelectorAll(".thumbs img").forEach(img => {
  img.onclick = () => {
    document.getElementById("mainImg").src = img.src;
  };
});

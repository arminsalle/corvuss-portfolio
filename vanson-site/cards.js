/* VANSON — shared product card factory + 3D hover tilt */
(function () {
  const G = window.VANSON_GROUPS || [];
  const gLabel = Object.fromEntries(G.map((g) => [g.id, g.label]));

  window.vansonCard = function (p, tag) {
    const a = document.createElement("a");
    a.className = "card";
    a.href = `product.html?id=${p.id}`;
    a.target = "_blank";
    a.rel = "noopener";
    a.innerHTML =
      (tag ? `<span class="card-tag">${tag}</span>` : "") +
      `<div class="card-img"><img loading="lazy" src="${p.im}" alt="${p.n}"></div>` +
      `<div class="card-info">
         <span class="card-cat">${gLabel[p.g] || ""}</span>
         <span class="card-name">${p.n}</span>
         <span class="card-price">${p.pr}</span>
       </div>`;
    attachTilt(a);
    return a;
  };

  /* 3D tilt that follows the cursor */
  function attachTilt(card) {
    const img = card.querySelector(".card-img img");
    if (!img) return;
    card.addEventListener("mousemove", (e) => {
      const r = card.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width - 0.5;   /* -0.5 .. 0.5 */
      const py = (e.clientY - r.top) / r.height - 0.5;
      img.style.transform =
        `perspective(700px) rotateY(${(px * 22).toFixed(2)}deg) rotateX(${(-py * 22).toFixed(2)}deg) scale(1.12) translateZ(24px)`;
    });
    card.addEventListener("mouseleave", () => {
      img.style.transform = "";
    });
  }
  window.vansonAttachTilt = attachTilt;
})();

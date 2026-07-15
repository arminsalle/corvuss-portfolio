/* VANSON — product detail page */
(function () {
  const P = window.VANSON_PRODUCTS || [];
  const D = window.VANSON_DETAILS || {};
  const G = window.VANSON_GROUPS || [];
  const gLabel = Object.fromEntries(G.map((g) => [g.id, g.label]));

  const id = parseInt(new URLSearchParams(location.search).get("id"), 10);
  const p = P.find((x) => x.id === id);
  if (!p) {
    document.getElementById("pd").innerHTML =
      '<div class="pd-crumb mono">PRODUCT NOT FOUND — <a href="shop.html">[ BACK TO THE RANGE ]</a></div>';
    return;
  }
  const det = D[id] || D[String(id)] || {};

  document.title = `${p.n} — VANSON LEATHERS`;
  document.getElementById("pd-crumb").innerHTML =
    `<a href="index.html">HOME</a> / <a href="shop.html">SHOP</a> / <a href="shop.html?g=${p.g}">${(gLabel[p.g] || "").toUpperCase()}</a> / <b>${p.n}</b>`;
  document.getElementById("pd-cat").textContent = `( ${(gLabel[p.g] || "").toUpperCase()} — HAND-BUILT IN FALL RIVER )`;
  document.getElementById("pd-name").textContent = p.n;
  document.getElementById("pd-price").textContent = p.pr;
  document.getElementById("pd-order").href = p.u;

  /* ---------- size picker ---------- */
  const sizes = det.sz || [];
  let selectedSize = "";
  const szWrap = document.getElementById("pd-sizes");
  const szSel = document.getElementById("pd-size-sel");
  const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "");
  function pickSize(optId, label, btn) {
    selectedSize = label;
    szSel.textContent = label;
    szWrap.querySelectorAll(".size-chip").forEach((c) => c.classList.remove("on"));
    if (btn) btn.classList.add("on");
    /* deep-link the size on their configurator */
    document.getElementById("pd-order").href = p.u.split("#")[0] + `#/${optId}-size-${slug(label)}`;
  }
  if (sizes.length) {
    szWrap.hidden = false;
    const grid = document.getElementById("pd-size-grid");
    sizes.forEach(([optId, label]) => {
      const b = document.createElement("button");
      b.className = "size-chip";
      b.textContent = label;
      b.addEventListener("click", () => pickSize(optId, label, b));
      grid.appendChild(b);
    });
    if (sizes.length === 1) pickSize(sizes[0][0], sizes[0][1], grid.querySelector(".size-chip"));
  }

  /* ---------- add to cart ---------- */
  const addBtn = document.getElementById("pd-add");
  addBtn.addEventListener("click", () => {
    if (sizes.length && !selectedSize) {
      szSel.textContent = "PLEASE PICK A SIZE";
      addBtn.classList.remove("shake");
      void addBtn.offsetWidth;
      addBtn.classList.add("shake");
      szWrap.scrollIntoView({ behavior: "smooth", block: "center" });
      return;
    }
    window.vansonCartAdd(p.id, selectedSize);
  });

  const short = document.getElementById("pd-short");
  short.innerHTML = det.ds || "<p>Hand-crafted by Vanson Leathers of Fall River, Massachusetts — designed, engineered, cut and produced in the U.S.A.</p>";
  const longWrap = document.getElementById("pd-long-wrap");
  if (det.dl) document.getElementById("pd-long").innerHTML = det.dl;
  else longWrap.style.display = "none";

  /* gallery: local primary + scraped views */
  const main = document.getElementById("pd-main");
  const thumbs = document.getElementById("pd-thumbs");
  const sources = [p.im].concat((det.gal || []).slice(1));
  main.src = sources[0];
  main.alt = p.n;
  if (sources.length > 1) {
    sources.forEach((src, i) => {
      const t = document.createElement("button");
      t.className = "pd-thumb" + (i === 0 ? " on" : "");
      t.innerHTML = `<img loading="lazy" src="${src}" alt="">`;
      t.addEventListener("click", () => {
        main.src = src;
        thumbs.querySelectorAll(".pd-thumb").forEach((x) => x.classList.remove("on"));
        t.classList.add("on");
      });
      thumbs.appendChild(t);
    });
  }
  window.vansonAttachTilt(document.getElementById("pd-stage"));

  /* related */
  const rel = P.filter((x) => x.g === p.g && x.id !== p.id).slice(0, 4);
  const grid = document.getElementById("pd-related-grid");
  rel.forEach((r) => grid.appendChild(window.vansonCard(r)));

  if (window.Lenis) {
    const lenis = new Lenis({ lerp: 0.09, smoothWheel: true });
    function raf(t) { lenis.raf(t); requestAnimationFrame(raf); }
    requestAnimationFrame(raf);
  }
})();

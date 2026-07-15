/* VANSON — page content wiring (loader, marquee, featured grid, categories) */
(function () {
  const P = window.VANSON_PRODUCTS || [];
  const G = window.VANSON_GROUPS || [];
  const gLabel = Object.fromEntries(G.map((g) => [g.id, g.label]));

  /* ---------- totals ---------- */
  const total = P.length;
  document.querySelectorAll(".js-total").forEach((el) => (el.textContent = total));
  const navCount = document.getElementById("nav-count");
  if (navCount) navCount.textContent = total;
  const totalStat = document.querySelector(".js-total-stat");
  if (totalStat) totalStat.dataset.count = total;

  /* ---------- loader: tracks hero frame preload ---------- */
  const loader = document.getElementById("loader");
  const pctEl = document.getElementById("loader-pct");
  if (loader && pctEl) {
    const HERO_FRAMES = 180;
    let loaded = 0, finished = false;
    const finish = () => {
      if (finished) return;
      finished = true;
      pctEl.textContent = "100%";
      setTimeout(() => loader.classList.add("done"), 250);
    };
    const bump = () => {
      loaded++;
      const pct = Math.min(99, Math.round((loaded / HERO_FRAMES) * 100));
      pctEl.textContent = String(pct).padStart(2, "0") + "%";
      if (loaded >= HERO_FRAMES) finish();
    };
    for (let i = 1; i <= HERO_FRAMES; i++) {
      const img = new Image();
      img.onload = bump;
      img.onerror = bump;
      img.src = `frames/hero/frame_${String(i).padStart(4, "0")}.jpg`;
    }
    setTimeout(finish, 12000); // hard fallback
  }

  /* ---------- marquee ---------- */
  const track = document.getElementById("marquee-track");
  if (track) {
    const words = ["TRADITIONAL", "SPORTRIDER", "CAFE RACER", "RACING SUITS", "MILITARY & POLICE", "ADVENTURE TOURING", "GLOVES", "BAGS & TOTES", "ARMOR"];
    const half = words.map((w) => `<span>${w}<i>·</i></span>`).join("");
    track.innerHTML = half + half; /* duplicate for seamless -50% loop */
  }

  /* ---------- product card factory (shared, from cards.js) ---------- */
  const card = window.vansonCard;

  /* ---------- 02 icons grid: curated best-of ---------- */
  const iconsGrid = document.getElementById("icons-grid");
  if (iconsGrid) {
    const wanted = [
      "MODEL AR - ORIGINAL VANSON",
      "COMMANDO",
      "ENFIELD",
      "MARK 2",
      "COBRA MARK",
      "DAYTONA",
      "STAR",
      "CHOPPER",
    ];
    const picked = [];
    const used = new Set();
    for (const w of wanted) {
      const hit = P.find((p) => p.n.toUpperCase().includes(w) && !used.has(p.u));
      if (hit) { picked.push(hit); used.add(hit.u); }
    }
    for (const p of P) {
      if (picked.length >= 8) break;
      if (!used.has(p.u) && (p.g === "traditional" || p.g === "sportrider" || p.g === "limited")) {
        picked.push(p); used.add(p.u);
      }
    }
    picked.slice(0, 8).forEach((p, i) => {
      const c = card(p, i < 4 ? "BEST SELLER" : "");
      c.classList.add("reveal");
      c.style.transitionDelay = (i % 4) * 70 + "ms";
      iconsGrid.appendChild(c);
    });
  }

  /* ---------- 04 categories list ---------- */
  const catList = document.getElementById("cat-list");
  const preview = document.getElementById("cat-preview");
  if (catList) {
    const firstImg = {};
    for (const p of P) if (!firstImg[p.g]) firstImg[p.g] = p.im;
    for (const g of G) {
      const row = document.createElement("a");
      row.className = "cat-row reveal";
      row.href = `shop.html?g=${g.id}`;
      row.innerHTML = `<h3>${g.label}</h3><span class="cat-count">[ ${g.count} ]</span>`;
      if (preview) {
        row.addEventListener("mouseenter", () => {
          preview.querySelector("img").src = firstImg[g.id] || "";
          preview.classList.add("on");
        });
        row.addEventListener("mouseleave", () => preview.classList.remove("on"));
      }
      catList.appendChild(row);
    }
    if (preview) {
      window.addEventListener("mousemove", (e) => {
        preview.style.left = e.clientX + 40 + "px";
        preview.style.top = e.clientY + "px";
      });
    }
  }

  /* ---------- re-observe injected .reveal nodes ---------- */
  document.addEventListener("DOMContentLoaded", () => {
    if (window.__revealObserver) {
      document.querySelectorAll(".reveal:not(.in)").forEach((el) => window.__revealObserver.observe(el));
    }
  });
})();

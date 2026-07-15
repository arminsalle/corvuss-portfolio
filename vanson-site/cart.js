/* VANSON — cart: localStorage-backed, drawer UI, nav badge */
(function () {
  const P = window.VANSON_PRODUCTS || [];
  const KEY = "vanson_cart_v1";

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; }
  }
  function save(items) {
    localStorage.setItem(KEY, JSON.stringify(items));
    renderBadge();
    renderDrawer();
  }
  function price(pr) {
    return parseFloat(String(pr).replace(/[^0-9.]/g, "")) || 0;
  }
  function fmt(n) {
    return "$" + n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  window.vansonCartAdd = function (id, size) {
    const items = load();
    const hit = items.find((i) => i.id === id && i.size === size);
    if (hit) hit.qty += 1;
    else items.push({ id, size: size || "", qty: 1 });
    save(items);
    openDrawer();
  };

  /* ---------- nav badge ---------- */
  function count() { return load().reduce((s, i) => s + i.qty, 0); }
  function renderBadge() {
    const b = document.getElementById("cart-count");
    if (b) b.textContent = count();
  }

  /* ---------- drawer ---------- */
  let built = false;
  function build() {
    if (built) return;
    built = true;
    const wrap = document.createElement("div");
    wrap.id = "cart-drawer-wrap";
    wrap.innerHTML =
      `<div class="cart-overlay" id="cart-overlay"></div>
       <aside class="cart-drawer" id="cart-drawer">
         <header class="cart-head">
           <span class="mono">[ CART — <span id="cart-drawer-count">0</span> ]</span>
           <button class="cart-close mono" id="cart-close">CLOSE ✕</button>
         </header>
         <div class="cart-items" id="cart-items"></div>
         <footer class="cart-foot">
           <div class="cart-total mono">SUBTOTAL <b id="cart-total">$0.00</b></div>
           <a class="pd-cta cart-checkout" id="cart-checkout" href="#">[ PLACE ORDER REQUEST ]</a>
           <span class="mono cart-note">ORDER REQUEST OPENS AN EMAIL TO THE VANSON WORKSHOP — THEY CONFIRM SIZING, SHIPPING &amp; PAYMENT.</span>
         </footer>
       </aside>`;
    document.body.appendChild(wrap);
    document.getElementById("cart-overlay").addEventListener("click", closeDrawer);
    document.getElementById("cart-close").addEventListener("click", closeDrawer);
    renderDrawer();
  }
  function openDrawer() { build(); document.body.classList.add("cart-open"); renderDrawer(); }
  function closeDrawer() { document.body.classList.remove("cart-open"); }
  window.vansonCartOpen = openDrawer;

  function renderDrawer() {
    const list = document.getElementById("cart-items");
    if (!list) return;
    const items = load();
    document.getElementById("cart-drawer-count").textContent = count();
    list.innerHTML = "";
    let total = 0;
    if (!items.length) {
      list.innerHTML = '<p class="cart-empty mono">YOUR CART IS EMPTY — THE WORKSHOP IS WAITING.</p>';
    }
    items.forEach((it, idx) => {
      const p = P.find((x) => x.id === it.id);
      if (!p) return;
      total += price(p.pr) * it.qty;
      const row = document.createElement("div");
      row.className = "cart-row";
      row.innerHTML =
        `<a href="product.html?id=${p.id}" target="_blank" rel="noopener" class="cart-thumb"><img src="${p.im}" alt=""></a>
         <div class="cart-info">
           <span class="cart-name">${p.n}</span>
           ${it.size ? `<span class="mono cart-size">SIZE ${it.size}</span>` : ""}
           <span class="mono cart-price">${p.pr}</span>
         </div>
         <div class="cart-qty">
           <button class="chip" data-a="-" aria-label="less">−</button>
           <span class="mono">${it.qty}</span>
           <button class="chip" data-a="+" aria-label="more">+</button>
           <button class="chip cart-rm" data-a="x" aria-label="remove">✕</button>
         </div>`;
      row.querySelectorAll("button").forEach((b) =>
        b.addEventListener("click", () => {
          const items2 = load();
          const h = items2.find((i) => i.id === it.id && i.size === it.size);
          if (!h) return;
          if (b.dataset.a === "+") h.qty += 1;
          if (b.dataset.a === "-") h.qty = Math.max(0, h.qty - 1);
          if (b.dataset.a === "x") h.qty = 0;
          save(items2.filter((i) => i.qty > 0));
        })
      );
      list.appendChild(row);
    });
    const t = document.getElementById("cart-total");
    if (t) t.textContent = fmt(total);
    const co = document.getElementById("cart-checkout");
    if (co) {
      const lines = items.map((it) => {
        const p = P.find((x) => x.id === it.id);
        return p ? `${it.qty}x ${p.n}${it.size ? " (size " + it.size + ")" : ""} — ${p.pr} — ${p.u.split("#")[0]}` : "";
      });
      const body = encodeURIComponent(
        "Hello Vanson,\n\nI would like to order:\n\n" + lines.join("\n") + `\n\nSubtotal: ${fmt(total)}\n\nName:\nShipping address:\nPhone:\n`
      );
      co.href = `mailto:vanson@vansonleathers.com?subject=${encodeURIComponent("Order request — vansonleathers.com")}&body=${body}`;
      co.classList.toggle("disabled", !items.length);
    }
  }

  /* ---------- wire nav button ---------- */
  document.addEventListener("DOMContentLoaded", () => {
    renderBadge();
    const btn = document.getElementById("cart-btn");
    if (btn) btn.addEventListener("click", (e) => { e.preventDefault(); openDrawer(); });
  });
  renderBadge();
  const btn = document.getElementById("cart-btn");
  if (btn) btn.addEventListener("click", (e) => { e.preventDefault(); openDrawer(); });
})();

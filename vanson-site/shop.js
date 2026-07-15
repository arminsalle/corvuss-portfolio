/* VANSON — shop page: filters, search, full product grid */
(function () {
  const P = window.VANSON_PRODUCTS || [];
  const G = window.VANSON_GROUPS || [];
  const gLabel = Object.fromEntries(G.map((g) => [g.id, g.label]));

  const tools = document.getElementById("shop-tools");
  const search = document.getElementById("shop-search");
  const grid = document.getElementById("shop-grid");
  const countEl = document.getElementById("shop-count");

  const params = new URLSearchParams(location.search);
  let activeGroup = params.get("g") || "all";
  let query = (params.get("q") || "").trim().toLowerCase();
  if (query) search.value = params.get("q").trim();

  /* filter chips */
  const chips = [];
  function addChip(id, label, count) {
    const b = document.createElement("button");
    b.className = "chip" + (id === activeGroup ? " on" : "");
    b.textContent = count != null ? `${label} [ ${count} ]` : label;
    b.addEventListener("click", () => {
      activeGroup = id;
      chips.forEach((c) => c.el.classList.toggle("on", c.id === id));
      history.replaceState(null, "", id === "all" ? "shop.html" : `shop.html?g=${id}`);
      render();
    });
    tools.insertBefore(b, search);
    chips.push({ id, el: b });
  }
  addChip("all", "ALL", P.length);
  for (const g of G) addChip(g.id, g.label, g.count);

  search.addEventListener("input", () => {
    query = search.value.trim().toLowerCase();
    render();
  });

  function render() {
    const items = P.filter(
      (p) =>
        (activeGroup === "all" || p.g === activeGroup) &&
        (!query || p.n.toLowerCase().includes(query))
    );
    countEl.textContent = `SHOWING ${items.length} / ${P.length} PRODUCTS`;
    grid.innerHTML = "";
    const frag = document.createDocumentFragment();
    for (const p of items) frag.appendChild(window.vansonCard(p));
    grid.appendChild(frag);
  }
  render();

  /* smooth scroll */
  if (window.Lenis) {
    const lenis = new Lenis({ lerp: 0.09, smoothWheel: true });
    function raf(t) { lenis.raf(t); requestAnimationFrame(raf); }
    requestAnimationFrame(raf);
  }
})();

// Title autocomplete for every search box marked with data-autocomplete.
(function () {
  let titlesPromise = null;
  const loadTitles = () =>
    (titlesPromise ||= fetch(window.TITLES_URL)
      .then((r) => r.json())
      .then((d) => d.titles)
      .catch(() => []));

  const escapeHtml = (s) =>
    s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

  document.querySelectorAll("input[data-autocomplete]").forEach((input) => {
    const form = input.form;
    const list = form.querySelector(".suggest");
    let items = [];
    let active = -1;

    const close = () => { list.hidden = true; active = -1; };
    const render = () => {
      list.innerHTML = items
        .map((t, i) => `<li role="option" data-i="${i}" aria-selected="${i === active}">${escapeHtml(t)}</li>`)
        .join("");
      list.hidden = items.length === 0;
    };
    const choose = (title) => { input.value = title; close(); form.submit(); };

    input.setAttribute("role", "combobox");
    input.setAttribute("aria-autocomplete", "list");
    input.addEventListener("focus", loadTitles, { once: true });
    input.addEventListener("input", async () => {
      const q = input.value.trim().toLowerCase();
      if (q.length < 2) { items = []; close(); return; }
      const titles = await loadTitles();
      const starts = [], contains = [];
      for (const t of titles) {
        const l = t.toLowerCase();
        if (l.startsWith(q)) starts.push(t);
        else if (l.includes(q)) contains.push(t);
        if (starts.length >= 8) break;
      }
      items = starts.concat(contains).slice(0, 8);
      active = -1;
      render();
    });
    input.addEventListener("keydown", (e) => {
      if (list.hidden) return;
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        const n = items.length;
        active = e.key === "ArrowDown" ? (active + 1) % n : (active - 1 + n) % n;
        render();
      } else if (e.key === "Enter" && active >= 0) {
        e.preventDefault();
        choose(items[active]);
      } else if (e.key === "Escape") {
        close();
      }
    });
    list.addEventListener("mousedown", (e) => {
      const li = e.target.closest("li");
      if (li) { e.preventDefault(); choose(items[+li.dataset.i]); }
    });
    input.addEventListener("blur", () => setTimeout(close, 100));
  });
})();

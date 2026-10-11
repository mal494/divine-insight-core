/* ============ Divine Insight Core — Card Explorer ============ */
(function () {
  "use strict";

  /* Path to the dataset, relative to this page.
     Bump this when Core ships a new release (keep in sync with the repo's tags). */
  var DATASET_PATH = "../data/tarot_data_v1.6.1.json";

  var SUIT_GLYPHS = { Wands: "♣", Cups: "♥", Swords: "♠", Pentacles: "♦" };
  var prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var grid = document.getElementById("grid");
  var searchInput = document.getElementById("search");
  var chipsEl = document.getElementById("chips");
  var sortSel = document.getElementById("sort");
  var resultCount = document.getElementById("resultCount");
  var emptyEl = document.getElementById("empty");
  var resetBtn = document.getElementById("resetBtn");
  var randomBtn = document.getElementById("randomBtn");
  var backdrop = document.getElementById("modalBackdrop");
  var modalBody = document.getElementById("modalBody");

  var state = {
    cards: [],
    meta: null,
    query: "",
    filter: "all",
    sort: "deck",
    list: [],       // currently visible cards
    modalIdx: -1
  };

  /* ---------- tiny starfield ---------- */
  (function stars() {
    var c = document.getElementById("stars");
    var ctx = c.getContext("2d");
    function paint() {
      c.width = innerWidth; c.height = innerHeight;
      for (var i = 0; i < 140; i++) {
        var gold = Math.random() < 0.15;
        ctx.beginPath();
        ctx.arc(Math.random() * c.width, Math.random() * c.height, Math.random() * 1.3 + 0.3, 0, 7);
        ctx.fillStyle = gold ? "rgba(227,195,124,0.5)" : "rgba(220,220,255,0.4)";
        ctx.fill();
      }
    }
    paint();
    if (!prefersReduced) {
      var t = 0;
      (function twinkle() {
        t += 0.02;
        paint();
        requestAnimationFrame(twinkle);
      })();
    }
    addEventListener("resize", paint);
  })();

  function toRoman(n) {
    var table = [[10, "X"], [9, "IX"], [5, "V"], [4, "IV"], [1, "I"]];
    var s = "";
    table.forEach(function (p) { while (n >= p[0]) { s += p[1]; n -= p[0]; } });
    return s || "0";
  }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function normalize(c, idx) {
    var major = c.arcana === "Major";
    var up = (c.meanings && c.meanings.upright) || {};
    var rev = (c.meanings && c.meanings.reversed) || {};
    return {
      idx: idx,
      key: c.key, name: c.name, arcana: c.arcana, suit: c.suit || "",
      element: c.element || "", astrology: c.astrology || "",
      short: c.short_description || "",
      num: major ? toRoman(c.number) : String(c.number),
      glyph: major ? "✦" : (SUIT_GLYPHS[c.suit] || "✦"),
      upKeys: up.keywords || [], upDesc: up.description || "",
      revKeys: rev.keywords || [], revDesc: rev.description || "",
      hay: [c.name, c.arcana, c.suit, c.element, c.astrology,
            (up.keywords || []).join(" "), up.description,
            (rev.keywords || []).join(" "), rev.description,
            c.short_description].join(" ").toLowerCase()
    };
  }

  function applyFilters() {
    var q = state.query.trim().toLowerCase();
    var list = state.cards.filter(function (c) {
      if (state.filter !== "all") {
        if (state.filter === "Major") { if (c.arcana !== "Major") return false; }
        else if (c.suit !== state.filter) return false;
      }
      if (q && c.hay.indexOf(q) === -1) return false;
      return true;
    });
    if (state.sort === "az") {
      list = list.slice().sort(function (a, b) { return a.name.localeCompare(b.name); });
    } else {
      list = list.slice().sort(function (a, b) { return a.idx - b.idx; });
    }
    state.list = list;
    render();
  }

  function render() {
    grid.innerHTML = "";
    var frag = document.createDocumentFragment();
    state.list.forEach(function (c, i) {
      var el = document.createElement("article");
      el.className = "mini";
      el.tabIndex = 0;
      el.setAttribute("role", "button");
      el.setAttribute("aria-label", c.name + ", view details");
      if (!prefersReduced) el.style.animationDelay = Math.min(i * 18, 500) + "ms";
      el.innerHTML =
        '<div class="mini-num">' + esc(c.num) + "</div>" +
        '<div class="mini-glyph">' + esc(c.glyph) + "</div>" +
        '<div class="mini-name">' + esc(c.name) + "</div>" +
        '<div class="mini-tags">' + esc(c.arcana === "Major" ? "Major Arcana" : c.suit) + "</div>" +
        '<div class="mini-keys">' + esc(c.upKeys.slice(0, 3).join(" · ")) + "</div>";
      el.addEventListener("click", function () { openModal(i); });
      el.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openModal(i); }
      });
      frag.appendChild(el);
    });
    grid.appendChild(frag);
    var n = state.list.length;
    resultCount.textContent = n === 78 ? "Showing all 78 cards"
      : n === 1 ? "1 card" : n + " cards";
    emptyEl.hidden = n !== 0;
  }

  function detailHTML(c) {
    function chips() {
      var out = [c.arcana === "Major" ? "Major Arcana" : "Minor Arcana"];
      if (c.suit) out.push(c.suit);
      if (c.element) out.push(c.element);
      return out.map(function (t) { return '<span class="d-chip">' + esc(t) + "</span>"; }).join("");
    }
    return (
      '<div style="text-align:center">' +
      '<div class="d-num">' + esc(c.num) + "</div>" +
      '<div class="d-glyph">' + esc(c.glyph) + "</div>" +
      '<h2 class="d-name" id="modalName">' + esc(c.name) + "</h2>" +
      '<div class="d-chips">' + chips() + "</div>" +
      (c.short ? '<p class="d-short">“' + esc(c.short) + "”</p>" : "") +
      (c.astrology ? '<p class="d-keys">Astrology · ' + esc(c.astrology) + "</p>" : "") +
      "</div>" +
      '<div class="d-section"><h3>Upright</h3>' +
      '<p class="d-keys">' + esc(c.upKeys.join(" · ")) + "</p>" +
      '<p class="meaning">' + esc(c.upDesc) + "</p></div>" +
      '<div class="d-section"><h3>Reversed</h3>' +
      '<p class="d-keys">' + esc(c.revKeys.join(" · ")) + "</p>" +
      '<p class="meaning">' + esc(c.revDesc) + "</p></div>"
    );
  }

  function openModal(i) {
    if (!state.list.length) return;
    state.modalIdx = (i + state.list.length) % state.list.length;
    modalBody.innerHTML = detailHTML(state.list[state.modalIdx]);
    backdrop.hidden = false;
    document.body.style.overflow = "hidden";
    document.getElementById("modalClose").focus();
  }
  function closeModal() {
    backdrop.hidden = true;
    document.body.style.overflow = "";
    state.modalIdx = -1;
  }
  function step(d) {
    if (state.modalIdx === -1) return;
    openModal(state.modalIdx + d);
    document.getElementById("modal").scrollTop = 0;
  }

  /* ---------- events ---------- */
  var deb;
  searchInput.addEventListener("input", function () {
    clearTimeout(deb);
    deb = setTimeout(function () { state.query = searchInput.value; applyFilters(); }, 160);
  });
  chipsEl.addEventListener("click", function (e) {
    var btn = e.target.closest(".chip");
    if (!btn) return;
    chipsEl.querySelectorAll(".chip").forEach(function (ch) {
      ch.classList.remove("active"); ch.setAttribute("aria-selected", "false");
    });
    btn.classList.add("active"); btn.setAttribute("aria-selected", "true");
    state.filter = btn.getAttribute("data-filter");
    applyFilters();
  });
  sortSel.addEventListener("change", function () { state.sort = sortSel.value; applyFilters(); });
  resetBtn.addEventListener("click", function () {
    searchInput.value = ""; state.query = ""; state.filter = "all"; state.sort = "deck";
    sortSel.value = "deck";
    chipsEl.querySelectorAll(".chip").forEach(function (ch) {
      var on = ch.getAttribute("data-filter") === "all";
      ch.classList.toggle("active", on); ch.setAttribute("aria-selected", String(on));
    });
    applyFilters();
  });
  randomBtn.addEventListener("click", function () {
    if (!state.list.length) return;
    openModal(Math.floor(Math.random() * state.list.length));
  });
  document.getElementById("modalClose").addEventListener("click", closeModal);
  document.getElementById("modalPrev").addEventListener("click", function (e) { e.stopPropagation(); step(-1); });
  document.getElementById("modalNext").addEventListener("click", function (e) { e.stopPropagation(); step(1); });
  backdrop.addEventListener("click", function (e) { if (e.target === backdrop) closeModal(); });
  document.addEventListener("keydown", function (e) {
    if (backdrop.hidden) return;
    if (e.key === "Escape") closeModal();
    if (e.key === "ArrowLeft") step(-1);
    if (e.key === "ArrowRight") step(1);
  });

  /* ---------- load ---------- */
  fetch(DATASET_PATH)
    .then(function (r) { if (!r.ok) throw new Error("fetch failed"); return r.json(); })
    .then(function (data) {
      state.meta = data.deck_metadata || {};
      state.cards = (data.cards || []).map(normalize);
      var m = state.meta;
      var ver = "deck " + (m.version || "?") + " · schema " + (m.schema_version || "?");
      document.getElementById("versionBadge").textContent = ver;
      document.getElementById("footVersion").textContent = ver;
      var majors = state.cards.filter(function (c) { return c.arcana === "Major"; }).length;
      document.getElementById("stats").innerHTML =
        stat(state.cards.length, "cards") + stat(majors, "major arcana") +
        stat(state.cards.length - majors, "minor arcana") + stat(m.schema_version || "?", "schema");
      applyFilters();
    })
    .catch(function () {
      document.getElementById("versionBadge").textContent = "could not load dataset";
      resultCount.textContent = "Could not load " + DATASET_PATH +
        ". Serve this page over http(s) — file:// blocks dataset loading.";
    });

  function stat(num, label) {
    return '<div class="stat"><span class="stat-num">' + esc(num) +
      '</span><span class="stat-label">' + esc(label) + "</span></div>";
  }
})();

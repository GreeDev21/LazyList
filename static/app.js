/* LazyList frontend — vanilla JS, Operate surface, Claymorphism world.
   The backend exposes only /api/search and /api/save (no list endpoint),
   so the visible catalog is the client's own record (localStorage), seeded
   with labeled synthetic demo data and enriched by the real API on capture. */

const API_BASE = "/api";

const CATEGORIES = [
  { key: "todo",        label: "Todo",      glyph: "stack",  gradient: "linear-gradient(160deg,#7c6cf0,#2b1f7a)" },
  { key: "juegos",      label: "Juegos",    glyph: "gamepad", gradient: "linear-gradient(160deg,#6d3df0,#221466)" },
  { key: "peliculas",   label: "Películas", glyph: "film",    gradient: "linear-gradient(160deg,#ec4899,#4a1245)" },
  { key: "series",      label: "Series",    glyph: "tv",      gradient: "linear-gradient(160deg,#60a5fa,#123a74)" },
  { key: "anime",       label: "Anime",     glyph: "sparkle", gradient: "linear-gradient(160deg,#e879f9,#55127a)" },
  { key: "mangas",      label: "Mangas",    glyph: "book",    gradient: "linear-gradient(160deg,#38bdf8,#0f3a66)" },
  { key: "comics",      label: "Cómics",    glyph: "chat",    gradient: "linear-gradient(160deg,#2dd4bf,#0f4a46)" },
  { key: "novelas",     label: "Novelas",   glyph: "bookmark", gradient: "linear-gradient(160deg,#f472b6,#6a1548)" },
  { key: "libros",      label: "Libros",    glyph: "book",    gradient: "linear-gradient(160deg,#818cf8,#2b1f7a)" },
  { key: "recursos",    label: "Recursos",  glyph: "link",    gradient: "linear-gradient(160deg,#a78bfa,#3b2a7a)" },
];

const SEARCHABLE = ["peliculas", "series", "anime", "mangas", "comics", "libros", "juegos", "recursos"];

const STATE_LABELS = { pendiente: "Pendiente", en_curso: "En curso", terminado: "Terminado" };
const STATE_ORDER = ["pendiente", "en_curso", "terminado"];

const ICONS = {
  stack: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M16.5 3.75V6h-9V3.75m9 0a2.25 2.25 0 00-2.25-2.25h-4.5A2.25 2.25 0 007.5 3.75m9 0h.008a2.25 2.25 0 012.25 2.25v10.5a2.25 2.25 0 01-2.25 2.25h-9a2.25 2.25 0 01-2.25-2.25V6a2.25 2.25 0 011.5-2.25M3.75 6h1.5m-1.5 3.75h1.5m-1.5 3.75h1.5m-1.5 3.75h1.5"/></svg>',
  gamepad: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M7 9h10a4 4 0 013.9 4.8l-.62 2.78a3 3 0 01-4.93 1.62l-1.6-1.38a1 1 0 00-1.3 0l-1.6 1.38a3 3 0 01-4.93-1.62L5.1 13.8A4 4 0 017 9z"/><path d="M9.25 12h.01M14.75 12h.01M12 10.5v.01M12 13.5v.01"/></svg>',
  film: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3.375 19.5h17.25m-17.25 0a1.125 1.125 0 01-1.125-1.125M3.375 19.5h7.5c.621 0 1.125-.504 1.125-1.125m-9.75 0V5.625m0 12.75v-1.5c0-.621.504-1.125 1.125-1.125m18.375 2.625V5.625m0 12.75c0 .621-.504 1.125-1.125 1.125m1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125m0 3.75h-7.5A1.125 1.125 0 0112 18.375m9.75-12.75c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125m19.5 0v1.5c0 .621-.504 1.125-1.125 1.125M2.25 5.625v1.5c0 .621.504 1.125 1.125 1.125m0 0h17.25m-17.25 0h7.5c.621 0 1.125.504 1.125 1.125M3.375 8.25c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125m17.25-3.75h-7.5c-.621 0-1.125.504-1.125 1.125m8.625-1.125c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h7.5m-7.5 0c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125M12 10.875v-1.5m0 1.5c0 .621-.504 1.125-1.125 1.125M12 10.875c0 .621.504 1.125 1.125 1.125m-2.25 0c.621 0 1.125.504 1.125 1.125M13.125 12h7.5m-7.5 0c-.621 0-1.125.504-1.125 1.125M20.625 12c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h7.5M12 14.625v-1.5m0 1.5c0 .621-.504 1.125-1.125 1.125M12 14.625c0 .621.504 1.125 1.125 1.125m-2.25 0c.621 0 1.125.504 1.125 1.125m0 1.5v-1.5m0 0c0-.621.504-1.125 1.125-1.125m0 0h7.5"/></svg>',
  tv: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M6 20.25h12M4.5 3.75h15a1.5 1.5 0 011.5 1.5v10.5a1.5 1.5 0 01-1.5 1.5h-15a1.5 1.5 0 01-1.5-1.5V5.25a1.5 1.5 0 011.5-1.5zM12 20.25v-2.25"/></svg>',
  sparkle: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456z"/></svg>',
  book: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25"/></svg>',
  bookmark: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M6.32 2.577a49.255 49.255 0 0111.36 0c1.497.174 2.57 1.46 2.57 2.93V21a.75.75 0 01-1.085.67L12 18.089l-7.165 3.583A.75.75 0 013.75 21V5.507c0-1.47 1.073-2.756 2.57-2.93z"/></svg>',
  chat: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 01-.825-.242m9.345-8.334a2.126 2.126 0 00-.476-.095 48.64 48.64 0 00-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0011.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155"/></svg>',
  link: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m13.35-.622l1.757-1.757a4.5 4.5 0 00-6.364-6.364l-4.5 4.5a4.5 4.5 0 001.242 7.244"/></svg>',
  tag: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M9.568 3H5.25A2.25 2.25 0 003 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 005.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 009.568 3z"/><path d="M6 6h.008v.008H6V6z"/></svg>',
  eye: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z"/><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>',
  eyeOff: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88"/></svg>',
  trash: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"/></svg>',
  plus: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4.5v15m7.5-7.5h-15"/></svg>',
  plusBadge: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" style="flex:none;width:1.8rem;height:1.8rem;padding:0.4rem;box-sizing:border-box;border-radius:999px;color:#fff;background:linear-gradient(180deg,var(--color-violet) 0%,var(--color-violet-deep) 100%);filter:drop-shadow(0 4px 10px rgba(109,61,240,0.5))"><path d="M12 4.5v15m7.5-7.5h-15"/></svg>',
  check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 12.75l6 6 9-13.5"/></svg>',
  warn: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"/></svg>',
  clock: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
  arrow: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757"/></svg>',
  pencil: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125"/></svg>',
  star: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.562.562 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.562.562 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z"/></svg>',
  starSolid: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.562.562 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.562.562 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z"/></svg>',
};

/* ------------------------------------------------------------------ state */
const LS_ITEMS = "lazylist:items";
const LS_SETTINGS = "lazylist:settings";

let items = [];
let settings = loadSettings();
let activeCategory = "todo";
let activeState = "todos";
let activeView = settings.view || "grid";
let captureCategory = "todo";

function apiToItem(apiData) {
  return Object.assign({}, apiData, {
    id: apiData.id,
    category: apiData.category,
    title: apiData.title || apiData.titulo || apiData.nombre || apiData.title_romaji || "Sin título",
    subtitle: subtitleFor(apiData, apiData.category),
    state: apiData.estado || "pendiente",
    demo: false,
    notas: apiData.notas || "",
    calificacion: apiData.calificacion
  });
}

async function loadItems() {
  try {
    const res = await fetch(`${API_BASE}/items`);
    if (res.ok) {
      const rawItems = await res.json();
      items = rawItems.map(apiToItem);
      render();
    }
  } catch (e) {
    console.error("Error cargando items", e);
  }
}

async function updateItemAPI(item) {
  try {
    await fetch(`${API_BASE}/items/${item.category}/${item.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        estado: item.state,
        notas: item.notas,
        calificacion: item.calificacion,
        volver_a_ver: item.volver_a_ver
      })
    });
  } catch (e) { console.error(e); }
}

async function deleteItemAPI(item) {
  try {
    await fetch(`${API_BASE}/items/${item.category}/${item.id}`, { method: "DELETE" });
  } catch (e) { console.error(e); }
}

function loadSettings() {
  try {
    return Object.assign({ view: "grid" }, JSON.parse(localStorage.getItem(LS_SETTINGS) || "{}"));
  } catch (e) {
    return { view: "grid" };
  }
}

function saveSettings() {
  localStorage.setItem(LS_SETTINGS, JSON.stringify(settings));
}

/* ------------------------------------------------------------------- dom */
const $ = (sel) => document.querySelector(sel);

const catMeta = (key) => CATEGORIES.find((c) => c.key === key) || CATEGORIES[0];

function renderRail() {
  const rail = $("#category-rail");
  rail.innerHTML = CATEGORIES.map((c) => `
    <button class="rail-pill" data-cat="${c.key}" aria-pressed="${c.key === activeCategory}" aria-label="${c.label}">
      ${ICONS[c.glyph]}<span>${c.label}</span>
    </button>`).join("");
  rail.querySelectorAll(".rail-pill").forEach((btn) => {
    btn.addEventListener("click", () => {
      activeCategory = btn.dataset.cat;
      renderRail();
      render();
    });
  });
}

function categoryCount(catKey) {
  const pool = items;
  if (catKey === "todo") return pool.length;
  return pool.filter((i) => i.category === catKey).length;
}

function filteredItems() {
  return items.filter((i) => {
    if (activeCategory !== "todo" && i.category !== activeCategory) return false;
    if (activeState !== "todos" && i.state !== activeState) return false;
    return true;
  });
}

function render() {
  const grid = $("#grid");
  const empty = $("#empty-state");
  const shown = filteredItems();

  if (shown.length === 0) {
    grid.innerHTML = "";
    empty.hidden = false;
    const meta = catMeta(activeCategory);
    empty.innerHTML = `
      <div class="empty-glyph">${ICONS[meta.glyph]}</div>
      <h2>${activeState === "todos" ? `Todavía no hay nada en ${activeCategory === "todo" ? "tu colección" : meta.label.toLowerCase()}` : `Sin ${STATE_LABELS[activeState].toLowerCase()}`}</h2>
      <p>${activeState === "todos"
        ? `Pegá una URL arriba o buscá un título: LazyList resuelve los metadatos y lo guarda con un solo gesto.`
        : `Ningún ítem de <strong>${meta.label}</strong> está marcado como <strong>${STATE_LABELS[activeState].toLowerCase()}</strong> todavía.`}</p>
      <button class="btn-primary" id="empty-add">${ICONS.plus}<span>Guardar algo</span></button>`;
    $("#empty-add").addEventListener("click", () => $("#capture-input").focus());
  } else {
    empty.hidden = true;
    grid.className = `grid-cards ${activeView === "list" ? "list" : ""}`;
    grid.innerHTML = shown.map(cardHTML).join("");
  }

  $("#count-label").textContent = `${shown.length} ${shown.length === 1 ? "ítem" : "ítems"}`;
  updateDemoNote();
}

function stateChipHTML(state) {
  return state && state !== "todos"
    ? `<span class="chip-state" data-state="${state}"><span class="dot"></span>${STATE_LABELS[state] || state}</span>`
    : "";
}

function fmtRating(r) {
  if (r == null) return "";
  return String(Math.round(r * 10) / 10).replace(".", ",");
}

function cardHTML(item) {
  const meta = catMeta(item.category);
  const ratingChip = item.calificacion
    ? `<span class="chip-rating">${ICONS.starSolid}<span>${fmtRating(item.calificacion)}</span></span>`
    : "";
  return `
    <article class="card" data-id="${item.id}" data-cat="${item.category}" tabindex="0" aria-label="Ver detalle de ${escapeHtml(item.title)}">
      <div class="card-cover" style="--cover:${meta.gradient}">
        <span class="card-cover-initial">${item.title.charAt(0)}</span>
        ${ICONS[meta.glyph]}
      </div>
      <div class="card-body">
        <div class="card-meta">
          <span class="chip">${meta.label}</span>
          ${stateChipHTML(item.state)}
          ${ratingChip}
        </div>
        <h3 class="card-title">${escapeHtml(item.title)}</h3>
        <div class="card-sub">${escapeHtml(item.subtitle || "")}</div>
        <div class="card-actions">
          <button class="mini-btn" data-act="state" title="Cambiar estado">
            <span class="dot" style="width:.42rem;height:.42rem;border-radius:999px;background:currentColor"></span>
            ${STATE_LABELS[item.state] || "Estado"}
          </button>
          <button class="mini-btn danger" data-act="delete" title="Eliminar">
            ${ICONS.trash}
          </button>
        </div>
      </div>
    </article>`;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (m) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));
}

function updateDemoNote() {
  $("#demo-hint").textContent = "Conectado a la base de datos local SQLite.";
}

/* ----------------------------------------------------------------- events */
$("#grid").addEventListener("click", async (e) => {
  const btn = e.target.closest("button[data-act]");
  if (!btn) return;
  const card = btn.closest(".card");
  const item = items.find((i) => i.id === card.dataset.id);
  if (!item) return;

  const act = btn.dataset.act;
  if (act === "state") {
    item.state = STATE_ORDER[(STATE_ORDER.indexOf(item.state) + 1) % STATE_ORDER.length];
    await updateItemAPI(item);
    render();
  } else if (act === "delete") {
    items = items.filter((i) => i.id !== item.id);
    await deleteItemAPI(item);
    render();
    toast("Ítem eliminado");
  }
});

$("#state-filter").addEventListener("click", (e) => {
  const btn = e.target.closest(".seg-btn");
  if (!btn) return;
  activeState = btn.dataset.state;
  $("#state-filter").querySelectorAll(".seg-btn").forEach((b) => b.setAttribute("aria-pressed", b === btn));
  render();
});

/* --- view toggle ---------------------------------------------------------- */
function setView(view) {
  activeView = view;
  settings.view = view;
  saveSettings();
  $("#view-grid").setAttribute("aria-pressed", view === "grid");
  $("#view-list").setAttribute("aria-pressed", view === "list");
  $("#views-segmented").querySelectorAll(".seg-btn").forEach((b) => b.setAttribute("aria-pressed", b.dataset.view === view));
  render();
}
$("#view-grid").addEventListener("click", () => setView("grid"));
$("#view-list").addEventListener("click", () => setView("list"));
$("#btn-open-views").addEventListener("click", () => $("#views-dialog").showModal());

/* --- settings dialog ------------------------------------------------------ */
$("#btn-settings").addEventListener("click", () => {
  $("#settings-dialog").showModal();
});
document.querySelectorAll("dialog .dialog-close, dialog [data-close]").forEach((b) => {
  b.addEventListener("click", () => b.closest("dialog").close());
});
document.querySelectorAll("dialog").forEach((d) => d.addEventListener("click", (e) => {
  if (e.target === d) d.close();
}));


$("#btn-clear-demo").addEventListener("click", () => {
  items = items.filter((i) => !i.demo);
  updateDemoNote();
  render();
  toast("Datos de ejemplo eliminados");
});

/* --- manual add dialog ---------------------------------------------------- */
let manualCategory = null;
let manualState = "pendiente";

function renderManualFields(category) {
  const container = $("#manual-dynamic-fields");
  if (!container) return;

  const fields = [];

  const addTextField = (name, label, placeholder, required = false) => {
    fields.push(`
      <div class="field">
        <label for="manual-f-${name}">${label}</label>
        <input id="manual-f-${name}" type="text" data-field="${name}" placeholder="${placeholder}" ${required ? "required" : ""}>
      </div>
    `);
  };

  const addNumberField = (name, label, placeholder, min = 0) => {
    fields.push(`
      <div class="field">
        <label for="manual-f-${name}">${label}</label>
        <input id="manual-f-${name}" type="number" data-field="${name}" placeholder="${placeholder}" min="${min}">
      </div>
    `);
  };

  if (category === "peliculas") {
    addTextField("original_title", "Título original", "Título en idioma original...");
    addTextField("director", "Director", "Director de la película...");
    addNumberField("duracion", "Duración", "Duración en minutos...");
    addTextField("release_date", "Lanzamiento", "Año o fecha de lanzamiento...");
  } else if (category === "series") {
    addTextField("original_title", "Título original", "Título en idioma original...");
    addTextField("plataform", "Plataforma", "Netflix, HBO Max, Prime Video...");
    addTextField("status", "Estado de emisión", "En emisión, Finalizada...");
    addTextField("premiered", "Estreno", "Año o fecha de estreno...");
  } else if (category === "anime") {
    addTextField("title_english", "Título en inglés", "English title...");
    addTextField("title_romaji", "Título romaji", "Romaji title...");
    addTextField("status", "Estado de emisión", "En emisión, Finalizado...");
    addNumberField("episodios", "Episodios", "Cantidad de episodios...");
  } else if (category === "mangas") {
    addTextField("title_english", "Título en inglés", "English title...");
    addTextField("title_romaji", "Título romaji", "Romaji title...");
    addTextField("autor", "Autor", "Nombre del mangaka...");
    addTextField("status", "Estado", "En publicación, Finalizado...");
    addNumberField("capitulos", "Capítulos", "Cantidad de capítulos...");
    addNumberField("year", "Año", "Año de publicación...");
  } else if (category === "comics") {
    addTextField("publisher", "Editorial", "DC, Marvel, Image...");
    addTextField("escritor", "Escritor", "Nombre del escritor/guionista...");
    addTextField("status", "Estado", "En publicación, Finalizado...");
    addNumberField("capitulos", "Capítulos", "Cantidad de capítulos/números...");
    addNumberField("year", "Año", "Año de publicación...");
  } else if (category === "novelas") {
    addTextField("escritor", "Escritor", "Nombre del escritor...");
    addTextField("status", "Estado", "En publicación, Finalizada...");
    addNumberField("capitulos", "Capítulos", "Cantidad de capítulos...");
    addNumberField("year", "Año", "Año de publicación...");
  } else if (category === "libros") {
    addTextField("autor", "Autor", "Nombre del autor...");
    addTextField("saga", "Saga", "Nombre de la saga (si aplica)...");
    addNumberField("orden", "Orden", "Número de orden en la saga...");
    addNumberField("ano", "Año", "Año de publicación...");
  } else if (category === "recursos") {
    addTextField("url", "Enlace (URL)", "https://ejemplo.com/recurso", true);
    addTextField("creado_autor", "Creado por", "Canal o autor del recurso...");
    fields.push(`
      <div class="field">
        <label>¿Volver a ver?</label>
        <div class="segmented" id="manual-f-volver_a_ver" role="group" aria-label="Volver a ver">
          <button type="button" class="seg-btn" data-val="true" aria-pressed="false">Sí</button>
          <button type="button" class="seg-btn" data-val="false" aria-pressed="true">No</button>
        </div>
      </div>
    `);
  } else if (category === "juegos") {
    addTextField("tienda", "Tienda", "Steam, Epic Games Store, GOG, Itch.io...");
    addTextField("mod", "Mod/Edición", "Edición Deluxe, Mods aplicados...");
  }

  container.innerHTML = fields.join("");

  const volverVerSeg = $("#manual-f-volver_a_ver");
  if (volverVerSeg) {
    volverVerSeg.addEventListener("click", (e) => {
      const btn = e.target.closest(".seg-btn");
      if (!btn) return;
      volverVerSeg.querySelectorAll(".seg-btn").forEach((b) => b.setAttribute("aria-pressed", b === btn));
    });
  }
}

function seedManualCategories() {
  const pick = activeCategory !== "todo" ? activeCategory : CATEGORIES[1].key;
  manualCategory = pick;
  const box = $("#manual-cats");
  box.innerHTML = CATEGORIES.filter((c) => c.key !== "todo").map((c) => `
    <button type="button" class="cat-pill" data-cat="${c.key}" aria-pressed="${c.key === pick}">
      ${ICONS[c.glyph]}<span>${c.label}</span>
    </button>`).join("");
  
  // Renderizar campos iniciales
  renderManualFields(pick);

  box.querySelectorAll(".cat-pill").forEach((b) => {
    b.addEventListener("click", () => {
      manualCategory = b.dataset.cat;
      box.querySelectorAll(".cat-pill").forEach((p) => p.setAttribute("aria-pressed", p === b));
      renderManualFields(manualCategory);
    });
  });
}

$("#btn-manual").addEventListener("click", () => {
  manualMode = "single";
  const modeTabs = $("#manual-mode-tabs");
  if (modeTabs) {
    modeTabs.querySelectorAll(".seg-btn").forEach((b) => {
      b.setAttribute("aria-pressed", b.dataset.mode === "single");
    });
  }
  $("#manual-single-fields").hidden = false;
  $("#manual-bulk-fields").hidden = true;

  seedManualCategories();
  $("#manual-state").querySelectorAll(".seg-btn").forEach((b) => b.setAttribute("aria-pressed", b.dataset.state === manualState));
  $("#manual-title-input").value = "";
  const bulkTextarea = $("#manual-bulk-textarea");
  if (bulkTextarea) bulkTextarea.value = "";
  $("#manual-dialog").showModal();
  $("#manual-title-input").focus();
});

$("#manual-state").addEventListener("click", (e) => {
  const btn = e.target.closest(".seg-btn");
  if (!btn) return;
  manualState = btn.dataset.state;
  $("#manual-state").querySelectorAll(".seg-btn").forEach((b) => b.setAttribute("aria-pressed", b === btn));
});

$("#manual-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  
  if (manualMode === "single") {
    const title = $("#manual-title-input").value.trim();
    if (!title) { $("#manual-title-input").focus(); return; }
    
    const extraFields = {};
    const container = $("#manual-dynamic-fields");
    if (container) {
      container.querySelectorAll("input[data-field]").forEach((inp) => {
        let val = inp.value.trim();
        if (val !== "") {
          if (inp.type === "number") {
            val = Number(val);
          }
          extraFields[inp.dataset.field] = val;
        }
      });
      const volverVerActive = container.querySelector("#manual-f-volver_a_ver .seg-btn[aria-pressed='true']");
      if (volverVerActive) {
        extraFields["volver_a_ver"] = volverVerActive.dataset.val === "true";
      }
    }

    const meta = catMeta(manualCategory);
    
    try {
        const res = await fetch(`${API_BASE}/items/manual`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                category: manualCategory, 
                titulo: title, 
                estado: manualState,
                fields: extraFields
            })
        });
        if (res.ok) {
            const data = await res.json();
            const item = apiToItem(data);
            items.push(item);
        }
    } catch (err) { console.error(err); }
    
    $("#manual-dialog").close();
    render();
    toast(`Guardado en ${meta.label}`);
  } else {
    const text = $("#manual-bulk-textarea").value.trim();
    if (!text) { $("#manual-bulk-textarea").focus(); return; }
    
    const rawLines = text.split("\n");
    const cleanedLines = rawLines.map((line) => {
      return line.trim()
        .replace(/^[\s\-*•\d\.)]+/, "") // Limpia guiones, viñetas y números iniciales
        .trim();
    }).filter(Boolean);
    
    // Deduplicar en el lote usando un Set (insensible a mayúsculas/minúsculas)
    const seen = new Set();
    const uniqueLines = [];
    for (const line of cleanedLines) {
      const lower = line.toLowerCase();
      if (!seen.has(lower)) {
        seen.add(lower);
        uniqueLines.push(line);
      }
    }
    
    if (uniqueLines.length === 0) { $("#manual-bulk-textarea").focus(); return; }
    
    const meta = catMeta(bulkCategory);
    
    try {
        const res = await fetch(`${API_BASE}/items/bulk`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                category: bulkCategory, 
                estado: manualState,
                items: uniqueLines
            })
        });
        if (res.ok) {
            const dataList = await res.json();
            dataList.forEach((data) => {
                items.push(apiToItem(data));
            });
        }
    } catch (err) { console.error(err); }
    
    $("#manual-dialog").close();
    render();
    toast(`Guardados ${cleanedLines.length} ítems en ${meta.label}`);
  }
});

/* --- detail dialog -------------------------------------------------------- */
let detailItem = null;
let notesTimer;
let notesHintTimer;

function renderEditorialFields(item) {
  const rows = [];
  const addRow = (label, val, isLink = false) => {
    if (val === null || val === undefined || val === "" || (Array.isArray(val) && val.length === 0)) return;
    const displayVal = Array.isArray(val) ? val.join(", ") : val;
    if (isLink) {
      rows.push(`<div class="prow"><span class="prow-k">${label}</span><span class="prow-v"><a href="${escapeHtml(val)}" target="_blank" rel="noopener noreferrer" style="color:var(--color-violet);text-decoration:underline;word-break:break-all">${escapeHtml(val)}</a></span></div>`);
    } else {
      rows.push(`<div class="prow"><span class="prow-k">${label}</span><span class="prow-v">${escapeHtml(displayVal)}</span></div>`);
    }
  };

  const cat = item.category;

  if (cat === "peliculas") {
    addRow("Título original", item.original_title);
    addRow("Director", item.director);
    addRow("Duración", item.duracion ? `${item.duracion} min` : null);
    addRow("Lanzamiento", item.release_date);
    addRow("País de origen", item.origin_country);
    addRow("Géneros", item.genre);
  } else if (cat === "series" || cat === "series_tvmaze") {
    addRow("Título original", item.original_title);
    addRow("Plataforma", item.plataform);
    addRow("Estado", item.status);
    addRow("Estreno", item.premiered);
    addRow("Fin", item.ended);
    addRow("País de origen", item.origin_country);
    addRow("Géneros", item.genre);
  } else if (cat === "anime") {
    addRow("Título en inglés", item.title_english);
    addRow("Título romaji", item.title_romaji);
    addRow("Estado", item.status);
    addRow("Episodios", item.episodios);
    addRow("Estreno", item.premiered);
    addRow("Fin", item.ended);
    addRow("Géneros", item.genre);
  } else if (cat === "mangas") {
    addRow("Título en inglés", item.title_english);
    addRow("Título romaji", item.title_romaji);
    addRow("Autor", item.autor);
    addRow("Estado", item.status);
    addRow("Capítulos", item.capitulos);
    addRow("Año", item.year);
  } else if (cat === "comics") {
    addRow("Editorial", item.publisher);
    addRow("Escritor", item.escritor);
    addRow("Estado", item.status);
    addRow("Capítulos", item.capitulos);
    addRow("Año", item.year);
  } else if (cat === "novelas") {
    addRow("Escritor", item.escritor);
    addRow("Estado", item.status);
    addRow("Capítulos", item.capitulos);
    addRow("Año", item.year);
    addRow("Géneros", item.genero);
  } else if (cat === "libros") {
    addRow("Autor", item.autor);
    addRow("Saga", item.saga);
    addRow("Orden", item.orden);
    addRow("Año", item.ano);
    addRow("Géneros", item.genero);
  } else if (cat === "recursos") {
    addRow("Enlace (URL)", item.url, true);
    addRow("Creado por", item.creado_autor);
    if (item.volver_a_ver !== undefined && item.volver_a_ver !== null) {
      addRow("Volver a ver", item.volver_a_ver ? "Sí" : "No");
    }
  } else if (cat === "juegos") {
    addRow("Tienda", item.tienda);
    addRow("Mod/Edición", item.mod);
  }

  const container = $("#detail-editorial-rows");
  const panel = $("#detail-editorial-panel");
  if (rows.length === 0) {
    panel.hidden = true;
    container.innerHTML = "";
  } else {
    panel.hidden = false;
    container.innerHTML = rows.join("");
  }
}

function openDetail(item) {
  if ($("#detail-dialog").open) return;
  detailItem = item;
  const meta = catMeta(item.category);
  $("#detail-cover").style.setProperty("--cover", meta.gradient);
  $("#detail-cover-initial").textContent = item.title.charAt(0);
  $("#detail-cover-glyph").innerHTML = ICONS[meta.glyph];
  $("#detail-title-text").textContent = item.title;
  $("#detail-sub").textContent = item.subtitle || "";
  $("#detail-chip").textContent = meta.label;
  $("#detail-state-chip").innerHTML = stateChipHTML(item.state);
  
  // Renderizar campos dinámicos de la categoría
  renderEditorialFields(item);

  // Mostrar/ocultar controles adicionales para Recursos (volver a ver)
  if (item.category === "recursos") {
    $("#detail-recurso-divider").hidden = false;
    $("#detail-recurso-fields").hidden = false;
    const volverVer = item.volver_a_ver === true;
    $("#detail-volver-ver").querySelectorAll(".seg-btn").forEach((btn) => {
      btn.setAttribute("aria-pressed", (btn.dataset.val === "true") === volverVer);
    });
  } else {
    $("#detail-recurso-divider").hidden = true;
    $("#detail-recurso-fields").hidden = true;
  }

  // Configurar panel de enriquecimiento
  const ENRICH_SUPPORTED = ["peliculas", "series", "anime", "mangas", "comics", "libros", "recursos"];
  const canEnrich = item.id.startsWith("manual_") && ENRICH_SUPPORTED.includes(item.category);
  const enrichPanel = $("#detail-enrich-panel");
  if (enrichPanel) {
    enrichPanel.hidden = !canEnrich;
    $("#detail-enrich-search-box").hidden = true;
    $("#detail-enrich-query").value = item.title;
    $("#detail-enrich-results").innerHTML = "";
  }

  const stores = (item.tienda || "").split(",").map((s) => s.trim()).filter(Boolean);
  const storesBox = $(".dialog-body .detail-stores");
  if (storesBox) {
    storesBox.innerHTML = stores.map((s) => `<span class="store-chip">${ICONS.tag}${escapeHtml(s)}</span>`).join("");
    storesBox.hidden = stores.length === 0;
  }
  $("#detail-notes").value = item.notas || "";
  $("#detail-notes-hint").textContent = "";
  $("#detail-state").querySelectorAll(".seg-btn").forEach((b) => b.setAttribute("aria-pressed", b.dataset.state === item.state));
  renderStars(item.calificacion);
  detailRatingReadout();
  $("#detail-dialog").showModal();
}

function renderStars(rating) {
  const box = $("#detail-stars");
  box.innerHTML = [1, 2, 3, 4, 5].map((i) => {
    const fill = Math.min(Math.max(rating == null ? 0 : rating - (i - 1), 0), 1);
    return `<button type="button" class="star-btn" data-value="${i}" aria-label="${i} de 5" aria-pressed="${fill >= 0.5}">
      <span class="star">
        ${ICONS.star}
        <svg class="star-full" viewBox="0 0 24 24" fill="currentColor" style="clip-path:inset(0 ${(100 - fill * 100).toFixed(2)}% 0 0)"><path d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.562.562 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.562.562 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z"/></svg>
      </span>
    </button>`;
  }).join("");
  box.querySelectorAll(".star-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      if (e.detail === 0) return;
      const i = Number(btn.dataset.value);
      const rect = btn.querySelector(".star").getBoundingClientRect();
      setRating(e.clientX - rect.left < rect.width / 2 ? i - 0.5 : i, i);
    });
  });
}

$("#detail-stars").addEventListener("keydown", (e) => {
  if (!detailItem || (e.key !== "Enter" && e.key !== " ")) return;
  const btn = e.target.closest(".star-btn");
  if (!btn) return;
  e.preventDefault();
  const i = Number(btn.dataset.value);
  setRating(e.shiftKey ? i - 0.5 : i, i);
});

function setRating(val, focusIndex) {
  detailItem.calificacion = val;
  updateItemAPI(detailItem);
  renderStars(val);
  detailRatingReadout();
  render();
  if (focusIndex) {
    const next = $("#detail-stars").querySelector(`.star-btn[data-value="${focusIndex}"]`);
    if (next) next.focus();
  }
}

function detailRatingReadout() {
  const r = detailItem.calificacion;
  $("#detail-rating-value").textContent = r == null ? "Sin calificar" : `${fmtRating(r)} / 5`;
  $("#detail-rating-clear").hidden = r == null;
  $("#detail-rating-chip").hidden = r == null;
  if (r != null) $("#detail-rating-chip").innerHTML = `${ICONS.starSolid}<span>${fmtRating(r)}</span>`;
}

$("#detail-rating-clear").addEventListener("click", () => {
  if (!detailItem) return;
  detailItem.calificacion = null;
  updateItemAPI(detailItem);
  renderStars(null);
  detailRatingReadout();
  render();
});

$("#detail-notes").addEventListener("input", () => {
  if (!detailItem) return;
  clearTimeout(notesTimer);
  notesTimer = setTimeout(async () => {
    detailItem.notas = $("#detail-notes").value;
    await updateItemAPI(detailItem);
    const hint = $("#detail-notes-hint");
    hint.textContent = "Guardado en DB";
    clearTimeout(notesHintTimer);
    notesHintTimer = setTimeout(() => { hint.textContent = ""; }, 1600);
  }, 350);
});

$("#detail-dialog").addEventListener("close", () => {
  if (detailItem && $("#detail-notes").value !== (detailItem.notas || "")) {
    detailItem.notas = $("#detail-notes").value;
    updateItemAPI(detailItem);
  }
  detailItem = null;
});

$("#detail-state").addEventListener("click", async (e) => {
  if (!detailItem) return;
  const btn = e.target.closest(".seg-btn");
  if (!btn) return;
  detailItem.state = btn.dataset.state;
  await updateItemAPI(detailItem);
  $("#detail-state").querySelectorAll(".seg-btn").forEach((b) => b.setAttribute("aria-pressed", b === btn));
  render();
});

$("#detail-volver-ver").addEventListener("click", async (e) => {
  if (!detailItem) return;
  const btn = e.target.closest(".seg-btn");
  if (!btn) return;
  const val = btn.dataset.val === "true";
  detailItem.volver_a_ver = val;
  await updateItemAPI(detailItem);
  $("#detail-volver-ver").querySelectorAll(".seg-btn").forEach((b) => b.setAttribute("aria-pressed", b === btn));
  renderEditorialFields(detailItem);
  render();
});

$("#detail-delete").addEventListener("click", async () => {
  if (!detailItem) return;
  items = items.filter((i) => i.id !== detailItem.id);
  await deleteItemAPI(detailItem);
  $("#detail-dialog").close();
  render();
  toast("Ítem eliminado");
});

let bulkCategory = null;
function seedBulkCategories() {
  const pick = activeCategory !== "todo" ? activeCategory : CATEGORIES[1].key;
  bulkCategory = pick;
  const box = $("#manual-bulk-cats");
  if (!box) return;
  box.innerHTML = CATEGORIES.filter((c) => c.key !== "todo").map((c) => `
    <button type="button" class="cat-pill" data-cat="${c.key}" aria-pressed="${c.key === pick}">
      ${ICONS[c.glyph]}<span>${c.label}</span>
    </button>`).join("");
  box.querySelectorAll(".cat-pill").forEach((b) => {
    b.addEventListener("click", () => {
      bulkCategory = b.dataset.cat;
      box.querySelectorAll(".cat-pill").forEach((p) => p.setAttribute("aria-pressed", p === b));
    });
  });
}

let manualMode = "single";
const modeTabs = $("#manual-mode-tabs");
if (modeTabs) {
  modeTabs.addEventListener("click", (e) => {
    const btn = e.target.closest(".seg-btn");
    if (!btn) return;
    manualMode = btn.dataset.mode;
    modeTabs.querySelectorAll(".seg-btn").forEach((b) => b.setAttribute("aria-pressed", b === btn));
    if (manualMode === "single") {
      $("#manual-single-fields").hidden = false;
      $("#manual-bulk-fields").hidden = true;
    } else {
      $("#manual-single-fields").hidden = true;
      $("#manual-bulk-fields").hidden = false;
      seedBulkCategories();
    }
  });
}

const enrichToggle = $("#detail-enrich-toggle");
if (enrichToggle) {
  enrichToggle.addEventListener("click", () => {
    const box = $("#detail-enrich-search-box");
    if (box) box.hidden = !box.hidden;
  });
}

async function runEnrichSearch() {
  const query = $("#detail-enrich-query").value.trim();
  if (!query || !detailItem) return;
  const resultsBox = $("#detail-enrich-results");
  if (!resultsBox) return;
  resultsBox.innerHTML = `<div class="prow" style="justify-content:center"><span class="prow-v">Buscando...</span></div>`;
  
  try {
    const res = await fetch(`${API_BASE}/search?q=${encodeURIComponent(query)}&category=${detailItem.category}`);
    if (res.ok) {
      const results = await res.json();
      if (results.length === 0) {
        resultsBox.innerHTML = `<div class="prow" style="justify-content:center"><span class="prow-v">Sin resultados.</span></div>`;
        return;
      }
      resultsBox.innerHTML = results.map((r) => {
        const yearText = r.year ? ` (${r.year})` : "";
        return `
          <button type="button" class="prow" data-api-id="${r.api_id}" style="text-align: left; width: 100%; border: 0; background: transparent; cursor: pointer; padding: 0.6rem 0.4rem; display: block; border-radius: 8px;">
            <span class="prow-v" style="font-weight: 700; color: var(--color-ink);">${escapeHtml(r.title)}${escapeHtml(yearText)}</span>
            <p style="font-size: 0.72rem; color: var(--color-ink-3); margin-top: 0.15rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%;">${escapeHtml(r.overview || "")}</p>
          </button>
        `;
      }).join("");
      
      resultsBox.querySelectorAll("button").forEach((btn) => {
        btn.addEventListener("click", () => selectEnrichMatch(btn.dataset.apiId));
      });
    } else {
      resultsBox.innerHTML = `<div class="prow" style="justify-content:center"><span class="prow-v" style="color:var(--color-rose)">Error en la búsqueda.</span></div>`;
    }
  } catch (err) {
    console.error(err);
    resultsBox.innerHTML = `<div class="prow" style="justify-content:center"><span class="prow-v" style="color:var(--color-rose)">Error de red.</span></div>`;
  }
}

async function selectEnrichMatch(apiId) {
  if (!detailItem) return;
  const resultsBox = $("#detail-enrich-results");
  if (resultsBox) {
    resultsBox.innerHTML = `<div class="prow" style="justify-content:center"><span class="prow-v">Vinculando metadatos...</span></div>`;
  }
  
  try {
    const res = await fetch(`${API_BASE}/items/enrich`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        category: detailItem.category,
        id: detailItem.id,
        api_id: apiId
      })
    });
    if (res.ok) {
      const updatedData = await res.json();
      const enrichedItem = apiToItem(updatedData);
      
      const index = items.findIndex((i) => i.id === detailItem.id);
      if (index !== -1) {
        items[index] = enrichedItem;
      }
      
      detailItem = enrichedItem;
      
      const enrichPanel = $("#detail-enrich-panel");
      if (enrichPanel) enrichPanel.hidden = true;
      $("#detail-title-text").textContent = enrichedItem.title;
      $("#detail-sub").textContent = enrichedItem.subtitle || "";
      renderEditorialFields(enrichedItem);
      render();
      toast("Metadatos vinculados correctamente");
    } else {
      toast("Error al vincular metadatos");
      if (resultsBox) resultsBox.innerHTML = "";
    }
  } catch (err) {
    console.error(err);
    toast("Error de red al vincular");
    if (resultsBox) resultsBox.innerHTML = "";
  }
}

const enrichSearchBtn = $("#detail-enrich-search-btn");
if (enrichSearchBtn) {
  enrichSearchBtn.addEventListener("click", runEnrichSearch);
}
const enrichQueryInput = $("#detail-enrich-query");
if (enrichQueryInput) {
  enrichQueryInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      runEnrichSearch();
    }
  });
}

$("#grid").addEventListener("click", (e) => {
  if (e.target.closest("button[data-act]")) return;
  const card = e.target.closest(".card");
  if (!card) return;
  const item = items.find((i) => i.id === card.dataset.id);
  if (item) openDetail(item);
});

$("#grid").addEventListener("keydown", (e) => {
  if ((e.key === "Enter" || e.key === " ") && e.target.classList.contains("card")) {
    e.preventDefault();
    const item = items.find((i) => i.id === e.target.dataset.id);
    if (item) openDetail(item);
  }
});

/* --- capture -------------------------------------------------------------- */
$("#capture-cat-btn").addEventListener("click", (e) => {
  e.stopPropagation();
  const btn = $("#capture-cat-btn");
  const open = btn.getAttribute("aria-expanded") === "true";
  closeResults();
  if (open) { btn.setAttribute("aria-expanded", "false"); return; }

  const opts = CATEGORIES.filter((c) => c.key === "todo" || SEARCHABLE.includes(c.key));
  const box = $("#capture-results");
  box.hidden = false;
  box.innerHTML = opts.map((c) => `
    <button class="result-row" data-cat-pick="${c.key}" role="option">
      <span class="result-cover" style="--cover:${c.gradient}">${ICONS[c.glyph]}</span>
      <span style="flex:1"><span class="result-title">${c.label}</span></span>
      <span class="result-year">${categoryCount(c.key)}</span>
    </button>`).join("");
  box.querySelectorAll("[data-cat-pick]").forEach((r) => {
    r.addEventListener("click", () => {
      captureCategory = r.dataset.catPick;
      $("#capture-cat-label").textContent = catMeta(captureCategory).label;
      btn.setAttribute("aria-expanded", "false");
      closeResults();
      $("#capture-input").focus();
    });
  });
  btn.setAttribute("aria-expanded", "true");
});

$("#capture-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const input = $("#capture-input").value.trim();
  if (!input) { $("#capture-input").focus(); return; }

  const isUrl = /^https?:\/\//i.test(input);
  const category = isUrl ? "recursos" : (captureCategory === "todo" ? null : captureCategory);

  if (category === null) {
    showCategoryPick(input);
    return;
  }

  setBusy(true);
  closeResults();
  try {
    const res = await fetch(`${API_BASE}/search?q=${encodeURIComponent(input)}&category=${category}`);
    if (!res.ok) throw new Error((await res.json()).detail || "Error de búsqueda");
    const results = await res.json();
    if (results.length === 0) {
      showResults(`<div class="results-empty">Sin resultados. Podés cargarlo a mano.</div>`);
      return;
    }
    renderResults(results, category, input);
  } catch (err) {
    showResults(`<div class="results-error">${ICONS.warn}<span style="display:inline-block;vertical-align:middle">${escapeHtml(err.message)}</span></div>`);
  } finally {
    setBusy(false);
  }
});

function showCategoryPick(query) {
  const box = $("#capture-results");
  box.hidden = false;
  box.innerHTML = `<div class="results-empty">¿Dónde buscamos “${escapeHtml(query)}”?</div>` +
    SEARCHABLE.map((key) => {
      const c = catMeta(key);
      return `<button class="result-row" data-pick="${key}" role="option">
        <span class="result-cover" style="--cover:${c.gradient}">${ICONS[c.glyph]}</span>
        <span style="flex:1"><span class="result-title">${c.label}</span></span>
      </button>`;
    }).join("");
  box.querySelectorAll("[data-pick]").forEach((r) => {
    r.addEventListener("click", async () => {
      captureCategory = r.dataset.pick;
      $("#capture-cat-label").textContent = catMeta(captureCategory).label;
      closeResults();
      await runSearch(query, captureCategory);
    });
  });
}

async function runSearch(input, category) {
  setBusy(true);
  try {
    const res = await fetch(`${API_BASE}/search?q=${encodeURIComponent(input)}&category=${category}`);
    if (!res.ok) throw new Error((await res.json()).detail || "Error de búsqueda");
    const results = await res.json();
    if (results.length === 0) {
      showResults(`<div class="results-empty">Sin resultados en ${catMeta(category).label}. Podés cargarlo a mano.</div>`);
      return;
    }
    renderResults(results, category, input);
  } catch (err) {
    showResults(`<div class="results-error">${ICONS.warn}<span style="display:inline-block;vertical-align:middle">${escapeHtml(err.message)}</span></div>`);
  } finally {
    setBusy(false);
  }
}

function renderResults(results, category, query) {
  const box = $("#capture-results");
  box.hidden = false;
  const meta = catMeta(category);
  box.innerHTML = results.map((r, idx) => `
    <button class="result-row" data-save="${escapeHtml(r.api_id)}" role="option" aria-selected="${idx === 0}">
      <span class="result-cover" style="--cover:${meta.gradient}">${ICONS[meta.glyph]}</span>
      <span style="flex:1">
        <span class="result-title">${escapeHtml(r.title)}</span>
        <div class="result-year">${r.year ? escapeHtml(r.year) + " · " : ""}${escapeHtml((r.overview || "").slice(0, 120))}</div>
      </span>
      ${ICONS.plusBadge}
    </button>`).join("");
  box.querySelectorAll("[data-save]").forEach((row) => {
    row.addEventListener("click", async () => await savePicked(row.dataset.save, category, query));
  });
}

async function savePicked(apiId, category, query) {
  setBusy(true);
  try {
    const res = await fetch(`${API_BASE}/save`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ api_id: apiId, category }),
    });
    if (!res.ok) throw new Error((await res.json()).detail || "No se pudo guardar");
    const saved = await res.json();
    saved.category = category;
    const item = apiToItem(saved);
    items.push(item);
    closeResults();
    $("#capture-input").value = "";
    render();
    const meta = catMeta(category);
    toast(`Guardado en ${meta.label}`);
  } catch (err) {
    toast(`No se pudo guardar: ${err.message}`);
  } finally {
    setBusy(false);
  }
}

function subtitleFor(saved, category) {
  const parts = [];
  if (category === "peliculas") {
    if (saved.director) parts.push(saved.director);
    if (saved.release_date) parts.push(String(saved.release_date).split("-")[0]);
    if (saved.duracion) parts.push(`${saved.duracion} min`);
    if (saved.genre && saved.genre.length) parts.push(saved.genre.slice(0, 2).join(", "));
  } else if (category === "series") {
    if (saved.status) parts.push(saved.status);
    if (saved.premiered) parts.push(String(saved.premiered).split("-")[0]);
    if (saved.genre && saved.genre.length) parts.push(saved.genre.slice(0, 2).join(", "));
  } else if (category === "anime") {
    if (saved.episodios) parts.push(`${saved.episodios} episodios`);
    if (saved.status) parts.push(saved.status);
    if (saved.genre && saved.genre.length) parts.push(saved.genre.slice(0, 2).join(", "));
  } else if (category === "mangas") {
    if (saved.autor) parts.push(saved.autor);
    if (saved.capitulos) parts.push(`${saved.capitulos} capítulos`);
    if (saved.year) parts.push(String(saved.year));
  } else if (category === "libros") {
    if (saved.autor) parts.push(saved.autor);
    if (saved.ano) parts.push(String(saved.ano));
    if (saved.genero && saved.genero.length) parts.push(saved.genero.slice(0, 2).join(", "));
  } else if (category === "comics") {
    if (saved.publisher) parts.push(saved.publisher);
    if (saved.year) parts.push(String(saved.year));
    if (saved.escritor) parts.push(saved.escritor);
  }
  return parts.join(" · ");
}

/* --- results helpers ------------------------------------------------------ */
function showResults(html) {
  const box = $("#capture-results");
  box.hidden = false;
  box.innerHTML = html;
}

function closeResults() {
  $("#capture-results").hidden = true;
}

function setBusy(busy) {
  $("#capture-go-label").textContent = busy ? "Buscando…" : "Guardar";
}

document.addEventListener("click", (e) => {
  if (!e.target.closest("#capture-shell")) closeResults();
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") { closeResults(); $("#capture-cat-btn").setAttribute("aria-expanded", "false"); }
});

/* --- toast ---------------------------------------------------------------- */
let toastTimer;
function toast(msg) {
  const t = $("#toast");
  t.innerHTML = `${ICONS.check}<span>${escapeHtml(msg)}</span>`;
  t.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove("show"), 2600);
}

/* --- boot ---------------------------------------------------------------- */
renderRail();
loadItems();

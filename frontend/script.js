/**
 * Gestion École - Frontend principal (liste étudiants)
 */
const API = "http://127.0.0.1:8001/api/v1";

// État
let state = {
  page: 1,
  limit: 15,
  search: "",
  classe: "",
  source: "",
  archive: false,
  editNumero: null,
};

// DOM
const tableBody = document.getElementById("tableBody");
const paginationInfo = document.getElementById("paginationInfo");
const paginationBtns = document.getElementById("paginationBtns");
const searchInput = document.getElementById("searchInput");
const filterClasse = document.getElementById("filterClasse");
const filterSource = document.getElementById("filterSource");
const filterArchive = document.getElementById("filterArchive");
const listePanel = document.getElementById("listePanel");
const detailPanel = document.getElementById("detailPanel");
const bulletinContent = document.getElementById("bulletinContent");
const modalOverlay = document.getElementById("modalOverlay");
const formEtudiant = document.getElementById("formEtudiant");
const modalTitle = document.getElementById("modalTitle");

// ========== Utils ==========
function toast(msg, type = "success") {
  const container = document.getElementById("toastContainer");
  const el = document.createElement("div");
  el.className = `toast ${type}`;
  el.textContent = msg;
  container.appendChild(el);
  setTimeout(() => el.remove(), 3500);
}

function formatDate(d) {
  if (!d) return "—";
  try {
    return new Date(d).toLocaleDateString("fr-FR");
  } catch {
    return d;
  }
}

// ========== API ==========
async function fetchEtudiants() {
  const params = new URLSearchParams({
    page: state.page,
    limit: state.limit,
    archive: state.archive,
  });
  if (state.search) params.set("search", state.search);
  if (state.classe) params.set("classe", state.classe);
  if (state.source) params.set("source", state.source);

  const res = await fetch(`${API}/etudiants?${params}`);
  if (!res.ok) throw new Error("Erreur chargement étudiants");
  return res.json();
}

async function fetchDetail(numero) {
  const res = await fetch(`${API}/etudiants/${numero}`);
  if (!res.ok) throw new Error("Étudiant non trouvé");
  return res.json();
}

// ========== Rendu liste ==========
function renderTable(data) {
  if (!data || data.length === 0) {
    tableBody.innerHTML = `
      <tr><td colspan="9">
        <div class="empty-state">
          <div class="icon">📭</div>
          <div>Aucun étudiant trouvé</div>
        </div>
      </td></tr>`;
    return;
  }

  tableBody.innerHTML = data
    .map(
      (e, i) => `
    <tr>
      <td>${(state.page - 1) * state.limit + i + 1}</td>
      <td><strong>${e.numero}</strong></td>
      <td>${e.nom}</td>
      <td>${e.prenom}</td>
      <td>${formatDate(e.date_naissance)}</td>
      <td>${e.classe || "—"}</td>
      <td>${e.user_at || "—"}</td>
      <td>
        <span class="badge ${e.source === "JSON" ? "badge-json" : "badge-db"}">
          ${e.source || "DB"}
        </span>
        ${e.archive ? '<span class="badge badge-archive">Archivé</span>' : ""}
      </td>
      <td>
        <div class="actions">
          <button class="btn btn-outline btn-sm" onclick="voirDetail('${e.numero}')">Détail</button>
          <button class="btn btn-outline btn-sm" onclick="ouvrirEdit('${e.numero}')">Édit</button>
          <button class="btn ${e.archive ? "btn-success" : "btn-warning"} btn-sm"
            onclick="toggleArchive('${e.numero}', ${!e.archive})">
            ${e.archive ? "Restaurer" : "Archiver"}
          </button>
        </div>
      </td>
    </tr>`
    )
    .join("");
}

function renderPagination(total, pages) {
  paginationInfo.textContent = `Page ${state.page} / ${pages || 1} — ${total} étudiant(s)`;

  let html = "";
  html += `<button ${state.page <= 1 ? "disabled" : ""} onclick="goPage(${state.page - 1})">‹</button>`;

  const maxVisible = 5;
  let start = Math.max(1, state.page - Math.floor(maxVisible / 2));
  let end = Math.min(pages, start + maxVisible - 1);
  start = Math.max(1, end - maxVisible + 1);

  for (let p = start; p <= end; p++) {
    html += `<button class="${p === state.page ? "active" : ""}" onclick="goPage(${p})">${p}</button>`;
  }

  html += `<button ${state.page >= pages ? "disabled" : ""} onclick="goPage(${state.page + 1})">›</button>`;
  paginationBtns.innerHTML = html;
}

async function loadData() {
  try {
    tableBody.innerHTML = `<tr><td colspan="9" class="loading"><div class="spinner"></div>Chargement…</td></tr>`;
    const res = await fetchEtudiants();
    renderTable(res.data);
    renderPagination(res.total, res.pages);

    // Remplir filtre classes (une seule fois)
    if (filterClasse.options.length <= 1 && res.data.length) {
      const classes = [...new Set(res.data.map((e) => e.classe).filter(Boolean))].sort();
      classes.forEach((c) => {
        const opt = document.createElement("option");
        opt.value = c;
        opt.textContent = c;
        filterClasse.appendChild(opt);
      });
    }
  } catch (err) {
    tableBody.innerHTML = `<tr><td colspan="9" class="empty-state">
      <div class="icon">⚠️</div>
      <div>Impossible de contacter l'API<br><small>${err.message}</small></div>
      <div class="mt-2 text-muted">Vérifiez que le backend tourne sur le port 8000</div>
    </td></tr>`;
    toast("Erreur de connexion à l'API", "error");
  }
}

function goPage(p) {
  state.page = p;
  loadData();
}

// ========== Détail ==========
window.voirDetail = async function (numero) {
  try {
    const etu = await fetchDetail(numero);
    listePanel.classList.add("hidden");
    detailPanel.classList.add("show");

    let notesHtml = "";
    if (etu.notes && etu.notes.length) {
      notesHtml = `
        <div class="notes-table">
          <h3>Bulletin de notes</h3>
          <table>
            <thead>
              <tr>
                <th>Matière</th>
                <th>Notes devoirs</th>
                <th>Examen</th>
                <th>Moyenne</th>
              </tr>
            </thead>
            <tbody>
              ${etu.notes
                .map(
                  (n) => `
                <tr>
                  <td><strong>${n.matiere}</strong></td>
                  <td>${n.note_devoirs?.map((d) => d.toFixed(1)).join(" - ") || "—"}</td>
                  <td>${n.note_examen != null ? n.note_examen.toFixed(1) : "—"}</td>
                  <td><strong>${n.moyenne != null ? n.moyenne.toFixed(2) : "—"}</strong></td>
                </tr>`
                )
                .join("")}
            </tbody>
          </table>
        </div>`;
    } else {
      notesHtml = `<div class="notes-table"><p class="text-muted">Aucune note enregistrée</p></div>`;
    }

    bulletinContent.innerHTML = `
      <div class="bulletin-header">
        <div>
          <h2>${etu.prenom} ${etu.nom}</h2>
          <div style="opacity:0.85; font-size:0.95rem;">N° ${etu.numero}</div>
        </div>
        <span class="badge ${etu.source === "JSON" ? "badge-json" : "badge-db"}" style="font-size:0.85rem;">
          ${etu.source || "DB"}
        </span>
      </div>
      <div class="bulletin-meta">
        <div class="meta-item">
          <div class="label">Classe</div>
          <div class="value">${etu.classe || "—"}</div>
        </div>
        <div class="meta-item">
          <div class="label">Date de naissance</div>
          <div class="value">${formatDate(etu.date_naissance)}</div>
        </div>
        <div class="meta-item">
          <div class="label">Code utilisateur</div>
          <div class="value">${etu.user_at || "—"}</div>
        </div>
        <div class="meta-item">
          <div class="label">Statut</div>
          <div class="value">${etu.archive ? "Archivé" : "Actif"}</div>
        </div>
      </div>
      ${notesHtml}
    `;
  } catch (err) {
    toast(err.message, "error");
  }
};

document.getElementById("btnRetour").addEventListener("click", () => {
  detailPanel.classList.remove("show");
  listePanel.classList.remove("hidden");
});

// ========== Archive ==========
window.toggleArchive = async function (numero, archive) {
  try {
    const res = await fetch(`${API}/etudiants/${numero}/archiver?archive=${archive}`, {
      method: "PATCH",
    });
    if (!res.ok) throw new Error("Échec");
    toast(archive ? "Étudiant archivé" : "Étudiant restauré");
    loadData();
  } catch {
    toast("Erreur lors de l'archivage", "error");
  }
};

// ========== Modal ==========
function openModal(edit = false) {
  modalTitle.textContent = edit ? "Modifier l'étudiant" : "Ajouter un étudiant";
  modalOverlay.classList.add("show");
  if (!edit) {
    formEtudiant.reset();
    document.getElementById("numero").disabled = false;
    state.editNumero = null;
  }
}

function closeModal() {
  modalOverlay.classList.remove("show");
  state.editNumero = null;
}

document.getElementById("btnAjouter").addEventListener("click", () => openModal(false));
document.getElementById("modalClose").addEventListener("click", closeModal);
document.getElementById("btnAnnuler").addEventListener("click", closeModal);
modalOverlay.addEventListener("click", (e) => {
  if (e.target === modalOverlay) closeModal();
});

window.ouvrirEdit = async function (numero) {
  try {
    const etu = await fetchDetail(numero);
    state.editNumero = numero;
    document.getElementById("numero").value = etu.numero;
    document.getElementById("numero").disabled = true;
    document.getElementById("nom").value = etu.nom;
    document.getElementById("prenom").value = etu.prenom;
    document.getElementById("date_naissance").value = etu.date_naissance;
    document.getElementById("user_at").value = etu.user_at;
    document.getElementById("classe").value = etu.classe;
    openModal(true);
  } catch {
    toast("Impossible de charger l'étudiant", "error");
  }
};

formEtudiant.addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    numero: document.getElementById("numero").value.trim().toUpperCase(),
    nom: document.getElementById("nom").value.trim(),
    prenom: document.getElementById("prenom").value.trim(),
    date_naissance: document.getElementById("date_naissance").value,
    user_at: document.getElementById("user_at").value.trim().toUpperCase(),
    classe: document.getElementById("classe").value.trim(),
    source: "DB",
  };

  try {
    let res;
    if (state.editNumero) {
      // Update
      const { numero, source, ...updateData } = payload;
      res = await fetch(`${API}/etudiants/${state.editNumero}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updateData),
      });
    } else {
      res = await fetch(`${API}/etudiants`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    }

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Erreur serveur");
    }

    toast(state.editNumero ? "Étudiant modifié" : "Étudiant ajouté");
    closeModal();
    loadData();
  } catch (err) {
    toast(err.message, "error");
  }
});

// ========== Import JSON ==========
document.getElementById("btnImport").addEventListener("click", async () => {
  if (!confirm("Importer les données du fichier JSON validé ?\nLes doublons seront ignorés.")) return;
  try {
    toast("Import en cours…", "warning");
    const res = await fetch(`${API}/import/json`, { method: "POST" });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Erreur import");
    toast(`Import terminé : ${data.inserted} ajoutés, ${data.skipped} ignorés`);
    loadData();
  } catch (err) {
    toast(err.message, "error");
  }
});

// ========== Filtres ==========
let searchTimeout;
searchInput.addEventListener("input", () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    state.search = searchInput.value.trim();
    state.page = 1;
    loadData();
  }, 350);
});

filterClasse.addEventListener("change", () => {
  state.classe = filterClasse.value;
  state.page = 1;
  loadData();
});

filterSource.addEventListener("change", () => {
  state.source = filterSource.value;
  state.page = 1;
  loadData();
});

filterArchive.addEventListener("change", () => {
  state.archive = filterArchive.checked;
  state.page = 1;
  loadData();
});

// ========== Init ==========
loadData();

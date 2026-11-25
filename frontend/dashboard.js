/**
 * Dashboard - Chart.js + stats
 */
const API = "http://127.0.0.1:8001/api/v1";

let charts = {};

function toast(msg, type = "success") {
  const container = document.getElementById("toastContainer");
  const el = document.createElement("div");
  el.className = `toast ${type}`;
  el.textContent = msg;
  container.appendChild(el);
  setTimeout(() => el.remove(), 3500);
}

const COLORS = [
  "#2563eb", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6",
  "#06b6d4", "#ec4899", "#84cc16", "#f97316", "#6366f1",
];

function destroyCharts() {
  Object.values(charts).forEach((c) => c.destroy());
  charts = {};
}

async function loadDashboard() {
  try {
    const res = await fetch(`${API}/dashboard`);
    if (!res.ok) throw new Error("Erreur chargement dashboard");
    const data = await res.json();

    // Cards
    document.getElementById("statEtudiants").textContent = data.total_etudiants ?? "—";
    document.getElementById("statClasses").textContent = data.total_classes ?? "—";
    document.getElementById("statMatieres").textContent = data.total_matieres ?? "—";
    document.getElementById("statMoyenne").textContent =
      data.moyenne_generale != null ? data.moyenne_generale.toFixed(2) : "—";

    destroyCharts();

    // Chart Classes
    const ctx1 = document.getElementById("chartClasses");
    charts.classes = new Chart(ctx1, {
      type: "bar",
      data: {
        labels: (data.etudiants_par_classe || []).map((d) => d.label),
        datasets: [
          {
            label: "Étudiants",
            data: (data.etudiants_par_classe || []).map((d) => d.value),
            backgroundColor: COLORS,
            borderRadius: 8,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, ticks: { precision: 0 } },
        },
      },
    });

    // Chart Source (doughnut)
    const ctx2 = document.getElementById("chartSource");
    charts.source = new Chart(ctx2, {
      type: "doughnut",
      data: {
        labels: (data.etudiants_par_source || []).map((d) => d.label),
        datasets: [
          {
            data: (data.etudiants_par_source || []).map((d) => d.value),
            backgroundColor: ["#10b981", "#2563eb", "#f59e0b"],
            borderWidth: 0,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "bottom" },
        },
      },
    });

    // Chart Notes
    const ctx3 = document.getElementById("chartNotes");
    charts.notes = new Chart(ctx3, {
      type: "bar",
      data: {
        labels: (data.repartition_notes || []).map((d) => d.label),
        datasets: [
          {
            label: "Nombre de notes",
            data: (data.repartition_notes || []).map((d) => d.value),
            backgroundColor: "#8b5cf6",
            borderRadius: 8,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, ticks: { precision: 0 } },
        },
      },
    });

    // Top étudiants
    const topBody = document.getElementById("topBody");
    const top = data.top_etudiants || [];
    if (!top.length) {
      topBody.innerHTML = `<tr><td colspan="6" class="empty-state">Aucune donnée de notes</td></tr>`;
    } else {
      topBody.innerHTML = top
        .map(
          (e, i) => `
        <tr>
          <td><strong>${i + 1}</strong></td>
          <td>${e.numero}</td>
          <td>${e.nom}</td>
          <td>${e.prenom}</td>
          <td>${e.classe || "—"}</td>
          <td><strong style="color:#059669">${Number(e.moy).toFixed(2)}</strong></td>
        </tr>`
        )
        .join("");
    }
  } catch (err) {
    toast("Impossible de charger le dashboard. Vérifiez l'API.", "error");
    console.error(err);
  }
}

document.getElementById("btnRefresh").addEventListener("click", loadDashboard);
loadDashboard();

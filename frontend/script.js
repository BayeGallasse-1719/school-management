// url de base
const API_BASE = "http://localhost:8000/api/v1";

// recuperer les elements du Dom
const tableData = document.querySelector('#tableauData');
const charger = document.querySelector('#datajson');
const tablePrincipal = document.querySelector('#tableauPrincipal');
const formEtudiant = document.getElementById('formEtudiant');
const btnAfficher = document.getElementById('btnAfficher');
    

btnAfficher.addEventListener('click', () => {    
  // toggle affichage
  if (formEtudiant.style.display === "none") {
    formEtudiant.style.display = "block";
    btnAfficher.textContent = "Annuler";
  } else {
    formEtudiant.style.display = "none";
    btnAfficher.textContent = "+ Ajouter";
  }
});

//-----------------------------------------------------------------------------------------------------------------------------------------------------------------
/////////////////  Fonctions Affichages
//----------------------------------------------------------------------------------------------------------------------------------------------------------------
// afficher les etudiants
function afficherEtudiant(etudiants){
  // vider le tableau 
  tableData.innerHTML = '';
  // parcourir tout les etudiants
  etudiants.forEach((etudiant, index) => {
    // ajouter une ligne
    const row = tableData.insertRow()

    // ajouter les cellules avec les donnees
    row.insertCell(0).textContent = index+1;
    row.insertCell(1).textContent = etudiant.numero || '-';
    row.insertCell(2).textContent = etudiant.nom || '-';
    row.insertCell(3).textContent = etudiant.prenom || '-';
    row.insertCell(4).textContent = etudiant.date_naissance || '-';
    row.insertCell(5).textContent = etudiant.user_at || '-';
    row.insertCell(6).textContent = etudiant.classe || '-';
    row.insertCell(7).textContent = etudiant.source || '-';

    // actions
    const action = row.insertCell(8);

    //button voir
    const buttonVoir = document.createElement('button');
    buttonVoir.textContent = 'Detail';
    buttonVoir.style.cursor = 'pointer';

    // afficher etudiant par numero
    buttonVoir.addEventListener('click', ()=>{
      //afficher les details
      getEtudiantByNumero(etudiant.numero);
    });

    // boutton archiver / dearchiver
    const buttonArchiver = document.createElement('button');
    buttonArchiver.textContent = 'Archiver'
    action.appendChild(buttonVoir);
    action.appendChild(buttonArchiver);
    
  });
  // activer la modification
  modif_cellule();
}

// afficher les details d'un etudiant dans la page
function afficherEtudiantParNumero(etudiant){
  tablePrincipal.innerHTML = `
    <div style="border:1px solid #ccc; border-radius:6px; padding:15px; background:#fff; max-width:400px;">
      <h3 style="margin-bottom:10px; font-size:18px; color:#333;">Informations Personnelles</h3>
      <p><strong>Numéro :</strong> ${etudiant.numero || '-'}</p>
      <p><strong>Nom :</strong> ${etudiant.nom || '-'}</p>
      <p><strong>Prénom :</strong> ${etudiant.prenom || '-'}</p>
      <p><strong>Date naissance :</strong> ${etudiant.date_naissance || '-'}</p>
      <p><strong>Utilisateur :</strong> ${etudiant.user_at || '-'}</p>
      <p><strong>Classe :</strong> ${etudiant.classe || '-'}</p>
      <p><strong>Source :</strong> ${etudiant.source || '-'}</p>
    </div>
  `;
}

//recuperer les donnees du formulaire
function recupEtudiant(){
  const data = {
    numero: formEtudiant.numero.value,
    nom: formEtudiant.nom.value,
    prenom: formEtudiant.prenom.value,
    date_naissance: formEtudiant.date_naissance.value,
    user_at: formEtudiant.user_at.value,
    classe: formEtudiant.classe.value,
    source: formEtudiant.source.value,
    archive: formEtudiant.archive.value === "true"
  }
  ajouterEtudiant(data);
}


function modif_cellule() {
  for (let i = 0; i < tableData.rows.length; i++) {
    const row = tableData.rows[i];
    // ignorer index (0) et actions (dernière)
    for (let j = 2; j < row.cells.length - 2; j++) {
      
      // recuperer le numero de l'etudiant
      const numero = row.cells[1].textContent; 
      row.cells[j].addEventListener("dblclick", () => {
        row.cells[j].contentEditable = true;
        row.cells[j].style.backgroundColor = "#2c8ee4";

        // sauvegarde quand on appuie sur Entrée
        row.cells[j].addEventListener("keydown", (e) => {
          if (e.key === "Enter") {
            e.preventDefault();
            row.cells[j].contentEditable = false;
            row.cells[j].style.backgroundColor = "";

            const updatedData = {};
            // construire l'objet avec toutes les colonnes modifiées
            updatedData.nom = row.cells[2].textContent;
            updatedData.prenom = row.cells[3].textContent;
            updatedData.date_naissance = row.cells[4].textContent;
            updatedData.user_at = row.cells[5].textContent;
            updatedData.classe = row.cells[6].textContent;

            update(numero, updatedData);
          }
        });
      });
    }
  }
}


//-----------------------------------------------------------------------------------------------------------------------------------------------------------------
//////////  Fonction de recuperation des api
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------

//==================== Etudiants =======================================================================/
// recuperer les etudiants
async function getEtudiants() {
  try {
    //limit = 5;
    //recuperer les donnees
    const reponse = await fetch(`${API_BASE}/etudiants`);
    // convertir en json
    const data = await reponse.json();
    
    // afficher les donnees
   afficherEtudiant(data)
    
  } catch (erreur) {
    console.error("Erreur :", erreur);
  }
}

// recuperer etudiant par numero
async function getEtudiantByNumero(numero) {
  try {
    const reponse = await fetch(`${API_BASE}/etudiants/${numero}`);
    //convertir en json
    const etudiant = await reponse.json();
    //affichage des infos de l'etudiant
    afficherEtudiantParNumero(etudiant);
  }catch (erreur){
    console.error('ERREUR: ', erreur)
  }
}

// ajouter un etudiant
async function ajouterEtudiant(data) {
  try {
    const reponse = await fetch(`${API_BASE}/etudiants`, {
      method: "POST", 
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });
    if (reponse.ok){
      alert("Étudiant ajouté avec succès !");
      // recharge la liste après ajout
      getEtudiants();
      formEtudiant.reset();
    } else {
      const erreur = await reponse.json();
      alert("Erreur lors de l'ajout : " + JSON.stringify(erreur));
    }
  } catch(erreur){
    console.error("Erreur :", erreur);
  }
}

// mettre a jour les infos d'un etudiant
async function update(numero, data) {
  const reponse = await fetch(`${API_BASE}/etudiants/${numero}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  if (reponse.ok) {
    alert("Étudiant mis à jour !");
    getEtudiants(); // recharger la liste
  } else {
    const err = await reponse.json();
    console.log("Erreur : " + JSON.stringify(err));
  }
}


//==================== Matieres =======================================================================


// evenement
getEtudiants()
// Soumission du formulaire
formEtudiant.addEventListener('submit', (e) => {
  // evite le refresh
  e.preventDefault(); 
  recupEtudiant();
});


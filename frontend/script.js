const API_BASE = "http://localhost:8000/api/v1";

// recuperer les elements du Dom
const tableData = document.querySelector('#tableauData');
const charger = document.querySelector('#datajson')

// afficher les etudiants
function afficherEtudiant(etudiants){
  // vider le tableau 
  tableData.innerHTML = '';
  // parcourir tout les etudiants
  etudiants.forEach((etudiant, index) => {
    // ajouter une ligne
    const row = tableData.insertRow()
    // ajouter les cellules avec les donnees
    row.insertCell(0).textContent = index;
    row.insertCell(1).textContent = etudiant.numero;
    row.insertCell(2).textContent = etudiant.nom;
    row.insertCell(3).textContent = etudiant.prenom;
    row.insertCell(4).textContent = etudiant.date_naissance;
    row.insertCell(5).textContent = etudiant.user_at;
    row.insertCell(6).textContent = etudiant.classe;
    row.insertCell(7).textContent = etudiant.source;
    row.insertCell(8).textContent = etudiant.archive;
    // actions
    const action = row.insertCell(9);
    //button voir
    const buttonVoir = document.createElement('button');
    buttonVoir.textContent = 'Detail';
    // afficher etudiant par numero
    buttonVoir.addEventListener('click' ,getEtudiantByNumero);
    const buttonArchiver = document.createElement('button');
    buttonArchiver.textContent = 'Archiver'
    action.appendChild(buttonVoir);
    action.appendChild(buttonArchiver);
    
  });
}

// recuperer les etudiants
async function getEtudiants() {
  try {
    //recuperer les donnees
    const reponse = await fetch(`${API_BASE}/etudiants`);
    // convertir en json
    const data = await reponse.json();
   console.log(data)
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
    console.log(reponse);
    console.log(etudiant);
  }catch (erreur){
    console.error('ERREUR: ', erreur)
  }
}

// evenement
charger.addEventListener('click', getEtudiants);

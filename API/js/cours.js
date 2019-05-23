

function afficher(reponse) {
    console.log(reponse);
}

ajaxGet("http://localhost/esir2_projet_aii_site_crowdfunding/javascript-web-srv/data/langages.txt", afficher);

ajaxGet("http://localhost/esir2_projet_aii_site_crowdfunding/javascript-web-srv/data/films.json", function (reponse) {
    // Transforme la réponse en tableau d'objets JavaScript
    var films = JSON.parse(reponse);
    // Affiche le titre de chaque film
    films.forEach(function (film) {
        console.log(film.titre);
    })
});


/*var premMinElt = document.getElementById("premMin");
// Accès aux informations publiques sur le Premier Ministre
ajaxGet("https://www.data.gouv.fr/api/1/organizations/premier-ministre/", function (reponse) {
    var premierMinistre = JSON.parse(reponse);
    // Ajout de la description et du logo dans la page web
    var descriptionElt = document.createElement("p");
    descriptionElt.textContent = premierMinistre.description;
    var logoElt = document.createElement("img");
    logoElt.src = premierMinistre.logo;
    premMinElt.appendChild(descriptionElt);
    premMinElt.appendChild(logoElt);
});*/


// Création d'un objet FormData

/*var commande = new FormData();
commande.append("couleur", "rouge");
commande.append("pointure", "43");
// Envoi de l'objet FormData au serveur
ajaxPost("http://localhost/esir2_projet_aii_site_crowdfunding/javascript-web-srv/post_form.php", commande,
    function (reponse) {
        // Affichage dans la console en cas de succès
        console.log("Commande envoyée au serveur");
    }
);*/


/*var form = document.querySelector("form");
// Gestion de la soumission du formulaire
form.addEventListener("submit", function (e) {
    e.preventDefault();
    // Récupération des champs du formulaire dans l'objet FormData
    var data = new FormData(form);
    // Envoi des données du formulaire au serveur
    // La fonction callback est ici vide
    ajaxPost("http://localhost/esir2_projet_aii_site_crowdfunding/javascript-web-srv/post_form.php", data, function () {});
});*/

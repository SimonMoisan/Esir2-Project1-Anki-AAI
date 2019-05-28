

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




const getImage = document.getElementById("getImg");
ajaxGet("http://localhost:3000/v1/images/45745c60-7b1a-11e8-9c9c-2d42b21b1a3e", function (reponse){
    const image = JSON.parse(reponse);
    const getIdElt = document.createElement("div");
    getIdElt.textContent = image.id;
    getIdElt.id = "id"
    const getImgElt = document.createElement("img");
    getImgElt.src = image.image;
    getImage.appendChild(getIdElt);
    getImage.appendChild(getImgElt);
});


const getAllId = document.getElementById("getAllId");
ajaxGet("http://localhost:3000/v1/images", function (reponse){
    const ids = JSON.parse(reponse);
    ids.forEach(function (id) {
        // Ajout du titre et du contenu de chaque article
        var p = document.createElement("p");
        var idElt = document.createElement("a");
        idElt.href = "index.php?id=" + id.id;
        idElt.textContent = id.id;
        p.appendChild(idElt);
        getAllId.appendChild(p);
        
    });
});





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

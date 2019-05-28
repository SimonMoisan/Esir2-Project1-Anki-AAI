# Projet COZMO-CROWD

## Description

Ce projet vise à utiliser le robot COZMO de ANKI avec la notion de crowdsourcing.


## Installation

### Installation COZMO

Pour installer COZMO et le SDK il vous faut matériellement :
* Un mobile/tablette Android 5.0 ou plus compatible COZMO ou un iPhone (non testé)
* Un Ordinateur, avec au moins 1 port USB et sous un des OS suivant : macOS (non-testé), ubuntu (non-testé), Windows 7-8-10 (testé avec Windows 10), et __il vous faudra y être administrateur/root absolu !__
* Un cable USB pour connecter votre mobile/tablette à votre Ordinateur

Pour savoir si votre mobile/tablette Android est compatible avec l'application COZMO, allez sur le playstore Android; Si vous retrouvez l'application COZMO en la recherchant dans la barre de recherche du playstore, alors c'est compatible. Si vous ne retrouver pas l'application, alors elle n'est pas compatible.

Ensuite, suivre les instructions sur un de ces sites en fonction de votre OS :

* Windows : http://cozmosdk.anki.com/docs/install-windows.html#install-windows
* macOS   : http://cozmosdk.anki.com/docs/install-macos.html#install-macos
* Linux   : http://cozmosdk.anki.com/docs/install-linux.html#install-linux

Pour résumer les liens ci-dessus :

* Installer Python sur l'ordinateur (avec les variables d'environnement PATH)
* Installer l'application COZMO sur le mobile
* Installer adb ou équivalent sur l'ordinateur (avec les variables d'environnement PATH)

### Installation API 

Pour l'API et le front, on a utilisé WAMP (pour Windows) (http://www.wampserver.com/#wampserver-64-bits-php-5-6-25-php-7) :
*  Une fois installé, il faut modifier le fichier httpd.conf de la manière suivante : 
    *   Retirer le caractère '#' devant la ligne `LoadModule headers_module modules/mod_headers.so`
    *   Ajouter les lignes suivantes à la fin du fichier :
        ```
        <IfModule mod_headers.c>
        	# Accept cross-domain requests
        	Header always set Access-Control-Allow-Origin "*"
        	Header always set Access-Control-Allow-Headers "Content-Type"
        </IfModule> 
        ```

*  Il faut ensuite placer le dossier API dans le dossier www de WAMP.
*  Lancer ou relancer WAMP pour que tout marche correctement.
*  Taper l'URL suivant : localhost/API/affichage.php (il n'y a pas d'auto-fafraichissement)

### Installation front

Avant de lancer l'API, il est important d'installer les modules adéquats. Pour cela Node.js doit être installé sur la machine.
Pour lancer l'installation des modules il faut taper "npm install" à l'intérieur du repertoire API (contenant index.php, app.js, etc...).
Cela peut prendre un moment, soyez patient.


## Utilisation

Pour que le front affiche les images stockés dans l'API, il faut lancer le serveur en tapant "npm start" dans le repertoire API.
Si jamais une erreur apparait, cela est surement du au fait qu'il manque un module. Pour y remedier, il faut identifier le module manquant dans le message d'erreur (assez explicite),
et taper "npm install nomdumodule --save". Il faut laisser tourner le serveur et rafriachir la page du front si nécessaire pour voir les liens des images.

### API

Cette API ne possède que des POST et GET sur les parties d'urls suivantes `/images`, `/images/{id}`, `/answers` et `/answers/{id}`.

Elle n'a pas de DELETE, la rendant impossible à utiliser dans un autre cadre qu'une démo.

Elle ne stock pas durablement ses objets, lorsqu'elle est éteinte ou redémarrée, ses objets sont perdus. 

Assurez vous donc d'éteindre COZMO __avant__ d'éteindre l'API.

- `/images` ==> __GET__ (fait par affichage.php) et __POST__ (fait par COZMO)
    - POST : `{id : <uuid>, image: <donnée en base64>}`
- `/images/{id}` ==> __GET__ (fait par le front)
- `/answers` ==> __GET__ (fait par rien) et __POST__ (fait par le front)
    - POST : `{id : <uuid>, nbrVotes : <entier représentant le nombre de votants>, answer: <La réponse la plus donnée>}`
- `/answers/{id}` ==> __GET__ (fait par COZMO)

### ActionCrowd

ActionCrowd désigne le programme situé dans le dossier `ActionCrowd`.

Il permet à COZMO de se balader et de réaliser les actions suivantes lorsqu'il aperçoit un de ses trois cube :
- COZMO se replace face au cube (fonction built-in de COZMO, ne fonctionne pas toujours)
- COZMO prend une photo de ce qu'il a devant lui (normalement le cube) et la converti en JPEG puis en base64
- COZMO envoit l'image à l'API sous la forme d'un objet JSON `{id: <uuid générée>, image: <donnée en base64>}`, via un POST réalisé via la bibliothèque __requests__ de Python
- COZMO attend activement (pas de parralélisme) qu'une réponse apparaît dans l'API avec la même uuid que l'image qu'il a posté (attente via des GET espacés de quelques secondes). La lumière sur le dos de COZMO sera alors <span style='color:red'>rouges</span> et jaune.
- COZMO attend activement que le nombre de votes indiqués dans la réponse dépasse un certain nombre (attente via des GET espacés de quelques secondes). La lumière sur le dos de COZMO sera alors <span style='color:red'>rouge</span> et jaune.
- COZMO récupère la chaîne de caractères de la réponse puis éxécute l'action concernée sur le cube ou lui-même (soit changer la couleur du cube, soit dire quelque chose). La lumière sur le dos de COZMO sera <span style='color:cyan'>cyan</span>.

Pour activer ce projet, lancer la commande `py main.py` en étant dans le dossier __ActionCrowd__.

### FaceCrowd

FaceCrowd désigne le programme situé dans le dossier `FaceCrowd`

Il permet à COZMO de rester en place et de pas bouger (lumières <span style='color:red'>rouges</span>). COZMO réalisera les actions suivantes lorqu'il reconnaîtra un visage humain (lumières bleues).
- La reconnaissance de visage n'étant pas parfaite, nous avons donné un peu de temps à COZMO afin qu'il reconnaisse un visage (lumières <span style='color:blue'>bleues</span> pendant la reconnaissance). Lors de la phase de reconnaissance, COZMO peut suivre le visage s'il se déplace lentement.
- Si le visage à déjà été reconnu complètement :
    - COZMO va juste bouger un peu et dire le nom de la personne reconnu (lumières <span style='color:green'>vertes</span>)
- Si le visage n'a __jamais__ été vu auparavant :
    - COZMO va prendre une photo et lancer un __thread de reconnaissance (voir plus bas)__ (programmation parrallèle asynchrone), puis énoncé d'une voix grave que le visage va passer un phase de reconnaissance. (lumières blanches et <span style='color:red'>rouges</span>)
- Si le visage est un visage déjà vu par COZMO mais qui n'a pas encore été reconnu par le crowdsourcing :
    - COZMO va anoncer l'uuid généré automatiquement pour le visage, et qu'il faudra patienter pour être reconnu. (lumières jaunes et <span style='color:red'>rouges</span>)

Le thread de reconnaissance va faire séquetiellement les actions suivantes :
- Le thread prend une photo de ce qu'il a devant lui (normalement le visage) et la converti en JPEG puis en base64
- Le thread modifie le nom du visage sous la forme `pending_<uuid sans chiffres ni tirets>`, afin que COZMO puisse savoir si le visage qu'il observe est déjà en cours de reconaissance ou non.
- Le thread envoit l'image à l'API sous la forme d'un objet JSON `{id: <uuid générée>, image: <donnée en base64>}`, via un POST réalisé via la bibliothèque __requests__ de Python
- Le thread attend activement qu'une réponse apparaît dans l'API avec la même uuid que l'image qu'il a posté (attente via des GET espacés de quelques secondes).
- Le thread attend activement que le nombre de votes indiqués dans la réponse dépasse un certain nombre (attente via des GET espacés de quelques secondes).
- Le thread récupère la chaîne de caractères de la réponse puis change le nom du visage en cette chaîne. si la chaîne commence par `pending_` COZMO va croire que le visage est en cours de reconnaissance alors que non.
- Le thread se termine et se supprime proprement

Pour activer cette démo, lancer la commande `py TestFaceCrowd.py` dans le dossier __FaceCrowd__.







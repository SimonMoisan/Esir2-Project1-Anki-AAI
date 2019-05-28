# Projet COZMO

## Description

Ce projet vise à utiliser le robot COZMO de ANKI avec la notion de crowdsourcing.


## Installation

Pour installer COZMO et le SDK il vous faut matériellement :
    - Un mobile/tablette Android 5.0 ou plus compatible COZMO ou un iPhone (non testé)
    - Un Ordinateur, avec au moins 1 port USB et sous un des OS suivant : macOS (non-testé), ubuntu (non-testé), Windows 7-8-10 (testé avec Windows 10)
    - Un cable USB pour connecter votre mobile/tablette à votre Ordinateur

Pour savoir si votre mobile/tablette Android est compatible avec l'application COZMO, allez sur le playstore Android; Si vous retrouvez l'application COZMO en la recherchant dans la barre de recherche du playstore, alors c'est compatible. Si vous ne retrouver pas l'application, alors elle n'est pas compatible.

Ensuite, suivre les instructions sur ces sites :
    - Windows : http://cozmosdk.anki.com/docs/install-windows.html#install-windows
    - macOS   : http://cozmosdk.anki.com/docs/install-macos.html#install-macos
    - Linux   : http://cozmosdk.anki.com/docs/install-linux.html#install-linux

Pour résumer les liens ci-dessus :
    - Installer Python sur l'ordinateur (avec les variables d'environnement PATH)
    - Installer l'application COZMO sur le mobile
    - Installer adb ou équivalent sur l'ordinateur (avec les variables d'environnement PATH)

Pour l'API et le front, on a utilisé WAMP (http://www.wampserver.com/#wampserver-64-bits-php-5-6-25-php-7) :
    - Une fois installer, il faut modifier le fichier httpd.conf de la manière suivante : 
        - Retirer le caractère '#' devant la ligne "LoadModule headers_module modules/mod_headers.so"
        - Ajouter les lignes suivantes à la fin du fichier :
        <IfModule mod_headers.c>
        	# Accept cross-domain requests
        	Header always set Access-Control-Allow-Origin "*"
        	Header always set Access-Control-Allow-Headers "Content-Type"
        </IfModule>
    - Il faut ensuite placer le dossier API dans le dossier www de WAMP.
    - Lancer ou relancer WAMP pour que tout marche correctement.
    - Taper l'URL suivant : localhost/API/affichage.php



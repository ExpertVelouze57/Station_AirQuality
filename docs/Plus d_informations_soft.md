# Fonctionnement du programme

Le programme est composé de 3 threads. 

* Le 1er gère l'affichage, il permet de faire variers les differents écran.

* Le 2ème gere la récuperation des données qui se fait toutes les 10s et les enregistres dans des variables globale.

* Le derniers le main, après avoir fait l'initialisation s'occupe d'enregistrer les données dans un fichiers scv et de les envoyers via MQTT.

!!! Note
    La gestion du bouton ce fait grace a une intéruption.

Gestion du bouton : 

| Type de clique         | Etat de la led    | Signification                 |
| :----------------------|:-------------------:| :-------------------------|
| 1 clique | fixe     |  Passage de données aux IPs ou inversement |
| 2 clique rappide   | Clignotant    | Mode réception de commandes  |
| 1 clique long  | Eteint puis allumée  | Sortie du mode réception |
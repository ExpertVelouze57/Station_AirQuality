# Flasher une image

Quelque soit la méthode d'installation utilisée vous aller forcément devoir flasher une carte SD avec une image pour faire fonctionner votre RaspberryPi. Cette section vous montrera comment faire.

!!! Note
    L'ensemble des données de la carte SD vont être suprimées. Faites en sorte qu'il n'y en ai pas.

1. Pour commencer il faut téléchager le logiciel [BalenaEtcher](https://www.balena.io/etcher/).

2. Inserez la carte SD dans votre ordinateur.

3. Ensuite démarrer le logiciel et sélectionner l'image que vous voulez flasher sur la carte SD (Voir les sections précédante pour le choix de l'image [basic](Configuration_facile.md) ou [custom](Configuration_custom.md) ). Pour cela cliquez sur ``flash from file``.

![Balena](configuration/balena1.webp)

4. Sélectionnez la carte SD que vous venez d'insérer, en vérifiant que c'est bien la bonne en regardant la taille de celle-ci par exemple. Pour sélectionner la carte cliquez sur ``Select target`` -> cocher le bon périphérique -> cliquez sur ``Select``.

![Balena](configuration/balena3.webp)

5. Pour finir cliquer sur ``Flash!`` et patientez un petit moment.

!!! Warning
    Pensez à ejecter votre carte SD avant de la retirer de l'ordinateur sinon vous risquez de l'endommager.

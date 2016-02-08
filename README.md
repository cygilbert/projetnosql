# Projet NoSQL

## Equipe

* Cyril Gilbert
* Derrick Ho
* Olivier Large
* Guillaume Mhor

## Contenu GitHub

* install_command: décrit les différentes commandes d'installation utilisées pendant le projet.
* Req24h.py: permet le calcul la tendance de chaque journée.
* Res30j.py: permet le calcul la tendance sur une période de 30j.
* add_date.py: ce script rajoute la date dans chaque fichier.
* load_data.py: ce script permet le chargement des données dans Cassandra.
* log_time: ce fichier stocke divers logs (ex: temps de chargement, temps de calcul, etc.). 
* flaskapp/: application Flask qui contient les slides de la présentation.
* Test/: contient les différents fichiers de tests.

## Application Flask

Afin de lancer l'application Flask:
```bash
cd flaskapp/
python flaskapp.py
```
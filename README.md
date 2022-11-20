# Projet : Etude du projet de loi sur l’installation obligatoire de panneaux solaires sur les grands parkings avant 2026

L'idée de notre projet est d'à partir des différentes bases de données du site data.gouv on effectue l'étude de la pertinance de ce projet de loi.


## Contexte

En 2026 le projet de loi impose que tous les parking de plus de 400 places, seront imposés de placer sur la moitié des places des panneaux solaires.

## Etude

L'idée est donc d'étudier la pertinence de projet qui ne fait pas de différence selon la position géographique des parkings. Nous allons nous concentrer sur deux questions:

- Est-ce que pour la même aire de panneaux solaires imposée, avec un placement géographique optimisé, les économies énérgétiques sont-elles considérables?

- Est-ce que placer les panneaux dans des parkings est le choix le plus pertinent? 

- Quelle est la meilleure répartition des panneaux solaires en prennant en plus en compte la consommation par zone géographique en considérant en plus le déplacement de l'énergie?

Nous allons nous intérésser aux bases de données suivantes :

- Irradiation du territoire français,
- Parkings en France et leur nombre de places,
- Prix éléctricité au cours du temps,
- Consommation électrique par département,
- Localisation des établissements publiques

Nous avons trouvées bases suivantes:

https://www.data.gouv.fr/fr/datasets/base-nationale-des-lieux-de-stationnement/


https://odre.opendatasoft.com/explore/dataset/rayonnement-solaire-vitesse-vent-tri-horaires-regionaux/information/?disjunctive.region&sort=date

## Sprints

1. Prise en main des bases de données
2. Transformation de chaque une des bd en dataframe pandas
3. Choix d'un model et implementation du calcul de l'énergie produite à partir des données d'ensoleillement
4. Calcul du bénéfice énergétique par choix de positions géographiques des panneaux solaires
5. Visualisation de données sur une carte des position les plus pertinentes
6. Calcul de l'aire optimale 
7. Comparaison avec le choix des parkings

# Guide d'installation


## Installation de l'ensemble des dépendances:

Pour installer l'ensemble des dépendances, saisir dans la console:

>pip3 install -r requirements.txt

ou

>pip install -r requirements.txt

## Mise en place des données

Ensuite decompresser dans le réperatoire du programme le fichier **data.zip**.
Vérifier que toutes les variables d'environnement sont bien correctes dans le fichier **vars.py**.


## Executer le programme dash

Executer le fichier **app.py** et lancer dans la barre d'un navigateur http://127.0.0.1:8050/


## Pour lancer l'execution des tests
> pytest --cov-report html:coverage tests/test_*.py


## tree map

projets2 - Copie/
├── __pycache__/
├── app.py
├── assets/
├── components/
│   ├── __init__.py
│   ├── __pycache__/
│   ├── histogramme.py
│   └── pie.py
├── data/
│   └── tweets/
│       ├── Eolien/
│       ├── Loi/
│       └── Solaire/
├── database/
│   └── __pycache__/
├── tests/
│   ├── __init__.py
│   └── test_dataframes.py
├── utils/
│   ├── __init__.py
│       └── Solaire/
├── database/
│   └── __pycache__/
├── tests/
│   ├── __init__.py
│   └── test_dataframes.py
├── utils/
│   ├── __init__.py
│   ├── __pycache__/
│   ├── dataframes.py
│   └── tweets.py
├── vars.py
└── visualisation/
    └── __pycache__/
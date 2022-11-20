""" Variables d'environnement et de projet """
ENV = {
    'data': {
        'departements': ('data/departements-region.csv', ','),
        'evolution': ('data/evolution-des-prix-domestiques-du-gaz-et-de-lelectricite.csv', ';'),
        'parkings': ('data/parkings.csv', ';'),
        'rayonnement': ('data/rayonnement-solaire-vitesse-vent-tri-horaires-regionaux.csv', ';'),
        'france' : ('data/departements-version-simplifiee.geojson', '')
    },
    'tweets' : {
        'solaire' : 'data/tweets/Solaire',
        'eolien' : 'data/tweets/Eolien',
        'loi' : 'data/tweets/Loi'
    }
}

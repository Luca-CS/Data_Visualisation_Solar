""" Module de gestion des parkings """

import pandas as pd

from vars import ENV

import warnings
warnings.filterwarnings("ignore")
warnings.simplefilter(action='ignore', category=FutureWarning)

def csv_to_dataframe(path, sep=';'):
    """
    Charge un fichier CSV en dataframe
    Input : path (str) : chemin du fichier CSV
    Output : dataframe
    """
    return pd.read_csv(path, sep=sep, encoding='utf-8')


def dict_of_dataframes():
    """
    Charge les fichiers CSV en dataframe et construit un dictionnaire avec tous les dataframes
    Input : None
    Output : dict de dataframes
    """
    print('Chargement des dataframes...')
    return {k: csv_to_dataframe(v[0], v[1]) for k, v in ENV['data'].items() if k != 'france'}


dataframes = dict_of_dataframes()


def build_parking_fullinfo(surface = 2.4 * 5, pourcentage_surface = 0.5, rendement= 0.15, prix = 250 ,minumum_parking = 400, prix_electricite = 0.1740):
    """
    Construit un dataframe avec les informations complètes des parkings
    Input : None
    Output : dataframe
    """
    df = dataframes['parkings'][['nom', 'nb_places','insee','Xlong', 'Ylat']].copy()
    df['num_dep'] = df['insee'].apply(lambda x: f"0{str(x)[:1]}" if len(str(x)) == 4 else f"{str(x)[:2]}")
    df['num_dep']=df['num_dep'].astype(int)
    df = df.join(dataframes['departements'].set_index('num_dep'), on='num_dep')
    df["surface"] = df["nb_places"] * surface
    df["surface_exploitable"] = df["surface"] * pourcentage_surface
    df_rayonnement = dataframes['rayonnement'].copy()
    df_rayonnement = df_rayonnement[df_rayonnement['Rayonnement solaire global (W/m2)'] != 0]
    df_rayonnement = df_rayonnement.groupby("Code INSEE région").mean()
    df_rayonnement = df_rayonnement.reset_index()
    df_rayonnement.rename(columns={"Code INSEE région": "num_region"}, inplace=True)
    df_rayonnement = df_rayonnement[["num_region", "Rayonnement solaire global (W/m2)"]]
    df_rayonnement.set_index("num_region", inplace=True)
    df_rayonnement.rename(columns={"Rayonnement solaire global (W/m2)": "rayonnement"}, inplace=True)
    df = df.join(df_rayonnement, on='num_region')
    df["puissance"] = df["surface"] * df["rayonnement"] * pourcentage_surface * rendement
    df["prix_panneaux"] = df['surface_exploitable'] * prix
    df["energie"] = df["puissance"] * 365 * 24
    df = df[df["nb_places"]>minumum_parking]
    df["prix_electricite_kwh"] = df["energie"] * prix_electricite / 1000
    return df

df = build_parking_fullinfo()


def augmentation(prix_actuel):
    df = build_parking_fullinfo(minumum_parking=400, pourcentage_surface=0.5, prix_electricite=prix_actuel)
    df = df[['num_dep','prix_panneaux','prix_electricite_kwh']]
    df = df.groupby('num_dep').sum().sort_values('prix_electricite_kwh', ascending=False)
    prix_loi, prix_electricite = df['prix_panneaux'].sum(), df['prix_electricite_kwh'].sum()
    df2 = build_parking_fullinfo(minumum_parking=0, pourcentage_surface=1, prix_electricite=prix_actuel)
    df2 = df2[['num_dep','prix_panneaux','prix_electricite_kwh','surface_exploitable']]
    df2 = df2.groupby('num_dep').sum()
    df2['prix_electricite_kwh_par_place'] = df2['prix_electricite_kwh'] / (df2['surface_exploitable'] )
    df2 = df2.sort_values('prix_electricite_kwh_par_place', ascending=False)
    prix_cumule = 0
    count = 0
    for i in df2.index:
        if prix_cumule < prix_loi:
            prix_cumule += df2.loc[i, 'prix_panneaux']
            count += df2.loc[i, 'prix_electricite_kwh']
    return count/prix_electricite

def classement_par_production(df):
    df2 = df.copy()
    df2 = df2.groupby('num_dep').sum()
    df2['prix_electricite_kwh_par_place'] = df2['prix_electricite_kwh'] / (df2['surface_exploitable'] )
    df2 = df2.sort_values('prix_electricite_kwh_par_place', ascending=False)
    return df2

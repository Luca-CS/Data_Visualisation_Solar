from utils.dataframes import csv_to_dataframe
import pandas as pd
from utils.dataframes import dict_of_dataframes
from utils.dataframes import build_parking_fullinfo 

def test_dict_of_dataframe(): 
    sample = {'conso': csv_to_dataframe('data/conso-elec-gaz-annuelle-par-naf-agregee-departement.csv', ";"), 'departements': csv_to_dataframe('data/departements-region.csv', ","), "evolution": csv_to_dataframe('data/evolution-des-prix-domestiques-du-gaz-et-de-lelectricite.csv', ';'), "parkings": csv_to_dataframe('data/parkings.csv', ";"), "rayonnement": csv_to_dataframe('data/rayonnement-solaire-vitesse-vent-tri-horaires-regionaux.csv', ";")}
    assert sample == dict_of_dataframes() 

def test_csv_to_dataframe(): 
    sample = pd.read_csv('data/conso-elec-gaz-annuelle-par-naf-agregee-departement.csv', sep=";", encoding='utf-8')
    assert sample.equals(csv_to_dataframe('data/conso-elec-gaz-annuelle-par-naf-agregee-departement.csv', ";"))

def test_build_parking_fullinfo():
    sample=[523,6088]
    h=[build_parking_fullinfo()["nb_places"][8],build_parking_fullinfo()["insee"][8]]
    assert sample==h

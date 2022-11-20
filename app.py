import os
import pathlib
import re

import warnings
warnings.filterwarnings("ignore")
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import utils.tweets as tw
import utils.dataframes as utils
import components.histogramme as hist
import components.pie as pie
from wordcloud import WordCloud
from PIL import Image
import pandas as pd
from dash.dependencies import Input, Output, State
import cufflinks as cf
import plotly.express as px 
import plotly.graph_objects as go
from vars import ENV

# Initialize app

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

df1 = tw.tweets_to_dataframe('solaire')
df2 = tw.tweets_to_dataframe('eolien')
df3 = tw.tweets_to_dataframe('loi')


def word_cloud():
    exclure_mots = ["Aliyah01150546","alors qu","co",'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',"https",'d', 'du', 'de', 'la', 'des', 'le', 'et', 'est', 'elle', 'une', 'en', 'que', 'aux', 'qui', 'ces', 'les', 'dans', 'sur', 'l', 'un', 'pour', 'par', 'il', 'ou', 'à', 'ce', 'a', 'sont', 'cas', 'plus', 'leur', 'se', 's', 'vous', 'au', 'c', 'aussi', 'toutes', 'autre', 'comme']
    text=''
    for x in df3["text"]:
        text+=x
    wordcloud = WordCloud(background_color = 'white', stopwords = exclure_mots, max_words = 50,width=800, height=400).generate(text)
    return px.imshow(wordcloud)
    





def histogramme_opinions_polarite():
    polarite1 = tw.polarity(df1)/100
    polarite2 = tw.polarity(df2)/100
    return hist.histogramme(['Solaire', 'Eolien'], [polarite1, polarite2],"","Polarité des sujets", "Comparaison des avis sur les deux sujets")
def histogramme_opinions_polarite_subjectivite():
    polarite1 = tw.avis_global(df1)/100
    polarite2 = tw.avis_global(df2)/100
    return hist.histogramme(['Solaire', 'Eolien'], [polarite1, polarite2],"","Polarité en considérant la subjectivité des sujets", "Comparaison des avis sur les deux sujets")

def pie_opinions():
    stats = tw.statistiques(df3)
    return pie.pie(list(stats.keys()), list(stats.values()), "Répartition des avis sur la nouvelle loi")

def visu_map():

    parkings = utils.df

    fig = px.scatter_mapbox(parkings, lat="Ylat", lon="Xlong", hover_name="nom", color = "nb_places",
        size = "nb_places", color_continuous_scale=px.colors.cyclical.IceFire, size_max=50, zoom=6)
    fig.update_layout(mapbox_style="open-street-map")   
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def camembert_production_elec():
    df=utils.classement_par_production(utils.build_parking_fullinfo())
    M=[60,6,34,33,69,57,67,90,75,86,38,73,49,87,94,92,17]
    L=["Oise","Alpes-Maritimes","Hérault","Gironde","Rhône","Moselle","Bas-Rhin","Territoire-de-Belfort","Paris","Vienne","Isère","Savoie","Maine-et-Loire","Haute-Vienne","Val-de-Marne","Hauts-de-Seine","Charente-Maritime"]
    x=[df["prix_electricite_kwh"][k] for k in M]
    fig = go.Figure(data=[go.Pie(labels=L, values=x)])
    return fig


def display_choropleth():
    newdf = utils.df.groupby('num_dep').sum().sort_values('prix_electricite_kwh', ascending=False)
    newdf = newdf.reset_index()
    newdf = newdf[['num_dep', 'prix_electricite_kwh']]
    for i in range(1, 96):
        if i not in newdf['num_dep'].values:
            newdf = newdf.append({'num_dep': i, 'prix_electricite_kwh': 0}, ignore_index=True)
    departements = json.load(open(ENV['data']['france'][0]))
    fig = px.choropleth(newdf, geojson=departements, locations='num_dep', featureidkey='properties.code' ,color='prix_electricite_kwh',
        color_continuous_scale="Viridis",
        range_color=(500000, 8000000),
        labels={'prix_electricite_kwh':"Prix de l'énergie généré par département"},projection="mercator"
        ,title = 'Prix de l\'énergie engendré par département en France'
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    return fig

def display_choropleth2():
    df_departements = utils.dataframes['departements']
    df_rayonnement = utils.dataframes['rayonnement'].copy()
    df_rayonnement = df_rayonnement[df_rayonnement['Rayonnement solaire global (W/m2)'] != 0]
    df_rayonnement = df_rayonnement.groupby("Code INSEE région").mean()
    df_rayonnement = df_rayonnement.reset_index()
    df_rayonnement.rename(columns={"Code INSEE région": "num_region"}, inplace=True)
    df_rayonnement = df_rayonnement[["num_region", "Rayonnement solaire global (W/m2)"]]
    df_rayonnement.set_index("num_region", inplace=True)
    df_rayonnement.rename(columns={"Rayonnement solaire global (W/m2)": "rayonnement"}, inplace=True)
    df_departements = df_departements.join(df_rayonnement, on='num_region')
    departements = json.load(open(ENV['data']['france'][0]))
    fig = px.choropleth(df_departements, geojson=departements, locations='num_dep', featureidkey='properties.code' ,color='rayonnement',
        color_continuous_scale="Viridis",
        range_color=(190, 250),
        labels={'rayonnement':'puissance moyenne (W)'},projection="mercator"
        ,title = 'Rayonnement par region'
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    return fig

def display_choropleth3():
    newdf = utils.df.groupby('num_dep').sum()
    newdf = newdf.reset_index()
    newdf = newdf[['num_dep', 'prix_panneaux']]
    for i in range(1, 96):
        if i not in newdf['num_dep'].values:
            newdf = newdf.append({'num_dep': i, 'prix_panneaux': 0}, ignore_index=True)
    departements = json.load(open(ENV['data']['france'][0]))
    fig = px.choropleth(newdf, geojson=departements, locations='num_dep', featureidkey='properties.code' ,color='prix_panneaux',
        color_continuous_scale="Viridis",
        range_color=(1000000, 45000000),
        labels={'prix_panneaux':'Prix de la mise en place de la loi par département'},projection="mercator"
        ,title = 'Carte des prix de la mise en place de la loi en France'
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    return fig

def display_choropleth4():
    newdf = utils.df.groupby('num_dep').sum()
    newdf['prix_electricite_kwh_par_place'] = newdf['prix_electricite_kwh'] / (newdf['nb_places'] * 0.5)
    newdf = newdf.sort_values('prix_electricite_kwh_par_place', ascending=False)
    newdf = newdf.reset_index()
    newdf = newdf[['num_dep', 'prix_electricite_kwh_par_place']]
    for i in range(1, 96):
        if i not in newdf['num_dep'].values:
            newdf = newdf.append({'num_dep': i, 'prix_electricite_kwh_par_place': 0}, ignore_index=True)
    departements = json.load(open(ENV['data']['france'][0]))
    fig = px.choropleth(newdf, geojson=departements, locations='num_dep', featureidkey='properties.code' ,color='prix_electricite_kwh_par_place',
        color_continuous_scale="Viridis",
        range_color=(500, 600),
        labels={'prix_electricite_kwh_par_place':'Prix de l\'energie engendré par une place d\'un parking du département'},projection="mercator"
        ,title = "Prix de l'énergie engendré par une place d'un parking en moyenne par département"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    return fig

def courbe():
    fig = px.line(
        x=[0.17 + i*0.01 for i in range(5)], y=[(utils.augmentation(0.17 + i*0.01)-1)*100 for i in range(5)], # replace with your own data source
        title="Evolution du benefice", height=525,
        labels={"x": "Prix du kWh", "y": "Pourcentage d'augmentation du bénéfice par rapport à la proposition de loi"},
    )
    return fig
def courbe_evolution_prix():
    df = utils.dataframes['evolution']
    df = df[df['semestre'] == 'S2']
    df = df[['annee', 'france_electricite']]
    df['france_electricite'] = df['france_electricite']/1000
    df.rename(columns={'france_electricite': 'prix'}, inplace=True)
    df.sort_values(by='annee', inplace=True)
    df = df.set_index('annee')
    fig = px.line(
        df, # replace with your own data source
        title="Evolution du prix du kWh en France", height=525,
        labels={"index": "Année", "prix": "Prix du kWh"},
    )
    return fig
app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.H4(children="Etude du projet de loi : Loi Climat"),
                html.P(
                    id="description",
                    children="Dans ce rapport on va s'intéresser à la popularité de la nouvelle loi Climat qui à été voté il y a une semaine et en particulier à une des mesures discutés qui impose l'installation de panneaux à tous les parkings de plus de 400 places.",
                ),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="container",
                    children=[
                        html.H1(
                            id="container-title",
                            children="Opinions sur le projet de loi",
                        ),
                        pie_opinions(),
                        dcc.Graph(id="word-cloud-loi", figure=word_cloud())
                    ]
                ),
                html.Div(
                    id='graph-container',
                    children=[
                        html.H2(
                            id="compare-title",
                            children="Comparaison de l'éolien et du solaire",
                        ),
                        dcc.RadioItems(
                            id='option', 
                            options=["Polarité", "Polarité avec subjectivité"],
                            value="type-comparaison",
                            inline=True
                        ),
                        dcc.Graph(id="comparaison-graph"),
                    ]
                ),
                html.Div(
                    id='graph-container',
                    children=[
                        html.H1(
                            id="section-title",
                            children="Analyse de la propostion de loi sur les panneaux solaires de parking",
                        ),
                        dcc.RadioItems(
                            id='option_france', 
                            options=["Localisation des parkings","Rayonnement moyen par région", "Prix de la mise en place de la loi","Prix de l'énergie engendrée par les parkings par département", "Prix de l'énergie engendrée par une place de parking par département","Repartition des plus grands bénéficiaires"],
                            value="rayonnement_moyen_region",
                            inline=True
                        ),
                        dcc.Graph(id="graph-france"),
                    ]
                ),
                html.Div(
                    id='graph-container',
                    children=[
                        html.H2(
                            id="section-title",
                            children="Variations du bénéfice entre la proposition de loi et une selection des parkings par rapport à leur potentiel",
                        ),
                        html.P(
                            id="observation",
                            children="Observons d'abord l'évolution du prix du kWh en France",
                        ),

                        dcc.Graph(id="variations", figure=courbe_evolution_prix()),
                        html.P(
                            id="texte_courbe_variations",
                            children="On remarque que le prix du kWh a augmenté de 50% en 10 ans. On va donc comparer le bénéfice qu'on peut avoir si au lieu d'appliquer la loi on effectue une selection de parkings par rapport à leur potentiel.",
                        ),
                        dcc.Graph(id="courbe_variations", figure=courbe()),
                    ]
                )
            ]
        ),
    ]
)


@app.callback(
    Output("comparaison-graph", "figure"), 
    Input("option", "value"))
def graph_comparaison(option):
    if option == "Polarité":
        return histogramme_opinions_polarite()
    else:
        return histogramme_opinions_polarite_subjectivite()
        

@app.callback(
    Output("graph-france", "figure"), 
    Input("option_france", "value"))
def graph_france(option_france):
    if option_france == "Prix de l'énergie engendrée par les parkings par département":
        return display_choropleth()
    elif option_france == "Rayonnement moyen par région":
        return display_choropleth2()
    elif option_france == "Prix de la mise en place de la loi":
        return display_choropleth3()
    elif option_france == "Prix de l'énergie engendrée par une place de parking par département":
        return display_choropleth4()
    elif option_france == "Repartition des plus grands bénéficiaires":
        return camembert_production_elec()
    else:
        return visu_map()


if __name__ == "__main__":
    app.run_server(debug=True)
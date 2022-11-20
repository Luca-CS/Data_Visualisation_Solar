from textblob import TextBlob
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import json
import matplotlib.pyplot as plt
from vars import ENV


def tweets_to_dataframe(data):
    dir_name = ENV['tweets'][data]
    onlyfiles = [f for f in listdir(dir_name) if isfile(join(dir_name, f))]
    df = pd.DataFrame(columns=['id', 'text', 'date'])
    for file in onlyfiles:
        with open(dir_name+"/" + file, 'r', encoding='utf-8') as f:
            try:
                j = json.load(f)
                id = file.split(".")[0]
                df = df.append(
                    {"id": id, "text": j["text"], "date": j["date"]}, ignore_index=True)
            except:
                pass
    df['polarity'] = df['text'].apply(lambda x: TextBlob(x).sentiment.polarity).astype(float)
    df['subjectivity'] = df['text'].apply(lambda x: TextBlob(x).sentiment.subjectivity).astype(float)
    df['avis_global'] = df['polarity'] * (1 - df['subjectivity'])
    df = df[df['polarity'] != 0]
    return df

def polarity(df):
    return df['polarity'].mean() * 100

def subjectivity(df):
    return df['subjectivity'].mean() * 100

def avis_global(df):
    return df['avis_global'].mean() * 100

def statistiques(df):
   return {
        "pour" : df[df['polarity'] > 0].shape[0],
        "contre" : df[df['polarity'] < 0].shape[0],
        "neutre" : df[df['polarity'] == 0].shape[0],
    }



def pieAvis(file): 
    stats = statistiques(tweets_to_dataframe(file))
    plt.pie([stats["pour"], stats["contre"], stats["neutre"]], labels=["Pour", "Contre", "Neutre"], normalize=True)
    plt.show()
def piePolarity(file):  # pie de la polarité
    polarite = polarity(tweets_to_dataframe(file))
    plt.pie([polarite, 100-polarite], labels=["Pour", "Contre"], normalize=True)
    plt.show()
def pieObj(file):  # pie de l'avis global objectif
    avis = avis_global(tweets_to_dataframe(file))
    plt.pie([avis, 100-avis], labels=["Objectivement pour",
            "Objectivement contre"], normalize=True)
    plt.show()

def histogramme(df1, df2):
    polarite1 = polarity(df1)/100
    polarite2 = polarity(df2)/100
    print("polarite",polarite1, polarite2)

    plt.bar(["Solaire", "Eolien"], [polarite1, polarite2])
    plt.show()

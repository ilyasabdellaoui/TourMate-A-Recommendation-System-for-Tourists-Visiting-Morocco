# Importation des librairies nécessaires
import numpy as np
import sqlite3
import pandas as pd
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import WordNetLemmatizer
import re

# Connexion à la bd et création du df
cnx = sqlite3.connect('tourmate.db')
df = pd.read_sql_query("SELECT * FROM hotels", cnx)

# Supprimer records avec "rank" ou "adress" vide & dupliqués
df = df.dropna(subset=['rank'])
df = df.dropna(subset=['address'])
df.drop_duplicates(subset='name', keep='first', inplace=True)

# Formater le nom: 21. name -> name
for index, row in df.iterrows():
    df.at[index, "name"] = re.findall('\s(.*)', row["name"])[0]

# Extraction de la ville d'une phrase
def VillesListe():
  return ['rabat', 'casablanca', 'tanger', 'tangier', 'fes', 'fez', 'agadir', 'marrakech', 'dakhla', 'chefchaouen', 'essaouira', 'meknes', 'ouarzazate', 'merzouga']
def format_ville(x):
    villes = VillesListe()
    formatted_x = x.lower().split(" ")[::-1]
    for word in formatted_x:
        if word in villes:
            if word == "tangier":
                word = "tanger"
            elif word == "fez":
                word == "fes"
            return word
    return 1 # Ville non valide

# Extraction et ajout de la ville au df
df['city'] = ""
for index, row in df.iterrows():
    output = format_ville(row["address"])
    if(output == 1):
        df = df.drop(index)
    else:
        df.at[index, "city"] = output

# Extraction des langues d'une phrase
def LanguesListe():
  return ['german', 'spanish', 'chinese', 'malay', 'dutch', 'korean', 'italian', 'japanese', 'catalan', 'english', 'french', 'arabic']
def format_langue(x):
    langues = LanguesListe()
    formatted_x = str(x).lower().replace(",", "").split(" ")
    intersection = list(set(formatted_x).intersection(langues))
    return ' '.join(intersection)

# Extraction et ajout de la ville au df
df['languages'] = ""
for index, row in df.iterrows():
    output = format_langue(row["hotel_styles_languages"])
    if(len(output) == 0):
        df = df.drop(index)
    else:
        df.at[index, "languages"] = output

# Systeme de recommendation
def recommendation(ville=None, langue=None, preference=None, prix=None):
    data = df.copy()
    data = data.set_index(np.arange(data.shape[0]))

    if preference is not None:
      # Formatage de la preference 
      preference = preference.lower()
      preference_tokens = word_tokenize(preference)  
      sw = stopwords.words('english')
      f1_set = {w for w in preference_tokens if not w in sw}
      lemm = WordNetLemmatizer()
      f_set = set()
      for se in f1_set:
          f_set.add(lemm.lemmatize(se))
      # Formatage de la description
      data['description'] = data['description'].str.lower()
      cos=[]
      for i in range(data.shape[0]):
          temp_tokens = word_tokenize(str(data['description'][i]))
          temp1_set = {w for w in temp_tokens if not w in sw}
          temp_set = set()
          for se in temp1_set:
              temp_set.add(lemm.lemmatize(se))
          similaire = temp_set.intersection(f_set)
          cos.append(len(similaire))
      data['similarity'] = cos
      data = data.sort_values(by='similarity', ascending=False)

    if ville is not None: 
      data = data[data['city']==ville.lower()]

    if prix is not None:
      data = data.dropna(subset=['av_price'])
      prix = float(prix)
      data = data[data['av_price'].astype(float) <= prix]

    if langue is not None:
      data = data[data['languages'].str.contains(langue.lower())]

    if preference is None:
      data = data.sort_values(by='rating',ascending=False)
      data['similarity'] = 0

    output_list = data[['name', 'rating', 'address', 'description', 'similarity']].head(5).values.tolist()
    
    return output_list # Retourne Top 5
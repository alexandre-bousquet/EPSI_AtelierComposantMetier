# -*- coding: utf-8 -*-
"""rendu_catégories_regroupées.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C7UsRXnO0vP-U3yJCVU1T6nFKd9DK7Gf
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

df_alim = pd.read_csv('/content/drive/MyDrive/Epsi/Atelier composants métier/Projet/export_alimconfiance@dgal.csv', sep=';')

df_alim.shape

df_alim.head()

df_alim.columns

df_alim[['filtre', 'ods_type_activite']]

df_alim['filtre'] = df_alim['filtre'].fillna('__')

df_comma_filtered = df_alim[df_alim['filtre'].str.contains(',')]

list_categories = list(set(df_comma_filtered['filtre'].values))

unique_categories = []
for cat in list_categories:
  unique_categories.extend([x for x in cat.split(',')])

set(unique_categories)

df_filtered = df_alim[~df_alim['filtre'].str.contains(',')]

list_df_filtered = list(df_filtered['filtre'].values)
list_df_filtered.extend(unique_categories)
list_unique_categories = list(set(list_df_filtered))

list_unique_categories.sort()
list_unique_categories

list_categorie = []

for index, row in df_alim.iterrows():
  if(row["filtre"].__contains__('Poissonnerie')):
    list_categorie.append('Poissonnerie')
    continue
  if(row["filtre"].__contains__('Boucherie')):
    list_categorie.append('Boucherie')
    continue
  if(row["filtre"].__contains__('Fermier')):
    list_categorie.append('Fermier')
    continue
  if(row["filtre"].__contains__('Primeur')):
    list_categorie.append('Primeur')
    continue
  if(row["filtre"].__contains__('Fromagerie')):
    list_categorie.append('Fromagerie')
    continue
  if(row["filtre"].__contains__('Restaurant') or row["filtre"].__contains__('Traiteur')):
    list_categorie.append('Restaurant')
    continue
  if(row["filtre"].__contains__('Chocolatier')):
    list_categorie.append('Chocolatier')
    continue
  if(row["filtre"].__contains__('Libre service')):
    list_categorie.append('Libre service')
    continue
  if(row["filtre"].__contains__('glacier')):
    list_categorie.append('glacier')
    continue
  if(row["filtre"].__contains__('Alimentation générale') or row["filtre"].__contains__('Rayon')):
    list_categorie.append('Libre service')
    continue
  list_categorie.append(row["filtre"])

df_alim['categorie'] = list_categorie
df_alim[['categorie','filtre']]

import matplotlib.pyplot as plt

#set(df_alim['APP_Libelle_activite_etablissement'].values)

from collections import Counter
count = Counter(df_alim['APP_Libelle_activite_etablissement'])

#count.most_common()

count.most_common()[0][1]

list_etab = [x[0] for x in count.most_common() if x[1] > 100]

df_alim = df_alim[df_alim['APP_Libelle_activite_etablissement'].isin(list_etab)].reset_index()

df_alim.to_csv('/content/drive/MyDrive/Epsi/Atelier composants métier/Projet/data_formated.csv', index=False)

df_alim.columns

df_alim.dtypes

from datetime import datetime
import pytz

def convert_to_timestamp(dt):
  date_time_str = dt

  date_time_obj = datetime.fromisoformat(date_time_str)

  timestamp = date_time_obj.timestamp()

  return timestamp

#df_alim['Date_inspection'] = df_alim.apply

list_date = list(df_alim['Date_inspection'].values)

timestamps = []

for dt in list_date:
  timestamp = convert_to_timestamp(dt)
  timestamps.append(timestamp)

df_alim['Date_inspection_timestamp'] = timestamps

df_alim.Date_inspection_timestamp = df_alim.Date_inspection_timestamp.astype(int)

#Labelisation des valeurs

from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()

# Encoder la chaîne de caractère
df_alim['Synthese_eval_sanit'] = label_encoder.fit_transform(df_alim['Synthese_eval_sanit'])

df_alim['categorie'] = label_encoder.fit_transform(df_alim['categorie'])
df_alim['Libelle_commune'] = label_encoder.fit_transform(df_alim['Libelle_commune'])

X = df_alim[['categorie','Libelle_commune', 'Date_inspection_timestamp']]
# X = df_alim[['categorie','Libelle_commune']]
y = df_alim['Synthese_eval_sanit']

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

#Division de notre jeu de données en jeu d'entraînement et de test
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

from sklearn.ensemble import RandomForestClassifier

#Utilisation du Random Forest Classifier pour de la classification
rf_model = RandomForestClassifier(random_state = 100)


rf_model.fit(train_X, train_y)

#On test les performances de notre modèle avec les données de test
results_predicted = rf_model.predict(val_X)

#Validation du modèle
print("Accuracy:",round(accuracy_score(val_y, results_predicted),2))
print("Precision:",round(precision_score(val_y, results_predicted, average='weighted'),2))
print("Recall:",round(recall_score(val_y, results_predicted, average='weighted'),2))
print("F1:",round(f1_score(val_y, results_predicted, average='weighted'),2))
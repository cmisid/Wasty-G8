# -*- coding: utf-8 -*-
# Version 1 : Prédiction du temps de disponibilité en R 
# Version 2 : Traduction en python

## --------------------------------------------------------
# Projet : WASTY
# Groupe 8 : Prédiction et recommandation
# Objectif : La prédiction du temps de disponibilité d'un
# objet
## --------------------------------------------------------


import json
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing
import datetime


# Version 1 : Prédiction du temps de disponibilité en R

# Ouverture de la table annonce et Recovery
# Import des donnees au format json
with open("../../data/Advert/Annonce.json") as data_file:    
    data_advert = json.load(data_file)

with open("../../data/Recovery/Recovery.json") as data_file:
    data_recovery = json.load(data_file)

# Transformation des donnees en dataframe
data_advert = pd.read_json(data_advert)
data_recovery = pd.read_json(data_recovery)

# Fusion des deux tables en fonction de l'id annonce 

df = pd.merge(data_advert, data_recovery, how = 'outer', on = 'id_advert')

# conversion des dates en format A-M-J H:M:S

df['recovery_date'] =  pd.to_datetime(df['recovery_date'], format='%Y-%m-%d %H:%M:%S')

# Suppression des lignes ou la date de récupération n'est pas renseignée
df = df.fillna('')
df = df[df['recovery_date'] != '']
df = df[df['forecast_price'] != '']
df['forecast_price'] = df['forecast_price'].convert_objects(convert_numeric=True)


# Variable a renseigner dans la requete
var_req = ['buy_place',
           'forecast_price',
           'id_sub_category',
           'object_state',
           'quantite',
           'situation',
           'type_place',
           'volume'
           ]

#calcul du temps disponible 
df['available_time'] = df.recovery_date - df.date
df['available_time'] = df['available_time'].dt.total_seconds()

# Entrée : liste des données saisies par l'utilisateur 
# 'buy_place','forecast_price','id_sub_category','object_state',
# 'quantite','situation','type_place','volume'
# Objectif : Prédire la durée de disponibilité d'un objet en 
# fonction des données saisies
# Sortie : Une durée en Jours-Heures-Minutes-Secondes

def available_time_prediction(pu_req):
    # Conversion de certaines donnees en format numerique
    if pu_req[1] != '':
            pu_req[1] = int(pu_req[1])
    if pu_req[2] != '':
            pu_req[2] = int(pu_req[2])
    if pu_req[4] != '':
            pu_req[4] = int(pu_req[4])
            
    # Mise en forme de la requête et suppression des champs a valeur
    # manquante
    X_pred = pd.DataFrame(pu_req).T
    X_pred.columns = var_req
    X_pred = X_pred[X_pred != ''].T.dropna().T

    # Variable necessaire pour entrainer le modele
    var_X_train = list(X_pred.columns)

    # Donnees pour entrainer le modele
    X_train = df[var_X_train]
    #X_train['forecast_price'] = X_train['forecast_price'].convert_objects(convert_numeric=True)

    # Encodage des donnees en facteur numeriques
    le = preprocessing.LabelEncoder()

    # Pour toutes les variables necessaire
    for var in var_X_train:
        # On assigne les strings a des integers
        le.fit(X_train[var])
        # On les transforme dans le X_train
        X_train[var] = list(le.transform(X_train[var]))
        # Et dans le X_pred
        X_pred[var] = list(le.transform(X_pred[var]))

    # Donnees d'entrainement a predire
    Y_train = df['available_time']

    # Modele utilise : RandomForest
    rf = RandomForestRegressor(n_estimators=1000)
    # Entrainement du modele avec les données adequats
    rf.fit(X_train, Y_train)
    # Prediction
    return str(datetime.timedelta(seconds = rf.predict(X_pred).item()))

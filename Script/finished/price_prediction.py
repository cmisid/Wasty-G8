# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 10:34:04 2017

@author: Giovanni
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 08:43:37 2017

@author: Giovanni
"""

## --------------------------------------------------------
# Projet : WASTY DataBase
# Groupe 8 : Prédiction et recommandation
# Objectif : La prédiction des prix
# Par : Giovanni Zanitti - CHRISMANN Céline - QUESNOT Sandy
## --------------------------------------------------------
import json
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing

# Ouverture de la table Annonce 
# Import des donnees au format json
with open('../../data/Advert/Annonce.json') as data_file:    
    data = json.load(data_file)

# Transformation des donnees en dataframe
df = pd.read_json(data)
# Suppression des lignes ou le prix n'est pas renseigne
df = df[df['forecast_price'] != '']
df = df[df['situation'] != 'a donner']


# Variable a renseigner dans la requete
var_req = ['buy_place',
           'id_sub_category',
           'object_state',
           'quantite',
           'type_place',
           'situation',
           'volume']


def price_prediction(pu_req):
     # Si l'utilisateur ne met pas en situation "a donner":
    if (pu_req[5] != 'a donner' or pu_req[5] == ''):
        if pu_req[1] != '':
            pu_req[1] = int(pu_req[1])
        if pu_req[3] != '':
            pu_req[3] = int(pu_req[3])

        # Mise en forme de la requete et suppression des champs a valeur
        # manquante
        X_pred = pd.DataFrame(pu_req).T
        X_pred.columns = var_req

        X_pred = X_pred[X_pred != ''].T.dropna().T

        # Variable necessaire pour entrainer le modele
        var_X_train = list(X_pred.columns)

        # Donnees pour entrainer le modele
        X_train = df[var_X_train]

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
        Y_train = df['forecast_price']
        # Conversion des donnees en numerique
        Y_train = Y_train.convert_objects(convert_numeric=True)

        # Modele utilise : RandomForest
        rf = RandomForestRegressor(n_estimators=1000)
        # Entrainement du modele avec les donnees adequats
        rf.fit(X_train, Y_train)
        prediction = rf.predict(X_pred).item()
        # Prediction
        return [prediction-0.1*prediction, prediction+0.1*prediction]
    else:
        return [0, 0]

